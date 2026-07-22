import Foundation
import SwiftUI

@MainActor
final class DataStore: ObservableObject {
    @Published private(set) var categories: [VocabularyCategory] = []
    @Published private(set) var terms: [VocabularyTerm] = []
    @Published private(set) var signs: [TrafficSign] = []
    @Published private(set) var signCategories: [SignCategoryInfo] = []
    @Published private(set) var loadError: String?
    @Published private(set) var isLoading = false

    let knownItems = KnownItemsStore()
    let knownUndo = KnownUndoController()
    let learningStats = LearningStatsStore()

    @Published var nativeLanguage: AppLanguage {
        didSet {
            UserDefaults.standard.set(nativeLanguage.rawValue, forKey: Self.languageKey)
            LocalizationManager.shared.language = nativeLanguage
            if oldValue != nativeLanguage {
                AnalyticsService.shared.logLanguageChanged(language: nativeLanguage)
            }
        }
    }

    private static let languageKey = "nativeLanguage"
    private var loadTask: Task<Void, Never>?

    init() {
        let saved = UserDefaults.standard.string(forKey: Self.languageKey)
        let language = saved.flatMap(AppLanguage.init(rawValue:)) ?? AppLanguage.systemDefault
        nativeLanguage = language
        LocalizationManager.shared.language = language
        knownItems.onChange = { [weak self] in
            self?.objectWillChange.send()
        }
        knownUndo.onChange = { [weak self] in
            self?.objectWillChange.send()
        }
        learningStats.onChange = { [weak self] in
            self?.objectWillChange.send()
        }
    }

    var coreTerms: [VocabularyTerm] {
        terms.filter(\.isCore)
    }

    func learningTerms(from terms: [VocabularyTerm]) -> [VocabularyTerm] {
        terms.filter { !knownItems.isTermKnown($0.id) }
    }

    func learningSigns(from signs: [TrafficSign]) -> [TrafficSign] {
        signs.filter { !knownItems.isSignKnown($0.id) }
    }

    func isTermKnown(_ id: String) -> Bool { knownItems.isTermKnown(id) }
    func isSignKnown(_ id: String) -> Bool { knownItems.isSignKnown(id) }

    func setTermKnown(_ id: String, known: Bool) {
        knownItems.setTermKnown(id, known: known)
    }

    func setSignKnown(_ id: String, known: Bool) {
        knownItems.setSignKnown(id, known: known)
    }

    func markTermAsKnown(_ id: String, onUndo: (() -> Void)? = nil) {
        guard !isTermKnown(id) else { return }
        setTermKnown(id, known: true)
        if let term = terms.first(where: { $0.id == id }) {
            AnalyticsService.shared.logTermMarkedKnown(categoryID: term.category)
        }
        knownUndo.offerUndo(message: L10n.Known.undoMessage) { [weak self] in
            self?.setTermKnown(id, known: false)
            onUndo?()
        }
    }

    func markSignAsKnown(_ id: String) {
        guard !isSignKnown(id) else { return }
        setSignKnown(id, known: true)
        let stvoCode = signs.first(where: { $0.id == id })?.stvoCode
        AnalyticsService.shared.logSignMarkedKnown(stvoCode: stvoCode)
        knownUndo.offerUndo(message: L10n.Known.undoMessage) { [weak self] in
            self?.setSignKnown(id, known: false)
        }
    }

    func resetKnownItems() {
        knownUndo.dismiss()
        knownItems.resetAll()
        AnalyticsService.shared.logKnownReset()
    }

    func knownTermCount(in categoryID: String) -> Int {
        terms(for: categoryID).filter { knownItems.isTermKnown($0.id) }.count
    }

    func categoryProgress(for category: VocabularyCategory) -> (known: Int, total: Int) {
        let categoryTerms = terms(for: category.id)
        let known = categoryTerms.filter { knownItems.isTermKnown($0.id) }.count
        return (known, categoryTerms.count)
    }

    func loadIfNeeded() {
        guard terms.isEmpty, loadError == nil, !isLoading else { return }
        loadTask?.cancel()
        isLoading = true
        loadTask = Task {
            do {
                let payload = try await Self.loadContent()
                guard !Task.isCancelled else { return }
                categories = payload.categories
                terms = payload.terms
                signs = payload.signs
                signCategories = payload.signCategories
                loadError = nil
            } catch {
                guard !Task.isCancelled else { return }
                loadError = Self.userFacingMessage(for: error)
            }
            isLoading = false
        }
    }

    private struct LoadedContent: Sendable {
        let categories: [VocabularyCategory]
        let terms: [VocabularyTerm]
        let signs: [TrafficSign]
        let signCategories: [SignCategoryInfo]
    }

    private nonisolated static func loadContent() async throws -> LoadedContent {
        try await Task.detached(priority: .userInitiated) {
            let vocabulary: VocabularyBundle = try loadJSON("vocabulary")
            let signsBundle: SignsBundle = try loadJSON("signs")
            let signCategories = signsBundle.categories ?? defaultSignCategories(for: signsBundle.signs)
            return LoadedContent(
                categories: vocabulary.categories,
                terms: vocabulary.terms,
                signs: signsBundle.signs,
                signCategories: signCategories
            )
        }.value
    }

    private static func userFacingMessage(for error: Error) -> String {
        if let dataError = error as? DataStoreError {
            return dataError.localizedDescription ?? error.localizedDescription
        }
        if let decoding = error as? DecodingError {
            switch decoding {
            case .keyNotFound(let key, let context):
                return "JSON-Fehler: Feld «\(key.stringValue)» fehlt (\(context.codingPath.map(\.stringValue).joined(separator: ".")))"
            case .typeMismatch(let type, let context):
                return "JSON-Fehler: falscher Typ für \(type) (\(context.codingPath.map(\.stringValue).joined(separator: ".")))"
            case .valueNotFound(let type, let context):
                return "JSON-Fehler: Wert \(type) fehlt (\(context.codingPath.map(\.stringValue).joined(separator: ".")))"
            case .dataCorrupted(let context):
                return "JSON-Fehler: beschädigte Daten — \(context.debugDescription)"
            @unknown default:
                return decoding.localizedDescription
            }
        }
        return error.localizedDescription
    }

    func terms(for categoryID: String) -> [VocabularyTerm] {
        terms.filter { $0.category == categoryID }
    }

    func category(for id: String) -> VocabularyCategory? {
        categories.first { $0.id == id }
    }

    private nonisolated static func defaultSignCategories(for signs: [TrafficSign]) -> [SignCategoryInfo] {
        let ids = Set(signs.map(\.category))
        return ids.sorted().map { id in
            SignCategoryInfo(id: id, de: id, ru: id, en: id, uk: id, fr: id, tr: id)
        }
    }

    private nonisolated static func loadJSON<T: Decodable>(_ name: String) throws -> T {
        guard let url = Bundle.main.url(forResource: name, withExtension: "json") else {
            throw DataStoreError.fileNotFound(name)
        }
        let data = try Data(contentsOf: url)
        let decoder = JSONDecoder()
        return try decoder.decode(T.self, from: data)
    }
}

enum DataStoreError: LocalizedError {
    case fileNotFound(String)

    var errorDescription: String? {
        switch self {
        case .fileNotFound(let name):
            return "Datei nicht gefunden: \(name).json"
        }
    }
}
