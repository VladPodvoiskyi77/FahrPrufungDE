import SwiftUI

struct QuizProgressHeader: View {
    let current: Int
    let total: Int

    private var progress: Double {
        guard total > 0 else { return 0 }
        return Double(current) / Double(total)
    }

    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            HStack {
                Text(L10n.Quiz.question(current, total))
                    .font(AppTheme.captionFont())
                    .foregroundStyle(.secondary)
                Spacer()
                Image(systemName: "steeringwheel")
                    .foregroundStyle(AppTheme.signalAmber)
            }
            GeometryReader { geo in
                ZStack(alignment: .leading) {
                    Capsule().fill(AppTheme.roadNavy.opacity(0.08))
                    Capsule()
                        .fill(AppTheme.accentGradient)
                        .frame(width: geo.size.width * progress)
                }
            }
            .frame(height: 6)
            .animation(AppMotion.spring, value: progress)
        }
    }
}

struct QuizOptionCard: View {
    let text: String
    let letter: String
    let state: QuizOptionState

    enum QuizOptionState {
        case idle, correct, wrong, neutral
    }

    var body: some View {
        HStack(spacing: 14) {
            Text(letter)
                .font(AppTheme.headlineFont(14))
                .foregroundStyle(letterColor)
                .frame(width: 32, height: 32)
                .background(Circle().fill(letterBackground))

            Text(text)
                .font(AppTheme.bodyFont(15))
                .foregroundStyle(AppTheme.roadNavy)
                .multilineTextAlignment(.leading)

            Spacer()

            if state == .correct {
                Image(systemName: "checkmark.circle.fill")
                    .foregroundStyle(AppTheme.signalGreen)
            } else if state == .wrong {
                Image(systemName: "xmark.circle.fill")
                    .foregroundStyle(AppTheme.signalRed)
            }
        }
        .padding(16)
        .background(
            RoundedRectangle(cornerRadius: AppTheme.chipRadius, style: .continuous)
                .fill(backgroundColor)
                .overlay(
                    RoundedRectangle(cornerRadius: AppTheme.chipRadius, style: .continuous)
                        .strokeBorder(borderColor, lineWidth: state == .idle ? 0 : 2)
                )
        )
        .animation(AppMotion.quick, value: state)
    }

    private var backgroundColor: Color {
        switch state {
        case .idle: return AppTheme.cardWhite
        case .correct: return AppTheme.signalGreen.opacity(0.12)
        case .wrong: return AppTheme.signalRed.opacity(0.10)
        case .neutral: return AppTheme.cardWhite.opacity(0.6)
        }
    }

    private var borderColor: Color {
        switch state {
        case .correct: return AppTheme.signalGreen
        case .wrong: return AppTheme.signalRed
        default: return .clear
        }
    }

    private var letterColor: Color {
        state == .idle ? AppTheme.highwayTeal : .white
    }

    private var letterBackground: Color {
        state == .idle ? AppTheme.highwayTeal.opacity(0.12) : (state == .correct ? AppTheme.signalGreen : AppTheme.signalRed)
    }
}

struct QuizResultView: View {
    let score: Int
    let total: Int
    let onReview: () -> Void
    let onRetry: () -> Void

    @State private var revealed = false

    private var percentage: Double {
        guard total > 0 else { return 0 }
        return Double(score) / Double(total)
    }

    private var message: String {
        switch percentage {
        case 0.9...: return L10n.Quiz.Result.perfect
        case 0.7..<0.9: return L10n.Quiz.Result.great
        case 0.5..<0.7: return L10n.Quiz.Result.good
        default: return L10n.Quiz.Result.keepGoing
        }
    }

