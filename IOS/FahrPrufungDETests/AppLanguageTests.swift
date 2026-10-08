import XCTest
@testable import FahrPrufungDE

final class AppLanguageTests: XCTestCase {
    func testAllCasesContainExpectedCodes() {
        XCTAssertEqual(
            AppLanguage.allCases.map(\.rawValue).sorted(),
            ["en", "fr", "ru", "tr", "uk"]
        )
    }

    func testDisplayNamesAreNonEmpty() {
        for language in AppLanguage.allCases {
            XCTAssertFalse(language.displayName.isEmpty, "\(language)")
            XCTAssertFalse(language.flag.isEmpty, "\(language)")
        }
    }

    func testRawValueRoundTrip() {
        for language in AppLanguage.allCases {
            XCTAssertEqual(AppLanguage(rawValue: language.rawValue), language)
        }
    }

    func testUnknownCodeFallsBackWhenCreatingFromRawValue() {
        XCTAssertNil(AppLanguage(rawValue: "de"))
        XCTAssertNil(AppLanguage(rawValue: "zz"))
    }
}
