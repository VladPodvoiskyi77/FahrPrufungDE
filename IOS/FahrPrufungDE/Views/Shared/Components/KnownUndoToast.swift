import SwiftUI

struct KnownUndoToast: View {
    @ObservedObject var controller: KnownUndoController

    var body: some View {
        if controller.isVisible {
            HStack(spacing: 12) {
                Image(systemName: "eye.slash.fill")
                    .font(.subheadline)
                    .foregroundStyle(.white.opacity(0.9))

                Text(controller.message)
                    .font(AppTheme.bodyFont(14))
                    .foregroundStyle(.white)
                    .lineLimit(2)

                Spacer(minLength: 8)

                Button(L10n.Known.undoAction) {
                    controller.performUndo()
                }
                .font(AppTheme.headlineFont(14))
                .foregroundStyle(AppTheme.signalAmber)
            }
            .padding(.horizontal, 16)
            .padding(.vertical, 14)
            .background(
                RoundedRectangle(cornerRadius: 14, style: .continuous)
                    .fill(AppTheme.roadNavy.opacity(0.92))
                    .shadow(color: .black.opacity(0.2), radius: 12, y: 4)
            )
            .padding(.horizontal, 20)
            .padding(.bottom, 8)
            .transition(.move(edge: .bottom).combined(with: .opacity))
        }
    }
}
