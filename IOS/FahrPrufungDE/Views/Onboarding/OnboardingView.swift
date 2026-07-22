import SwiftUI

struct OnboardingView: View {
    @StateObject var viewModel: OnboardingViewModel
    @EnvironmentObject private var coordinator: AppCoordinator

    var body: some View {
        ZStack {
            AppTheme.screenBackground.ignoresSafeArea()
            RoadDecoration().ignoresSafeArea().allowsHitTesting(false)

            VStack(spacing: 0) {
                HStack {
                    Spacer()
                    if !viewModel.isLastPage {
                        Button(localized(\.skip)) {
                            complete(savingLanguage: false)
                        }
                        .font(AppTheme.captionFont())
                        .foregroundStyle(.secondary)
                    }
                }
                .padding(.horizontal, 24)
                .padding(.top, 16)

                TabView(selection: $viewModel.page) {
                    welcomePage.tag(0)
                    featuresPage.tag(1)
                    languagePage.tag(2)
                }
                .tabViewStyle(.page(indexDisplayMode: .always))
                .indexViewStyle(.page(backgroundDisplayMode: .always))

                bottomBar
                    .padding(.horizontal, 24)
                    .padding(.bottom, 32)
            }
        }
    }

    private var welcomePage: some View {
        VStack(spacing: 28) {
            Spacer()

            ZStack {
                Circle()
                    .fill(AppTheme.heroGradient)
                    .frame(width: 140, height: 140)
                    .shadow(color: AppTheme.roadNavy.opacity(0.2), radius: 20, y: 10)
                Image(systemName: "car.side.fill")
                    .font(.system(size: 56))
                    .foregroundStyle(.white)
            }

            VStack(spacing: 12) {
                Text(localized(\.welcomeTitle))
                    .font(AppTheme.titleFont(32))
                    .foregroundStyle(AppTheme.roadNavy)
                    .multilineTextAlignment(.center)

                Text(localized(\.welcomeSubtitle))
                    .font(AppTheme.bodyFont(16))
                    .foregroundStyle(.secondary)
                    .multilineTextAlignment(.center)
                    .padding(.horizontal, 24)
            }

            languageQuickPick

            Text(localized(\.disclaimer))
                .font(AppTheme.captionFont(11))
                .foregroundStyle(.secondary)
                .multilineTextAlignment(.center)
                .padding(.horizontal, 28)

            Spacer()
        }
        .padding(.horizontal, 20)
    }

    private var featuresPage: some View {
        VStack(alignment: .leading, spacing: 20) {
            Spacer()

            Text(localized(\.featuresTitle))
                .font(AppTheme.titleFont(28))
                .foregroundStyle(AppTheme.roadNavy)

            OnboardingFeatureRow(
                icon: "rectangle.on.rectangle.angled",
                text: localized(\.featureCards),
                colors: [AppTheme.highwayTeal, AppTheme.roadNavy]
            )
            OnboardingFeatureRow(
                icon: "brain.head.profile",
                text: localized(\.featureQuiz),
                colors: [AppTheme.signalAmber, Color(red: 0.92, green: 0.55, blue: 0.10)]
            )
            OnboardingFeatureRow(
                icon: "person.wave.2.fill",
                text: localized(\.featureExaminer),
                colors: CategoryStyle.style(for: "phrases").gradient
            )
            OnboardingFeatureRow(
                icon: "signpost.right.and.left.fill",
                text: localized(\.featureSigns),
                colors: [AppTheme.signalGreen, Color(red: 0.12, green: 0.58, blue: 0.38)]
            )

            Spacer()
        }
        .padding(.horizontal, 24)
    }

    private var languagePage: some View {
        VStack(spacing: 24) {
            Spacer()

            Image(systemName: "globe.europe.africa.fill")
                .font(.system(size: 48))
                .foregroundStyle(AppTheme.highwayTeal)

            Text(localized(\.languageTitle))
                .font(AppTheme.titleFont(28))
                .foregroundStyle(AppTheme.roadNavy)

            LanguagePickerCard(selection: $viewModel.draftLanguage)
                .padding(.horizontal, 4)

            Spacer()
        }
        .padding(.horizontal, 20)
    }

