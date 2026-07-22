# TestFlight — Fahrprufung DE

Пошаговая инструкция для первой загрузки в TestFlight.

## Предварительно

- [ ] Apple Developer Program активен
- [ ] Bundle ID `de.fahrprufung.app` зарегистрирован в [Certificates, Identifiers & Profiles](https://developer.apple.com/account/resources/identifiers/list)
- [ ] В Xcode → Signing & Capabilities: Team **28QWPQX3PF**, Automatic signing
- [ ] Privacy Policy URL опубликован (для финального релиза; для TestFlight не обязателен)

## 1. App Store Connect

1. [App Store Connect](https://appstoreconnect.apple.com) → **My Apps** → **+** → New App
2. Platform: **iOS**
3. Name: **Fahrprufung DE**
4. Primary Language: **German** (или English)
5. Bundle ID: **de.fahrprufung.app**
6. SKU: `fahrprufung-de` (любой уникальный идентификатор)

## 2. Archive в Xcode

1. Откройте `FahrPrufungDE.xcodeproj`
2. Выберите **Any iOS Device (arm64)** (не симулятор)
3. **Product → Archive**
4. В Organizer → **Distribute App**
5. **App Store Connect** → Upload
6. Следуйте мастеру (Automatic signing, Upload symbols)

### Альтернатива: скрипт

```bash
chmod +x scripts/archive-testflight.sh
./scripts/archive-testflight.sh
```

Требуется настроенный signing в Xcode.

## 3. TestFlight

1. App Store Connect → ваше приложение → **TestFlight**
2. Дождитесь обработки билда (5–30 мин, иногда до 1 ч)
3. **Missing Compliance** → обычно «No» для exempt encryption (только HTTPS)
4. **Internal Testing** → добавьте себя как тестера (до 100 человек в команде)
5. Установите **TestFlight** на iPhone → примите приглашение

## 4. Что проверить за 2–3 дня

| Область | Проверка |
|---------|----------|
| Холодный старт | Запуск после force quit |
| Онбординг | Дисклеймер на первом экране |
| Все вкладки | Учить, Знаки, Прогресс, Настройки |
| Карточки / Quiz | Сессия до конца |
| Знаки | Поиск, деталь, «Уже знаю» |
| Настройки | Дисклеймер, аналитика вкл/выкл |
| Иконка | На домашнем экране под названием **Fahrprufung DE** |
| Языки | Переключение RU/EN/DE/UK/FR/TR |

## 5. Следующий билд

Перед каждой новой загрузкой увеличьте **Build** (не Version):

Xcode → Target → General → **Build** (`CURRENT_PROJECT_VERSION`)

Сейчас: **1.0 (1)**

## 6. Submit for Review

После TestFlight, когда готовы к публичному релизу:

1. Заполните описание, скриншоты, Privacy Policy URL
2. App Privacy по `docs/app-store-privacy.md`
3. TestFlight → тот же билд → **Submit for Review**

## Review Notes (пример для Apple)

```
Fahrprufung DE is an unofficial study app for the German practical driving exam.
No account required. Optional anonymous analytics (Firebase) can be disabled in Settings.
Traffic sign images are based on official StVO/VzKat specifications (public domain).
```
