#!/usr/bin/env python3
"""Capitalize first letter in vocabulary.json display fields."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VOCAB_PATH = ROOT / "FahrPrufungDE" / "Resources" / "vocabulary.json"

TERM_FIELDS = ("de", "ru", "en", "uk", "fr", "tr", "exam_phrase_de")
CATEGORY_FIELDS = ("de", "ru", "en", "uk", "fr", "tr")


def capitalize_first(text: str) -> str:
    for i, ch in enumerate(text):
        if ch.isalpha() or ch.isdigit():
            return text[:i] + ch.upper() + text[i + 1 :]
    return text


def main() -> None:
    data = json.loads(VOCAB_PATH.read_text(encoding="utf-8"))
    changed = 0

    for term in data.get("terms", []):
        for field in TERM_FIELDS:
            value = term.get(field)
            if not value or not isinstance(value, str):
                continue
            fixed = capitalize_first(value)
            if fixed != value:
                term[field] = fixed
                changed += 1

    for category in data.get("categories", []):
        for field in CATEGORY_FIELDS:
            value = category.get(field)
            if not value or not isinstance(value, str):
                continue
            fixed = capitalize_first(value)
            if fixed != value:
                category[field] = fixed
                changed += 1

    VOCAB_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Capitalized {changed} fields in {VOCAB_PATH.name}")


if __name__ == "__main__":
    main()
