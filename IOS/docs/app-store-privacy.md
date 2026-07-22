# App Store Connect — App Privacy (Fahrprufung DE)

Используйте эту инструкцию при заполнении **App Privacy** в App Store Connect для приложения **Fahrprufung DE** (`de.fahrprufung.app`).

## Privacy Policy URL

Опубликуйте `docs/privacy-policy.html` на **любом** хостинге (см. `docs/HOSTING.md`) и укажите получившийся HTTPS-URL в App Store Connect.

Пример (замените на свой):

```
https://ваш-домен/privacy-policy.html
```

Тот же URL — в `AppLinks.privacyPolicyURL` в коде приложения.

---

## Шаг 1: Собираете ли вы данные?

**Do you or your third-party partners collect data from this app?**

→ **Yes**

---

## Шаг 2: Типы данных (когда аналитика включена)

Отметьте только то, что реально передаётся через **Firebase Analytics**. Локальные данные (прогресс в UserDefaults) **не отмечайте** — они не покидают устройство.

### Usage Data → Product Interaction

| Вопрос | Ответ |
|--------|-------|
| Collected | Yes |
| Linked to the user's identity | **No** |
| Used for tracking | **No** |
| Purposes | **Analytics** |

*События: экраны, quiz (включая просмотр ответов), карточки, смена языка, онбординг, действия на главном экране, серия дней обучения. Без персональных данных — только агрегированные счётчики и коды категорий/знаков.*

### Identifiers → Device ID

| Вопрос | Ответ |
|--------|-------|
| Collected | Yes (Firebase Installation ID) |
| Linked to the user's identity | **No** |
| Used for tracking | **No** |
| Purposes | **Analytics** |

### Usage Data → Other Usage Data (опционально)

Если Apple предложит отдельно — можно указать технические данные сессии (модель устройства, версия ОС) через Firebase:

| Вопрос | Ответ |
|--------|-------|
| Collected | Yes |
| Linked to the user's identity | **No** |
| Used for tracking | **No** |
| Purposes | **Analytics** |

---

## Шаг 3: Что НЕ отмечать

- Contact Info (email, name, phone)
- Health & Fitness
- Financial Info
- Location
- Sensitive Info
- Contacts
- User Content (фото, аудио)
- Browsing History
- Purchases (если нет IAP)
- Advertising Data
- Crash Data — **только если не подключён Firebase Crashlytics** (сейчас не подключён)

---

## Шаг 4: Tracking

**Does your app use data for tracking purposes?**

→ **No**

Приложение не использует ATT, не показывает рекламу и не связывает данные с третьими сторонами для таргетинга.

---

## Шаг 5: Privacy Nutrition Label (итог для пользователя)

На странице App Store пользователь увидит примерно:

- **Data Used to Track You:** None
- **Data Linked to You:** None (при ответах «Not linked»)
- **Data Not Linked to You:** Usage Data, Identifiers — для Analytics

---

## Шаг 6: Дополнительные поля в App Store Connect

| Поле | Значение |
|------|----------|
| Privacy Policy URL | URL из `docs/privacy-policy.html` |
| Age Rating | 4+ (образовательное, без UGC) |
| Encryption | Uses encryption — exempt (HTTPS only, standard) |
| Third-party content | Signs from StVO / Wikimedia — указать в описании при необходимости |

---

## Соответствие коду приложения

- Аналитика отключается: **Настройки → Анонимная аналитика**
- При `isEnabled = false` события в Firebase не отправляются (`AnalyticsService.swift`); при отключении логируется одно событие `analytics_disabled`
- Автоматический screen reporting Firebase отключён (`FirebaseAutomaticScreenReportingEnabled = NO`)
- Локальный прогресс не синхронизируется с сервером
- Контакт разработчика: `appentwickler2025@gmail.com`

---

## Чеклист перед отправкой

- [ ] `docs/privacy-policy.html` опубликован по HTTPS
- [ ] Ссылка «Политика конфиденциальности» открывается в приложении
- [ ] App Privacy заполнена по таблицам выше
- [ ] Privacy Policy URL вставлен в версию приложения
- [ ] Скриншоты и описание готовы
