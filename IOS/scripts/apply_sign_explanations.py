#!/usr/bin/env python3
"""Apply explain_sign() to all signs in signs.json and save updated notes."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SIGNS_PATH = ROOT / "FahrPrufungDE" / "Resources" / "signs.json"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from official_sign_data import officialize_notes  # noqa: E402
from sign_explanation_engine import explain_sign  # noqa: E402


def main() -> None:
    data = json.loads(SIGNS_PATH.read_text(encoding="utf-8"))
    signs = data["signs"]
    for sign in signs:
        sign["notes"] = officialize_notes(explain_sign(sign))
    data.setdefault("meta", {})["has_explanations"] = True
    SIGNS_PATH.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Updated explanations for {len(signs)} signs → {SIGNS_PATH}")


if __name__ == "__main__":
    main()
