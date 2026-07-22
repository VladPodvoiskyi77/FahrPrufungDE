import Foundation

@MainActor
final class SignDetailViewModel: ObservableObject {
    let sign: TrafficSign
    private let store: DataStore

    init(sign: TrafficSign, store: DataStore) {
        self.sign = sign
        self.store = store
    }

    var language: AppLanguage { store.nativeLanguage }
    var title: String { sign.translation(for: store.nativeLanguage) }

    var note: String? {
        guard let note = sign.note(for: store.nativeLanguage) else { return nil }
        let title = sign.translation(for: store.nativeLanguage)
        if note == sign.de || note == title { return nil }
        return note
    }

    var categoryLabel: String {
        store.signCategories.first { $0.id == sign.category }?
            .title(for: store.nativeLanguage) ?? sign.category
    }
}
