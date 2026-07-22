import Combine
import Foundation

@MainActor
final class HomeViewModel: ObservableObject {
    private let store: DataStore
    private var storeSubscription: AnyCancellable?

    init(store: DataStore) {
        self.store = store
        storeSubscription = store.objectWillChange.sink { [weak self] _ in
            self?.objectWillChange.send()
        }
    }

    var language: AppLanguage { store.nativeLanguage }
    var termCount: Int { store.terms.count }
    var categoryCount: Int { store.categories.count }
    var signCount: Int { store.signs.count }
    var coreTerms: [VocabularyTerm] { store.learningTerms(from: store.coreTerms) }
    var examinerTerms: [VocabularyTerm] { store.learningTerms(from: store.terms.filter(\.isExaminerPhrase)) }
    var allTerms: [VocabularyTerm] { store.learningTerms(from: store.terms) }
    var quizSourceTerms: [VocabularyTerm] { store.terms }
    var knownTermCount: Int { store.knownItems.knownTermCount }
    var knownSignCount: Int { store.knownItems.knownSignCount }
    var studyStreak: Int { store.learningStats.studyStreak }
    var overallTermPercent: Int {
        guard termCount > 0 else { return 0 }
        return Int((Double(knownTermCount) / Double(termCount) * 100).rounded())
    }
}
