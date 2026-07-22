import Foundation

enum ExaminerPhraseGroup: String, CaseIterable, Identifiable {
    case start
    case direction
    case maneuver
    case safety
    case hint
    case result

    var id: String { rawValue }

    var tag: String { rawValue }

    var icon: String {
        switch self {
        case .start: return "flag.checkered"
        case .direction: return "arrow.triangle.turn.up.right.diamond.fill"
        case .maneuver: return "arrow.uturn.backward.circle.fill"
        case .safety: return "wrench.and.screwdriver.fill"
        case .hint: return "exclamationmark.bubble.fill"
        case .result: return "checkmark.seal.fill"
        }
    }

    func title() -> String {
        switch self {
        case .start: return L10n.ExaminerPhrases.Group.start
        case .direction: return L10n.ExaminerPhrases.Group.direction
        case .maneuver: return L10n.ExaminerPhrases.Group.maneuver
        case .safety: return L10n.ExaminerPhrases.Group.safety
        case .hint: return L10n.ExaminerPhrases.Group.hint
        case .result: return L10n.ExaminerPhrases.Group.result
        }
    }
}

extension VocabularyTerm {
    var examinerGroup: ExaminerPhraseGroup {
        guard isExaminerPhrase else { return .start }
        for group in ExaminerPhraseGroup.allCases where tags.contains(group.tag) {
            return group
        }
        return .start
    }
}
