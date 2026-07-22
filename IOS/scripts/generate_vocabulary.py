#!/usr/bin/env python3
"""Generate vocabulary.json and signs.json for FahrPrufungDE app."""

import json
from pathlib import Path
from typing import Optional, Tuple

ROOT = Path(__file__).resolve().parent.parent
RESOURCES = ROOT / "FahrPrufungDE" / "Resources"

CATEGORIES = [
    {"id": "exam", "de": "Prüfung", "ru": "Экзамен", "en": "Exam", "uk": "Іспит", "fr": "Examen"},
    {"id": "technik", "de": "Technik", "ru": "Техника", "en": "Technical check", "uk": "Техніка", "fr": "Technique"},
    {"id": "car", "de": "Fahrzeug", "ru": "Автомобиль", "en": "Vehicle", "uk": "Автомобіль", "fr": "Véhicule"},
    {"id": "lights", "de": "Beleuchtung", "ru": "Освещение", "en": "Lights", "uk": "Освітлення", "fr": "Éclairage"},
    {"id": "brakes", "de": "Bremsen", "ru": "Тормоза", "en": "Brakes", "uk": "Гальма", "fr": "Freins"},
    {"id": "fluids", "de": "Flüssigkeiten", "ru": "Жидкости", "en": "Fluids", "uk": "Рідини", "fr": "Liquides"},
    {"id": "safety", "de": "Sicherheit", "ru": "Безопасность", "en": "Safety", "uk": "Безпека", "fr": "Sécurité"},
    {"id": "assist", "de": "Assistenzsysteme", "ru": "Ассистенты", "en": "Driver assistance", "uk": "Асистенти", "fr": "Aides à la conduite"},
    {"id": "maneuvers", "de": "Manöver", "ru": "Манёвры", "en": "Maneuvers", "uk": "Маневри", "fr": "Manœuvres"},
    {"id": "grundaufgaben", "de": "Grundfahraufgaben", "ru": "Базовые упражнения", "en": "Basic tasks", "uk": "Базові вправи", "fr": "Exercices de base"},
    {"id": "traffic", "de": "Verkehr", "ru": "Дорожное движение", "en": "Traffic", "uk": "Дорожній рух", "fr": "Circulation"},
    {"id": "phrases", "de": "Prüfer-Phrasen", "ru": "Фразы экзаменатора", "en": "Examiner phrases", "uk": "Фрази екзаменатора", "fr": "Phrases de l'examinateur"},
    {"id": "documents", "de": "Dokumente", "ru": "Документы", "en": "Documents", "uk": "Документи", "fr": "Documents"},
    {"id": "emergency", "de": "Panne & Unfall", "ru": "Поломка и ДТП", "en": "Breakdown & accident", "uk": "Поломка та ДТП", "fr": "Panne & accident"},
]

