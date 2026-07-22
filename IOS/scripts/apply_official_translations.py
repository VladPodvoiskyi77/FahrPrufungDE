#!/usr/bin/env python3
"""Apply official/legal translations to vocabulary.json."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VOCAB_PATH = ROOT / "FahrPrufungDE" / "Resources" / "vocabulary.json"
PATCH_PATH = Path(__file__).resolve().parent / "official_translations.json"


def main() -> None:
    patches: dict[str, dict[str, str]] = json.loads(PATCH_PATH.read_text(encoding="utf-8"))
    data = json.loads(VOCAB_PATH.read_text(encoding="utf-8"))

    updated = 0
    missing = []
    for term in data["terms"]:
        patch = patches.get(term["id"])
        if not patch:
            missing.append(term["id"])
            continue
        for lang in ("ru", "en", "uk", "fr", "tr"):
            if lang in patch:
                term[lang] = patch[lang]
        updated += 1

    VOCAB_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Updated {updated} / {len(data['terms'])} terms")
    if missing:
        print(f"Missing patches ({len(missing)}): {', '.join(missing[:10])}{'...' if len(missing) > 10 else ''}")


if __name__ == "__main__":
    main()
