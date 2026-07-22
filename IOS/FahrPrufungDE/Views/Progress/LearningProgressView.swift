import SwiftUI

struct LearningProgressView: View {
    @StateObject var viewModel: ProgressViewModel

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 20) {
                overallSection
                    .staggeredAppear(index: 0)
                if viewModel.studyStreak > 0 {
                    streakCard
                        .staggeredAppear(index: 1)
                }
                categoriesSection
                    .staggeredAppear(index: 2)
                quizHistorySection
                    .staggeredAppear(index: 3)
            }
            .padding(.horizontal, 20)
            .padding(.bottom, 32)
        }
        .appScreenBackground()
        .navigationTitle(L10n.Progress.title)
        .navigationBarTitleDisplayMode(.large)
        .onAppear {
            AnalyticsService.shared.logProgressViewed()
            AnalyticsService.shared.logScreen("progress")
        }
    }

    private var overallSection: some View {
        VStack(alignment: .leading, spacing: 12) {
            SectionHeader(title: L10n.Progress.overall, icon: "chart.bar.fill")

            VStack(spacing: 10) {
                ProgressRingRow(
                    title: L10n.Progress.terms,
                    known: viewModel.knownTermCount,
                    total: viewModel.totalTermCount,
                    percent: viewModel.overallTermPercent,
                    color: AppTheme.highwayTeal
                )
                ProgressRingRow(
                    title: L10n.Progress.signs,
                    known: viewModel.knownSignCount,
                    total: viewModel.totalSignCount,
                    percent: viewModel.overallSignPercent,
                    color: AppTheme.signalAmber
                )
            }
        }
    }

    private var streakCard: some View {
        HStack(spacing: 14) {
            Image(systemName: "flame.fill")
                .font(.title2)
                .foregroundStyle(AppTheme.signalAmber)
                .symbolEffect(.pulse, options: .repeating)
            VStack(alignment: .leading, spacing: 4) {
                Text(L10n.Progress.streak)
                    .font(AppTheme.captionFont())
                    .foregroundStyle(.secondary)
                Text(L10n.Progress.streakDays(viewModel.studyStreak))
                    .font(AppTheme.headlineFont())
                    .foregroundStyle(AppTheme.roadNavy)
                    .contentTransition(.numericText())
            }
            Spacer()
        }
        .padding(16)
        .appCard(accent: AppTheme.signalAmber)
        .animation(AppMotion.spring, value: viewModel.studyStreak)
    }

    private var categoriesSection: some View {
        VStack(alignment: .leading, spacing: 12) {
            SectionHeader(title: L10n.Progress.byCategory, icon: "folder.fill")

            VStack(spacing: 8) {
                ForEach(viewModel.categoryItems) { item in
                    CategoryProgressRow(item: item)
                }
            }
        }
    }

    @ViewBuilder
    private var quizHistorySection: some View {
        VStack(alignment: .leading, spacing: 12) {
            SectionHeader(title: L10n.Progress.recentQuizzes, icon: "brain.head.profile")

            if viewModel.recentQuizResults.isEmpty {
                Text(L10n.Progress.noQuizzesYet)
                    .font(AppTheme.bodyFont(15))
                    .foregroundStyle(.secondary)
                    .frame(maxWidth: .infinity, alignment: .leading)
                    .padding(16)
                    .appCard(accent: AppTheme.roadNavy)
            } else {
                VStack(spacing: 8) {
                    ForEach(viewModel.recentQuizResults.prefix(5)) { result in
                        QuizResultRow(result: result)
                    }
                }
            }
        }
    }
}

private struct ProgressRingRow: View {
    let title: String
    let known: Int
    let total: Int
    let percent: Int
    let color: Color

    var body: some View {
        HStack(spacing: 16) {
            ZStack {
                Circle()
                    .stroke(color.opacity(0.15), lineWidth: 6)
                Circle()
                    .trim(from: 0, to: CGFloat(percent) / 100)
                    .stroke(color, style: StrokeStyle(lineWidth: 6, lineCap: .round))
                    .rotationEffect(.degrees(-90))
                    .animation(AppMotion.spring, value: percent)
                Text("\(percent)%")
                    .font(AppTheme.captionFont(12))
                    .foregroundStyle(AppTheme.roadNavy)
                    .contentTransition(.numericText())
            }
            .frame(width: 52, height: 52)

            VStack(alignment: .leading, spacing: 4) {
                Text(title)
                    .font(AppTheme.headlineFont())
                    .foregroundStyle(AppTheme.roadNavy)
                Text(L10n.Progress.learnedCount(known, total))
                    .font(AppTheme.captionFont())
                    .foregroundStyle(.secondary)
            }
            Spacer()
        }
        .padding(14)
        .appCard(accent: color)
    }
}

private struct CategoryProgressRow: View {
    let item: CategoryProgressItem

    private var color: Color {
        CategoryStyle.style(for: item.colorName).color
    }

    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            HStack {
                Text(item.title)
                    .font(AppTheme.bodyFont(15))
                    .foregroundStyle(AppTheme.roadNavy)
                Spacer()
                Text(L10n.Progress.learnedCount(item.known, item.total))
                    .font(AppTheme.captionFont())
                    .foregroundStyle(.secondary)
            }

            GeometryReader { geo in
                ZStack(alignment: .leading) {
                    Capsule().fill(color.opacity(0.12))
                    Capsule()
                        .fill(color)
                        .frame(width: geo.size.width * item.fraction)
                }
            }
            .frame(height: 8)
        }
        .padding(14)
        .appCard(accent: color)
    }
}

private struct QuizResultRow: View {
    let result: QuizResultRecord

    var body: some View {
        HStack {
            VStack(alignment: .leading, spacing: 4) {
                Text(result.sessionTitle)
                    .font(AppTheme.bodyFont(15))
                    .foregroundStyle(AppTheme.roadNavy)
                    .lineLimit(1)
                Text(result.date, style: .date)
                    .font(AppTheme.captionFont(11))
                    .foregroundStyle(.secondary)
            }
            Spacer()
            Text(L10n.Progress.quizScore(result.score, result.total))
                .font(AppTheme.headlineFont(15))
                .foregroundStyle(result.score == result.total ? AppTheme.signalGreen : AppTheme.highwayTeal)
        }
        .padding(14)
        .appCard(accent: AppTheme.highwayTeal)
    }
}
