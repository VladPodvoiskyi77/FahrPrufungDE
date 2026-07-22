import Combine
import Foundation

/// Resolves localized strings for the in-app selected language
/// (independent of the system locale).
final class LocalizationManager: ObservableObject {
    static let shared = LocalizationManager()

    @Published var language: AppLanguage = .en {
        didSet { cachedBundle = nil }
    }

    private var cachedBundle: Bundle?

    private init() {}

    var bundle: Bundle {
        if let cachedBundle { return cachedBundle }
        let resolved = Self.bundle(for: language)
        cachedBundle = resolved
        return resolved
    }

    /// Resolves a string for an explicit language without mutating `language`.
    static func localized(_ key: String, for language: AppLanguage, fallback: String) -> String {
        bundle(for: language).localizedString(forKey: key, value: fallback, table: "Localizable")
    }

    static func bundle(for language: AppLanguage) -> Bundle {
        if let path = Bundle.main.path(forResource: language.rawValue, ofType: "lproj"),
           let bundle = Bundle(path: path) {
            return bundle
        }
        if language != .en,
           let path = Bundle.main.path(forResource: "de", ofType: "lproj"),
           let bundle = Bundle(path: path) {
            return bundle
        }
        return .main
    }
}

/// SwiftGen lookup function (see swiftgen.yml `lookupFunction`).
func l10nLookup(_ key: String, _ table: String, _ fallbackValue: String) -> String {
    LocalizationManager.shared.bundle
        .localizedString(forKey: key, value: fallbackValue, table: table)
}
