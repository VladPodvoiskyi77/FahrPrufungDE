import Foundation

struct VocabularyTerm: Codable, Identifiable, Hashable {
    let id: String
    let de: String
    let article: String?
    let deBase: String
    let ru: String
    let en: String
    let uk: String
    let fr: String
    let tr: String
    let category: String
    let tags: [String]
    let examPhraseDe: String?

    enum CodingKeys: String, CodingKey {
        case id, de, article, ru, en, uk, fr, tr, category, tags
        case deBase = "de_base"
        case examPhraseDe = "exam_phrase_de"
    }

    func translation(for language: AppLanguage) -> String {
        switch language {
        case .ru: return ru
        case .en: return en
        case .uk: return uk
        case .fr: return fr
        case .tr: return tr
        }
    }

    var displayDe: String { de.withLeadingCapital }
    func displayTranslation(for language: AppLanguage) -> String {
        translation(for: language).withLeadingCapital
    }
    var displayExamPhraseDe: String? {
        examPhraseDe?.withLeadingCapital
    }

    var isCore: Bool { tags.contains("core") }
    var isExaminerPhrase: Bool { tags.contains("examiner") }
}

extension String {
    /// First letter/digit uppercased for UI display (lists, flashcards, quiz).
    var withLeadingCapital: String {
        guard let index = firstIndex(where: { $0.isLetter || $0.isNumber }) else { return self }
        let prefix = self[..<index]
        let first = self[index]
        let rest = self[index...].dropFirst()
        return prefix + String(first).uppercased(with: Locale.current) + rest
    }
}
