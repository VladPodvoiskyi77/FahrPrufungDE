import Foundation

struct SignsBundle: Codable {
    let version: String
    let description: String?
    let source: String?
    let sourceNote: String?
    let categories: [SignCategoryInfo]?
    let signs: [TrafficSign]

    enum CodingKeys: String, CodingKey {
        case version, description, source, categories, signs
        case sourceNote = "source_note"
    }
}