    private var languageQuickPick: some View {
        HStack(spacing: 10) {
            ForEach(AppLanguage.allCases) { language in
                Button {
                    withAnimation(.spring(response: 0.3)) {
                        viewModel.draftLanguage = language
                    }
                } label: {
                    Text(language.flag)
                        .font(.title2)
                        .padding(10)
                        .background(
                            Circle()
                                .fill(viewModel.draftLanguage == language ? AppTheme.signalAmber.opacity(0.25) : Color.white)
                                .shadow(color: AppTheme.cardShadow, radius: 4, y: 2)
                        )
                        .overlay {
                            if viewModel.draftLanguage == language {
                                Circle().stroke(AppTheme.signalAmber, lineWidth: 2)
                            }
                        }
                }
                .buttonStyle(.plain)
            }
        }
    }

    private var bottomBar: some View {
        Button {
            if viewModel.isLastPage {
                complete(savingLanguage: true)
            } else {
                withAnimation { viewModel.advance() }
            }
        } label: {
            Text(viewModel.isLastPage ? localized(\.start) : localized(\.next))
        }
        .buttonStyle(PrimaryButtonStyle())
    }

    private func complete(savingLanguage: Bool) {
        if savingLanguage {
            viewModel.finish()
        } else {
            viewModel.skip()
        }
        withAnimation(.spring(response: 0.4)) {
            coordinator.isOnboardingPresented = false
        }
    }

    /// Onboarding shows strings in the draft language the user is picking,
    /// before it is persisted in DataStore / LocalizationManager.
    private func localized(_ key: KeyPath<OnboardingTexts, String>) -> String {
        OnboardingTexts(language: viewModel.draftLanguage)[keyPath: key]
    }
}

/// Resolves onboarding strings against an explicit language (draft selection).
private struct OnboardingTexts {
    let language: AppLanguage

    var welcomeTitle: String { localized("onboarding.welcomeTitle", fallback: "Willkommen!") }
    var welcomeSubtitle: String {
        localized(
            "onboarding.welcomeSubtitle",
            fallback: "Lerne deutsche Begriffe für die praktische Prüfung — in deiner Sprache."
        )
    }
    var featuresTitle: String { localized("onboarding.featuresTitle", fallback: "So lernst du") }
    var featureCards: String {
        localized("onboarding.featureCards", fallback: "Karteikarten — deutsches Wort und Übersetzung")
    }
    var featureQuiz: String { localized("onboarding.featureQuiz", fallback: "Quiz — teste dich selbst") }
    var featureExaminer: String {
        localized("onboarding.featureExaminer", fallback: "Prüfer-Phrasen — was er sagt")
    }
    var featureSigns: String {
        localized("onboarding.featureSigns", fallback: "Verkehrszeichen — mit Erklärungen")
    }
    var languageTitle: String { localized("onboarding.languageTitle", fallback: "Wähle deine Sprache") }
    var disclaimer: String {
        localized(
            "settings.disclaimer",
            fallback: "Inoffizielle App zur Selbstvorbereitung. Ersetzt keine Fahrstunden und keine offiziellen StVO-/TÜV-Materialien."
        )
    }
    var start: String { localized("onboarding.start", fallback: "Lernen beginnen") }
    var next: String { localized("common.next", fallback: "Weiter") }
    var skip: String { localized("common.skip", fallback: "Überspringen") }

    private func localized(_ key: String, fallback: String) -> String {
        LocalizationManager.localized(key, for: language, fallback: fallback)
    }
}

private struct OnboardingFeatureRow: View {
    let icon: String
    let text: String
    let colors: [Color]

    var body: some View {
        HStack(spacing: 16) {
            ZStack {
                RoundedRectangle(cornerRadius: 12, style: .continuous)
                    .fill(LinearGradient(colors: colors, startPoint: .topLeading, endPoint: .bottomTrailing))
                    .frame(width: 44, height: 44)
                Image(systemName: icon)
                    .foregroundStyle(.white)
            }
            Text(text)
                .font(AppTheme.bodyFont(15))
                .foregroundStyle(AppTheme.roadNavy)
            Spacer()
        }
        .padding(14)
        .appCard(accent: colors.first ?? AppTheme.highwayTeal)
    }
}
