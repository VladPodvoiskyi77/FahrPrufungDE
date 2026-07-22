# FahrPrufung DE

Подготовка к **практическому экзамену** (Fahrprüfung) в Германии — словарь, фразы экзаменатора, знаки StVO, карточки и квиз.

## Структура репозитория

```
FahrPrufungDE/
├── IOS/          # SwiftUI-приложение (App Store)
├── Android/      # Kotlin + Jetpack Compose (Google Play)
└── README.md
```

| Платформа | Путь | Bundle ID |
|-----------|------|-----------|
| iOS | `IOS/FahrPrufungDE.xcodeproj` | `de.fahrprufung.app` |
| Android | `Android/` | `de.fahrprufung.app` |

## Языки интерфейса

`ru` · `en` · `uk` · `fr` · `tr` — немецкий только как учебный контент.

## iOS

```bash
open IOS/FahrPrufungDE.xcodeproj
```

Сборка и публикация: Xcode → Archive. Скрипты и документация — в `IOS/scripts/`, `IOS/docs/`.

## Android

Требования: Android Studio, JDK 17+, Android SDK 35.

```bash
cd Android
export JAVA_HOME="/Applications/Android Studio.app/Contents/jbr/Contents/Home"
./gradlew assembleDebug
```

APK: `Android/app/build/outputs/apk/debug/app-debug.apk`

Открыть в Android Studio: **File → Open → `Android/`**

## Контент

- `vocabulary.json` — 386 терминов, 14 категорий
- `signs.json` + PNG в `assets/Signs/` — 556 знаков

Источник для iOS: `IOS/FahrPrufungDE/Resources/`.  
Для Android: `Android/app/src/main/assets/` (синхронизировать при обновлении контента).

## Фичи (обе платформы)

- Онбординг + выбор языка
- 4 вкладки: Учёба · Знаки · Прогресс · Настройки
- Категории, карточки, квиз (до 10 вопросов)
- Фразы экзаменатора + TTS (de-DE)
- Знаки StVO с поиском и фильтрами
- «Знаю» + отмена, серия дней, история квизов
- Тёмная тема не используется — светлая «Open Road»
