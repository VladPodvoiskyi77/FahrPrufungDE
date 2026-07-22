import SwiftUI

struct InfoTile: View {
    let value: String
    let label: String
    let icon: String
    let color: Color
    var wide: Bool = false

    var body: some View {
        HStack(spacing: 12) {
            Image(systemName: icon)
                .font(.title3)
                .foregroundStyle(color)
                .frame(width: 36)
            VStack(alignment: .leading, spacing: 2) {
                Text(value)
                    .font(AppTheme.headlineFont(18))
                    .foregroundStyle(AppTheme.roadNavy)
                Text(label)
                    .font(AppTheme.captionFont(11))
                    .foregroundStyle(.secondary)
            }
            if !wide { Spacer() }
        }
        .padding(14)
        .frame(maxWidth: wide ? .infinity : nil)
        .appCard(accent: color)
    }
}
