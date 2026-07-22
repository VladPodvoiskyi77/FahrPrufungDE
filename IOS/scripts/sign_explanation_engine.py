#!/usr/bin/env python3
"""Rule-based multilingual sign explanations for FahrPrüfung DE.

Each explanation tells the driver what to do or expect — never repeats the sign title.
"""

from __future__ import annotations

import re
from typing import Callable

LANGS = ("de", "ru", "en", "uk", "fr", "tr")


def _n(de: str, ru: str, en: str, uk: str, fr: str, tr: str) -> dict[str, str]:
    return {"de": de, "ru": ru, "en": en, "uk": uk, "fr": fr, "tr": tr}


# ---------------------------------------------------------------------------
# Reusable multilingual fragments
# ---------------------------------------------------------------------------

SLOW_DOWN = _n(
    "Geschwindigkeit anpassen und besonders vorsichtig fahren.",
    "Снизьте скорость и соблюдайте повышенную осторожность.",
    "Reduce speed and exercise increased caution.",
    "Зменшіть швидкість і дотримуйтесь підвищеної обережності.",
    "Réduisez votre vitesse et faites preuve d'une vigilance accrue.",
    "Hızınızı azaltın ve artırılmış dikkatle sürün.",
)

VORBAU_RIGHT = _n(
    "Vorankündigungszeichen: Das Hauptzeichen steht voraussichtlich rechts der Fahrbahn.",
    "Предварительный указатель: основной знак будет справа на обочине.",
    "Advance warning plate: the main sign will be on the right side of the road ahead.",
    "Попередній вказівник: основний знак буде праворуч на узбіччі.",
    "Panneau d'annonce : le panneau principal sera à droite de la chaussée.",
    "Ön uyarı levhası: asıl işaret yolun sağ tarafında olacaktır.",
)

VORBAU_LEFT = _n(
    "Vorankündigungszeichen: Das Hauptzeichen steht voraussichtlich links der Fahrbahn.",
    "Предварительный указатель: основной знак будет слева на обочине.",
    "Advance warning plate: the main sign will be on the left side of the road ahead.",
    "Попередній вказівник: основний знак буде ліворуч на узбіччі.",
    "Panneau d'annonce : le panneau principal sera à gauche de la chaussée.",
    "Ön uyarı levhası: asıl işaret yolun sol tarafında olacaktır.",
)

DISTANCE_PLATE = _n(
    "Zusatzzeichen mit Entfernungsangabe — das Hauptzeichen folgt in der angegebenen Entfernung.",
    "Дополнительная табличка с расстоянием — основной знак будет через указанное расстояние.",
    "Supplementary plate with distance — the main sign follows at the distance shown.",
    "Додаткова табличка з відстанню — основний знак буде через зазначену відстань.",
    "Plaque complémentaire avec distance — le panneau principal suit à la distance indiquée.",
    "Mesafe göstergeli ek levha — asıl işaret gösterilen mesafede gelecektir.",
)

GEGENVERKEHR_YES = _n(
    "Gegenverkehr ist vorhanden — Fahrstreifen für beide Richtungen.",
    "Есть встречное движение — полосы для обоих направлений.",
    "Oncoming traffic present — lanes for both directions.",
    "Є зустрічний рух — смуги для обох напрямків.",
    "Circulation en sens inverse — voies pour les deux directions.",
    "Karşı yönden trafik var — her iki yön için şeritler.",
)

GEGENVERKEHR_NO = _n(
    "Kein Gegenverkehr — nur Fahrstreifen in Ihrer Fahrtrichtung.",
    "Встречного движения нет — только полосы в вашем направлении.",
    "No oncoming traffic — lanes in your direction only.",
    "Зустрічного руху немає — лише смуги у вашому напрямку.",
    "Pas de circulation en sens inverse — voies dans votre sens uniquement.",
    "Karşı yönden trafik yok — yalnızca gidiş yönünüzdeki şeritler.",
)

