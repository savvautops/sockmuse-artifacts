#!/usr/bin/env python3
"""Snake Arena live server.

Serves the dashboard UI and runs live snake games: every move of every
enabled player is one real model call to that player's configured endpoint.
Endpoints, models and instructions are editable from the dashboard and
persisted to config.json. Pause halts model calls; finished games are saved
to matches/ for replay.

API:
  GET  /                        -> dashboard HTML
  GET  /api/config              -> player config
  POST /api/config              -> save player config
  GET  /api/recordings          -> recorded match summaries (newest first)
  GET  /api/recordings/<file>   -> full recorded match
  GET  /api/games               -> live games (newest first)
  POST /api/games               -> start live game {players:[ids], grid, max_moves}
  GET  /api/games/<id>          -> live game state
  POST /api/games/<id>/pause|resume|stop
"""
import json
import os
import re
import sys
import threading
import time
import traceback
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import play
from play import (
    DIRS, Game, QWEN_SYSTEM, QUESTION_INSTRUCTIONS,
    parse_choice, parse_qwen, post_json,
)

PORT = int(os.environ.get("ARENA_PORT", "8080"))
CFG_PATH = os.path.join(HERE, "config.json")
MATCH_DIR = os.path.join(HERE, "matches")
HTML_PATH = os.path.join(HERE, "arena.html")
MAX_CONSEC_ERRORS = 5

CRITERIA = {
    "up": "move up (decrease y)",
    "down": "move down (increase y)",
    "left": "move left (decrease x)",
    "right": "move right (increase x)",
}


def default_config():
    return {
        "grid": 12,
        "max_moves": 400,
        "players": [
            {"id": "jev", "label": "Jev", "color": "#4ade80", "tag": "OpenCode Zen",
             "enabled": True, "protocol": "systemone",
             "url": "https://opencode.ai/zen/v1/systemone",
             "model": "jev-1.13-free", "via_tunnel": False,
             "instructions": QUESTION_INSTRUCTIONS},
            {"id": "laya", "label": "Laya", "color": "#f5a623", "tag": "nucbox",
             "enabled": True, "protocol": "systemone",
             "url": "https://nucbox-m7-1.taila7272b.ts.net:9479/api/predict",
             "model": "laya-rl-agent", "via_tunnel": True,
             "instructions": QUESTION_INSTRUCTIONS},
            {"id": "qwen", "label": "Qwen", "color": "#a78bfa", "tag": "LM Studio",
             "enabled": True, "protocol": "openai",
             "url": "https://nucbox-m7-1.taila7272b.ts.net:9480/v1/chat/completions",
             "model": "jev-style-qwen3.5-2b-decision-v2", "via_tunnel": True,
             "instructions": QWEN_SYSTEM},
        ],
    }


def load_config():
    if os.path.exists(CFG_PATH):
        try:
            cfg = json.load(open(CFG_PATH))
            if isinstance(cfg.get("players"), list) and cfg["players"]:
                return cfg
        except Exception:
            pass
    cfg = default_config()
    save_config(cfg)
    return cfg


def save_config(cfg):
    json.dump(cfg, open(CFG_PATH, "w"), indent=2)


def validate_config(data):
    if not isinstance(data, dict):
        return None, "config must be an object"
    players = data.get("players")
    if not isinstance(players, list) or not players:
        return None, "need at least one player"
    seen = set()
    for p in players:
        pid = p.get("id", "")
        if not re.fullmatch(r"[a-z0-9_-]{1,24}", pid) or pid in seen:
            return None, f"bad player id: {pid!r}"
        seen.add(pid)
        if p.get("protocol") not in ("systemone", "openai"):
            return None, f"bad protocol for {pid}"
        url = p.get("url", "")
        if not re.match(r"^https?://", url) or len(url) > 500:
            return None, f"bad url for {pid}"
        if not p.get("model") or len(p["model"]) > 200:
            return None, f"bad model for {pid}"
        for k in ("label", "tag", "color", "instructions"):
            p[k] = str(p.get(k, ""))[:2000]
        p["enabled"] = bool(p.get("enabled"))
        p["via_tunnel"] = bool(p.get("via_tunnel"))
    try:
        grid = int(data.get("grid", 12))
        max_moves = int(data.get("max_moves", 400))
    except (TypeError, ValueError):
        return None, "grid/max_moves must be numbers"
    if not 6 <= grid <= 24:
        return None, "grid must be 6-24"
    if not 1 <= max_moves <= 2000:
        return None, "max_moves must be 1-2000"
    return {"grid": grid, "max_moves": max_moves, "players": players}, None


