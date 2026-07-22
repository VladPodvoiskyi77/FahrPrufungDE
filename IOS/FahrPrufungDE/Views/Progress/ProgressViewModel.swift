import Combine
import Foundation

struct CategoryProgressItem: Identifiable {
    let id: String
    let title: String
    let known: Int
    let total: Int
    let colorName: String

    var fraction: Double {
        guard total > 0 else { return 0 }
        return Double(known) / Double(total)
    }

    var percent: Int {
        Int((fraction * 100).rounded())
    }
}

@MainActor
final class ProgressViewModel: ObservableObject {
    private let store: DataStore
    private var storeSubscription: AnyCancellable?

    init(store: DataStore) {
        self.store = store
        storeSubscription = store.objectWillChange.sink { [weak self] _ in
            self?.objectWillChange.send()
        }
    }

    var language: AppLanguage { store.nativeLanguage }

    var knownTermCount: Int { store.knownItems.knownTermCount }
    var totalTermCount: Int { store.terms.count }
    var knownSignCount: Int { store.knownItems.knownSignCount }
    var totalSignCount: Int { store.signs.count }

    var overallTermPercent: Int {
        percent(known: knownTermCount, total: totalTermCount)
    }

    var overallSignPercent: Int {
        percent(known: knownSignCount, total: totalSignCount)
    }

    var studyStreak: Int { store.learningStats.studyStreak }

    var recentQuizResults: [QuizResultRecord] {
        store.learningStats.quizResults
    }

    var categoryItems: [CategoryProgressItem] {
        store.categories.map { category in
            let progress = store.categoryProgress(for: category)
            return CategoryProgressItem(
                id: category.id,
                title: category.title(for: store.nativeLanguage),
                known: progress.known,
                total: progress.total,
                colorName: category.id
            )
        }
        .filter { $0.total > 0 }
        .sorted { $0.fraction > $1.fraction }
    }

    private func percent(known: Int, total: Int) -> Int {
        guard total > 0 else { return 0 }
        return Int((Double(known) / Double(total) * 100).rounded())
    }
}
