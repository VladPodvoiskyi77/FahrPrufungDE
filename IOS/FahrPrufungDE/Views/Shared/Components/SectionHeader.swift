import SwiftUI

struct SectionHeader: View {
    let title: String
    var icon: String? = nil

    var body: some View {
        HStack(spacing: 8) {
            if let icon {
                Image(systemName: icon)
                    .foregroundStyle(AppTheme.signalAmber)
            }
            Text(title.uppercased())
                .font(AppTheme.captionFont(12))
                .tracking(1.2)
                .foregroundStyle(AppTheme.roadNavy.opacity(0.55))
            RoadDashedLine()
        }
        .padding(.top, 8)
        .padding(.bottom, 4)
    }
}
