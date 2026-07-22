import Foundation

enum AppLanguage: String, CaseIterable, Identifiable, Codable {
    case ru
    case en
    case uk
    case fr
    case tr

    var id: String { rawValue }

    var displayName: String {
        switch self {
        case .ru: return "Русский"
        case .en: return "English"
        case .uk: return "Українська"
        case .fr: return "Français"
        case .tr: return "Türkçe"
        }
    }

    var flag: String {
        switch self {
        case .ru: return "🇷🇺"
        case .en: return "🇬🇧"
        case .uk: return "🇺🇦"
        case .fr: return "🇫🇷"
        case .tr: return "🇹🇷"
        }
    }

    /// First-launch default: use the phone's primary language if we support it, otherwise English.
    static var systemDefault: AppLanguage {
        guard let preferred = Locale.preferredLanguages.first else { return .en }
        let code = Locale(identifier: preferred).language.languageCode?.identifier
            ?? String(preferred.prefix(2))
        return AppLanguage(rawValue: code) ?? .en
    }
}
