import SwiftUI

struct CoreTermBadge: View {
    @State private var showHint = false

    var body: some View {
        Button {
            showHint = true
        } label: {
            Image(systemName: "star.fill")
                .font(.caption)
                .foregroundStyle(AppTheme.signalAmber)
                .frame(width: 28, height: 28)
                .contentShape(Rectangle())
        }
        .buttonStyle(.plain)
        .accessibilityLabel(L10n.CoreTerm.hintTitle)
        .accessibilityHint(L10n.CoreTerm.hintMessage)
        .popover(isPresented: $showHint, arrowEdge: .top) {
            VStack(alignment: .leading, spacing: 10) {
                Label {
                    Text(L10n.CoreTerm.hintTitle)
                        .font(AppTheme.headlineFont(15))
                        .foregroundStyle(AppTheme.roadNavy)
                } icon: {
                    Image(systemName: "star.fill")
                        .foregroundStyle(AppTheme.signalAmber)
                }

                Text(L10n.CoreTerm.hintMessage)
                    .font(AppTheme.bodyFont(14))
                    .foregroundStyle(.secondary)
                    .fixedSize(horizontal: false, vertical: true)
            }
            .padding(16)
            .frame(maxWidth: 280, alignment: .leading)
            .presentationCompactAdaptation(.popover)
        }
    }
}
