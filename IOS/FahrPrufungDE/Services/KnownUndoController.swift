import Foundation

@MainActor
final class KnownUndoController: ObservableObject {
    @Published private(set) var isVisible = false
    @Published private(set) var message = ""

    var onChange: (() -> Void)?

    private var undoAction: (() -> Void)?
    private var dismissTask: Task<Void, Never>?

    private static let displayNanoseconds: UInt64 = 3_000_000_000

    func offerUndo(message: String, undo: @escaping () -> Void) {
        dismissTask?.cancel()
        undoAction = undo
        self.message = message
        isVisible = true
        notifyChange()

        dismissTask = Task { [weak self] in
            try? await Task.sleep(nanoseconds: Self.displayNanoseconds)
            guard !Task.isCancelled else { return }
            await MainActor.run {
                self?.dismiss()
            }
        }
    }

    func performUndo() {
        undoAction?()
        dismiss()
    }

    func dismiss() {
        dismissTask?.cancel()
        dismissTask = nil
        undoAction = nil
        guard isVisible else { return }
        isVisible = false
        message = ""
        notifyChange()
    }

    private func notifyChange() {
        onChange?()
    }
}