    var body: some View {
        VStack(spacing: 28) {
            ZStack {
                Circle()
                    .stroke(AppTheme.roadNavy.opacity(0.08), lineWidth: 12)
                    .frame(width: 140, height: 140)
                Circle()
                    .trim(from: 0, to: revealed ? percentage : 0)
                    .stroke(
                        AppTheme.accentGradient,
                        style: StrokeStyle(lineWidth: 12, lineCap: .round)
                    )
                    .frame(width: 140, height: 140)
                    .rotationEffect(.degrees(-90))

                VStack(spacing: 2) {
                    Text("\(score)/\(total)")
                        .font(AppTheme.titleFont(28))
                        .foregroundStyle(AppTheme.roadNavy)
                    Text(L10n.Quiz.correct)
                        .font(AppTheme.captionFont())
                        .foregroundStyle(.secondary)
                }
                .scaleEffect(revealed ? 1 : 0.85)
                .opacity(revealed ? 1 : 0)
            }

            VStack(spacing: 8) {
                Image(systemName: percentage >= 0.7 ? "checkmark.seal.fill" : "arrow.clockwise.circle.fill")
                    .font(.largeTitle)
                    .foregroundStyle(percentage >= 0.7 ? AppTheme.signalGreen : AppTheme.signalAmber)
                    .symbolEffect(.bounce, value: revealed)
                Text(message)
                    .font(AppTheme.headlineFont(18))
                    .foregroundStyle(AppTheme.roadNavy)
                    .multilineTextAlignment(.center)
            }
            .offset(y: revealed ? 0 : 12)
            .opacity(revealed ? 1 : 0)

            VStack(spacing: 12) {
                Button(action: onReview) {
                    Text(L10n.Quiz.reviewAnswers)
                        .font(AppTheme.headlineFont())
                        .foregroundStyle(AppTheme.highwayTeal)
                        .frame(maxWidth: .infinity)
                        .padding(.vertical, 14)
                        .background(
                            RoundedRectangle(cornerRadius: AppTheme.chipRadius, style: .continuous)
                                .stroke(AppTheme.highwayTeal, lineWidth: 2)
                        )
                }

                Button(L10n.Common.retry, action: onRetry)
                    .buttonStyle(PrimaryButtonStyle())
            }
            .padding(.horizontal, 40)
            .opacity(revealed ? 1 : 0)
        }
        .padding(32)
        .onAppear {
            withAnimation(AppMotion.spring.delay(0.1)) {
                revealed = true
            }
        }
    }
}

struct QuizReviewView: View {
    let records: [QuizAnswerRecord]

    var body: some View {
        ScrollView {
            VStack(spacing: 12) {
                ForEach(records) { record in
                    QuizReviewRow(record: record)
                        .staggeredAppear(index: min(record.id, 8))
                }
            }
            .padding(20)
        }
        .appScreenBackground()
        .navigationTitle(L10n.Quiz.reviewTitle)
        .navigationBarTitleDisplayMode(.inline)
    }
}

private struct QuizReviewRow: View {
    let record: QuizAnswerRecord

    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            HStack(alignment: .top) {
                Text(L10n.Quiz.reviewQuestion(record.id + 1))
                    .font(AppTheme.captionFont())
                    .foregroundStyle(.secondary)
                Spacer()
                Image(systemName: record.isCorrect ? "checkmark.circle.fill" : "xmark.circle.fill")
                    .foregroundStyle(record.isCorrect ? AppTheme.signalGreen : AppTheme.signalRed)
            }

            Text(record.prompt)
                .font(AppTheme.headlineFont())
                .foregroundStyle(AppTheme.roadNavy)

            VStack(alignment: .leading, spacing: 6) {
                Text(L10n.Quiz.yourAnswer)
                    .font(AppTheme.captionFont(11))
                    .foregroundStyle(.secondary)
                Text(record.selectedText)
                    .font(AppTheme.bodyFont(15))
                    .foregroundStyle(record.isCorrect ? AppTheme.signalGreen : AppTheme.signalRed)
            }

            if !record.isCorrect {
                VStack(alignment: .leading, spacing: 6) {
                    Text(L10n.Quiz.correctAnswer)
                        .font(AppTheme.captionFont(11))
                        .foregroundStyle(.secondary)
                    Text(record.correctText)
                        .font(AppTheme.bodyFont(15))
                        .foregroundStyle(AppTheme.signalGreen)
                }
            }
        }
        .padding(16)
        .appCard(accent: record.isCorrect ? AppTheme.signalGreen : AppTheme.signalRed)
    }
}