# Warning hazard advice (driver action, not title)
HAZARD_ADVICE: dict[str, dict[str, str]] = {
    "gefahrstelle": _n(
        "Gefahr kann von verschiedenen Seiten kommen — besonders aufmerksam sein.",
        "Опасность может возникнуть неожиданно — соблюдайте предельную осторожность.",
        "Hazard may come from any direction — remain especially vigilant.",
        "Небезпека може виникнути несподівано — дотримуйтесь максимальної уважності.",
        "Le danger peut venir de n'importe où — restez particulièrement vigilant.",
        "Tehlike her yönden gelebilir — azami dikkatle ilerleyin.",
    ),
    "flugbetrieb": _n(
        "Flugbetrieb in der Nähe — tief fliegende Flugzeuge oder Hubschrauber möglich.",
        "Рядом аэродром или вертолётная площадка — возможны низколетящие самолёты или вертолёты.",
        "Flight operations nearby — low-flying aircraft or helicopters possible.",
        "Поблизу аеродром або вертолітний майданчик — можливі низьколітаючі літаки або гелікоптери.",
        "Activité aérienne à proximité — avions ou hélicoptères volant bas possibles.",
        "Yakında uçuş faaliyeti — alçak uçan uçak veya helikopter olabilir.",
    ),
    "fussgaengerueberweg": _n(
        "Fußgängerüberweg voraus — Fußgänger können die Fahrbahn überqueren.",
        "Впереди пешеходный переход — пешеходы могут переходить дорогу.",
        "Pedestrian crossing ahead — pedestrians may cross the road.",
        "Попереду пішохідний перехід — пішоходи можуть переходити дорогу.",
        "Passage piéton à venir — des piétons peuvent traverser.",
        "İleride yaya geçidi — yayalar yolu geçebilir.",
    ),
    "viehtrieb": _n(
        "Viehtrieb möglich — Tiere können die Fahrbahn betreten.",
        "Возможен прогон скота — животные могут выходить на дорогу.",
        "Cattle drive possible — animals may enter the road.",
        "Можливий перегін худоби — тварини можуть виходити на дорогу.",
        "Conduite de bétail possible — des animaux peuvent entrer sur la route.",
        "Hayvan sürüsü olabilir — hayvanlar yola çıkabilir.",
    ),
    "reiter": _n(
        "Reiter auf der Straße möglich — Pferde langsam und mit Abstand überholen.",
        "Возможны всадники на дороге — обгоняйте лошадей медленно, с большим расстоянием.",
        "Horse riders possible — overtake horses slowly with plenty of space.",
        "Можливі вершники на дорозі — обганяйте коней повільно, з великою дистанцією.",
        "Cavaliers possibles — dépassez les chevaux lentement en gardant de la distance.",
        "Atlılar olabilir — atları yavaşça ve geniş mesafeyle geçin.",
    ),
    "amphibienwanderung": _n(
        "Amphibienwanderung — Tiere überqueren die Straße, besonders nachts.",
        "Миграция земноводных — животные переходят дорогу, особенно ночью.",
        "Amphibian migration — animals cross the road, especially at night.",
        "Міграція земноводних — тварини переходять дорогу, особенно вночі.",
        "Migration d'amphibiens — les animaux traversent, surtout la nuit.",
        "Amfibi göçü — hayvanlar yolu geçer, özellikle gece.",
    ),
    "steinschlag": _n(
        "Steinschlaggefahr — Steine können auf die Fahrbahn fallen.",
        "Опасность камнепада — камни могут падать на проезжую часть.",
        "Risk of falling rocks — stones may land on the road.",
        "Небезпека каменепаду — камені можуть падати на проїзну частину.",
        "Risque d'éboulement — des pierres peuvent tomber sur la chaussée.",
        "Taş düşmesi riski — taşlar yola düşebilir.",
    ),
    "schnee_eis": _n(
        "Schnee- oder Eisglätte — vorsichtig bremsen und lenken.",
        "Скользко от снега или льда — тормозите и рулите осторожно.",
        "Snow or ice — brake and steer gently.",
        "Слизько від снігу чи льоду — гальмуйте та керуйте обережно.",
        "Neige ou verglas — freinez et dirigez avec douceur.",
        "Kar veya buz — yavaşça frenleyin ve dikkatli direksiyon kullanın.",
    ),
    "splitt": _n(
        "Lose Schotteroberfläche — erhöhte Rutschgefahr, Geschwindigkeit reduzieren.",
        "Рыхлая гравийная поверхность — повышенный риск заноса, снизьте скорость.",
        "Loose gravel surface — higher skid risk, reduce speed.",
        "Розсипчаста гравійна поверхня — підвищений ризик заносу, зменшіть швидкість.",
        "Surface en gravier — risque de dérapage accru, réduisez la vitesse.",
        "Gevşek çakıl yüzey — kayma riski yüksek, hızı düşürün.",
    ),
    "ufer": _n(
        "Uferstraße — enge Fahrbahn, Absturzgefahr zum Wasser.",
        "Дорога у берега — узкая проезжая часть, риск падения в воду.",
        "Road along water — narrow carriageway, risk of falling into water.",
        "Дорога біля берега — вузька проїзна частина, ризик падіння у воду.",
        "Route en bord d'eau — chaussée étroite, risque de chute dans l'eau.",
        "Su kenarı yol — dar yol, suya düşme riski.",
    ),
    "lichtraumprofil": _n(
        "Unzureichendes Lichtraumprofil — hohe Fahrzeuge können Schäden erleiden.",
        "Недостаточная высота проезда — высокие ТС могут задеть конструкцию.",
        "Insufficient clearance height — tall vehicles may be damaged.",
        "Недостатня висота проїзду — високі ТЗ можуть зачепити конструкцію.",
        "Hauteur insuffisante — les véhicules hauts peuvent être endommagés.",
        "Yetersiz geçiş yüksekliği — yüksek araçlar hasar görebilir.",
    ),
    "bewegliche_bruecke": _n(
        "Bewegliche Brücke — Brücke kann sich öffnen, nur bei freier Fahrt passieren.",
        "Разводной мост — мост может разводиться, проезжайте только когда открыто.",
        "Movable bridge — bridge may open, cross only when clear.",
        "Розвідний міст — міст може розводитися, проїжджайте лише коли відкрито.",
        "Pont mobile — le pont peut s'ouvrir, ne passez que s'il est libre.",
        "Açılır köprü — köprü açılabilir, yalnızca açıkken geçin.",
    ),
    "kreuzung": _n(
        "Kreuzung oder Einmündung voraus — auf Querverkehr achten.",
        "Впереди перекрёсток или примыкание — следите за поперечным движением.",
        "Intersection or junction ahead — watch for cross traffic.",
        "Попереду перехрестя або приєднання — стежте за поперечним рухом.",
        "Croisement ou jonction — surveillez le trafic transversal.",
        "İleride kavşak veya birleşme — çapraz trafiğe dikkat edin.",
    ),
    "kurve_links": _n(
        "Gefährliche Linkskurve voraus — Geschwindigkeit vor der Kurve reduzieren.",
        "Впереди опасный поворот налево — снизьте скорость до входа в поворот.",
        "Dangerous left bend ahead — slow down before the curve.",
        "Попереду небезпечний поворот ліворуч — зменшіть швидкість до входу в поворот.",
        "Virage dangereux à gauche — ralentissez avant le virage.",
        "İleride tehlikeli sol viraj — virajdan önce yavaşlayın.",
    ),
    "kurve_rechts": _n(
        "Gefährliche Rechtskurve voraus — Geschwindigkeit vor der Kurve reduzieren.",
        "Впереди опасный поворот направо — снизьте скорость до входа в поворот.",
        "Dangerous right bend ahead — slow down before the curve.",
        "Попереду небезпечний поворот праворуч — зменшіть швидкість до входу в поворот.",
        "Virage dangereux à droite — ralentissez avant le virage.",
        "İleride tehlikeli sağ viraj — virajdan önce yavaşlayın.",
    ),
    "doppelkurve_links": _n(
        "Doppelkurve, zuerst links — zwei Kurven hintereinander, Geschwindigkeit anpassen.",
        "Двойной поворот, сначала налево — две кривые подряд, снизьте скорость.",
        "Double bend, left first — two curves in succession, adjust speed.",
        "Подвійний поворот, спочатку ліворуч — дві криві поспіль, зменшіть швидкість.",
        "Double virage, d'abord à gauche — deux courbes successives, adaptez la vitesse.",
        "Çift viraj, önce sola — art arda iki viraj, hızı ayarlayın.",
    ),
    "doppelkurve_rechts": _n(
        "Doppelkurve, zuerst rechts — zwei Kurven hintereinander, Geschwindigkeit anpassen.",
        "Двойной поворот, сначала направо — две кривые подряд, снизьте скорость.",
        "Double bend, right first — two curves in succession, adjust speed.",
        "Подвійний поворот, спочатку праворуч — дві криві поспіль, зменшіть швидкість.",
        "Double virage, d'abord à droite — deux courbes successives, adaptez la vitesse.",
        "Çift viraj, önce sağa — art arda iki viraj, hızı ayarlayın.",
    ),
    "unebene_fahrbahn": _n(
        "Unebene Fahrbahn — Schlaglöcher oder Wellen, Geschwindigkeit reduzieren.",
        "Неровное покрытие — выбоины или волны, снизьте скорость.",
        "Uneven road surface — potholes or bumps, reduce speed.",
        "Нерівне покриття — вибоїни чи хвилі, зменшіть швидкість.",
        "Chaussée inégale — nids-de-poule ou bosses, réduisez la vitesse.",
        "Düzensiz yol yüzeyi — çukurlar veya dalgalar, hızı düşürün.",
    ),
    "rutschgefahr": _n(
        "Schleuder- oder Rutschgefahr — besonders bei Nässe oder Schnee vorsichtig fahren.",
        "Опасность заноса — особенно в дождь или снег езжайте осторожно.",
        "Skid risk — drive carefully especially in wet or snowy conditions.",
        "Небезпека заносу — особливо в дощ чи сніг їдьте обережно.",
        "Risque de dérapage — roulez prudemment par temps humide ou neigeux.",
        "Kayma riski — özellikle yağmur veya karlı havada dikkatli sürün.",
    ),
    "seitenwind_rechts": _n(
        "Seitenwind von rechts — Fahrzeug kann nach links abdriften, Lenkrad festhalten.",
        "Боковой ветер справа — автомобиль может сносить влево, крепко держите руль.",
        "Crosswind from the right — vehicle may drift left, hold the wheel firmly.",
        "Бічний вітер праворуч — авто може зносити ліворуч, міцно тримайте кермо.",
        "Vent latéral de droite — le véhicule peut dériver à gauche, tenez le volant.",
        "Sağdan yan rüzgar — araç sola kayabilir, direksiyonu sıkı tutun.",
    ),
    "seitenwind_links": _n(
        "Seitenwind von links — Fahrzeug kann nach rechts abdriften, Lenkrad festhalten.",
        "Боковой ветер слева — автомобиль может сносить вправо, крепко держите руль.",
        "Crosswind from the left — vehicle may drift right, hold the wheel firmly.",
        "Бічний вітер ліворуч — авто може зносити праворуч, міцно тримайте кермо.",
        "Vent latéral de gauche — le véhicule peut dériver à droite, tenez le volant.",
        "Soldan yan rüzgar — araç sağa kayabilir, direksiyonu sıkı tutun.",
    ),
    "verengte_fahrbahn": _n(
        "Fahrbahn verengt sich — Vorfahrt beachten, nicht drängeln.",
        "Дорога сужается — соблюдайте приоритет, не подталкивайте.",
        "Road narrows — observe right of way, do not push.",
        "Дорога звужується — дотримуйтесь пріоритету, не підштовхуйте.",
        "Chaussée rétrécie — respectez la priorité, ne forcez pas le passage.",
        "Yol daralıyor — geçiş önceliğine uyun, zorlamayın.",
    ),
    "verengung_rechts": _n(
        "Fahrbahn verengt sich rechts — links bleibende Fahrzeuge haben Vorfahrt.",
        "Дорога сужается справа — уступите тем, кто продолжает слева.",
        "Road narrows on the right — give way to traffic keeping left.",
        "Дорога звужується праворуч — поступіться тим, хто їде ліворуч.",
        "Rétrécissement à droite — cédez le passage à ceux qui restent à gauche.",
        "Yol sağdan daralıyor — solda kalanlara yol verin.",
    ),
    "verengung_links": _n(
        "Fahrbahn verengt sich links — rechts bleibende Fahrzeuge haben Vorfahrt.",
        "Дорога сужается слева — уступите тем, кто продолжает справа.",
        "Road narrows on the left — give way to traffic keeping right.",
        "Дорога звужується ліворуч — поступіться тим, хто їде праворуч.",
        "Rétrécissement à gauche — cédez le passage à ceux qui restent à droite.",
        "Yol soldan daralıyor — sağda kalanlara yol verin.",
    ),
    "arbeitsstelle": _n(
        "Baustelle voraus — Arbeiter und Baumaschinen möglich, Tempo 30 oft vorgeschrieben.",
        "Впереди дорожные работы — возможны рабочие и техника, часто действует 30 км/ч.",
        "Road works ahead — workers and machinery possible, often 30 km/h limit.",
        "Попереду дорожні роботи — можливі робітники та техніка, часто діє 30 км/год.",
        "Travaux — ouvriers et engins possibles, souvent 30 km/h.",
        "İleride yol çalışması — işçi ve makine olabilir, genelde 30 km/s.",
    ),
    "stau": _n(
        "Staugefahr — Abstand vergrößern, nicht ungeduldig werden.",
        "Опасность пробки — увеличьте дистанцию, не нервничайте.",
        "Risk of traffic jam — increase following distance, stay patient.",
        "Небезпека затору — збільште дистанцію, не нервуйте.",
        "Risque d'embouteillage — augmentez la distance, restez patient.",
        "Trafik sıkışıklığı riski — mesafeyi artırın, sabırlı olun.",
    ),
    "gegenverkehr": _n(
        "Gegenverkehr voraus — auf die richtige Spur achten.",
        "Впереди встречное движение — следите за правильной полосой.",
        "Oncoming traffic ahead — stay in the correct lane.",
        "Попереду зустрічний рух — стежте за правильною смугою.",
        "Circulation en sens inverse — restez sur la bonne voie.",
        "İleride karşı yön trafiği — doğru şeritte kalın.",
    ),
    "lichtzeichen": _n(
        "Ampelanlage voraus — auf Lichtzeichen achten, bei Gelb nicht beschleunigen.",
        "Впереди светофор — следите за сигналами, на жёлтый не ускоряйтесь.",
        "Traffic lights ahead — watch signals, do not speed up on yellow.",
        "Попереду світлофор — стежте за сигналами, на жовтий не прискорюйтесь.",
        "Feux tricolores — surveillez les signaux, n'accélérez pas au jaune.",
        "İleride trafik ışığı — sinyallere dikkat edin, sarıda hızlanmayın.",
    ),
    "fussgaenger": _n(
        "Fußgänger auf oder neben der Straße — besonders in Wohngebieten vorsichtig.",
        "Пешеходы на дороге или у обочины — особенно осторожно в жилых зонах.",
        "Pedestrians on or near the road — extra care in residential areas.",
        "Пішоходи на дорозі чи біля узбіччя — особливо обережно в житлових зонах.",
        "Piétons sur ou près de la route — prudence en zone résidentielle.",
        "Yayalar yolda veya kenarında — özellikle yerleşim yerlerinde dikkatli olun.",
    ),
    "kinder": _n(
        "Kinder auf der Straße möglich — langsam fahren, mit Unberechenbarkeit rechnen.",
        "Возможны дети на дороге — езжайте медленно, дети непредсказуемы.",
        "Children may be on the road — drive slowly, expect unpredictable behaviour.",
        "Можливі діти на дорозі — їдьте повільно, діти непередбачувані.",
        "Enfants possibles — roulez lentement, comportement imprévisible.",
        "Çocuklar yolda olabilir — yavaş sürün, öngörülemez davranış bekleyin.",
    ),
    "radverkehr": _n(
        "Radfahrer voraus oder auf der Straße — ausreichend Abstand beim Überholen.",
        "Впереди велосипедисты — при обгоне оставляйте достаточный боковой интервал.",
        "Cyclists ahead or on the road — leave enough space when overtaking.",
        "Попереду велосипедисти — при обгоні залишайте достатній боковий інтервал.",
        "Cyclistes — laissez assez d'espace en les dépassant.",
        "Bisikletliler — geçerken yeterli yan mesafe bırakın.",
    ),
    "wildwechsel": _n(
        "Wildwechsel — Wildtiere können die Straße überqueren, besonders bei Dämmerung.",
        "Переход диких животных — звери могут выбегать на дорогу, особенно в сумерки.",
        "Wild animals crossing — animals may run onto the road, especially at dusk.",
        "Перехід диких тварин — звірі можуть вибігати на дорогу, особливо в сутінки.",
        "Passage d'animaux sauvages — surtout au crépuscule.",
        "Yabani hayvan geçişi — özellikle alacakaranlıkta hayvanlar yola çıkabilir.",
    ),
    "bahnuebergang": _n(
        "Bahnübergang voraus — Schienenverkehr hat Vorrang, nie auf Schienen warten.",
        "Впереди железнодорожный переезд — поезда имеют приоритет, не стойте на рельсах.",
        "Level crossing ahead — trains have priority, never wait on the tracks.",
        "Попереду залізничний переїзд — поїзди мають пріоритет, не стійте на рейках.",
        "Passage à niveau — les trains ont la priorité, ne restez pas sur les rails.",
        "Demiryolu geçidi — trenlerin önceliği var, raylar üzerinde beklemeyin.",
    ),
    "andreaskreuz": _n(
        "Andreaskreuz — Schienenverkehr hat Vorrang! Anhalten wenn nötig, nie auf Gleisen halten.",
        "Андреасов крест — поезда имеют приоритет! Остановитесь при необходимости, не стойте на путях.",
        "St Andrew's cross — trains have priority! Stop if needed, never wait on tracks.",
        "Андреасів хрест — поїзди мають пріоритет! Зупиніться за потреби, не стійте на коліях.",
        "Croix de Saint-André — les trains ont la priorité ! Arrêtez-vous si nécessaire.",
        "Andrea haçı — trenlerin önceliği var! Gerekirse durun, raylarda beklemeyin.",
    ),
}


