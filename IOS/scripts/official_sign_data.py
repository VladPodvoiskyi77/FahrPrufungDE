"""Official StVO-style sign translations for signs.json."""

from __future__ import annotations

import re

LANGS = ("ru", "en", "uk", "fr", "tr")

# Category labels (StVO / exam terminology)
CATEGORY_OFFICIAL: dict[str, dict[str, str]] = {
    "warning": {
        "de": "Gefahr",
        "ru": "Предупреждающие знаки",
        "en": "Warning signs",
        "uk": "Попереджувальні знаки",
        "fr": "Signaux d'avertissement",
        "tr": "Tehlike işaretleri",
    },
    "prohibitory": {
        "de": "Verbote",
        "ru": "Запрещающие знаки",
        "en": "Prohibitory signs",
        "uk": "Заборонні знаки",
        "fr": "Signaux d'interdiction",
        "tr": "Yasak işaretleri",
    },
    "mandatory": {
        "de": "Gebote",
        "ru": "Предписывающие знаки",
        "en": "Mandatory signs",
        "uk": "Обов'язкові знаки",
        "fr": "Signaux d'obligation",
        "tr": "Zorunluluk işaretleri",
    },
    "information": {
        "de": "Hinweise",
        "ru": "Информационно-указательные знаки",
        "en": "Information signs",
        "uk": "Інформаційно-вказівні знаки",
        "fr": "Signaux d'indication",
        "tr": "Bilgi işaretleri",
    },
    "additional": {
        "de": "Zusatz",
        "ru": "Знаки дополнительных сведений",
        "en": "Supplementary plates",
        "uk": "Знаки додаткових відомостей",
        "fr": "Panneaux additionnels",
        "tr": "Ek levha işaretleri",
    },
}

