import SwiftUI

struct KnownMarkButton: View {
    let isKnown: Bool
    var style: KnownMarkStyle = .prominent
    let action: () -> Void

    enum KnownMarkStyle {
        case prominent
        case compact
    }

    var body: some View {
        Button(action: action) {
            switch style {
            case .prominent:
                prominentBody
            case .compact:
                compactBody
            }
        }
        .buttonStyle(.plain)
        .accessibilityLabel(isKnown ? L10n.Known.unmarkTitle : L10n.Known.markTitle)
    }

    private var prominentBody: some View {
        HStack(spacing: 12) {
            Image(systemName: isKnown ? "checkmark.circle.fill" : "circle")
                .font(.title3)
                .foregroundStyle(isKnown ? AppTheme.signalGreen : AppTheme.roadNavy.opacity(0.35))

            VStack(alignment: .leading, spacing: 2) {
                Text(isKnown ? L10n.Known.unmarkTitle : L10n.Known.markTitle)
                    .font(AppTheme.headlineFont(15))
                    .foregroundStyle(AppTheme.roadNavy)
                if !isKnown {
                    Text(L10n.Known.markSubtitle)
                        .font(AppTheme.captionFont(12))
                        .foregroundStyle(.secondary)
                }
            }
            Spacer(minLength: 0)
        }
        .padding(14)
        .background(
            RoundedRectangle(cornerRadius: AppTheme.chipRadius, style: .continuous)
                .fill(isKnown ? AppTheme.signalGreen.opacity(0.08) : AppTheme.cardWhite)
                .shadow(color: AppTheme.cardShadow, radius: 6, y: 2)
        )
        .overlay {
            RoundedRectangle(cornerRadius: AppTheme.chipRadius, style: .continuous)
                .strokeBorder(
                    isKnown ? AppTheme.signalGreen.opacity(0.25) : AppTheme.roadNavy.opacity(0.08),
                    lineWidth: 1
                )
        }
    }

    private var compactBody: some View {
        Image(systemName: isKnown ? "checkmark.circle.fill" : "circle")
            .font(.title3)
            .foregroundStyle(isKnown ? AppTheme.signalGreen : AppTheme.roadNavy.opacity(0.25))
            .frame(width: 36, height: 36)
    }
}

extension View {
    func knownDimmed(_ isKnown: Bool) -> some View {
        opacity(isKnown ? 0.42 : 1)
    }
}
