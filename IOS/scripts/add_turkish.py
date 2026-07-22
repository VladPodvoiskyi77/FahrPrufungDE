#!/usr/bin/env python3
"""Add Turkish (tr) translations to vocabulary.json and signs.json."""

from __future__ import annotations

import json
import time
from pathlib import Path

from deep_translator import GoogleTranslator

ROOT = Path(__file__).resolve().parent.parent
RESOURCES = ROOT / "FahrPrufungDE" / "Resources"

TITLE_GLOSSARY: dict[str, str] = {
    "Halt. Vorfahrt gewähren.": "Dur. Yol ver.",
    "Vorfahrt gewähren.": "Yol ver",
    "Vorfahrt": "Sonraki kavşakta geçiş önceliği",
    "Vorfahrtstraße": "Ana yol",
    "Vorgeschriebene Fahrtrichtung – hier links": "Zorunlu yön — burada sola",
    "Vorgeschriebene Fahrtrichtung – hier rechts": "Zorunlu yön — burada sağa",
    "Ende der Vorfahrtstraße": "Ana yol sonu",
    "Ortstafel Vorderseite": "Yerleşim yeri başlangıcı",
    "Ortstafel Rückseite": "Yerleşim yeri sonu",
    "Einbahnstraße, linksweisend": "Tek yön (sola)",
    "Einbahnstraße, rechtsweisend": "Tek yön (sağa)",
}


def translate_batch(texts: list[str]) -> list[str]:
    translator = GoogleTranslator(source="de", target="tr")
    out: list[str] = []
    for text in texts:
        try:
            out.append(translator.translate(text) or text)
            time.sleep(0.05)
        except Exception:
            out.append(text)
    return out


def add_tr_to_vocabulary() -> None:
    path = RESOURCES / "vocabulary.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    langs = data.setdefault("languages", [])
    if "tr" not in langs:
        langs.append("tr")

    pending_cats = [c for c in data["categories"] if "tr" not in c]
    if pending_cats:
        translated = translate_batch([c["de"] for c in pending_cats])
        for cat, tr in zip(pending_cats, translated):
            cat["tr"] = tr.strip().rstrip(".")
        print(f"vocabulary categories: +{len(pending_cats)} tr")

    pending_terms = [t for t in data["terms"] if "tr" not in t]
    print(f"vocabulary terms to translate: {len(pending_terms)}")
    batch_size = 40
    for i in range(0, len(pending_terms), batch_size):
        batch = pending_terms[i : i + batch_size]
        for term in batch:
            if term["de"] in TITLE_GLOSSARY:
                term["tr"] = TITLE_GLOSSARY[term["de"]]
        to_mt = [t for t in batch if "tr" not in t]
        if to_mt:
            translated = translate_batch([t["de"] for t in to_mt])
            for term, tr in zip(to_mt, translated):
                term["tr"] = tr.strip().rstrip(".")
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"  … {min(i + batch_size, len(pending_terms))} terms")

    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def add_tr_to_signs() -> None:
    path = RESOURCES / "signs.json"
    data = json.loads(path.read_text(encoding="utf-8"))

    for cat in data.get("categories", []):
        if "tr" not in cat:
            cat["tr"] = translate_batch([cat["de"]])[0].strip().rstrip(".")

    pending = [s for s in data["signs"] if "tr" not in s]
    print(f"signs to translate: {len(pending)}")
    batch_size = 30
    for i in range(0, len(pending), batch_size):
        batch = pending[i : i + batch_size]
        for sign in batch:
            if sign["de"] in TITLE_GLOSSARY:
                sign["tr"] = TITLE_GLOSSARY[sign["de"]]
        to_mt = [s for s in batch if "tr" not in s]
        if to_mt:
            translated = translate_batch([s["de"] for s in to_mt])
            for sign, tr in zip(to_mt, translated):
                sign["tr"] = tr.strip().rstrip(".")
        if (i + batch_size) % 150 == 0 or i + batch_size >= len(pending):
            path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"  … {min(i + batch_size, len(pending))} signs")

    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> None:
    add_tr_to_vocabulary()
    add_tr_to_signs()
    print("Done")


if __name__ == "__main__":
    main()
