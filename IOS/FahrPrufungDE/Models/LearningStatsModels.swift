import Foundation

struct QuizResultRecord: Codable, Identifiable, Hashable {
    let id: UUID
    let score: Int
    let total: Int
    let sessionTitle: String
    let date: Date

    var accuracy: Double {
        guard total > 0 else { return 0 }
        return Double(score) / Double(total)
    }
}

struct FlashcardSessionRecord: Codable, Identifiable, Hashable {
    let id: UUID
    let sessionTitle: String
    let cardsSeen: Int
    let date: Date
}
