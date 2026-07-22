#!/usr/bin/env python3
"""Generate PNG previews from SVG sign files via rsvg-convert.

Preserves aspect ratio, transparent background. Requires: brew install librsvg
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RESOURCES = ROOT / "FahrPrufungDE" / "Resources"
SIGNS_DIR = RESOURCES / "Signs"
SVG_DIR = ROOT / "signs-svg"
TARGET_SIZE = 512

RSVG = shutil.which("rsvg-convert")


def svg_to_png(svg_path: Path, png_path: Path, force: bool = False) -> bool:
    if not svg_path.exists() or svg_path.stat().st_size < 100:
        return False
    if png_path.exists() and png_path.stat().st_size > 100 and not force:
        return True
    png_path.parent.mkdir(parents=True, exist_ok=True)
    result = subprocess.run(
        [
            RSVG,
            "--keep-aspect-ratio",
            "--width", str(TARGET_SIZE),
            "--height", str(TARGET_SIZE),
            "--output", str(png_path),
            str(svg_path),
        ],
        capture_output=True,
    )
    if result.returncode == 0 and png_path.exists():
        return True
    # Fallback for SVGs that exceed librsvg's nesting limit
    try:
        import cairosvg

        cairosvg.svg2png(
            url=str(svg_path),
            write_to=str(png_path),
            output_width=TARGET_SIZE,
        )
        return True
    except Exception as exc:
        print(f"  FAIL {svg_path.name}: {str(exc)[:120]}")
        return False


def main() -> None:
    if not RSVG:
        sys.exit("rsvg-convert not found — run: brew install librsvg")

    force = "--force" in sys.argv
    data = json.loads((RESOURCES / "signs.json").read_text(encoding="utf-8"))
    ok = fail = 0
    for i, sign in enumerate(data.get("signs", []), start=1):
        if svg_to_png(SVG_DIR / Path(sign["svg"]).name, SIGNS_DIR / sign["image"], force=force):
            ok += 1
        else:
            fail += 1
        if i % 50 == 0:
            print(f"  … {i} (ok {ok}, fail {fail})")
    print(f"Done: {ok} PNG, {fail} failed")


if __name__ == "__main__":
    main()
