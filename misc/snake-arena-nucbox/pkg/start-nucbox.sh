#!/bin/bash
# Snake Arena - nucbox launcher. Phone reaches this over Tailscale.
cd "$(dirname "$0")"
export ARENA_HOST=0.0.0.0
export ARENA_PORT=8080
python3 server.py
