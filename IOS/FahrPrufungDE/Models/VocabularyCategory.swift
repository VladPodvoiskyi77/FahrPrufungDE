import Foundation

struct VocabularyCategory: Codable, Identifiable, Hashable {
    let id: String
    let de: String
    let ru: String
    let en: String
    let uk: String
    let fr: String
    let tr: String

    func title(for language: AppLanguage) -> String {
        switch language {
        case .ru: return ru.withLeadingCapital
        case .en: return en.withLeadingCapital
        case .uk: return uk.withLeadingCapital
        case .fr: return fr.withLeadingCapital
        case .tr: return tr.withLeadingCapital
        }
    }

    var displayDe: String { de.withLeadingCapital }
}
