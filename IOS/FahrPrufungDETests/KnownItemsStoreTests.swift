import XCTest
@testable import FahrPrufungDE

@MainActor
final class KnownItemsStoreTests: XCTestCase {
    override func setUp() async throws {
        try await super.setUp()
        UserDefaults.standard.removeObject(forKey: "knownTermIDs")
        UserDefaults.standard.removeObject(forKey: "knownSignIDs")
    }

    override func tearDown() async throws {
        UserDefaults.standard.removeObject(forKey: "knownTermIDs")
        UserDefaults.standard.removeObject(forKey: "knownSignIDs")
        try await super.tearDown()
    }

    func testMarkTermKnownPersistsAndCounts() {
        let store = KnownItemsStore()
        XCTAssertEqual(store.knownTermCount, 0)

        store.setTermKnown("term-a", known: true)
        XCTAssertTrue(store.isTermKnown("term-a"))
        XCTAssertEqual(store.knownTermCount, 1)

        let reloaded = KnownItemsStore()
        XCTAssertTrue(reloaded.isTermKnown("term-a"))
    }

    func testUnmarkAndReset() {
        let store = KnownItemsStore()
        store.setTermKnown("term-a", known: true)
        store.setSignKnown("sign-a", known: true)

        store.setTermKnown("term-a", known: false)
        XCTAssertFalse(store.isTermKnown("term-a"))
        XCTAssertEqual(store.knownTermCount, 0)
        XCTAssertEqual(store.knownSignCount, 1)

        store.resetAll()
        XCTAssertEqual(store.knownSignCount, 0)
        XCTAssertFalse(store.isSignKnown("sign-a"))
    }

    func testOnChangeFires() {
        let store = KnownItemsStore()
        var calls = 0
        store.onChange = { calls += 1 }

        store.setTermKnown("x", known: true)
        store.setSignKnown("y", known: true)
        store.resetAll()

        XCTAssertEqual(calls, 3)
    }
}
