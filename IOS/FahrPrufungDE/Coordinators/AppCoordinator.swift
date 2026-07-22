import SwiftUI

@MainActor
final class AppCoordinator: ObservableObject {
    enum Tab: Hashable {
        case learn
        case signs
        case progress
        case settings
    }

    @Published var selectedTab: Tab = .learn
    @Published var isOnboardingPresented = false

    let learn = LearnCoordinator()
    let signs = SignsCoordinator()

    func showOnboardingIfNeeded() {
        let completed = UserDefaults.standard.bool(forKey: OnboardingViewModel.completedKey)
        if !completed {
            isOnboardingPresented = true
        }
    }
}
