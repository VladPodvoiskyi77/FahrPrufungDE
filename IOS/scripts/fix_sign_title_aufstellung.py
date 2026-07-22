#!/usr/bin/env python3
"""Fix mistranslated 'Aufstellung rechts/links' and related advance-plate sign titles."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SIGNS_PATH = ROOT / "FahrPrufungDE" / "Resources" / "signs.json"

# German base (before „ – Aufstellung …“) → localized short title
BASE_TITLES: dict[str, dict[str, str]] = {
    "Flugbetrieb": {
        "ru": "Полёты вблизи аэродрома",
        "en": "Low-flying aircraft",
        "uk": "Польоти біля аеродрому",
        "fr": "Vol à basse altitude",
        "tr": "Alçak uçuş",
    },
    "Fußgängerüberweg": {
        "ru": "Пешеходный переход",
        "en": "Pedestrian crossing",
        "uk": "Пішохідний перехід",
        "fr": "Passage piéton",
        "tr": "Yaya geçidi",
    },
    "Viehtrieb": {
        "ru": "Прогон скота",
        "en": "Cattle drive",
        "uk": "Перегін худоби",
        "fr": "Transhumance",
        "tr": "Hayvan sürüsü",
    },
    "Reiter": {
        "ru": "Всадники",
        "en": "Horse riders",
        "uk": "Вершники",
        "fr": "Cavaliers",
        "tr": "Atlılar",
    },
    "Amphibienwanderung": {
        "ru": "Миграция земноводных",
        "en": "Amphibian migration",
        "uk": "Міграція земноводних",
        "fr": "Migration d'amphibiens",
        "tr": "Amfibi göçü",
    },
    "Steinschlag": {
        "ru": "Камнепад",
        "en": "Falling rocks",
        "uk": "Каменепад",
        "fr": "Chutes de pierres",
        "tr": "Taş düşmesi",
    },
    "Fußgänger": {
        "ru": "Пешеходы",
        "en": "Pedestrians",
        "uk": "Пішоходи",
        "fr": "Piétons",
        "tr": "Yayalar",
    },
    "Kinder": {
        "ru": "Дети",
        "en": "Children",
        "uk": "Діти",
        "fr": "Enfants",
        "tr": "Çocuklar",
    },
    "Radverkehr": {
        "ru": "Велосипедисты",
        "en": "Cyclists",
        "uk": "Велосипедисти",
        "fr": "Cyclistes",
        "tr": "Bisikletliler",
    },
    "Wildwechsel": {
        "ru": "Выход диких животных",
        "en": "Wild animals crossing",
        "uk": "Вихід диких тварин",
        "fr": "Passage d'animaux sauvages",
        "tr": "Vahşi hayvan geçişi",
    },
    "Bahnübergang mit dreistreifiger Bake": {
        "ru": "Ж/д переезд (трёхполосный шлагбаум)",
        "en": "Level crossing (three-bar gate)",
        "uk": "Залізничний переїзд (трисмуговий шлагбаум)",
        "fr": "Passage à niveau (barrière à trois bandes)",
        "tr": "Demiryolu geçidi (üç şeritli bariyer)",
    },
    "Bahnübergang mit dreistreifiger Bake, mit Entfernungsangabe": {
        "ru": "Ж/д переезд (трёхполосный шлагбаум, с расстоянием)",
        "en": "Level crossing (three-bar gate, distance shown)",
        "uk": "Залізничний переїзд (трисмуговий шлагбаум, з відстанню)",
        "fr": "Passage à niveau (barrière à trois bandes, distance indiquée)",
        "tr": "Demiryolu geçidi (üç şeritli bariyer, mesafe belirtilmiş)",
    },
    "Dreistreifige Bake": {
        "ru": "Трёхполосный шлагбаум",
        "en": "Three-bar gate",
        "uk": "Трисмуговий шлагбаум",
        "fr": "Barrière à trois bandes",
        "tr": "Üç şeritli bariyer",
    },
    "Dreistreifige Bake mit Entfernungsangabe": {
        "ru": "Трёхполосный шлагбаум (с расстоянием)",
        "en": "Three-bar gate (distance shown)",
        "uk": "Трисмуговий шлагбаум (з відстанню)",
        "fr": "Barrière à trois bandes (distance indiquée)",
        "tr": "Üç şeritli bariyer (mesafe belirtilmiş)",
    },
    "Zweistreifige Bake": {
        "ru": "Двухполосный шлагбаум",
        "en": "Two-bar gate",
        "uk": "Двосмуговий шлагбаум",
        "fr": "Barrière à deux bandes",
        "tr": "İki şeritli bariyer",
    },
    "Zweistreifige Bake mit Entfernungsangabe": {
        "ru": "Двухполосный шлагбаум (с расстоянием)",
        "en": "Two-bar gate (distance shown)",
        "uk": "Двосмуговий шлагбаум (з відстанню)",
        "fr": "Barrière à deux bandes (distance indiquée)",
        "tr": "İki şeritli bariyer (mesafe belirtilmiş)",
    },
    "Einstreifige Bake": {
        "ru": "Однополосный шлагбаум",
        "en": "Single-bar gate",
        "uk": "Односмуговий шлагбаум",
        "fr": "Barrière à une bande",
        "tr": "Tek şeritli bariyer",
    },
    "Einstreifige Bake mit Entfernungsangabe": {
        "ru": "Однополосный шлагбаум (с расстоянием)",
        "en": "Single-bar gate (distance shown)",
        "uk": "Односмуговий шлагбаум (з відстанню)",
        "fr": "Barrière à une bande (distance indiquée)",
        "tr": "Tek şeritli bariyer (mesafe belirtilmiş)",
    },
    "Taxistand – Anfang": {
        "ru": "Стоянка такси — начало",
        "en": "Taxi stand — start",
        "uk": "Стоянка таксі — початок",
        "fr": "Station de taxis — début",
        "tr": "Taksi durağı — başlangıç",
    },
    "Taxistand – Ende": {
        "ru": "Стоянка такси — конец",
        "en": "Taxi stand — end",
        "uk": "Стоянка таксі — кінець",
        "fr": "Station de taxis — fin",
        "tr": "Taksi durağı — son",
    },
    "Taxistand – Mitte": {
        "ru": "Стоянка такси — середина",
        "en": "Taxi stand — middle",
        "uk": "Стоянка таксі — середина",
        "fr": "Station de taxis — milieu",
        "tr": "Taksi durağı — orta",
    },
    "Ladebereich – Anfang": {
        "ru": "Зона погрузки — начало",
        "en": "Loading zone — start",
        "uk": "Зона навантаження — початок",
        "fr": "Zone de chargement — début",
        "tr": "Yükleme alanı — başlangıç",
    },
    "Ladebereich – Ende": {
        "ru": "Зона погрузки — конец",
        "en": "Loading zone — end",
        "uk": "Зона навантаження — кінець",
        "fr": "Zone de chargement — fin",
        "tr": "Yükleme alanı — son",
    },
    "Ladebereich – Mitte": {
        "ru": "Зона погрузки — середина",
        "en": "Loading zone — middle",
        "uk": "Зона навантаження — середина",
        "fr": "Zone de chargement — milieu",
        "tr": "Yükleme alanı — orta",
    },
    "Radschnellweg": {
        "ru": "Велосипедная магистраль",
        "en": "Cycle highway",
        "uk": "Велосипедна магістраль",
        "fr": "Voie cyclable rapide",
        "tr": "Bisiklet otoyolu",
    },
    "Ende des Radschnellwegs": {
        "ru": "Конец велосипедной магистрали",
        "en": "End of cycle highway",
        "uk": "Кінець велосипедної магістралі",
        "fr": "Fin de voie cyclable rapide",
        "tr": "Bisiklet otoyolu sonu",
    },
}

AUFSTELLUNG_SUFFIX = {
    ("ru", "rechts"): " — предварительный указатель (справа)",
    ("ru", "links"): " — предварительный указатель (слева)",
    ("en", "rechts"): " — advance warning plate (right)",
    ("en", "links"): " — advance warning plate (left)",
    ("uk", "rechts"): " — попередній вказівник (праворуч)",
    ("uk", "links"): " — попередній вказівник (ліворуч)",
    ("fr", "rechts"): " — panneau d'annonce (à droite)",
    ("fr", "links"): " — panneau d'annonce (à gauche)",
    ("tr", "rechts"): " — ön uyarı levhası (sağda)",
    ("tr", "links"): " — ön uyarı levhası (solda)",
}

AUFSTELLUNG_RE = re.compile(r" – Aufstellung (rechts|links)$")


def fix_sign(sign: dict) -> int:
    de = sign["de"]
    m = AUFSTELLUNG_RE.search(de)
    if not m:
        return 0
    side = m.group(1)
    base_de = de[: m.start()]
    base_map = BASE_TITLES.get(base_de)
    if not base_map:
        return 0
    changed = 0
    for lang in ("ru", "en", "uk", "fr", "tr"):
        suffix = AUFSTELLUNG_SUFFIX.get((lang, side))
        base_tr = base_map.get(lang)
        if not suffix or not base_tr:
            continue
        new_title = base_tr + suffix
        if sign.get(lang) != new_title:
            sign[lang] = new_title
            changed += 1
    return changed


def main() -> None:
    data = json.loads(SIGNS_PATH.read_text(encoding="utf-8"))
    total = 0
    missing: set[str] = set()
    for sign in data["signs"]:
        de = sign["de"]
        if " – Aufstellung " in de:
            base_de = AUFSTELLUNG_RE.sub("", de)
            if base_de not in BASE_TITLES:
                missing.add(base_de)
        total += fix_sign(sign)
    SIGNS_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Fixed {total} title fields (Aufstellung → advance plate)")
    if missing:
        print("Missing BASE_TITLES entries:", ", ".join(sorted(missing)))


if __name__ == "__main__":
    main()
