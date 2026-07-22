#!/usr/bin/env python3
"""Add missing StVO signs using the Wikipedia Bildtafel (file name + official title)."""

from __future__ import annotations

import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RESOURCES = ROOT / "FahrPrufungDE" / "Resources"
SIGNS_DIR = RESOURCES / "Signs"
SVG_DIR = ROOT / "signs-svg"
USER_AGENT = "FahrPrufungDE/1.0 (educational)"

PAGE = "Bildtafel der Verkehrszeichen in der Bundesrepublik Deutschland seit 2017"

# code -> (filename, name)
GALLERY_RE = re.compile(
    r"^([^|\n]+\.svg)\|'''Zeichen\s+([\d.]+(?:-\d+)?[a-z]?)'''<br\s*/>([^\n]+)",
    re.MULTILINE,
)

# Empty list means: import every sign from the Bildtafel that is missing.
WANTED_CODES: list[str] = []


def fetch_wikitext(page: str) -> str:
    url = "https://de.wikipedia.org/w/api.php?" + urllib.parse.urlencode(
        {"action": "parse", "page": page, "prop": "wikitext", "format": "json"}
    )
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode())["parse"]["wikitext"]["*"]


def clean_name(raw: str) -> str:
    text = re.sub(r"<[^>]+>", " ", raw)
    text = re.sub(r"\[\[(?:[^|\]]*\|)?([^\]]+)\]\]", r"\1", text)
    text = re.sub(r"''+", "", text)
    text = text.replace("&shy;", "").replace("&nbsp;", " ").replace("&amp;", "&")
    return re.sub(r"\s+", " ", text).strip(" ;,–-")


def slugify(code: str, label: str) -> str:
    safe = re.sub(r"[^a-z0-9]+", "-", label.lower()).strip("-")[:40]
    code_slug = code.replace(".", "_")
    return f"{code_slug}-{safe}" if safe else code_slug


def stvo_category(code: str, de: str = "") -> str:
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "fix_sign_categories",
        Path(__file__).resolve().parent / "fix_sign_categories.py",
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.stvo_category(code, de)


def resolve_direct_urls(filenames: list[str]) -> dict[str, str]:
    """Batch-resolve Commons file names to direct upload.wikimedia.org URLs."""
    urls: dict[str, str] = {}
    for i in range(0, len(filenames), 50):
        batch = filenames[i : i + 50]
        query = urllib.parse.urlencode(
            {
                "action": "query",
                "titles": "|".join(f"File:{name}" for name in batch),
                "prop": "imageinfo",
                "iiprop": "url",
                "format": "json",
            }
        )
        req = urllib.request.Request(
            "https://commons.wikimedia.org/w/api.php?" + query,
            headers={"User-Agent": USER_AGENT},
        )
        with urllib.request.urlopen(req, timeout=60) as resp:
            payload = json.loads(resp.read().decode())
        normalized = {
            n["to"]: n["from"]
            for n in payload.get("query", {}).get("normalized", [])
        }
        for page in payload.get("query", {}).get("pages", {}).values():
            title = normalized.get(page.get("title"), page.get("title", ""))
            info = page.get("imageinfo")
            if info:
                urls[title.removeprefix("File:")] = info[0]["url"]
        time.sleep(2)
    return urls


def download(url: str, dest: Path) -> bool:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and dest.stat().st_size > 100:
        return True
    for attempt in range(5):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=120) as resp:
                dest.write_bytes(resp.read())
            time.sleep(1.5)
            return True
        except urllib.error.HTTPError as exc:
            if exc.code == 429:
                time.sleep(15 * (attempt + 1))
                continue
            print(f"  FAIL {dest.name}: {exc}")
            return False
        except Exception as exc:
            print(f"  FAIL {dest.name}: {exc}")
            return False
    return False


def main() -> None:
    data = json.loads((RESOURCES / "signs.json").read_text(encoding="utf-8"))
    existing_codes = {s.get("stvo_code") for s in data["signs"]}

    wikitext = fetch_wikitext(PAGE)
    catalog: dict[str, tuple[str, str]] = {}
    for filename, code, raw_name in GALLERY_RE.findall(wikitext):
        clean_file = filename.strip()
        for prefix in ("Datei:", "File:"):
            clean_file = clean_file.removeprefix(prefix)
        catalog.setdefault(code, (clean_file, clean_name(raw_name)))

    print(f"Bildtafel catalog entries: {len(catalog)}")

    wanted = WANTED_CODES or sorted(catalog.keys())
    existing_ids = {s["id"] for s in data["signs"]}

    missing = [
        code
        for code in wanted
        if code not in existing_codes
        and f"Z{code}" not in existing_codes
        and code in catalog
        and slugify(code, catalog[code][1]) not in existing_ids
    ]
    print(f"Missing signs to import: {len(missing)}")

    direct_urls = resolve_direct_urls([catalog[code][0] for code in missing])
    print(f"Resolved direct URLs: {len(direct_urls)}")

    added = 0
    for code in missing:
        filename, name = catalog[code]
        sign_id = slugify(code, name)
        category = stvo_category(code, name)
        svg_rel = f"svg/{sign_id}.svg"
        png_rel = f"{category}/{sign_id}.png"

        file_url = direct_urls.get(filename)
        if not file_url:
            print(f"  no URL for {filename}")
            continue
        if not download(file_url, SVG_DIR / f"{sign_id}.svg"):
            continue

        data["signs"].append(
            {
                "id": sign_id,
                "stvo_code": code,
                "shape": None,
                "image": png_rel,
                "svg": svg_rel,
                "de": name,
                "ru": name,
                "en": name,
                "uk": name,
                "fr": name,
                "category": category,
                "source_url": file_url,
                "wikimedia_title": f"File:{filename}",
                "license": "Public domain (PD-VzKat / StVO)",
                "notes": {k: name for k in ("de", "ru", "en", "uk", "fr")},
            }
        )
        existing_ids.add(sign_id)
        added += 1
        print(f"  + {code}: {name}")
        if added % 25 == 0:
            data["signs"].sort(key=lambda s: (s.get("stvo_code") or "").removeprefix("Z"))
            (RESOURCES / "signs.json").write_text(
                json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
            )

    data["signs"].sort(key=lambda s: (s.get("stvo_code") or "").removeprefix("Z"))
    data.setdefault("meta", {})["sign_count"] = len(data["signs"])
    (RESOURCES / "signs.json").write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"Added {added}, total {len(data['signs'])}")


if __name__ == "__main__":
    main()
