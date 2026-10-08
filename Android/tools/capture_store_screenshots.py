#!/usr/bin/env python3
"""Capture Android Play-Store screenshots for every UI language (deep-link driven)."""

from __future__ import annotations

import shutil
import subprocess
import sys
import time
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "store-screenshots"
IOS_SCRIPT_DIR = ROOT.parent / "IOS" / "scripts"
sys.path.insert(0, str(IOS_SCRIPT_DIR))
from make_app_store_screenshot import compose  # noqa: E402
from generate_app_store_screenshots import TEXTS  # noqa: E402  # same copy as Desktop «скрины с описанием»

PACKAGE = "de.fahrprufung.app"
ACTIVITY = f"{PACKAGE}/.MainActivity"
ADB = shutil.which("adb") or str(Path.home() / "Library/Android/sdk/platform-tools/adb")

LANGS = ["en", "ru", "uk", "fr", "tr"]

# Localized session titles used in deep links (match strings.xml)
TITLES = {
    "en": {
        "top": "Top terms",
        "quiz": "Quiz",
        "examiner": "Examiner phrases",
    },
    "ru": {
        "top": "Топ-слова",
        "quiz": "Викторина",
        "examiner": "Фразы экзаменатора",
    },
    "uk": {
        "top": "Топ-слова",
        "quiz": "Вікторина",
        "examiner": "Фрази екзаменатора",
    },
    "fr": {
        "top": "Mots essentiels",
        "quiz": "Quiz",
        "examiner": "Phrases de l'examinateur",
    },
    "tr": {
        "top": "En önemli kelimeler",
        "quiz": "Quiz",
        "examiner": "Sınav görevlisi ifadeleri",
    },
}

# Match Desktop «скрины с описанием» / iOS store frames (room for headline above phone).
CANVAS_W = 1242
CANVAS_H = 2688
SIGN_DETAIL_ID = "101-11-fu-g-nger-berweg-aufstellung-rechts"


