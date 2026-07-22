import SwiftUI

struct ProgressSummaryCard: View {
    let knownTerms: Int
    let totalTerms: Int
    let knownSigns: Int
    let totalSigns: Int
    let streak: Int
    let termPercent: Int

    var body: some View {
        VStack(alignment: .leading, spacing: 14) {
            HStack(spacing: 12) {
                ZStack {
                    RoundedRectangle(cornerRadius: 14, style: .continuous)
                        .fill(
                            LinearGradient(
                                colors: [AppTheme.highwayTeal, AppTheme.roadNavy],
                                startPoint: .topLeading,
                                endPoint: .bottomTrailing
                            )
                        )
                        .frame(width: 48, height: 48)
                    Image(systemName: "chart.bar.fill")
                        .font(.title3)
                        .foregroundStyle(.white)
                }

                VStack(alignment: .leading, spacing: 2) {
                    Text(L10n.Progress.title)
                        .font(AppTheme.headlineFont())
                        .foregroundStyle(AppTheme.roadNavy)
                    Text(L10n.Progress.homeTapHint)
                        .font(AppTheme.captionFont(11))
                        .foregroundStyle(.secondary)
                }

                Spacer(minLength: 0)

                Text("\(termPercent)%")
                    .font(AppTheme.titleFont(22))
                    .foregroundStyle(AppTheme.highwayTeal)

                Image(systemName: "chevron.right")
                    .font(.caption.weight(.bold))
                    .foregroundStyle(AppTheme.signalAmber)
            }

            VStack(alignment: .leading, spacing: 6) {
                Text(L10n.Progress.homeSummary(knownTerms, totalTerms))
                    .font(AppTheme.bodyFont(14))
                    .foregroundStyle(AppTheme.roadNavy.opacity(0.85))
                Text(L10n.Progress.homeSignsSummary(knownSigns, totalSigns))
                    .font(AppTheme.captionFont())
                    .foregroundStyle(.secondary)
            }

            GeometryReader { geo in
                ZStack(alignment: .leading) {
                    Capsule().fill(AppTheme.highwayTeal.opacity(0.12))
                    Capsule()
                        .fill(AppTheme.highwayTeal)
                        .frame(width: geo.size.width * CGFloat(termPercent) / 100)
                }
            }
            .frame(height: 8)
            .animation(AppMotion.spring, value: termPercent)

            if streak > 0 {
                Label(L10n.Progress.streakDays(streak), systemImage: "flame.fill")
                    .font(AppTheme.captionFont(12))
                    .foregroundStyle(AppTheme.signalAmber)
                    .symbolEffect(.bounce, value: streak)
                    .animation(AppMotion.spring, value: streak)
            }
        }
        .padding(16)
        .appCard(accent: AppTheme.highwayTeal)
    }
}
