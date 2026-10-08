# Android Play Store screenshots

Generated marketing screenshots mirroring the iOS App Store set (active-use state, per language).

## Layout

- `en|ru|uk|fr|tr/raw/` — emulator screencaps
- `en|ru|uk|fr|tr/framed/` — framed 1242×2688 assets with localized headlines (same texts as Desktop `скрины с описанием`)
- `play-listing/{lang}/phone-01.png` … `phone-08.png` — ready to upload to Google Play

## Screens (order)

1. Home
2. Flashcards
3. Quiz
4. Signs list
5. Sign detail
6. Progress
7. Examiner phrases
8. Settings

## Regenerate

```bash
# Emulator running, debug build installed
cd Android
./gradlew installDebug
python3 -u tools/capture_store_screenshots.py
```

Uses debug intent extras `seed_screenshots` / `lang` / `open_route` (see `ScreenshotSeed`).
