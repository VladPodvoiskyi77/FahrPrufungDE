#!/usr/bin/env python3
"""Build official_translations.json from translation data modules."""

from __future__ import annotations

import json
from pathlib import Path

from official_translation_data import TRANSLATIONS as CORE
from official_translation_phrases import TRANSLATIONS as PHRASES
from official_translation_technical import TRANSLATIONS as TECHNICAL

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "official_translations.json"


def main() -> None:
    merged = {**CORE, **TECHNICAL, **PHRASES}
    OUT.write_text(json.dumps(merged, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(merged)} translation patches to {OUT.name}")


if __name__ == "__main__":
    main()
