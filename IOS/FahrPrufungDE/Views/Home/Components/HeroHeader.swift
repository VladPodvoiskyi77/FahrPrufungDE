import SwiftUI

struct HeroHeader: View {
    let termCount: Int
    let language: AppLanguage

    var body: some View {
        ZStack(alignment: .bottomLeading) {
            RoundedRectangle(cornerRadius: 28, style: .continuous)
                .fill(AppTheme.heroGradient)
                .frame(height: 200)
                .overlay(alignment: .topTrailing) {
                    ZStack {
                        Circle()
                            .fill(.white.opacity(0.08))
                            .frame(width: 120, height: 120)
                            .offset(x: 20, y: -20)
                        Circle()
                            .fill(.white.opacity(0.05))
                            .frame(width: 80, height: 80)
                            .offset(x: 60, y: 30)
                        Image(systemName: "car.side.fill")
                            .font(.system(size: 64))
                            .foregroundStyle(.white.opacity(0.15))
                            .offset(x: 24, y: 8)
                    }
                }
                .shadow(color: AppTheme.roadNavy.opacity(0.25), radius: 20, y: 10)

            VStack(alignment: .leading, spacing: 10) {
                HStack(spacing: 6) {
                    GermanFlagBadge()
                        .frame(width: 18, height: 12)
                    Text(L10n.Home.badge)
                        .font(AppTheme.captionFont(12))
                }
                .foregroundStyle(.white.opacity(0.85))
                .padding(.horizontal, 10)
                .padding(.vertical, 5)
                .background(Capsule().fill(.white.opacity(0.15)))

                Text(L10n.Home.title)
                    .font(AppTheme.titleFont(32))
                    .foregroundStyle(.white)

                Text(L10n.Home.subtitle)
                    .font(AppTheme.bodyFont(15))
                    .foregroundStyle(.white.opacity(0.88))

                HStack(spacing: 16) {
                    StatChip(value: "\(termCount)", label: L10n.Home.terms)
                    StatChip(value: language.flag, label: language.displayName)
                }
                .padding(.top, 4)
            }
            .padding(24)
        }
    }
}

private struct GermanFlagBadge: View {
    var body: some View {
        VStack(spacing: 0) {
            Color.black
            Color(red: 0.87, green: 0.11, blue: 0.15)
            Color(red: 1.0, green: 0.80, blue: 0.0)
        }
        .clipShape(RoundedRectangle(cornerRadius: 2, style: .continuous))
        .overlay {
            RoundedRectangle(cornerRadius: 2, style: .continuous)
                .strokeBorder(.white.opacity(0.35), lineWidth: 0.5)
        }
    }
}

private struct StatChip: View {
    let value: String
    let label: String

    var body: some View {
        VStack(alignment: .leading, spacing: 2) {
            Text(value)
                .font(AppTheme.headlineFont(16))
                .foregroundStyle(.white)
            Text(label)
                .font(AppTheme.captionFont(11))
                .foregroundStyle(.white.opacity(0.75))
        }
        .padding(.horizontal, 12)
        .padding(.vertical, 8)
        .background(
            RoundedRectangle(cornerRadius: 10, style: .continuous)
                .fill(.white.opacity(0.12))
        )
    }
}
