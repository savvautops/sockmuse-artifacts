#!/usr/bin/env python3
"""Snake arena: Jev (OpenCode Zen, free) vs Laya (nucbox RTX 3060) vs Jev-style Qwen (LM Studio) play snake.
Each move, the backend gets game state + a direction question and picks a move.
Records every step to matches/<ts>.json for the dashboard replay.
"""
import json, os, random, re, sys, time, threading, urllib.request
from datetime import datetime

GRID = 12
DIRS = {"up": (0, -1), "down": (0, 1), "left": (-1, 0), "right": (1, 0)}
REVERSE = {"up": "down", "down": "up", "left": "right", "right": "left"}
ZEN_URL = "https://opencode.ai/zen/v1/systemone"
LAYA_URL = "https://nucbox-m7-1.taila7272b.ts.net:9479/api/predict"
QWEN_URL = "https://nucbox-m7-1.taila7272b.ts.net:9480/v1/chat/completions"
QWEN_MODEL = "jev-style-qwen3.5-2b-decision-v2"
BACKENDS = ["jev", "laya", "qwen"]
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"}

_tunnel_opener = None
def tunnel_opener():
    global _tunnel_opener
    if _tunnel_opener is None:
        proxy = re.sub(r":\d+$", ":3130", os.environ["HTTPS_PROXY"])
        _tunnel_opener = urllib.request.build_opener(
            urllib.request.ProxyHandler({"http": proxy, "https": proxy}))
    return _tunnel_opener

def post_json(url, payload, timeout=45, via_tunnel=False):
    data = json.dumps(payload).encode()
    headers = dict(UA); headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    t = time.time()
    try:
        opener = tunnel_opener() if via_tunnel else urllib.request.build_opener()
        with opener.open(req, timeout=timeout) as r:
            return {"ok": True, "ms": int((time.time() - t) * 1000),
                    "http": r.status, "body": json.load(r)}
    except Exception as e:
        return {"ok": False, "ms": int((time.time() - t) * 1000),
                "error": str(e)[:160]}

def parse_choice(body):
    """Tolerant choice parser for Zen and Laya response shapes."""
    ans = (body.get("answers") or (body.get("result") or {}).get("answers") or {})
    q = ans.get("move") or next(iter(ans.values()), {})
    c = q.get("choice")
    if c in DIRS:
        return c, q.get("confidence")
    probs = q.get("probabilities") or {}
    if probs:
        best = max(probs, key=lambda k: probs[k])
        if best in DIRS:
            return best, probs[best]
    return None, None

QUESTION_INSTRUCTIONS = (
    "You are playing Snake. The state's 'options' field rates each direction: "
    "pick a SAFE direction, preferring ones that move toward the food. "
    "Never pick ILLEGAL or BLOCKED directions.")

def ask_jev(g):
    payload = {
        "model": "jev-1.13-free",
        "state": g.state_str(),
        "questions": {"move": {
            "type": "choice",
            "instructions": QUESTION_INSTRUCTIONS,
            "criteria": {
                "up": "move up (decrease y)",
                "down": "move down (increase y)",
                "left": "move left (decrease x)",
                "right": "move right (increase x)",
            },
        }},
    }
    return post_json(ZEN_URL, payload)

def ask_laya(g):
    payload = {
        "state": g.state_str(),
        "questions": {"move": {
            "type": "choice",
            "instructions": QUESTION_INSTRUCTIONS,
            "criteria": {
                "up": "move up (decrease y)",
                "down": "move down (increase y)",
                "left": "move left (decrease x)",
                "right": "move right (increase x)",
            },
        }},
    }
    return post_json(LAYA_URL, payload, via_tunnel=True)

QWEN_SYSTEM = ("You are playing Snake on a 12x12 grid. Reply with exactly one word, "
               "no explanation: up, down, left, or right.")

def qwen_prose(g):
    hx, hy = g.snake[0]
    opts = g.analyze()
    return (f"Snake game, 12x12 board. Your head is at ({hx},{hy}), moving {g.dir}, "
            f"body length {len(g.snake)}. Food is at {tuple(g.food)}. "
            f"Your options: " + "; ".join(f"{d}: {o}" for d, o in opts.items()) + ".")

def parse_qwen(body):
    try:
        content = body["choices"][0]["message"]["content"] or ""
    except (KeyError, IndexError, TypeError):
        return None
    words = re.findall(r"\b(up|down|left|right)\b", content.lower())
    return words[-1] if words else None

def ask_qwen(g):
    payload = {
        "model": QWEN_MODEL,
        "messages": [
            {"role": "system", "content": QWEN_SYSTEM},
            {"role": "user", "content": qwen_prose(g) + " Your move:"},
        ],
        "max_tokens": 10,
        "temperature": 0,
    }
    r = post_json(QWEN_URL, payload, via_tunnel=True)
    if r["ok"]:
        r["qwen_choice"] = parse_qwen(r["body"])
    return r

