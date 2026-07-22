import SwiftUI

/// Displays the real StVO PNG from bundle, or a vector fallback.
struct SignPlaceholderView: View {
    let sign: TrafficSign
    var size: CGFloat = 80

    var body: some View {
        Group {
            if let uiImage = SignImageLoader.image(for: sign) {
                Image(uiImage: uiImage)
                    .resizable()
                    .scaledToFit()
                    .padding(6)
            } else {
                VectorSignFallback(sign: sign, size: size)
            }
        }
        .frame(width: size, height: size)
        .background(
            RoundedRectangle(cornerRadius: 14, style: .continuous)
                .fill(Color.white)
                .shadow(color: .black.opacity(0.08), radius: 6, y: 2)
        )
    }
}

private struct VectorSignFallback: View {
    let sign: TrafficSign
    let size: CGFloat

    var body: some View {
        ZStack {
            RoundedRectangle(cornerRadius: 8)
                .fill(SignStyle.categoryColor(sign.category).opacity(0.12))
            Image(systemName: SignStyle.categoryIcon(sign.category))
                .font(.system(size: size * 0.32))
                .foregroundStyle(SignStyle.categoryColor(sign.category))
        }
        .padding(8)
    }
}

enum SignStyle {
    static func categoryColor(_ category: String) -> Color {
        switch category {
        case "vorfahrt", "warning", "danger": return AppTheme.signalAmber
        case "speed", "prohibitory", "prohibition": return AppTheme.signalRed
        case "direction", "mandatory": return AppTheme.highwayTeal
        case "pedestrian": return AppTheme.signalGreen
        case "additional": return AppTheme.roadNavy
        default: return AppTheme.roadNavy
        }
    }

    static func categoryIcon(_ category: String) -> String {
        switch category {
        case "vorfahrt": return "arrow.triangle.merge"
        case "warning", "danger": return "exclamationmark.triangle.fill"
        case "speed": return "speedometer"
        case "prohibitory", "prohibition": return "nosign"
        case "direction": return "arrow.turn.up.right"
        case "pedestrian": return "figure.walk"
        case "mandatory": return "arrow.right.circle.fill"
        case "additional": return "plus.rectangle.fill"
        default: return "signpost.right.fill"
        }
    }
}
