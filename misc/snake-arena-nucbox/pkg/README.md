# Snake Arena - nucbox install

Live dashboard for testing how AI models play Snake. Each move is a real model call.

## What's here
- `server.py` - game engine + API (Python 3, stdlib only, no pip packages needed)
- `arena.html` - the dashboard UI
- `play.py` - game logic (imported by server.py)
- `config.json` - players, endpoints, instructions, board size
- `start-nucbox.sh` - launcher

## Setup (for the implementing agent)
1. Unzip anywhere on the nucbox, e.g. `~/snake-arena/`
2. `python3 --version` (needs 3.8+; stdlib only, nothing to install)
3. Run: `./start-nucbox.sh` (or `ARENA_HOST=0.0.0.0 python3 server.py`)
4. Open on the phone (on Tailscale): `http://<nucbox-tailnet-ip>:8080/arena.html`

## Notes
- `ARENA_HOST=0.0.0.0` is required so the phone can reach it; without it the
  server only listens on localhost.
- `config.json` holds the three players (Jev, Laya, Qwen) with their Tailscale
  endpoints and per-model instructions. Editable live in the dashboard UI.
- Match recordings save to `matches/` next to server.py.
- Pause halts new model calls (one in-flight call may finish). Reset starts a
  brand-new game. Leaving the page open costs nothing; calls happen only while
  a started game is running.
