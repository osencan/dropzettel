#!/bin/bash
# Dropzettel runner, for launchd or manual use:  run.sh [process|digest|status|init] ...
# launchd starts with a bare environment, so put the usual tool locations on PATH
# (python, claude, pdftotext, tesseract, yt-dlp).
DIR="$(cd "$(dirname "$0")" && pwd)"
export PATH="/opt/homebrew/bin:/usr/local/bin:$HOME/.local/bin:/usr/bin:/bin:$PATH"
PY="$DIR/.venv/bin/python3"
[ -x "$PY" ] || PY="python3"
[ $# -eq 0 ] && set -- process
# When launchd fires because a file just landed, give the sync client time to finish writing it.
if [ -n "$DROPZETTEL_FROM_LAUNCHD" ]; then
  case " $* " in *" process "*) sleep 30 ;; esac
fi
exec "$PY" "$DIR/dropzettel.py" "$@"