def _join(*parts: dict[str, str]) -> dict[str, str]:
    return {lang: " ".join(p[lang] for p in parts if p.get(lang)) for lang in LANGS}


def _extract_speed(code: str, de: str) -> int | None:
    m = re.search(r"(\d+)\s*km/h", de, re.I)
    if m:
        return int(m.group(1))
    suffix = code.split("-")[-1] if "-" in code else ""
    if suffix.isdigit():
        val = int(suffix)
        if val in (5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130):
            return val
    return None


def _side_from_de(de: str) -> str | None:
    dl = de.lower()
    if "aufstellung rechts" in dl or "rechts)" in dl or ", aufstellung rechts" in dl:
        return "right"
    if "aufstellung links" in dl or "links)" in dl or ", aufstellung links" in dl:
        return "left"
    if "verengung rechts" in dl:
        return "right"
    if "verengung links" in dl:
        return "left"
    return None


def _has_gegenverkehr(de: str) -> bool | None:
    dl = de.lower()
    if "mit gegenverkehr" in dl:
        return True
    if "ohne gegenverkehr" in dl:
        return False
    return None


def _hazard_key(de: str) -> str | None:
    dl = de.lower()
    pairs = [
        ("flugbetrieb", "flugbetrieb"),
        ("fußgängerüberweg", "fussgaengerueberweg"),
        ("viehtrieb", "viehtrieb"),
        ("reiter", "reiter"),
        ("amphibienwanderung", "amphibienwanderung"),
        ("steinschlag", "steinschlag"),
        ("schnee- oder eisglätte", "schnee_eis"),
        ("splitt", "splitt"),
        ("ufer", "ufer"),
        ("unzureichendes lichtraumprofil", "lichtraumprofil"),
        ("bewegliche brücke", "bewegliche_bruecke"),
        ("kreuzung oder einmündung", "kreuzung"),
        ("doppelkurve – zunächst links", "doppelkurve_links"),
        ("doppelkurve – zunächst rechts", "doppelkurve_rechts"),
        ("kurve – links", "kurve_links"),
        ("kurve – rechts", "kurve_rechts"),
        ("unebene fahrbahn", "unebene_fahrbahn"),
        ("schleuder- oder rutschgefahr", "rutschgefahr"),
        ("seitenwind von rechts", "seitenwind_rechts"),
        ("seitenwind von links", "seitenwind_links"),
        ("einseitig verengte fahrbahn – verengung rechts", "verengung_rechts"),
        ("einseitig verengte fahrbahn – verengung links", "verengung_links"),
        ("verengte fahrbahn", "verengte_fahrbahn"),
        ("arbeitsstelle", "arbeitsstelle"),
        ("stau", "stau"),
        ("gegenverkehr", "gegenverkehr"),
        ("lichtzeichenanlage", "lichtzeichen"),
        ("fußgänger", "fussgaenger"),
        ("kinder", "kinder"),
        ("radverkehr", "radverkehr"),
        ("wildwechsel", "wildwechsel"),
        ("bahnübergang", "bahnuebergang"),
        ("andreaskreuz", "andreaskreuz"),
        ("gefahrstelle", "gefahrstelle"),
    ]
    for needle, key in pairs:
        if needle in dl:
            return key
    return None


def _vorbauweiser(sign: dict, hazard_key: str) -> dict[str, str]:
    de = sign["de"]
    side = _side_from_de(de)
    parts = [HAZARD_ADVICE[hazard_key]]
    if side == "right":
        parts.insert(0, VORBAU_RIGHT)
    elif side == "left":
        parts.insert(0, VORBAU_LEFT)
    if "entfernungsangabe" in de.lower():
        parts.append(DISTANCE_PLATE)
    parts.append(SLOW_DOWN)
    return _join(*parts)


def _bake_explanation(sign: dict) -> dict[str, str]:
    de = sign["de"].lower()
    side = _side_from_de(sign["de"])
    if "dreistreifig" in de:
        stripes = _n(
            "Dreistreifige Bake — drei rot-weiße Balken kündigen beschrankten Bahnübergang an.",
            "Трёхполосная разметка (Bake) — три красно-белые полосы предупреждают о переезде со шлагбаумом.",
            "Three-bar marking (Bake) — three red-white bars warn of a gated level crossing.",
            "Трисмугова розмітка (Bake) — три червоно-білі смуги попереджають про переїзд із шлагбаумом.",
            "Balisage à trois bandes — trois barres rouge-blanc annoncent un passage à niveau avec barrières.",
            "Üç şeritli Bake — üç kırmızı-beyaz çubuk, bariyerli demiryolu geçidini bildirir.",
        )
    elif "zweistreifig" in de:
        stripes = _n(
            "Zweistreifige Bake — zwei rot-weiße Balken vor Bahnübergang ohne Schranken.",
            "Двухполосная разметка — два красно-белых бруска перед переездом без шлагбаума.",
            "Two-bar marking — two red-white bars before an ungated level crossing.",
            "Двосмугова розмітка — два червоно-білі бруски перед переїздом без шлагбауму.",
            "Balisage à deux bandes — deux barres rouge-blanc avant passage sans barrières.",
            "İki şeritli Bake — bariyersiz geçitten önce iki kırmızı-beyaz çubuk.",
        )
    else:
        stripes = _n(
            "Einstreifige Bake — ein rot-weißer Balken kündigt Bahnübergang an.",
            "Однополосная разметка — один красно-белый брусок предупреждает о переезде.",
            "Single-bar marking — one red-white bar warns of a level crossing.",
            "Односмугова розмітка — один червоно-білий брусок попереджає про переїзд.",
            "Balisage à une bande — une barre rouge-blanc annonce un passage à niveau.",
            "Tek şeritli Bake — bir kırmızı-beyaz çubuk demiryolu geçidini bildirir.",
        )
    parts = [stripes]
    if side == "right":
        parts.append(VORBAU_RIGHT)
    elif side == "left":
        parts.append(VORBAU_LEFT)
    if "entfernungsangabe" in de:
        parts.append(DISTANCE_PLATE)
    parts.append(_n(
        "Geschwindigkeit reduzieren und auf Züge achten.",
        "Снизьте скорость и следите за поездами.",
        "Reduce speed and watch for trains.",
        "Зменшіть швидкість і стежте за поїздами.",
        "Réduisez la vitesse et surveillez les trains.",
        "Hızı düşürün ve trenlere dikkat edin.",
    ))
    return _join(*parts)




def _speed_limit(speed: int) -> dict[str, str]:
    return _n(
        f"Höchstgeschwindigkeit {speed} km/h — schneller fahren ist verboten.",
        f"Максимальная скорость {speed} км/ч — ехать быстрее запрещено.",
        f"Maximum speed {speed} km/h — driving faster is prohibited.",
        f"Максимальна швидкість {speed} км/год — їхати швидше заборонено.",
        f"Vitesse maximale {speed} km/h — rouler plus vite est interdit.",
        f"Azami hız {speed} km/s — daha hızlı sürmek yasaktır.",
    )


def _speed_limit_end(speed: int) -> dict[str, str]:
    return _n(
        f"Ende der Höchstgeschwindigkeit {speed} km/h — allgemeine oder nächste Beschilderung gilt.",
        f"Конец ограничения {speed} км/ч — действуют общие или следующие знаки.",
        f"End of {speed} km/h limit — general or next signs apply.",
        f"Кінець обмеження {speed} км/год — діють загальні або наступні знаки.",
        f"Fin de la limitation {speed} km/h — règles générales ou panneaux suivants.",
        f"{speed} km/s sınırı sona erdi — genel veya sonraki işaretler geçerli.",
    )


def _min_speed(speed: int) -> dict[str, str]:
    return _n(
        f"Mindestgeschwindigkeit {speed} km/h — langsamer fahren ist verboten.",
        f"Минимальная скорость {speed} км/ч — ехать медленнее запрещено.",
        f"Minimum speed {speed} km/h — driving slower is prohibited.",
        f"Мінімальна швидкість {speed} км/год — їхати повільніше заборонено.",
        f"Vitesse minimale {speed} km/h — rouler plus lentement est interdit.",
        f"Minimum hız {speed} km/s — daha yavaş sürmek yasaktır.",
    )


def _min_speed_end(speed: int) -> dict[str, str]:
    return _n(
        f"Ende der Mindestgeschwindigkeit {speed} km/h.",
        f"Конец минимальной скорости {speed} км/ч.",
        f"End of minimum speed {speed} km/h.",
        f"Кінець мінімальної швидкості {speed} км/год.",
        f"Fin de la vitesse minimale {speed} km/h.",
        f"Minimum hız {speed} km/s sona erdi.",
    )


