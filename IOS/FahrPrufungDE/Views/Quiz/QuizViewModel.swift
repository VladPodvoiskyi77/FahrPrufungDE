import Foundation

struct QuizQuestion {
    let prompt: String
    let correctID: String
    let options: [QuizOption]
}

struct QuizOption {
    let id: String
    let text: String
}

struct QuizAnswerRecord: Identifiable {
    let id: Int
    let prompt: String
    let selectedText: String
    let correctText: String
    let isCorrect: Bool
}

@MainActor
final class QuizViewModel: ObservableObject {
    /// Full term pool for the session (learning + known), used to build answer options.
    let sourceTerms: [VocabularyTerm]
    private let store: DataStore
    private let sessionTitle: String

    @Published private(set) var questions: [QuizQuestion] = []
    @Published private(set) var currentIndex = 0
    @Published private(set) var score = 0
    @Published private(set) var selectedID: String?
    @Published private(set) var isFinished = false
    @Published private(set) var answerRecords: [QuizAnswerRecord] = []

    private var hasRecordedResult = false
    private var didStart = false

    init(sourceTerms: [VocabularyTerm], store: DataStore, sessionTitle: String) {
        self.sourceTerms = sourceTerms
        self.store = store
        self.sessionTitle = sessionTitle
    }

    var learningTerms: [VocabularyTerm] {
        store.learningTerms(from: sourceTerms)
    }

    var currentQuestion: QuizQuestion? {
        guard questions.indices.contains(currentIndex) else { return nil }
        return questions[currentIndex]
    }

    var hasAnswered: Bool { selectedID != nil }

    func startIfNeeded() {
        guard !didStart else {
            refreshTranslations()
            return
        }
        didStart = true
        start()
    }

    func start() {
        hasRecordedResult = false
        let learning = learningTerms.shuffled()
        guard !learning.isEmpty else {
            questions = []
            return
        }

        let optionPool = buildOptionPool(learning: learning)
        guard optionPool.count >= 2 else {
            questions = []
            return
        }

        let questionCount = min(10, learning.count)
        questions = learning.prefix(questionCount).map { makeQuestion(for: $0, pool: optionPool) }
        currentIndex = 0
        score = 0
        selectedID = nil
        isFinished = false
        answerRecords = []
    }

    func answer(_ option: QuizOption) {
        guard selectedID == nil else { return }
        selectedID = option.id
        if option.id == currentQuestion?.correctID {
            score += 1
        }
    }

    func next() {
        recordCurrentAnswer()
        if currentIndex + 1 >= questions.count {
            isFinished = true
            recordCompletionIfNeeded()
        } else {
            currentIndex += 1
            selectedID = nil
        }
    }

    func optionLetter(_ index: Int) -> String {
        let letters = ["A", "B", "C", "D"]
        return letters.indices.contains(index) ? letters[index] : "?"
    }

    func optionState(for option: QuizOption) -> QuizOptionCard.QuizOptionState {
        guard let selectedID else { return .idle }
        if option.id == currentQuestion?.correctID { return .correct }
        if option.id == selectedID { return .wrong }
        return .neutral
    }

    /// Keeps quiz progress but updates answer labels after a language change.
    func refreshTranslations() {
        guard !questions.isEmpty, !isFinished else { return }

        let lookup = Dictionary(uniqueKeysWithValues: store.terms.map { ($0.id, $0) })
        questions = questions.map { question in
            QuizQuestion(
                prompt: question.prompt,
                correctID: question.correctID,
                options: question.options.map { option in
                    guard let term = lookup[option.id] else { return option }
                    return QuizOption(
                        id: option.id,
                        text: term.displayTranslation(for: store.nativeLanguage)
                    )
                }
            )
        }
    }

    private func recordCurrentAnswer() {
        guard let question = currentQuestion, let selectedID else { return }
        let correctText = question.options.first { $0.id == question.correctID }?.text ?? ""
        let selectedText = question.options.first { $0.id == selectedID }?.text ?? ""
        answerRecords.append(
            QuizAnswerRecord(
                id: answerRecords.count,
                prompt: question.prompt,
                selectedText: selectedText,
                correctText: correctText,
                isCorrect: selectedID == question.correctID
            )
        )
    }

    private func recordCompletionIfNeeded() {
        guard !hasRecordedResult else { return }
        hasRecordedResult = true
        let total = questions.count
        let isNewStudyDay = store.learningStats.recordQuizResult(
            score: score,
            total: total,
            sessionTitle: sessionTitle
        )
        AnalyticsService.shared.logQuizCompleted(score: score, total: total, sessionTitle: sessionTitle)
        if isNewStudyDay {
            AnalyticsService.shared.logStudyDayEarned(source: "quiz")
            AnalyticsService.shared.syncEngagementProperties(
                onboardingCompleted: UserDefaults.standard.bool(forKey: OnboardingViewModel.completedKey),
                studyStreak: store.learningStats.studyStreak,
                knownTermCount: store.knownItems.knownTermCount
            )
        }
    }

    /// Learning terms are questions; known terms fill in wrong-answer options when needed.
    private func buildOptionPool(learning: [VocabularyTerm]) -> [VocabularyTerm] {
        var pool = learning
        let learningIDs = Set(learning.map(\.id))
        let knownSupplement = sourceTerms
            .filter { store.isTermKnown($0.id) && !learningIDs.contains($0.id) }
            .shuffled()

        let targetSize = max(4, learning.count)
        for term in knownSupplement where pool.count < targetSize {
            pool.append(term)
        }
        return pool
    }

    private func makeQuestion(for term: VocabularyTerm, pool: [VocabularyTerm]) -> QuizQuestion {
        let wrong = pool.filter { $0.id != term.id }.shuffled().prefix(3)
        let options = (wrong + [term]).shuffled().map {
            QuizOption(id: $0.id, text: $0.displayTranslation(for: store.nativeLanguage))
        }
        return QuizQuestion(prompt: term.displayDe, correctID: term.id, options: options)
    }
}