def adb(*args: str, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run([ADB, *args], check=check, capture_output=True, text=True)


def device_serial() -> str:
    out = adb("devices").stdout
    for line in out.splitlines()[1:]:
        parts = line.split()
        if len(parts) >= 2 and parts[1] == "device":
            return parts[0]
    raise RuntimeError("No adb device/emulator in 'device' state")


def sleep(sec: float) -> None:
    time.sleep(sec)


def force_stop() -> None:
    adb("shell", "am", "force-stop", PACKAGE, check=False)
    sleep(0.5)


def app_resumed() -> bool:
    out = adb("shell", "dumpsys", "activity", "activities", check=False).stdout
    # Look for our activity as the resumed/top one.
    for line in out.splitlines():
        if "mResumedActivity" in line or "topResumedActivity" in line:
            if PACKAGE in line:
                return True
    # Fallback: recent task dump
    out2 = adb("shell", "dumpsys", "window", "windows", check=False).stdout
    return PACKAGE in out2 and "mCurrentFocus" in out2 and PACKAGE in "".join(
        ln for ln in out2.splitlines() if "mCurrentFocus" in ln or "mFocusedApp" in ln
    )


def start_app(lang: str, route: str | None = None) -> None:
    force_stop()
    args = [
        "shell",
        "am",
        "start",
        "-W",
        "-n",
        ACTIVITY,
        "--ez",
        "seed_screenshots",
        "true",
        "--es",
        "lang",
        lang,
    ]
    if route:
        args += ["--es", "open_route", route]
    result = adb(*args, check=False)
    if result.returncode != 0:
        print("  ! am start failed:", result.stderr.strip() or result.stdout.strip())

    # Wait until activity is resumed and seed has had time to apply.
    deadline = time.time() + 20
    while time.time() < deadline:
        if app_resumed():
            break
        sleep(0.4)
    else:
        print("  ! app not resumed, retrying launch")
        adb(*args, check=False)
        sleep(3.0)

    # Extra settle for DataStore seed + optional navigation.
    # Examiner screen is heavier to compose after seed.
    if route == "examinerPhrases":
        sleep(6.5)
    elif route:
        sleep(5.0)
    else:
        sleep(3.5)


def screencap(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    # Only capture if app is still foreground; otherwise retry launch once.
    if not app_resumed():
        print(f"  ! not foreground before capture of {path.name}")
    adb("shell", "screencap", "-p", "/sdcard/fp_shot.png")
    adb("pull", "/sdcard/fp_shot.png", str(path))


def enc(title: str) -> str:
    return urllib.parse.quote(title, safe="")


def is_launcher_shot(path: Path) -> bool:
    """Detect Android launcher wallpaper shots (dark navy dominant)."""
    try:
        from PIL import Image
        import collections

        im = Image.open(path)
        colors = collections.Counter(
            im.getpixel((x, y)) for x in range(0, im.width, 50) for y in range(0, im.height, 50)
        )
        top, count = colors.most_common(1)[0]
        # Launcher wallpaper is near (15,15,25); app cream is ~ (255,252,247) or teal headers.
        if top[0] < 40 and top[1] < 40 and top[2] < 50 and count > 200:
            return True
        if path.stat().st_size > 1_200_000 and top[0] < 40:
            return True
        return False
    except Exception:
        return False


def capture_lang(lang: str) -> None:
    t = TITLES[lang]
    raw_dir = OUT / lang / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    print(f"\n=== {lang} ===", flush=True)

    shots = [
        ("01-home.png", None),
        ("02-flashcards.png", f"flashcards/core/{enc(t['top'])}"),
        ("03-quiz.png", f"quiz/core/{enc(t['quiz'])}"),
        ("04-signs.png", "signsList"),
        ("05-sign-detail.png", f"signDetail/{enc(SIGN_DETAIL_ID)}"),
        ("06-progress.png", "progress"),
        ("07-examiner.png", "examinerPhrases"),
        ("08-settings.png", "settings"),
    ]

    for name, route in shots:
        for attempt in range(2):
            start_app(lang, route)
            # For quiz, tap a couple answers to look mid-session
            if name.startswith("03-"):
                for _ in range(3):
                    adb("shell", "input", "tap", "540", "1100", check=False)
                    sleep(0.4)
                    adb("shell", "input", "tap", "540", "1650", check=False)
                    sleep(0.5)
            # For flashcards, flip once
            if name.startswith("02-"):
                adb("shell", "input", "tap", "540", "1000", check=False)
                sleep(0.5)
            out = raw_dir / name
            screencap(out)
            if is_launcher_shot(out) and attempt == 0:
                print(f"  retry {name} (launcher detected)", flush=True)
                continue
            print(f"  ✓ {name} ({out.stat().st_size // 1024} KB)", flush=True)
            break


def frame_all() -> None:
    total = 0
    for lang, texts in TEXTS.items():
        raw_dir = OUT / lang / "raw"
        framed_dir = OUT / lang / "framed"
        framed_dir.mkdir(parents=True, exist_ok=True)
        for path in sorted(raw_dir.glob("*.png")):
            idx = int(path.name.split("-", 1)[0]) - 1
            if idx < 0 or idx >= len(texts):
                continue
            out = framed_dir / path.name
            compose(
                screenshot=path,
                output=out,
                headline=texts[idx],
                subtitle="",
                canvas_w=CANVAS_W,
                canvas_h=CANVAS_H,
            )
            total += 1
            print(f"framed {lang}/{out.name}", flush=True)
    print(f"\nFramed {total} → {OUT}", flush=True)


def main() -> None:
    # Unbuffered-ish progress
    sys.stdout.reconfigure(line_buffering=True) if hasattr(sys.stdout, "reconfigure") else None
    print("device:", device_serial(), flush=True)
    if OUT.exists():
        for p in OUT.rglob("*.png"):
            p.unlink()
    OUT.mkdir(parents=True, exist_ok=True)
    for lang in LANGS:
        capture_lang(lang)
    frame_all()
    print("DONE", OUT, flush=True)


if __name__ == "__main__":
    main()
