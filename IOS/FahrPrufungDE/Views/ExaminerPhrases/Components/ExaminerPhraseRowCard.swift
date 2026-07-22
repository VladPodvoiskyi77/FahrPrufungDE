import SwiftUI

struct ExaminerPhraseRowCard: View {
    let term: VocabularyTerm
    let language: AppLanguage
    var group: ExaminerPhraseGroup?
    var style: CategoryStyle = CategoryStyle.style(for: "phrases")
    var isKnown: Bool = false
    var onToggleKnown: (() -> Void)?

    @ObservedObject private var speech = GermanSpeechService.shared

    private var speechID: String { term.id }
    private var isSpeaking: Bool { speech.isSpeaking(id: speechID) }

    var body: some View {
        HStack(alignment: .top, spacing: 10) {
            if let onToggleKnown {
                KnownMarkButton(isKnown: isKnown, style: .compact, action: onToggleKnown)
                    .padding(.top, 2)
            }

            VStack(alignment: .leading, spacing: 8) {
                HStack(alignment: .top, spacing: 10) {
                    Image(systemName: "person.wave.2.fill")
                        .font(.caption)
                        .foregroundStyle(style.color)
                        .padding(.top, 3)

                    Text(term.displayDe)
                        .font(AppTheme.headlineFont(16))
                        .foregroundStyle(AppTheme.roadNavy)
                        .fixedSize(horizontal: false, vertical: true)

                    Spacer(minLength: 0)

                    Button {
                        speech.speakGerman(term.displayDe, id: speechID)
                    } label: {
                        Image(systemName: isSpeaking ? "speaker.wave.3.fill" : "speaker.wave.2.fill")
                            .font(.body)
                            .foregroundStyle(isSpeaking ? style.color : AppTheme.roadNavy.opacity(0.45))
                            .frame(width: 36, height: 36)
                            .background(
                                Circle().fill(isSpeaking ? style.color.opacity(0.12) : AppTheme.roadNavy.opacity(0.06))
                            )
                    }
                    .buttonStyle(.plain)
                    .accessibilityLabel(L10n.Common.listen)
                }

                Text(term.displayTranslation(for: language))
                    .font(AppTheme.bodyFont(15))
                    .foregroundStyle(.secondary)
                    .padding(.leading, 22)

                if let group {
                    Text(group.title())
                        .font(AppTheme.captionFont(11))
                        .foregroundStyle(style.color)
                        .padding(.horizontal, 8)
                        .padding(.vertical, 4)
                        .background(Capsule().fill(style.color.opacity(0.12)))
                        .padding(.leading, 22)
                }
            }
        }
        .padding(14)
        .frame(maxWidth: .infinity, alignment: .leading)
        .appCard(accent: style.color)
        .knownDimmed(isKnown)
    }
}
