import XCTest

/// Smoke UI tests. Prefers English UI after skipping onboarding when possible.
final class FahrPrufungDEUITests: XCTestCase {
    private var app: XCUIApplication!

    override func setUpWithError() throws {
        continueAfterFailure = false
        app = XCUIApplication()
        app.launchArguments += ["-ui-testing"]
        app.launch()
    }

    func testAppLaunchesToOnboardingOrMain() {
        // Either first-launch onboarding or main tabs should appear quickly.
        let skip = app.buttons["Skip"].firstMatch
        let welcome = app.staticTexts["Welcome!"].firstMatch
        let learnTab = app.tabBars.buttons.element(boundBy: 0)

        let appeared = skip.waitForExistence(timeout: 8)
            || welcome.waitForExistence(timeout: 1)
            || learnTab.waitForExistence(timeout: 8)
        XCTAssertTrue(appeared, "Expected onboarding or main tab UI after launch")
    }

    func testSkipOnboardingReachesMainTabs() {
        let skip = app.buttons["Skip"].firstMatch
        if skip.waitForExistence(timeout: 6) {
            skip.tap()
        }

        // Tab bar should exist after onboarding is dismissed/skipped.
        let tabBar = app.tabBars.firstMatch
        XCTAssertTrue(tabBar.waitForExistence(timeout: 8), "Main tab bar missing after skip/launch")

        // Open Settings tab (last of 4).
        let settingsTab = tabBar.buttons.element(boundBy: 3)
        if settingsTab.exists {
            settingsTab.tap()
            let settingsTitle = app.staticTexts["Settings"].firstMatch
            XCTAssertTrue(
                settingsTitle.waitForExistence(timeout: 5) || app.staticTexts.matching(NSPredicate(format: "label CONTAINS[c] %@", "Settings")).firstMatch.waitForExistence(timeout: 2),
                "Settings screen did not appear"
            )
        }
    }

    func testLearnTabShowsQuickStartOrHomeContent() {
        let skip = app.buttons["Skip"].firstMatch
        if skip.waitForExistence(timeout: 4) {
            skip.tap()
        }

        let tabBar = app.tabBars.firstMatch
        XCTAssertTrue(tabBar.waitForExistence(timeout: 8))
        tabBar.buttons.element(boundBy: 0).tap()

        let brand = app.staticTexts["Fahrprufung DE"].firstMatch
        let quiz = app.staticTexts["Quiz"].firstMatch
        let topTerms = app.staticTexts.matching(NSPredicate(format: "label CONTAINS[c] %@", "Top")).firstMatch

        let homeVisible = brand.waitForExistence(timeout: 6)
            || quiz.waitForExistence(timeout: 2)
            || topTerms.waitForExistence(timeout: 2)
        XCTAssertTrue(homeVisible, "Home/Learn content not found")
    }
}
