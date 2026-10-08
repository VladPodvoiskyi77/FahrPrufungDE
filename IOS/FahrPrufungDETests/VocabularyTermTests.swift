import XCTest
@testable import FahrPrufungDE

final class VocabularyTermTests: XCTestCase {
    private func makeTerm(
        id: String = "t1",
        de: String = "gefahrenbremsung",
        tags: [String] = ["core"],
        category: String = "brakes"
    ) -> VocabularyTerm {
        VocabularyTerm(
            id: id,
            de: de,
            article: "die",
            deBase: de,
            ru: "экстренное торможение",
            en: "emergency braking",
            uk: "екстрене гальмування",
            fr: "freinage d'urgence",
            tr: "acil fren",
            category: category,
            tags: tags,
            examPhraseDe: nil
        )
    }

    func testTranslationUsesSelectedLanguage() {
        let term = makeTerm()
        XCTAssertEqual(term.translation(for: .ru), "экстренное торможение")
        XCTAssertEqual(term.translation(for: .en), "emergency braking")
        XCTAssertEqual(term.translation(for: .uk), "екстрене гальмування")
        XCTAssertEqual(term.translation(for: .fr), "freinage d'urgence")
        XCTAssertEqual(term.translation(for: .tr), "acil fren")
    }

    func testDisplayTranslationCapitalizes() {
        let term = makeTerm()
        XCTAssertEqual(term.displayTranslation(for: .en), "Emergency braking")
        XCTAssertEqual(term.displayDe, "Gefahrenbremsung")
    }

    func testIsCoreAndExaminerTags() {
        XCTAssertTrue(makeTerm(tags: ["core"]).isCore)
        XCTAssertFalse(makeTerm(tags: ["core"]).isExaminerPhrase)
        XCTAssertTrue(makeTerm(tags: ["examiner"]).isExaminerPhrase)
        XCTAssertFalse(makeTerm(tags: ["examiner"]).isCore)
    }

    func testWithLeadingCapitalPreservesPrefixPunctuation() {
        XCTAssertEqual("hello".withLeadingCapital, "Hello")
        XCTAssertEqual("  hello".withLeadingCapital, "  Hello")
        XCTAssertEqual("".withLeadingCapital, "")
    }
}
