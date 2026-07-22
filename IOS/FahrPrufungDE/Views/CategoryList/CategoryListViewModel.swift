import Foundation

@MainActor
final class CategoryListViewModel: ObservableObject {
    private let store: DataStore

    init(store: DataStore) {
        self.store = store
    }

    var language: AppLanguage { store.nativeLanguage }
    var categories: [VocabularyCategory] { store.categories }

    func termCount(for category: VocabularyCategory) -> Int {
        store.terms(for: category.id).count
    }
}
