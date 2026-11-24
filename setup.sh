#!/bin/bash
# Dropzettel setup: creates a Python environment, then runs the setup wizard.
#   ./setup.sh                 interactive
#   ./setup.sh --help          all options (everything can be passed as flags)
set -e
DIR="$(cd "$(dirname "$0")" && pwd)"
export PATH="/opt/homebrew/bin:/usr/local/bin:$HOME/.local/bin:$PATH"
if [ "$(uname)" != "Darwin" ]; then
  echo "Note: the background jobs and the phone shortcut need macOS. The processor itself runs anywhere."
fi
command -v python3 >/dev/null || { echo "python3 not found. Install Python 3.10 or newer first."; exit 1; }
if [ ! -x "$DIR/.venv/bin/python3" ]; then
  echo "Creating Python environment in .venv ..."
  python3 -m venv "$DIR/.venv"
fi
"$DIR/.venv/bin/python3" -m pip install --quiet --disable-pip-version-check -r "$DIR/requirements.txt"
exec "$DIR/.venv/bin/python3" "$DIR/scripts/setup_wizard.py" "$@"