class Game:
    def __init__(self, seed, grid=GRID):
        rng = random.Random(seed)
        self.n = grid
        cx, cy = self.n // 2, self.n // 2
        self.snake = [[cx, cy], [cx - 1, cy], [cx - 2, cy]]
        self.dir = "right"
        self.rng = rng
        self.score = 0
        self.steps = 0
        self.alive = True
        self.death = None
        self.food = self._place_food()

    def _place_food(self):
        free = [[x, y] for x in range(self.n) for y in range(self.n)
                if [x, y] not in self.snake]
        return self.rng.choice(free) if free else None

    def analyze(self):
        """Per-direction safety/toward-food analysis, computed in code so the
        model decides on clean facts instead of parsing raw coordinates."""
        out = {}
        hx, hy = self.snake[0]
        fx, fy = self.food if self.food else (hx, hy)
        cur_dist = abs(hx - fx) + abs(hy - fy)
        for d, (dx, dy) in DIRS.items():
            nx, ny = hx + dx, hy + dy
            if d == REVERSE[self.dir]:
                out[d] = "ILLEGAL: reverse of current direction"
            elif nx < 0 or nx >= self.n or ny < 0 or ny >= self.n:
                out[d] = "BLOCKED: wall"
            elif [nx, ny] in self.snake:
                out[d] = "BLOCKED: your own body"
            else:
                toward = (abs(nx - fx) + abs(ny - fy)) < cur_dist
                out[d] = "SAFE, moves toward food" if toward else "SAFE, moves away from food"
        return out

    def state_str(self):
        return json.dumps({
            "grid": self.n,
            "head": self.snake[0],
            "length": len(self.snake),
            "food": self.food,
            "direction": self.dir,
            "score": self.score,
            "options": self.analyze(),
        })

    def step(self, want):
        d = want if (want in DIRS and want != REVERSE[self.dir]) else self.dir
        self.dir = d
        dx, dy = DIRS[d]
        head = [self.snake[0][0] + dx, self.snake[0][1] + dy]
        if head[0] < 0 or head[0] >= self.n or head[1] < 0 or head[1] >= self.n:
            self.alive = False
            self.death = "wall"
            return
        if head in self.snake:
            self.alive = False
            self.death = "self"
            return
        self.snake.insert(0, head)
        self.steps += 1
        if head == self.food:
            self.score += 1
            self.food = self._place_food()
            if self.food is None:
                self.alive = False  # filled the board: legendary
                self.death = "board_full"
        else:
            self.snake.pop()

    def snapshot(self, lat_ms, err=None):
        return {"snake": [s[:] for s in self.snake], "food": self.food[:] if self.food else None,
                "dir": self.dir, "score": self.score, "steps": self.steps,
                "alive": self.alive, "lat_ms": lat_ms, "err": err}

def play_game(backend, seed, max_moves, ask):
    g = Game(seed)
    frames = [g.snapshot(0)]
    lats, errors = [], 0
    while g.alive and g.steps < max_moves:
        r = ask(g)
        if not r["ok"]:
            time.sleep(1)  # one retry before giving up on this move
            r = ask(g)
        if r["ok"]:
            if backend == "qwen":
                choice = r.get("qwen_choice")
            else:
                choice, _ = parse_choice(r["body"])
            lats.append(r["ms"])
            g.step(choice)
            frames.append(g.snapshot(r["ms"]))
        else:
            errors += 1
            g.step(None)  # keep going straight on backend error
            frames.append(g.snapshot(r["ms"], err=r["error"]))
    return {"backend": backend, "seed": seed, "score": g.score, "steps": g.steps,
            "alive": g.alive, "death": g.death or ("max_moves" if g.steps >= max_moves else None),
            "frames": frames,
            "lat": {"n": len(lats),
                    "avg_ms": round(sum(lats) / len(lats), 1) if lats else 0,
                    "p50_ms": sorted(lats)[len(lats) // 2] if lats else 0,
                    "p95_ms": sorted(lats)[int(len(lats) * 0.95)] if lats else 0,
                    "max_ms": max(lats) if lats else 0},
            "errors": errors}

def main():
    games = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    max_moves = int(sys.argv[2]) if len(sys.argv) > 2 else 400
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    outdir = os.path.expanduser("~/workspace/snake-arena/matches")
    os.makedirs(outdir, exist_ok=True)
    results = {}
    base_seed = int(time.time()) % 100000

    def run(which, ask):
        gs = []
        for i in range(games):
            print(f"[{which}] game {i+1}/{games} ...", flush=True)
            gs.append(play_game(which, base_seed + i, max_moves, ask))
            print(f"[{which}] game {i+1}: score={gs[-1]['score']} steps={gs[-1]['steps']} "
                  f"avg_lat={gs[-1]['lat']['avg_ms']}ms errors={gs[-1]['errors']}", flush=True)
        results[which] = gs

    ts = [threading.Thread(target=run, args=("jev", ask_jev)),
          threading.Thread(target=run, args=("laya", ask_laya)),
          threading.Thread(target=run, args=("qwen", ask_qwen))]
    [t.start() for t in ts]
    [t.join() for t in ts]
    path = os.path.join(outdir, f"{stamp}.json")
    json.dump({"stamp": stamp, "grid": GRID,
               "models": {"jev": "jev-1.13-free", "laya": "laya-rl-agent",
                          "qwen": QWEN_MODEL},
               "results": results},
              open(path, "w"))
    print("saved", path)

if __name__ == "__main__":
    main()