def _panel_sign(sign: dict) -> dict[str, str] | None:
    de = sign["de"]
    dl = de.lower()
    parts: list[dict[str, str]] = []

    if "überleitungstafel" in dl:
        parts.append(_n(
            "Überleitungstafel — Fahrstreifen werden in eine andere Richtung geleitet (z. B. bei Baustelle oder Umleitung).",
            "Табличка перенаправления — полосы направляются в другую сторону (например, при объезде).",
            "Diversion panel — lanes are guided in another direction (e.g. road works or detour).",
            "Табличка перенаправлення — смуги спрямовуються в інший бік (наприклад, при об'їзді).",
            "Panneau de report — voies dirigées dans une autre direction (détour, travaux).",
            "Yönlendirme paneli — şeritler başka yöne yönlendirilir (ör. yol çalışması).",
        ))
    elif "verschwenkungstafel" in dl:
        short = "kurze verschwenkung" in dl
        parts.append(_n(
            "Verschwenkungstafel — Fahrstreifen verschwenken seitlich, Spurwechsel rechtzeitig vorbereiten."
            + (" Kurze Verschwenkung — schneller Spurwechsel nötig." if short else ""),
            "Табличка смещения — полосы смещаются вбок, заранее перестройтесь."
            + (" Короткое смещение — быстрая перестройка." if short else ""),
            "Shift panel — lanes shift sideways; change lanes in good time."
            + (" Short shift — quick lane change needed." if short else ""),
            "Табличка зміщення — смуги зміщуються вбік, завчасно перебудуйтеся."
            + (" Коротке зміщення — швидка перебудова." if short else ""),
            "Panneau de déviation — voies décalées latéralement ; changez de voie à temps."
            + (" Déviation courte — changement rapide." if short else ""),
            "Kaydırma paneli — şeritler yana kayar; zamanında şerit değiştirin."
            + (" Kısa kaydırma — hızlı şerit değişimi." if short else ""),
        ))
    elif "trennungstafel" in dl:
        parts.append(_n(
            "Trennungstafel — Fahrstreifen teilen sich, wählen Sie rechtzeitig die richtige Spur.",
            "Табличка разделения — полосы расходятся, заранее выберите нужную.",
            "Separation panel — lanes split; choose the correct lane in good time.",
            "Табличка розділення — смуги розходяться, завчасно оберіть потрібну.",
            "Panneau de séparation — voies qui se séparent ; choisissez la bonne voie.",
            "Ayırma paneli — şeritler ayrılır; doğru şeridi zamanında seçin.",
        ))
    elif "zusammenführungstafel" in dl:
        merging = "einmündender" in dl
        parts.append(_n(
            "Zusammenführungstafel — Fahrstreifen führen zusammen, Reißverschlussverfahren anwenden."
            + (" Verkehr von einmündender Strecke mischt sich ein." if merging else ""),
            "Табличка слияния — полосы сходятся, пропускайте по принципу «молнии»."
            + (" Трафик с примыкающей дороги вливается." if merging else ""),
            "Merge panel — lanes merge; use zip-merge."
            + (" Traffic from joining road merges in." if merging else ""),
            "Табличка злиття — смуги сходяться, пропускайте за принципом «блискавки»."
            + (" Рух з приєднувальної дороги вливається." if merging else ""),
            "Panneau de convergence — voies qui fusionnent ; insertion en alternance."
            + (" Trafic de la route qui se joint." if merging else ""),
            "Birleşme paneli — şeritler birleşir; sırayla geçiş yapın."
            + (" Birleşen yoldan trafik katılır." if merging else ""),
        ))
    elif "einengungstafel" in dl or "aufweitungstafel" in dl:
        narrow = "einengung" in dl
        parts.append(_n(
            "Einengungstafel — Fahrbahn verengt sich, Geschwindigkeit anpassen."
            if narrow else
            "Aufweitungstafel — Fahrbahn verbreitert sich, Spurwechsel möglich.",
            "Табличка сужения — дорога сужается, снизьте скорость."
            if narrow else
            "Табличка расширения — дорога расширяется, можно перестроиться.",
            "Narrowing panel — road narrows; adjust speed."
            if narrow else
            "Widening panel — road widens; lane change possible.",
            "Табличка звуження — дорога звужується, зменшіть швидкість."
            if narrow else
            "Табличка розширення — дорога розширюється, можна перебудуватися.",
            "Panneau de rétrécissement — chaussée rétrécie."
            if narrow else
            "Panneau d'élargissement — chaussée s'élargit.",
            "Daralma paneli — yol daralır, hızı ayarlayın."
            if narrow else
            "Genişleme paneli — yol genişler, şerit değiştirilebilir.",
        ))
    elif "aufleitungstafel" in dl:
        parts.append(_n(
            "Aufleitungstafel — Fahrstreifen werden seitlich auf eine andere Spur oder Richtung geleitet.",
            "Табличка направления — полосы боково направляются на другую траекторию.",
            "Guidance panel — lanes are led sideways to another lane or direction.",
            "Табличка наведення — смуги боково спрямовуються на іншу траєкторію.",
            "Panneau de guidage — voies dirigées latéralement.",
            "Yönlendirme paneli — şeritler yana doğru başka yöne yönlendirilir.",
        ))
    elif "fahrstreifentafel" in dl:
        parts.append(_n(
            "Fahrstreifentafel — zeigt die Anzahl und Anordnung der Fahrstreifen voraus.",
            "Табличка полос — показывает количество и расположение полос впереди.",
            "Lane panel — shows number and layout of lanes ahead.",
            "Табличка смуг — показує кількість і розташування смуг попереду.",
            "Panneau de voies — indique le nombre et la disposition des voies.",
            "Şerit paneli — ilerideki şerit sayısı ve düzenini gösterir.",
        ))
    else:
        return None

    gv = _has_gegenverkehr(de)
    if gv is True:
        parts.append(GEGENVERKEHR_YES)
    elif gv is False:
        parts.append(GEGENVERKEHR_NO)

    if re.search(r"\b(ein|zwei|drei|vier|fünf|funf)streifig", dl):
        parts.append(_n(
            "Anzahl der Fahrstreifen auf der Tafel beachten und frühzeitig einordnen.",
            "Смотрите количество полос на табличке и заранее занимайте нужную.",
            "Note lane count on panel and position yourself early.",
            "Дивіться кількість смуг на табличці та завчасно займайте потрібну.",
            "Observez le nombre de voies et placez-vous tôt.",
            "Şerit sayısına dikkat edin ve erken konumlanın.",
        ))

    if "integriertem zeichen" in dl:
        parts.append(_n(
            "Integriertes Verkehrszeichen auf der Tafel beachten (Geschwindigkeit, Verbot etc.).",
            "Учитывайте встроенный знак на табличке (скорость, запрет и т.д.).",
            "Observe integrated sign on panel (speed, prohibition, etc.).",
            "Враховуйте вбудований знак на табличці (швидкість, заборона тощо).",
            "Respectez le panneau intégré (vitesse, interdiction, etc.).",
            "Paneldeki entegre işarete dikkat edin (hız, yasak vb.).",
        ))

    parts.append(_n(
        "Geschwindigkeit an die Situation anpassen.",
        "Скорость подстройте под ситуацию.",
        "Adjust speed to the situation.",
        "Швидкість підлаштуйте під ситуацію.",
        "Adaptez la vitesse à la situation.",
        "Hızı duruma göre ayarlayın.",
    ))
    return _join(*parts)


def _wegweiser(sign: dict) -> dict[str, str] | None:
    de = sign["de"]
    dl = de.lower()
    if not any(k in dl for k in ("wegweiser", "richtung", "ausfahrt", "ausfahrttafel", "ortshinweis", "tourist")):
        return None

    if "vorwegweiser" in dl:
        kind = _n(
            "Vorwegweiser — kündigt Wegweiser mit Zielrichtung frühzeitig an.",
            "Предварительный указатель направления — заранее сообщает о знаке с целями.",
            "Advance direction sign — announces destination sign ahead.",
            "Попередній вказівник напрямку — завчасно повідомляє про знак з цілями.",
            "Présignalisation directionnelle — annonce le panneau de destination.",
            "Ön yön levhası — hedef levhasını önceden bildirir.",
        )
    elif "pfeilwegweiser" in dl:
        kind = _n(
            "Pfeilwegweiser — zeigt Richtung zu Ziel(en) mit Pfeil.",
            "Стрелочный указатель — показывает направление к пункту(ам) назначения.",
            "Arrow direction sign — shows direction to destination(s).",
            "Стрілковий вказівник — показує напрямок до пункту(ів) призначення.",
            "Panneau directionnel à flèche — indique la direction vers la/les destination(s).",
            "Ok yön levhası — hedef(ler)e yönü gösterir.",
        )
    elif "ausfahrt" in dl and "tafel" not in dl:
        kind = _n(
            "Ausfahrtszeichen — markiert die Ausfahrt von Autobahn oder Schnellstraße.",
            "Знак съезда — обозначает выезд с автобана или скоростной дороги.",
            "Exit sign — marks exit from motorway or expressway.",
            "Знак з'їзду — позначає виїзд з автобану або швидкісної дороги.",
            "Signal de sortie — marque la sortie d'autoroute ou voie rapide.",
            "Çıkış işareti — otoyol veya hızlı yoldan çıkışı gösterir.",
        )
    elif "ausfahrttafel" in dl:
        kind = _n(
            "Ausfahrttafel — Tafel mit Zielen der kommenden Ausfahrt.",
            "Табличка съезда — показывает пункты назначения ближайшего съезда.",
            "Exit panel — lists destinations for the upcoming exit.",
            "Табличка з'їзду — показує пункти призначення найближчого з'їзду.",
            "Panneau de sortie — destinations de la prochaine sortie.",
            "Çıkış paneli — yaklaşan çıkışın hedeflerini listeler.",
        )
    elif "tourist" in dl:
        kind = _n(
            "Touristischer Hinweis — Wegweiser zu Sehenswürdigkeit oder Route.",
            "Туристический указатель — направление к достопримечательности или маршруту.",
            "Tourist sign — direction to attraction or route.",
            "Туристичний вказівник — напрямок до пам'ятки або маршруту.",
            "Signal touristique — direction vers site ou itinéraire.",
            "Turistik işaret — cazibe veya rotaya yön.",
        )
    elif "ortshinweis" in dl:
        kind = _n(
            "Ortshinweistafel — Hinweis auf Orte in der Umgebung.",
            "Указатель населённых пунктов — направление к ближайшим городам/районам.",
            "Place name panel — directions to nearby towns or districts.",
            "Вказівник населених пунктів — напрямок до найближчих міст/районів.",
            "Panneau de localités — directions vers villes ou quartiers.",
            "Yer adı paneli — yakın kasaba veya bölgelere yön.",
        )
    else:
        kind = _n(
            "Wegweiser — zeigt Fahrtrichtung zu Zielort(en).",
            "Указатель направления — показывает путь к пункту(ам) назначения.",
            "Direction sign — shows route to destination(s).",
            "Вказівник напрямку — показує шлях до пункту(ів) призначення.",
            "Panneau de direction — indique la route vers la/les destination(s).",
            "Yön levhası — hedef(ler)e giden yolu gösterir.",
        )

    parts = [kind, _n(
        "Rechtzeitig die passende Spur wählen.",
        "Заранее выберите нужную полосу.",
        "Choose the correct lane in good time.",
        "Завчасно оберіть потрібну смугу.",
        "Choisissez la bonne voie à temps.",
        "Zamanında doğru şeridi seçin.",
    )]
    if "linksweisend" in dl or "nach links" in dl:
        parts.append(_n(
            "Ziele liegen links — links einordnen.",
            "Цели слева — перестройтесь налево.",
            "Destinations are to the left — move left.",
            "Цілі ліворуч — перебудуйтеся ліворуч.",
            "Destinations à gauche — placez-vous à gauche.",
            "Hedefler solda — sola geçin.",
        ))
    elif "rechtsweisend" in dl or "nach rechts" in dl:
        parts.append(_n(
            "Ziele liegen rechts — rechts einordnen.",
            "Цели справа — перестройтесь направо.",
            "Destinations are to the right — move right.",
            "Цілі праворуч — перебудуйтеся праворуч.",
            "Destinations à droite — placez-vous à droite.",
            "Hedefler sağda — sağa geçin.",
        ))
    return _join(*parts)



