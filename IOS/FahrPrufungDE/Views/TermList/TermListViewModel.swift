import Foundation

@MainActor
final class TermListViewModel: ObservableObject {
    let category: VocabularyCategory
    private let store: DataStore

    init(category: VocabularyCategory, store: DataStore) {
        self.category = category
        self.store = store
    }

    var language: AppLanguage { store.nativeLanguage }
    var terms: [VocabularyTerm] { store.terms(for: category.id) }
    var learningTerms: [VocabularyTerm] { store.learningTerms(from: terms) }
    var categoryTitle: String { category.title(for: store.nativeLanguage) }
    var knownCount: Int { terms.filter { store.isTermKnown($0.id) }.count }

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
}
