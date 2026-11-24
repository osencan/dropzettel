# Dropzettel — agent contract

Read this first. It applies to Claude, Gemini and Codex alike.

Dropzettel is a public, MIT-licensed tool: an inbox folder, a processor that files captures into an Obsidian Zettelkasten, a starter vault, a phone shortcut builder and launchd job templates. See `README.md` for what users see, `INSIGHTS.md` for why things are the way they are, `TASKS.md` for open work.

## Layout

| Path | Role |
|---|---|
| `dropzettel.py` | The processor. One file on purpose, so users can read all of it |
| `run.sh` | Runner used by launchd and by hand |
| `setup.sh`, `scripts/setup_wizard.py` | Install: venv, config, vault init, shortcut, optional jobs |
| `shortcut/build_shortcut.py` | Generates the phone shortcut (Dropbox or iCloud variant) |
| `launchd/*.plist.template` | Background job templates, filled in by setup |
| `vault-template/` | Starter vault: folders, templates, `AGENTS.md` for the user's vault |
| `tests/selftest.py` | Checks that need no model call and no network |

## Rules

- **This repository is public. Nothing personal goes in.** No real paths under a home directory, no real captures, notes, config or logs. `make validate` fails on any absolute macOS home path. Examples must be invented.
- **The classifier stays tool-less.** `llm_json()` calls the CLI with `--tools ""` and a JSON schema. Fetched web content is untrusted; never give that call file or shell access.
- **The script does all file operations**, and sanitises model output (tag slugs, safe titles, related titles must exist).
- **Never delete or rewrite user notes.** Additive only: new notes, appended index lines, starter files copied only when missing.
- **Never write to the permanent-notes folder** (`4 - Zettelkasten`).
- **Setup installs nothing persistent without an explicit yes.** The jobs default to "no".
- **State what was tested.** The README's "Sync options" and "Limitations" must say honestly which paths have run on real devices.
- Never `git commit` or `git push`; the developer does that. Update `TASKS.md` and `INSIGHTS.md` when you change something.
- Run `make validate` before reporting a task complete. Test processor changes against a scratch vault: `./run.sh --home <tmp>/home process`.

## Commands

```bash
make validate
./setup.sh --help
./run.sh --home <data folder> process | status | digest | init
```
