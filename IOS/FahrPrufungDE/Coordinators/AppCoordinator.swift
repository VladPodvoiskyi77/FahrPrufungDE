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
    /// DEBUG: Settings should scroll to Privacy Policy after open_route.
    @Published var scrollSettingsToPrivacy = false

    let learn = LearnCoordinator()
    let signs = SignsCoordinator()

    private var didApplyLaunchRoute = false

    func showOnboardingIfNeeded() {
        let completed = UserDefaults.standard.bool(forKey: OnboardingViewModel.completedKey)
        if !completed {
            isOnboardingPresented = true
        }
    }

    /// Debug helper for simulator parity captures:
    /// `xcrun simctl launch <udid> de.fahrprufung.app -open_route settings`
    func applyLaunchRouteIfNeeded(store: DataStore) {
        #if DEBUG
        guard !didApplyLaunchRoute else { return }
        let args = ProcessInfo.processInfo.arguments
        guard let idx = args.firstIndex(of: "-open_route"),
              args.indices.contains(idx + 1) else { return }
        didApplyLaunchRoute = true
        isOnboardingPresented = false
        UserDefaults.standard.set(true, forKey: OnboardingViewModel.completedKey)

        switch args[idx + 1] {
        case "settings":
            selectedTab = .settings
        case "settings_privacy":
            selectedTab = .settings
            scrollSettingsToPrivacy = true
        case "progress":
            selectedTab = .progress
        case "signs":
            selectedTab = .signs
        case "quiz":
            selectedTab = .learn
            learn.popToRoot()
            guard store.terms.count >= 4 else { return }
            learn.show(.quiz(terms: store.terms, title: L10n.Home.Quiz.title))
        case "home":
            selectedTab = .learn
            learn.popToRoot()
        default:
            break
        }
        #endif
    }
}
