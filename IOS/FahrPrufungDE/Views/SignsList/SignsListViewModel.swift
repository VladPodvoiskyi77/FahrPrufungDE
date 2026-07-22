import Combine
import Foundation

@MainActor
final class SignsListViewModel: ObservableObject {
    @Published var searchText = "" {
        didSet { recomputeFilteredSigns() }
    }
    @Published var selectedCategory: String? {
        didSet { recomputeFilteredSigns() }
    }
    @Published private(set) var filteredSigns: [TrafficSign] = []

    private let store: DataStore
    private var cancellables = Set<AnyCancellable>()

    init(store: DataStore) {
        self.store = store
        store.$signs
            .dropFirst()
            .sink { [weak self] _ in
                self?.recomputeFilteredSigns()
            }
            .store(in: &cancellables)
        recomputeFilteredSigns()
    }

    var language: AppLanguage { store.nativeLanguage }
    var signCount: Int { store.signs.count }
    var categories: [SignCategoryInfo] { store.signCategories }

    var heroSign: TrafficSign? {
        store.signs.first { $0.stvoCode == "206" }
            ?? store.signs.first { $0.category == "prohibitory" }
            ?? store.signs.first
    }

    func isKnown(_ sign: TrafficSign) -> Bool {
        store.isSignKnown(sign.id)
    }

    func toggleKnown(_ sign: TrafficSign) {
        if store.isSignKnown(sign.id) {
            store.knownUndo.dismiss()
            store.setSignKnown(sign.id, known: false)
        } else {
            store.markSignAsKnown(sign.id)
        }
    }

    var knownCount: Int {
        store.knownItems.knownSignCount
    }

    private func recomputeFilteredSigns() {
        var result = store.signs
        if let selectedCategory {
            result = result.filter { $0.category == selectedCategory }
        }
        if !searchText.isEmpty {
            let query = searchText.lowercased()
            result = result.filter {
                $0.de.lowercased().contains(query)
                    || $0.translation(for: store.nativeLanguage).lowercased().contains(query)
                    || ($0.stvoCode?.lowercased().contains(query) ?? false)
            }
        }
        filteredSigns = result
    }
}
