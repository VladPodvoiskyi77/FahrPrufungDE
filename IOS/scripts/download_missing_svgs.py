#!/usr/bin/env python3
"""Download only missing StVO sign SVGs from Wikimedia (slow, rate-limit safe)."""

from __future__ import annotations

import json
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RESOURCES = ROOT / "FahrPrufungDE" / "Resources"
SIGNS_DIR = RESOURCES / "Signs"
SVG_DIR = ROOT / "signs-svg"
USER_AGENT = "FahrPrufungDE/1.0 (educational iOS app; local development)"
DELAY = 5.0


def download(url: str, dest: Path) -> bool:
    if dest.exists() and dest.stat().st_size > 100:
        return True
    for attempt in range(10):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=120) as resp:
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_bytes(resp.read())
            time.sleep(DELAY)
            return True
        except urllib.error.HTTPError as exc:
            if exc.code == 429:
                wait = 30 * (attempt + 1)
                print(f"  429 {dest.name}, wait {wait}s …")
                time.sleep(wait)
                continue
            print(f"  FAIL {dest.name}: {exc}")
            return False
        except Exception as exc:
            print(f"  FAIL {dest.name}: {exc}")
            return False
    return False


def main() -> None:
    data = json.loads((RESOURCES / "signs.json").read_text(encoding="utf-8"))
    missing = []
    for sign in data.get("signs", []):
        svg_path = SVG_DIR / Path(sign["svg"]).name
        if not svg_path.exists() or svg_path.stat().st_size < 100:
            missing.append(sign)

    print(f"Missing SVG: {len(missing)} / {len(data.get('signs', []))}")
    ok = 0
    for i, sign in enumerate(missing, start=1):
        url = sign.get("source_url")
        if not url:
            print(f"  skip {sign['id']}: no source_url")
            continue
        if download(url, SVG_DIR / Path(sign["svg"]).name):
            ok += 1
        print(f"  … {i}/{len(missing)} (ok {ok})")
    print(f"Downloaded {ok} SVG files")


if __name__ == "__main__":
    main()