def ask_player(cfg, g):
    """One model call for one move. Returns (response_dict, direction|None)."""
    grid = g.n
    if cfg.get("protocol") == "openai":
        system = cfg.get("instructions", "").replace("{grid}", str(grid))
        hx, hy = g.snake[0]
        opts = g.analyze()
        user = (f"Snake game, {grid}x{grid} board. Your head is at ({hx},{hy}), "
                f"moving {g.dir}, body length {len(g.snake)}. "
                f"Food is at {tuple(g.food)}. Your options: " +
                "; ".join(f"{d}: {o}" for d, o in opts.items()) +
                ". Your move:")
        payload = {"model": cfg["model"],
                   "messages": [{"role": "system", "content": system},
                                {"role": "user", "content": user}],
                   "max_tokens": 10, "temperature": 0}
        r = post_json(cfg["url"], payload, timeout=60,
                      via_tunnel=cfg.get("via_tunnel", False))
        choice = parse_qwen(r["body"]) if r["ok"] else None
        return r, choice
    payload = {"model": cfg["model"], "state": g.state_str(),
               "questions": {"move": {"type": "choice",
                                      "instructions": cfg.get("instructions", ""),
                                      "criteria": CRITERIA}}}
    r = post_json(cfg["url"], payload, timeout=60,
                  via_tunnel=cfg.get("via_tunnel", False))
    choice, _ = parse_choice(r["body"]) if r["ok"] else (None, None)
    return r, choice


GAMES = {}
GAMES_LOCK = threading.Lock()


def player_loop(game, pid):
    p = game["players"][pid]
    cfg = p["cfg"]
    g = Game(seed=game["seed"] + p["idx"], grid=game["grid"])
    frames = [g.snapshot(0)]
    consec_err = 0
    while g.alive and g.steps < game["max_moves"]:
        if game["stop_evt"].is_set():
            break
        game["pause_evt"].wait()  # paused: no model calls happen here
        if game["stop_evt"].is_set():
            break
        try:
            r, choice = ask_player(cfg, g)
            if not r.get("ok") or choice not in DIRS:
                time.sleep(1)  # one retry before counting it as an error
                r, choice = ask_player(cfg, g)
        except Exception as e:  # never let one bad call kill the loop
            r = {"ok": False, "ms": 0, "error": f"local: {e}"[:160]}
            choice = None
        with game["lock"]:
            p["calls"] += 1
            if r.get("ok") and choice in DIRS:
                consec_err = 0
                p["lats"].append(r["ms"])
                g.step(choice)
                frames.append(g.snapshot(r["ms"]))
            else:
                consec_err += 1
                p["errors"] += 1
                err = (r.get("error") or "bad/no choice")[:160]
                frames.append(g.snapshot(r.get("ms", 0), err=err))
                p["last_error"] = err
                if consec_err >= MAX_CONSEC_ERRORS:
                    p["failed"] = f"stopped after {MAX_CONSEC_ERRORS} consecutive errors: {err}"
                    break
                g.step(None)  # drift straight on a transient error
            p["frames"] = frames
            p["score"], p["steps"], p["alive"] = g.score, g.steps, g.alive
    with game["lock"]:
        p["done"] = True
        if game["stop_evt"].is_set() and not p.get("failed"):
            p["death"] = "stopped"
        else:
            p["death"] = g.death or ("max_moves" if g.steps >= game["max_moves"] else None)
        p["frames"] = frames
    maybe_finish(game)


