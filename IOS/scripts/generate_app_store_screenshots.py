#!/usr/bin/env python3
"""Compose App Store marketing screenshots (batch) — matches docs example style."""

from __future__ import annotations

import glob
import re
from pathlib import Path

from make_app_store_screenshot import compose

# App Store 6.5" — scale layout from 1290×2796 reference
APP_STORE_W = 1242
APP_STORE_H = 2688

ROOT = Path("/Users/test/Desktop/FahrPrüfung De/Screens")

TEXTS: dict[str, list[str]] = {
    "ru": [
        "Всё для экзамена в одном приложении",
        "Учите термины быстро",
        "Проверяйте свои знания",
        "Все официальные знаки StVO",
        "Понимайте не только название, но и смысл знака",
        "Следите за своим прогрессом",
        "Понимайте ключевые фразы на экзамене",
        "Учитесь на удобном для вас языке",
    ],
    "en": [
        "Everything for the exam in one app",
        "Learn terms quickly",
        "Test your knowledge",
        "All official StVO signs",
        "Understand not just the name, but the meaning of each sign",
        "Track your progress",
        "Understand key phrases on the exam",
        "Learn in the language that suits you",
    ],
    "uk": [
        "Усе для іспиту в одному застосунку",
        "Вивчайте терміни швидко",
        "Перевіряйте свої знання",
        "Усі офіційні знаки StVO",
        "Розумійте не лише назву, а й сенс знака",
        "Слідкуйте за своїм прогресом",
        "Розумійте ключові фрази на іспиті",
        "Навчайтесь зручною для вас мовою",
    ],
    "fr": [
        "Tout pour l'examen dans une seule app",
        "Apprenez le vocabulaire rapidement",
        "Testez vos connaissances",
        "Tous les panneaux officiels StVO",
        "Comprenez non seulement le nom, mais le sens du panneau",
        "Suivez vos progrès",
        "Comprenez les phrases clés à l'examen",
        "Apprenez dans la langue qui vous convient",
    ],
    "tr": [
        "Sınav için her şey tek uygulamada",
        "Terimleri hızlı öğrenin",
        "Bilginizi test edin",
        "Tüm resmî StVO işaretleri",
        "Yalnızca adı değil, işaretin anlamını da anlayın",
        "İlerlemenizi takip edin",
        "Sınavdaki temel ifadeleri anlayın",
        "Size uygun dilde öğrenin",
    ],
}


def screen_index(filename: str) -> int:
    m = re.match(r"(\d+)", filename)
    if not m:
        raise ValueError(f"Cannot parse index from {filename}")
    return int(m.group(1))


def main() -> None:
    total = 0
    for lang, texts in TEXTS.items():
        src_dir = ROOT / lang / "просто скрины"
        out_dir = ROOT / lang / "скрины с описанием"
        out_dir.mkdir(parents=True, exist_ok=True)

        for path in sorted(glob.glob(str(src_dir / "*.png"))):
            p = Path(path)
            idx = screen_index(p.name) - 1
            out_path = out_dir / p.name
            compose(
                screenshot=p,
                output=out_path,
                headline=texts[idx],
                subtitle="",
                canvas_w=APP_STORE_W,
                canvas_h=APP_STORE_H,
            )
            total += 1
            print(f"✓ {lang}/{out_path.name}")

    print(f"\nDone: {total} screenshots (style: docs/app-store-screenshots/01-signs-example.png)")


if __name__ == "__main__":
    main()
