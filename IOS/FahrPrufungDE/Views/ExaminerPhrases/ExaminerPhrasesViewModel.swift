import Combine
import Foundation

@MainActor
final class ExaminerPhrasesViewModel: ObservableObject {
    @Published var selectedGroup: ExaminerPhraseGroup?

    private let store: DataStore
    private var storeSubscription: AnyCancellable?

    init(store: DataStore) {
        self.store = store
        storeSubscription = store.objectWillChange.sink { [weak self] _ in
            self?.objectWillChange.send()
        }
    }

    var language: AppLanguage { store.nativeLanguage }
    var style: CategoryStyle { CategoryStyle.style(for: "phrases") }

    var allTerms: [VocabularyTerm] {
        store.terms.filter(\.isExaminerPhrase)
    }

    var filteredTerms: [VocabularyTerm] {
        guard let selectedGroup else { return allTerms }
        return allTerms.filter { $0.examinerGroup == selectedGroup }
    }

    var groupedSections: [(group: ExaminerPhraseGroup, terms: [VocabularyTerm])] {
        ExaminerPhraseGroup.allCases.compactMap { group in
            let terms = allTerms.filter { $0.examinerGroup == group }
            guard !terms.isEmpty else { return nil }
            return (group, terms)
        }
    }

    func termCount(for group: ExaminerPhraseGroup) -> Int {
        allTerms.filter { $0.examinerGroup == group }.count
    }

    func selectGroup(_ group: ExaminerPhraseGroup?) {
        selectedGroup = group
    }

    func isKnown(_ term: VocabularyTerm) -> Bool {
        store.isTermKnown(term.id)
    }

    func toggleKnown(_ term: VocabularyTerm) {
        if store.isTermKnown(term.id) {
            store.knownUndo.dismiss()
            store.setTermKnown(term.id, known: false)
        } else {
            store.markTermAsKnown(term.id)
        }
    }

    var learningTerms: [VocabularyTerm] {
        store.learningTerms(from: filteredTerms)
    }

    var knownCount: Int {
        allTerms.filter { store.isTermKnown($0.id) }.count
    }
}
