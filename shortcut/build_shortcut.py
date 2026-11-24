#!/usr/bin/env python3
"""Build the phone shortcut that saves a link or a thought into the Dropzettel inbox.

    python3 build_shortcut.py --service dropbox --path /Dropzettel/inbox/ --out Dropzettel.unsigned.shortcut
    shortcuts sign --mode anyone --input Dropzettel.unsigned.shortcut --output Dropzettel.shortcut

setup.sh does both steps for you. The signed file is what an iPhone imports (AirDrop it, or open it
from the Files / Dropbox app).

What the shortcut does:

    If something was shared (share sheet):
        ask "Why save this? (optional)"  ->  text file:  <shared link or text>, blank line, <your note>
    Otherwise (run from the Home Screen):
        ask "Thought"                    ->  text file:  <your thought>
    Save as  <path>/phone-<yyyyMMdd-HHmmss>.txt

--service dropbox   uses the "Save Dropbox File" action. --path is a path inside your Dropbox.
--service icloud    uses the "Save File" action, which writes below the Shortcuts folder in
                    iCloud Drive. --path is relative to that folder. Experimental.

It accepts only links and text on purpose: Safari and most apps then hand over the link itself
instead of the page contents. Photos and files go through "Save to Files" / "Save to Dropbox".
"""
import argparse
import plistlib
import uuid
from pathlib import Path

OBJ = "￼"          # placeholder character that a variable replaces


def new_id() -> str:
    return str(uuid.uuid4()).upper()


def output_ref(action_uuid: str, name: str) -> dict:
    return {"OutputUUID": action_uuid, "OutputName": name, "Type": "ActionOutput"}


def attachment(value: dict) -> dict:
    return {"Value": value, "WFSerializationType": "WFTextTokenAttachment"}


def token_string(parts: list) -> dict:
    """parts: plain strings and variable dicts, in order."""
    text, ranges = "", {}
    for part in parts:
        if isinstance(part, str):
            text += part
        else:
            ranges["{%d, 1}" % (len(text.encode("utf-16-le")) // 2)] = part   # offsets are UTF-16 units
            text += OBJ
    return {"Value": {"string": text, "attachmentsByRange": ranges},
            "WFSerializationType": "WFTextTokenString"}


def action(identifier: str, **params) -> dict:
    return {"WFWorkflowActionIdentifier": identifier, "WFWorkflowActionParameters": params}


SAVE_ACTIONS = {
    "dropbox": "is.workflow.actions.dropbox.savefile",
    "icloud": "is.workflow.actions.documentpicker.save",
}


def build(service: str, folder: str, name: str, prefix: str = "phone-") -> dict:
    folder = "/" + folder.strip("/") + "/"
    shortcut_input = {"Type": "ExtensionInput"}
    capture_var = {"Type": "Variable", "VariableName": "Capture"}
    if_group = new_id()
    ask_note, text_block, ask_thought, stamp = new_id(), new_id(), new_id(), new_id()

    actions = [
        # If Shortcut Input has any value
        action("is.workflow.actions.conditional",
               GroupingIdentifier=if_group, WFControlFlowMode=0, WFCondition=100,
               WFInput={"Type": "Variable", "Variable": attachment(shortcut_input)}),
        action("is.workflow.actions.ask",
               UUID=ask_note, WFInputType="Text", WFAskActionPrompt="Why save this? (optional)"),
        action("is.workflow.actions.gettext",
               UUID=text_block,
               WFTextActionText=token_string([shortcut_input, "\n\n", output_ref(ask_note, "Ask for Input")])),
        action("is.workflow.actions.setvariable",
               WFVariableName="Capture", WFInput=attachment(output_ref(text_block, "Text"))),
        # Otherwise
        action("is.workflow.actions.conditional", GroupingIdentifier=if_group, WFControlFlowMode=1),
        action("is.workflow.actions.ask",
               UUID=ask_thought, WFInputType="Text", WFAskActionPrompt="Thought"),
        action("is.workflow.actions.setvariable",
               WFVariableName="Capture", WFInput=attachment(output_ref(ask_thought, "Ask for Input"))),
        # End If
        action("is.workflow.actions.conditional",
               GroupingIdentifier=if_group, WFControlFlowMode=2, UUID=new_id()),
        # Timestamp for a unique file name: one file per capture, never a shared file
        action("is.workflow.actions.format.date",
               UUID=stamp, WFDateFormatStyle="Custom", WFDateFormat="yyyyMMdd-HHmmss",
               WFDate=token_string([{"Type": "CurrentDate"}])),
        action(SAVE_ACTIONS[service],
               UUID=new_id(), WFInput=attachment(capture_var),
               WFAskWhereToSave=False, WFSaveFileOverwrite=False,
               WFFileDestinationPath=token_string(
                   [folder + prefix, output_ref(stamp, "Formatted Date"), ".txt"])),
    ]
    return {
        "WFWorkflowName": name,
        "WFWorkflowClientVersion": "2607.0.2",
        "WFWorkflowMinimumClientVersion": 900,
        "WFWorkflowMinimumClientVersionString": "900",
        "WFWorkflowIcon": {"WFWorkflowIconStartColor": 2071128575, "WFWorkflowIconGlyphNumber": 61440},
        "WFWorkflowImportQuestions": [],
        "WFWorkflowTypes": ["ActionExtension"],                       # show in the share sheet
        "WFQuickActionSurfaces": [],
        "WFWorkflowInputContentItemClasses": ["WFURLContentItem", "WFStringContentItem"],
        "WFWorkflowOutputContentItemClasses": [],
        "WFWorkflowHasOutputFallback": False,
        "WFWorkflowHasShortcutInputVariables": True,
        "WFWorkflowActions": actions,
    }


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--service", choices=sorted(SAVE_ACTIONS), default="dropbox")
    ap.add_argument("--path", default="/Dropzettel/inbox/", help="inbox folder as the phone's save action sees it")
    ap.add_argument("--name", default="Dropzettel", help="shortcut name shown on the phone")
    ap.add_argument("--out", default=str(Path(__file__).with_name("Dropzettel.unsigned.shortcut")))
    args = ap.parse_args()
    shortcut = build(args.service, args.path, args.name)
    with open(args.out, "wb") as fh:
        plistlib.dump(shortcut, fh, fmt=plistlib.FMT_BINARY)
    print(f"wrote {args.out} ({len(shortcut['WFWorkflowActions'])} actions, {args.service}, {args.path})")


if __name__ == "__main__":
    main()
