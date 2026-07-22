import Foundation

struct TrafficSign: Codable, Identifiable, Hashable {
    let id: String
    let stvoCode: String?
    let shape: String?
    let image: String?
    let svg: String?
    let de: String
    let ru: String
    let en: String
    let uk: String
    let fr: String
    let tr: String
    let category: String
    let sourceURL: String?
    let license: String?
    let notes: LocalizedNotes?

    enum CodingKeys: String, CodingKey {
        case id, shape, image, svg, de, ru, en, uk, fr, tr, category, license, notes
        case stvoCode = "stvo_code"
        case sourceURL = "source_url"
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

    func note(for language: AppLanguage) -> String? {
        notes?.text(for: language)
    }
}
