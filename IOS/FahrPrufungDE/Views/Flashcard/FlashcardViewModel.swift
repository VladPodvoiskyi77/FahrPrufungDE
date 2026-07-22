import Foundation

@MainActor
final class FlashcardViewModel: ObservableObject {
    @Published private(set) var deck: [VocabularyTerm]
    @Published private(set) var index = 0
    @Published var isFlipped = false

    private let store: DataStore
    private let sessionTitle: String
    private var maxCardsSeen = 0
    private var didRecordSession = false
    private var didCountStudyDay = false

    init(terms: [VocabularyTerm], store: DataStore, sessionTitle: String) {
        self.deck = terms.shuffled()
        self.store = store
        self.sessionTitle = sessionTitle
        maxCardsSeen = deck.isEmpty ? 0 : 1
    }

    var current: VocabularyTerm? {
        guard deck.indices.contains(index) else { return nil }
        return deck[index]
    }

    var progress: Double {
        guard !deck.isEmpty else { return 0 }
        return Double(index + 1) / Double(deck.count)
    }

    var canGoBack: Bool { index > 0 }
    var canGoForward: Bool { index < deck.count - 1 }

    var isCurrentKnown: Bool {
        guard let current else { return false }
        return store.isTermKnown(current.id)
    }

    func flip() {
        isFlipped.toggle()
    }

    func resetFlip() {
        isFlipped = false
    }

    func move(by offset: Int) {
        let next = index + offset
        guard deck.indices.contains(next) else { return }
        index = next
        maxCardsSeen = max(maxCardsSeen, index + 1)
        isFlipped = false
        countStudyDayIfNeeded()
    }

    func finishSessionIfNeeded() {
        guard !didRecordSession else { return }
        didRecordSession = true
        guard maxCardsSeen >= LearningStatsStore.minimumCardsForStudyDay else { return }
        store.learningStats.recordFlashcardSession(title: sessionTitle, cardsSeen: maxCardsSeen)
        AnalyticsService.shared.logFlashcardSession(title: sessionTitle, cardsSeen: maxCardsSeen)
    }

    private func countStudyDayIfNeeded() {
        guard !didCountStudyDay else { return }
        guard maxCardsSeen >= LearningStatsStore.minimumCardsForStudyDay else { return }
        didCountStudyDay = true
        if store.learningStats.recordStudyActivity() {
            AnalyticsService.shared.logStudyDayEarned(source: "flashcards")
            AnalyticsService.shared.syncEngagementProperties(
                onboardingCompleted: UserDefaults.standard.bool(forKey: OnboardingViewModel.completedKey),
                studyStreak: store.learningStats.studyStreak,
                knownTermCount: store.knownItems.knownTermCount
            )
        }
    }

    func toggleKnownForCurrent() {
        guard let term = current else { return }

        if store.isTermKnown(term.id) {
            store.knownUndo.dismiss()
            store.setTermKnown(term.id, known: false)
            return
        }

        let savedIndex = index
        store.markTermAsKnown(term.id) { [weak self] in
            guard let self else { return }
            guard !self.deck.contains(where: { $0.id == term.id }) else { return }
            let insertAt = min(savedIndex, self.deck.count)
            self.deck.insert(term, at: insertAt)
            self.index = insertAt
            self.isFlipped = false
        }

        deck.removeAll { $0.id == term.id }
        if deck.isEmpty {
            index = 0
        } else if index >= deck.count {
            index = deck.count - 1
        }
        isFlipped = false
    }
}
