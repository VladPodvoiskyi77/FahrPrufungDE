import Foundation

@MainActor
final class SettingsViewModel: ObservableObject {
    private let store: DataStore

    init(store: DataStore) {
        self.store = store
    }

    var termCount: Int { store.terms.count }
    var categoryCount: Int { store.categories.count }
    var signCount: Int { store.signs.count }
    var knownTermCount: Int { store.knownItems.knownTermCount }
    var knownSignCount: Int { store.knownItems.knownSignCount }
    var hasKnownItems: Bool { knownTermCount > 0 || knownSignCount > 0 }

    var analyticsEnabled: Bool {
        get { AnalyticsService.shared.isEnabled }
        set { AnalyticsService.shared.isEnabled = newValue }
    }

    var language: AppLanguage {
        get { store.nativeLanguage }
        set { store.nativeLanguage = newValue }
    }

    func resetOnboarding() {
        UserDefaults.standard.set(false, forKey: OnboardingViewModel.completedKey)
    }

    func resetKnownItems() {
        store.resetKnownItems()
    }
}