def _category_fallback(category: str) -> dict[str, str]:
    fallbacks = {
        "warning": _n(
            "Gefahr voraus — Geschwindigkeit anpassen und aufmerksam fahren.",
            "Опасность впереди — снизьте скорость и будьте внимательны.",
            "Hazard ahead — adjust speed and drive attentively.",
            "Небезпека попереду — зменшіть швидкість і будьте уважні.",
            "Danger — adaptez la vitesse et soyez attentif.",
            "Tehlike ileride — hızı ayarlayın ve dikkatli sürün.",
        ),
        "prohibitory": _n(
            "Verbot — die auf dem Schild dargestellte Handlung ist nicht erlaubt.",
            "Запрет — действие на знаке не разрешено.",
            "Prohibition — the action shown is not allowed.",
            "Заборона — дія на знаку не дозволена.",
            "Interdiction — l'action indiquée n'est pas autorisée.",
            "Yasak — gösterilen eylem izin verilmez.",
        ),
        "mandatory": _n(
            "Gebot — Sie müssen die angezeigte Handlung ausführen.",
            "Предписание — вы обязаны выполнить указанное действие.",
            "Mandatory — you must perform the indicated action.",
            "Примус — ви зобов'язані виконати вказану дію.",
            "Obligation — vous devez effectuer l'action indiquée.",
            "Zorunluluk — gösterilen eylemi yapmalısınız.",
        ),
        "information": _n(
            "Hinweiszeichen — informiert über Straßenverlauf, Einrichtung oder Regelung.",
            "Информационный знак — сообщает о дорожной ситуации, объекте или правиле.",
            "Information sign — indicates road layout, facility or rule.",
            "Інформаційний знак — повідомляє про дорожню ситуацію, об'єкт або правило.",
            "Panneau d'information — indique configuration, équipement ou règle.",
            "Bilgi işareti — yol düzeni, tesis veya kural hakkında bilgi verir.",
        ),
        "additional": _n(
            "Zusatzzeichen — modifiziert die Bedeutung des darüberliegenden Hauptzeichens.",
            "Дополнительная табличка — уточняет значение основного знака над ней.",
            "Supplementary plate — modifies the meaning of the main sign above it.",
            "Додаткова табличка — уточнює значення основного знака над нею.",
            "Plaque complémentaire — modifie le sens du panneau principal au-dessus.",
            "Ek levha — üstündeki ana işaretin anlamını değiştirir.",
        ),
    }
    return fallbacks.get(category, fallbacks["information"])


def _code_num(code: str) -> int | None:
    m = re.match(r"(\d+)", code.replace("Z", ""))
    return int(m.group(1)) if m else None


def _is_panel_or_direction(de: str) -> bool:
    dl = de.lower()
    return any(k in dl for k in (
        "überleitungstafel", "verschwenkungstafel", "trennungstafel",
        "zusammenführungstafel", "einengungstafel", "aufleitungstafel",
        "aufweitungstafel", "fahrstreifentafel", "wegweiser", "ausfahrttafel",
        "vorwegweiser", "pfeilwegweiser", "ortshinweis", "ankündigungstafel",
        "entfernungstafel", "touristischer hinweis",
    ))


def _warning_handler(sign: dict) -> dict[str, str] | None:
    de = sign["de"]
    dl = de.lower()
    code = sign.get("stvo_code", "")

    if sign.get("category") == "information" or _is_panel_or_direction(de):
        return None

    if "aufstellung" in dl:
        hk = _hazard_key(de)
        if hk:
            return _vorbauweiser(sign, hk)

    hk = _hazard_key(de)
    if hk and hk in HAZARD_ADVICE:
        return _join(HAZARD_ADVICE[hk], SLOW_DOWN)

    if code.startswith("201"):
        return _join(HAZARD_ADVICE["andreaskreuz"], SLOW_DOWN)

    return None


def _bake_handler(sign: dict) -> dict[str, str] | None:
    de = sign["de"].lower()
    if "bake" in de or ("bahnübergang" in de and "aufstellung" in de):
        return _bake_explanation(sign)
    return None


def _priority_handler(sign: dict) -> dict[str, str] | None:
    code = sign.get("stvo_code", "")
    de = sign["de"].lower()

    rules: list[tuple[Callable[[], bool], dict[str, str]]] = [
        (lambda: code == "206" or ("halt" in de and "vorfahrt" in de),
         _n("Vollständig an der Haltelinie anhalten, dann anderen Verkehrsteilnehmern Vorfahrt gewähren.",
            "Полная остановка у линии «Стоп», затем уступить дорогу.",
            "Complete stop at stop line, then give way.",
            "Повна зупинка біля лінії «Стоп», потім дайте дорогу.",
            "Arrêt complet, puis cédez le passage.",
            "Dur çizgisinde tam durun, ardından yol verin.")),
        (lambda: code == "205" or de.startswith("vorfahrt gewähren"),
         _n("Anderen Verkehrsteilnehmern Vorfahrt gewähren — nur anhalten wenn nötig.",
            "Уступите дорогу — останавливайтесь только если мешает транспорт.",
            "Give way — stop only if necessary.",
            "Дайте дорогу — зупиняйтесь лише якщо заважає транспорт.",
            "Cédez le passage — arrêtez-vous si nécessaire.",
            "Yol verin — yalnızca gerekirse durun.")),
        (lambda: code == "306" or ("vorfahrtstraße" in de and "ende" not in de),
         _n("Sie befinden sich auf einer Vorfahrtstraße — Vorfahrt an Kreuzungen.",
            "Вы на главной дороге — преимущество на перекрёстках.",
            "Priority road — right of way at intersections.",
            "Ви на головній дорозі — перевага на перехрестях.",
            "Route prioritaire — priorité aux carrefours.",
            "Ana yoldasınız — kavşaklarda önceliğiniz var.")),
        (lambda: code == "307" or "ende der vorfahrtstraße" in de,
         _n("Ende der Vorfahrtstraße — normale Vorfahrtsregeln gelten.",
            "Конец главной дороги — обычные правила приоритета.",
            "End of priority road — normal rules apply.",
            "Кінець головної дороги — звичайні правила пріоритету.",
            "Fin de route prioritaire — règles normales.",
            "Ana yol sonu — normal kurallar geçerli.")),
        (lambda: code == "301" or de == "vorfahrt",
         _n("An der nächsten Kreuzung haben Sie Vorfahrt.",
            "На следующем перекрёстке у вас преимущество.",
            "Priority at the next intersection.",
            "На наступному перехресті у вас перевага.",
            "Priorité à la prochaine intersection.",
            "Bir sonraki kavşakta önceliğiniz var.")),
        (lambda: code == "208" or "vorrang des gegenverkehrs" in de,
         _n("Dem Gegenverkehr Vorrang gewähren — bei Beenigung zuerst warten.",
            "Уступите встречному — при сужении сначала пропустите его.",
            "Give way to oncoming traffic at narrow sections.",
            "Поступіться зустрічному — на звуженні спочатку пропустіть.",
            "Cédez le passage au trafic en sens inverse.",
            "Karşı yönden gelenlere yol verin.")),
        (lambda: code == "308" or "vorrang vor dem gegenverkehr" in de,
         _n("Sie haben Vorrang vor dem Gegenverkehr.",
            "У вас преимущество перед встречным.",
            "You have priority over oncoming traffic.",
            "У вас перевага перед зустрічним.",
            "Vous avez la priorité sur le trafic en sens inverse.",
            "Karşı yönden gelenlere göre önceliğiniz var.")),
    ]
    for cond, result in rules:
        if cond():
            return result
    return None


def _mandatory_handler(sign: dict) -> dict[str, str] | None:
    de = sign["de"].lower()
    code = sign.get("stvo_code", "")

    if "hier links" in de or (code.startswith("211") and "links" in de):
        return _n("Pflicht: hier nach links.", "Обязательно: здесь налево.", "Mandatory: turn left here.",
                  "Обов'язково: тут ліворуч.", "Obligatoire : à gauche ici.", "Zorunlu: burada sola.")
    if "hier rechts" in de or (code.startswith("211") and "rechts" in de):
        return _n("Pflicht: hier nach rechts.", "Обязательно: здесь направо.", "Mandatory: turn right here.",
                  "Обов'язково: тут праворуч.", "Obligatoire : à droite ici.", "Zorunlu: burada sağa.")
    if "geradeaus oder rechts" in de:
        return _n("Pflicht: nur geradeaus oder rechts.", "Только прямо или направо.", "Straight or right only.",
                  "Лише прямо або праворуч.", "Tout droit ou à droite.", "Düz veya sağa.")
    if "geradeaus oder links" in de:
        return _n("Pflicht: nur geradeaus oder links.", "Только прямо или налево.", "Straight or left only.",
                  "Лише прямо або ліворуч.", "Tout droit ou à gauche.", "Düz veya sola.")
    if "geradeaus" in de and code.startswith(("209", "214")):
        return _n("Pflicht: nur geradeaus.", "Только прямо.", "Straight ahead only.",
                  "Лише прямо.", "Tout droit uniquement.", "Yalnızca düz.")
    if code.startswith("209") and "links" in de:
        return _n("Pflicht: nach links.", "Обязательно налево.", "Mandatory: left.",
                  "Обов'язково ліворуч.", "Obligatoire : à gauche.", "Zorunlu: sola.")
    if code.startswith("209") and "rechts" in de:
        return _n("Pflicht: nach rechts.", "Обязательно направо.", "Mandatory: right.",
                  "Обов'язково праворуч.", "Obligatoire : à droite.", "Zorunlu: sağa.")
    if code == "215" or "kreisverkehr" in de:
        return _n(
            "Kreisverkehr — Verkehr im Kreis hat Vorfahrt, rechts herumfahren.",
            "Кольцевой разъезд — уступите транспорту в круге, движение по часовой стрелке.",
            "Roundabout — give way to traffic in the circle; drive clockwise.",
            "Кільцевий перехрестя — надайте перевагу транспорту в колі, рухайтесь за годинниковою стрілкою.",
            "Carrefour giratoire — cédez le passage aux véhicules engagés ; circulez dans le sens horaire.",
            "Dönel kavşak — kavşaktaki trafiğe yol verin, saat yönünde ilerleyin.",
        )
    if "einbahn" in de and "links" in de:
        return _n("Einbahnstraße — nur in Pfeilrichtung (links).", "Одностороннее — только налево.",
                  "One-way — left only.", "Односторонній — лише ліворуч.", "Sens unique — gauche.", "Tek yön — sola.")
    if "einbahn" in de and "rechts" in de:
        return _n("Einbahnstraße — nur in Pfeilrichtung (rechts).", "Одностороннее — только направо.",
                  "One-way — right only.", "Односторонній — лише праворуч.", "Sens unique — droite.", "Tek yön — sağa.")
    if "rechts vorbei" in de:
        return _n("Hindernis rechts umfahren.", "Объезжайте справа.", "Pass on the right.",
                  "Об'їжджайте праворуч.", "Contournez par la droite.", "Sağdan geçin.")
    if "links vorbei" in de:
        return _n("Hindernis links umfahren.", "Объезжайте слева.", "Pass on the left.",
                  "Об'їжджайте ліворуч.", "Contournez par la gauche.", "Soldan geçin.")
    if code.startswith("224"):
        if "schulbus" in de:
            return _n("Schulbushaltestelle — besonders vorsichtig.", "Остановка школьного автобуса — осторожно.",
                      "School bus stop — extra care.", "Зупинка шкільного автобуса — обережно.",
                      "Arrêt bus scolaire — prudence.", "Okul otobüsü durağı — dikkatli.")
        return _n("Haltestelle — nicht halten/parken.", "Остановка — не останавливайтесь.",
                  "Bus stop — do not stop/park.", "Зупинка — не зупиняйтесь.", "Arrêt — ne stationnez pas.", "Durak — durmayın.")
    if code == "237" or de == "radweg":
        return _n("Radweg — nur für Radfahrer.", "Велодорожка — только велосипеды.", "Cycle path only.",
                  "Велодоріжка — лише велосипеди.", "Piste cyclable.", "Bisiklet yolu.")
    if code == "238" or de == "reitweg":
        return _n("Reitweg — nur für Reiter.", "Конная дорожка.", "Bridle path only.",
                  "Кінна доріжка.", "Chemin équestre.", "At yolu.")
    if code == "239" or de == "gehweg":
        return _n("Gehweg — nur für Fußgänger.", "Тротуар — только пешеходы.", "Footpath only.",
                  "Тротуар — лише пішоходи.", "Chemin piéton.", "Yaya yolu.")
    if code == "268" or "schneeketten" in de:
        return _n("Schneeketten vorgeschrieben.", "Нужны снежные цепи.", "Snow chains required.",
                  "Потрібні ланцюги.", "Chaînes obligatoires.", "Kar zinciri zorunlu.")
    return None


