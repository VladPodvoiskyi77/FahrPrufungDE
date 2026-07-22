import SwiftUI

/// Subtle road motif — dashed center line at the bottom of the screen.
struct RoadDecoration: View {
    var body: some View {
        GeometryReader { geo in
            ZStack(alignment: .bottom) {
                // Soft horizon glow
                Ellipse()
                    .fill(
                        RadialGradient(
                            colors: [
                                AppTheme.highwayTeal.opacity(0.06),
                                .clear
                            ],
                            center: .center,
                            startRadius: 0,
                            endRadius: geo.size.width * 0.6
                        )
                    )
                    .frame(width: geo.size.width * 1.2, height: geo.size.height * 0.35)
                    .offset(y: geo.size.height * 0.15)

                // Road surface strip
                RoundedRectangle(cornerRadius: 24, style: .continuous)
                    .fill(
                        LinearGradient(
                            colors: [
                                AppTheme.asphalt.opacity(0.04),
                                AppTheme.asphalt.opacity(0.08)
                            ],
                            startPoint: .top,
                            endPoint: .bottom
                        )
                    )
                    .frame(height: 56)
                    .padding(.horizontal, 32)
                    .padding(.bottom, 8)

                // Dashed lane divider
                HStack(spacing: 14) {
                    ForEach(0..<Int(geo.size.width / 30), id: \.self) { _ in
                        Capsule()
                            .fill(AppTheme.signalAmber.opacity(0.35))
                            .frame(width: 18, height: 3)
                    }
                }
                .padding(.bottom, 34)
            }
        }
    }
}

struct RoadDashedLine: View {
    var body: some View {
        GeometryReader { geo in
            HStack(spacing: 8) {
                ForEach(0..<max(1, Int(geo.size.width / 20)), id: \.self) { _ in
                    Capsule()
                        .fill(AppTheme.signalAmber.opacity(0.5))
                        .frame(width: 12, height: 2)
                }
            }
        }
        .frame(height: 4)
    }
}
