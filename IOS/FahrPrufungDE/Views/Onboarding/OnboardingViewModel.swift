import Foundation

@MainActor
final class OnboardingViewModel: ObservableObject {
    static let completedKey = "hasCompletedOnboarding"

    @Published var page = 0
    @Published var draftLanguage: AppLanguage

    private let store: DataStore

    init(store: DataStore) {
        self.store = store
        draftLanguage = store.nativeLanguage
    }

    var isLastPage: Bool { page >= 2 }

    func advance() {
        page += 1
    }

    func finish() {
        store.nativeLanguage = draftLanguage
        markCompleted()
        AnalyticsService.shared.logOnboardingCompleted(language: draftLanguage)
        syncEngagement()
    }

    func skip() {
        markCompleted()
        AnalyticsService.shared.logOnboardingSkipped()
        syncEngagement()
    }

    func markCompleted() {
        UserDefaults.standard.set(true, forKey: Self.completedKey)
    }

    private func syncEngagement() {
        AnalyticsService.shared.syncEngagementProperties(
            onboardingCompleted: true,
            studyStreak: store.learningStats.studyStreak,
            knownTermCount: store.knownItems.knownTermCount
        )
    }
}