# Each term: (id, de_with_article, ru, en, uk, fr, category, [tags], exam_phrase_de or None)
TERMS = [
    # === EXAM ===
    ("pruefungsfahrt", "die Prüfungsfahrt", "экзаменационная поездка", "practical driving test", "іспитна поїздка", "examen pratique de conduite", "exam", ["core"]),
    ("pruefer", "der Prüfer", "экзаменатор", "examiner", "екзаменатор", "examinateur", "exam", ["core"]),
    ("pruefling", "der Prüfling", "кандидат на экзамене", "candidate", "кандидат на іспиті", "candidat", "exam", []),
    ("fahrlehrer", "der Fahrlehrer", "инструктор", "driving instructor", "інструктор", "moniteur d'auto-école", "exam", ["core"]),
    ("fahrlehrerin", "die Fahrlehrerin", "инструктор (жен.)", "driving instructor (f.)", "інструкторка", "monitrice d'auto-école", "exam", []),
    ("fahrschueler", "der Fahrschüler", "ученик автошколы", "driving student", "учень автошколи", "élève conducteur", "exam", []),
    ("fuehrerschein", "der Führerschein", "водительское удостоверение", "driving licence", "водійське посвідчення", "permis de conduire", "exam", ["core"]),
    ("pruefungsstrecke", "die Prüfungsstrecke", "маршрут экзамена", "test route", "маршрут іспиту", "parcours d'examen", "exam", []),
    ("pruefungsdauer", "die Prüfungsdauer", "длительность экзамена", "test duration", "тривалість іспиту", "durée de l'examen", "exam", []),
    ("durchfallen", "durchfallen", "провалить экзамен", "to fail the test", "провалити іспит", "échouer à l'examen", "exam", ["verb"]),
    ("bestehen", "bestehen", "сдать экзамен", "to pass the test", "скласти іспит", "réussir l'examen", "exam", ["verb"]),
    ("tuev_gelaende", "das TÜV-Gelände", "территория TÜV", "TÜV premises", "територія TÜV", "terrain du TÜV", "exam", []),
    ("grundfahraufgabe", "die Grundfahraufgabe", "базовое упражнение", "basic driving task", "базова вправа", "exercice de base", "exam", ["core"]),
    ("theoriepruefung", "die Theorieprüfung", "теоретический экзамен", "theory test", "теоретичний іспит", "examen théorique", "exam", []),
    ("praktische_pruefung", "die praktische Prüfung", "практический экзамен", "practical test", "практичний іспит", "examen pratique", "exam", []),
    ("fahrschule", "die Fahrschule", "автошкола", "driving school", "автошкола", "auto-école", "exam", []),
    ("fahrstunde", "die Fahrstunde", "урок вождения", "driving lesson", "урок водіння", "leçon de conduite", "exam", []),
    ("ausweis", "der Ausweis", "удостоверение личности", "ID card", "посвідчення особи", "pièce d'identité", "exam", []),
    ("reisepass", "der Reisepass", "загранпаспорт", "passport", "закордонний паспорт", "passeport", "exam", []),

    # === TECHNIK ===
    ("technische_frage", "die technische Frage", "технический вопрос", "technical question", "технічне питання", "question technique", "technik", ["core"]),
    ("betriebsbremse", "die Betriebsbremse", "рабочий тормоз", "service brake / foot brake", "робоче гальмо", "frein de service", "technik", ["core", "exam"], "Wie überprüfen Sie die Betriebsbremse?"),
    ("bremspedal", "das Bremspedal", "педаль тормоза", "brake pedal", "педаль гальма", "pédale de frein", "technik", []),
    ("feststellbremse", "die Feststellbremse", "стояночный тормоз", "handbrake / parking brake", "стоянкове гальмо", "frein de stationnement", "technik", ["core", "exam"], "Wie überprüfen Sie die Feststellbremse?"),
    ("handbremse", "die Handbremse", "ручной тормоз", "handbrake", "ручне гальмо", "frein à main", "technik", []),
    ("kontrollleuchte", "die Kontrollleuchte", "контрольная лампа", "warning light", "контрольна лампа", "voyant de contrôle", "technik", ["core"]),
    ("zuendung", "die Zündung", "зажигание", "ignition", "запалювання", "allumage", "technik", []),
    ("zuendung_an", "die Zündung an", "включить зажигание", "turn on ignition", "увімкнути запалювання", "mettre le contact", "technik", ["phrase"]),
    ("motor_aus", "den Motor aus", "заглушить двигатель", "turn off engine", "заглушити двигун", "couper le moteur", "technik", ["phrase"]),
    ("verkehrssicher", "verkehrssicher", "безопасный для дороги", "roadworthy", "безпечний для дороги", "en état de circuler", "technik", []),
    ("lenkradschloss", "das Lenkradschloss", "блокировка руля", "steering lock", "блокування керма", "antivol de direction", "technik", []),
    ("reifenzustand", "der Reifenzustand", "состояние шин", "tyre condition", "стан шин", "état des pneus", "technik", ["exam"], "Wie prüfen Sie den Reifenzustand?"),
    ("profiltiefe", "die Profiltiefe", "глубина протектора", "tread depth", "глибина протектора", "profondeur de sculpture", "technik", []),
    ("beleuchtung_pruefen", "die Beleuchtung prüfen", "проверить освещение", "check the lights", "перевірити освітлення", "vérifier l'éclairage", "technik", ["exam"], "Wie prüfen Sie die Beleuchtung?"),

    # === CAR ===
    ("auto", "das Auto", "автомобиль", "car", "автомобіль", "voiture", "car", ["core"]),
    ("pkw", "der PKW", "легковой автомобиль", "passenger car", "легковий автомобіль", "voiture particulière", "car", []),
    ("motor", "der Motor", "двигатель", "engine", "двигун", "moteur", "car", []),
    ("getriebe", "das Getriebe", "коробка передач", "gearbox", "коробка передач", "boîte de vitesses", "car", []),
    ("lenkrad", "das Lenkrad", "руль", "steering wheel", "кермо", "volant", "car", ["core"]),
    ("gaspedal", "das Gaspedal", "педаль газа", "accelerator pedal", "педаль газу", "pédale d'accélération", "car", []),
    ("kupplung", "die Kupplung", "сцепление", "clutch", "зчеплення", "embrayage", "car", ["core"]),
    ("kupplungspedal", "das Kupplungspedal", "педаль сцепления", "clutch pedal", "педаль зчеплення", "pédale d'embrayage", "car", []),
    ("erster_gang", "der erste Gang", "первая передача", "first gear", "перша передача", "première vitesse", "car", ["core"]),
    ("rueckwaertsgang", "der Rückwärtsgang", "задняя передача", "reverse gear", "задня передача", "marche arrière", "car", ["core"]),
    ("leerlauf", "der Leerlauf", "нейтральная передача", "neutral", "нейтральна передача", "point mort", "car", []),
    ("schaltgetriebe", "das Schaltgetriebe", "механическая КПП", "manual transmission", "механічна КПП", "boîte manuelle", "car", []),
    ("automatikgetriebe", "das Automatikgetriebe", "автоматическая КПП", "automatic transmission", "автоматична КПП", "boîte automatique", "car", []),
    ("rückspiegel", "der Rückspiegel", "внутреннее зеркало", "rear-view mirror", "внутрішнє дзеркало", "rétroviseur intérieur", "car", ["core"]),
    ("aussenspiegel", "der Außenspiegel", "боковое зеркало", "side mirror", "бокове дзеркало", "rétroviseur extérieur", "car", ["core"]),
    ("totwinkel", "der Totwinkel", "слепая зона", "blind spot", "сліпа зона", "angle mort", "car", ["core"]),
    ("sitz", "der Sitz", "сиденье", "seat", "сидіння", "siège", "car", []),
    ("fahrersitz", "der Fahrersitz", "сиденье водителя", "driver's seat", "сидіння водія", "siège conducteur", "car", []),
    ("kopfstuetze", "die Kopfstütze", "подголовник", "headrest", "підголівник", "appui-tête", "car", ["core"]),
    ("sicherheitsgurt", "der Sicherheitsgurt", "ремень безопасности", "seat belt", "ремінь безпеки", "ceinture de sécurité", "car", ["core"]),
    ("windschutzscheibe", "die Windschutzscheibe", "лобовое стекло", "windscreen", "лобове скло", "pare-brise", "car", []),
    ("heckscheibe", "die Heckscheibe", "заднее стекло", "rear window", "заднє скло", "lunette arrière", "car", []),
    ("motorhaube", "die Motorhaube", "капот", "bonnet / hood", "капот", "capot", "car", []),
    ("kofferraum", "der Kofferraum", "багажник", "boot / trunk", "багажник", "coffre", "car", []),
    ("reifen", "der Reifen", "шина", "tyre", "шина", "pneu", "car", []),
    ("rad", "das Rad", "колесо", "wheel", "колесо", "roue", "car", []),
    ("bordstein", "der Bordstein", "бордюр", "kerb", "бордюр", "bordure", "car", []),
    ("tank", "der Tank", "бак", "fuel tank", "бак", "réservoir", "car", []),
    ("armaturenbrett", "das Armaturenbrett", "приборная панель", "dashboard", "панель приладів", "tableau de bord", "car", []),
    ("tacho", "der Tacho", "спидометр", "speedometer", "спідометр", "compteur de vitesse", "car", []),
    ("drehzahlmesser", "der Drehzahlmesser", "тахометр", "rev counter", "тахометр", "compte-tours", "car", []),
    ("blinker", "der Blinker", "поворотник", "indicator / turn signal", "поворотник", "clignotant", "car", ["core"]),
    ("hupe", "die Hupe", "звуковой сигнал", "horn", "сигнал", "klaxon", "car", []),
    ("scheibenwischer", "der Scheibenwischer", "стеклоочиститель", "windscreen wiper", "склоочисник", "essuie-glace", "car", []),
    ("schluessel", "der Schlüssel", "ключ зажигания", "key", "ключ запалювання", "clé de contact", "car", []),
    ("startknopf", "der Startknopf", "кнопка запуска", "start button", "кнопка запуску", "bouton de démarrage", "car", []),

    # === LIGHTS ===
    ("abblendlicht", "das Abblendlicht", "ближний свет", "dipped beam", "ближнє світло", "feux de croisement", "lights", ["core", "exam"]),
    ("fernlicht", "das Fernlicht", "дальний свет", "main beam / high beam", "далеке світло", "feux de route", "lights", ["core", "exam"]),
    ("standlicht", "das Standlicht", "габаритные огни", "side lights", "габаритні вогні", "feux de position", "lights", []),
    ("tagfahrlicht", "das Tagfahrlicht", "дневные ходовые огни", "daytime running lights", "денні ходові вогні", "feux de jour", "lights", []),
    ("nebelscheinwerfer", "der Nebelscheinwerfer", "противотуманные фары", "fog lights", "протитуманні фари", "feux antibrouillard", "lights", []),
    ("nebelschlusslicht", "das Nebelschlusslicht", "задний противотуманный фонарь", "rear fog light", "задній протитуманний ліхтар", "feu antibrouillard arrière", "lights", []),
    ("ruecklicht", "das Rücklicht", "задний габарит", "tail light", "задній габарит", "feu arrière", "lights", []),
    ("bremslicht", "das Bremslicht", "стоп-сигнал", "brake light", "стоп-сигнал", "feu de freinage", "lights", []),
    ("rueckfahrlicht", "das Rückfahrlicht", "фонарь заднего хода", "reversing light", "ліхтар заднього ходу", "feu de marche arrière", "lights", []),
    ("warnblinkanlage", "die Warnblinkanlage", "аварийная сигнализация", "hazard warning lights", "аварійна сигналізація", "feux de détresse", "lights", ["core"]),
    ("kontrollleuchte_oel", "die Kontrollleuchte für Öldruck", "лампа давления масла", "oil pressure warning light", "лампа тиску масла", "voyant de pression d'huile", "lights", []),
    ("kontrollleuchte_batterie", "die Kontrollleuchte für die Batterie", "лампа аккумулятора", "battery warning light", "лампа акумулятора", "voyant de batterie", "lights", []),
    ("kontrollleuchte_abs", "die Kontrollleuchte für ABS", "лампа ABS", "ABS warning light", "лампа ABS", "voyant ABS", "lights", []),
    ("kontrollleuchte_esp", "die Kontrollleuchte für ESP", "лампа ESP", "ESP warning light", "лампа ESP", "voyant ESP", "lights", []),
    ("kontrollleuchte_airbag", "die Kontrollleuchte für Airbag", "лампа подушки безопасности", "airbag warning light", "лампа подушки безпеки", "voyant airbag", "lights", []),

    # === BRAKES ===
    ("bremsanlage", "die Bremsanlage", "тормозная система", "braking system", "гальмівна система", "système de freinage", "brakes", []),
    ("bremsfluessigkeit", "die Bremsflüssigkeit", "тормозная жидкость", "brake fluid", "гальмівна рідина", "liquide de frein", "brakes", []),
    ("bremsbelag", "der Bremsbelag", "тормозная колодка", "brake pad", "гальмівна колодка", "plaquette de frein", "brakes", []),
    ("bremsscheibe", "die Bremsscheibe", "тормозной диск", "brake disc", "гальмівний диск", "disque de frein", "brakes", []),
    ("abs", "das ABS", "антиблокировочная система", "anti-lock braking system", "антиблокувальна система", "système antiblocage", "brakes", []),
    ("esp", "das ESP", "система стабилизации", "electronic stability program", "система стабілізації", "programme de stabilité électronique", "brakes", []),
    ("bremsweg", "der Bremsweg", "тормозной путь", "braking distance", "гальмівний шлях", "distance de freinage", "brakes", []),
    ("anhalteweg", "der Anhalteweg", "путь остановки", "stopping distance", "шлях зупинки", "distance d'arrêt", "brakes", []),
    ("gefahrenbremsung", "die Gefahrenbremsung", "экстренное торможение", "emergency braking", "екстрене гальмування", "freinage d'urgence", "brakes", ["core"]),
    ("vollbremsung", "die Vollbremsung", "полное торможение", "full braking", "повне гальмування", "freinage complet", "brakes", []),
    ("motorbremse", "die Motorbremse", "торможение двигателем", "engine braking", "гальмування двигуном", "frein moteur", "brakes", []),
    ("handbremse_anziehen", "die Handbremse anziehen", "поставить ручник", "pull handbrake", "поставити ручник", "serrer le frein à main", "brakes", ["phrase"]),
    ("handbremse_loesen", "die Handbremse lösen", "отпустить ручник", "release handbrake", "відпустити ручник", "relâcher le frein à main", "brakes", ["phrase"]),

    # === FLUIDS ===
    ("motoroel", "das Motoröl", "моторное масло", "engine oil", "моторна олива", "huile moteur", "fluids", []),
    ("oelstand", "der Ölstand", "уровень масла", "oil level", "рівень оливи", "niveau d'huile", "fluids", ["exam"], "Wie überprüfen Sie den Ölstand?"),
    ("oelpeilstab", "der Ölpeilstab", "щуп масла", "dipstick", "щуп оливи", "jauge d'huile", "fluids", []),
    ("kuehlmittel", "das Kühlmittel", "охлаждающая жидкость", "coolant", "охолоджувальна рідина", "liquide de refroidissement", "fluids", []),
    ("kuehlwasserstand", "der Kühlwasserstand", "уровень охлаждающей жидкости", "coolant level", "рівень охолоджувальної рідини", "niveau de liquide de refroidissement", "fluids", []),
    ("scheibenwaschfluessigkeit", "die Scheibenwaschflüssigkeit", "жидкость омывателя", "windscreen washer fluid", "рідина омивача", "liquide lave-glace", "fluids", []),
    ("kraftstoff", "der Kraftstoff", "топливо", "fuel", "паливо", "carburant", "fluids", []),
    ("benzin", "das Benzin", "бензин", "petrol / gasoline", "бензин", "essence", "fluids", []),
    ("diesel", "der Diesel", "дизель", "diesel", "дизель", "diesel", "fluids", []),
    ("batterie", "die Batterie", "аккумулятор", "battery", "акумулятор", "batterie", "fluids", []),
    ("reifendruck", "der Reifendruck", "давление в шинах", "tyre pressure", "тиск у шинах", "pression des pneus", "fluids", []),

    # === SAFETY ===
    ("airbag", "der Airbag", "подушка безопасности", "airbag", "подушка безпеки", "airbag", "safety", []),
    ("kindersitz", "der Kindersitz", "детское кресло", "child seat", "дитяче крісло", "siège enfant", "safety", []),
    ("isofix", "die Isofix-Haltevorrichtung", "крепление Isofix", "Isofix mount", "кріплення Isofix", "fixation Isofix", "safety", []),
    ("warndreieck", "das Warndreieck", "знак аварийной остановки", "warning triangle", "знак аварійної зупинки", "triangle de signalisation", "safety", ["core"]),
    ("warnweste", "die Warnweste", "светоотражающий жилет", "high-visibility vest", "світловідбивний жилет", "gilet de sécurité", "safety", ["core"]),
    ("verbandskasten", "der Verbandskasten", "аптечка", "first-aid kit", "аптечка", "trousse de secours", "safety", []),
    ("notfallausruestung", "die Notfallausrüstung", "аварийный комплект", "emergency equipment", "аварійний комплект", "équipement de secours", "safety", []),
    ("winterreifen", "der Winterreifen", "зимняя шина", "winter tyre", "зимова шина", "pneu hiver", "safety", []),
    ("sommerreifen", "der Sommerreifen", "летняя шина", "summer tyre", "літня шина", "pneu été", "safety", []),

    # === ASSIST ===
    ("assistenzsystem", "das Assistenzsystem", "система помощи водителю", "driver assistance system", "система допомоги водію", "système d'aide à la conduite", "assist", ["core"]),
    ("acc", "der ACC", "адаптивный круиз-контроль", "adaptive cruise control", "адаптивний круїз-контроль", "régulateur de vitesse adaptatif", "assist", ["core", "exam"]),
    ("tempomat", "der Tempomat", "круиз-контроль", "cruise control", "круїз-контроль", "régulateur de vitesse", "assist", ["core"]),
    ("abstandsregler", "der Abstandsregler", "регулятор дистанции", "distance control", "регулятор дистанції", "régulateur de distance", "assist", []),
    ("parkautomatik", "die Parkautomatik", "автоматическая парковка", "parking assist", "автоматичне паркування", "aide au stationnement", "assist", ["exam"]),
    ("einparkassistent", "der Einparkassistent", "парковочный ассистент", "parking assistant", "парковочний асистент", "assistant de stationnement", "assist", []),
    ("parksensoren", "die Parksensoren", "парктроник", "parking sensors", "парктронік", "capteurs de stationnement", "assist", []),
    ("rueckfahrkamera", "die Rückfahrkamera", "камера заднего хода", "reversing camera", "камера заднього ходу", "caméra de recul", "assist", []),
    ("spurhalteassistent", "der Spurhalteassistent", "ассистент удержания в полосе", "lane keeping assist", "асистент утримання смуги", "aide au maintien de voie", "assist", []),
    ("notbremsassistent", "der Notbremsassistent", "ассистент экстренного торможения", "emergency brake assist", "асистент екстренного гальмування", "aide au freinage d'urgence", "assist", []),
    ("berganfahrassistent", "der Berganfahrassistent", "ассистент трогания на подъёме", "hill start assist", "асистент рушу на підйомі", "aide au démarrage en côte", "assist", []),

    # === MANEUVERS ===
    ("schulterblick", "der Schulterblick", "взгляд через плечо", "shoulder check", "погляд через плече", "contrôle de l'angle mort", "maneuvers", ["core"]),
    ("anfahren", "anfahren", "тронуться с места", "to pull away", "рушити з місця", "démarrer", "maneuvers", ["verb", "core"]),
    ("anhalten", "anhalten", "остановиться", "to stop", "зупинитися", "s'arrêter", "maneuvers", ["verb", "core"]),
    ("abbiegen", "abbiegen", "повернуть", "to turn", "повернути", "tourner", "maneuvers", ["verb", "core"]),
    ("links_abbiegen", "links abbiegen", "повернуть налево", "turn left", "повернути ліворуч", "tourner à gauche", "maneuvers", ["phrase"]),
    ("rechts_abbiegen", "rechts abbiegen", "повернуть направо", "turn right", "повернути праворуч", "tourner à droite", "maneuvers", ["phrase"]),
    ("ueberholen", "überholen", "обогнать", "to overtake", "обігнати", "dépasser", "maneuvers", ["verb"]),
    ("einscheren", "einscheren", "перестроиться в ряд", "to merge in", "перебудуватися в ряд", "se rabattre", "maneuvers", ["verb"]),
    ("ausscheren", "ausscheren", "выехать из ряда", "to pull out", "виїхати з ряду", "sortir de la file", "maneuvers", ["verb"]),
    ("spurwechsel", "der Spurwechsel", "смена полосы", "lane change", "зміна смуги", "changement de voie", "maneuvers", []),
    ("einparken", "einparken", "припарковаться", "to park", "припаркуватися", "se garer", "maneuvers", ["verb", "core"]),
    ("ausparken", "ausparken", "выехать с парковки", "to pull out of parking", "виїхати з парковки", "sortir d'un stationnement", "maneuvers", ["verb"]),
    ("rueckwaertsfahren", "rückwärtsfahren", "движение задним ходом", "to reverse", "рух заднім ходом", "reculer", "maneuvers", ["verb"]),
    ("rangieren", "rangieren", "маневрировать", "to manoeuvre", "маневрувати", "manœuvrer", "maneuvers", ["verb"]),
    ("wenden", "wenden", "развернуться", "to turn around", "розвернутися", "faire demi-tour", "maneuvers", ["verb"]),
    ("umkehren", "umkehren", "развернуться / сделать разворот", "to make a U-turn", "розвернутися", "inverser la marche", "maneuvers", ["verb", "core"]),
    ("durchlassen", "durchlassen", "пропустить", "to let pass", "пропустити", "laisser passer", "maneuvers", ["verb"]),
    ("vorfahrt_gewaehren", "Vorfahrt gewähren", "уступить дорогу", "give way", "поступитися дорогою", "céder le passage", "maneuvers", ["phrase", "core"]),
    ("vorausschauend_fahren", "vorausschauend fahren", "ехать с упреждением", "to drive anticipatorily", "їхати з випередженням", "conduire avec anticipation", "maneuvers", ["phrase", "core"]),
    ("sich_einordnen", "sich einordnen", "выстроиться", "to position oneself", "вибудуватися", "se placer", "maneuvers", ["verb"]),
    ("sich_rechts_einordnen", "sich rechts einordnen", "выстроиться справа", "position on the right", "вибудуватися праворуч", "se placer à droite", "maneuvers", ["phrase", "core"]),
    ("grosser_bogen", "der große Bogen", "широкая дуга", "wide arc", "широка дуга", "grand virage", "maneuvers", []),
    ("schleifende_kupplung", "die schleifende Kupplung", "полувыжатое сцепление", "slipping clutch / biting point", "напіввивільнене зчеплення", "embrayage en prise douce", "maneuvers", []),
    ("schrittgeschwindigkeit", "die Schrittgeschwindigkeit", "скорость шага (~7 км/ч)", "walking pace", "швидкість кроку", "allure piétonne", "maneuvers", []),
    ("passgeschwindigkeit", "die Passgeschwindigkeit", "очень медленная скорость", "very slow speed", "дуже повільна швидкість", "vitesse très lente", "maneuvers", []),
    ("motor_abwueren", "den Motor abwürgen", "заглохнуть", "to stall", "заглохнути", "caler le moteur", "maneuvers", ["phrase"]),
    ("sich_anschnallen", "sich anschnallen", "пристегнуться", "to fasten seat belt", "пристебнутися", "s'attacher", "maneuvers", ["verb", "core"]),
    ("kopf_nach_hinten", "den Kopf nach hinten drehen", "повернуть голову назад", "look over shoulder backwards", "повернути голову назад", "tourner la tête vers l'arrière", "maneuvers", ["phrase"]),

    # === GRUNDFAHRAUFGABEN ===
    ("parken_laengs", "das Parken in Längsaufstellung", "параллельная парковка вдоль бордюра", "parallel parking", "паралельне паркування вздовж бордюра", "stationnement en créneau", "grundaufgaben", ["core"]),
    ("rueckwaerts_einparken", "rückwärts einparken", "парковка задним ходом", "reverse parking", "паркування заднім ходом", "garer en marche arrière", "grundaufgaben", ["phrase"]),
    ("vorwaerts_einparken", "vorwärts einparken", "парковка передом", "forward parking", "паркування передом", "garer en marche avant", "grundaufgaben", ["phrase"]),
    ("wendehammer", "der Wendehammer", "площадка для разворота", "turning bay", "майданчик для розвороту", "boucle de retournement", "grundaufgaben", []),
    ("parkluecke", "die Parklücke", "парковочное место", "parking space", "парковочне місце", "place de stationnement", "grundaufgaben", []),
    ("parkbox", "die Parkbox", "парковочный карман", "parking bay", "парковочна ніша", "emplacement de stationnement", "grundaufgaben", []),
    ("30cm_bordstein", "nicht weiter als 30 cm vom Bordstein", "не дальше 30 см от бордюра", "no more than 30 cm from kerb", "не далі 30 см від бордюра", "pas plus de 30 cm du trottoir", "grundaufgaben", ["phrase"]),
    ("fertig_sagen", "So, fertig.", "Готово. (сообщить экзаменатору)", "Done. (tell examiner)", "Готово.", "C'est fini.", "grundaufgaben", ["phrase"]),

    # === TRAFFIC ===
    ("ampel", "die Ampel", "светофор", "traffic light", "світлофор", "feu tricolore", "traffic", ["core"]),
    ("vorfahrt", "die Vorfahrt", "приоритет", "right of way", "перевага", "priorité", "traffic", ["core"]),
    ("vorfahrtstrasse", "die Vorfahrtstraße", "главная дорога", "priority road", "головна дорога", "route prioritaire", "traffic", ["core"]),
    ("rechts_vor_links", "rechts vor links", "помеха справа", "priority to the right", "перешкода справа", "priorité à droite", "traffic", ["core", "phrase"]),
    ("einbahnstrasse", "die Einbahnstraße", "одностороннее движение", "one-way street", "односторонній рух", "rue à sens unique", "traffic", []),
    ("hindernis", "das Hindernis", "препятствие", "obstacle", "перешкода", "obstacle", "traffic", ["core"]),
    ("gegenverkehr", "der Gegenverkehr", "встречный поток", "oncoming traffic", "зустрічний потік", "circulation en sens inverse", "traffic", ["core"]),
    ("freie_luecke", "die freie Lücke", "свободное окно в потоке", "gap in traffic", "вільне вікно в потоці", "trou dans la circulation", "traffic", []),
    ("verkehrszeichen", "das Verkehrszeichen", "дорожный знак", "traffic sign", "дорожній знак", "panneau de signalisation", "traffic", ["core"]),
    ("gefahrenzeichen", "das Gefahrenzeichen", "предупреждающий знак", "warning sign", "попереджувальний знак", "panneau de danger", "traffic", []),
    ("stoppschild", "das Stoppschild", "знак STOP", "stop sign", "знак STOP", "panneau STOP", "traffic", []),
    ("haltverbot", "das Haltverbot", "запрет остановки", "no stopping", "заборона зупинки", "arrêt interdit", "traffic", []),
    ("parkverbot", "das Parkverbot", "запрет стоянки", "no parking", "заборона стоянки", "stationnement interdit", "traffic", []),
    ("kreuzung", "die Kreuzung", "перекрёсток", "intersection", "перехрестя", "carrefour", "traffic", ["core"]),
    ("richtlinie", "die Richtlinie", "линия разметки", "road marking line", "лінія розмітки", "ligne de marquage", "traffic", []),
    ("kreisverkehr", "der Kreisverkehr", "круговое движение", "roundabout", "кільцевий рух", "rond-point", "traffic", []),
    ("kreisel", "der Kreisel", "круговое движение (разг.)", "roundabout (colloq.)", "кільце (розм.)", "rond-point (fam.)", "traffic", []),
    ("autobahn", "die Autobahn", "автобан", "motorway", "автобан", "autoroute", "traffic", []),
    ("kraftfahrstrasse", "die Kraftfahrstraße", "скоростная дорога", "expressway", "швидкісна дорога", "voie rapide", "traffic", []),
    ("geschlossene_ortschaft", "die geschlossene Ortschaft", "населённый пункт", "built-up area", "населений пункт", "agglomération", "traffic", ["core"]),
    ("ortseingangstafel", "die Ortseingangstafel", "знак въезда в населённый пункт", "town entry sign", "знак в'їзду в населений пункт", "panneau d'entrée d'agglomération", "traffic", []),
    ("hoechstgeschwindigkeit", "die Höchstgeschwindigkeit", "максимальная скорость", "maximum speed", "максимальна швидкість", "vitesse maximale", "traffic", []),
    ("tempolimit", "das Tempolimit", "лимит скорости", "speed limit", "ліміт швидкості", "limitation de vitesse", "traffic", []),
    ("rechtsfahrgebot", "das Rechtsfahrgebot", "правило «держись правее»", "keep right rule", "правило «тримайся правіше»", "obligation de tenir la droite", "traffic", ["core"]),
    ("fahrstreifen", "der Fahrstreifen", "полоса движения", "lane", "смуга руху", "voie", "traffic", []),
    ("fussgaenger", "der Fußgänger", "пешеход", "pedestrian", "пішохід", "piéton", "traffic", ["core"]),
    ("fussgaengerueberweg", "der Fußgängerüberweg", "пешеходный переход", "pedestrian crossing", "пішохідний перехід", "passage piéton", "traffic", ["core"]),
    ("zebrastreifen", "der Zebrastreifen", "пешеходный переход (зебра)", "zebra crossing", "пішохідний перехід (зебра)", "passage clouté", "traffic", []),
    ("radfahrer", "der Radfahrer", "велосипедист", "cyclist", "велосипедист", "cycliste", "traffic", ["core"]),
    ("radweg", "der Radweg", "велодорожка", "cycle path", "велодоріжка", "piste cyclable", "traffic", []),
    ("seitenabstand", "der Seitenabstand", "боковой зазор", "lateral clearance", "боковий зазор", "distance latérale", "traffic", ["core"]),
    ("sicherheitsabstand", "der Sicherheitsabstand", "безопасная дистанция", "safe distance", "безпечна дистанція", "distance de sécurité", "traffic", []),
    ("verkehrsbehinderung", "die Verkehrsbehinderung", "помеха движению", "traffic obstruction", "перешкода руху", "gêne à la circulation", "traffic", []),
    ("bahnuebergang", "der Bahnübergang", "железнодорожный переезд", "level crossing", "залізничний переїзд", "passage à niveau", "traffic", []),
    ("andreaskreuz", "das Andreaskreuz", "знак ж/д переезда", "level crossing sign", "знак залізничного переїзду", "croix de Saint-André", "traffic", []),
    ("baustelle", "die Baustelle", "дорожные работы", "road works", "дорожні роботи", "chantier", "traffic", []),
    ("gefahrenstelle", "die Gefahrenstelle", "опасный участок", "hazard area", "небезпечна ділянка", "zone dangereuse", "traffic", []),
    ("rettungsgasse", "die Rettungsgasse", "коридор для спецтранспорта", "emergency lane", "коридор для спецтранспорту", "couloir de secours", "traffic", []),
    ("busspur", "die Busspur", "полоса для автобусов", "bus lane", "смуга для автобусів", "voie de bus", "traffic", []),
    ("vordermann", "der Vordermann", "водитель впереди", "driver ahead", "водій попереду", "conducteur devant", "traffic", []),
    ("fahrbahn", "die Fahrbahn", "проезжая часть", "carriageway", "проїзна частина", "chaussée", "traffic", []),
    ("fahrbahnueberquerung", "die Fahrbahnüberquerung", "пересечение проезжей части", "crossing the road", "перетин проїзної частини", "traversée de chaussée", "traffic", []),
    ("unbegrenzt", "unbegrenzt", "без ограничения (на участке)", "no limit (on section)", "без обмеження (на ділянці)", "sans limitation (sur le tronçon)", "traffic", []),
    ("gelbphase", "die Gelbphase", "жёлтая фаза светофора", "amber phase", "жовта фаза світлофора", "feu orange", "traffic", []),

    # === PHRASES (examiner) ===
    ("phrase_ausweis", "Zeigen Sie mir bitte Ihren Ausweis.", "Покажите удостоверение личности.", "Please show me your ID.", "Покажіть посвідчення особи.", "Montrez-moi votre pièce d'identité.", "phrases", ["examiner"], "Zeigen Sie mir bitte Ihren Ausweis."),
    ("phrase_bereit", "Fühlen Sie sich in der Lage, eine Prüfung zu fahren?", "Чувствуете ли вы себя готовым сдавать экзамен?", "Do you feel fit to take the test?", "Чи почуваєте себе готовим до іспиту?", "Vous sentez-vous en mesure de passer l'examen?", "phrases", ["examiner"]),
    ("phrase_weg", "Ich sage Ihnen heute den Weg an.", "Сегодня я буду указывать маршрут.", "I will direct you today.", "Сьогодні я вказуватиму маршрут.", "Je vous indiquerai le chemin aujourd'hui.", "phrases", ["examiner"]),
    ("phrase_geradeaus", "Wenn nichts gesagt wird, geradeaus.", "Если ничего не сказано — прямо.", "If nothing is said, go straight.", "Якщо нічого не сказано — прямо.", "Si rien n'est dit, tout droit.", "phrases", ["examiner"]),
    ("phrase_fernlicht", "Zeigen Sie mal die Kontrollleuchte fürs Fernlicht.", "Покажите лампу дальнего света.", "Show the main beam warning light.", "Покажіть лампу дальнього світла.", "Montrez le voyant des feux de route.", "phrases", ["examiner"], "Zeigen Sie mal die Kontrollleuchte fürs Fernlicht."),
    ("phrase_acc", "Benutzen Sie den ACC.", "Включите ACC.", "Use the ACC.", "Увімкніть ACC.", "Utilisez l'ACC.", "phrases", ["examiner"]),
    ("phrase_einparken", "Packen Sie hier irgendwo ein.", "Припаркуйтесь где-нибудь.", "Park somewhere here.", "Припаркуйтеся десь тут.", "Garez-vous quelque part ici.", "phrases", ["examiner"]),
    ("phrase_gefahrenbremse", "Bitte einmal eine Gefahrenbremse.", "Раз — экстренное торможение.", "Please do an emergency stop.", "Будь ласка, екстрене гальмування.", "Faites un freinage d'urgence.", "phrases", ["examiner"]),
    ("phrase_umkehren", "Ich will umkehren, ja sofort.", "Развернитесь прямо сейчас.", "Turn around right now.", "Розверніться прямо зараз.", "Faites demi-tour tout de suite.", "phrases", ["examiner"]),
    ("phrase_aussteigen", "Steigen Sie mal bitte aus.", "Выйдите, пожалуйста.", "Please get out.", "Вийдіть, будь ласка.", "Descendez, s'il vous plaît.", "phrases", ["examiner"]),
    ("phrase_bestanden", "Sie haben bestanden.", "Вы сдали.", "You have passed.", "Ви склали.", "Vous avez réussi.", "phrases", ["examiner"]),
    ("phrase_gut_gemacht", "Sie haben gut gemacht.", "Вы молодец.", "Well done.", "Ви молодець.", "Bien joué.", "phrases", ["examiner"]),
    ("phrase_kein_durchfall", "Das ist kein Durchfallgrund.", "Это не повод для провала.", "That is not a reason to fail.", "Це не привід для провалу.", "Ce n'est pas un motif d'échec.", "phrases", ["examiner"]),
    ("phrase_spiegel_blinker_schulter", "Spiegel, Blinker, Schulterblick.", "Зеркала, поворотник, взгляд через плечо.", "Mirror, indicator, shoulder check.", "Дзеркала, поворотник, погляд через плече.", "Rétroviseur, clignotant, contrôle d'angle mort.", "phrases", ["core"]),

    # === DOCUMENTS ===
    ("fahrerlaubnis", "die Fahrerlaubnis", "право на управление ТС", "driving entitlement", "право на керування ТЗ", "permis de conduire (droit)", "documents", []),
    ("fuehrerschein_probe", "der Führerschein auf Probe", "права на испытательный срок", "probationary licence", "права на випробувальний термін", "permis probatoire", "documents", []),
    ("fahrzeugschein", "der Fahrzeugschein", "свидетельство о регистрации (ч. I)", "vehicle registration document", "свідоцтво про реєстрацію (ч. I)", "certificat d'immatriculation (I)", "documents", []),
    ("kennzeichen", "das Kennzeichen", "номерной знак", "number plate", "номерний знак", "plaque d'immatriculation", "documents", []),
    ("versicherung", "die Versicherung", "страховка", "insurance", "страховка", "assurance", "documents", []),
    ("tuev", "der TÜV", "техосмотр (организация)", "MOT / technical inspection", "техогляд (організація)", "contrôle technique", "documents", []),
    ("hauptuntersuchung", "die Hauptuntersuchung (HU)", "основной техосмотр", "main inspection", "основний техогляд", "contrôle technique principal", "documents", []),

    # === EMERGENCY ===
    ("panne", "die Panne", "поломка", "breakdown", "поломка", "panne", "emergency", []),
    ("unfall", "der Unfall", "ДТП", "accident", "ДТП", "accident", "emergency", []),
    ("verkehrsunfall", "der Verkehrsunfall", "дорожно-транспортное происшествие", "traffic accident", "дорожньо-транспортна пригода", "accident de la route", "emergency", []),
    ("standstreifen", "der Standstreifen", "обочина / аварийная полоса", "hard shoulder", "узбіччя", "bande d'arrêt d'urgence", "emergency", []),
    ("gefahrenstelle_absichern", "die Gefahrenstelle absichern", "обозначить опасное место", "secure the hazard area", "позначити небезпечне місце", "sécuriser la zone dangereuse", "emergency", ["phrase"]),
    ("warndreieck_aufstellen", "das Warndreieck aufstellen", "установить знак аварийной остановки", "place warning triangle", "встановити знак аварійної зупинки", "placer le triangle de signalisation", "emergency", ["phrase"]),
    ("warnweste_anziehen", "die Warnweste anziehen", "надеть светоотражающий жилет", "put on high-vis vest", "одягнути світловідбивний жилет", "enfiler le gilet de sécurité", "emergency", ["phrase"]),
    ("polizei_rufen", "die Polizei rufen", "вызвать полицию", "call the police", "викликати поліцію", "appeler la police", "emergency", ["phrase"]),
    ("abschleppdienst", "der Abschleppdienst", "эвакуатор", "breakdown service", "евакуатор", "service de dépannage", "emergency", []),
    ("reifenpanne", "die Reifenpanne", "прокол шины", "flat tyre", "прокол шини", "crevaison", "emergency", []),
]


