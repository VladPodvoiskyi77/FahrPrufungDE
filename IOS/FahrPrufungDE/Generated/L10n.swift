// swiftlint:disable all
// Generated using SwiftGen — https://github.com/SwiftGen/SwiftGen

import Foundation

// swiftlint:disable superfluous_disable_command file_length implicit_return prefer_self_in_static_references

// MARK: - Strings

// swiftlint:disable explicit_type_interface function_parameter_count identifier_name line_length
// swiftlint:disable nesting type_body_length type_name vertical_whitespace_opening_braces
internal enum L10n {
  internal enum Category {
    /// Karten
    internal static var cards: String { return L10n.tr("Localizable", "category.cards", fallback: "Karten") }
    /// Quiz
    internal static var quiz: String { return L10n.tr("Localizable", "category.quiz", fallback: "Quiz") }
    /// Category
    internal static func termCount(_ p1: Int) -> String {
      return L10n.tr("Localizable", "category.termCount", p1, fallback: "%d Begriffe")
    }
    /// Begriffe
    internal static var terms: String { return L10n.tr("Localizable", "category.terms", fallback: "Begriffe") }
  }
  internal enum Common {
    /// Alle
    internal static var all: String { return L10n.tr("Localizable", "common.all", fallback: "Alle") }
    /// Weiter
    internal static var `continue`: String { return L10n.tr("Localizable", "common.continue", fallback: "Weiter") }
    /// Common
    internal static var next: String { return L10n.tr("Localizable", "common.next", fallback: "Weiter") }
    /// Nochmal
    internal static var retry: String { return L10n.tr("Localizable", "common.retry", fallback: "Nochmal") }
    /// Überspringen
    internal static var skip: String { return L10n.tr("Localizable", "common.skip", fallback: "Überspringen") }
    /// Wird geladen…
    internal static var loading: String { return L10n.tr("Localizable", "common.loading", fallback: "Wird geladen…") }
    /// Anhören
    internal static var listen: String { return L10n.tr("Localizable", "common.listen", fallback: "Anhören") }
  }
  internal enum Error {
    /// Errors
    internal static var loadTitle: String { return L10n.tr("Localizable", "error.loadTitle", fallback: "Fehler beim Laden") }
  }
  internal enum ExaminerPhrases {
    /// Alle Phrasen & Fragen
    internal static var listTitle: String { return L10n.tr("Localizable", "examinerPhrases.listTitle", fallback: "Alle Phrasen & Fragen") }
    /// Liste
    internal static var listMode: String { return L10n.tr("Localizable", "examinerPhrases.listMode", fallback: "Liste") }
    internal enum Group {
      /// Richtung
      internal static var direction: String { return L10n.tr("Localizable", "examinerPhrases.group.direction", fallback: "Richtung") }
      /// Hinweise
      internal static var hint: String { return L10n.tr("Localizable", "examinerPhrases.group.hint", fallback: "Hinweise") }
      /// Manöver
      internal static var maneuver: String { return L10n.tr("Localizable", "examinerPhrases.group.maneuver", fallback: "Manöver") }
      /// Ergebnis
      internal static var result: String { return L10n.tr("Localizable", "examinerPhrases.group.result", fallback: "Ergebnis") }
      /// Sicherheitskontrolle
      internal static var safety: String { return L10n.tr("Localizable", "examinerPhrases.group.safety", fallback: "Sicherheitskontrolle") }
      /// Vor der Fahrt
      internal static var start: String { return L10n.tr("Localizable", "examinerPhrases.group.start", fallback: "Vor der Fahrt") }
    }
  }
  internal enum Flashcards {
    /// Karten
    internal static var cards: String { return L10n.tr("Localizable", "flashcards.cards", fallback: "Karten") }
    /// Flashcards
    internal static func counter(_ p1: Int, _ p2: Int) -> String {
      return L10n.tr("Localizable", "flashcards.counter", p1, p2, fallback: "%d von %d")
    }
    /// Keine Begriffe
    internal static var empty: String { return L10n.tr("Localizable", "flashcards.empty", fallback: "Keine Begriffe") }
    /// Prüfer sagt:
    internal static var examinerSays: String { return L10n.tr("Localizable", "flashcards.examinerSays", fallback: "Prüfer sagt:") }
    /// Tippen zum Umdrehen
    internal static var tapToFlip: String { return L10n.tr("Localizable", "flashcards.tapToFlip", fallback: "Tippen zum Umdrehen") }
  }
  internal enum Known {
    /// Alle Begriffe als bekannt markiert. In Einstellungen zurücksetzen.
    internal static var allKnownFlashcards: String { return L10n.tr("Localizable", "known.allKnownFlashcards", fallback: "Alle Begriffe als bekannt markiert. In Einstellungen zurücksetzen.") }
    /// Nicht genug Begriffe zum Üben. Markierte zurücksetzen in Einstellungen.
    internal static var allKnownQuiz: String { return L10n.tr("Localizable", "known.allKnownQuiz", fallback: "Nicht genug Begriffe zum Üben. Markierte zurücksetzen in Einstellungen.") }
    /// Abbrechen
    internal static var cancel: String { return L10n.tr("Localizable", "known.cancel", fallback: "Abbrechen") }
    /// Known items
    internal static func listHiddenCount(_ p1: Int) -> String {
      return L10n.tr("Localizable", "known.listHiddenCount", p1, fallback: "%d als bekannt markiert")
    }
    /// Nicht mehr in Karten & Quiz anzeigen
    internal static var markSubtitle: String { return L10n.tr("Localizable", "known.markSubtitle", fallback: "Nicht mehr in Karten & Quiz anzeigen") }
    /// Das kenne ich schon
    internal static var markTitle: String { return L10n.tr("Localizable", "known.markTitle", fallback: "Das kenne ich schon") }
    /// Zurücksetzen
    internal static var resetConfirm: String { return L10n.tr("Localizable", "known.resetConfirm", fallback: "Zurücksetzen") }
    /// Alle Begriffe und Zeichen werden wieder in Karten und Quiz angezeigt.
    internal static var resetConfirmMessage: String { return L10n.tr("Localizable", "known.resetConfirmMessage", fallback: "Alle Begriffe und Zeichen werden wieder in Karten und Quiz angezeigt.") }
    /// Zurücksetzen?
    internal static var resetConfirmTitle: String { return L10n.tr("Localizable", "known.resetConfirmTitle", fallback: "Zurücksetzen?") }
    /// Alle wieder zum Lernen
    internal static var resetTitle: String { return L10n.tr("Localizable", "known.resetTitle", fallback: "Alle wieder zum Lernen") }
    /// Mein Lernfortschritt
    internal static var settingsSection: String { return L10n.tr("Localizable", "known.settingsSection", fallback: "Mein Lernfortschritt") }
    /// Zeichen als bekannt markiert
    internal static var signsMarked: String { return L10n.tr("Localizable", "known.signsMarked", fallback: "Zeichen als bekannt markiert") }
    /// Begriffe als bekannt markiert
    internal static var termsMarked: String { return L10n.tr("Localizable", "known.termsMarked", fallback: "Begriffe als bekannt markiert") }
    /// Wieder lernen
    internal static var unmarkTitle: String { return L10n.tr("Localizable", "known.unmarkTitle", fallback: "Wieder lernen") }
    /// Rückgängig
    internal static var undoAction: String { return L10n.tr("Localizable", "known.undoAction", fallback: "Rückgängig") }
    /// Aus dem Lernen ausgeblendet
    internal static var undoMessage: String { return L10n.tr("Localizable", "known.undoMessage", fallback: "Aus dem Lernen ausgeblendet") }
  }
  internal enum CoreTerm {
    /// Dieser Begriff gehört zu den Kernbegriffen der praktischen Fahrprüfung — besonders oft gefragt.
    internal static var hintMessage: String { return L10n.tr("Localizable", "coreTerm.hintMessage", fallback: "Dieser Begriff gehört zu den Kernbegriffen der praktischen Fahrprüfung — besonders oft gefragt.") }
    /// Wichtig für die Prüfung
    internal static var hintTitle: String { return L10n.tr("Localizable", "coreTerm.hintTitle", fallback: "Wichtig für die Prüfung") }
  }
  internal enum Home {
    /// Home
    internal static var badge: String { return L10n.tr("Localizable", "home.badge", fallback: "Deutschland · Führerschein") }
    /// Kategorien
    internal static var categoriesTitle: String { return L10n.tr("Localizable", "home.categoriesTitle", fallback: "Kategorien") }
    /// Lernen
    internal static var learnSection: String { return L10n.tr("Localizable", "home.learnSection", fallback: "Lernen") }
    /// Schnellstart
    internal static var quickStart: String { return L10n.tr("Localizable", "home.quickStart", fallback: "Schnellstart") }
    /// Verkehrszeichen
    internal static var signsSection: String { return L10n.tr("Localizable", "home.signsSection", fallback: "Verkehrszeichen") }
    /// Deutsch für die praktische Prüfung
    internal static var subtitle: String { return L10n.tr("Localizable", "home.subtitle", fallback: "Deutsch für die praktische Prüfung") }
    /// Begriffe
    internal static var terms: String { return L10n.tr("Localizable", "home.terms", fallback: "Begriffe") }
    /// Fahrprüfung
    internal static var title: String { return L10n.tr("Localizable", "home.title", fallback: "Fahrprufung DE") }
    internal enum AllCategories {
      /// Alle Themen — von Technik bis Verkehr
      internal static var subtitle: String { return L10n.tr("Localizable", "home.allCategories.subtitle", fallback: "Alle Themen — von Technik bis Verkehr") }
      /// Alle Kategorien
      internal static var title: String { return L10n.tr("Localizable", "home.allCategories.title", fallback: "Alle Kategorien") }
    }
    internal enum ExaminerPhrases {
      /// Was der Prüfer sagt — und was du tun musst
      internal static var subtitle: String { return L10n.tr("Localizable", "home.examinerPhrases.subtitle", fallback: "Was der Prüfer sagt — und was du tun musst") }
      /// Prüfer-Phrasen
      internal static var title: String { return L10n.tr("Localizable", "home.examinerPhrases.title", fallback: "Prüfer-Phrasen") }
    }
    internal enum Quiz {
      /// Alle Begriffe — Multiple Choice
      internal static var subtitle: String { return L10n.tr("Localizable", "home.quiz.subtitle", fallback: "Alle Begriffe — Multiple Choice") }
      /// Quiz
      internal static var title: String { return L10n.tr("Localizable", "home.quiz.title", fallback: "Quiz") }
    }
    internal enum Signs {
      /// Offizielle StVO-Zeichen — %d Stück
      internal static func subtitle(_ p1: Int) -> String {
        return L10n.tr("Localizable", "home.signs.subtitle", p1, fallback: "Offizielle StVO-Zeichen — %d Stück")
      }
    }
    internal enum TopTerms {
      /// Die wichtigsten Wörter für die Prüfung
      internal static var subtitle: String { return L10n.tr("Localizable", "home.topTerms.subtitle", fallback: "Die wichtigsten Wörter für die Prüfung") }
      /// Top-Begriffe
      internal static var title: String { return L10n.tr("Localizable", "home.topTerms.title", fallback: "Top-Begriffe") }
    }
  }
  internal enum Onboarding {
    /// Karteikarten — deutsches Wort und Übersetzung
    internal static var featureCards: String { return L10n.tr("Localizable", "onboarding.featureCards", fallback: "Karteikarten — deutsches Wort und Übersetzung") }
    /// Prüfer-Phrasen — was er sagt
    internal static var featureExaminer: String { return L10n.tr("Localizable", "onboarding.featureExaminer", fallback: "Prüfer-Phrasen — was er sagt") }
    /// Quiz — teste dich selbst
    internal static var featureQuiz: String { return L10n.tr("Localizable", "onboarding.featureQuiz", fallback: "Quiz — teste dich selbst") }
    /// Verkehrszeichen — mit Erklärungen
    internal static var featureSigns: String { return L10n.tr("Localizable", "onboarding.featureSigns", fallback: "Verkehrszeichen — mit Erklärungen") }
    /// So lernst du
    internal static var featuresTitle: String { return L10n.tr("Localizable", "onboarding.featuresTitle", fallback: "So lernst du") }
    /// Wähle deine Sprache
    internal static var languageTitle: String { return L10n.tr("Localizable", "onboarding.languageTitle", fallback: "Wähle deine Sprache") }
    /// Lernen beginnen
    internal static var start: String { return L10n.tr("Localizable", "onboarding.start", fallback: "Lernen beginnen") }
    /// Lerne deutsche Begriffe für die praktische Prüfung — in deiner Sprache.
    internal static var welcomeSubtitle: String { return L10n.tr("Localizable", "onboarding.welcomeSubtitle", fallback: "Lerne deutsche Begriffe für die praktische Prüfung — in deiner Sprache.") }
    /// Onboarding
    internal static var welcomeTitle: String { return L10n.tr("Localizable", "onboarding.welcomeTitle", fallback: "Willkommen!") }
  }
  internal enum Quiz {
    /// richtig
    internal static var correct: String { return L10n.tr("Localizable", "quiz.correct", fallback: "richtig") }
    /// Quiz
    internal static func question(_ p1: Int, _ p2: Int) -> String {
      return L10n.tr("Localizable", "quiz.question", p1, p2, fallback: "Frage %d / %d")
    }
    /// Zu wenig Begriffe
    internal static var tooFew: String { return L10n.tr("Localizable", "quiz.tooFew", fallback: "Zu wenig Begriffe") }
    /// Was bedeutet:
    internal static var whatMeans: String { return L10n.tr("Localizable", "quiz.whatMeans", fallback: "Was bedeutet:") }
    /// Richtige Antwort
    internal static var correctAnswer: String { return L10n.tr("Localizable", "quiz.correctAnswer", fallback: "Richtige Antwort") }
    /// Antworten ansehen
    internal static var reviewAnswers: String { return L10n.tr("Localizable", "quiz.reviewAnswers", fallback: "Antworten ansehen") }
    /// Quiz-Auswertung
    internal static var reviewTitle: String { return L10n.tr("Localizable", "quiz.reviewTitle", fallback: "Quiz-Auswertung") }
    /// Frage %d
    internal static func reviewQuestion(_ p1: Int) -> String {
      return L10n.tr("Localizable", "quiz.reviewQuestion", p1, fallback: "Frage %d")
    }
    /// Deine Antwort
    internal static var yourAnswer: String { return L10n.tr("Localizable", "quiz.yourAnswer", fallback: "Deine Antwort") }
    internal enum Result {
      /// Gut! Noch ein bisschen üben.
      internal static var good: String { return L10n.tr("Localizable", "quiz.result.good", fallback: "Gut! Noch ein bisschen üben.") }
      /// Sehr gut! Weiter üben.
      internal static var great: String { return L10n.tr("Localizable", "quiz.result.great", fallback: "Sehr gut! Weiter üben.") }
      /// Weiter lernen — du schaffst das!
      internal static var keepGoing: String { return L10n.tr("Localizable", "quiz.result.keepGoing", fallback: "Weiter lernen — du schaffst das!") }
      /// Perfekt! Bereit für die Prüfung!
      internal static var perfect: String { return L10n.tr("Localizable", "quiz.result.perfect", fallback: "Perfekt! Bereit für die Prüfung!") }
    }
  }
  internal enum Progress {
    /// Nach Kategorie
    internal static var byCategory: String { return L10n.tr("Localizable", "progress.byCategory", fallback: "Nach Kategorie") }
    /// %d von %d
    internal static func homeSignsSummary(_ p1: Int, _ p2: Int) -> String {
      return L10n.tr("Localizable", "progress.homeSignsSummary", p1, p2, fallback: "Zeichen: %d von %d")
    }
    /// %d von %d Begriffen gelernt
    internal static func homeSummary(_ p1: Int, _ p2: Int) -> String {
      return L10n.tr("Localizable", "progress.homeSummary", p1, p2, fallback: "%d von %d Begriffen gelernt")
    }
    /// Tippen für Details
    internal static var homeTapHint: String { return L10n.tr("Localizable", "progress.homeTapHint", fallback: "Tippen für Details") }
    /// %d von %d
    internal static func learnedCount(_ p1: Int, _ p2: Int) -> String {
      return L10n.tr("Localizable", "progress.learnedCount", p1, p2, fallback: "%d von %d")
    }
    /// Quiz absolvieren — Ergebnisse erscheinen hier
    internal static var noQuizzesYet: String { return L10n.tr("Localizable", "progress.noQuizzesYet", fallback: "Quiz absolvieren — Ergebnisse erscheinen hier") }
    /// Gesamtfortschritt
    internal static var overall: String { return L10n.tr("Localizable", "progress.overall", fallback: "Gesamtfortschritt") }
    /// %d / %d
    internal static func quizScore(_ p1: Int, _ p2: Int) -> String {
      return L10n.tr("Localizable", "progress.quizScore", p1, p2, fallback: "%d / %d")
    }
    /// Letzte Quiz
    internal static var recentQuizzes: String { return L10n.tr("Localizable", "progress.recentQuizzes", fallback: "Letzte Quiz") }
    /// Zeichen
    internal static var signs: String { return L10n.tr("Localizable", "progress.signs", fallback: "Zeichen") }
    /// Serie
    internal static var streak: String { return L10n.tr("Localizable", "progress.streak", fallback: "Serie") }
    /// %d Tage in Folge
    internal static func streakDays(_ p1: Int) -> String {
      return L10n.tr("Localizable", "progress.streakDays", p1, fallback: "%d Tage in Folge")
    }
    /// Begriffe
    internal static var terms: String { return L10n.tr("Localizable", "progress.terms", fallback: "Begriffe") }
    /// Mein Fortschritt
    internal static var title: String { return L10n.tr("Localizable", "progress.title", fallback: "Mein Fortschritt") }
  }
  internal enum Settings {
    /// Für Menschen, die neu in Deutschland sind und sich auf die praktische Fahrprüfung vorbereiten — ohne perfektes Deutsch.
    internal static var about: String { return L10n.tr("Localizable", "settings.about", fallback: "Für Menschen, die neu in Deutschland sind und sich auf die praktische Fahrprüfung vorbereiten — ohne perfektes Deutsch.") }
    /// Anonyme Analyse
    internal static var analytics: String { return L10n.tr("Localizable", "settings.analytics", fallback: "Anonyme Analyse") }
    /// Hilft, die App zu verbessern. Keine persönlichen Daten.
    internal static var analyticsSubtitle: String { return L10n.tr("Localizable", "settings.analyticsSubtitle", fallback: "Hilft, die App zu verbessern. Keine persönlichen Daten.") }
    /// Kategorien
    internal static var categories: String { return L10n.tr("Localizable", "settings.categories", fallback: "Kategorien") }
    /// Entwickler kontaktieren
    internal static var contactDeveloper: String { return L10n.tr("Localizable", "settings.contactDeveloper", fallback: "Entwickler kontaktieren") }
    /// Inoffizielle App zur Selbstvorbereitung. Ersetzt keine Fahrstunden und keine offiziellen StVO-/TÜV-Materialien.
    internal static var disclaimer: String { return L10n.tr("Localizable", "settings.disclaimer", fallback: "Inoffizielle App zur Selbstvorbereitung. Ersetzt keine Fahrstunden und keine offiziellen StVO-/TÜV-Materialien.") }
    /// Hinweis
    internal static var disclaimerTitle: String { return L10n.tr("Localizable", "settings.disclaimerTitle", fallback: "Hinweis") }
    /// Datenschutzerklärung
    internal static var privacyPolicy: String { return L10n.tr("Localizable", "settings.privacyPolicy", fallback: "Datenschutzerklärung") }
    /// Ihre Sprache
    internal static var language: String { return L10n.tr("Localizable", "settings.language", fallback: "Ihre Sprache") }
    /// Unsere anderen Projekte
    internal static var otherProjects: String { return L10n.tr("Localizable", "settings.otherProjects", fallback: "Unsere anderen Projekte") }
    /// Präpositionen trainieren — A1 bis C1
    internal static var prapodeSubtitle: String { return L10n.tr("Localizable", "settings.prapodeSubtitle", fallback: "Präpositionen trainieren — A1 bis C1") }
    /// PrapoDe: Deutsche Präpositionen
    internal static var prapodeTitle: String { return L10n.tr("Localizable", "settings.prapodeTitle", fallback: "PrapoDe: Deutsche Präpositionen") }
    /// Willkommen erneut anzeigen
    internal static var replayOnboarding: String { return L10n.tr("Localizable", "settings.replayOnboarding", fallback: "Willkommen erneut anzeigen") }
    /// Verkehrszeichen
    internal static var signs: String { return L10n.tr("Localizable", "settings.signs", fallback: "Verkehrszeichen") }
    /// Statistik
    internal static var statistics: String { return L10n.tr("Localizable", "settings.statistics", fallback: "Statistik") }
    /// Begriffe
    internal static var terms: String { return L10n.tr("Localizable", "settings.terms", fallback: "Begriffe") }
    /// Settings
    internal static var title: String { return L10n.tr("Localizable", "settings.title", fallback: "Einstellungen") }
    /// Mein Fortschritt
    internal static var viewProgress: String { return L10n.tr("Localizable", "settings.viewProgress", fallback: "Mein Fortschritt") }
  }
  internal enum Signs {
    /// %d Zeichen
    internal static func count(_ p1: Int) -> String {
      return L10n.tr("Localizable", "signs.count", p1, fallback: "%d Zeichen")
    }
    /// Erklärung
    internal static var explanation: String { return L10n.tr("Localizable", "signs.explanation", fallback: "Erklärung") }
    /// Offizielle Zeichen Deutschlands
    internal static var heroSubtitle: String { return L10n.tr("Localizable", "signs.heroSubtitle", fallback: "Offizielle Zeichen Deutschlands") }
    /// Auf Deutsch
    internal static var inGerman: String { return L10n.tr("Localizable", "signs.inGerman", fallback: "Auf Deutsch") }
    /// Zeichen suchen…
    internal static var searchPlaceholder: String { return L10n.tr("Localizable", "signs.searchPlaceholder", fallback: "Zeichen suchen…") }
    /// Zeichen (%d)
    internal static func section(_ p1: Int) -> String {
      return L10n.tr("Localizable", "signs.section", p1, fallback: "Zeichen (%d)")
    }
    /// Signs
    internal static var title: String { return L10n.tr("Localizable", "signs.title", fallback: "Verkehrszeichen") }
    internal enum Empty {
      /// Versuche eine andere Suche
      internal static var subtitle: String { return L10n.tr("Localizable", "signs.empty.subtitle", fallback: "Versuche eine andere Suche") }
      /// Nichts gefunden
      internal static var title: String { return L10n.tr("Localizable", "signs.empty.title", fallback: "Nichts gefunden") }
    }
  }
  internal enum Tab {
    /// Tabs
    internal static var learn: String { return L10n.tr("Localizable", "tab.learn", fallback: "Lernen") }
    /// Einstellungen
    internal static var settings: String { return L10n.tr("Localizable", "tab.settings", fallback: "Einstellungen") }
    /// Zeichen
    internal static var signs: String { return L10n.tr("Localizable", "tab.signs", fallback: "Zeichen") }
    /// Fortschritt
    internal static var progress: String { return L10n.tr("Localizable", "tab.progress", fallback: "Fortschritt") }
  }
}
// swiftlint:enable explicit_type_interface function_parameter_count identifier_name line_length
// swiftlint:enable nesting type_body_length type_name vertical_whitespace_opening_braces

// MARK: - Implementation Details

extension L10n {
  private static func tr(_ table: String, _ key: String, _ args: CVarArg..., fallback value: String) -> String {
    let format = l10nLookup(key, table, value)
    return String(format: format, locale: Locale.current, arguments: args)
  }
}
