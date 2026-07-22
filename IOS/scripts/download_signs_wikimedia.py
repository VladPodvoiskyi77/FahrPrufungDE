#!/usr/bin/env python3
"""Download German StVO / VzKat traffic sign SVGs from Wikimedia Commons (PD-VzKat).

Official VzKat vectors from BASt are sold for manufacturing; Wikimedia hosts
public-domain recreations aligned with StVO (§ 5 Abs. 1 UrhG — amtliche Werke).
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

try:
    from deep_translator import GoogleTranslator
except ImportError:
    GoogleTranslator = None

ROOT = Path(__file__).resolve().parent.parent
RESOURCES = ROOT / "FahrPrufungDE" / "Resources"
SIGNS_DIR = RESOURCES / "Signs"
SVG_DIR = ROOT / "signs-svg"
MANIFEST_PATH = RESOURCES / "signs_wikimedia_manifest.json"

USER_AGENT = "FahrPrufungDE/1.0 (educational iOS app; local development)"
API_DELAY = 3.0
DOWNLOAD_DELAY = 2.0

CATEGORY_MAP = {
    "warning": {"de": "Gefahr", "ru": "Предупреждающие", "en": "Warning", "uk": "Попереджувальні", "fr": "Danger"},
    "prohibitory": {"de": "Verbote", "ru": "Запрещающие", "en": "Prohibitory", "uk": "Заборонні", "fr": "Interdictions"},
    "mandatory": {"de": "Gebote", "ru": "Обязательные", "en": "Mandatory", "uk": "Обов'язкові", "fr": "Obligations"},
    "information": {"de": "Hinweise", "ru": "Информационные", "en": "Information", "uk": "Інформаційні", "fr": "Informations"},
    "additional": {"de": "Zusatz", "ru": "Дополнительные", "en": "Additional", "uk": "Додаткові", "fr": "Additionnels"},
    "priority": {"de": "Vorfahrt", "ru": "Приоритет", "en": "Priority", "uk": "Перевага", "fr": "Priorité"},
    "speed": {"de": "Geschwindigkeit", "ru": "Скорость", "en": "Speed", "uk": "Швидкість", "fr": "Vitesse"},
}

TITLE_RE = re.compile(
    r"^(?:Zeichen|Zusatzzeichen)\s+([\d.]+(?:-\d+)?[a-z]?)\s*[-–]?\s*(.*?)(?:,\s*StVO.*)?$",
    re.IGNORECASE,
)
STVO_YEAR_RE = re.compile(r"StVO\s+(\d{4})")
FILE_FILTER_RE = re.compile(r"^(Zeichen|Zusatzzeichen)\s+\d", re.IGNORECASE)


def api(params: dict, retries: int = 6) -> dict:
    params = {**params, "format": "json"}
    url = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(params)
    for attempt in range(retries):
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        try:
            with urllib.request.urlopen(req, timeout=90) as resp:
                return json.loads(resp.read().decode())
        except urllib.error.HTTPError as exc:
            if exc.code == 429 and attempt < retries - 1:
                time.sleep(API_DELAY * (attempt + 2))
                continue
            raise
    raise RuntimeError("Wikimedia API failed after retries")


def category_members(title: str) -> list[dict]:
    members: list[dict] = []
    cmcontinue: str | None = None
    while True:
        params: dict = {
            "action": "query",
            "list": "categorymembers",
            "cmtitle": title,
            "cmlimit": "500",
        }
        if cmcontinue:
            params["cmcontinue"] = cmcontinue
        data = api(params)
        members.extend(data["query"]["categorymembers"])
        time.sleep(API_DELAY)
        if "continue" not in data:
            break
        cmcontinue = data["continue"]["cmcontinue"]
    return members


def collect_candidates() -> dict[str, dict]:
    """Return best Wikimedia file per sign code (prefers newer StVO revision)."""
    by_title: dict[str, dict] = {}

    categories = [
        "Category:SVG road signs in Germany",
        "Category:Diagrams of road signs of Germany",
    ]
    print("Listing category members …", flush=True)
    for cat in categories:
        print(f"  {cat}")
        for member in category_members(cat):
            if member["ns"] != 6:
                continue
            title = member["title"]
            name = title.removeprefix("File:")
            if not name.lower().endswith(".svg"):
                continue
            if not FILE_FILTER_RE.search(name):
                continue
            by_title[title] = {"title": title}

    print(f"Found {len(by_title)} candidate SVG titles", flush=True)

    # fetch URLs for category-only entries
    titles_needing_url = [t for t, v in by_title.items() if "url" not in v]
    for i in range(0, len(titles_needing_url), 40):
        batch = titles_needing_url[i : i + 40]
        data = api(
            {
                "action": "query",
                "titles": "|".join(batch),
                "prop": "imageinfo",
                "iiprop": "url|thumburl|mime|extmetadata",
                "iiurlwidth": "256",
                "iiextmetadatafilter": "LicenseShortName|Credit",
            }
        )
        for page in data.get("query", {}).get("pages", {}).values():
            if "imageinfo" not in page:
                continue
            info = page["imageinfo"][0]
            if info.get("mime") != "image/svg+xml":
                continue
            meta = info.get("extmetadata", {})
            by_title[page["title"]] = {
                "title": page["title"],
                "url": info["url"],
                "thumb_url": info.get("thumburl") or info["url"],
                "license": meta.get("LicenseShortName", {}).get("value", ""),
                "credit": meta.get("Credit", {}).get("value", ""),
            }
        time.sleep(API_DELAY * 1.5)

    best: dict[str, dict] = {}
    for item in by_title.values():
        if "url" not in item:
            continue
        parsed = parse_title(item["title"])
        if not parsed:
            continue
        code, label, year, kind = parsed
        key = f"{kind}:{code}"
        prev = best.get(key)
        if prev is None or year > prev["stvo_year"] or (year == prev["stvo_year"] and len(label) > len(prev["label"])):
            best[key] = {
                **item,
                "code": code,
                "label": label,
                "stvo_year": year,
                "kind": kind,
            }
    return best


def parse_title(title: str) -> tuple[str, str, int, str] | None:
    name = title.removeprefix("File:").removesuffix(".svg")
    kind = "zusatz" if name.lower().startswith("zusatzzeichen") else "zeichen"
    match = TITLE_RE.match(name)
    if not match:
        return None
    code = match.group(1)
    label = match.group(2).strip(" -–")
    year_match = STVO_YEAR_RE.search(name)
    year = int(year_match.group(1)) if year_match else 0
    return code, label, year, kind


def stvo_category(code: str, kind: str, de: str = "") -> str:
    if kind == "zusatz":
        return "additional"
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "fix_sign_categories",
        Path(__file__).resolve().parent / "fix_sign_categories.py",
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.stvo_category(code, de)


def slugify(code: str, label: str, kind: str) -> str:
    prefix = "z" if kind == "zusatz" else ""
    safe_label = re.sub(r"[^a-z0-9]+", "-", label.lower()).strip("-")[:40]
    code_slug = code.replace(".", "_")
    return f"{prefix}{code_slug}-{safe_label}" if safe_label else f"{prefix}{code_slug}"


def download_bytes(url: str, dest: Path, retries: int = 8) -> bool:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and dest.stat().st_size > 100:
        return True
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=120) as resp:
                dest.write_bytes(resp.read())
            time.sleep(DOWNLOAD_DELAY)
            return True
        except urllib.error.HTTPError as exc:
            if exc.code == 429 and attempt < retries - 1:
                time.sleep(15 * (attempt + 1))
                continue
            if attempt == retries - 1:
                print(f"  FAIL {dest.name}: {exc}", flush=True)
        except Exception as exc:
            if attempt == retries - 1:
                print(f"  FAIL {dest.name}: {exc}", flush=True)
            time.sleep(1.5)
    return False


def svg_to_png_local(svg_path: Path, png_path: Path, size: int = 256) -> bool:
    png_path.parent.mkdir(parents=True, exist_ok=True)
    if png_path.exists() and png_path.stat().st_size > 100:
        return True
    if not svg_path.exists() or svg_path.stat().st_size < 100:
        return False
    qlmanage = shutil.which("qlmanage")
    if not qlmanage:
        return False
    tmp_dir = png_path.parent / ".thumbs"
    tmp_dir.mkdir(exist_ok=True)
    try:
        subprocess.run(
            [qlmanage, "-t", "-s", str(size), "-o", str(tmp_dir), str(svg_path)],
            check=False,
            capture_output=True,
        )
        thumb = tmp_dir / f"{svg_path.name}.png"
        if thumb.exists():
            thumb.replace(png_path)
            return True
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)
    return False


def process_sign(item: dict, existing_by_de: dict[str, dict]) -> tuple[dict, bool, bool]:
    de = item["label"] or item["title"].removeprefix("File:").removesuffix(".svg")
    category = stvo_category(item["code"], item["kind"], de)
    sign_id = slugify(item["code"], item["label"], item["kind"])
    svg_rel = f"svg/{sign_id}.svg"
    png_rel = f"{category}/{sign_id}.png"
    svg_path = SVG_DIR / Path(svg_rel).name
    png_path = SIGNS_DIR / png_rel

    ok_svg = download_bytes(item["url"], svg_path)
    ok_png = svg_to_png_local(svg_path, png_path)

    prev = existing_by_de.get(de.strip().lower())
    ru = prev.get("ru", de) if prev else de
    en = prev.get("en", de) if prev else de
    uk = prev.get("uk", de) if prev else de
    fr = prev.get("fr", de) if prev else de

    sign = {
        "id": sign_id,
        "stvo_code": item["code"] if item["kind"] == "zeichen" else f"Z{item['code']}",
        "shape": None,
        "image": png_rel,
        "svg": svg_rel,
        "de": de,
        "ru": ru,
        "en": en,
        "uk": uk,
        "fr": fr,
        "category": category,
        "source_url": item["url"],
        "wikimedia_title": item.get("title"),
        "license": item.get("license") or "Public domain (PD-VzKat / StVO)",
        "notes": {"de": de, "ru": ru, "en": en, "uk": uk, "fr": fr},
    }
    return sign, ok_svg, ok_png


def translate_batch(texts: list[str], target: str, source: str = "de") -> list[str]:
    if not texts or GoogleTranslator is None:
        return texts
    translator = GoogleTranslator(source=source, target=target)
    out: list[str] = []
    for text in texts:
        try:
            out.append(translator.translate(text))
            time.sleep(0.08)
        except Exception:
            out.append(text)
    return out


def load_existing_translations() -> dict[str, dict]:
    path = RESOURCES / "signs.json"
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    by_de: dict[str, dict] = {}
    for sign in data.get("signs", []):
        de = sign.get("de", "").strip().lower()
        if de:
            by_de[de] = sign
    return by_de


def thumb_from_svg_url(url: str, width: int = 256) -> str:
    if "/thumb/" in url:
        return url
    marker = "/wikipedia/commons/"
    idx = url.find(marker)
    if idx == -1:
        return url
    rest = url[idx + len(marker) :]
    parts = rest.split("/")
    filename = parts[-1]
    dirpath = "/".join(parts[:-1])
    return (
        f"https://upload.wikimedia.org/wikipedia/commons/thumb/{dirpath}/{filename}/"
        f"{width}px-{filename}.png"
    )


def load_manifest_items() -> list[dict] | None:
    path = RESOURCES / "signs.json"
    if not path.exists():
        return None
    data = json.loads(path.read_text(encoding="utf-8"))
    if not data.get("version", "").startswith("3.") or not data.get("signs"):
        return None
    items = []
    for sign in data["signs"]:
        source = sign.get("source_url")
        if not source:
            return None
        code = sign.get("stvo_code") or sign["id"]
        kind = "zusatz" if str(code).startswith("Z") else "zeichen"
        code_value = str(code).removeprefix("Z")
        items.append(
            {
                "title": sign.get("wikimedia_title") or sign["id"],
                "url": source,
                "thumb_url": sign.get("thumb_url") or thumb_from_svg_url(source),
                "code": code_value,
                "label": sign["de"],
                "kind": kind,
                "license": sign.get("license", ""),
            }
        )
    return items


def main() -> None:
    SVG_DIR.mkdir(parents=True, exist_ok=True)
    existing_by_de = load_existing_translations()

    cached = load_manifest_items()
    if cached:
        print(f"Resuming from signs.json ({len(cached)} signs) …", flush=True)
        items = cached
        best = None
    else:
        best = collect_candidates()
        print(f"Unique sign codes after dedup: {len(best)}", flush=True)
        items = sorted(best.values(), key=lambda x: (x["kind"], x["code"]))

    downloaded_svg = 0
    downloaded_png = 0
    print(f"Downloading {len(items)} signs sequentially …", flush=True)

    signs = []
    for i, item in enumerate(items, start=1):
        sign, ok_svg, ok_png = process_sign(item, existing_by_de)
        signs.append(sign)
        downloaded_svg += int(ok_svg)
        downloaded_png += int(ok_png)
        if i % 5 == 0 or i == len(items):
            print(f"  … {i}/{len(items)} (svg {downloaded_svg}, png {downloaded_png})", flush=True)

    categories = [
        {"id": key, **labels}
        for key, labels in CATEGORY_MAP.items()
        if any(s["category"] == key for s in signs)
    ]

    manifest = {
        "version": "3.0.0",
        "description": "German StVO traffic signs — SVG source (Wikimedia Commons, PD-VzKat)",
        "source": "https://commons.wikimedia.org/wiki/Category:SVG_road_signs_in_Germany",
        "source_note": (
            "Vectors recreated from official StVO / VzKat specifications. "
            "Amtliche Werke — public domain in Germany (§ 5 Abs. 1 UrhG). "
            "Wikimedia license: PD-VzKat."
        ),
        "categories": categories,
        "signs": signs,
        "meta": {
            "sign_count": len(signs),
            "svg_downloaded": downloaded_svg,
            "png_generated": downloaded_png,
        },
    }

    signs_json = RESOURCES / "signs.json"
    signs_json.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    MANIFEST_PATH.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"SVG → {SVG_DIR} ({downloaded_svg} files)", flush=True)
    print(f"PNG → {SIGNS_DIR} ({downloaded_png} files)", flush=True)
    print(f"Wrote {len(signs)} signs → {signs_json}", flush=True)


if __name__ == "__main__":
    main()