# Exact German title → official translations (exam / StVO wording)
EXACT_TITLE: dict[str, dict[str, str]] = {
  # --- warning ---
  "Gefahrstelle": {
    "ru": "Место повышенной опасности",
    "en": "General hazard",
    "uk": "Місце підвищеної небезпеки",
    "fr": "Danger",
    "tr": "Tehlike",
  },
  "Kreuzung oder Einmündung": {
    "ru": "Перекрёсток или примыкание",
    "en": "Intersection or junction",
    "uk": "Перехрестя або приєднання",
    "fr": "Carrefour ou jonction",
    "tr": "Kavşak veya birleşme",
  },
  "Kurve – links": {
    "ru": "Опасный поворот налево",
    "en": "Curve to the left",
    "uk": "Небезпечний поворот ліворуч",
    "fr": "Virage à gauche",
    "tr": "Sola tehlikeli viraj",
  },
  "Kurve – rechts": {
    "ru": "Опасный поворот направо",
    "en": "Curve to the right",
    "uk": "Небезпечний поворот праворуч",
    "fr": "Virage à droite",
    "tr": "Sağa tehlikeli viraj",
  },
  "Doppelkurve – zunächst links": {
    "ru": "Двойной поворот, сначала налево",
    "en": "Double curve, first to the left",
    "uk": "Подвійний поворот, спочатку ліворуч",
    "fr": "Virage en S, d'abord à gauche",
    "tr": "Çift viraj, önce sola",
  },
  "Doppelkurve – zunächst rechts": {
    "ru": "Двойной поворот, сначала направо",
    "en": "Double curve, first to the right",
    "uk": "Подвійний поворот, спочатку праворуч",
    "fr": "Virage en S, d'abord à droite",
    "tr": "Çift viraj, önce sağa",
  },
  "Unebene Fahrbahn": {
    "ru": "Неровное покрытие",
    "en": "Uneven road surface",
    "uk": "Нерівне покриття",
    "fr": "Chaussée déformée",
    "tr": "Bozuk yol yüzeyi",
  },
  "Schleuder- oder Rutschgefahr": {
    "ru": "Опасность заноса или скольжения",
    "en": "Risk of skidding or slipping",
    "uk": "Небезпека заносу або ковзання",
    "fr": "Risque de dérapage ou de glissade",
    "tr": "Kayma veya savrulma tehlikesi",
  },
  "Seitenwind von rechts": {
    "ru": "Боковой ветер справа",
    "en": "Crosswind from the right",
    "uk": "Боковий вітер праворуч",
    "fr": "Vent latéral venant de droite",
    "tr": "Sağdan yan rüzgâr",
  },
  "Seitenwind von links": {
    "ru": "Боковой ветер слева",
    "en": "Crosswind from the left",
    "uk": "Боковий вітер ліворуч",
    "fr": "Vent latéral venant de gauche",
    "tr": "Soldan yan rüzgâr",
  },
  "Verengte Fahrbahn": {
    "ru": "Сужение проезжей части",
    "en": "Road narrows",
    "uk": "Звуження проїжджої частини",
    "fr": "Chaussée rétrécie",
    "tr": "Yol daralması",
  },
  "Einseitig verengte Fahrbahn – Verengung rechts": {
    "ru": "Сужение проезжей части справа",
    "en": "Road narrows on the right",
    "uk": "Звуження проїжджої частини праворуч",
    "fr": "Chaussée rétrécie à droite",
    "tr": "Yol sağdan daralıyor",
  },
  "Einseitig verengte Fahrbahn – Verengung links": {
    "ru": "Сужение проезжей части слева",
    "en": "Road narrows on the left",
    "uk": "Звуження проїжджої частини ліворуч",
    "fr": "Chaussée rétrécie à gauche",
    "tr": "Yol soldan daralıyor",
  },
  "Arbeitsstelle": {
    "ru": "Дорожные работы",
    "en": "Road works",
    "uk": "Дорожні роботи",
    "fr": "Travaux",
    "tr": "Yol çalışması",
  },
  "Stau": {
    "ru": "Затор",
    "en": "Traffic queue",
    "uk": "Затор",
    "fr": "Embouteillage",
    "tr": "Trafik sıkışıklığı",
  },
  "Gegenverkehr": {
    "ru": "Встречное движение",
    "en": "Oncoming traffic",
    "uk": "Зустрічний рух",
    "fr": "Circulation en sens inverse",
    "tr": "Karşı yönden trafik",
  },
  "Lichtzeichenanlage": {
    "ru": "Светофорная установка",
    "en": "Traffic signals ahead",
    "uk": "Світлофорна установка",
    "fr": "Feux tricolores",
    "tr": "Trafik ışıkları",
  },
  "Bahnübergang": {
    "ru": "Железнодорожный переезд",
    "en": "Level crossing",
    "uk": "Залізничний переїзд",
    "fr": "Passage à niveau",
    "tr": "Demiryolu geçidi",
  },
  "Schnee- oder Eisglätte": {
    "ru": "Скользко из-за снега или льда",
    "en": "Snow or ice hazard",
    "uk": "Слизько через сніг або лід",
    "fr": "Neige ou verglas",
    "tr": "Kar veya buzlanma",
  },
  "Splitt, Schotter": {
    "ru": "Гравийное покрытие",
    "en": "Loose gravel",
    "uk": "Гравійне покриття",
    "fr": "Gravier",
    "tr": "Çakıllı yol",
  },
  "Ufer": {
    "ru": "Берег или обрыв у воды",
    "en": "Riverbank or quayside",
    "uk": "Берег або обрив біля води",
    "fr": "Berge ou quai",
    "tr": "Kıyı veya su kenarı",
  },
  "Unzureichendes Lichtraumprofil": {
    "ru": "Недостаточная высота проезда",
    "en": "Limited clearance height",
    "uk": "Недостатня висота проїзду",
    "fr": "Hauteur libre insuffisante",
    "tr": "Yetersiz geçiş yüksekliği",
  },
  "Bewegliche Brücke": {
    "ru": "Разводной мост",
    "en": "Opening or swing bridge",
    "uk": "Розвідний міст",
    "fr": "Pont mobile",
    "tr": "Açılır köprü",
  },
  "Andreaskreuz — stehend: Dem Schienenverkehr Vorrang gewähren!": {
    "ru": "Знак «Крест Святого Андрея» (вертикальный): уступить железнодорожному транспорту",
    "en": "St Andrew's cross (upright): give way to rail traffic",
    "uk": "Знак «Хрест святого Андрія» (вертикальний): поступитися залізничному транспорту",
    "fr": "Croix de Saint-André (verticale) : céder le passage au rail",
    "tr": "Andrea haçı (dikey): demiryolu trafiğine yol verin",
  },
  "Andreaskreuz — stehend mit Blitzpfeil: Dem Schienenverkehr Vorrang gewähren!": {
    "ru": "Знак «Крест Святого Андрея» (вертикальный, со стрелкой): уступить железнодорожному транспорту",
    "en": "St Andrew's cross (upright, with arrow): give way to rail traffic",
    "uk": "Знак «Хрест святого Андрія» (вертикальний, зі стрілкою): поступитися залізничному транспорту",
    "fr": "Croix de Saint-André (verticale, flèche) : céder le passage au rail",
    "tr": "Andrea haçı (dikey, ok): demiryolu trafiğine yol verin",
  },
  "Andreaskreuz — liegend: Dem Schienenverkehr Vorrang gewähren!": {
    "ru": "Знак «Крест Святого Андрея» (горизонтальный): уступить железнодорожному транспорту",
    "en": "St Andrew's cross (horizontal): give way to rail traffic",
    "uk": "Знак «Хрест святого Андрія» (горизонтальний): поступитися залізничному транспорту",
    "fr": "Croix de Saint-André (horizontale) : céder le passage au rail",
    "tr": "Andrea haçı (yatay): demiryolu trafiğine yol verin",
  },
  "Andreaskreuz — liegend mit Blitzpfeil: Dem Schienenverkehr Vorrang gewähren!": {
    "ru": "Знак «Крест Святого Андрея» (горизонтальный, со стрелкой): уступить железнодорожному транспорту",
    "en": "St Andrew's cross (horizontal, with arrow): give way to rail traffic",
    "uk": "Знак «Хрест святого Андрія» (горизонтальний, зі стрілкою): поступитися залізничному транспорту",
    "fr": "Croix de Saint-André (horizontale, flèche) : céder le passage au rail",
    "tr": "Andrea haçı (yatay, ok): demiryolu trafiğine yol verin",
  },
  # --- prohibitory ---
  "Halt. Vorfahrt gewähren": {
    "ru": "Остановка. Предоставление преимущества в движении",
    "en": "Stop. Give way",
    "uk": "Зупинка. Надання переваги в русі",
    "fr": "Stop. Cédez le passage",
    "tr": "Dur. Yol verin",
  },
  "Halt. Vorfahrt gewähren.": {
    "ru": "Остановка. Предоставление преимущества в движении",
    "en": "Stop. Give way",
    "uk": "Зупинка. Надання переваги в русі",
    "fr": "Stop. Cédez le passage",
    "tr": "Dur. Yol verin",
  },
  "Vorfahrt gewähren.": {
    "ru": "Предоставление преимущества в движении",
    "en": "Give way",
    "uk": "Надання переваги в русі",
    "fr": "Cédez le passage",
    "tr": "Yol verin",
  },
  "Verbot der Einfahrt": {
    "ru": "Въезд запрещён",
    "en": "No entry",
    "uk": "В'їзд заборонено",
    "fr": "Sens interdit",
    "tr": "Giriş yasak",
  },
  "Verbot des Wendens": {
    "ru": "Разворот запрещён",
    "en": "No U-turn",
    "uk": "Розворот заборонено",
    "fr": "Interdiction de faire demi-tour",
    "tr": "U dönüşü yasak",
  },
  "Zulässige Höchstgeschwindigkeit": {
    "ru": "Ограничение максимальной скорости",
    "en": "Maximum speed limit",
    "uk": "Обмеження максимальної швидкості",
    "fr": "Limitation de vitesse maximale",
    "tr": "Azami hız sınırı",
  },
  "Ende der zulässigen Höchstgeschwindigkeit": {
    "ru": "Конец ограничения максимальной скорости",
    "en": "End of maximum speed limit",
    "uk": "Кінець обмеження максимальної швидкості",
    "fr": "Fin de limitation de vitesse maximale",
    "tr": "Azami hız sınırı sonu",
  },
  "Überholverbot für Kraftfahrzeuge aller Art": {
    "ru": "Обгон запрещён для всех механических ТС",
    "en": "No overtaking for all motor vehicles",
    "uk": "Обгін заборонено для всіх механічних ТЗ",
    "fr": "Dépassement interdit pour tous véhicules à moteur",
    "tr": "Tüm motorlu araçlar için sollama yasağı",
  },
  "Überholverbot für Kraftfahrzeuge über 3,5 t": {
    "ru": "Обгон запрещён для ТС массой свыше 3,5 т",
    "en": "No overtaking for vehicles over 3.5 t",
    "uk": "Обгін заборонено для ТЗ масою понад 3,5 т",
    "fr": "Dépassement interdit pour véhicules de plus de 3,5 t",
    "tr": "3,5 t üzeri araçlar için sollama yasağı",
  },
  "Ende des Überholverbotes für Kraftfahrzeuge aller Art": {
    "ru": "Конец запрета обгона для всех механических ТС",
    "en": "End of no-overtaking restriction (all motor vehicles)",
    "uk": "Кінець заборони обгону для всіх механічних ТЗ",
    "fr": "Fin d'interdiction de dépasser (tous véhicules à moteur)",
    "tr": "Tüm motorlu araçlar için sollama yasağı sonu",
  },
  "Ende des Überholverbotes für Kraftfahrzeuge über 3,5 t": {
    "ru": "Конец запрета обгона для ТС массой свыше 3,5 т",
    "en": "End of no-overtaking restriction (vehicles over 3.5 t)",
    "uk": "Кінець заборони обгону для ТЗ масою понад 3,5 т",
    "fr": "Fin d'interdiction de dépasser (plus de 3,5 t)",
    "tr": "3,5 t üzeri araçlar için sollama yasağı sonu",
  },
  "Ende sämtlicher streckenbezogener Geschwindigkeitsbeschränkungen und Überholverbote": {
    "ru": "Конец всех участковых ограничений скорости и запретов обгона",
    "en": "End of all route-specific speed limits and overtaking bans",
    "uk": "Кінець усіх ділянкових обмежень швидкості та заборон обгону",
    "fr": "Fin de toutes limitations de vitesse et interdictions de dépasser sur le tronçon",
    "tr": "Tüm kesim hız sınırları ve sollama yasakları sonu",
  },
  "Absolutes Haltverbot": {
    "ru": "Остановка и стоянка запрещены",
    "en": "No stopping or parking",
    "uk": "Зупинка та стоянка заборонені",
    "fr": "Arrêt et stationnement interdits",
    "tr": "Duraklama ve park yasak",
  },
  "Eingeschränktes Haltverbot": {
    "ru": "Стоянка запрещена",
    "en": "No parking",
    "uk": "Стоянка заборонена",
    "fr": "Stationnement interdit",
    "tr": "Park yasak",
  },
  "Verbot für Mofas": {
    "ru": "Движение мопедов запрещено",
    "en": "No mopeds",
    "uk": "Рух мопедів заборонено",
    "fr": "Interdiction aux cyclomoteurs",
    "tr": "Moped yasağı",
  },
  "Verbot für Viehtrieb": {
    "ru": "Прогон скота запрещён",
    "en": "No cattle drive",
    "uk": "Перегін худоби заборонено",
    "fr": "Interdiction de transhumance",
    "tr": "Hayvan sürüsü yasağı",
  },
  "Verbot für Personenkraftwagen mit Anhänger": {
    "ru": "Движение легковых автомобилей с прицепом запрещено",
    "en": "No passenger cars with trailer",
    "uk": "Рух легкових автомобілів з причепом заборонено",
    "fr": "Interdiction aux voitures avec remorque",
    "tr": "Römorklu binek araç yasağı",
  },
  "Verbot für Lastkraftwagen mit Anhänger": {
    "ru": "Движение грузовиков с прицепом запрещено",
    "en": "No lorries with trailer",
    "uk": "Рух вантажівок з причепом заборонено",
    "fr": "Interdiction aux camions avec remorque",
    "tr": "Römorklu kamyon yasağı",
  },
  "Verbot für Kraftfahrzeuge und Züge, die nicht schneller als 25 km/h fahren können oder dürfen": {
    "ru": "Движение ТС, не способных или не имеющих права двигаться быстрее 25 км/ч, запрещено",
    "en": "No vehicles unable or not permitted to exceed 25 km/h",
    "uk": "Рух ТЗ, що не можуть або не мають права рухатися швидше 25 км/год, заборонено",
    "fr": "Interdiction aux véhicules ne pouvant ou n'ayant pas le droit de dépasser 25 km/h",
    "tr": "25 km/s hızı aşamayan veya aşmasına izin verilmeyen araç yasağı",
  },
  "Verbot für Elektrokleinstfahrzeuge im Sinne der Elektrokleinstfahrzeuge-Verordnung (eKFV)": {
    "ru": "Движение электромикромобилей (eKFV) запрещено",
    "en": "No light electric vehicles (eKFV)",
    "uk": "Рух електромікромобілів (eKFV) заборонено",
    "fr": "Interdiction aux véhicules électriques légers (eKFV)",
    "tr": "Hafif elektrikli araç (eKFV) yasağı",
  },
  "Verbot für Fahrzeuge mit wassergefährdender Ladung": {
    "ru": "Движение ТС с опасной для воды грузом запрещено",
    "en": "No vehicles carrying water-polluting cargo",
    "uk": "Рух ТЗ з вантажем, небезпечним для води, заборонено",
    "fr": "Interdiction aux véhicules transportant des marchandises dangereuses pour l'eau",
    "tr": "Suyu kirletici yük taşıyan araç yasağı",
  },
  "Verbot des Unterschreitens des angegebenen Mindestabstandes": {
    "ru": "Запрещено сокращать указанный минимальный интервал",
    "en": "Minimum distance must not be undershot",
    "uk": "Заборонено зменшувати зазначений мінімальний інтервал",
    "fr": "Distance minimale indiquée à ne pas réduire",
    "tr": "Belirtilen asgari mesafenin altına inilemez",
  },
  "Verbot des Überholens von einspurigen Fahrzeugen für mehrspurige Kraftfahrzeuge und Krafträder mit Beiwagen Wer ein mehrspuriges Kraftfahrzeug führt, darf ein- und mehrspurige Fahrzeuge nicht überholen.": {
    "ru": "Запрет обгона однорядных ТС для многорядных ТС и мотоциклов с коляской",
    "en": "No overtaking single-track vehicles (multi-track vehicles and motorcycles with sidecar)",
    "uk": "Заборона обгону однорядних ТЗ для багаторядних ТЗ і мотоциклів з коляскою",
    "fr": "Interdiction de dépasser les véhicules à une file (véhicules multivoies et motos avec side-car)",
    "tr": "Tek şeritli araçları sollama yasağı (çok şeritli araçlar ve sepetli motosikletler)",
  },
  # --- mandatory ---
  "Vorgeschriebene Fahrtrichtung – rechts": {
    "ru": "Обязательное направление — направо",
    "en": "Mandatory direction — right",
    "uk": "Обов'язковий напрямок — праворуч",
    "fr": "Direction obligatoire — à droite",
    "tr": "Zorunlu yön — sağa",
  },
  "Vorgeschriebene Fahrtrichtung – links": {
    "ru": "Обязательное направление — налево",
    "en": "Mandatory direction — left",
    "uk": "Обов'язковий напрямок — ліворуч",
    "fr": "Direction obligatoire — à gauche",
    "tr": "Zorunlu yön — sola",
  },
  "Vorgeschriebene Fahrtrichtung – geradeaus": {
    "ru": "Обязательное направление — прямо",
    "en": "Mandatory direction — straight ahead",
    "uk": "Обов'язковий напрямок — прямо",
    "fr": "Direction obligatoire — tout droit",
    "tr": "Zorunlu yön — düz",
  },
  "Vorgeschriebene Fahrtrichtung — hier rechts": {
    "ru": "Обязательное направление — здесь направо",
    "en": "Mandatory direction — turn right here",
    "uk": "Обов'язковий напрямок — тут праворуч",
    "fr": "Direction obligatoire — ici à droite",
    "tr": "Zorunlu yön — burada sağa",
  },
  "Vorgeschriebene Fahrtrichtung – hier links": {
    "ru": "Обязательное направление — здесь налево",
    "en": "Mandatory direction — turn left here",
    "uk": "Обов'язковий напрямок — тут ліворуч",
    "fr": "Direction obligatoire — ici à gauche",
    "tr": "Zorunlu yön — burada sola",
  },
  "Vorgeschriebene Fahrtrichtung – geradeaus oder rechts": {
    "ru": "Обязательное направление — прямо или направо",
    "en": "Mandatory direction — straight or right",
    "uk": "Обов'язковий напрямок — прямо або праворуч",
    "fr": "Direction obligatoire — tout droit ou à droite",
    "tr": "Zorunlu yön — düz veya sağa",
  },
  "Vorgeschriebene Fahrtrichtung – geradeaus oder links": {
    "ru": "Обязательное направление — прямо или налево",
    "en": "Mandatory direction — straight or left",
    "uk": "Обов'язковий напрямок — прямо або ліворуч",
    "fr": "Direction obligatoire — tout droit ou à gauche",
    "tr": "Zorunlu yön — düz veya sola",
  },
  "Kreisverkehr": {
    "ru": "Кольцевой разъезд",
    "en": "Roundabout",
    "uk": "Кільцевий перехрестя",
    "fr": "Carrefour à sens giratoire",
    "tr": "Dönel kavşak",
  },
  "Einbahnstraße, linksweisend": {
    "ru": "Улица с односторонним движением (налево)",
    "en": "One-way street (to the left)",
    "uk": "Вулиця з одностороннім рухом (ліворуч)",
    "fr": "Rue à sens unique (vers la gauche)",
    "tr": "Tek yön (sola)",
  },
  "Einbahnstraße, rechtsweisend": {
    "ru": "Улица с односторонним движением (направо)",
    "en": "One-way street (to the right)",
    "uk": "Вулиця з одностороннім рухом (праворуч)",
    "fr": "Rue à sens unique (vers la droite)",
    "tr": "Tek yön (sağa)",
  },
  "Vorgeschriebene Vorbeifahrt – rechts vorbei": {
    "ru": "Объезд препятствия — справа",
    "en": "Pass on the right",
    "uk": "Об'їзд перешкоди — праворуч",
    "fr": "Contournement obligatoire — par la droite",
    "tr": "Zorunlu geçiş — sağdan",
  },
  "Vorgeschriebene Vorbeifahrt – links vorbei": {
    "ru": "Объезд препятствия — слева",
    "en": "Pass on the left",
    "uk": "Об'їзд перешкоди — ліворуч",
    "fr": "Contournement obligatoire — par la gauche",
    "tr": "Zorunlu geçiş — soldan",
  },
  "Haltestelle": {
    "ru": "Остановка общественного транспорта",
    "en": "Bus or tram stop",
    "uk": "Зупинка громадського транспорту",
    "fr": "Arrêt de transport en commun",
    "tr": "Toplu taşıma durağı",
  },
  "Schulbushaltestelle (mit Zusatzzeichen 1042-36)": {
    "ru": "Остановка школьного автобуса",
    "en": "School bus stop",
    "uk": "Зупинка шкільного автобуса",
    "fr": "Arrêt de bus scolaire",
    "tr": "Okul servisi durağı",
  },
  "Radweg": {
    "ru": "Велосипедная дорожка",
    "en": "Cycle path",
    "uk": "Велосипедна доріжка",
    "fr": "Piste cyclable",
    "tr": "Bisiklet yolu",
  },
  "Reitweg": {
    "ru": "Конная дорожка",
    "en": "Bridle path",
    "uk": "Кінна доріжка",
    "fr": "Chemin équestre",
    "tr": "At yolu",
  },
  "Gehweg": {
    "ru": "Пешеходная дорожка",
    "en": "Footpath",
    "uk": "Пішохідна доріжка",
    "fr": "Chemin piéton",
    "tr": "Yaya yolu",
  },
  "Schneeketten vorgeschrieben": {
    "ru": "Обязательны цепи противоскольжения",
    "en": "Snow chains required",
    "uk": "Обов'язкові ланцюги протиковзання",
    "fr": "Chaînes à neige obligatoires",
    "tr": "Kar zinciri zorunlu",
  },
  "Vorgeschriebene Mindestgeschwindigkeit": {
    "ru": "Минимальная разрешённая скорость",
    "en": "Minimum speed required",
    "uk": "Мінімальна дозволена швидкість",
    "fr": "Vitesse minimale obligatoire",
    "tr": "Asgari hız zorunlu",
  },
  "Ende der vorgeschriebenen Mindestgeschwindigkeit": {
    "ru": "Конец минимальной разрешённой скорости",
    "en": "End of minimum speed requirement",
    "uk": "Кінець мінімальної дозволеної швидкості",
    "fr": "Fin de vitesse minimale obligatoire",
    "tr": "Asgari hız zorunluluğu sonu",
  },
  # --- information (common) ---
  "Autobahn": {
    "ru": "Автомагистраль",
    "en": "Motorway",
    "uk": "Автомагістраль",
    "fr": "Autoroute",
    "tr": "Otoyol",
  },
  "Autobahngasthaus": {
    "ru": "Мотель на автомагистрали",
    "en": "Motorway service inn",
    "uk": "Мотель на автомагістралі",
    "fr": "Auberge d'autoroute",
    "tr": "Otoyol hanı",
  },
  "Autobahnkapelle": {
    "ru": "Часовня на автомагистрали",
    "en": "Motorway chapel",
    "uk": "Каплиця на автомагістралі",
    "fr": "Chapelle d'autoroute",
    "tr": "Otoyol şapeli",
  },
  "Beginn einer Fußgängerzone": {
    "ru": "Начало пешеходной зоны",
    "en": "Start of pedestrian zone",
    "uk": "Початок пішохідної зони",
    "fr": "Début de zone piétonne",
    "tr": "Yaya bölgesi başlangıcı",
  },
  "Beginn einer Fahrradzone": {
    "ru": "Начало велосипедной зоны",
    "en": "Start of cycle zone",
    "uk": "Початок велосипедної зони",
    "fr": "Début de zone cyclable",
    "tr": "Bisiklet bölgesi başlangıcı",
  },
  "Beginn einer Tempo 30-Zone": {
    "ru": "Начало зоны ограничения скорости 30 км/ч",
    "en": "Start of 30 km/h zone",
    "uk": "Початок зони обмеження швидкості 30 км/год",
    "fr": "Début de zone 30 km/h",
    "tr": "30 km/s bölgesi başlangıcı",
  },
  "Beginn eines verkehrsberuhigten Bereichs": {
    "ru": "Начало зоны с ограничением движения (verkehrsberuhigter Bereich)",
    "en": "Start of traffic-calmed area",
    "uk": "Початок зони з обмеженням руху",
    "fr": "Début de zone apaisée",
    "tr": "Trafik sakinleştirilmiş bölge başlangıcı",
  },
  "Ende der Vorfahrtstraße": {
    "ru": "Конец дороги с преимущественным правом проезда",
    "en": "End of priority road",
    "uk": "Кінець дороги з переважним правом проїзду",
    "fr": "Fin de route prioritaire",
    "tr": "Ana yol sonu",
  },
}