def parse_article(de: str) -> Tuple[Optional[str], str]:
    for art in ("der ", "die ", "das ", "den ", "dem ", "des "):
        if de.startswith(art):
            return art.strip(), de[len(art):]
    return None, de


def build_vocabulary() -> dict:
    terms = []
    for row in TERMS:
        tid, de, ru, en, uk, fr, cat = row[:7]
        tags: list[str] = []
        exam_phrase = None
        if len(row) > 7:
            if isinstance(row[7], list):
                tags = row[7]
                if len(row) > 8:
                    exam_phrase = row[8]
            else:
                exam_phrase = row[7]

        article, de_base = parse_article(de)

        entry = {
            "id": tid,
            "de": de,
            "article": article,
            "de_base": de_base,
            "ru": ru,
            "en": en,
            "uk": uk,
            "fr": fr,
            "category": cat,
            "tags": tags,
        }
        if exam_phrase:
            entry["exam_phrase_de"] = exam_phrase
        terms.append(entry)

    return {
        "version": "1.0.0",
        "app": "FahrPrufungDE",
        "description": "Driving exam vocabulary for newcomers in Germany",
        "languages": ["de", "ru", "en", "uk", "fr"],
        "categories": CATEGORIES,
        "terms": terms,
        "meta": {
            "term_count": len(terms),
            "category_count": len(CATEGORIES),
        },
    }


