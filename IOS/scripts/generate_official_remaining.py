#!/usr/bin/env python3
"""Generate technical + phrase official translation modules from vocabulary."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VOCAB = ROOT / "FahrPrufungDE" / "Resources" / "vocabulary.json"
SCRIPTS = Path(__file__).resolve().parent

# Formal TR replacements for examiner phrases (Sie-form / official)
TR_PHRASE_FIXES = {
    "Lütfen bana kimliğini göster": "Lütfen kimlik belgenizi gösteriniz",
    "Bugün sana yolu göstereceğim": "Bugün güzergâhı size bildireceğim",
    "Sen geçtin": "Sınavı geçtiniz",
    "İyi iş çıkardın": "Başarılı bir performans sergilediniz",
    "Bunu tekrar edebilir misiniz?": "Bunu tekrar eder misiniz?",
    "Maalesef geçemediniz": "Maalesef sınavı geçemediniz",
    "Geçiş önceliğine uymadınız": "Geçiş üstünlüğüne uymadınız",
    "Temel sürüş görevleri hatalıydı": "Temel sürüş manevraları hatalıydı",
}

# Official RU phrase polish
RU_PHRASE_FIXES = {
    "Покажите удостоверение личности.": "Предъявите документ, удостоверяющий личность.",
    "Чувствуете ли вы себя готовым сдавать экзамен?": "Считаете ли Вы себя способным сдать экзамен?",
    "Вы сдали.": "Экзамен сдан.",
    "Вы молодец.": "Экзамен сдан успешно.",
    "К сожалению, вы не сдали.": "К сожалению, экзамен не сдан.",
    "Вы не уступили дорогу.": "Не предоставлено преимущество в движении.",
    "Базовые упражнения выполнены с ошибками.": "Основные маневровые задания выполнены с нарушениями.",
    "Обратите внимание на преимущество проезда.": "Соблюдайте преимущество в движении.",
}

EN_PHRASE_FIXES = {
    "You have passed.": "You have passed the examination.",
    "Well done.": "Examination passed successfully.",
    "Unfortunately, you have not passed.": "Unfortunately, you have not passed the examination.",
    "You failed to give way.": "You failed to yield right of way.",
    "The basic driving tasks were incorrect.": "The basic manoeuvre tasks were not performed correctly.",
    "Pay attention to right of way.": "Observe right of way.",
}

UK_PHRASE_FIXES = {
    "Покажіть посвідчення особи.": "Пред'явіть документ, що посвідчує особу.",
    "Ви склали.": "Іспит складено.",
    "Ви молодець.": "Іспит складено успішно.",
    "На жаль, ви не склали.": "На жаль, іспит не складено.",
    "Ви не поступилися дорогою.": "Не надано перевагу в русі.",
    "Базові вправи виконані з помилками.": "Основні маневрові завдання виконано з порушеннями.",
    "Зверніть увагу на перевагу руху.": "Дотримуйтесь переваги в русі.",
}

FR_PHRASE_FIXES: dict[str, str] = {}

PHRASE_OVERRIDES: dict[str, dict[str, str]] = {
    "phrase_vorfahrtsstrasse": {
        "ru": "Следуйте по дороге с преимущественным правом проезда.",
        "en": "Please follow the priority road.",
        "uk": "Рухайтеся дорогою з переважним правом проїзду.",
        "fr": "Veuillez suivre la route prioritaire.",
        "tr": "Lütfen öncelikli yoldan devam ediniz.",
    },
    "phrase_grundfahraufgaben": {
        "ru": "Основные маневровые задания выполнены с нарушениями.",
        "en": "The basic manoeuvre tasks were not performed correctly.",
        "uk": "Основні маневрові завдання виконано з порушеннями.",
        "fr": "Les manœuvres de base n'ont pas été exécutées correctement.",
        "tr": "Temel sürüş manevraları usulüne uygun yapılmamıştır.",
    },
    "phrase_spiegel_blinker_schulter": {
        "ru": "Зеркало — указатель поворота — контрольный обзор через плечо.",
        "en": "Mirror — indicator — shoulder check.",
        "uk": "Дзеркало — вказівник повороту — контрольний огляд через плече.",
        "fr": "Rétroviseur — clignotant — contrôle de l'angle mort.",
        "tr": "Ayna — sinyal — omuz üzerinden kontrol.",
    },
}

# Technical / maneuver official overrides (id -> langs)
TECHNICAL_OVERRIDES: dict[str, dict[str, str]] = {
    "schulterblick": {
        "ru": "Контрольный обзор через плечо (Schulterblick)",
        "en": "Shoulder check (blind spot check)",
        "uk": "Контрольний огляд через плече (Schulterblick)",
        "fr": "Contrôle de l'angle mort (Schulterblick)",
        "tr": "Omuz üzerinden kontrol (Schulterblick)",
    },
    "vorfahrt_gewaehren": {
        "ru": "Предоставить преимущество в движении",
        "en": "Yield right of way",
        "uk": "Надати перевагу в русі",
        "fr": "Céder la priorité",
        "tr": "Geçiş üstünlüğü vermek",
    },
    "betriebsbremse": {
        "ru": "Рабочая тормозная система",
        "en": "Service brake (foot brake)",
        "uk": "Робоча гальмівна система",
        "fr": "Frein de service",
        "tr": "Hizmet freni",
    },
    "feststellbremse": {
        "ru": "Стояночная тормозная система",
        "en": "Parking brake / handbrake",
        "uk": "Стоянкова гальмівна система",
        "fr": "Frein de stationnement",
        "tr": "Park freni",
    },
    "verkehrssicher": {
        "ru": "Соответствие требованиям безопасности дорожного движения",
        "en": "Roadworthy / fit for road use",
        "uk": "Відповідність вимогам безпеки дорожнього руху",
        "fr": "En état de circuler en sécurité",
        "tr": "Trafik güvenliğine uygun",
    },
    "gefahrenbremsung": {
        "ru": "Экстренное торможение",
        "en": "Emergency braking",
        "uk": "Екстрене гальмування",
        "fr": "Freinage d'urgence",
        "tr": "Acil frenleme",
    },
    "anfahren": {
        "ru": "Начало движения",
        "en": "Moving off",
        "uk": "Початок руху",
        "fr": "Démarrer (mise en mouvement)",
        "tr": "Harekete başlama",
    },
    "anhalten": {
        "ru": "Остановка транспортного средства",
        "en": "Stopping the vehicle",
        "uk": "Зупинка транспортного засобу",
        "fr": "Arrêt du véhicule",
        "tr": "Aracı durdurma",
    },
    "wenden": {
        "ru": "Разворот в противоположном направлении",
        "en": "Turning around (reversing direction)",
        "uk": "Розворот у протилежному напрямку",
        "fr": "Demi-tour",
        "tr": "Yön değiştirerek dönme",
    },
    "sich_einordnen": {
        "ru": "Занять положение на проезжей части",
        "en": "Take up position on the carriageway",
        "uk": "Зайняти положення на проїзній частині",
        "fr": "Se placer sur la chaussée",
        "tr": "Taşıt yolunda konum alma",
    },
    "sich_rechts_einordnen": {
        "ru": "Занять крайнее правое положение",
        "en": "Take up position on the right",
        "uk": "Зайняти крайнє праве положення",
        "fr": "Se placer à droite",
        "tr": "Sağ şeride yanaşma",
    },
    "schrittgeschwindigkeit": {
        "ru": "Скорость пешеходного шага (Schrittgeschwindigkeit)",
        "en": "Walking pace speed (Schrittgeschwindigkeit)",
        "uk": "Швидкість пішохідного кроку (Schrittgeschwindigkeit)",
        "fr": "Allure au pas (Schrittgeschwindigkeit)",
        "tr": "Yürüme hızı (Schrittgeschwindigkeit)",
    },
    "passgeschwindigkeit": {
        "ru": "Минимальная скорость движения (Passgeschwindigkeit)",
        "en": "Minimum manoeuvring speed (Passgeschwindigkeit)",
        "uk": "Мінімальна швидкість руху (Passgeschwindigkeit)",
        "fr": "Vitesse minimale de manœuvre (Passgeschwindigkeit)",
        "tr": "Minimum manevra hızı (Passgeschwindigkeit)",
    },
    "assistenzsystem": {
        "ru": "Система помощи водителю",
        "en": "Driver assistance system",
        "uk": "Система допомоги водію",
        "fr": "Système d'aide à la conduite",
        "tr": "Sürücü destek sistemi",
    },
    "warndreieck": {
        "ru": "Знак аварийной остановки",
        "en": "Warning triangle",
        "uk": "Знак аварійної зупинки",
        "fr": "Triangle de pré-signalisation",
        "tr": "Uyarı üçgeni",
    },
    "warnweste": {
        "ru": "Световозвращающий жилет",
        "en": "High-visibility warning vest",
        "uk": "Світловідбивний жилет",
        "fr": "Gilet de sécurité haute visibilité",
        "tr": "Uyarı yeleği",
    },
    "pkw": {
        "ru": "Легковой автомобиль (PKW)",
        "en": "Passenger motor vehicle (PKW)",
        "uk": "Легковий автомобіль (PKW)",
        "fr": "Véhicule particulier (PKW)",
        "tr": "Binek otomobil (PKW)",
    },
    "totwinkel": {
        "ru": "Мёртвая зона (слепая зона)",
        "en": "Blind spot",
        "uk": "Мертва зона (сліпа зона)",
        "fr": "Angle mort",
        "tr": "Kör nokta",
    },
    "sicherheitsgurt": {
        "ru": "Ремень безопасности",
        "en": "Seat belt",
        "uk": "Ремінь безпеки",
        "fr": "Ceinture de sécurité",
        "tr": "Emniyet kemeri",
    },
    "technische_frage": {
        "ru": "Вопрос по технической части экзамена",
        "en": "Technical examination question",
        "uk": "Питання з технічної частини іспиту",
        "fr": "Question technique d'examen",
        "tr": "Teknik sınav sorusu",
    },
}


def load_core_ids() -> set[str]:
    text = (SCRIPTS / "official_translation_data.py").read_text(encoding="utf-8")
    return set(re.findall(r'"([a-z0-9_]+)":\s*\{', text))


def officialize_phrase(term: dict) -> dict[str, str]:
    if term["id"] in PHRASE_OVERRIDES:
        return PHRASE_OVERRIDES[term["id"]]

    ru = RU_PHRASE_FIXES.get(term["ru"], term["ru"])
    en = EN_PHRASE_FIXES.get(term["en"], term["en"])
    uk = UK_PHRASE_FIXES.get(term["uk"], term["uk"])
    fr = FR_PHRASE_FIXES.get(term["fr"], term["fr"])
    tr = term["tr"]
    for old, new in TR_PHRASE_FIXES.items():
        if old in tr:
            tr = tr.replace(old, new)

    de = term["de"]
    if re.search(r"\bBitte\b", de, re.I) and not en.lower().startswith("please"):
        en = f"Please {en[0].lower()}{en[1:]}" if en else en
    if de.startswith("Zeigen Sie") and en.lower().startswith("show "):
        en = "Please " + en[0].lower() + en[1:]

    # Formal address in Russian examiner instructions
    ru = re.sub(r"\bвы\b", "Вы", ru)
    ru = re.sub(r"\bвас\b", "Вас", ru)
    ru = re.sub(r"\bвам\b", "Вам", ru)

    return {"ru": ru, "en": en, "uk": uk, "fr": fr, "tr": tr}


def officialize_technical(term: dict) -> dict[str, str]:
    if term["id"] in TECHNICAL_OVERRIDES:
        base = TECHNICAL_OVERRIDES[term["id"]]
        return {
            lang: base.get(lang, term[lang])
            for lang in ("ru", "en", "uk", "fr", "tr")
        }
    # Keep current but ensure formal register markers for legal driving terms
    return {lang: term[lang] for lang in ("ru", "en", "uk", "fr", "tr")}


def write_module(path: Path, var_name: str, data: dict) -> None:
    lines = [
        f'{var_name}: dict[str, dict[str, str]] = {{',
    ]
    for tid, langs in sorted(data.items()):
        lines.append(f'    "{tid}": {{')
        for lang in ("ru", "en", "uk", "fr", "tr"):
            val = langs[lang].replace("\\", "\\\\").replace('"', '\\"')
            lines.append(f'        "{lang}": "{val}",')
        lines.append("    },")
    lines.append("}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    vocab = json.loads(VOCAB.read_text(encoding="utf-8"))
    core_ids = load_core_ids()

    technical: dict[str, dict[str, str]] = {}
    phrases: dict[str, dict[str, str]] = {}

    for term in vocab["terms"]:
        tid = term["id"]
        if tid in core_ids:
            continue
        if term["category"] == "phrases":
            phrases[tid] = officialize_phrase(term)
        else:
            technical[tid] = officialize_technical(term)

    write_module(SCRIPTS / "official_translation_technical.py", "TRANSLATIONS", technical)
    write_module(SCRIPTS / "official_translation_phrases.py", "TRANSLATIONS", phrases)
    print(f"technical: {len(technical)}, phrases: {len(phrases)}")


if __name__ == "__main__":
    main()
