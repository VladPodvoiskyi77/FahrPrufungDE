import Foundation
import FirebaseAnalytics
import FirebaseCore
import os

@MainActor
final class AnalyticsService {
    static let shared = AnalyticsService()

    private static let enabledKey = "analyticsEnabled"
    private let logger = Logger(subsystem: "de.fahrprufung.app", category: "Analytics")

    var isEnabled: Bool {
        get {
            if UserDefaults.standard.object(forKey: Self.enabledKey) == nil {
                return true
            }
            return UserDefaults.standard.bool(forKey: Self.enabledKey)
        }
        set {
            let wasEnabled = isEnabled
            if wasEnabled, !newValue {
                logAnalyticsDisabled()
            }
            UserDefaults.standard.set(newValue, forKey: Self.enabledKey)
        }
    }

    private init() {}

    func logAppOpen() {
        log("app_open")
    }

    func logOnboardingCompleted(language: AppLanguage) {
        log("onboarding_completed", ["language": language.rawValue])
        setUserProperty(language.rawValue, forName: "ui_language")
        setUserProperty("true", forName: "onboarding_done")
    }

    func logOnboardingSkipped(language: AppLanguage) {
        log("onboarding_skipped", ["language": language.rawValue])
        setUserProperty(language.rawValue, forName: "ui_language")
        setUserProperty("true", forName: "onboarding_done")
    }

    func logScreen(_ name: String, parameters: [String: Any] = [:]) {
        var params: [String: Any] = [
            AnalyticsParameterScreenName: name,
            AnalyticsParameterScreenClass: name,
        ]
        parameters.forEach { params[$0.key] = $0.value }
        log(AnalyticsEventScreenView, params)
    }

    func logHomeAction(_ action: String) {
        log("home_action_tapped", ["action": action])
    }

    func logQuizCompleted(score: Int, total: Int, sessionTitle: String) {
        let accuracy = total > 0 ? Int((Double(score) / Double(total) * 100).rounded()) : 0
        log("quiz_completed", [
            "score": score,
            "total": total,
            "accuracy_percent": accuracy,
            "session_title": sessionTitle,
        ])
    }

    func logQuizReviewOpened() {
        log("quiz_review_opened")
    }

    func logFlashcardSession(title: String, cardsSeen: Int) {
        log("flashcard_session", [
            "session_title": title,
            "cards_seen": cardsSeen,
        ])
    }

    func logStudyDayEarned(source: String) {
        log("study_day_earned", ["source": source])
    }

    func logTermMarkedKnown(categoryID: String) {
        log("term_marked_known", ["category_id": categoryID])
    }

    func logSignMarkedKnown(stvoCode: String?) {
        log("sign_marked_known", ["stvo_code": stvoCode ?? "unknown"])
    }

    func logLanguageChanged(language: AppLanguage) {
        log("language_changed", ["language": language.rawValue])
        setUserProperty(language.rawValue, forName: "ui_language")
    }

    func logKnownReset() {
        log("known_reset")
    }

    func logProgressViewed() {
        log("progress_viewed")
    }

    func syncEngagementProperties(
        onboardingCompleted: Bool,
        studyStreak: Int,
        knownTermCount: Int
    ) {
        setUserProperty(onboardingCompleted ? "true" : "false", forName: "onboarding_done")
        setUserProperty(studyStreak > 0 ? "yes" : "no", forName: "has_study_streak")
        setUserProperty(Self.knownTermsBucket(for: knownTermCount), forName: "known_terms_bucket")
    }

    private func logAnalyticsDisabled() {
        log("analytics_disabled", bypassEnabledCheck: true)
    }

    private static func knownTermsBucket(for count: Int) -> String {
        switch count {
        case 0: return "0"
        case 1 ... 50: return "1_50"
        case 51 ... 150: return "51_150"
        default: return "150_plus"
        }
    }

    private func log(_ name: String, _ parameters: [String: Any] = [:], bypassEnabledCheck: Bool = false) {
        guard bypassEnabledCheck || isEnabled else { return }
        if parameters.isEmpty {
            logger.debug("\(name, privacy: .public)")
        } else {
            logger.debug("\(name, privacy: .public) \(String(describing: parameters), privacy: .public)")
        }
        Analytics.logEvent(name, parameters: parameters)
    }

    private func setUserProperty(_ value: String, forName name: String) {
        guard isEnabled else { return }
        Analytics.setUserProperty(value, forName: name)
    }
}
