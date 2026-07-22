#!/usr/bin/env python3
"""Translate sign titles in signs.json from German to ru/en/uk/fr.

Uses a curated glossary for key driving-exam terminology, falls back to
deep-translator (Google) for the rest. Re-runnable: only translates
entries where the target language still equals the German source.
"""

from __future__ import annotations

import json
import time
from pathlib import Path

from deep_translator import GoogleTranslator

ROOT = Path(__file__).resolve().parent.parent
RESOURCES = ROOT / "FahrPrufungDE" / "Resources"
TARGETS = ("ru", "en", "uk", "fr", "tr")

# Curated translations for core exam terminology (override machine output)
GLOSSARY: dict[str, dict[str, str]] = {
    "Halt. Vorfahrt gewähren.": {
        "ru": "Стоп. Уступите дорогу.",
        "en": "Stop. Give way.",
        "uk": "Стоп. Дайте дорогу.",
        "fr": "Stop. Cédez le passage.",
        "tr": "Dur. Yol ver.",
    },
    "Vorfahrt gewähren.": {
        "ru": "Уступите дорогу",
        "en": "Give way",
        "uk": "Дайте дорогу",
        "fr": "Cédez le passage",
        "tr": "Yol ver",
    },
    "Vorfahrt": {
        "ru": "Преимущество на следующем перекрёстке",
        "en": "Priority at next intersection",
        "uk": "Перевага на наступному перехресті",
        "fr": "Priorité à la prochaine intersection",
        "tr": "Sonraki kavşakta geçiş önceliği",
    },
    "Vorfahrtstraße": {
        "ru": "Главная дорога",
        "en": "Priority road",
        "uk": "Головна дорога",
        "fr": "Route prioritaire",
        "tr": "Ana yol",
    },
    "Einbahnstraße, linksweisend": {
        "ru": "Одностороннее движение (налево)",
        "en": "One-way street (left)",
        "uk": "Односторонній рух (ліворуч)",
        "fr": "Sens unique (vers la gauche)",
        "tr": "Tek yön (sola)",
    },
    "Einbahnstraße, rechtsweisend": {
        "ru": "Одностороннее движение (направо)",
        "en": "One-way street (right)",
        "uk": "Односторонній рух (праворуч)",
        "fr": "Sens unique (vers la droite)",
        "tr": "Tek yön (sağa)",
    },
    "Ortstafel Vorderseite": {
        "ru": "Начало населённого пункта",
        "en": "Town sign (entry)",
        "uk": "Початок населеного пункту",
        "fr": "Entrée d'agglomération",
        "tr": "Yerleşim yeri başlangıcı",
    },
    "Ortstafel Rückseite": {
        "ru": "Конец населённого пункта",
        "en": "Town sign (exit)",
        "uk": "Кінець населеного пункту",
        "fr": "Sortie d'agglomération",
        "tr": "Yerleşim yeri sonu",
    },
}


def translate_batch(texts: list[str], target: str) -> list[str]:
    translator = GoogleTranslator(source="de", target=target)
    out: list[str] = []
    for text in texts:
        try:
            out.append(translator.translate(text) or text)
            time.sleep(0.06)
        except Exception:
            out.append(text)
    return out


def main() -> None:
    path = RESOURCES / "signs.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    signs = data["signs"]

    for lang in TARGETS:
        pending = [s for s in signs if s[lang] == s["de"] and s["de"].strip()]
        glossary_hits = 0
        to_translate = []
        for sign in pending:
            entry = GLOSSARY.get(sign["de"])
            if entry and lang in entry:
                sign[lang] = entry[lang]
                glossary_hits += 1
            else:
                to_translate.append(sign)

        print(f"{lang}: glossary {glossary_hits}, machine {len(to_translate)}")
        translated = translate_batch([s["de"] for s in to_translate], lang)
        for sign, text in zip(to_translate, translated):
            sign[lang] = text.strip().rstrip(".")

        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"  saved after {lang}")

    print("Done")


if __name__ == "__main__":
    main()
