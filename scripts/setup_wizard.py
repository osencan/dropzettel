#!/usr/bin/env python3
"""Dropzettel setup wizard. Run through ./setup.sh (which prepares the Python environment).

Asks where things live, writes config.json, prepares the vault, builds the phone shortcut and,
only if you say yes, installs the two background jobs. Every answer can be given as a flag,
so the whole thing can run unattended:

    ./setup.sh --sync folder --home ~/Dropzettel --vault ~/Vault --about "..." --jobs no --yes
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

CODE = Path(__file__).resolve().parent.parent
LAUNCH_AGENTS = Path.home() / "Library" / "LaunchAgents"
JOBS = ("dropzettel.inbox", "dropzettel.digest")
ICLOUD_SHORTCUTS = Path.home() / "Library/Mobile Documents/iCloud~is~workflow~my~workflows/Documents"


def say(msg: str = "") -> None:
    print(msg, flush=True)


def ask(question: str, default: str = "", choices: list[str] | None = None) -> str:
    hint = f" [{'/'.join(choices)}]" if choices else ""
    hint += f" (default: {default})" if default else ""
    while True:
        answer = input(f"{question}{hint}: ").strip() or default
        if not choices or answer in choices:
            return answer
        say(f"  Please answer one of: {', '.join(choices)}")


def dropbox_root() -> Path:
    info = Path.home() / ".dropbox" / "info.json"
    try:
        data = json.loads(info.read_text())
        for account in ("personal", "business"):
            if account in data:
                return Path(data[account]["path"])
    except (OSError, ValueError, KeyError):
        pass
    return Path.home() / "Dropbox"


def uid_domain() -> str:
    return f"gui/{os.getuid()}"


def uninstall_jobs() -> None:
    for label in JOBS:
        subprocess.run(["launchctl", "bootout", f"{uid_domain()}/{label}"], capture_output=True)
        plist = LAUNCH_AGENTS / f"{label}.plist"
        if plist.exists():
            plist.unlink()
            say(f"removed {plist}")
    say("Background jobs are off. Your notes, config and inbox were not touched.")


def install_jobs(home: Path, inbox: Path) -> None:
    LAUNCH_AGENTS.mkdir(parents=True, exist_ok=True)
    (home / "state").mkdir(parents=True, exist_ok=True)
    for label in JOBS:
        text = (CODE / "launchd" / f"{label}.plist.template").read_text()
        text = text.replace("__CODE__", str(CODE)).replace("__HOME__", str(home)).replace("__INBOX__", str(inbox))
        plist = LAUNCH_AGENTS / f"{label}.plist"
        subprocess.run(["launchctl", "bootout", f"{uid_domain()}/{label}"], capture_output=True)
        plist.write_text(text)
        r = subprocess.run(["launchctl", "bootstrap", uid_domain(), str(plist)], capture_output=True, text=True)
        say(f"  {label}: {'loaded' if r.returncode == 0 else 'could not load: ' + r.stderr.strip()}")


def build_shortcut(service: str, phone_path: str, out_dir: Path) -> Path | None:
    unsigned = out_dir / "Dropzettel.unsigned.shortcut"
    signed = out_dir / "Dropzettel.shortcut"
    subprocess.run([sys.executable, str(CODE / "shortcut" / "build_shortcut.py"), "--service", service,
                    "--path", phone_path, "--out", str(unsigned)], check=True, capture_output=True)
    if not shutil.which("shortcuts"):
        say("  The `shortcuts` command is missing (needs macOS 12+), so the shortcut could not be signed.")
        return None
    r = subprocess.run(["shortcuts", "sign", "--mode", "anyone", "--input", str(unsigned), "--output", str(signed)],
                       capture_output=True, text=True)
    unsigned.unlink(missing_ok=True)
    if r.returncode != 0 or not signed.exists():
        say(f"  Signing failed: {r.stderr.strip() or 'unknown error'}")
        return None
    signed.chmod(0o644)
    return signed


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--sync", choices=["dropbox", "icloud", "folder"],
                    help="how captures travel from your phone to this Mac")
    ap.add_argument("--home", help="data folder: config, state, archive of processed captures")
    ap.add_argument("--inbox", help="inbox folder (default depends on --sync)")
    ap.add_argument("--vault", help="Obsidian vault folder (created if missing)")
    ap.add_argument("--about", help="one or two sentences about you, for the librarian")
    ap.add_argument("--language", help="language for summaries (default English)")
    ap.add_argument("--model", help="Claude model alias: haiku, sonnet or opus (default sonnet)")
    ap.add_argument("--jobs", choices=["yes", "no"], help="install the background jobs")
    ap.add_argument("--shortcut", choices=["yes", "no"], help="build and sign the phone shortcut")
    ap.add_argument("--yes", action="store_true", help="never prompt; use defaults for anything not given")
    ap.add_argument("--uninstall-jobs", action="store_true", help="remove the background jobs and exit")
    a = ap.parse_args()

    if a.uninstall_jobs:
        uninstall_jobs()
        return

    interactive = not a.yes and sys.stdin.isatty()

    def get(value, question, default="", choices=None):
        if value:
            return value
        return ask(question, default, choices) if interactive else default

    say("Dropzettel setup\n")

    # 1. tools
    claude = shutil.which("claude")
    say(f"  claude CLI : {claude or 'NOT FOUND. Install Claude Code and sign in, then run setup again.'}")
    for tool, purpose in (("yt-dlp", "YouTube transcripts"), ("pdftotext", "PDF text"), ("tesseract", "OCR backup for images")):
        say(f"  {tool:<11}: {shutil.which(tool) or f'not found (optional, used for {purpose})'}")
    say()

    # 2. where things live
    sync = get(a.sync, "How do captures reach this Mac? dropbox, icloud, or any synced folder", "dropbox",
               ["dropbox", "icloud", "folder"])
    if sync == "dropbox":
        default_home = dropbox_root() / "Dropzettel"
    else:
        default_home = Path.home() / "Dropzettel"
    home = Path(get(a.home, "Data folder (config, state, archive)", str(default_home))).expanduser().resolve()
    if sync == "icloud":
        default_inbox = ICLOUD_SHORTCUTS / "Dropzettel" / "inbox"
    else:
        default_inbox = home / "inbox"
    inbox = Path(get(a.inbox, "Inbox folder (must sync to your phone)", str(default_inbox))).expanduser().resolve()
    vault = Path(get(a.vault, "Obsidian vault folder (an existing vault is fine; nothing in it is changed)",
                     str(Path.home() / "Documents" / "Zettelkasten"))).expanduser().resolve()
    about = get(a.about, "One or two sentences about you (what you do, what you are curious about)", "")
    language = get(a.language, "Language for summaries", "English")
    model = get(a.model, "Claude model: haiku (lightest), sonnet, opus (most thorough)", "sonnet")

    # 3. config
    home.mkdir(parents=True, exist_ok=True)
    cfg_path = home / "config.json"
    if cfg_path.exists():
        say(f"\n  {cfg_path} already exists; keeping it as it is.")
    else:
        cfg = {"vault": str(vault), "inbox": str(inbox), "model": model, "note_language": language}
        if about:
            cfg["owner_context"] = about
        if claude:
            cfg["claude_bin"] = claude
        cfg_path.write_text(json.dumps(cfg, indent=2, ensure_ascii=False) + "\n")
        say(f"\n  wrote {cfg_path}")
    cfg = json.loads(cfg_path.read_text())
    inbox = Path(cfg.get("inbox") or home / "inbox").expanduser()

    # 4. vault folders, templates, dashboard
    subprocess.run([sys.executable, str(CODE / "dropzettel.py"), "--home", str(home), "init"], check=True)

    # 5. phone shortcut
    shortcut_file = None
    if sync in ("dropbox", "icloud") and sys.platform == "darwin":
        root = dropbox_root() if sync == "dropbox" else ICLOUD_SHORTCUTS
        try:
            phone_path = "/" + str(inbox.resolve().relative_to(root.resolve())) + "/"
        except ValueError:
            phone_path = None
            say(f"\n  The inbox is not inside {root}, so no phone shortcut was built.")
        if phone_path and get(a.shortcut, f"Build the phone shortcut (saves to {phone_path})? It is sent to Apple for signing",
                              "yes", ["yes", "no"]) == "yes":
            shortcut_file = build_shortcut(sync, phone_path, home)

    # 6. background jobs: only on an explicit yes
    jobs = "no"
    if sys.platform == "darwin":
        jobs = get(a.jobs, "Install the background jobs (file the inbox automatically, weekly review on Sundays)?",
                   "no", ["yes", "no"])
        if jobs == "yes":
            install_jobs(home, inbox)

    run = f"{CODE}/run.sh --home '{home}'"
    say("\nDone.\n")
    say(f"  Vault   : {cfg['vault']}  (open this folder in Obsidian, install the Dataview plugin)")
    say(f"  Inbox   : {inbox}")
    if shortcut_file:
        say(f"  Shortcut: {shortcut_file}  (AirDrop it to your iPhone, tap Add Shortcut)")
    if jobs == "yes":
        say("  Jobs    : installed. Remove them with ./setup.sh --uninstall-jobs")
    else:
        say(f"  Process the inbox by hand:  {run} process")
    say(f"  Status  :  {run} status")
    say("\nTry it: save a text file with a link into the inbox, wait a minute (or run process),\n"
        "then open '0 - Dashboard/Capture Log' in Obsidian.")


if __name__ == "__main__":
    main()
