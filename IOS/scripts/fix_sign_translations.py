#!/usr/bin/env python3
"""Post-process sign titles: fix common machine-translation errors in driving terminology."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SIGNS_PATH = ROOT / "FahrPrufungDE" / "Resources" / "signs.json"

# Exact German title → correct translations (highest priority)
TITLE_GLOSSARY: dict[str, dict[str, str]] = {
    "Vorgeschriebene Fahrtrichtung – hier links": {
        "ru": "Обязательное направление — здесь налево",
        "en": "Mandatory direction — turn left here",
        "uk": "Обов'язковий напрямок — тут ліворуч",
        "fr": "Direction obligatoire — ici à gauche",
    },
    "Vorgeschriebene Fahrtrichtung – hier rechts": {
        "ru": "Обязательное направление — здесь направо",
        "en": "Mandatory direction — turn right here",
        "uk": "Обов'язковий напрямок — тут праворуч",
        "fr": "Direction obligatoire — ici à droite",
    },
    "Vorgeschriebene Fahrtrichtung – geradeaus": {
        "ru": "Обязательное направление — только прямо",
        "en": "Mandatory direction — straight ahead only",
        "uk": "Обов'язковий напрямок — лише прямо",
        "fr": "Direction obligatoire — tout droit",
    },
    "Ende der Vorfahrtstraße": {
        "ru": "Конец главной дороги",
        "en": "End of priority road",
        "uk": "Кінець головної дороги",
        "fr": "Fin de route prioritaire",
    },
    "Halt. Vorfahrt gewähren.": {
        "ru": "Стоп. Уступите дорогу.",
        "en": "Stop. Give way.",
        "uk": "Стоп. Дайте дорогу.",
        "fr": "Stop. Cédez le passage.",
    },
    "Vorfahrt gewähren.": {
        "ru": "Уступите дорогу",
        "en": "Give way",
        "uk": "Дайте дорогу",
        "fr": "Cédez le passage",
    },
}

# Regex replacements applied to already-translated text (per language)
POST_FIXES: dict[str, list[tuple[str, str]]] = {
    "ru": [
        (r"оставлено здесь", "здесь налево"),
        (r"оставленное на круг", "на круговом разъезде налево"),
        (r"оставлен", "налево"),
        (r"полосы отвода", "главной дороги"),
        (r"Уступи дорогу", "Уступите дорогу"),
        (r"Останавливаться\. Уступи", "Стоп. Уступите"),
        (r"^Табло перехода", "Табличка перенаправления"),
        (r"^Знак перехода", "Табличка перенаправления"),
        (r"Производство пол[её]тов", "Полёты вблизи аэродрома"),
    ],
    "en": [
        (r"\bleft here\b(?!\s+direction)", "turn left here"),
        (r"\bleft on the circle\b", "left at the roundabout"),
    ],
    "uk": [
        (r"залишено", "ліворуч"),
        (r"Уступи дорогу", "Дайте дорогу"),
    ],
    "fr": [
        (r"\bgauche ici\b", "ici à gauche"),
    ],
}

# German phrase fragments → per-language replacements (for titles still matching DE patterns)
DE_FRAGMENT_FIXES: list[tuple[str, dict[str, str]]] = [
    (r"hier links", {"ru": "здесь налево", "en": "turn left here", "uk": "тут ліворуч", "fr": "ici à gauche"}),
    (r"hier rechts", {"ru": "здесь направо", "en": "turn right here", "uk": "тут праворуч", "fr": "ici à droite"}),
    (r"linksweisend", {"ru": "направление налево", "en": "to the left", "uk": "ліворуч", "fr": "vers la gauche"}),
    (r"rechtsweisend", {"ru": "направление направо", "en": "to the right", "uk": "праворуч", "fr": "vers la droite"}),
    (r" – links", {"ru": " — налево", "en": " — left", "uk": " — ліворуч", "fr": " — à gauche"}),
    (r" – rechts", {"ru": " — направо", "en": " — right", "uk": " — праворуч", "fr": " — à droite"}),
    (r"Ende der Vorfahrtstraße", {"ru": "Конец главной дороги", "en": "End of priority road", "uk": "Кінець головної дороги", "fr": "Fin de route prioritaire"}),
]


def apply_post_fixes(text: str, lang: str) -> str:
    for pattern, repl in POST_FIXES.get(lang, []):
        text = re.sub(pattern, repl, text, flags=re.IGNORECASE)
    return text


def fix_from_german(sign: dict) -> bool:
    de = sign["de"]
    changed = False

    entry = TITLE_GLOSSARY.get(de)
    if entry:
        for lang, text in entry.items():
            if sign[lang] != text:
                sign[lang] = text
                changed = True
        return changed

    for pattern, translations in DE_FRAGMENT_FIXES:
        if re.search(pattern, de, re.IGNORECASE):
            for lang, fragment in translations.items():
                if lang == "ru" and sign["ru"] == de:
                    # full re-derive from DE not implemented; skip
                    continue
                if re.search(pattern, de, re.IGNORECASE) and fragment.lower() not in sign[lang].lower():
                    # only fix obvious wrong MT in ru/en when DE contains direction
                    if lang == "ru" and ("остав" in sign["ru"].lower() or sign["ru"] == sign["de"]):
                        base = sign["de"]
                        for p2, t2 in DE_FRAGMENT_FIXES:
                            base = re.sub(p2, t2["ru"], base, flags=re.IGNORECASE)
                        if base != sign["ru"]:
                            sign["ru"] = base
                            changed = True
    return changed


def main() -> None:
    data = json.loads(SIGNS_PATH.read_text(encoding="utf-8"))
    title_fixes = 0
    post_fixes = 0

    for sign in data["signs"]:
        if fix_from_german(sign):
            title_fixes += 1
        for lang in ("ru", "en", "uk", "fr"):
            fixed = apply_post_fixes(sign[lang], lang)
            if fixed != sign[lang]:
                sign[lang] = fixed
                post_fixes += 1

    SIGNS_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Glossary title fixes: {title_fixes}, post-fix replacements: {post_fixes}")


if __name__ == "__main__":
    main()
