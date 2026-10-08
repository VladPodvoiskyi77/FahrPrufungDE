import XCTest
@testable import FahrPrufungDE

@MainActor
final class QuizViewModelTests: XCTestCase {
    private var store: DataStore!

    override func setUp() async throws {
        try await super.setUp()
        UserDefaults.standard.removeObject(forKey: "knownTermIDs")
        UserDefaults.standard.set("en", forKey: "nativeLanguage")
        store = DataStore()
        store.loadIfNeeded()

        let deadline = Date().addingTimeInterval(5)
        while store.terms.isEmpty && store.loadError == nil && Date() < deadline {
            try await Task.sleep(nanoseconds: 50_000_000)
        }
        XCTAssertFalse(store.terms.isEmpty, "vocabulary.json must load in test host: \(store.loadError ?? "nil")")
    }

    override func tearDown() async throws {
        UserDefaults.standard.removeObject(forKey: "knownTermIDs")
        try await super.tearDown()
    }

    func testStartBuildsUpToTenQuestionsWithFourOptions() {
        let source = Array(store.terms.prefix(20))
        let vm = QuizViewModel(sourceTerms: source, store: store, sessionTitle: "Test Quiz")
        vm.start()

        XCTAssertFalse(vm.questions.isEmpty)
        XCTAssertLessThanOrEqual(vm.questions.count, 10)
        XCTAssertEqual(vm.currentIndex, 0)
        XCTAssertFalse(vm.isFinished)

        for question in vm.questions {
            XCTAssertEqual(question.options.count, 4)
            XCTAssertTrue(question.options.contains { $0.id == question.correctID })
        }
    }

    func testAnsweringCorrectIncrementsScoreAndNextFinishes() {
        let source = Array(store.terms.prefix(8))
        let vm = QuizViewModel(sourceTerms: source, store: store, sessionTitle: "Test Quiz")
        vm.start()
        XCTAssertGreaterThanOrEqual(vm.questions.count, 1)

        let total = vm.questions.count
        for _ in 0 ..< total {
            guard let question = vm.currentQuestion else {
                XCTFail("missing question")
                return
            }
            let correct = question.options.first { $0.id == question.correctID }!
            vm.answer(correct)
            XCTAssertTrue(vm.hasAnswered)
            vm.next()
        }

        XCTAssertTrue(vm.isFinished)
        XCTAssertEqual(vm.score, total)
        XCTAssertEqual(vm.answerRecords.count, total)
        XCTAssertTrue(vm.answerRecords.allSatisfy(\.isCorrect))
    }

    func testCannotAnswerTwice() {
        let source = Array(store.terms.prefix(6))
        let vm = QuizViewModel(sourceTerms: source, store: store, sessionTitle: "Test Quiz")
        vm.start()
        guard let question = vm.currentQuestion, question.options.count >= 2 else {
            XCTFail("need options")
            return
        }

        vm.answer(question.options[0])
        let selected = vm.selectedID
        vm.answer(question.options[1])
        XCTAssertEqual(vm.selectedID, selected)
    }

    func testKnownTermsAreExcludedFromQuestions() {
        let source = Array(store.terms.prefix(12))
        guard let first = source.first else {
            XCTFail("no terms")
            return
        }
        store.setTermKnown(first.id, known: true)

        let vm = QuizViewModel(sourceTerms: source, store: store, sessionTitle: "Test Quiz")
        vm.start()

        XCTAssertFalse(vm.questions.contains { $0.correctID == first.id })
        XCTAssertEqual(vm.learningTerms.count, source.count - 1)
    }
}
