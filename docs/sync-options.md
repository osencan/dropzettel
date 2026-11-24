# Sync options

Dropzettel only needs one thing from a sync service: a folder that exists on your Mac and that your phone can save small files into. Each capture is its own file, so there is nothing to merge and nothing to conflict.

## Dropbox

- **Inbox:** `Dropbox/Dropzettel/inbox` (setup's default).
- **Phone:** the shortcut uses the *Save Dropbox File* action that is built into Apple's Shortcuts app. It talks to Dropbox directly and takes a plain path such as `/Dropzettel/inbox/phone-20261124-153000.txt`.
- **First run on the phone:** Shortcuts asks you to connect your Dropbox account, then asks whether the shortcut may save a file on Dropbox. Choose *Always Allow*.
- **Files and photos:** the Dropbox app's own share extension (*Save to Dropbox*) → the inbox folder.
- **Known issue:** on some Macs the Dropbox folder lives under `~/Library/CloudStorage/`. Background jobs may then need Full Disk Access for `/bin/bash` (System Settings → Privacy & Security). If `state/launchd.log` shows "Operation not permitted", that is the cause.

## iCloud Drive (experimental)

- **Inbox:** `iCloud Drive/Shortcuts/Dropzettel/inbox`. On the Mac that is `~/Library/Mobile Documents/iCloud~is~workflow~my~workflows/Documents/Dropzettel/inbox`.
- **Why that folder:** the *Save File* action can write below the Shortcuts folder using a plain path. Any other iCloud folder needs a location picked by hand on the phone.
- **Data folder:** kept outside iCloud (`~/Dropzettel`), so state files are not synced.
- **Status:** the shortcut builds and signs, and the processor does not care where the inbox is. Nobody has run this variant on a phone yet. If you try it, please open an issue with what happened.
- **Likely issue:** background jobs reading `~/Library/Mobile Documents` may need Full Disk Access for `/bin/bash`.

## Any synced folder

Choose `folder` in setup and point the inbox at any path: Syncthing, Google Drive, OneDrive, a NAS share. No shortcut is built. Anything that can save a text file into that folder works as a capture tool, and so does dragging files in on the Mac.

## If the shortcut does not appear in the share sheet

Scroll to the end of the share sheet's action list → *Edit Actions* → switch *Dropzettel* on.

## Changing the shortcut

`shortcut/build_shortcut.py` generates it. Edit the script, then:

```bash
python3 shortcut/build_shortcut.py --service dropbox --path /Dropzettel/inbox/ --out Dropzettel.unsigned.shortcut
```

```bash
shortcuts sign --mode anyone --input Dropzettel.unsigned.shortcut --output Dropzettel.shortcut
```
