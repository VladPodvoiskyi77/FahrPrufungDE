import Foundation

@MainActor
final class LearningStatsStore {
    private static let storageKey = "learningStats.v1"
    private static let maxQuizResults = 20
    private static let maxFlashcardSessions = 10
    static let minimumCardsForStudyDay = 10

    private(set) var quizResults: [QuizResultRecord] = []
    private(set) var flashcardSessions: [FlashcardSessionRecord] = []
    private(set) var studyDayKeys: Set<String> = []

    var onChange: (() -> Void)?

    init() {
        load()
    }

    /// Consecutive study days ending today, or ending yesterday if today is not over yet.
    var studyStreak: Int {
        guard !studyDayKeys.isEmpty else { return 0 }
        guard let streakStart = streakCountStartDay else { return 0 }

        let calendar = Calendar.current
        var streak = 0
        var day = streakStart

        while studyDayKeys.contains(dayKey(for: day)) {
            streak += 1
            guard let previous = calendar.date(byAdding: .day, value: -1, to: day) else { break }
            day = previous
        }
        return streak
    }

    /// Today if already studied; otherwise yesterday until the calendar day ends.
    private var streakCountStartDay: Date? {
        let calendar = Calendar.current
        let today = calendar.startOfDay(for: Date())

        if studyDayKeys.contains(dayKey(for: today)) {
            return today
        }

        guard
            let yesterday = calendar.date(byAdding: .day, value: -1, to: today),
            studyDayKeys.contains(dayKey(for: yesterday))
        else {
            return nil
        }

        return yesterday
    }

    var lastStudyDate: Date? {
        studyDayKeys.compactMap { Self.date(fromDayKey: $0) }.max()
    }

    @discardableResult
    func recordStudyActivity() -> Bool {
        let key = dayKey(for: Date())
        let isNew = !studyDayKeys.contains(key)
        studyDayKeys.insert(key)
        persist()
        onChange?()
        return isNew
    }

    @discardableResult
    func recordQuizResult(score: Int, total: Int, sessionTitle: String) -> Bool {
        let isNewStudyDay = recordStudyActivity()
        let record = QuizResultRecord(
            id: UUID(),
            score: score,
            total: total,
            sessionTitle: sessionTitle,
            date: Date()
        )
        quizResults.insert(record, at: 0)
        if quizResults.count > Self.maxQuizResults {
            quizResults = Array(quizResults.prefix(Self.maxQuizResults))
        }
        persist()
        onChange?()
        return isNewStudyDay
    }

    func recordFlashcardSession(title: String, cardsSeen: Int) {
        guard cardsSeen >= Self.minimumCardsForStudyDay else { return }
        recordStudyActivity()
        let record = FlashcardSessionRecord(
            id: UUID(),
            sessionTitle: title,
            cardsSeen: cardsSeen,
            date: Date()
        )
        flashcardSessions.insert(record, at: 0)
        if flashcardSessions.count > Self.maxFlashcardSessions {
            flashcardSessions = Array(flashcardSessions.prefix(Self.maxFlashcardSessions))
        }
        persist()
        onChange?()
    }

    private func dayKey(for date: Date) -> String {
        Self.dayKey(for: date)
    }

    private static func dayKey(for date: Date) -> String {
        let components = Calendar.current.dateComponents([.year, .month, .day], from: date)
        return String(format: "%04d-%02d-%02d", components.year ?? 0, components.month ?? 0, components.day ?? 0)
    }

    private static func date(fromDayKey key: String) -> Date? {
        let parts = key.split(separator: "-").compactMap { Int($0) }
        guard parts.count == 3 else { return nil }
        return Calendar.current.date(from: DateComponents(year: parts[0], month: parts[1], day: parts[2]))
    }

    private struct Payload: Codable {
        var quizResults: [QuizResultRecord]
        var flashcardSessions: [FlashcardSessionRecord]
        var studyDayKeys: [String]
    }

    private func load() {
        guard
            let data = UserDefaults.standard.data(forKey: Self.storageKey),
            let payload = try? JSONDecoder().decode(Payload.self, from: data)
        else { return }
        quizResults = payload.quizResults
        flashcardSessions = payload.flashcardSessions
        studyDayKeys = Set(payload.studyDayKeys)
    }

    private func persist() {
        let payload = Payload(
            quizResults: quizResults,
            flashcardSessions: flashcardSessions,
            studyDayKeys: Array(studyDayKeys)
        )
        guard let data = try? JSONEncoder().encode(payload) else { return }
        UserDefaults.standard.set(data, forKey: Self.storageKey)
    }
}
