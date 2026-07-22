import SwiftUI

struct HomeView: View {
    @StateObject var viewModel: HomeViewModel
    @EnvironmentObject private var store: DataStore
    @EnvironmentObject private var coordinator: AppCoordinator

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 20) {
                HeroHeader(
                    termCount: viewModel.termCount,
                    language: viewModel.language
                )
                .staggeredAppear(index: 0)

                Button {
                    AnalyticsService.shared.logHomeAction("progress")
                    coordinator.learn.show(.progress)
                } label: {
                    ProgressSummaryCard(
                        knownTerms: viewModel.knownTermCount,
                        totalTerms: viewModel.termCount,
                        knownSigns: viewModel.knownSignCount,
                        totalSigns: viewModel.signCount,
                        streak: viewModel.studyStreak,
                        termPercent: viewModel.overallTermPercent
                    )
                }
                .buttonStyle(ScalePressButtonStyle())
                .staggeredAppear(index: 1)

                SectionHeader(title: L10n.Home.quickStart, icon: "bolt.fill")
                    .staggeredAppear(index: 2)

                VStack(spacing: 12) {
                    Button {
                        AnalyticsService.shared.logHomeAction("top_terms")
                        coordinator.learn.show(
                            .flashcards(terms: viewModel.coreTerms, title: L10n.Home.TopTerms.title)
                        )
                    } label: {
                        ActionCard(
                            title: L10n.Home.TopTerms.title,
                            subtitle: L10n.Home.TopTerms.subtitle,
                            icon: "star.fill",
                            colors: [AppTheme.signalAmber, Color(red: 0.92, green: 0.55, blue: 0.10)],
                            badge: "\(viewModel.coreTerms.count)"
                        )
                    }
                    .buttonStyle(ScalePressButtonStyle())
                    .staggeredAppear(index: 3)

                    Button {
                        AnalyticsService.shared.logHomeAction("examiner_phrases")
                        coordinator.learn.show(.examinerPhrases)
                    } label: {
                        ActionCard(
                            title: L10n.Home.ExaminerPhrases.title,
                            subtitle: L10n.Home.ExaminerPhrases.subtitle,
                            icon: "person.wave.2.fill",
                            colors: CategoryStyle.style(for: "phrases").gradient,
                            badge: "\(viewModel.examinerTerms.count)"
                        )
                    }
                    .buttonStyle(ScalePressButtonStyle())
                    .staggeredAppear(index: 4)

                    Button {
                        AnalyticsService.shared.logHomeAction("quiz")
                        coordinator.learn.show(
                            .quiz(terms: viewModel.quizSourceTerms, title: L10n.Home.Quiz.title)
                        )
                    } label: {
                        ActionCard(
                            title: L10n.Home.Quiz.title,
                            subtitle: L10n.Home.Quiz.subtitle,
                            icon: "brain.head.profile",
                            colors: [AppTheme.highwayTeal, AppTheme.roadNavy]
                        )
                    }
                    .buttonStyle(ScalePressButtonStyle())
                    .staggeredAppear(index: 5)
                }

                SectionHeader(title: L10n.Home.learnSection, icon: "books.vertical.fill")
                    .staggeredAppear(index: 6)

                Button {
                    AnalyticsService.shared.logHomeAction("categories")
                    coordinator.learn.show(.categories)
                } label: {
                    ActionCard(
                        title: L10n.Home.AllCategories.title,
                        subtitle: L10n.Home.AllCategories.subtitle,
                        icon: "square.grid.2x2.fill",
                        colors: [AppTheme.roadNavy, AppTheme.highwayTeal],
                        badge: "\(viewModel.categoryCount)"
                    )
                }
                .buttonStyle(ScalePressButtonStyle())
                .staggeredAppear(index: 7)

                SectionHeader(title: L10n.Home.signsSection, icon: "signpost.right.fill")
                    .staggeredAppear(index: 8)

                Button {
                    AnalyticsService.shared.logHomeAction("signs_tab")
                    coordinator.selectedTab = .signs
                } label: {
                    ActionCard(
                        title: L10n.Signs.title,
                        subtitle: L10n.Home.Signs.subtitle(viewModel.signCount),
                        icon: "signpost.right.and.left.fill",
                        colors: [AppTheme.signalGreen, Color(red: 0.12, green: 0.55, blue: 0.38)],
                        badge: "\(viewModel.signCount)"
                    )
                }
                .buttonStyle(ScalePressButtonStyle())
                .staggeredAppear(index: 9)
            }
            .padding(.horizontal, 20)
            .padding(.bottom, 32)
            .id(store.nativeLanguage)
        }
        .appScreenBackground()
        .navigationBarHidden(true)
        .onAppear {
            AnalyticsService.shared.logScreen("home")
        }
    }
}