# German fragments → per-language (longest match first when applying)
DE_TERM: dict[str, dict[str, str]] = {
  "Überleitungstafel": {
    "ru": "Табличка перенаправления движения",
    "en": "Lane transition plate",
    "uk": "Табличка перенаправлення руху",
    "fr": "Panneau de redirection",
    "tr": "Şerit yönlendirme levhası",
  },
  "Aufleitungstafel": {
    "ru": "Табличка направления движения",
    "en": "Lane guidance plate",
    "uk": "Табличка напрямку руху",
    "fr": "Panneau de guidage",
    "tr": "Şerit yönlendirme levhası",
  },
  "Aufweitungstafel": {
    "ru": "Табличка расширения полос",
    "en": "Lane widening plate",
    "uk": "Табличка розширення смуг",
    "fr": "Panneau d'élargissement",
    "tr": "Şerit genişletme levhası",
  },
  "Ankündigungstafel": {
    "ru": "Предварительная табличка",
    "en": "Advance direction plate",
    "uk": "Попередня табличка",
    "fr": "Panneau d'annonce",
    "tr": "Ön bilgi levhası",
  },
  "Ankündigungsbake": {
    "ru": "Предупредительный столбик",
    "en": "Advance warning post",
    "uk": "Попереджувальний стовпчик",
    "fr": "Balise d'annonce",
    "tr": "Ön uyarı direği",
  },
  "ohne Gegenverkehr": {
    "ru": "без встречного движения",
    "en": "without oncoming traffic",
    "uk": "без зустрічного руху",
    "fr": "sans circulation en sens inverse",
    "tr": "karşı yönden trafik olmadan",
  },
  "mit Gegenverkehr": {
    "ru": "со встречным движением",
    "en": "with oncoming traffic",
    "uk": "зі зустрічним рухом",
    "fr": "avec circulation en sens inverse",
    "tr": "karşı yönden trafikle",
  },
  "einstreifig nach links": {
    "ru": "одна полоса — поворот налево",
    "en": "single lane — turn left",
    "uk": "одна смуга — поворот ліворуч",
    "fr": "une voie — à gauche",
    "tr": "tek şerit — sola",
  },
  "einstreifig nach rechts": {
    "ru": "одна полоса — поворот направо",
    "en": "single lane — turn right",
    "uk": "одна смуга — поворот праворуч",
    "fr": "une voie — à droite",
    "tr": "tek şerit — sağa",
  },
  "zweistreifig nach links": {
    "ru": "две полосы — поворот налево",
    "en": "two lanes — turn left",
    "uk": "дві смуги — поворот ліворуч",
    "fr": "deux voies — à gauche",
    "tr": "iki şerit — sola",
  },
  "zweistreifig nach rechts": {
    "ru": "две полосы — поворот направо",
    "en": "two lanes — turn right",
    "uk": "дві смуги — поворот праворуч",
    "fr": "deux voies — à droite",
    "tr": "iki şerit — sağa",
  },
  "dreistreifig nach links": {
    "ru": "три полосы — поворот налево",
    "en": "three lanes — turn left",
    "uk": "три смуги — поворот ліворуч",
    "fr": "trois voies — à gauche",
    "tr": "üç şerit — sola",
  },
  "dreistreifig nach rechts": {
    "ru": "три полосы — поворот направо",
    "en": "three lanes — turn right",
    "uk": "три смуги — поворот праворуч",
    "fr": "trois voies — à droite",
    "tr": "üç şerit — sağa",
  },
  "Fahrstreifen": {
    "ru": "полоса движения",
    "en": "traffic lane",
    "uk": "смуга руху",
    "fr": "voie de circulation",
    "tr": "şerit",
  },
  "Kreisverkehr": {
    "ru": "кольцевой разъезд",
    "en": "roundabout",
    "uk": "кільцевий перехрестя",
    "fr": "carrefour giratoire",
    "tr": "dönel kavşak",
  },
  "Umleitung": {
    "ru": "объезд",
    "en": "detour",
    "uk": "об'їзд",
    "fr": "déviation",
    "tr": "yönlendirme",
  },
  "Bedarfsumleitung": {
    "ru": "объезд по необходимости",
    "en": "temporary detour",
    "uk": "об'їзд за потреби",
    "fr": "déviation temporaire",
    "tr": "ihtiyari yönlendirme",
  },
  "Vorfahrtstraße": {
    "ru": "дорога с преимущественным правом проезда",
    "en": "priority road",
    "uk": "дорога з переважним правом проїзду",
    "fr": "route prioritaire",
    "tr": "ana yol",
  },
  "Vorfahrt gewähren": {
    "ru": "предоставление преимущества в движении",
    "en": "give way",
    "uk": "надання переваги в русі",
    "fr": "céder le passage",
    "tr": "yol verme",
  },
  "Haltverbot": {
    "ru": "запрет остановки и стоянки",
    "en": "no stopping",
    "uk": "заборона зупинки та стоянки",
    "fr": "arrêt interdit",
    "tr": "duraklama yasağı",
  },
  "Parkplatz": {
    "ru": "парковка",
    "en": "parking",
    "uk": "парковка",
    "fr": "stationnement",
    "tr": "park alanı",
  },
  "Fußgängerzone": {
    "ru": "пешеходная зона",
    "en": "pedestrian zone",
    "uk": "пішохідна зона",
    "fr": "zone piétonne",
    "tr": "yaya bölgesi",
  },
  "Fahrradzone": {
    "ru": "велосипедная зона",
    "en": "cycle zone",
    "uk": "велосипедна зона",
    "fr": "zone cyclable",
    "tr": "bisiklet bölgesi",
  },
  "Anfang": {
    "ru": "начало",
    "en": "start",
    "uk": "початок",
    "fr": "début",
    "tr": "başlangıç",
  },
  "Ende": {
    "ru": "конец",
    "en": "end",
    "uk": "кінець",
    "fr": "fin",
    "tr": "son",
  },
  "Mitte": {
    "ru": "середина",
    "en": "middle",
    "uk": "середина",
    "fr": "milieu",
    "tr": "orta",
  },
  "Beginn": {
    "ru": "начало",
    "en": "start",
    "uk": "початок",
    "fr": "début",
    "tr": "başlangıç",
  },
  "Aufstellung rechts": {
    "ru": "предварительный указатель (справа)",
    "en": "advance warning plate (right)",
    "uk": "попередній вказівник (праворуч)",
    "fr": "panneau d'annonce (à droite)",
    "tr": "ön uyarı levhası (sağda)",
  },
  "Aufstellung links": {
    "ru": "предварительный указатель (слева)",
    "en": "advance warning plate (left)",
    "uk": "попередній вказівник (ліворуч)",
    "fr": "panneau d'annonce (à gauche)",
    "tr": "ön uyarı levhası (solda)",
  },
  "Flugbetrieb": {
    "ru": "полёты вблизи аэродрома",
    "en": "low-flying aircraft",
    "uk": "польоти біля аеродрому",
    "fr": "vol à basse altitude",
    "tr": "alçak uçuş",
  },
  "Fußgängerüberweg": {
    "ru": "пешеходный переход",
    "en": "pedestrian crossing",
    "uk": "пішохідний перехід",
    "fr": "passage piéton",
    "tr": "yaya geçidi",
  },
  "Viehtrieb": {
    "ru": "прогон скота",
    "en": "cattle drive",
    "uk": "перегін худоби",
    "fr": "transhumance",
    "tr": "hayvan sürüsü",
  },
  "Reiter": {
    "ru": "всадники",
    "en": "horse riders",
    "uk": "вершники",
    "fr": "cavaliers",
    "tr": "atlılar",
  },
  "Amphibienwanderung": {
    "ru": "миграция земноводных",
    "en": "amphibian migration",
    "uk": "міграція земноводних",
    "fr": "migration d'amphibiens",
    "tr": "amfibi göçü",
  },
  "Steinschlag": {
    "ru": "камнепад",
    "en": "falling rocks",
    "uk": "каменепад",
    "fr": "chutes de pierres",
    "tr": "taş düşmesi",
  },
  "Fußgänger": {
    "ru": "пешеходы",
    "en": "pedestrians",
    "uk": "пішоходи",
    "fr": "piétons",
    "tr": "yayalar",
  },
  "Kinder": {
    "ru": "дети",
    "en": "children",
    "uk": "діти",
    "fr": "enfants",
    "tr": "çocuklar",
  },
  "Radverkehr": {
    "ru": "велосипедисты",
    "en": "cyclists",
    "uk": "велосипедисти",
    "fr": "cyclistes",
    "tr": "bisikletliler",
  },
  "Wildwechsel": {
    "ru": "выход диких животных",
    "en": "wild animals crossing",
    "uk": "вихід диких тварин",
    "fr": "passage d'animaux sauvages",
    "tr": "vahşi hayvan geçişi",
  },
}

