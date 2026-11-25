# INSIGHTS

Decisions and discoveries, newest last.

## 2026-11-24 — Design carried over from the private setup

**The script does the filing; the model only returns JSON.** `dropzettel.py` owns every file operation. The model is called once per capture through the local `claude` CLI with all tools off, no MCP servers, no settings loaded, and output forced into a JSON schema. A fetched web page is untrusted text; with this setup the worst it can do is produce an odd summary. The script sanitises the result: tags are slugged, titles made filename-safe, related links dropped unless the title exists in the vault.

**The Claude CLI, not an API key.** Users who have Claude Code are already signed in, so there is no key to create or store. Only `llm_json()` needs replacing for another backend.

**One file per capture, never a shared append file.** A single inbox file that the phone appends to and the Mac truncates would produce sync conflict copies. Separate files cannot conflict.

**Files younger than 20 seconds are skipped,** and the launchd runner sleeps 30 seconds, so a file that is still syncing is not read half-written.

**Nothing is deleted.** Binaries move into the vault and are embedded in their note. Link and text captures move to `processed/`. Unfileable items move to `failed/` with a log entry.

**Two kinds of failure.** A bad item goes to `failed/` and the run continues. If the classifier itself is unavailable, the run stops and everything stays in the inbox.

**Full text lives outside the vault** (`fulltext/<capture_id>.txt`), so notes stay readable and an agent can still search the full transcript.

**Tags and topics are different things.** Tags are native Obsidian tags for subjects. Topics are links to index notes, one per note. The librarian is given the existing vocabulary and told to reuse it.

**The permanent-notes folder is never written to.** The weekly review proposes candidates; the owner writes them.

## 2026-11-24 — Decisions made for the public version

**Code and data are separate.** The clone holds code. A data folder (`--home` or `DROPZETTEL_HOME`) holds `config.json`, state and archives. Personal data therefore never sits inside the repository, and `.gitignore` covers the case where someone uses the clone as the data folder anyway.

**The inbox path is its own setting,** because with iCloud the inbox has to sit in the Shortcuts folder while state should not be synced.

**Clean folder numbering.** The starter vault uses `0 - Dashboard` to `6 - Attachments`. Names are configurable, so an existing vault with other names works by setting `folders` in the config.

**Default model is `sonnet`.** Cheaper for strangers trying it; `opus` and `haiku` are one config value away.

**Tag slugs keep letters of any alphabet,** not only ASCII plus Turkish as in the private version.

**The shortcut accepts only links and text.** Safari and most apps then pass the link itself instead of page contents. Files go through the sync service's own share extension.

**Dropbox variant uses "Save Dropbox File"** (`is.workflow.actions.dropbox.savefile`), which takes a plain path. The generic "Save File" action stores a per-device folder bookmark that cannot be generated on the Mac; it can only address the Shortcuts folder by plain path, which is why the iCloud variant puts the inbox there.

**No affiliation claims.** The name avoids the Dropbox trademark and the README says the project is independent.

**The project was not created with the workspace's `init-project.sh`,** because that script makes an initial git commit and adds boilerplate (`package.json`, `.env`, sample `src/`) that a public repository should not carry. The conventions were applied by hand instead: `agents.md` with `CLAUDE.md` and `.gemini/GEMINI.md` links, `TASKS.md`, `INSIGHTS.md`, `CRITICS/`, `make validate`, `.github/FUNDING.yml`.

## 2026-11-24 — What was tested

- `make validate` passes.
- Unattended `./setup.sh --sync folder …` into a scratch folder: config written, vault created with starter files, then one link (with a note) and one thought were filed on `sonnet`; topic indexes, capture log and tag registry were created.
- Both shortcut variants build and are accepted by `shortcuts sign`.
- The Dropbox shortcut and the launchd job shape are in use in the private setup this was extracted from.

- Fresh clone of the public repository (commit `4a0c68c`) into a temporary folder, `./setup.sh --sync folder … --jobs yes --yes`: the environment was created, both jobs loaded, and a text file dropped into the inbox was filed by the inbox job 37 seconds later with exit code 0. `./setup.sh --uninstall-jobs` then removed both jobs and their plist files.

Not tested: the iCloud shortcut on a phone, the Dropbox path through the public setup (shortcut build inside a real Dropbox folder), the interactive prompts, the digest job firing on schedule, any non-macOS system.

## 2026-11-25 — `import-whatsapp` documented as it behaves

The README now has its own section for the importer. It was checked against two invented exports (iPhone bracket layout, Android dash layout), split step only, no model call. Observed and written down rather than fixed: all senders are imported and the name is dropped; media placeholders are skipped by the English word "omitted" only; the capture date is the import time, the WhatsApp date survives as text; a second import re-files plain-text thoughts because only links and files have a duplicate key. The fixes are listed in `TASKS.md`.