def _prohibitory_handler(sign: dict) -> dict[str, str] | None:
    code = sign.get("stvo_code", "")
    de = sign["de"].lower()
    speed = _extract_speed(code, sign["de"])

    if code.startswith("274") and speed:
        return _speed_limit(speed)
    if code.startswith("278") and speed:
        return _speed_limit_end(speed)
    if code.startswith("275") and speed:
        return _min_speed(speed)
    if code.startswith("279") and speed:
        return _min_speed_end(speed)

    prohibitions = [
        (lambda: code == "260",
         _n("Verbotsschild — die dargestellte Handlung ist für den angegebenen Verkehrsteilnehmer verboten.",
            "Запрещающий знак — указанное действие запрещено для данной категории участников движения.",
            "Prohibition sign — the shown action is forbidden for the indicated road users.",
            "Заборонний знак — зазначена дія заборонена для відповідної категорії учасників руху.",
            "Panneau d'interdiction — l'action indiquée est interdite pour les usagers concernés.",
            "Yasak işareti — gösterilen eylem ilgili yol kullanıcıları için yasaktır.")),
        (lambda: code == "261",
         _n("Ende des Verbots — die vorherige Beschränkung gilt nicht mehr.",
            "Конец запрета — предыдущее ограничение больше не действует.",
            "End of prohibition — the previous restriction no longer applies.",
            "Кінець заборони — попереднє обмеження більше не діє.",
            "Fin de l'interdiction — la restriction précédente ne s'applique plus.",
            "Yasağın sonu — önceki kısıtlama artık geçerli değil.")),
        (lambda: code == "267" or "verbot der einfahrt" in de,
         _n("Einfahrt verboten.", "Въезд запрещён.", "No entry.", "В'їзд заборонений.", "Entrée interdite.", "Giriş yasak.")),
        (lambda: code == "272" or "wendens" in de,
         _n("Wenden verboten.", "Разворот запрещён.", "No U-turn.", "Розворот заборонений.", "Demi-tour interdit.", "U dönüşü yasak.")),
        (lambda: "mindestabstand" in de,
         _n("Mindestabstand einhalten.", "Соблюдайте дистанцию.", "Keep minimum distance.", "Дотримуйтесь дистанції.", "Distance minimale.", "Minimum mesafe.")),
        (lambda: code == "276",
         _n("Überholverbot für alle Kraftfahrzeuge.", "Обгон запрещён всем.", "No overtaking (all).", "Обгін заборонений усім.", "Dépassement interdit.", "Sollama yasak.")),
        (lambda: code == "277",
         _n("Überholverbot für Fahrzeuge über 3,5 t.", "Обгон запрещён грузовикам.", "No overtaking (>3.5t).", "Обгін заборонений вантажівкам.", "Dépassement interdit >3,5t.", ">3,5t sollama yasak.")),
        (lambda: code.startswith("277.1"),
         _n("Mehrspurige dürfen Einspurige nicht überholen.", "Многополосные не обгоняют однополосных.", "Multi-lane must not overtake single-track.", "Багатосмугові не обганяють односмугових.", "Multi-voies ne dépassent pas mono-voie.", "Çok şeritliler tek şeritlileri geçemez.")),
        (lambda: code == "280",
         _n("Ende Überholverbot (alle).", "Конец запрета обгона.", "End overtaking ban.", "Кінець заборони обгону.", "Fin interdiction dépassement.", "Sollama yasağı bitti.")),
        (lambda: code == "281",
         _n("Ende Überholverbot (>3,5 t).", "Конец запрета для грузовиков.", "End heavy overtaking ban.", "Кінець заборони для вантажівок.", "Fin interdiction >3,5t.", "Ağır sollama yasağı bitti.")),
        (lambda: code == "282",
         _n("Ende aller streckenbezogenen Beschränkungen.", "Конец всех участковых ограничений.", "End all local restrictions.", "Кінець усіх ділянкових обмежень.", "Fin restrictions locales.", "Yerel kısıtlamalar bitti.")),
        (lambda: code == "283" or (code.startswith("283") and "absolut" in de),
         _n("Absolutes Haltverbot.", "Абсолютный запрет остановки.", "Absolute no stopping.", "Абсолютна заборона зупинки.", "Arrêt absolument interdit.", "Mutlak durma yasağı.")),
        (lambda: code == "286" or (code.startswith("286") and "eingeschränkt" in de),
         _n("Eingeschränktes Haltverbot — Parken verboten.", "Ограниченный запрет — парковка запрещена.", "Restricted stopping ban.", "Обмежена заборона — паркування заборонене.", "Arrêt limité.", "Sınırlı durma yasağı.")),
        (lambda: "mofas" in de,
         _n("Mofas verboten.", "Мопеды запрещены.", "Mopeds prohibited.", "Мопеди заборонені.", "Mobylettes interdites.", "Mopedler yasak.")),
        (lambda: "viehtrieb" in de and "verbot" in de,
         _n("Viehtrieb verboten.", "Прогон скота запрещён.", "Cattle drive prohibited.", "Перегін худоби заборонений.", "Bétail interdit.", "Hayvan sürüsü yasak.")),
        (lambda: "personenkraftwagen mit anhänger" in de,
         _n("PKW mit Anhänger verboten.", "Легковые с прицепом запрещены.", "Cars with trailer prohibited.", "Легкові з причепом заборонені.", "Voitures avec remorque interdites.", "Römorklu binek yasak.")),
        (lambda: "lastkraftwagen mit anhänger" in de,
         _n("LKW mit Anhänger verboten.", "Грузовики с прицепом запрещены.", "Trucks with trailer prohibited.", "Вантажівки з причепом заборонені.", "Camions avec remorque interdits.", "Römorklu kamyon yasak.")),
        (lambda: "25 km/h" in de,
         _n("Fahrzeuge ≤25 km/h verboten.", "ТС ≤25 км/ч запрещены.", "Vehicles ≤25 km/h prohibited.", "ТЗ ≤25 км/год заборонені.", "Véhicules ≤25 km/h interdits.", "≤25 km/s araçlar yasak.")),
        (lambda: "elektrokleinstfahrzeuge" in de,
         _n("E-Scooter etc. verboten.", "E-scooter запрещены.", "E-scooters prohibited.", "E-scooter заборонені.", "Trottinettes interdites.", "E-scooter yasak.")),
        (lambda: "wassergefährdender" in de,
         _n("Wassergefährdende Ladung verboten.", "Груз, опасный для воды, запрещён.", "Water-polluting cargo prohibited.", "Вантаж, небезпечний для води, заборонений.", "Marchandises dangereuses pour l'eau interdites.", "Su için tehlikeli yük yasak.")),
    ]
    for cond, result in prohibitions:
        if cond():
            return result
    return None


