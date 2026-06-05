#!/usr/bin/env bash
# Double-click this file to launch paw.
# macOS will open Terminal and run this script.
# First run installs everything. After that, it just opens the tutorial.

set -euo pipefail

PAW_DIR="$(cd "$(dirname "$0")" && pwd)"
WEB_PORT=8042

clear
printf '\033[0;36m'
cat << 'ART'

        _______________
       /               \
      |  ┌───┐ ┌───┐  |
      |  │ ● │ │ ● │  |
      |  └───┘ └───┘  |
      |      ___      |
      |     /   \     |
      |    | === |    |
       \   \_____/   /
        \___________/
         /    |    \
        *     *     *

     p a w
     Personal Agent Workflows

ART
printf '\033[0m'

# ── Check if first run ─────────────────────────────────

FIRST_RUN=false
if ! command -v python3 &>/dev/null; then
    FIRST_RUN=true
fi
if [ ! -f "$HOME/.claude/settings.json" ] || ! grep -q "git_safety.py" "$HOME/.claude/settings.json" 2>/dev/null; then
    FIRST_RUN=true
fi

if [ "$FIRST_RUN" = true ]; then
    printf '\033[1m  First time? Let'\''s get you set up.\033[0m\n\n'
    "$PAW_DIR/setup" --yes
    printf '\n'
fi

# ── Launch web tutorial ────────────────────────────────

printf '\033[0;36m  Starting tutorial server...\033[0m\n'

# Kill any existing paw server on this port
lsof -ti :"$WEB_PORT" 2>/dev/null | xargs kill 2>/dev/null || true

python3 -m http.server "$WEB_PORT" --directory "$PAW_DIR" &>/dev/null &
SERVER_PID=$!
sleep 1

if kill -0 "$SERVER_PID" 2>/dev/null; then
    open "http://localhost:${WEB_PORT}/tutorial.html"
    printf '\033[0;32m  Tutorial opened in your browser.\033[0m\n\n'
    printf '\033[2m  Server: http://localhost:%s/tutorial.html\n' "$WEB_PORT"
    printf '  Press Ctrl+C or close this window to stop.\033[0m\n\n'
    wait "$SERVER_PID"
else
    printf '\033[0;31m  Failed to start server.\033[0m\n'
    printf '  Try manually: python3 -m http.server %s --directory %s\n' "$WEB_PORT" "$PAW_DIR"
fi
