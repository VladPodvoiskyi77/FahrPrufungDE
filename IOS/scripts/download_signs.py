#!/usr/bin/env python3
"""Download German traffic sign images and metadata from traffic-rules.com."""

from __future__ import annotations

import json
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path

try:
    from deep_translator import GoogleTranslator
except ImportError:
    GoogleTranslator = None

ROOT = Path(__file__).resolve().parent.parent
SIGNS_DIR = ROOT / "FahrPrufungDE" / "Resources" / "Signs"
RESOURCES = ROOT / "FahrPrufungDE" / "Resources"

LOCALES = {
    "ru": "https://traffic-rules.com/ru-de/%D0%BA%D0%BD%D0%B8%D0%B3%D0%B0/traffic-signs",
    "en": "https://traffic-rules.com/en-de/book/traffic-signs",
    "uk": "https://traffic-rules.com/uk-de/book/traffic-signs",
    "fr": "https://traffic-rules.com/fr-de/book/traffic-signs",
}

CATEGORY_MAP = {
    "warning": {"de": "Gefahr", "ru": "Предупреждающие", "en": "Warning", "uk": "Попереджувальні", "fr": "Danger"},
    "prohibitory": {"de": "Verbote", "ru": "Запрещающие", "en": "Prohibitory", "uk": "Заборонні", "fr": "Interdictions"},
    "mandatory": {"de": "Gebote", "ru": "Обязательные", "en": "Mandatory", "uk": "Обов'язкові", "fr": "Obligations"},
    "information": {"de": "Hinweise", "ru": "Информационные", "en": "Information", "uk": "Інформаційні", "fr": "Informations"},
    "additional": {"de": "Zusatz", "ru": "Дополнительные", "en": "Additional", "uk": "Додаткові", "fr": "Additionnels"},
    "priority": {"de": "Vorfahrt", "ru": "Приоритет", "en": "Priority", "uk": "Перевага", "fr": "Priorité"},
    "speed": {"de": "Geschwindigkeit", "ru": "Скорость", "en": "Speed", "uk": "Швидкість", "fr": "Vitesse"},
}

IMG_PATTERN = re.compile(
    r'<img title="([^"]*)"[^>]*src="(/img/traffic-rules/Traffic signs/de/[^"]+)"[^>]*id="([^"]+)"',
    re.IGNORECASE,
)


def fetch_html(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "FahrPrufungDE/1.0 (educational)"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read().decode("utf-8", errors="ignore")


def parse_signs(html: str) -> dict[str, str]:
    return {path: title for title, path, _ in IMG_PATTERN.findall(html)}


def sign_id_from_path(path: str) -> str:
    filename = Path(path).stem
    return filename


def category_from_path(path: str) -> str:
    parts = Path(path).parts
    # /img/traffic-rules/Traffic signs/de/warning/warning-crossroad.png
    if len(parts) >= 2:
        folder = parts[-2].lower()
        if folder in CATEGORY_MAP:
            return folder
    return "information"


def image_url(path: str) -> str:
    return "https://traffic-rules.com" + urllib.parse.quote(path, safe="/:")


def download_image(path: str, dest: Path) -> bool:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and dest.stat().st_size > 0:
        return True
    url = image_url(path)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "FahrPrufungDE/1.0"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            dest.write_bytes(resp.read())
        return True
    except Exception as exc:
        print(f"  FAIL {dest.name}: {exc}")
        return False


def translate_batch(texts: list[str], target: str, source: str = "en") -> list[str]:
    if not texts:
        return []
    if GoogleTranslator is None:
        return texts
    translator = GoogleTranslator(source=source, target=target)
    out: list[str] = []
    for text in texts:
        try:
            out.append(translator.translate(text))
            time.sleep(0.05)
        except Exception:
            out.append(text)
    return out


def relative_image_path(full_path: str) -> str:
    marker = "/de/"
    idx = full_path.find(marker)
    if idx == -1:
        return Path(full_path).name
    return full_path[idx + len(marker) :]


def main():
    print("Fetching metadata from traffic-rules.com …")
    by_locale: dict[str, dict[str, str]] = {}
    for lang, url in LOCALES.items():
        print(f"  {lang}: {url}")
        by_locale[lang] = parse_signs(fetch_html(url))

    all_paths = sorted(set(by_locale["en"].keys()))
    # Skip category header icons (single segment under de/)
    all_paths = [p for p in all_paths if p.count("/") >= 2 or "/" in relative_image_path(p)]

    print(f"Found {len(all_paths)} signs")

    en_titles = [by_locale["en"].get(p, "") for p in all_paths]
    print("Translating to German …")
    de_titles = translate_batch(en_titles, "de", "en")

    signs = []
    downloaded = 0
    for i, path in enumerate(all_paths):
        rel = relative_image_path(path)
        sid = sign_id_from_path(path)
        category = category_from_path(path)

        dest = SIGNS_DIR / rel
        if download_image(path, dest):
            downloaded += 1

        en = by_locale["en"].get(path, "").strip()
        ru = by_locale["ru"].get(path, en).strip()
        uk = by_locale["uk"].get(path, en).strip()
        fr = by_locale["fr"].get(path, en).strip()
        de = de_titles[i].strip() if i < len(de_titles) else en

        stvo_code = None
        code_match = re.search(r"/([A-Z]\d{4})-", path)
        if code_match:
            stvo_code = code_match.group(1)

        signs.append({
            "id": sid,
            "stvo_code": stvo_code,
            "shape": None,
            "image": rel,
            "de": de.rstrip("."),
            "ru": ru.rstrip("."),
            "en": en.rstrip("."),
            "uk": uk.rstrip("."),
            "fr": fr.rstrip("."),
            "category": category,
            "notes": {
                "de": de,
                "ru": ru,
                "en": en,
                "uk": uk,
                "fr": fr,
            },
        })

        if (i + 1) % 50 == 0:
            print(f"  … {i + 1}/{len(all_paths)}")

    categories = [
        {"id": k, **v}
        for k, v in CATEGORY_MAP.items()
        if any(s["category"] == k for s in signs)
    ]

    bundle = {
        "version": "2.0.0",
        "description": "German traffic signs with official PNG images",
        "source": "https://traffic-rules.com/ru-de/книга/traffic-signs",
        "source_note": "Images used for educational purposes. © traffic-rules.com",
        "categories": categories,
        "signs": signs,
        "meta": {"sign_count": len(signs), "images_downloaded": downloaded},
    }

    signs_json = RESOURCES / "signs.json"
    with open(signs_json, "w", encoding="utf-8") as f:
        json.dump(bundle, f, ensure_ascii=False, indent=2)

    print(f"Downloaded {downloaded} images → {SIGNS_DIR}")
    print(f"Wrote {len(signs)} signs → {signs_json}")


if __name__ == "__main__":
    main()
