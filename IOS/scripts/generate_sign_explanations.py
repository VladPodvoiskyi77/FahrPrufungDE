#!/usr/bin/env python3
"""Generate learner-friendly sign explanations (notes) in de/ru/en/uk/fr/tr.

Explanations are rule-based from StVO code + German title, then translated
with a driving glossary. Re-run safe: overwrites notes only.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SIGNS_PATH = ROOT / "FahrPrufungDE" / "Resources" / "signs.json"
TARGETS = ("ru", "en", "uk", "fr", "tr")

# Multilingual templates keyed by explanation id
TEMPLATES: dict[str, dict[str, str]] = {
    "stop_give_way": {
        "de": "Vollständig anhalten, dann anderen Verkehrsteilnehmern Vorfahrt gewähren.",
        "ru": "Полная остановка у линии знака, затем уступить дорогу другим участникам движения.",
        "en": "Come to a complete stop, then give way to other road users.",
        "uk": "Повна зупинка біля знака, потім дайте дорогу іншим учасникам руху.",
        "fr": "Arrêt complet, puis cédez le passage aux autres usagers.",
    },
    "give_way": {
        "de": "Anderen Verkehrsteilnehmern Vorfahrt gewähren — nicht zwingend anhalten, wenn frei.",
        "ru": "Уступите дорогу — останавливаться обязательно только если мешает другой транспорт.",
        "en": "Give way to other traffic — stop only if needed.",
        "uk": "Дайте дорогу — зупиняйтесь лише якщо заважає інший транспорт.",
        "fr": "Cédez le passage — arrêtez-vous seulement si nécessaire.",
    },
    "priority_road": {
        "de": "Sie befinden sich auf einer Vorfahrtstraße — Sie haben Vorfahrt an Kreuzungen.",
        "ru": "Вы на главной дороге — у вас преимущество на перекрёстках.",
        "en": "You are on a priority road — you have right of way at intersections.",
        "uk": "Ви на головній дорозі — у вас перевага на перехрестях.",
        "fr": "Route prioritaire — vous avez la priorité aux intersections.",
    },
    "end_priority": {
        "de": "Ende der Vorfahrtstraße — ab hier gelten normale Vorfahrtsregeln.",
        "ru": "Конец главной дороги — дальше действуют обычные правила приоритета.",
        "en": "End of priority road — normal priority rules apply ahead.",
        "uk": "Кінець головної дороги — далі звичайні правила пріоритету.",
        "fr": "Fin de route prioritaire — règles normales de priorité ensuite.",
    },
    "priority_next": {
        "de": "An der nächsten Kreuzung haben Sie Vorfahrt.",
        "ru": "На следующем перекрёстке у вас преимущество проезда.",
        "en": "You have priority at the next intersection.",
        "uk": "На наступному перехресті у вас перевага.",
        "fr": "Priorité à la prochaine intersection.",
    },
    "mandatory_left": {
        "de": "Pflichtzeichen: An dieser Stelle müssen Sie nach links fahren.",
        "ru": "Обязательный знак: здесь разрешено/требуется движение только налево.",
        "en": "Mandatory: you must go/turn left here.",
        "uk": "Обов'язковий знак: тут дозволено/потрібно рух лише ліворуч.",
        "fr": "Obligatoire : vous devez tourner/partir à gauche ici.",
    },
    "mandatory_right": {
        "de": "Pflichtzeichen: An dieser Stelle müssen Sie nach rechts fahren.",
        "ru": "Обязательный знак: здесь разрешено/требуется движение только направо.",
        "en": "Mandatory: you must go/turn right here.",
        "uk": "Обов'язковий знак: тут дозволено/потрібно рух лише праворуч.",
        "fr": "Obligatoire : vous devez tourner/partir à droite ici.",
    },
    "mandatory_straight": {
        "de": "Pflichtzeichen: Nur geradeaus fahren.",
        "ru": "Обязательный знак: движение только прямо.",
        "en": "Mandatory: straight ahead only.",
        "uk": "Обов'язковий знак: рух лише прямо.",
        "fr": "Obligatoire : tout droit uniquement.",
    },
    "one_way_left": {
        "de": "Einbahnstraße — Verkehr nur in Pfeilrichtung (hier: links).",
        "ru": "Одностороннее движение — ехать только в направлении стрелки (здесь: налево).",
        "en": "One-way street — traffic flows in arrow direction (here: left).",
        "uk": "Односторонній рух — їздити лише за напрямком стрілки (тут: ліворуч).",
        "fr": "Sens unique — circulation dans le sens de la flèche (ici : gauche).",
    },
    "one_way_right": {
        "de": "Einbahnstraße — Verkehr nur in Pfeilrichtung (hier: rechts).",
        "ru": "Одностороннее движение — ехать только в направлении стрелки (здесь: направо).",
        "en": "One-way street — traffic flows in arrow direction (here: right).",
        "uk": "Односторонній рух — їздити лише за напрямком стрілки (тут: праворуч).",
        "fr": "Sens unique — circulation dans le sens de la flèche (ici : droite).",
    },
    "speed_limit": {
        "de": "Höchstgeschwindigkeit — schneller fahren ist verboten.",
        "ru": "Максимальная скорость — ехать быстрее запрещено.",
        "en": "Maximum speed — driving faster is prohibited.",
        "uk": "Максимальна швидкість — їхати швидше заборонено.",
        "fr": "Vitesse maximale — rouler plus vite est interdit.",
    },
    "town_entry": {
        "de": "Ortsbeginn — innerorts gelten andere Geschwindigkeits- und Verkehrsregeln.",
        "ru": "Начало населённого пункта — внутри действуют другие скоростные и дорожные правила.",
        "en": "Town entry — different speed and traffic rules apply inside.",
        "uk": "Початок населеного пункту — всередині інші правила швидкості та руху.",
        "fr": "Entrée d'agglomération — règles de vitesse et de circulation différentes.",
    },
    "town_exit": {
        "de": "Ortsende — außerorts gelten andere Regeln.",
        "ru": "Конец населённого пункта — за городом действуют другие правила.",
        "en": "Town exit — rules outside built-up areas apply.",
        "uk": "Кінець населеного пункту — поза містом інші правила.",
        "fr": "Sortie d'agglomération — règles hors agglomération.",
    },
    "warning_generic": {
        "de": "Warnung vor Gefahr — Geschwindigkeit anpassen und vorsichtig fahren.",
        "ru": "Предупреждение об опасности — снизьте скорость и будьте внимательны.",
        "en": "Warning of hazard — reduce speed and drive carefully.",
        "uk": "Попередження про небезпеку — зменшіть швидкість і будьте обережні.",
        "fr": "Danger — réduisez la vitesse et soyez prudent.",
    },
    "prohibitory_generic": {
        "de": "Verbot — die auf dem Schild angegebene Handlung ist nicht erlaubt.",
        "ru": "Запрет — действие, указанное на знаке, не разрешено.",
        "en": "Prohibition — the action shown is not allowed.",
        "uk": "Заборона — дія, зазначена на знаку, не дозволена.",
        "fr": "Interdiction — l'action indiquée n'est pas autorisée.",
    },
    "info_generic": {
        "de": "Hinweiszeichen — informiert über Straßenverlauf oder Regelung.",
        "ru": "Информационный знак — сообщает о дорожной ситуации или правиле.",
        "en": "Information sign — indicates road layout or a rule.",
        "uk": "Інформаційний знак — повідомляє про дорожню ситуацію або правило.",
        "fr": "Panneau d'information — indique la configuration ou une règle.",
    },
    "zone_generic": {
        "de": "Zonenzeichen — ab hier gelten besondere Regeln in der markierten Zone.",
        "ru": "Зональный знак — с этого места действуют особые правила в обозначенной зоне.",
        "en": "Zone sign — special rules apply within the marked zone from here.",
        "uk": "Зонний знак — від цього місця діють особливі правила в позначеній зоні.",
        "fr": "Panneau de zone — règles particulières dans la zone indiquée.",
    },
}

TR: dict[str, str] = {
    "stop_give_way": "Tam durun, ardından diğer yol kullanıcılarına yol verin.",
    "give_way": "Yol verin — gerekmedikçe durmak zorunda değilsiniz.",
    "priority_road": "Ana yoldasınız — kavşaklarda geçiş önceliğiniz var.",
    "end_priority": "Ana yol sonu — bundan sonra normal geçiş kuralları geçerli.",
    "priority_next": "Bir sonraki kavşakta geçiş önceliğiniz var.",
    "mandatory_left": "Zorunlu işaret: burada yalnızca sola gidilmelidir.",
    "mandatory_right": "Zorunlu işaret: burada yalnızca sağa gidilmelidir.",
    "mandatory_straight": "Zorunlu işaret: yalnızca düz gidin.",
    "one_way_left": "Tek yön — trafik ok yönünde (burada: sola).",
    "one_way_right": "Tek yön — trafik ok yönünde (burada: sağa).",
    "speed_limit": "Azami hız — daha hızlı sürmek yasaktır.",
    "town_entry": "Yerleşim yeri başlangıcı — içeride farklı hız ve trafik kuralları geçerli.",
    "town_exit": "Yerleşim yeri sonu — dışarıda farklı kurallar geçerli.",
    "warning_generic": "Tehlike uyarısı — hızınızı düşürün ve dikkatli sürün.",
    "prohibitory_generic": "Yasak — işarette gösterilen eylem izin verilmez.",
    "info_generic": "Bilgi işareti — yol düzeni veya kural hakkında bilgi verir.",
    "zone_generic": "Bölge işareti — buradan itibaren işaretli bölgede özel kurallar geçerlidir.",
}
for _key, _text in TR.items():
    TEMPLATES[_key]["tr"] = _text


def code_num(code: str) -> int | None:
    m = re.match(r"(\d+)", code.replace("Z", ""))
    return int(m.group(1)) if m else None


def pick_template(sign: dict) -> dict[str, str]:
    code = (sign.get("stvo_code") or "").removeprefix("Z")
    de = sign["de"].lower()
    n = code_num(code)

    if code in ("206",) or "halt" in de and "vorfahrt" in de:
        return TEMPLATES["stop_give_way"]
    if code in ("205",) or de.startswith("vorfahrt gewähren"):
        return TEMPLATES["give_way"]
    if code in ("306",) or "vorfahrtstraße" in de and "ende" not in de:
        return TEMPLATES["priority_road"]
    if code in ("307",) or "ende der vorfahrtstraße" in de:
        return TEMPLATES["end_priority"]
    if code in ("301",) or de == "vorfahrt":
        return TEMPLATES["priority_next"]
    if "hier links" in de or code.startswith("211") and "links" in de:
        return TEMPLATES["mandatory_left"]
    if "hier rechts" in de or code.startswith("211") and "rechts" in de:
        return TEMPLATES["mandatory_right"]
    if "geradeaus" in de or code.startswith("209"):
        return TEMPLATES["mandatory_straight"]
    if "einbahn" in de and "links" in de:
        return TEMPLATES["one_way_left"]
    if "einbahn" in de and "rechts" in de:
        return TEMPLATES["one_way_right"]
    if (
        "zone" in de
        or "bereich" in de and any(x in de for x in ("taxi", "lade", "beginn", "ende"))
        or re.fullmatch(r"244\.[234]", code)
        or re.fullmatch(r"242\.1", code)
        or re.fullmatch(r"274\.[12](?:-\d+)?", code)
        or re.fullmatch(r"270\.[12]", code)
        or re.fullmatch(r"290\.[12]", code)
    ):
        return TEMPLATES["zone_generic"]
    if n and 274 <= n <= 278 or "höchstgeschwindigkeit" in de or "geschwindigkeit" in de and "zulässig" in de:
        return TEMPLATES["speed_limit"]
    if code in ("310",) or "ortstafel vorderseite" in de:
        return TEMPLATES["town_entry"]
    if code in ("311",) or "ortstafel rückseite" in de:
        return TEMPLATES["town_exit"]
    if sign.get("category") == "warning" or (n and 100 <= n <= 151):
        return TEMPLATES["warning_generic"]
    if sign.get("category") in ("prohibitory", "prohibition"):
        return TEMPLATES["prohibitory_generic"]
    return TEMPLATES["info_generic"]


def explain_sign(sign: dict) -> dict[str, str]:
    tpl = pick_template(sign)
    de_extra = sign["de"].strip().rstrip(".")

    if tpl is TEMPLATES["warning_generic"] and de_extra:
        return {
            "de": f"Warnung: {de_extra}. Geschwindigkeit anpassen und vorsichtig fahren.",
            "ru": f"Предупреждение: {sign['ru']}. Снизьте скорость и будьте внимательны.",
            "en": f"Warning: {sign['en']}. Reduce speed and drive carefully.",
            "uk": f"Попередження: {sign['uk']}. Зменшіть швидкість і будьте обережні.",
            "fr": f"Avertissement : {sign['fr']}. Réduisez la vitesse et soyez prudent.",
            "tr": f"Uyarı: {sign.get('tr', sign['de'])}. Hızınızı düşürün ve dikkatli sürün.",
        }
    if tpl is TEMPLATES["prohibitory_generic"] and de_extra:
        return {
            "de": f"Verbot: {de_extra}.",
            "ru": f"Запрет: {sign['ru']}.",
            "en": f"Prohibited: {sign['en']}.",
            "uk": f"Заборона: {sign['uk']}.",
            "fr": f"Interdit : {sign['fr']}.",
            "tr": f"Yasak: {sign.get('tr', sign['de'])}.",
        }
    if tpl is TEMPLATES["info_generic"] and de_extra:
        return {
            "de": f"Hinweis: {de_extra}.",
            "ru": f"Информация: {sign['ru']}.",
            "en": f"Information: {sign['en']}.",
            "uk": f"Інформація: {sign['uk']}.",
            "fr": f"Information : {sign['fr']}.",
            "tr": f"Bilgi: {sign.get('tr', sign['de'])}.",
        }
    if tpl is TEMPLATES["zone_generic"] and de_extra:
        return {
            "de": f"Zonenzeichen: {de_extra}. In der Zone gelten besondere Verkehrsregeln.",
            "ru": f"Зональный знак: {sign['ru']}. В зоне действуют особые правила движения.",
            "en": f"Zone sign: {sign['en']}. Special traffic rules apply within the zone.",
            "uk": f"Зонний знак: {sign['uk']}. У зоні діють особливі правила руху.",
            "fr": f"Panneau de zone : {sign['fr']}. Des règles particulières s'appliquent dans la zone.",
            "tr": f"Bölge işareti: {sign.get('tr', sign['de'])}. Bölgede özel trafik kuralları geçerlidir.",
        }
    return dict(tpl)


def main() -> None:
    data = json.loads(SIGNS_PATH.read_text(encoding="utf-8"))
    for i, sign in enumerate(data["signs"], 1):
        sign["notes"] = explain_sign(sign)
        if i % 50 == 0:
            print(f"  … {i}")
            SIGNS_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    data.setdefault("meta", {})["has_explanations"] = True
    SIGNS_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Done: {len(data['signs'])} explanations")


if __name__ == "__main__":
    main()
