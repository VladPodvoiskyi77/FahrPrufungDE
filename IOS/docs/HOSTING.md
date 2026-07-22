# Публикация Privacy Policy

Файл готов: `docs/privacy-policy.html`

Apple требует **публичный HTTPS-URL** — страница должна открываться в браузере без авторизации.

## Куда положить

Любой вариант на ваш выбор:

1. **Отдельный репозиторий на GitHub** → Settings → Pages → папка `/docs`
2. **Свой сайт / домен**
3. **Netlify / Vercel / Cloudflare Pages** — загрузить `privacy-policy.html`

Имя репозитория и путь — любые. ACTest или другие проекты **трогать не нужно**.

## После публикации

1. Скопируйте URL, например: `https://ваш-домен/privacy-policy.html`
2. Вставьте в `FahrPrufungDE/Services/AppLinks.swift`:

```swift
static let privacyPolicyURL: URL? = URL(string: "https://ваш-домен/privacy-policy.html")
```

3. Тот же URL — в **App Store Connect → Privacy Policy URL**
4. Заполните **App Privacy** по инструкции в `docs/app-store-privacy.md`

## Проверка

Откройте URL в Safari на iPhone — должна открыться страница на немецком и английском.
