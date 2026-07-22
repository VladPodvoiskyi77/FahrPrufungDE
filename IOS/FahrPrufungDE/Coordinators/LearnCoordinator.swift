import SwiftUI

/// A coordinator that owns a NavigationStack path.
@MainActor
protocol FlowCoordinator: ObservableObject {
    var path: NavigationPath { get set }
}

enum LearnRoute: Hashable {
    case categories
    case terms(VocabularyCategory)
    case examinerPhrases
    case flashcards(terms: [VocabularyTerm], title: String)
    case quiz(terms: [VocabularyTerm], title: String)
    case progress
}

@MainActor
final class LearnCoordinator: ObservableObject, FlowCoordinator {
    @Published var path = NavigationPath()

    func show(_ route: LearnRoute) {
        path.append(route)
    }

    func pop() {
        guard !path.isEmpty else { return }
        path.removeLast()
    }

    func popToRoot() {
        path = NavigationPath()
    }
}
