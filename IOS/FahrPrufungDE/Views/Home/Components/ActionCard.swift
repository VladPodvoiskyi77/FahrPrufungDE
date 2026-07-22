import SwiftUI

struct ActionCard: View {
    let title: String
    let subtitle: String
    let icon: String
    let colors: [Color]
    var badge: String? = nil

    var body: some View {
        HStack(spacing: 16) {
            ZStack {
                RoundedRectangle(cornerRadius: 14, style: .continuous)
                    .fill(
                        LinearGradient(
                            colors: colors,
                            startPoint: .topLeading,
                            endPoint: .bottomTrailing
                        )
                    )
                    .frame(width: 52, height: 52)
                Image(systemName: icon)
                    .font(.title2)
                    .foregroundStyle(.white)
            }

            VStack(alignment: .leading, spacing: 4) {
                Text(title)
                    .font(AppTheme.headlineFont())
                    .foregroundStyle(AppTheme.roadNavy)
                Text(subtitle)
                    .font(AppTheme.captionFont())
                    .foregroundStyle(.secondary)
                    .lineLimit(2)
            }

            Spacer(minLength: 0)

            if let badge {
                Text(badge)
                    .font(AppTheme.captionFont(11))
                    .foregroundStyle(AppTheme.highwayTeal)
                    .padding(.horizontal, 10)
                    .padding(.vertical, 5)
                    .background(
                        Capsule().fill(AppTheme.highwayTeal.opacity(0.12))
                    )
            }

            Image(systemName: "chevron.right")
                .font(.caption.weight(.bold))
                .foregroundStyle(AppTheme.signalAmber)
        }
        .padding(16)
        .appCard(accent: colors.first ?? AppTheme.highwayTeal)
    }
}
