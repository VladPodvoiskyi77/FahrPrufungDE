#!/usr/bin/env python3
"""Reclassify StVO signs into correct app categories and move PNG assets."""

from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SIGNS_JSON = ROOT / "FahrPrufungDE" / "Resources" / "signs.json"
SIGNS_DIR = ROOT / "FahrPrufungDE" / "Resources" / "Signs"


def code_num(code: str) -> int | None:
    m = re.match(r"(\d+)", (code or "").replace("Z", ""))
    return int(m.group(1)) if m else None


def stvo_category(code: str, de: str = "") -> str:
    """Map StVO sign code + German label to app category."""
    de_lower = de.lower()
    code = (code or "").strip()

    if code.startswith("Z") or code.startswith("z"):
        return "additional"

    n = code_num(code)
    if n is None:
        return "information"

    # Gefahrzeichen
    if 100 <= n <= 151:
        return "warning"
    if n == 201 or "andreaskreuz" in de_lower:
        return "warning"

    # Zone / Bereich / priority Hinweise — not Verbote
    if n in (205, 208, 301, 305, 306, 307, 308):
        return "information"
    if n in (223, 229, 230):
        return "information"
    if n in (240, 241, 246, 247, 248):
        return "information"
    if n in (242, 244, 325):
        return "information"
    if re.fullmatch(r"270\.[12]", code) or (
        n == 270 and "zone" in de_lower
    ):
        return "information"
    if re.fullmatch(r"274\.[12](?:-\d+)?", code) or (
        n == 274 and "zone" in de_lower
    ):
        return "information"
    if re.fullmatch(r"290\.[12]", code) or (
        n == 290 and "zone" in de_lower
    ):
        return "information"
    if "fußgängerzone" in de_lower or "fahrradzone" in de_lower:
        return "information"
    if "fahrradstraße" in de_lower and n == 244:
        return "information"
    if "verkehrsberuhigt" in de_lower:
        return "information"

    # Stop
    if n == 206:
        return "prohibitory"

    # Gebotszeichen (blue round)
    if n in (
        209, 210, 211, 212, 213, 214, 215,
        220, 222, 224,
        237, 238, 239,
        268, 275, 279,
    ):
        return "mandatory"

    # Verbotszeichen (red round / speed / halt / park)
    if n in (
        250, 251, 253, 254, 255, 257, 259, 260, 261, 262, 263, 264, 265, 266,
        267, 269, 272, 273, 276, 277, 280, 281, 282, 283, 286,
    ):
        return "prohibitory"
    if n == 274 and "höchstgeschwindigkeit" in de_lower:
        return "prohibitory"
    if n == 278 and "höchstgeschwindigkeit" in de_lower:
        return "prohibitory"
    if n == 277 and "überhol" in de_lower:
        return "prohibitory"

    if n >= 284:
        return "information"

    return "information"


def move_png(old_rel: str, new_category: str) -> str:
    """Move PNG to category folder; return updated relative path."""
    if not old_rel or not old_rel.endswith(".png"):
        return old_rel
    parts = old_rel.split("/", 1)
    if len(parts) != 2:
        return old_rel
    old_cat, filename = parts
    if old_cat == new_category:
        return old_rel
    src = SIGNS_DIR / old_cat / filename
    dst = SIGNS_DIR / new_category / filename
    if src.exists():
        dst.parent.mkdir(parents=True, exist_ok=True)
        if dst.exists():
            dst.unlink()
        shutil.move(str(src), str(dst))
    return f"{new_category}/{filename}"


def main() -> None:
    data = json.loads(SIGNS_JSON.read_text(encoding="utf-8"))
    changes: list[tuple[str, str, str, str]] = []

    for sign in data["signs"]:
        old = sign.get("category", "information")
        new = stvo_category(sign.get("stvo_code", ""), sign.get("de", ""))
        if old != new:
            changes.append((sign.get("stvo_code", "?"), old, new, sign["de"][:50]))
            sign["category"] = new
            if sign.get("image"):
                sign["image"] = move_png(sign["image"], new)

    SIGNS_JSON.write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print(f"Updated {len(changes)} signs:")
    for code, old, new, de in sorted(changes, key=lambda x: (x[0] or "")):
        print(f"  {code:12} {old:12} -> {new:12} | {de}")


if __name__ == "__main__":
    main()