SIGNS = [
    ("vorfahrt_gewaehren", "205", "yield", "Vorfahrt gewähren", "Уступите дорогу", "Give way", "Поступіться дорогою", "Cédez le passage", "vorfahrt",
     "An Kreuzungen und Einmündungen. Langsam anfahren und ggf. halten.",
     "На перекрёстках. Замедлиться и при необходимости остановиться."),
    ("stop", "206", "stop", "Stop", "Стоп", "Stop", "Стоп", "Stop", "vorfahrt",
     "Halt an der Haltelinie. Vorfahrt für alle.",
     "Полная остановка у линии. Уступить всем."),
    ("vorfahrtstrasse", "306", "priority_road", "Vorfahrtstraße", "Главная дорога", "Priority road", "Головна дорога", "Route prioritaire", "vorfahrt",
     "Gilt bis Schild Ende Vorfahrtstraße.",
     "Действует до знака конца главной дороги."),
    ("ende_vorfahrtstrasse", "307", "priority_road_end", "Ende der Vorfahrtstraße", "Конец главной дороги", "End of priority road", "Кінець головної дороги", "Fin de route prioritaire", "vorfahrt",
     "Ab hier gilt rechts vor links.",
     "Отсюда действует помеха справа."),
    ("rechts_vor_links", "—", "info", "Rechts vor links", "Помеха справа", "Priority to the right", "Перешкода справа", "Priorité à droite", "vorfahrt",
     "Grundregel an Kreuzungen ohne Ampel.",
     "Основное правило на перекрёстках без светофора."),
    ("zone_30", "274.1", "speed", "Tempo 30 Zone", "Зона 30", "30 km/h zone", "Зона 30", "Zone 30", "speed",
     "Höchstgeschwindigkeit 30 km/h in der ganzen Zone.",
     "Максимум 30 км/ч на всей территории зоны."),
    ("zone_50", "274.1", "speed", "Tempo 50", "Ограничение 50", "50 km/h limit", "Обмеження 50", "Limitation 50", "speed",
     "Höchstgeschwindigkeit 50 km/h.",
     "Максимальная скорость 50 км/ч."),
    ("haltverbot", "283", "prohibition", "Haltverbot", "Запрет остановки", "No stopping", "Заборона зупинки", "Arrêt interdit", "prohibition",
     "Anhalten und Halten verboten.",
     "Останавливаться и стоять нельзя."),
    ("parkverbot", "286", "prohibition", "Parkverbot", "Запрет стоянки", "No parking", "Заборона стоянки", "Stationnement interdit", "prohibition",
     "Parken verboten.",
     "Стоянка запрещена."),
    ("einbahnstrasse", "220", "mandatory", "Einbahnstraße", "Одностороннее движение", "One-way street", "Односторонній рух", "Rue à sens unique", "direction",
     "Nur in Pfeilrichtung fahren.",
     "Движение только в направлении стрелки."),
    ("andreaskreuz", "201", "danger", "Andreaskreuz", "Ж/д переезд", "Level crossing", "Залізничний переїзд", "Passage à niveau", "danger",
     "Bahn hat Vorrang. Links und rechts schauen.",
     "Поезд имеет приоритет."),
    ("fussgaengerueberweg", "293", "pedestrian", "Fußgängerüberweg", "Пешеходный переход", "Pedestrian crossing", "Пішохідний перехід", "Passage piéton", "pedestrian",
     "Fußgänger haben Vorrang.",
     "Пешеходы имеют приоритет."),
    ("baustelle", "123", "danger", "Baustelle", "Дорожные работы", "Road works", "Дорожні роботи", "Travaux", "danger",
     "Langsam fahren.",
     "Ехать медленно."),
    ("kreisverkehr", "215", "mandatory", "Kreisverkehr", "Круговое движение", "Roundabout", "Кільцевий рух", "Rond-point", "direction",
     "Vorfahrt für den Kreisverkehr.",
     "Приоритет у тех, кто на круге."),
    ("autobahn", "330.1", "info", "Autobahn", "Автобан", "Motorway", "Автобан", "Autoroute", "info",
     "Nur für Kraftfahrzeuge.",
     "Только для моторных ТС."),
    ("ende_aller_streckenverbote", "330.2", "info", "Ende aller Streckenverbote", "Конец ограничений", "End of restrictions", "Кінець обмежень", "Fin des interdits", "info",
     "Außerorts oft 100 km/h erlaubt.",
     "За городом часто 100 км/ч."),
    ("ortseingang", "310", "info", "Ortstafel", "Населённый пункт", "Town name sign", "Населений пункт", "Entrée d'agglomération", "info",
     "Geschlossene Ortschaft — Regeln innerorts.",
     "Населённый пункт — правила внутри."),
    ("umleitung", "455.1", "detour", "Umleitung", "Объезд", "Detour", "Об'їзд", "Déviation", "direction",
     "Dem angezeigten Weg folgen.",
     "Следовать указанному объезду."),
    ("rechtsfahrgebot", "—", "info", "Rechtsfahrgebot", "Держись правее", "Keep right", "Тримайся правіше", "Tenir la droite", "info",
     "So weit rechts wie möglich fahren.",
     "Держаться как можно правее."),
    ("busspur", "245", "mandatory", "Bussonderfahrstreifen", "Полоса для автобусов", "Bus lane", "Смуга для автобусів", "Voie de bus", "mandatory",
     "Nur Busse und freigegebene Fahrzeuge.",
     "Только автобусы и разрешённые ТС."),
]

