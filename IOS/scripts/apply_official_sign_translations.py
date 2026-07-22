#!/usr/bin/env python3
"""Apply official StVO-style translations to signs.json (titles, notes, categories)."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

from official_sign_data import CATEGORY_OFFICIAL, LANGS

ROOT = Path(__file__).resolve().parent.parent
SIGNS_PATH = ROOT / "FahrPrufungDE" / "Resources" / "signs.json"
PATCH_PATH = Path(__file__).resolve().parent / "official_sign_translations.json"
BASELINE_PATH = Path(__file__).resolve().parent / "signs_before_official.json"


def main() -> None:
    if not PATCH_PATH.exists():
        raise SystemExit(f"Missing patch file: {PATCH_PATH}. Run build_official_sign_patch.py first.")

    if not BASELINE_PATH.exists():
        shutil.copy(SIGNS_PATH, BASELINE_PATH)
        print(f"Saved baseline → {BASELINE_PATH}")

    baseline = json.loads(BASELINE_PATH.read_text(encoding="utf-8"))
    base_by_code = {s["stvo_code"]: s for s in baseline["signs"]}

    patches = json.loads(PATCH_PATH.read_text(encoding="utf-8"))
    data = json.loads(SIGNS_PATH.read_text(encoding="utf-8"))

    for cat in data.get("categories", []):
        official = CATEGORY_OFFICIAL.get(cat["id"])
        if official:
            cat.update(official)

    title_fields = 0
    note_fields = 0
    signs_changed = 0

    for sign in data["signs"]:
        code = sign["stvo_code"]
        patch = patches.get(code)
        if not patch:
            continue
        changed = False

        for lang in LANGS:
            new_title = patch.get("titles", {}).get(lang)
            if new_title and sign.get(lang) != new_title:
                sign[lang] = new_title
                title_fields += 1
                changed = True

        new_notes = patch.get("notes")
        if new_notes:
            sign.setdefault("notes", {})
            for lang in LANGS:
                if lang in new_notes and sign["notes"].get(lang) != new_notes[lang]:
                    sign["notes"][lang] = new_notes[lang]
                    note_fields += 1
                    changed = True

        if changed:
            signs_changed += 1

    SIGNS_PATH.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    # Stats vs baseline
    base_titles = base_notes = 0
    for sign in data["signs"]:
        code = sign["stvo_code"]
        old = base_by_code.get(code, {})
        for lang in LANGS:
            if sign.get(lang) != old.get(lang):
                base_titles += 1
            if sign.get("notes", {}).get(lang) != old.get("notes", {}).get(lang):
                base_notes += 1

    print(f"Updated categories: {len(CATEGORY_OFFICIAL)}")
    print(f"Signs with changes: {signs_changed} / {len(data['signs'])}")
    print(f"Title fields changed: {base_titles}")
    print(f"Note fields changed: {base_notes}")
    print(f"Total fields changed: {base_titles + base_notes}")


if __name__ == "__main__":
    main()
