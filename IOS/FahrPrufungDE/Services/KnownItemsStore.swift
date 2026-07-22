import Foundation

@MainActor
final class KnownItemsStore {
    private static let termsKey = "knownTermIDs"
    private static let signsKey = "knownSignIDs"

    private(set) var knownTermIDs: Set<String>
    private(set) var knownSignIDs: Set<String>

    var onChange: (() -> Void)?

    init() {
        knownTermIDs = Set(UserDefaults.standard.stringArray(forKey: Self.termsKey) ?? [])
        knownSignIDs = Set(UserDefaults.standard.stringArray(forKey: Self.signsKey) ?? [])
    }

    var knownTermCount: Int { knownTermIDs.count }
    var knownSignCount: Int { knownSignIDs.count }

    func isTermKnown(_ id: String) -> Bool { knownTermIDs.contains(id) }
    func isSignKnown(_ id: String) -> Bool { knownSignIDs.contains(id) }

    func setTermKnown(_ id: String, known: Bool) {
        if known {
            knownTermIDs.insert(id)
        } else {
            knownTermIDs.remove(id)
        }
        persist(knownTermIDs, key: Self.termsKey)
        onChange?()
    }

    func setSignKnown(_ id: String, known: Bool) {
        if known {
            knownSignIDs.insert(id)
        } else {
            knownSignIDs.remove(id)
        }
        persist(knownSignIDs, key: Self.signsKey)
        onChange?()
    }

    func resetAll() {
        knownTermIDs = []
        knownSignIDs = []
        UserDefaults.standard.removeObject(forKey: Self.termsKey)
        UserDefaults.standard.removeObject(forKey: Self.signsKey)
        onChange?()
    }

    private func persist(_ ids: Set<String>, key: String) {
        UserDefaults.standard.set(Array(ids), forKey: key)
    }
}