def maybe_finish(game):
    with game["lock"]:
        if game.get("saved") or not all(p["done"] for p in game["players"].values()):
            return
        game["saved"] = True
    results, models = {}, {}
    for pid, p in game["players"].items():
        lats = p["lats"]
        sl = sorted(lats)
        results[pid] = [{
            "backend": pid, "seed": game["seed"] + p["idx"],
            "score": p["score"], "steps": p["steps"], "alive": p["alive"],
            "death": p["death"], "frames": p["frames"],
            "lat": {"n": len(lats),
                    "avg_ms": round(sum(lats) / len(lats), 1) if lats else 0,
                    "p50_ms": sl[len(sl) // 2] if sl else 0,
                    "p95_ms": sl[int(len(sl) * 0.95)] if sl else 0,
                    "max_ms": max(lats) if lats else 0},
            "errors": p["errors"]}]
        models[pid] = p["cfg"]["model"]
    doc = {"stamp": game["stamp"], "grid": game["grid"], "models": models,
           "live": True, "results": results}
    os.makedirs(MATCH_DIR, exist_ok=True)
    with open(os.path.join(MATCH_DIR, game["file"]), "w") as f:
        json.dump(doc, f)


def game_status(game):
    if all(p["done"] for p in game["players"].values()):
        return "finished"
    if game["stop_evt"].is_set():
        return "stopping"
    if not game["pause_evt"].is_set():
        return "paused"
    return "running"


def game_public(game):
    players = {}
    for pid, p in game["players"].items():
        lats = p["lats"]
        players[pid] = {
            "label": p["cfg"]["label"], "color": p["cfg"]["color"],
            "tag": p["cfg"].get("tag", ""), "model": p["cfg"]["model"],
            "frames": p["frames"], "score": p["score"], "steps": p["steps"],
            "alive": p["alive"], "death": p["death"], "done": p["done"],
            "calls": p["calls"], "errors": p["errors"],
            "failed": p.get("failed"), "last_error": p.get("last_error"),
            "avg_ms": round(sum(lats) / len(lats), 1) if lats else 0,
        }
    return {"id": game["id"], "stamp": game["stamp"], "grid": game["grid"],
            "max_moves": game["max_moves"], "status": game_status(game),
            "started": game["started"], "players": players}


def list_recordings():
    out = []
    if not os.path.isdir(MATCH_DIR):
        return out
    for name in sorted(os.listdir(MATCH_DIR), reverse=True):
        if not name.endswith(".json"):
            continue
        try:
            doc = json.load(open(os.path.join(MATCH_DIR, name)))
        except Exception:
            continue
        players = {}
        for pid, games in (doc.get("results") or {}).items():
            g0 = games[0] if games else {}
            players[pid] = {"score": g0.get("score", 0), "steps": g0.get("steps", 0),
                            "death": g0.get("death"), "errors": g0.get("errors", 0),
                            "model": (doc.get("models") or {}).get(pid, "")}
        out.append({"file": name, "stamp": doc.get("stamp", name[:-5]),
                    "grid": doc.get("grid", 12), "live": bool(doc.get("live")),
                    "players": players})
    return out


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        sys.stderr.write(f"[arena] {self.address_string()} {fmt % args}\n")

    def _send(self, body, ctype, code=200):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _json(self, obj, code=200):
        self._send(json.dumps(obj).encode(), "application/json", code)

    def _file(self, path, ctype):
        try:
            with open(path, "rb") as f:
                self._send(f.read(), ctype)
        except FileNotFoundError:
            self._json({"error": "not found"}, 404)

    def do_GET(self):
        try:
            u = urlparse(self.path)
            if u.path == "/":
                return self._file(HTML_PATH, "text/html; charset=utf-8")
            if u.path == "/api/config":
                return self._json(load_config())
            if u.path == "/api/recordings":
                return self._json(list_recordings())
            if u.path.startswith("/api/recordings/"):
                name = u.path.rsplit("/", 1)[1]
                if not re.fullmatch(r"[\w\-. ]+\.json", name):
                    return self._json({"error": "bad name"}, 400)
                return self._file(os.path.join(MATCH_DIR, name), "application/json")
            if u.path == "/api/games":
                with GAMES_LOCK:
                    games = [game_public(g) for g in
                             sorted(GAMES.values(), key=lambda g: g["started"], reverse=True)]
                return self._json(games)
            parts = u.path.strip("/").split("/")
            if len(parts) == 3 and parts[0] == "api" and parts[1] == "games":
                with GAMES_LOCK:
                    game = GAMES.get(parts[2])
                if not game:
                    return self._json({"error": "no such game"}, 404)
                return self._json(game_public(game))
            return self._json({"error": "not found"}, 404)
        except BrokenPipeError:
            pass
        except Exception:
            traceback.print_exc()
            self._json({"error": "server error"}, 500)

    def do_POST(self):
        try:
            u = urlparse(self.path)
            try:
                length = int(self.headers.get("Content-Length", 0))
            except ValueError:
                length = 0
            try:
                data = json.loads(self.rfile.read(length) or b"{}")
            except json.JSONDecodeError:
                return self._json({"error": "bad json"}, 400)

            if u.path == "/api/config":
                cfg, err = validate_config(data)
                if err:
                    return self._json({"error": err}, 400)
                save_config(cfg)
                return self._json({"ok": True})

            if u.path == "/api/games":
                return self._start_game(data)

            parts = u.path.strip("/").split("/")
            if len(parts) == 4 and parts[0] == "api" and parts[1] == "games":
                return self._game_action(parts[2], parts[3])
            return self._json({"error": "not found"}, 404)
        except BrokenPipeError:
            pass
        except Exception:
            traceback.print_exc()
            self._json({"error": "server error"}, 500)

    def _start_game(self, data):
        cfg = load_config()
        by_id = {p["id"]: p for p in cfg["players"]}
        ids = data.get("players") if isinstance(data.get("players"), list) else \
            [p["id"] for p in cfg["players"] if p["enabled"]]
        ids = [i for i in ids if i in by_id]
        if not ids:
            return self._json({"error": "no valid players selected"}, 400)
        try:
            grid = int(data.get("grid", cfg["grid"]))
            max_moves = int(data.get("max_moves", cfg["max_moves"]))
        except (TypeError, ValueError):
            return self._json({"error": "grid/max_moves must be numbers"}, 400)
        if not 6 <= grid <= 24 or not 1 <= max_moves <= 2000:
            return self._json({"error": "grid 6-24, max_moves 1-2000"}, 400)
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        gid = stamp + "-" + os.urandom(3).hex()
        game = {
            "id": gid, "stamp": stamp, "file": f"{stamp}-{gid[-6:]}.json",
            "grid": grid, "max_moves": max_moves,
            "seed": int(time.time()) % 100000,
            "started": time.time(), "saved": False,
            "pause_evt": threading.Event(), "stop_evt": threading.Event(),
            "lock": threading.Lock(), "players": {},
        }
        game["pause_evt"].set()
        for idx, pid in enumerate(ids):
            game["players"][pid] = {
                "cfg": dict(by_id[pid]), "idx": idx,
                "frames": [], "score": 0, "steps": 0, "alive": True,
                "death": None, "done": False, "calls": 0, "errors": 0,
                "lats": [], "failed": None, "last_error": None,
            }
        threads = [threading.Thread(target=player_loop, args=(game, pid),
                                     daemon=True, name=f"arena-{gid}-{pid}")
                   for pid in ids]
        with GAMES_LOCK:
            GAMES[gid] = game
        for t in threads:
            t.start()
        return self._json({"ok": True, "id": gid})

    def _game_action(self, gid, action):
        with GAMES_LOCK:
            game = GAMES.get(gid)
        if not game:
            return self._json({"error": "no such game"}, 404)
        if action == "pause":
            game["pause_evt"].clear()
        elif action == "resume":
            game["pause_evt"].set()
        elif action == "stop":
            game["stop_evt"].set()
            game["pause_evt"].set()  # unblock so threads can exit
        else:
            return self._json({"error": "unknown action"}, 400)
        return self._json({"ok": True, "status": game_status(game)})


def main():
    load_config()  # ensure config.json exists
    os.makedirs(MATCH_DIR, exist_ok=True)
    srv = ThreadingHTTPServer((os.environ.get("ARENA_HOST", "127.0.0.1"), PORT), Handler)
    print(f"[arena] serving on {os.environ.get("ARENA_HOST", "127.0.0.1")}:{PORT}", flush=True)
    srv.serve_forever()


if __name__ == "__main__":
    main()
