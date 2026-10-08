# FahrPrufung DE — Android

Kotlin + Jetpack Compose. Зеркалит iOS-версию: те же цвета, экраны и логика.

## Запуск

1. В Android Studio открой именно папку `Android/` (не корень репо)
2. Дождись окончания Gradle Sync (полоска внизу исчезнет)
3. Выбери устройство сверху и нажми Run ▶ (minSdk 26)

Если Sync долго качает зависимости — это нормально при первом открытии.  
Пока идёт Sync, кнопка Run недоступна.

Или из терминала (телефон подключён по USB с отладкой):

```bash
cd Android
export JAVA_HOME="/Applications/Android Studio.app/Contents/jbr/Contents/Home"
./gradlew installDebug
adb shell am start -n de.fahrprufung.app/.MainActivity
```

## Архитектура

| Слой | Пакет |
|------|--------|
| UI | `ui/home`, `ui/quiz`, `ui/flashcards`, … |
| Данные | `data/AppContainer`, `ContentRepository`, `PreferencesRepository` |
| Модели | `model/VocabularyModels`, `SignModels` |
| Тема | `theme/Color.kt`, `Theme.kt`, `CategoryStyle.kt` |

## Локализация

`res/values-{ru,en,uk,fr,tr,de}/strings.xml` — UI-строки.  
Переводы терминов и знаков — в `assets/vocabulary.json` и `assets/signs.json`.

## Аналитика

Firebase Analytics (тот же проект `fahrprufung-de`, что и iOS).

- Конфиг: скачай `google-services.json` из Firebase Console → Project settings → Your apps → Android, положи в `app/google-services.json` (файл в git не коммитится; есть `google-services.json.example`)
- События: `AnalyticsService` (экраны, квиз start/complete, карточки, онбординг, язык, «знаю», фон/foreground)
- Opt-out: переключатель в Settings (`analyticsEnabled`)

## Отличия от iOS (пока)

- Нет Crashlytics (как на iOS)

## Синхронизация контента с iOS

```bash
cp IOS/FahrPrufungDE/Resources/vocabulary.json app/src/main/assets/
cp IOS/FahrPrufungDE/Resources/signs.json app/src/main/assets/
cp -R IOS/FahrPrufungDE/Resources/Signs app/src/main/assets/
```
