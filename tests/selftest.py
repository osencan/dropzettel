#!/usr/bin/env python3
"""Checks that need no model call and no network. Run with:  make validate"""
import argparse
import json
import plistlib
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "shortcut"))
import dropzettel as dz          # noqa: E402
import build_shortcut            # noqa: E402

failures = []


def check(name, got, want):
    if got != want:
        failures.append(f"{name}: got {got!r}, want {want!r}")


with tempfile.TemporaryDirectory() as tmp:
    home, vault = Path(tmp) / "home", Path(tmp) / "vault"
    home.mkdir()
    (home / "config.json").write_text(json.dumps({"vault": str(vault), "settle_seconds": 0}))
    args = argparse.Namespace(home=str(home), vault=None, inbox=None)
    dz.load_config(args)

    check("slug ascii", dz.slug_tag("#AI Agents"), "ai-agents")
    check("slug unicode", dz.slug_tag("Öğrenme_Bilimi"), "öğrenme-bilimi")
    check("title", dz.safe_title('What: is "this"? [draft]'), "What is this draft")
    check("url tracking", dz.normalize_url("https://www.Example.com/a/?utm_source=x&id=7"), "https://example.com/a?id=7")
    check("url twitter", dz.normalize_url("https://x.com/u/status/1?s=20&t=abc"), "https://x.com/u/status/1")

    dz.cmd_init(args)
    for folder in dz.DEFAULTS["folders"].values():
        check(f"folder {folder}", (vault / folder).is_dir(), True)
    for f in ("Start Here.md", "AGENTS.md", "0 - Dashboard/To Check.md", "0 - Dashboard/Tag Registry.md",
              "5 - Templates/Permanent Note.md"):
        check(f"starter {f}", (vault / f).is_file(), True)
    (vault / "Start Here.md").write_text("mine")
    dz.cmd_init(args)
    check("init never overwrites", (vault / "Start Here.md").read_text(), "mine")

    inbox = Path(dz.CFG["inbox"])
    (inbox / "a.txt").write_text("https://example.com/post?utm_medium=y\n\nfor the onboarding flow")
    (inbox / "b.txt").write_text("a thought with no link")
    (inbox / "c.txt").write_text("https://a.example/1\nhttps://b.example/2\nhttps://c.example/3")
    (inbox / ".hidden").write_text("x")
    check("waiting", [p.name for p in sorted(dz.waiting_files())], ["a.txt", "b.txt", "c.txt"])
    a = dz.expand(inbox / "a.txt")
    check("link + note", (a[0].source_type, a[0].url, a[0].owner_note),
          ("link", "https://example.com/post?utm_medium=y", "for the onboarding flow"))
    b = dz.expand(inbox / "b.txt")
    check("thought", (b[0].source_type, b[0].owner_note), ("text", "a thought with no link"))
    check("link list", len(dz.expand(inbox / "c.txt")), 3)

for service, action_id in build_shortcut.SAVE_ACTIONS.items():
    sc = build_shortcut.build(service, "Dropzettel/inbox", "Dropzettel")
    plistlib.dumps(sc, fmt=plistlib.FMT_BINARY)
    save = sc["WFWorkflowActions"][-1]
    check(f"shortcut {service} action", save["WFWorkflowActionIdentifier"], action_id)
    check(f"shortcut {service} path", save["WFWorkflowActionParameters"]["WFFileDestinationPath"]["Value"]["string"],
          "/Dropzettel/inbox/phone-￼.txt")

if failures:
    print("\n".join("FAIL " + f for f in failures))
    sys.exit(1)
print("selftest: all checks passed")
