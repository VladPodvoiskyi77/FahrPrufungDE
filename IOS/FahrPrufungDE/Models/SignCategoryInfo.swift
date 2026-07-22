import Foundation

struct SignCategoryInfo: Codable, Identifiable, Hashable {
    let id: String
    let de: String
    let ru: String
    let en: String
    let uk: String
    let fr: String
    let tr: String

    func title(for language: AppLanguage) -> String {
        switch language {
        case .ru: return ru
        case .en: return en
        case .uk: return uk
        case .fr: return fr
        case .tr: return tr
        }
    }
}
