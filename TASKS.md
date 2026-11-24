# TASKS

## Done (2026-11-24)

- [x] Extract the processor from the private setup and remove everything machine-specific
- [x] Config defaults, separate data folder (`--home` / `DROPZETTEL_HOME`), configurable vault folders
- [x] Starter vault (`vault-template/`) with templates, `Start Here` and `AGENTS.md`
- [x] Setup wizard with unattended flags; background jobs only on an explicit yes; uninstall command
- [x] Shortcut builder with Dropbox and iCloud variants
- [x] `make validate`: compile, shell syntax, plist lint, self-test, no-personal-paths check
- [x] Fresh unattended install into a scratch folder, one link and one thought filed on the default model
- [x] Fresh clone from GitHub, `setup.sh --jobs yes`: jobs loaded, a dropped capture was filed by the inbox job, `--uninstall-jobs` removed both
- [x] README, sync options doc, MIT license, GitHub Sponsors funding file

## Before the first push (developer)

- [x] Name decided 2026-11-24: Dropzettel
- [ ] Trademark check for the name (not done)
- [ ] Read `README.md` end to end; it speaks in your voice
- [ ] `git init`, review, commit, create the public repository, push
- [ ] Add a screenshot or short clip of a capture landing in Obsidian (the README has none)

## Next

- [ ] Run the iCloud shortcut variant on a phone; update `docs/sync-options.md` with the result
- [ ] Second model backend (API key, or a local model) behind `llm_json()`
- [ ] Index URLs inside pre-existing notes so old sources are detected as duplicates
- [ ] Android capture (a share target that writes a text file into the synced folder)
- [ ] Linux: systemd path unit as the counterpart of the launchd jobs
- [ ] Import helpers: X bookmarks, browser reading lists
