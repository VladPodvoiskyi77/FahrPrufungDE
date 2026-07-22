# FahrPrufungDE

iOS app for newcomers in Germany preparing for the practical driving exam (Prüfungsfahrt).

## Languages

- **German** (always shown) — with article (der/die/das)
- **Translation:** Russian, English, Ukrainian, French, Turkish
- UI strings live in `FahrPrufungDE/Resources/Localization/{de,ru,en,uk,fr,tr}.lproj/Localizable.strings` and are accessed through SwiftGen (`L10n`). The language is selected in-app (not the system locale) via a custom lookup in `LocalizationManager`.

## Architecture

MVVM + Coordinator (SwiftUI):

| Layer | Location |
|-------|----------|
| Models (one type per file) | `FahrPrufungDE/Models/` |
| ViewModels (one per screen) | `FahrPrufungDE/ViewModels/` |
| Coordinators (`AppCoordinator`, `LearnCoordinator`, `SignsCoordinator` with `NavigationPath`) | `FahrPrufungDE/Coordinators/` |
| Views (thin, no business logic) | `FahrPrufungDE/Views/` |
| Services (`DataStore`, `LocalizationManager`, `SignImageLoader`) | `FahrPrufungDE/Services/` |
| Generated code (SwiftGen `L10n`) | `FahrPrufungDE/Generated/` |

Regenerate `L10n.swift` after editing `Localizable.strings`:

```bash
swiftgen config run
```

## Data

| File | Description |
|------|-------------|
| `FahrPrufungDE/Resources/vocabulary.json` | 239+ terms, 14 categories |
| `FahrPrufungDE/Resources/signs.json` | StVO signs (DE/RU/EN/UK/FR/TR), official VzKat names |
| `signs-svg/` | SVG source (Wikimedia Commons, PD-VzKat) — not bundled in app |
| `FahrPrufungDE/Resources/Signs/` | PNG previews only (rendered via rsvg-convert) |

### Scripts

```bash
python3 scripts/generate_vocabulary.py        # regenerate vocabulary.json

python3 scripts/restore_from_bildtafel.py     # import missing signs (names + SVG) from Wikipedia Bildtafel
python3 scripts/download_missing_svgs.py      # retry failed SVG downloads only
python3 scripts/clean_catalog.py              # fix junk titles / drop sketches from signs.json
python3 scripts/generate_sign_pngs.py         # render PNGs from SVG (requires: brew install librsvg)
python3 scripts/add_turkish.py                 # add Turkish to vocabulary.json + signs.json
python3 scripts/translate_signs.py            # translate sign names de → ru/en/uk/fr/tr
```

## Open in Xcode

```bash
open FahrPrufungDE.xcodeproj
```

Select your Development Team in Signing & Capabilities, then Run (⌘R).

## MVP features

- Category browser
- Flashcards (tap to flip)
- Quiz (multiple choice)
- Core terms & examiner phrases shortcuts
- Traffic sign catalog with search and category filter
- Native language picker in Settings & onboarding

## Roadmap

- [ ] Rule explanations per sign
- [ ] Turkish localization
- [ ] German TTS pronunciation
- [ ] Spaced repetition
- [ ] Android (Flutter / Kotlin)