SIGN_CATEGORIES = [
    {"id": "vorfahrt", "de": "Vorfahrt", "ru": "Приоритет", "en": "Priority", "uk": "Перевага", "fr": "Priorité"},
    {"id": "speed", "de": "Geschwindigkeit", "ru": "Скорость", "en": "Speed", "uk": "Швидкість", "fr": "Vitesse"},
    {"id": "prohibition", "de": "Verbote", "ru": "Запреты", "en": "Prohibitions", "uk": "Заборони", "fr": "Interdictions"},
    {"id": "danger", "de": "Gefahr", "ru": "Опасность", "en": "Danger", "uk": "Небезпека", "fr": "Danger"},
    {"id": "direction", "de": "Richtung", "ru": "Направление", "en": "Direction", "uk": "Направлення", "fr": "Direction"},
    {"id": "pedestrian", "de": "Fußgänger", "ru": "Пешеходы", "en": "Pedestrians", "uk": "Пішоходи", "fr": "Piétons"},
    {"id": "info", "de": "Hinweise", "ru": "Подсказки", "en": "Information", "uk": "Підказки", "fr": "Informations"},
    {"id": "mandatory", "de": "Gebote", "ru": "Предписания", "en": "Mandatory", "uk": "Пресрипції", "fr": "Obligations"},
]


