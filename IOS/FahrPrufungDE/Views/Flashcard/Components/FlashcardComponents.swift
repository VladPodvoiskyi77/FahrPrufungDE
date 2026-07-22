import SwiftUI

struct FlashcardSurface: View {
    let term: VocabularyTerm
    let language: AppLanguage
    let isFlipped: Bool
    let progress: Double

    var body: some View {
        VStack(spacing: 0) {
            // Progress bar
            GeometryReader { geo in
                ZStack(alignment: .leading) {
                    Capsule()
                        .fill(AppTheme.roadNavy.opacity(0.08))
                    Capsule()
                        .fill(AppTheme.accentGradient)
                        .frame(width: geo.size.width * progress)
                }
            }
            .frame(height: 5)
            .padding(.horizontal, 20)
            .padding(.top, 20)
            .animation(AppMotion.spring, value: progress)

            Spacer(minLength: 16)

            VStack(spacing: 20) {
                Image(systemName: isFlipped ? "globe.europe.africa.fill" : "character.book.closed.fill")
                    .font(.title)
                    .foregroundStyle(AppTheme.signalAmber)
                    .symbolEffect(.bounce, value: isFlipped)

                if isFlipped {
                    Text(term.displayTranslation(for: language))
                        .font(AppTheme.titleFont(26))
                        .foregroundStyle(AppTheme.roadNavy)
                        .multilineTextAlignment(.center)
                        .transition(.opacity.combined(with: .scale(scale: 0.95)))

                    RoadDashedLine()
                        .padding(.horizontal, 40)

                    Text(term.displayDe)
                        .font(AppTheme.bodyFont(17))
                        .foregroundStyle(.secondary)
                        .multilineTextAlignment(.center)
                } else {
                    if let article = term.article {
                        Text(article)
                            .font(AppTheme.captionFont())
                            .foregroundStyle(AppTheme.highwayTeal)
                            .padding(.horizontal, 12)
                            .padding(.vertical, 5)
                            .background(Capsule().fill(AppTheme.highwayTeal.opacity(0.12)))
                    }

                    Text(term.displayDe)
                        .font(AppTheme.titleFont(28))
                        .foregroundStyle(AppTheme.roadNavy)
                        .multilineTextAlignment(.center)

                    Text(L10n.Flashcards.tapToFlip)
                        .font(AppTheme.captionFont())
                        .foregroundStyle(AppTheme.signalAmber)
                }

                if let phrase = term.displayExamPhraseDe {
                    ExaminerPhraseBubble(text: phrase)
                }
            }
            .padding(24)
            .animation(.spring(response: 0.4), value: isFlipped)

            Spacer(minLength: 16)
        }
        .frame(maxWidth: .infinity, minHeight: 300)
        .background {
            RoundedRectangle(cornerRadius: 28, style: .continuous)
                .fill(AppTheme.cardWhite)
                .shadow(color: AppTheme.roadNavy.opacity(0.12), radius: 24, y: 12)
                .overlay(
                    RoundedRectangle(cornerRadius: 28, style: .continuous)
                        .strokeBorder(
                            LinearGradient(
                                colors: [.white.opacity(0.8), AppTheme.highwayTeal.opacity(0.15)],
                                startPoint: .topLeading,
                                endPoint: .bottomTrailing
                            ),
                            lineWidth: 1
                        )
                )
        }
    }
}

struct ExaminerPhraseBubble: View {
    let text: String

    var body: some View {
        HStack(alignment: .top, spacing: 10) {
            ZStack {
                Circle()
                    .fill(
                        LinearGradient(
                            colors: CategoryStyle.style(for: "phrases").gradient,
                            startPoint: .topLeading,
                            endPoint: .bottomTrailing
                        )
                    )
                    .frame(width: 36, height: 36)
                Image(systemName: "person.fill")
                    .font(.caption)
                    .foregroundStyle(.white)
            }
            VStack(alignment: .leading, spacing: 4) {
                Text(L10n.Flashcards.examinerSays)
                    .font(AppTheme.captionFont(11))
                    .foregroundStyle(.secondary)
                Text(text)
                    .font(AppTheme.bodyFont(14))
                    .foregroundStyle(AppTheme.roadNavy)
                    .italic()
            }
            Spacer(minLength: 0)
        }
        .padding(14)
        .background(
            RoundedRectangle(cornerRadius: 16, style: .continuous)
                .fill(Color(red: 0.95, green: 0.93, blue: 0.98))
        )
    }
}

struct NavCircleButton: View {
    let icon: String
    let enabled: Bool
    let action: () -> Void

    var body: some View {
        Button(action: action) {
            Image(systemName: icon)
                .font(.title2.weight(.semibold))
                .foregroundStyle(enabled ? AppTheme.roadNavy : .secondary.opacity(0.4))
                .frame(width: 56, height: 56)
                .background(
                    Circle()
                        .fill(AppTheme.cardWhite)
                        .shadow(color: AppTheme.cardShadow, radius: 8, y: 3)
                )
        }
        .buttonStyle(ScalePressButtonStyle())
        .disabled(!enabled)
    }
}
