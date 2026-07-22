import SwiftUI

struct ContentView: View {
    @EnvironmentObject private var store: DataStore
    @EnvironmentObject private var coordinator: AppCoordinator
    @ObservedObject private var localization = LocalizationManager.shared
    @AppStorage(OnboardingViewModel.completedKey) private var hasCompletedOnboarding = false

    var body: some View {
        Group {
            if store.isLoading && store.terms.isEmpty {
                ProgressView(L10n.Common.loading)
                    .frame(maxWidth: .infinity, maxHeight: .infinity)
            } else if let error = store.loadError {
                ContentUnavailableView(
                    L10n.Error.loadTitle,
                    systemImage: "exclamationmark.triangle",
                    description: Text(error)
                )
            } else {
                mainTabs
            }
        }
        .onAppear {
            store.loadIfNeeded()
            AnalyticsService.shared.logAppOpen()
            AnalyticsService.shared.logScreen("root")
            AnalyticsService.shared.syncEngagementProperties(
                onboardingCompleted: hasCompletedOnboarding,
                studyStreak: store.learningStats.studyStreak,
                knownTermCount: store.knownItems.knownTermCount
            )
        }
        .onChange(of: hasCompletedOnboarding) { _, completed in
            if !completed { coordinator.isOnboardingPresented = true }
        }
    }

    private var mainTabs: some View {
        TabView(selection: $coordinator.selectedTab) {
            LearnFlowView()
                .tabItem {
                    Label(L10n.Tab.learn, systemImage: "road.lanes")
                }
                .tag(AppCoordinator.Tab.learn)

            SignsFlowView()
                .tabItem {
                    Label(L10n.Tab.signs, systemImage: "signpost.right.and.left")
                }
                .tag(AppCoordinator.Tab.signs)

            NavigationStack {
                LearningProgressView(viewModel: ProgressViewModel(store: store))
            }
            .tabItem {
                Label(L10n.Tab.progress, systemImage: "chart.bar.fill")
            }
            .tag(AppCoordinator.Tab.progress)

            NavigationStack {
                SettingsView(viewModel: SettingsViewModel(store: store))
            }
            .tabItem {
                Label(L10n.Tab.settings, systemImage: "globe")
            }
            .tag(AppCoordinator.Tab.settings)
        }
        .tint(AppTheme.signalAmber)
        .onAppear {
            configureTabBarAppearance()
            coordinator.showOnboardingIfNeeded()
        }
        .fullScreenCover(isPresented: $coordinator.isOnboardingPresented) {
            OnboardingView(viewModel: OnboardingViewModel(store: store))
        }
        .overlay(alignment: .bottom) {
            KnownUndoToast(controller: store.knownUndo)
                .padding(.bottom, 56)
                .animation(.spring(response: 0.35, dampingFraction: 0.85), value: store.knownUndo.isVisible)
        }
    }

    private func configureTabBarAppearance() {
        let appearance = UITabBarAppearance()
        appearance.configureWithOpaqueBackground()
        appearance.backgroundColor = UIColor(AppTheme.cardWhite)
        appearance.shadowColor = UIColor.black.withAlphaComponent(0.06)

        UITabBar.appearance().standardAppearance = appearance
        UITabBar.appearance().scrollEdgeAppearance = appearance
    }
}

/// Learn tab: NavigationStack driven by LearnCoordinator.
private struct LearnFlowView: View {
    @EnvironmentObject private var store: DataStore
    @EnvironmentObject private var coordinator: AppCoordinator

    var body: some View {
        FlowStack(coordinator: coordinator.learn) {
            HomeView(viewModel: HomeViewModel(store: store))
                .navigationDestination(for: LearnRoute.self) { route in
                    destination(for: route)
                }
        }
    }

    @ViewBuilder
    private func destination(for route: LearnRoute) -> some View {
        switch route {
        case .categories:
            CategoryListView(viewModel: CategoryListViewModel(store: store))
        case .terms(let category):
            if category.id == "phrases" {
                ExaminerPhrasesView(viewModel: ExaminerPhrasesViewModel(store: store))
            } else {
                TermListView(viewModel: TermListViewModel(category: category, store: store))
            }
        case .examinerPhrases:
            ExaminerPhrasesView(viewModel: ExaminerPhrasesViewModel(store: store))
        case .flashcards(let terms, let title):
            FlashcardView(
                viewModel: FlashcardViewModel(
                    terms: store.learningTerms(from: terms),
                    store: store,
                    sessionTitle: title
                ),
                title: title
            )
        case .quiz(let terms, let title):
            QuizView(
                viewModel: QuizViewModel(sourceTerms: terms, store: store, sessionTitle: title),
                title: title
            )
        case .progress:
            LearningProgressView(viewModel: ProgressViewModel(store: store))
        }
    }
}

/// Signs tab: NavigationStack driven by SignsCoordinator.
private struct SignsFlowView: View {
    @EnvironmentObject private var store: DataStore
    @EnvironmentObject private var coordinator: AppCoordinator

    var body: some View {
        FlowStack(coordinator: coordinator.signs) {
            SignsListView(viewModel: SignsListViewModel(store: store))
                .navigationDestination(for: SignsRoute.self) { route in
                    switch route {
                    case .detail(let sign):
                        SignDetailView(viewModel: SignDetailViewModel(sign: sign, store: store))
                    }
                }
        }
    }
}

/// Observes a flow coordinator so its NavigationPath binding stays live.
private struct FlowStack<Coordinator: FlowCoordinator, Content: View>: View {
    @ObservedObject var coordinator: Coordinator
    @ViewBuilder let content: () -> Content

    var body: some View {
        NavigationStack(path: $coordinator.path) {
            content()
        }
    }
}

#Preview {
    ContentView()
        .environmentObject(DataStore())
        .environmentObject(AppCoordinator())
}
