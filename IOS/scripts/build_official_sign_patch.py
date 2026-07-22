#!/usr/bin/env python3
"""Build official_sign_translations.json patch for all signs."""

from __future__ import annotations

import json
from pathlib import Path

from official_sign_data import LANGS, build_title_translations, officialize_notes

ROOT = Path(__file__).resolve().parent.parent
SIGNS_PATH = ROOT / "FahrPrufungDE" / "Resources" / "signs.json"
PATCH_PATH = Path(__file__).resolve().parent / "official_sign_translations.json"


def main() -> None:
    data = json.loads(SIGNS_PATH.read_text(encoding="utf-8"))
    patches: dict[str, dict] = {}

    for sign in data["signs"]:
        code = sign["stvo_code"]
        titles = build_title_translations(sign)
        notes = officialize_notes(sign.get("notes", {}))
        patch: dict = {"titles": titles}
        if notes:
            patch["notes"] = notes
        patches[code] = patch

    PATCH_PATH.write_text(
        json.dumps(patches, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {len(patches)} sign patches → {PATCH_PATH}")


if __name__ == "__main__":
    main()
