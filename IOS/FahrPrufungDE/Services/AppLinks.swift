import Foundation

enum AppLinks {
    static let developerEmail = "appentwickler2025@gmail.com"
    static let mailtoURL = URL(string: "mailto:\(developerEmail)")!

    /// Опубликуйте `docs/privacy-policy.html` на любом хостинге (GitHub Pages, свой сайт и т.д.)
    /// и вставьте сюда публичный HTTPS-URL перед отправкой в App Store.
    static let privacyPolicyURL: URL? = nil

    static let prapoDeAppStoreURL = URL(
        string: "https://apps.apple.com/app/id6758207550"
    )!
}
