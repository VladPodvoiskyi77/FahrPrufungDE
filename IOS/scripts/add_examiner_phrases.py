#!/usr/bin/env python3
"""Add examiner phrases to vocabulary.json (preserves existing terms and tr)."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VOCAB_PATH = ROOT / "FahrPrufungDE" / "Resources" / "vocabulary.json"

# Typical instructions from practical driving exams (DE sources: Fahrschule Braun,
# deutsch-im-alltag.com, TÜV NORD, Fahrcoaching).
NEW_PHRASES: list[dict] = [
    # --- Richtungsanweisungen ---
    {
        "id": "phrase_links_kreuzung",
        "de": "Bitte biegen Sie an der nächsten Kreuzung links ab.",
        "ru": "Поверните налево на следующем перекрёстке.",
        "en": "Please turn left at the next junction.",
        "uk": "Поверніть ліворуч на наступному перехресті.",
        "fr": "Veuillez tourner à gauche au prochain carrefour.",
        "tr": "Lütfen bir sonraki kavşakta sola dönün.",
        "tags": ["examiner", "direction"],
    },
    {
        "id": "phrase_rechts_kreuzung",
        "de": "Bitte biegen Sie an der nächsten Kreuzung rechts ab.",
        "ru": "Поверните направо на следующем перекрёстке.",
        "en": "Please turn right at the next junction.",
        "uk": "Поверніть праворуч на наступному перехресті.",
        "fr": "Veuillez tourner à droite au prochain carrefour.",
        "tr": "Lütfen bir sonraki kavşakta sağa dönün.",
        "tags": ["examiner", "direction"],
    },
    {
        "id": "phrase_links_moeglichkeit",
        "de": "Bei der nächsten Möglichkeit links abbiegen.",
        "ru": "Поверните налево при первой возможности.",
        "en": "Turn left at the next opportunity.",
        "uk": "Поверніть ліворуч при першій нагоді.",
        "fr": "Tournez à gauche à la prochaine occasion.",
        "tr": "Bir sonraki fırsatta sola dönün.",
        "tags": ["examiner", "direction"],
    },
    {
        "id": "phrase_rechts_moeglichkeit",
        "de": "Bei der nächsten Möglichkeit rechts abbiegen.",
        "ru": "Поверните направо при первой возможности.",
        "en": "Turn right at the next opportunity.",
        "uk": "Поверніть праворуч при першій нагоді.",
        "fr": "Tournez à droite à la prochaine occasion.",
        "tr": "Bir sonraki fırsatta sağa dönün.",
        "tags": ["examiner", "direction"],
    },
    {
        "id": "phrase_halb_links",
        "de": "Bitte halb links abbiegen.",
        "ru": "Поверните слегка налево.",
        "en": "Please bear left.",
        "uk": "Поверніть трохи ліворуч.",
        "fr": "Veuillez bifurquer légèrement à gauche.",
        "tr": "Lütfen hafif sola dönün.",
        "tags": ["examiner", "direction"],
    },
    {
        "id": "phrase_halb_rechts",
        "de": "Bitte halb rechts abbiegen.",
        "ru": "Поверните слегка направо.",
        "en": "Please bear right.",
        "uk": "Поверніть трохи праворуч.",
        "fr": "Veuillez bifurquer légèrement à droite.",
        "tr": "Lütfen hafif sağa dönün.",
        "tags": ["examiner", "direction"],
    },
    {
        "id": "phrase_erste_ausfahrt",
        "de": "Nehmen Sie die erste Ausfahrt.",
        "ru": "Сверните на первый съезд.",
        "en": "Take the first exit.",
        "uk": "Зверніть на перший з'їзд.",
        "fr": "Prenez la première sortie.",
        "tr": "İlk çıkışı alın.",
        "tags": ["examiner", "direction"],
    },
    {
        "id": "phrase_zweite_ausfahrt",
        "de": "Nehmen Sie die zweite Ausfahrt.",
        "ru": "Сверните на второй съезд.",
        "en": "Take the second exit.",
        "uk": "Зверніть на другий з'їзд.",
        "fr": "Prenez la deuxième sortie.",
        "tr": "İkinci çıkışı alın.",
        "tags": ["examiner", "direction"],
    },
    {
        "id": "phrase_dritte_ausfahrt",
        "de": "Nehmen Sie die dritte Ausfahrt.",
        "ru": "Сверните на третий съезд.",
        "en": "Take the third exit.",
        "uk": "Зверніть на третій з'їзд.",
        "fr": "Prenez la troisième sortie.",
        "tr": "Üçüncü çıkışı alın.",
        "tags": ["examiner", "direction"],
    },
    {
        "id": "phrase_kreisverkehr_zweite",
        "de": "Beim nächsten Kreisverkehr nehmen Sie die zweite Ausfahrt.",
        "ru": "На следующем кольце сверните на второй съезд.",
        "en": "At the next roundabout, take the second exit.",
        "uk": "На наступному колі зверніть на другий з'їзд.",
        "fr": "Au prochain rond-point, prenez la deuxième sortie.",
        "tr": "Bir sonraki dönel kavşakta ikinci çıkışı alın.",
        "tags": ["examiner", "direction"],
    },
    {
        "id": "phrase_vorfahrtsstrasse",
        "de": "Folgen Sie der Vorfahrtsstraße.",
        "ru": "Следуйте по главной дороге.",
        "en": "Follow the priority road.",
        "uk": "Рухайтеся головною дорогою.",
        "fr": "Suivez la route prioritaire.",
        "tr": "Ana yolu takip edin.",
        "tags": ["examiner", "direction"],
    },
    {
        "id": "phrase_richtung_autobahn",
        "de": "Fahren Sie Richtung Autobahn.",
        "ru": "Двигайтесь в направлении автобана.",
        "en": "Head towards the motorway.",
        "uk": "Рухайтеся в напрямку автобану.",
        "fr": "Roulez en direction de l'autoroute.",
        "tr": "Otoyol yönünde gidin.",
        "tags": ["examiner", "direction"],
    },
    {
        "id": "phrase_richtung_kraftfahrstrasse",
        "de": "Fahren Sie Richtung Kraftfahrstraße.",
        "ru": "Двигайтесь в направлении скоростной дороги.",
        "en": "Head towards the dual carriageway.",
        "uk": "Рухайтеся в напрямку швидкісної дороги.",
        "fr": "Roulez en direction de la voie rapide.",
        "tr": "Otoyol benzeri yol yönünde gidin.",
        "tags": ["examiner", "direction"],
    },
    {
        "id": "phrase_richtung_stadt",
        "de": "Fahren Sie Richtung Stadtzentrum.",
        "ru": "Двигайтесь в направлении центра города.",
        "en": "Head towards the city centre.",
        "uk": "Рухайтеся в напрямку центру міста.",
        "fr": "Roulez en direction du centre-ville.",
        "tr": "Şehir merkezi yönünde gidin.",
        "tags": ["examiner", "direction"],
    },
    {
        "id": "phrase_weiterfahren",
        "de": "Fahren Sie bitte weiter.",
        "ru": "Продолжайте движение.",
        "en": "Please continue driving.",
        "uk": "Будь ласка, продовжуйте рух.",
        "fr": "Veuillez continuer à rouler.",
        "tr": "Lütfen devam edin.",
        "tags": ["examiner", "direction"],
    },
    # --- Manöver ---
    {
        "id": "phrase_anhalten",
        "de": "Bitte halten Sie an.",
        "ru": "Остановитесь, пожалуйста.",
        "en": "Please stop.",
        "uk": "Будь ласка, зупиніться.",
        "fr": "Veuillez vous arrêter.",
        "tr": "Lütfen durun.",
        "tags": ["examiner", "maneuver"],
    },
    {
        "id": "phrase_rueckwaerts_links",
        "de": "Bitte rückwärts links einparken.",
        "ru": "Припаркуйтесь задним ходом налево.",
        "en": "Please reverse park to the left.",
        "uk": "Припаркуйтеся заднім ходом ліворуч.",
        "fr": "Garez-vous en marche arrière à gauche.",
        "tr": "Lütfen geri geri sola park edin.",
        "tags": ["examiner", "maneuver"],
    },
    {
        "id": "phrase_rueckwaerts_rechts",
        "de": "Bitte rückwärts rechts einparken.",
        "ru": "Припаркуйтесь задним ходом направо.",
        "en": "Please reverse park to the right.",
        "uk": "Припаркуйтеся заднім ходом праворуч.",
        "fr": "Garez-vous en marche arrière à droite.",
        "tr": "Lütfen geri geri sağa park edin.",
        "tags": ["examiner", "maneuver"],
    },
    {
        "id": "phrase_vorwaerts_links",
        "de": "Bitte vorwärts links einparken.",
        "ru": "Припаркуйтесь передом налево.",
        "en": "Please forward park to the left.",
        "uk": "Припаркуйтеся передом ліворуч.",
        "fr": "Garez-vous en marche avant à gauche.",
        "tr": "Lütfen ileri doğru sola park edin.",
        "tags": ["examiner", "maneuver"],
    },
    {
        "id": "phrase_vorwaerts_rechts",
        "de": "Bitte vorwärts rechts einparken.",
        "ru": "Припаркуйтесь передом направо.",
        "en": "Please forward park to the right.",
        "uk": "Припаркуйтеся передом праворуч.",
        "fr": "Garez-vous en marche avant à droite.",
        "tr": "Lütfen ileri doğru sağa park edin.",
        "tags": ["examiner", "maneuver"],
    },
    {
        "id": "phrase_laengs_einparken",
        "de": "Parken Sie längs ein.",
        "ru": "Припаркуйтесь параллельно.",
        "en": "Parallel park.",
        "uk": "Припаркуйтеся паралельно.",
        "fr": "Garez-vous en créneau parallèle.",
        "tr": "Paralel park yapın.",
        "tags": ["examiner", "maneuver"],
    },
    {
        "id": "phrase_quer_vorwaerts",
        "de": "Parken Sie quer vorwärts ein.",
        "ru": "Припаркуйтесь перпендикулярно передом.",
        "en": "Bay park forwards.",
        "uk": "Припаркуйтеся поперек передом.",
        "fr": "Garez-vous en bataille en marche avant.",
        "tr": "Öne doğru dik park yapın.",
        "tags": ["examiner", "maneuver"],
    },
    {
        "id": "phrase_quer_rueckwaerts",
        "de": "Parken Sie quer rückwärts ein.",
        "ru": "Припаркуйтесь перпендикулярно задним ходом.",
        "en": "Bay park in reverse.",
        "uk": "Припаркуйтеся поперек заднім ходом.",
        "fr": "Garez-vous en bataille en marche arrière.",
        "tr": "Geri geri dik park yapın.",
        "tags": ["examiner", "maneuver"],
    },
    {
        "id": "phrase_wenden",
        "de": "Bitte wenden Sie.",
        "ru": "Развернитесь, пожалуйста.",
        "en": "Please turn around.",
        "uk": "Будь ласка, розверніться.",
        "fr": "Veuillez faire demi-tour.",
        "tr": "Lütfen U dönüşü yapın.",
        "tags": ["examiner", "maneuver"],
    },
    {
        "id": "phrase_hinter_fahrzeug",
        "de": "Parken Sie hinter dem Fahrzeug.",
        "ru": "Припаркуйтесь за автомобилем.",
        "en": "Park behind the vehicle.",
        "uk": "Припаркуйтеся за автомобілем.",
        "fr": "Garez-vous derrière le véhicule.",
        "tr": "Aracın arkasına park edin.",
        "tags": ["examiner", "maneuver"],
    },
    {
        "id": "phrase_zwischen_fahrzeugen",
        "de": "Parken Sie zwischen den Fahrzeugen.",
        "ru": "Припаркуйтесь между автомобилями.",
        "en": "Park between the vehicles.",
        "uk": "Припаркуйтеся між автомобілями.",
        "fr": "Garez-vous entre les véhicules.",
        "tr": "Araçların arasına park edin.",
        "tags": ["examiner", "maneuver"],
    },
    {
        "id": "phrase_parkluecke",
        "de": "Finden Sie hier eine geeignete Parklücke und parken Sie seitwärts rückwärts ein.",
        "ru": "Найдите подходящее место и припаркуйтесь параллельно задним ходом.",
        "en": "Find a suitable parking space and parallel park in reverse.",
        "uk": "Знайдіть відповідне місце і припаркуйтеся паралельно заднім ходом.",
        "fr": "Trouvez une place adaptée et garez-vous en créneau en marche arrière.",
        "tr": "Uygun bir park yeri bulun ve geri geri paralel park yapın.",
        "tags": ["examiner", "maneuver"],
    },
    # --- Sicherheitskontrolle ---
    {
        "id": "phrase_abblendlicht_wo",
        "de": "Wo am Fahrzeug schaltet man das Abblendlicht ein?",
        "ru": "Где на автомобиле включается ближний свет?",
        "en": "Where do you switch on the dipped headlights?",
        "uk": "Де на автомобілі вмикається ближнє світло?",
        "fr": "Où allume-t-on les feux de croisement sur le véhicule ?",
        "tr": "Araçta kısa farlar nereden açılır?",
        "tags": ["examiner", "safety"],
    },
    {
        "id": "phrase_standlicht_pruefen",
        "de": "Wie können Sie prüfen, ob das Standlicht funktioniert?",
        "ru": "Как проверить, работает ли габаритный свет?",
        "en": "How can you check if the sidelights work?",
        "uk": "Як перевірити, чи працює габаритне світло?",
        "fr": "Comment vérifier si les feux de position fonctionnent ?",
        "tr": "Park lambalarının çalışıp çalışmadığını nasıl kontrol edersiniz?",
        "tags": ["examiner", "safety"],
    },
    {
        "id": "phrase_warnblinkanlage",
        "de": "Bitte betätigen Sie die Warnblinkanlage!",
        "ru": "Включите аварийную сигнализацию!",
        "en": "Please switch on the hazard warning lights!",
        "uk": "Увімкніть аварійну сигналізацію!",
        "fr": "Veuillez actionner les feux de détresse !",
        "tr": "Lütfen dörtlü flaşörleri açın!",
        "tags": ["examiner", "safety"],
    },
    {
        "id": "phrase_hupen",
        "de": "Bitte hupen!",
        "ru": "Пожалуйста, подайте звуковой сигнал!",
        "en": "Please sound the horn!",
        "uk": "Будь ласка, подайте звуковий сигнал!",
        "fr": "Veuillez klaxonner !",
        "tr": "Lütfen korna çalın!",
        "tags": ["examiner", "safety"],
    },
    {
        "id": "phrase_parkfertig",
        "de": "Stellen Sie das Fahrzeug parkfertig ab.",
        "ru": "Заглушите автомобиль и поставьте на стоянку.",
        "en": "Park the vehicle properly (engine off, secured).",
        "uk": "Заглушіть автомобіль і поставте на стоянку.",
        "fr": "Garez le véhicule correctement (moteur coupé, sécurisé).",
        "tr": "Aracı park haline getirin (motor kapalı, güvenli).",
        "tags": ["examiner", "safety"],
    },
    {
        "id": "phrase_standlicht_ein",
        "de": "Bitte schalten Sie das Standlicht ein.",
        "ru": "Включите габаритные огни.",
        "en": "Please switch on the sidelights.",
        "uk": "Увімкніть габаритні вогні.",
        "fr": "Veuillez allumer les feux de position.",
        "tr": "Lütfen park lambalarını açın.",
        "tags": ["examiner", "safety"],
    },
    {
        "id": "phrase_abblendlicht_ein",
        "de": "Bitte schalten Sie das Abblendlicht ein.",
        "ru": "Включите ближний свет фар.",
        "en": "Please switch on the dipped headlights.",
        "uk": "Увімкніть ближнє світло фар.",
        "fr": "Veuillez allumer les feux de croisement.",
        "tr": "Lütfen kısa farları açın.",
        "tags": ["examiner", "safety"],
    },
    {
        "id": "phrase_blinker_links",
        "de": "Bitte schalten Sie den Blinker links ein.",
        "ru": "Включите левый поворотник.",
        "en": "Please switch on the left indicator.",
        "uk": "Увімкніть лівий поворотник.",
        "fr": "Veuillez actionner le clignotant gauche.",
        "tr": "Lütfen sol sinyali açın.",
        "tags": ["examiner", "safety"],
    },
    {
        "id": "phrase_blinker_rechts",
        "de": "Bitte schalten Sie den Blinker rechts ein.",
        "ru": "Включите правый поворотник.",
        "en": "Please switch on the right indicator.",
        "uk": "Увімкніть правий поворотник.",
        "fr": "Veuillez actionner le clignotant droit.",
        "tr": "Lütfen sağ sinyali açın.",
        "tags": ["examiner", "safety"],
    },
    {
        "id": "phrase_bremslichter",
        "de": "Zeigen Sie mir, ob die Bremslichter funktionieren.",
        "ru": "Покажите, работают ли стоп-сигналы.",
        "en": "Show me whether the brake lights work.",
        "uk": "Покажіть, чи працюють стоп-сигнали.",
        "fr": "Montrez-moi si les feux stop fonctionnent.",
        "tr": "Fren lambalarının çalışıp çalışmadığını gösterin.",
        "tags": ["examiner", "safety"],
    },
    {
        "id": "phrase_motorhaube",
        "de": "Bitte öffnen Sie die Motorhaube.",
        "ru": "Откройте капот, пожалуйста.",
        "en": "Please open the bonnet.",
        "uk": "Відкрийте капот, будь ласка.",
        "fr": "Veuillez ouvrir le capot.",
        "tr": "Lütfen motor kaputunu açın.",
        "tags": ["examiner", "safety"],
    },
    {
        "id": "phrase_profiltiefe",
        "de": "Bitte prüfen Sie die Profiltiefe am Reifen.",
        "ru": "Проверьте глубину протектора шины.",
        "en": "Please check the tyre tread depth.",
        "uk": "Перевірте глибину протектора шини.",
        "fr": "Veuillez vérifier la profondeur de la sculpture du pneu.",
        "tr": "Lütfen lastik diş derinliğini kontrol edin.",
        "tags": ["examiner", "safety"],
    },
    {
        "id": "phrase_reifendruck",
        "de": "Wie kontrollieren Sie den Reifendruck?",
        "ru": "Как проверить давление в шинах?",
        "en": "How do you check tyre pressure?",
        "uk": "Як перевірити тиск у шинах?",
        "fr": "Comment contrôlez-vous la pression des pneus ?",
        "tr": "Lastik basıncını nasıl kontrol edersiniz?",
        "tags": ["examiner", "safety"],
    },
    {
        "id": "phrase_fluessigkeiten",
        "de": "Was für Flüssigkeiten finden Sie unter der Motorhaube?",
        "ru": "Какие жидкости находятся под капотом?",
        "en": "What fluids are found under the bonnet?",
        "uk": "Які рідини знаходяться під капотом?",
        "fr": "Quels liquides trouve-t-on sous le capot ?",
        "tr": "Motor kaputunun altında hangi sıvıları bulursunuz?",
        "tags": ["examiner", "safety"],
    },
    {
        "id": "phrase_kontrollleuchten",
        "de": "Bitte benennen Sie die Kontrollleuchten im Armaturenbrett.",
        "ru": "Назовите контрольные лампы на приборной панели.",
        "en": "Please name the warning lights on the dashboard.",
        "uk": "Назвіть контрольні лампи на приладовій панелі.",
        "fr": "Veuillez nommer les voyants du tableau de bord.",
        "tr": "Lütfen gösterge panelindeki uyarı ışıklarını adlandırın.",
        "tags": ["examiner", "safety"],
    },
    {
        "id": "phrase_wegrollen",
        "de": "Bitte sichern Sie das Fahrzeug gegen Wegrollen.",
        "ru": "Зафиксируйте автомобиль от скатывания.",
        "en": "Please secure the vehicle against rolling.",
        "uk": "Зафіксуйте автомобіль від скочування.",
        "fr": "Veuillez sécuriser le véhicule contre le roulement.",
        "tr": "Lütfen aracı yuvarlanmaya karşı güvence altına alın.",
        "tags": ["examiner", "safety"],
    },
    # --- Hinweise während der Fahrt ---
    {
        "id": "phrase_schneller",
        "de": "Bitte etwas schneller fahren.",
        "ru": "Езжайте чуть быстрее.",
        "en": "Please drive a bit faster.",
        "uk": "Їдьте трохи швидше.",
        "fr": "Roulez un peu plus vite, s'il vous plaît.",
        "tr": "Lütfen biraz daha hızlı gidin.",
        "tags": ["examiner", "hint"],
    },
    {
        "id": "phrase_einordnen",
        "de": "Bitte ordnen Sie sich rechts ein.",
        "ru": "Выстроитесь правее, пожалуйста.",
        "en": "Please move to the right lane.",
        "uk": "Будь ласка, вибудуйтеся праворуч.",
        "fr": "Veuillez vous placer à droite.",
        "tr": "Lütfen sağa yanaşın.",
        "tags": ["examiner", "hint"],
    },
    {
        "id": "phrase_radfahrer",
        "de": "Achten Sie auf die Radfahrer.",
        "ru": "Следите за велосипедистами.",
        "en": "Watch out for cyclists.",
        "uk": "Стежте за велосипедистами.",
        "fr": "Faites attention aux cyclistes.",
        "tr": "Bisikletlilere dikkat edin.",
        "tags": ["examiner", "hint"],
    },
    {
        "id": "phrase_parkende_autos",
        "de": "Achten Sie auf parkende Fahrzeuge.",
        "ru": "Следите за припаркованными автомобилями.",
        "en": "Watch out for parked vehicles.",
        "uk": "Стежте за припаркованими автомобілями.",
        "fr": "Faites attention aux véhicules stationnés.",
        "tr": "Park halindeki araçlara dikkat edin.",
        "tags": ["examiner", "hint"],
    },
    {
        "id": "phrase_spiegel_beobachten",
        "de": "Beobachten Sie bitte die Spiegel.",
        "ru": "Следите за зеркалами.",
        "en": "Please check your mirrors.",
        "uk": "Стежте за дзеркалами.",
        "fr": "Observez vos rétroviseurs, s'il vous plaît.",
        "tr": "Lütfen aynaları kontrol edin.",
        "tags": ["examiner", "hint"],
    },
    {
        "id": "phrase_wiederholen",
        "de": "Können Sie das bitte wiederholen?",
        "ru": "Можете повторить, пожалуйста?",
        "en": "Can you please repeat that?",
        "uk": "Чи можете повторити, будь ласка?",
        "fr": "Pouvez-vous répéter, s'il vous plaît ?",
        "tr": "Bunu tekrar edebilir misiniz?",
        "tags": ["examiner", "hint"],
    },
    {
        "id": "phrase_nicht_bestanden",
        "de": "Sie haben leider nicht bestanden.",
        "ru": "К сожалению, вы не сдали.",
        "en": "Unfortunately, you have not passed.",
        "uk": "На жаль, ви не склали.",
        "fr": "Malheureusement, vous n'avez pas réussi.",
        "tr": "Maalesef geçemediniz.",
        "tags": ["examiner", "result"],
    },
    {
        "id": "phrase_grundfahraufgaben",
        "de": "Die Grundfahraufgaben waren fehlerhaft.",
        "ru": "Базовые упражнения выполнены с ошибками.",
        "en": "The basic driving tasks were incorrect.",
        "uk": "Базові вправи виконані з помилками.",
        "fr": "Les exercices de base étaient incorrects.",
        "tr": "Temel sürüş görevleri hatalıydı.",
        "tags": ["examiner", "result"],
    },
    {
        "id": "phrase_vorfahrt_missachtet",
        "de": "Sie haben die Vorfahrt missachtet.",
        "ru": "Вы не уступили дорогу.",
        "en": "You failed to give way.",
        "uk": "Ви не поступилися дорогою.",
        "fr": "Vous n'avez pas respecté la priorité.",
        "tr": "Geçiş önceliğine uymadınız.",
        "tags": ["examiner", "result"],
    },
]

TR_FIXES = {
    "phrase_kein_durchfall": "Bu, kalma sebebi değil.",
    "phrase_einparken": "Burada bir yere park edin.",
}


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
    added = 0
    insert_before = "phrase_spiegel_blinker_schulter"

    new_terms = [term_from_phrase(p) for p in NEW_PHRASES if p["id"] not in existing_ids]
    if not new_terms:
        print("No new phrases to add.")
        return

    out: list[dict] = []
    inserted = False
    for term in data["terms"]:
        if not inserted and term["id"] == insert_before:
            out.extend(new_terms)
            inserted = True
            added = len(new_terms)
        if term["id"] in TR_FIXES:
            term["tr"] = TR_FIXES[term["id"]]
        out.append(term)

    if not inserted:
        out.extend(new_terms)
        added = len(new_terms)

    data["terms"] = out
    data["meta"]["term_count"] = len(out)

    with open(VOCAB_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    examiner_count = sum(1 for t in out if "examiner" in t.get("tags", []))
    print(f"Added {added} examiner phrases ({examiner_count} total with 'examiner' tag)")
    print(f"term_count → {data['meta']['term_count']}")


if __name__ == "__main__":
    main()
