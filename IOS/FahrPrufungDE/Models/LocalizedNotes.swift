import Foundation

struct LocalizedNotes: Codable, Hashable {
    let de: String
    let ru: String
    let en: String
    let uk: String
    let fr: String
    let tr: String

    func text(for language: AppLanguage) -> String {
        switch language {
        case .ru: return ru
        case .en: return en
        case .uk: return uk
        case .fr: return fr
        case .tr: return tr
        }
    }
}