def _info_handler(sign: dict) -> dict[str, str] | None:
    if sign.get("category") == "warning":
        return None
    code = sign.get("stvo_code", "")
    de = sign["de"]
    dl = de.lower()
    if "aufstellung" in dl:
        return None

    panel = _panel_sign(sign)
    if panel:
        return panel

    weg = _wegweiser(sign)
    if weg:
        return weg

    bake = _bake_handler(sign)
    if bake:
        return bake

    if code in ("310",) or "ortstafel vorderseite" in dl:
        return _n("Ortsbeginn — innerorts meist 50 km/h und besondere Regeln.",
                  "Начало населённого пункта — внутри обычно 50 км/ч.", "Town entry — typically 50 km/h inside.",
                  "Початок населеного пункту — зазвичай 50 км/год.", "Entrée agglomération — 50 km/h.", "Yerleşim başlangıcı — 50 km/s.")
    if code.startswith("311") or "ortstafel rückseite" in dl:
        return _n("Ortsende — außerorts andere Regeln.", "Конец населённого пункта.", "Town exit.", "Кінець населеного пункту.", "Sortie agglomération.", "Yerleşim sonu.")
    if code.startswith("330.1") or (de.startswith("Autobahn") and "ende" not in dl):
        return _n("Autobahn — nur Kraftfahrzeuge, Mindestgeschwindigkeit.", "Автобан — только моторные ТС.", "Motorway — motor vehicles only.", "Автобан — лише моторні ТЗ.", "Autoroute — véhicules à moteur.", "Otoyol — motorlu araçlar.")
    if code.startswith("330.2") or "ende der autobahn" in dl:
        return _n("Ende Autobahn.", "Конец автобана.", "End of motorway.", "Кінець автобану.", "Fin autoroute.", "Otoyol sonu.")
    if code.startswith("331.1"):
        return _n("Kraftfahrstraße — nur Kraftfahrzeuge.", "Автомагистраль.", "Expressway.", "Автомагістраль.", "Route pour automobiles.", "Kraftfahrstraße.")
    if code.startswith("331.2"):
        return _n("Ende Kraftfahrstraße.", "Конец автомагистрали.", "End expressway.", "Кінець автомагістралі.", "Fin route automobiles.", "Kraftfahrstraße sonu.")
    if "sackgasse" in dl:
        if "radverkehr" in dl or "fußgänger" in dl:
            return _n("Sackgasse — für Rad/Fuß durchlässig, Autos wenden.", "Тупик — вело/пешходы проходят.", "Dead end — bikes/peds pass through.", "Тупик — вело/пішоходи проходять.", "Impasse — cyclistes/piétons passent.", "Çıkmaz — bisiklet/yaya geçer.")
        return _n("Sackgasse — nur zum Wenden.", "Тупик — только разворот.", "Dead end — turn only.", "Тупик — лише розворот.", "Impasse — retour uniquement.", "Çıkmaz — yalnızca dönüş.")
    if "tunnel" in dl:
        return _n("Tunnel — Abstand, Licht an, nicht anhalten.", "Тоннель — дистанция, свет.", "Tunnel — distance, lights on.", "Тунель — дистанція, світло.", "Tunnel — distance, feux.", "Tünel — mesafe, farlar.")
    if "nothalte" in dl or "pannenbucht" in dl:
        return _n("Nothaltebucht — nur bei Notfall.", "Аварийный карман — только при поломке.", "Emergency bay — breakdown only.", "Аварійна карман — лише при поломці.", "Baie urgence — panne seulement.", "Acil cebe — arıza için.")
    if "taxistand" in dl:
        parts = [_n("Taxistand — nur Taxis.", "Стоянка такси.", "Taxi stand only.", "Стоянка таксі.", "Station taxis.", "Taksi durağı.")]
        if "anfang" in dl:
            parts.append(_n("Beginn Zone.", "Начало зоны.", "Zone start.", "Початок зони.", "Début zone.", "Bölge başı."))
        elif "ende" in dl:
            parts.append(_n("Ende Zone.", "Конец зоны.", "Zone end.", "Кінець зони.", "Fin zone.", "Bölge sonu."))
        side = _side_from_de(de)
        if side == "right":
            parts.append(VORBAU_RIGHT)
        elif side == "left":
            parts.append(VORBAU_LEFT)
        return _join(*parts)
    if "ladebereich" in dl:
        parts = [_n("Ladebereich — nur Be-/Entladen.", "Зона погрузки.", "Loading zone only.", "Зона навантаження.", "Zone chargement.", "Yükleme alanı.")]
        side = _side_from_de(de)
        if side == "right":
            parts.append(VORBAU_RIGHT)
        elif side == "left":
            parts.append(VORBAU_LEFT)
        return _join(*parts)
    if "parken auf gehwegen" in dl:
        return _join(_n("Parken auf Gehweg — halb, in Richtung.", "Парковка на тротуаре — наполовину.", "Pavement parking — half, in direction.", "Паркування на тротуарі — наполовину.", "Stationnement trottoir — à moitié.", "Kaldırımda park — yarısı."),
                     _n("Fußgängern Platz lassen.", "Место для пешеходов.", "Leave space for pedestrians.", "Місце для пішоходів.", "Place aux piétons.", "Yayalara yer bırakın."))
    if "parken" in dl or code.startswith("314"):
        return _n("Parken erlaubt — Zusatzzeichen beachten.", "Парковка разрешена.", "Parking allowed.", "Паркування дозволене.", "Stationnement autorisé.", "Park izinli.")
    if "parkscheibe" in dl:
        return _n("Parkscheibe erforderlich.", "Нужен парковочный диск.", "Parking disc required.", "Потрібен парковий диск.", "Disque requis.", "Park diski gerekli.")
    if code.startswith("242"):
        return _n("Fußgängerzone beginnt.", "Пешеходная зона.", "Pedestrian zone starts.", "Пішохідна зона.", "Zone piétonne.", "Yaya bölgesi.")
    if code.startswith("244.3"):
        return _n("Fahrradzone beginnt.", "Велозона.", "Bicycle zone starts.", "Велозона.", "Zone cyclable.", "Bisiklet bölgesi.")
    if code.startswith("244.2") or code.startswith("244.4"):
        return _n("Zone endet.", "Конец зоны.", "Zone ends.", "Кінець зони.", "Fin de zone.", "Bölge sonu.")
    if code.startswith("325.1"):
        return _n("Verkehrsberuhigter Bereich — Schrittgeschwindigkeit.", "Зона успокоенного движения.", "Traffic-calmed area.", "Зона заспокоєного руху.", "Zone de rencontre.", "Sakinleştirilmiş bölge.")
    if code.startswith("325.2"):
        return _n("Ende verkehrsberuhigter Bereich.", "Конец зоны.", "End calmed area.", "Кінець зони.", "Fin zone.", "Bölge sonu.")
    if code.startswith("270.1"):
        return _n("Umweltzone — Plakette erforderlich.", "Экозона — нужна наклейка.", "Low-emission zone — badge required.", "Екозона — потрібна наклейка.", "Zone environnementale.", "Çevre bölgesi.")
    if code.startswith("270.2"):
        return _n("Ende Umweltzone.", "Конец экозоны.", "End low-emission zone.", "Кінець екозони.", "Fin zone.", "Bölge sonu.")
    if code.startswith("290.1"):
        return _n("Haltverbotszone beginnt.", "Зона запрета остановки.", "No-stopping zone starts.", "Зона заборони зупинки.", "Zone arrêt interdit.", "Durma yasağı bölgesi.")
    if code.startswith("290.2"):
        return _n("Haltverbotszone endet.", "Конец зоны.", "Zone ends.", "Кінець зони.", "Fin zone.", "Bölge sonu.")
    if "seitenstreifen" in dl and "nicht befahrbar" in dl:
        return _n("Seitenstreifen nicht befahrbar.", "Обочина не для движения.", "Shoulder not drivable.", "Узбіччя не для руху.", "Accotement interdit.", "Banket kullanılamaz.")
    if "seitenstreifen" in dl and "befahrbar" in dl:
        return _n("Seitenstreifen befahrbar — bei Stau nutzbar.", "Обочину можно использовать.", "Shoulder may be used.", "Узбіччя можна використовувати.", "Accotement praticable.", "Banket kullanılabilir.")
    if code == "293" or "fußgängerüberweg" in dl:
        return _n("Fußgängerüberweg — Fußgänger haben Vorrang.", "Пешеходный переход — приоритет пешеходов.", "Crossing — pedestrians have priority.", "Пішохідний перехід — пріоритет пішоходів.", "Passage piéton — priorité piétons.", "Yaya geçidi — yayalar öncelikli.")
    if code == "294" or "haltlinie" in dl:
        return _n("Haltlinie — hier anhalten wenn nötig.", "Линия остановки.", "Stop line.", "Лінія зупинки.", "Ligne d'arrêt.", "Dur çizgisi.")
    if code == "341" or "wartelinie" in dl:
        return _n("Wartelinie — hier warten.", "Линия ожидания.", "Waiting line.", "Лінія очікування.", "Ligne d'attente.", "Bekleme çizgisi.")
    if "haifischzähne" in dl:
        return _n("Haifischzähne — Vorfahrt gewähren.", "«Акульи зубы» — уступите.", "Shark's teeth — give way.", "«Акулі зуби» — поступіться.", "Dents de requin — cédez.", "Köpekbalığı dişleri — yol verin.")
    if code == "356" or "verkehrshelfer" in dl:
        return _n("Verkehrshelfer — Anweisungen befolgen.", "Регулировщик — выполняйте указания.", "Traffic controller — follow instructions.", "Регулювальник — виконуйте вказівки.", "Agent circulation.", "Trafik görevlisi.")
    if "seniorenheim" in dl:
        return _n("Seniorenheim — ältere Menschen können überqueren.", "Дом престарелых — пожилые могут переходить.", "Senior home — elderly may cross.", "Будинок для літніх.", "Maison de retraite.", "Yaşlılar evi.")
    if "richtungstafel" in dl:
        parts = [_n(
            "Richtungstafel in Kurve — empfiehlt sichere Geschwindigkeit und Fahrtrichtung.",
            "Указатель в повороте — рекомендует безопасную скорость и направление.",
            "Curve direction plate — recommends safe speed and line.",
            "Вказівник у повороті — рекомендує безпечну швидкість і напрямок.",
            "Panneau en courbe — vitesse et trajectoire sûres.",
            "Viraj yön levhası — güvenli hız ve yön önerir.",
        )]
        side = _side_from_de(de)
        if side == "right":
            parts.insert(0, VORBAU_RIGHT)
        elif side == "left":
            parts.insert(0, VORBAU_LEFT)
        return _join(*parts)
    if "umleitung" in dl:
        return _n("Umleitung — folgen Sie der ausgeschilderten Route.", "Объезд — следуйте по указанному маршруту.", "Detour — follow signed route.", "Об'їзд — слідуйте за вказівниками.", "Déviation — suivez la route.", "Yönlendirme — işaretli rotayı izleyin.")
    if "fernsprecher" in dl:
        return _n("Notruftelefon in der Nähe.", "Телефон экстренной связи.", "Emergency phone nearby.", "Телефон екстренного зв'язку.", "Téléphone d'urgence.", "Acil telefon.")
    if "tankstelle" in dl:
        return _n("Tankstelle in der Nähe.", "Заправка поблизости.", "Petrol station nearby.", "Заправка поблизу.", "Station-service.", "Benzin istasyonu.")
    if "ladestation" in dl:
        return _n("Ladestation für Elektrofahrzeuge.", "Зарядка для электромобилей.", "EV charging.", "Зарядка для електромобілів.", "Borne VE.", "Elektrikli araç şarjı.")
    if "gemeinsamer geh- und radweg" in dl:
        return _n("Gemeinsamer Geh- und Radweg — Fußgänger und Radfahrer teilen sich den Weg.",
                  "Общая дорожка для пешеходов и велосипедистов.", "Shared foot and cycle path.",
                  "Спільна доріжка для пішоходів і велосипедистів.", "Chemin partagé piétons/cyclistes.", "Ortak yaya/bisiklet yolu.")
    if "getrennter rad- und gehweg" in dl:
        return _n("Getrennter Rad- und Gehweg — nicht auf den Gehweg fahren.",
                  "Раздельные вело- и пешеходная дорожки.", "Separated cycle and foot paths.",
                  "Роздільні вело- та пішохідна доріжки.", "Pistes séparées.", "Ayrı bisiklet/yaya yolları.")
    if "seitenstreifen" in dl and code.startswith("223"):
        if "befahren" in dl and "nicht" not in dl:
            return _n("Seitenstreifen darf befahren werden — nur wenn ausgeschildert.",
                      "Обочину можно использовать.", "Hard shoulder may be used.", "Узбіччя можна використовувати.", "Accotement praticable.", "Banket kullanılabilir.")
        if "nicht mehr befahren" in dl or "räumen" in dl:
            return _n("Seitenstreifen nicht mehr befahren — zurück auf Fahrstreifen.",
                      "Покиньте обочину — вернитесь на полосу.", "Leave shoulder — return to lane.", "Покиньте узбіччя — поверніться на смугу.", "Quittez l'accotement.", "Banketi terk edin.")
    if code.startswith("274.1") or "tempo 30-zone" in dl:
        return _n("Tempo-30-Zone beginnt — Höchstgeschwindigkeit 30 km/h in der ganzen Zone.",
                  "Зона 30 км/ч — максимум 30 во всей зоне.", "30 km/h zone starts.", "Зона 30 км/год.", "Zone 30 km/h.", "30 km/s bölgesi başlıyor.")
    if code.startswith("274.2"):
        return _n("Tempo-30-Zone endet.", "Конец зоны 30 км/ч.", "30 km/h zone ends.", "Кінець зони 30 км/год.", "Fin zone 30 km/h.", "30 km/s bölgesi bitiyor.")
    if "fahrstreifenbegrenzung" in dl:
        return _n("Einseitige Fahrstreifenbegrenzung — nicht über die Linie fahren.",
                  "Одностороннее ограничение полосы — не пересекайте линию.", "Lane boundary — do not cross.", "Обмеження смуги — не перетинайте лінію.", "Limite de voie.", "Şerit sınırı.")
    if "pfeilmarkierung" in dl or "vorankündigungspfeil" in dl:
        return _n("Pfeilmarkierung — Fahrtrichtung oder Spurende beachten.",
                  "Стрелочная разметка — следуйте направлению.", "Arrow marking — follow direction.", "Стрілкова розмітка.", "Marquage flèche.", "Ok işareti.")
    if code == "298" or "sperrfläche" in dl:
        return _n("Sperrfläche — Halten und Parken verboten.", "Запретная зона — нельзя останавливаться.", "Keep-clear area — no stopping.", "Заборонена зона.", "Zone interdite.", "Yasak alan.")
    if code == "299" or "grenzmarkierung" in dl:
        return _n("Grenzmarkierung — zeigt Ausmaß des Halt-/Parkverbots.", "Граница зоны запрета остановки.", "Boundary of stopping ban.", "Межа заборони зупинки.", "Limite arrêt interdit.", "Durma yasağı sınırı.")
    if "wandererparkplatz" in dl:
        return _n("Wandererparkplatz — für Wanderer, kurz parken.", "Парковка для туристов.", "Hiker parking.", "Паркування для туристів.", "Parking randonneurs.", "Yürüyüşçü parkı.")
    if "radschnellweg" in dl:
        if "ende" in dl:
            return _n("Ende Radschnellweg.", "Конец велоскоростной дороги.", "End cycle highway.", "Кінець велошвидкісної дороги.", "Fin piste cyclable rapide.", "Bisiklet otoyolu sonu.")
        return _n("Radschnellweg — schnelle Radverbindung, Radfahrer haben Vorrang.", "Велоскоростная дорога.", "Cycle highway — cyclists priority.", "Велошвидкісна дорога.", "Piste cyclable rapide.", "Bisiklet otoyolu.")
    if "wasserschutzgebiet" in dl:
        return _n("Wasserschutzgebiet — keine Verunreinigung.", "Водоохранная зона.", "Water protection area.", "Водоохоронна зона.", "Protection des eaux.", "Su koruma bölgesi.")
    if "pannenhilfe" in dl:
        return _n("Pannenhilfe verfügbar.", "Помощь при поломке.", "Breakdown assistance.", "Допомога при поломці.", "Assistance panne.", "Arıza yardımı.")
    if "wohnmobil" in dl:
        return _n("Stellplatz für Wohnmobile.", "Стоянка для автодомов.", "Motorhome site.", "Стоянка для будинків на колесах.", "Aire camping-cars.", "Karavan alanı.")
    if "richtgeschwindigkeit" in dl:
        return _n("Richtgeschwindigkeit — empfohlene, nicht Höchstgeschwindigkeit.", "Рекомендуемая скорость — не лимит.", "Advisory speed — not a limit.", "Рекомендована швидкість.", "Vitesse conseillée.", "Tavsiye edilen hız.")
    if "mautpflicht" in dl:
        if "ende" in dl:
            return _n("Ende Mautpflicht.", "Конец платного участка.", "End toll section.", "Кінець платної ділянки.", "Fin péage.", "Ücretli yol sonu.")
        return _n("Mautpflicht — Gebühr entrichten.", "Платный участок — оплатите.", "Toll required.", "Платна ділянка.", "Péage obligatoire.", "Ücret gerekli.")
    if code == "392" or "zollstelle" in dl:
        return _n("Zollstelle — anhalten und Zollvorschriften beachten.", "Таможня — остановитесь.", "Customs — stop and comply.", "Митниця — зупиніться.", "Douane — arrêtez-vous.", "Gümrük — durun.")
    if "laternenring" in dl:
        return _n("Laternenring — Orientierungshilfe in der Stadt.", "Кольцо фонарей — ориентир.", "Lantern ring — city landmark.", "Кільце ліхтарів.", "Anneau de lanternes.", "Fener halkası.")
    if code.startswith("405") or code.startswith("406"):
        return _n("Autobahn-Knotenpunkt/Nummer — Orientierung auf der Autobahn.", "Узел/номер автобана.", "Motorway junction/number.", "Вузол автобану.", "Jonction autoroute.", "Otoyol kavşağı.")
    if code == "410" or "europastraßen" in dl:
        return _n("Europastraße — Teil des internationalen Straßennetzes.", "Европейская дорога.", "European route.", "Європейська дорога.", "Route européenne.", "Avrupa yolu.")
    if "ankündigungstafel" in dl:
        return _n("Ankündigungstafel — kündigt Wegweiser/Ausfahrt an.", "Предварительная табличка.", "Advance announcement panel.", "Попередня табличка.", "Panneau d'annonce.", "Ön duyuru paneli.")
    if code.startswith("453") or "entfernungstafel" in dl:
        return _n("Entfernungstafel — zeigt Entfernungen zu Zielen.", "Табличка расстояний.", "Distance panel.", "Табличка відстаней.", "Panneau de distances.", "Mesafe paneli.")
    if "planskizze" in dl:
        return _n("Planskizze — vereinfachter Straßenplan zur Orientierung.", "Схема дороги.", "Road layout sketch.", "Схема дороги.", "Plan simplifié.", "Yol planı.")
    if "schwierige verkehrsführung" in dl:
        return _n("Schwierige Verkehrsführung — besonders aufmerksam fahren.", "Сложная организация движения.", "Difficult traffic routing.", "Складна організація руху.", "Circulation difficile.", "Zor trafik düzeni.")
    if "absperrschranke" in dl or "sperrpfosten" in dl:
        return _n("Absperrung — nicht passieren.", "Преграда — не проезжать.", "Barrier — do not pass.", "Перегородження — не проїжджати.", "Barrière — ne pas passer.", "Bariyer — geçmeyin.")
    if "leitpfosten" in dl:
        return _n("Leitpfosten — markiert Fahrbahnrand.", "Направляющий столбик.", "Guide post — marks road edge.", "Направляючий стовпчик.", "Poteau guide.", "Yönlendirme direği.")
    if code == "353" or ("einbahnstraße" in dl and "angeordnet" in dl):
        return _n("Einbahnstraße — nur in Pfeilrichtung fahren.", "Одностороннее движение — только по стрелке.", "One-way street — follow arrow direction.", "Односторонній рух — лише за стрілкою.", "Sens unique — sens de la flèche.", "Tek yön — ok yönünde.")
    if code == "450" or de.lower() == "white":
        return _n("Leerzeichen/Platzhalter — Bedeutung ergibt sich aus Kontext oder Zusatzzeichen.",
                  "Пустой/белый знак — значение из контекста или дополнительных табличек.", "Blank/white sign — meaning from context or supplementary plates.",
                  "Порожній знак — значення з контексту.", "Panneau vierge — sens selon contexte.", "Boş levha — anlam bağlamdan.")
    if code == "721" or "grünpfeil" in dl:
        return _n("Grünpfeil nur für Radverkehr — rechts abbiegen bei Rot erlaubt, wenn frei und Fußgänger nicht gefährdet.",
                  "Зелёная стрелка для велосипедов — поворот направо на красный, если свободно.", "Green arrow for cyclists — right on red if clear.",
                  "Зелена стрілка для велосипедистів — праворуч на червоний, якщо вільно.", "Flèche verte cyclistes — à droite au rouge si libre.", "Bisikletliler için yeşil ok — kırmızıda sağa, mümkünse.")
    return None


