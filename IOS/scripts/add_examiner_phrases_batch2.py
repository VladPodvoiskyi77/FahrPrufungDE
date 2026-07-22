#!/usr/bin/env python3
"""Add examiner phrases from practical exam prep list (batch 2)."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VOCAB_PATH = ROOT / "FahrPrufungDE" / "Resources" / "vocabulary.json"

NEW_ITEMS: list[dict] = [
    # --- start ---
    {
        "id": "phrase_motor_starten",
        "de": "Starten Sie den Motor.",
        "ru": "Запустите двигатель.",
        "en": "Start the engine.",
        "uk": "Запустіть двигун.",
        "fr": "Démarrez le moteur.",
        "tr": "Motoru çalıştırın.",
        "tags": ["examiner", "start"],
    },
    {
        "id": "phrase_fahren_los",
        "de": "Fahren Sie los.",
        "ru": "Начинайте движение.",
        "en": "Start driving.",
        "uk": "Починайте рух.",
        "fr": "Partez.",
        "tr": "Harekete geçin.",
        "tags": ["examiner", "start"],
    },
    # --- direction ---
    {
        "id": "phrase_bitte_geradeaus",
        "de": "Bitte geradeaus fahren.",
        "ru": "Пожалуйста, езжайте прямо.",
        "en": "Please drive straight ahead.",
        "uk": "Будь ласка, їдьте прямо.",
        "fr": "Veuillez aller tout droit.",
        "tr": "Lütfen düz gidin.",
        "tags": ["examiner", "direction"],
    },
    {
        "id": "phrase_auf_autobahn",
        "de": "Fahren Sie auf die Autobahn.",
        "ru": "Выезжайте на автобан.",
        "en": "Drive onto the motorway.",
        "uk": "Виїжджайте на автобан.",
        "fr": "Roulez sur l'autoroute.",
        "tr": "Otoyola çıkın.",
        "tags": ["examiner", "direction"],
    },
    {
        "id": "phrase_naechste_strasse_rechts",
        "de": "Nehmen Sie die nächste Straße rechts.",
        "ru": "Поверните на следующую улицу направо.",
        "en": "Take the next street on the right.",
        "uk": "Поверніть на наступну вулицю праворуч.",
        "fr": "Prenez la prochaine rue à droite.",
        "tr": "Bir sonraki sokaktan sağa dönün.",
        "tags": ["examiner", "direction"],
    },
    {
        "id": "phrase_naechste_strasse_links",
        "de": "Nehmen Sie die nächste Straße links.",
        "ru": "Поверните на следующую улицу налево.",
        "en": "Take the next street on the left.",
        "uk": "Поверніть на наступну вулицю ліворуч.",
        "fr": "Prenez la prochaine rue à gauche.",
        "tr": "Bir sonraki sokaktan sola dönün.",
        "tags": ["examiner", "direction"],
    },
    {
        "id": "phrase_kreuzung_geradeaus",
        "de": "Fahren Sie an der Kreuzung geradeaus.",
        "ru": "На перекрёстке езжайте прямо.",
        "en": "Go straight ahead at the junction.",
        "uk": "На перехресті їдьте прямо.",
        "fr": "Allez tout droit au carrefour.",
        "tr": "Kavşakta düz gidin.",
        "tags": ["examiner", "direction"],
    },
    {
        "id": "phrase_bis_naechste_ampel",
        "de": "Fahren Sie bis zur nächsten Ampel.",
        "ru": "Езжайте до следующего светофора.",
        "en": "Drive to the next traffic lights.",
        "uk": "Їдьте до наступного світлофора.",
        "fr": "Roulez jusqu'au prochain feu.",
        "tr": "Bir sonraki trafik ışığına kadar gidin.",
        "tags": ["examiner", "direction"],
    },
    {
        "id": "phrase_kreisverkehr_rechts",
        "de": "Fahren Sie im Kreisverkehr rechts.",
        "ru": "На круговом движении держитесь правее.",
        "en": "Keep right in the roundabout.",
        "uk": "На колі тримайтеся праворуч.",
        "fr": "Restez à droite sur le rond-point.",
        "tr": "Dönel kavşakta sağdan gidin.",
        "tags": ["examiner", "direction"],
    },
    {
        "id": "phrase_einbahnstrasse",
        "de": "Fahren Sie durch die Einbahnstraße.",
        "ru": "Езжайте по улице с односторонним движением.",
        "en": "Drive through the one-way street.",
        "uk": "Їдьте вулицею з одностороннім рухом.",
        "fr": "Roulez dans la rue à sens unique.",
        "tr": "Tek yönlü caddeden gidin.",
        "tags": ["examiner", "direction"],
    },
    # --- maneuver ---
    {
        "id": "phrase_halten_hier",
        "de": "Halten Sie bitte hier an.",
        "ru": "Остановитесь здесь, пожалуйста.",
        "en": "Please stop here.",
        "uk": "Зупиніться тут, будь ласка.",
        "fr": "Arrêtez-vous ici, s'il vous plaît.",
        "tr": "Lütfen burada durun.",
        "tags": ["examiner", "maneuver"],
    },
    {
        "id": "phrase_halten_ampel",
        "de": "Halten Sie an der Ampel an.",
        "ru": "Остановитесь на светофоре.",
        "en": "Stop at the traffic lights.",
        "uk": "Зупиніться на світлофорі.",
        "fr": "Arrêtez-vous au feu.",
        "tr": "Trafik ışığında durun.",
        "tags": ["examiner", "maneuver"],
    },
    {
        "id": "phrase_wenden_wenn_sicher",
        "de": "Wenden Sie bitte, wenn es sicher ist.",
        "ru": "Развернитесь, когда это будет безопасно.",
        "en": "Please turn around when it is safe.",
        "uk": "Розверніться, коли це буде безпечно.",
        "fr": "Faites demi-tour quand c'est sûr.",
        "tr": "Güvenli olduğunda lütfen U dönüşü yapın.",
        "tags": ["examiner", "maneuver"],
    },
    {
        "id": "phrase_wenden_moeglichkeit",
        "de": "Suchen Sie eine geeignete Möglichkeit zum Wenden.",
        "ru": "Найдите подходящую возможность для разворота.",
        "en": "Find a suitable place to turn around.",
        "uk": "Знайдіть відповідну можливість для розвороту.",
        "fr": "Trouvez un endroit adapté pour faire demi-tour.",
        "tr": "U dönüşü için uygun bir yer bulun.",
        "tags": ["examiner", "maneuver"],
    },
    {
        "id": "phrase_auf_parkplatz",
        "de": "Fahren Sie auf den Parkplatz.",
        "ru": "Заезжайте на парковку.",
        "en": "Drive onto the car park.",
        "uk": "Заїжджайте на парковку.",
        "fr": "Roulez sur le parking.",
        "tr": "Otoparka girin.",
        "tags": ["examiner", "maneuver"],
    },
    {
        "id": "phrase_halten_fahrbahnrand",
        "de": "Halten Sie am rechten Fahrbahnrand an.",
        "ru": "Остановитесь у правого края дороги.",
        "en": "Stop at the right edge of the road.",
        "uk": "Зупиніться біля правого краю дороги.",
        "fr": "Arrêtez-vous au bord droit de la chaussée.",
        "tr": "Yolun sağ kenarında durun.",
        "tags": ["examiner", "maneuver"],
    },
    {
        "id": "phrase_sicherer_halt",
        "de": "Machen Sie einen sicheren Halt.",
        "ru": "Выполните безопасную остановку.",
        "en": "Make a safe stop.",
        "uk": "Зробіть безпечну зупинку.",
        "fr": "Effectuez un arrêt en toute sécurité.",
        "tr": "Güvenli bir duruş yapın.",
        "tags": ["examiner", "maneuver"],
    },
    {
        "id": "phrase_anhalten_warten",
        "de": "Halten Sie an und warten Sie.",
        "ru": "Остановитесь и подождите.",
        "en": "Stop and wait.",
        "uk": "Зупиніться і зачекайте.",
        "fr": "Arrêtez-vous et attendez.",
        "tr": "Durun ve bekleyin.",
        "tags": ["examiner", "maneuver"],
    },
    {
        "id": "phrase_warten_bahnuebergang",
        "de": "Warten Sie am Bahnübergang.",
        "ru": "Подождите на железнодорожном переезде.",
        "en": "Wait at the level crossing.",
        "uk": "Зачекайте на залізничному переїзді.",
        "fr": "Attendez au passage à niveau.",
        "tr": "Demiryolu geçidinde bekleyin.",
        "tags": ["examiner", "maneuver"],
    },
    # --- hint ---
    {
        "id": "phrase_geschwindigkeit_reduzieren",
        "de": "Reduzieren Sie die Geschwindigkeit.",
        "ru": "Снизьте скорость.",
        "en": "Reduce your speed.",
        "uk": "Зменшіть швидкість.",
        "fr": "Réduisez votre vitesse.",
        "tr": "Hızınızı azaltın.",
        "tags": ["examiner", "hint"],
    },
    {
        "id": "phrase_beschleunigen",
        "de": "Beschleunigen Sie bitte.",
        "ru": "Ускорьтесь, пожалуйста.",
        "en": "Please speed up.",
        "uk": "Прискоріться, будь ласка.",
        "fr": "Accélérez, s'il vous plaît.",
        "tr": "Lütfen hızlanın.",
        "tags": ["examiner", "hint"],
    },
    {
        "id": "phrase_rueckspiegel",
        "de": "Schauen Sie in den Rückspiegel.",
        "ru": "Посмотрите в зеркало заднего вида.",
        "en": "Look in the rear-view mirror.",
        "uk": "Подивіться в дзеркало заднього виду.",
        "fr": "Regardez dans le rétroviseur.",
        "tr": "Dikiz aynasına bakın.",
        "tags": ["examiner", "hint"],
    },
    {
        "id": "phrase_schulterblick_machen",
        "de": "Machen Sie einen Schulterblick.",
        "ru": "Сделайте контрольный взгляд через плечо.",
        "en": "Do a shoulder check.",
        "uk": "Зробіть контрольний погляд через плече.",
        "fr": "Faites un contrôle de l'angle mort.",
        "tr": "Omuz üzerinden kontrol yapın.",
        "tags": ["examiner", "hint"],
    },
    {
        "id": "phrase_achten_verkehr",
        "de": "Achten Sie auf den Verkehr.",
        "ru": "Следите за движением.",
        "en": "Watch the traffic.",
        "uk": "Стежте за рухом.",
        "fr": "Faites attention à la circulation.",
        "tr": "Trafiğe dikkat edin.",
        "tags": ["examiner", "hint"],
    },
    {
        "id": "phrase_achten_vorfahrt",
        "de": "Achten Sie auf die Vorfahrt.",
        "ru": "Обратите внимание на преимущество проезда.",
        "en": "Pay attention to right of way.",
        "uk": "Зверніть увагу на перевагу руху.",
        "fr": "Faites attention à la priorité.",
        "tr": "Geçiş hakkına dikkat edin.",
        "tags": ["examiner", "hint"],
    },
    {
        "id": "phrase_bleiben_ruhig",
        "de": "Bleiben Sie ruhig.",
        "ru": "Сохраняйте спокойствие.",
        "en": "Stay calm.",
        "uk": "Зберігайте спокій.",
        "fr": "Restez calme.",
        "tr": "Sakin kalın.",
        "tags": ["examiner", "hint"],
    },
    {
        "id": "phrase_tempolimit",
        "de": "Achten Sie auf die Geschwindigkeitsbegrenzung.",
        "ru": "Соблюдайте ограничение скорости.",
        "en": "Observe the speed limit.",
        "uk": "Дотримуйтесь обмеження швидкості.",
        "fr": "Respectez la limitation de vitesse.",
        "tr": "Hız sınırına dikkat edin.",
        "tags": ["examiner", "hint"],
    },
    {
        "id": "phrase_fussgaenger_passieren",
        "de": "Lassen Sie die Fußgänger passieren.",
        "ru": "Пропустите пешеходов.",
        "en": "Let the pedestrians pass.",
        "uk": "Пропустіть пішоходів.",
        "fr": "Laissez passer les piétons.",
        "tr": "Yayalara yol verin.",
        "tags": ["examiner", "hint"],
    },
]

NEW_VOCAB_TERM = {
    "id": "parkplatz",
    "de": "Der Parkplatz",
    "article": "der",
    "de_base": "Parkplatz",
    "ru": "Парковка",
    "en": "Car park / parking lot",
    "uk": "Парковка",
    "fr": "Parking",
    "tr": "Otopark",
    "category": "traffic",
    "tags": ["core"],
}


def normalize_de(text: str) -> str:
    text = text.lower().strip().rstrip(".")
    text = re.sub(r"\s+", " ", text)
    return text


def term_from_phrase(p: dict) -> dict:
    de = p["de"]
    return {
        "id": p["id"],
        "de": de,
        "article": None,
        "de_base": de,
        "ru": p["ru"],
        "en": p["en"],
        "uk": p["uk"],
        "fr": p["fr"],
        "tr": p["tr"],
        "category": "phrases",
        "tags": p["tags"],
        "exam_phrase_de": de,
    }


def main() -> None:
    with open(VOCAB_PATH, encoding="utf-8") as f:
        data = json.load(f)

    existing_ids = {t["id"] for t in data["terms"]}
    existing_de = {normalize_de(t["de"]) for t in data["terms"]}

    added_phrases = 0
    skipped = 0

    for p in NEW_ITEMS:
        if p["id"] in existing_ids:
            skipped += 1
            continue
        if normalize_de(p["de"]) in existing_de:
            skipped += 1
            continue
        data["terms"].append(term_from_phrase(p))
        existing_ids.add(p["id"])
        existing_de.add(normalize_de(p["de"]))
        added_phrases += 1

    added_vocab = 0
    if NEW_VOCAB_TERM["id"] not in existing_ids:
        data["terms"].append(NEW_VOCAB_TERM)
        added_vocab += 1

    data["meta"]["term_count"] = len(data["terms"])

    with open(VOCAB_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    examiner_count = sum(1 for t in data["terms"] if "examiner" in t.get("tags", []))
    print(f"Added {added_phrases} examiner phrases ({skipped} skipped as duplicates)")
    print(f"Added {added_vocab} vocabulary term(s)")
    print(f"Examiner phrases total: {examiner_count}")
    print(f"term_count → {data['meta']['term_count']}")


if __name__ == "__main__":
    main()
