#!/usr/bin/env python3
"""Clean signs.json: fix junk DE titles via Wikipedia Bildtafel, drop sketches/combos."""

from __future__ import annotations

import json
import re
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RESOURCES = ROOT / "FahrPrufungDE" / "Resources"
SIGNS_DIR = RESOURCES / "Signs"
USER_AGENT = "FahrPrufungDE/1.0 (educational)"

BILDTAFEL_PAGES = [
    "Bildtafel der Verkehrszeichen in der Bundesrepublik Deutschland seit 2017",
    "Bildtafel der Zusatzzeichen in der Bundesrepublik Deutschland",
]

ENTRY_RE = re.compile(
    r"\|'''(?:Zeichen|Zusatzzeichen)\s+([\d.]+(?:-\d+)?[a-z]?)'''<br\s*/>([^\n|]+)"
)

JUNK_TITLE_RE = re.compile(r"^(Zeichen|Zusatzzeichen)\s+[\d.]")
DROP_RE = re.compile(r"Skizze|mit Zusatzzeichen", re.IGNORECASE)


def fetch_wikitext(page: str) -> str:
    url = "https://de.wikipedia.org/w/api.php?" + urllib.parse.urlencode(
        {"action": "parse", "page": page, "prop": "wikitext", "format": "json"}
    )
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = json.loads(resp.read().decode())
    return data["parse"]["wikitext"]["*"]


def official_names() -> dict[str, str]:
    names: dict[str, str] = {}
    for page in BILDTAFEL_PAGES:
        try:
            wikitext = fetch_wikitext(page)
        except Exception as exc:
            print(f"  WARN: {page}: {exc}")
            continue
        for code, name in ENTRY_RE.findall(wikitext):
            clean = re.sub(r"<[^>]+>", " ", name)
            clean = re.sub(r"\[\[(?:[^|\]]*\|)?([^\]]+)\]\]", r"\1", clean)
            clean = re.sub(r"''+", "", clean)
            clean = re.sub(r"\s+", " ", clean).strip(" ;,–-")
            if clean:
                names.setdefault(code, clean)
    return names


def main() -> None:
    data = json.loads((RESOURCES / "signs.json").read_text(encoding="utf-8"))
    signs = data["signs"]
    names = official_names()
    print(f"Official names from Bildtafel: {len(names)}")

    kept, dropped, renamed = [], [], 0
    for sign in signs:
        de = sign["de"].strip()
        code = (sign.get("stvo_code") or "").removeprefix("Z")

        if DROP_RE.search(de) or DROP_RE.search(sign["id"]):
            dropped.append(sign)
            continue

        if JUNK_TITLE_RE.match(de):
            official = names.get(code) or names.get(code.replace("_", "."))
            if official:
                sign["de"] = official
                for lang in ("ru", "en", "uk", "fr"):
                    sign[lang] = official
                sign["notes"] = {k: official for k in ("de", "ru", "en", "uk", "fr")}
                renamed += 1
            else:
                dropped.append(sign)
                continue
        kept.append(sign)

    for sign in dropped:
        for key in ("svg", "image"):
            path = SIGNS_DIR / sign[key]
            path.unlink(missing_ok=True)

    data["signs"] = kept
    data.setdefault("meta", {})["sign_count"] = len(kept)
    (RESOURCES / "signs.json").write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print(f"Renamed with official titles: {renamed}")
    print(f"Dropped: {len(dropped)} -> {[s['id'] for s in dropped]}")
    print(f"Kept: {len(kept)} signs")


if __name__ == "__main__":
    main()
