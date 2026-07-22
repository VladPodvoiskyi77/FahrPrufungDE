import Foundation

struct VocabularyBundle: Codable {
    let version: String
    let categories: [VocabularyCategory]
    let terms: [VocabularyTerm]
}
