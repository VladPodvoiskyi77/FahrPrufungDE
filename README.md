# FahrPrufung DE

**iOS app for preparing for the German practical driving exam (Prüfungsfahrt).**

Helps newcomers learn exam vocabulary, examiner phrases, and official StVO road signs — with flashcards, quizzes, and progress tracking.

[![Platform](https://img.shields.io/badge/iOS-17%2B-blue)](https://developer.apple.com/ios/)
[![Swift](https://img.shields.io/badge/Swift-5.9-orange)](https://swift.org)
[![SwiftUI](https://img.shields.io/badge/SwiftUI-5.9-blue)](https://developer.apple.com/xcode/swiftui/)

**Live on the App Store** · Bundle ID: `de.fahrprufung.app`

---

## About

FahrPrufung DE is an educational iOS app built for people preparing for the **practical driving test in Germany**. The exam is conducted in German; this app bridges the language gap with structured learning content in **5 UI languages** (Russian, English, Ukrainian, French, Turkish).

German is always the source language (terms, signs, examiner phrases). Translations help users understand what they will hear and see on test day.

## Features

- **386 vocabulary terms** across 14 categories (vehicle controls, safety checks, manoeuvres, examiner phrases, traffic rules)
- **556 official StVO road signs** with search, category filters, and detailed explanations
- **Flashcards** — flip German ↔ translation, mark terms as known
- **Quiz mode** — up to 10 questions per session with answer review
- **Examiner phrases** — grouped by context (directions, manoeuvres, safety, results) with German text-to-speech
- **Progress tracking** — known terms/signs, category breakdown, study streak, quiz history
- **Onboarding** — language selection and feature overview
- **Custom in-app localization** — UI language independent of system locale

## Tech Stack

| Layer | Technology |
|-------|------------|
| UI | SwiftUI |
| Architecture | MVVM + Coordinator pattern |
| Navigation | `NavigationStack`, tab-based shell |
| Localization | SwiftGen (`L10n`) + 6 `.lproj` bundles |
| Data | Bundled JSON + `UserDefaults` |
| Analytics | Firebase Analytics |
| Speech | `AVSpeechSynthesizer` (de-DE) |

The app uses a custom **"Open Road"** design system — brand colors, rounded typography, and card-based layout.

## Repository Structure

```
FahrPrufungDE/
└── IOS/
    ├── FahrPrufungDE/              # SwiftUI source code
    ├── FahrPrufungDE.xcodeproj     # Xcode project
    ├── scripts/                    # Content generation tools
    ├── docs/                       # App Store & privacy docs
    └── signs-svg/                  # SVG sources (not bundled in app)
```

## Content

| Asset | Count | Description |
|-------|-------|-------------|
| `vocabulary.json` | 386 terms | 14 categories, 5 translation languages |
| `signs.json` | 556 signs | Official StVO names (VzKat), 5 categories |
| `Signs/*.png` | 556 images | Rendered sign previews |

Sign graphics are based on Wikimedia Commons / PD-VzKat sources.

## UI Languages

`ru` · `en` · `uk` · `fr` · `tr`

German is exam content only, not a UI language.

## Getting Started

```bash
open IOS/FahrPrufungDE.xcodeproj
```

1. Open the project in Xcode
2. Select your Development Team in **Signing & Capabilities**
3. Run (⌘R)

Regenerate localization after editing `Localizable.strings`:

```bash
cd IOS && swiftgen config run
```

## Screens

| Home | Categories | Flashcards | Quiz | Signs | Progress |
|------|------------|------------|------|-------|----------|
| Hero + quick actions | 14 topic groups | Flip cards | 4-choice quiz | StVO catalog | Streak + history |

## Author

**Vlad Podvoiskyi** — iOS developer

Also on the App Store: [PrapoDe](https://apps.apple.com/app/id6758207550) (German prepositions — A1 to C1)

## License

Educational project. Sign images: Wikimedia Commons / public domain (PD-VzKat). App content and code © Vlad Podvoiskyi.