def build_signs_placeholder() -> dict:
    signs = []
    for row in SIGNS:
        sid, code, shape, de, ru, en, uk, fr, cat, note_de, note_ru = row
        signs.append({
            "id": sid,
            "stvo_code": code,
            "shape": shape,
            "image": None,
            "de": de,
            "ru": ru,
            "en": en,
            "uk": uk,
            "fr": fr,
            "category": cat,
            "notes": {"de": note_de, "ru": note_ru, "en": note_de, "uk": note_ru, "fr": note_de},
        })
    return {
        "version": "1.1.0",
        "description": "Traffic signs with vector placeholders",
        "categories": SIGN_CATEGORIES,
        "signs": signs,
        "meta": {"sign_count": len(signs)},
    }


def main():
    RESOURCES.mkdir(parents=True, exist_ok=True)
    vocab = build_vocabulary()
    signs = build_signs_placeholder()

    vocab_path = RESOURCES / "vocabulary.json"
    signs_path = RESOURCES / "signs.json"

    with open(vocab_path, "w", encoding="utf-8") as f:
        json.dump(vocab, f, ensure_ascii=False, indent=2)

    with open(signs_path, "w", encoding="utf-8") as f:
        json.dump(signs, f, ensure_ascii=False, indent=2)

    print(f"Wrote {vocab['meta']['term_count']} terms → {vocab_path}")
    print(f"Wrote {signs['meta']['sign_count']} sign placeholders → {signs_path}")


if __name__ == "__main__":
    main()
