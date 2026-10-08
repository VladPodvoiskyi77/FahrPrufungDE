import XCTest
@testable import FahrPrufungDE

@MainActor
final class OnboardingAndContentTests: XCTestCase {
    func testOnboardingCompletedKeyConstant() {
        XCTAssertEqual(OnboardingViewModel.completedKey, "hasCompletedOnboarding")
    }

    func testVocabularyBundleLoadsFromApp() throws {
        let url = try XCTUnwrap(Bundle.main.url(forResource: "vocabulary", withExtension: "json"))
        let data = try Data(contentsOf: url)
        let bundle = try JSONDecoder().decode(VocabularyBundle.self, from: data)
        XCTAssertFalse(bundle.terms.isEmpty)
        XCTAssertFalse(bundle.categories.isEmpty)
        XCTAssertTrue(bundle.terms.contains { $0.isCore })
    }

    func testSignsBundleLoadsFromApp() throws {
        let url = try XCTUnwrap(Bundle.main.url(forResource: "signs", withExtension: "json"))
        let data = try Data(contentsOf: url)
        let bundle = try JSONDecoder().decode(SignsBundle.self, from: data)
        XCTAssertFalse(bundle.signs.isEmpty)
    }

    func testDataStoreLearningTermsFiltersKnown() async throws {
        UserDefaults.standard.removeObject(forKey: "knownTermIDs")
        let store = DataStore()
        store.loadIfNeeded()
        let deadline = Date().addingTimeInterval(5)
        while store.terms.isEmpty && store.loadError == nil && Date() < deadline {
            try await Task.sleep(nanoseconds: 50_000_000)
        }
        XCTAssertFalse(store.terms.isEmpty)

        let sample = Array(store.terms.prefix(5))
        store.setTermKnown(sample[0].id, known: true)
        let learning = store.learningTerms(from: sample)
        XCTAssertEqual(learning.count, 4)
        XCTAssertFalse(learning.contains { $0.id == sample[0].id })

        UserDefaults.standard.removeObject(forKey: "knownTermIDs")
    }
}
