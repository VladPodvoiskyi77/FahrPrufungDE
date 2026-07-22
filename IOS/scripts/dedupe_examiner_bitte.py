#!/usr/bin/env python3
"""Remove examiner phrases that duplicate a Bitte variant (keep polite form)."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VOCAB_PATH = ROOT / "FahrPrufungDE" / "Resources" / "vocabulary.json"

# Without Bitte → keep the Bitte variant (same instruction, polite form preferred).
MANUAL_REMOVE: dict[str, str] = {
    "phrase_geradeaus_fahren": "phrase_bitte_geradeaus",
    "phrase_biegen_links": "phrase_links_kreuzung",
    "phrase_biegen_rechts": "phrase_rechts_kreuzung",
    "phrase_licht_ein": "phrase_abblendlicht_ein",
    "phrase_parken_rueckwaerts": "phrase_rueckwaerts_links",
    "phrase_parken_vorwaerts": "phrase_vorwaerts_links",
}


def norm_without_bitte(text: str) -> str:
    text = text.lower().strip().rstrip(".!?")
    text = re.sub(r"\bbitte\b", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def has_bitte(text: str) -> bool:
    return bool(re.search(r"\bbitte\b", text, re.I))


def main() -> None:
    with open(VOCAB_PATH, encoding="utf-8") as f:
        data = json.load(f)

    by_id = {t["id"]: t for t in data["terms"]}
    remove_ids: set[str] = set(MANUAL_REMOVE)

    examiner = [t for t in data["terms"] if "examiner" in t.get("tags", [])]
    by_norm: dict[str, list[dict]] = {}
    for t in examiner:
        by_norm.setdefault(norm_without_bitte(t["de"]), []).append(t)

    for items in by_norm.values():
        if len(items) < 2:
            continue
        with_bitte = [t for t in items if has_bitte(t["de"])]
        without_bitte = [t for t in items if not has_bitte(t["de"])]
        if with_bitte and without_bitte:
            for t in without_bitte:
                remove_ids.add(t["id"])

    removed = []
    for rid in sorted(remove_ids):
        if rid not in by_id:
            continue
        keep = MANUAL_REMOVE.get(rid)
        removed.append((rid, by_id[rid]["de"], keep))

    data["terms"] = [t for t in data["terms"] if t["id"] not in remove_ids]
    data["meta"]["term_count"] = len(data["terms"])

    with open(VOCAB_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    examiner_count = sum(1 for t in data["terms"] if "examiner" in t.get("tags", []))
    print(f"Removed {len(removed)} examiner phrase(s):")
    for rid, de, keep in removed:
        keep_de = by_id[keep]["de"] if keep and keep in by_id else "—"
        print(f"  - {rid}: {de}")
        if keep:
            print(f"    kept: {keep}: {keep_de}")
    print(f"Examiner phrases: {examiner_count}")
    print(f"term_count → {data['meta']['term_count']}")


if __name__ == "__main__":
    main()