AUFSTELLUNG_RE = re.compile(r" – Aufstellung (rechts|links)$")
AUFSTELLUNG_BASE = {
  "Flugbetrieb": EXACT_TITLE.get("Flugbetrieb", DE_TERM["Flugbetrieb"]),
  "Fußgängerüberweg": DE_TERM["Fußgängerüberweg"],
  "Viehtrieb": DE_TERM["Viehtrieb"],
  "Reiter": DE_TERM["Reiter"],
  "Amphibienwanderung": DE_TERM["Amphibienwanderung"],
  "Steinschlag": DE_TERM["Steinschlag"],
  "Fußgänger": DE_TERM["Fußgänger"],
  "Kinder": DE_TERM["Kinder"],
  "Radverkehr": DE_TERM["Radverkehr"],
  "Wildwechsel": DE_TERM["Wildwechsel"],
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
  "Absolutes Haltverbot": EXACT_TITLE["Absolutes Haltverbot"],
  "Eingeschränktes Haltverbot": EXACT_TITLE["Eingeschränktes Haltverbot"],
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

HALTVERBOT_ZONE_RE = re.compile(
  r"^(Absolutes|Eingeschränktes) Haltverbot \((Anfang|Ende|Mitte)\), Aufstellung (rechts|links)$"
)

TITLE_POST_FIXES: dict[str, list[tuple[str, str]]] = {
  "ru": [
    (r"\bперекресток\b", "перекрёсток"),
    (r"\bУступите дорогу\b", "Предоставление преимущества в движении"),
    (r"\bуступите дорогу\b", "предоставление преимущества в движении"),
    (r"\bГлавная дорога\b", "Дорога с преимущественным правом проезда"),
    (r"\bглавной дороги\b", "дороги с преимущественным правом проезда"),
    (r"\bшоссе\b", "автомагистраль"),
    (r"\bТабло перехода\b", "Табличка перенаправления движения"),
    (r"\bЗнак перехода\b", "Табличка перенаправления движения"),
    (r"\bоставлено здесь\b", "здесь налево"),
    (r"\bоставленное на круг\b", "на кольцевом разъезде налево"),
    (r"\bоставлен\b", "налево"),
    (r"\bполосы отвода\b", "дороги с преимущественным правом проезда"),
    (r"\bПроизводство пол[её]тов\b", "Полёты вблизи аэродрома"),
    (r" — ", " — "),
  ],
  "en": [
    (r"\bHighway\b", "Motorway"),
    (r"\bTransition board\b", "Lane transition plate"),
    (r"\bleft here\b(?!\s+direction)", "turn left here"),
    (r"\bleft on the circle\b", "left at the roundabout"),
    (r"\bGive way\b", "Give way"),
  ],
  "uk": [
    (r"\bзалишено\b", "ліворуч"),
    (r"\bУступи дорогу\b", "Надання переваги в русі"),
    (r"\bковзання або ковзання\b", "заносу або ковзання"),
    (r"\bперетин або перетин\b", "перехрестя або приєднання"),
  ],
  "fr": [
    (r"\bgauche ici\b", "ici à gauche"),
  ],
  "tr": [
    (r"\bkavşak veya kavşak\b", "kavşak veya birleşme"),
    (r"\bKayma veya kayma\b", "kayma veya savrulma"),
    (r"\bemirler\b", "zorunluluk işaretleri"),
  ],
}

NOTE_POST_FIXES: dict[str, list[tuple[str, str]]] = {
  "ru": [
    (r"будьте особенно внимательны", "соблюдайте повышенную осторожность"),
    (r"будьте предельно внимательны", "соблюдайте предельную осторожность"),
    (r"следите за поперечным движением", "контролируйте поперечное движение"),
    (r"уступить дорогу", "предоставить преимущество в движении"),
    (r"Уступить дорогу", "Предоставить преимущество в движении"),
    (r"уступите дорогу", "предоставьте преимущество в движении"),
    (r"Уступите дорогу", "Предоставьте преимущество в движении"),
  ],
  "en": [
    (r"drive with extra care", "exercise increased caution"),
    (r"stay especially alert", "remain especially vigilant"),
    (r"Adjust your speed", "Reduce speed"),
  ],
  "uk": [
    (r"будьте особливо обережні", "дотримуйтесь підвищеної обережності"),
    (r"будьте максимально уважні", "дотримуйтесь максимальної уважності"),
    (r"стежте за поперечним рухом", "контролюйте поперечний рух"),
    (r"ковзання або ковзання", "заносу або ковзання"),
    (r"Дайте дорогу", "надайте перевагу в русі"),
    (r"дайте дорогу", "надайте перевагу в русі"),
  ],
  "fr": [],
  "tr": [
    (r"kavşak veya kavşak", "kavşak veya birleşme"),
    (r"özellikle dikkatli sürün", "artırılmış dikkatle sürün"),
    (r"Hızınızı ayarlayın", "Hızınızı azaltın"),
  ],
}

_GERMAN_HINT = re.compile(r"[äöüßÄÖÜ]|(?:\b(?:mit|ohne|der|die|das|und|oder|von|für|im|auf)\b)", re.I)
_SORTED_TERMS = sorted(DE_TERM.keys(), key=len, reverse=True)


def _capitalize_first(text: str) -> str:
  if not text:
    return text
  return text[0].upper() + text[1:]


def _apply_post_fixes(text: str, lang: str, fixes: dict[str, list[tuple[str, str]]]) -> str:
  for pattern, repl in fixes.get(lang, []):
    text = re.sub(pattern, repl, text, flags=re.IGNORECASE)
  return text


def _translate_aufstellung(de: str) -> dict[str, str] | None:
  m = AUFSTELLUNG_RE.search(de)
  if not m:
    m2 = re.search(r", Aufstellung (rechts|links)$", de)
    if not m2:
      m3 = HALTVERBOT_ZONE_RE.match(de)
      if m3:
        kind, part, side = m3.group(1), m3.group(2), m3.group(3)
        base_key = f"{kind} Haltverbot"
        base = EXACT_TITLE.get(base_key, {})
        part_map = {
          "ru": {"Anfang": "начало", "Ende": "конец", "Mitte": "середина"},
          "en": {"Anfang": "start", "Ende": "end", "Mitte": "middle"},
          "uk": {"Anfang": "початок", "Ende": "кінець", "Mitte": "середина"},
          "fr": {"Anfang": "début", "Ende": "fin", "Mitte": "milieu"},
          "tr": {"Anfang": "başlangıç", "Ende": "son", "Mitte": "orta"},
        }
        out: dict[str, str] = {}
        for lang in LANGS:
          suffix = AUFSTELLUNG_SUFFIX.get((lang, side), "")
          part_tr = part_map[lang][part]
          out[lang] = f"{base[lang]} ({part_tr}){suffix}"
        return out
      return None
    side = m2.group(1)
    base_de = de[: m2.start()]
  else:
    side = m.group(1)
    base_de = de[: m.start()]

  base_map = AUFSTELLUNG_BASE.get(base_de)
  if not base_map:
    return None
  out: dict[str, str] = {}
  for lang in LANGS:
    suffix = AUFSTELLUNG_SUFFIX.get((lang, side), "")
    base_tr = base_map.get(lang, "")
    if base_tr and suffix:
      out[lang] = base_tr + suffix
  return out if out else None


def _translate_from_terms(de: str, lang: str) -> str:
  text = de
  for term in _SORTED_TERMS:
    if term in text:
      text = text.replace(term, DE_TERM[term][lang])
  text = text.replace(" – ", " — ").replace(" - ", " — ")
  return _capitalize_first(text.strip())


def _looks_german(text: str) -> bool:
  return bool(_GERMAN_HINT.search(text))


def build_title_translations(sign: dict) -> dict[str, str]:
  de = sign["de"]
  if de in EXACT_TITLE:
    return dict(EXACT_TITLE[de])

  auf = _translate_aufstellung(de)
  if auf:
    return auf

  result: dict[str, str] = {}
  for lang in LANGS:
    from_terms = _translate_from_terms(de, lang)
    if not _looks_german(from_terms) and from_terms != de:
      result[lang] = from_terms
    else:
      current = sign.get(lang, de)
      result[lang] = _capitalize_first(_apply_post_fixes(current, lang, TITLE_POST_FIXES))
  return result


def officialize_notes(notes: dict[str, str]) -> dict[str, str]:
  out = dict(notes)
  for lang in LANGS:
    if lang in out:
      out[lang] = _apply_post_fixes(out[lang], lang, NOTE_POST_FIXES)
  return out