def _additional_handler(sign: dict) -> dict[str, str] | None:
    de = sign["de"]
    dl = de.lower()
    if "lastenfahrrad" in dl or "fahrrad zum transport" in dl:
        return _n("Lastenfahrräder sind von der Beschränkung ausgenommen.",
                  "Грузовые велосипеды освобождены от ограничения.", "Cargo bikes exempt.",
                  "Вантажні велосипеди звільнені.", "Vélos cargos exemptés.", "Kargo bisikletler muaftır.")
    m = re.search(r"(\d+)\s*taxis?", dl)
    if m:
        n = m.group(1)
        return _n(
            f"Nur {n} Taxis dürfen gleichzeitig an der Haltestelle warten.",
            f"Одновременно на стоянке может ждать только {n} такси.",
            f"Only {n} taxis may wait at the stand at once.",
            f"Одночасно може чекати лише {n} таксі.",
            f"Seuls {n} taxis peuvent attendre.",
            f"Aynı anda yalnızca {n} taksi bekleyebilir.",
        )
    return None


def explain_sign(sign: dict) -> dict[str, str]:
    """Return notes dict with keys de, ru, en, uk, fr, tr."""
    category = sign.get("category", "")

    for handler in (
        _additional_handler,
        _priority_handler,
        _mandatory_handler,
        _prohibitory_handler,
        _warning_handler,
        _bake_handler,
        _info_handler,
    ):
        result = handler(sign)
        if result:
            return result

    if category != "information":
        for extra in (_panel_sign, _wegweiser):
            result = extra(sign)
            if result:
                return result

    if "aufstellung" in sign["de"].lower():
        hk = _hazard_key(sign["de"]) or "gefahrstelle"
        if hk in HAZARD_ADVICE:
            return _vorbauweiser(sign, hk)

    return _category_fallback(category)

