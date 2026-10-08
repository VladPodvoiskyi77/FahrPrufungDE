import SwiftUI

struct SettingsView: View {
    @StateObject var viewModel: SettingsViewModel
    @EnvironmentObject private var store: DataStore
    @EnvironmentObject private var coordinator: AppCoordinator
    @State private var showResetKnownAlert = false

    var body: some View {
        ScrollViewReader { proxy in
        ScrollView {
            VStack(alignment: .leading, spacing: 20) {
                ZStack(alignment: .bottomLeading) {
                    RoundedRectangle(cornerRadius: 24, style: .continuous)
                        .fill(AppTheme.heroGradient)
                        .frame(height: 120)
                    VStack(alignment: .leading, spacing: 6) {
                        Image(systemName: "gearshape.fill")
                            .font(.title2)
                            .foregroundStyle(.white.opacity(0.8))
                        Text(L10n.Settings.title)
                            .font(AppTheme.titleFont(26))
                            .foregroundStyle(.white)
                    }
                    .padding(24)
                }

                LanguagePickerCard(selection: $store.nativeLanguage)

                NavigationLink {
                    LearningProgressView(viewModel: ProgressViewModel(store: store))
                } label: {
                    HStack {
                        Image(systemName: "chart.line.uptrend.xyaxis")
                            .foregroundStyle(AppTheme.highwayTeal)
                        Text(L10n.Settings.viewProgress)
                            .font(AppTheme.bodyFont(15))
                            .foregroundStyle(AppTheme.roadNavy)
                        Spacer()
                        Image(systemName: "chevron.right")
                            .font(.caption.weight(.bold))
                            .foregroundStyle(.secondary)
                    }
                    .padding(16)
                    .appCard(accent: AppTheme.highwayTeal)
                }

                VStack(alignment: .leading, spacing: 12) {
                    SectionHeader(title: L10n.Settings.statistics)

                    HStack(spacing: 12) {
                        InfoTile(
                            value: "\(viewModel.termCount)",
                            label: L10n.Settings.terms,
                            icon: "text.book.closed.fill",
                            color: AppTheme.highwayTeal
                        )
                        InfoTile(
                            value: "\(viewModel.categoryCount)",
                            label: L10n.Settings.categories,
                            icon: "folder.fill",
                            color: AppTheme.roadNavy
                        )
                    }
                    InfoTile(
                        value: "\(viewModel.signCount)",
                        label: L10n.Settings.signs,
                        icon: "signpost.right.fill",
                        color: AppTheme.signalAmber,
                        wide: true
                    )
                }

                if viewModel.hasKnownItems {
                    VStack(alignment: .leading, spacing: 12) {
                        SectionHeader(title: L10n.Known.settingsSection, icon: "checkmark.circle.fill")

                        VStack(spacing: 8) {
                            if viewModel.knownTermCount > 0 {
                                knownStatRow(
                                    count: viewModel.knownTermCount,
                                    label: L10n.Known.termsMarked
                                )
                            }
                            if viewModel.knownSignCount > 0 {
                                knownStatRow(
                                    count: viewModel.knownSignCount,
                                    label: L10n.Known.signsMarked
                                )
                            }
                        }

                        Button {
                            showResetKnownAlert = true
                        } label: {
                            HStack {
                                Image(systemName: "arrow.counterclockwise")
                                    .foregroundStyle(AppTheme.signalGreen)
                                Text(L10n.Known.resetTitle)
                                    .font(AppTheme.bodyFont(15))
                                    .foregroundStyle(AppTheme.roadNavy)
                                Spacer()
                            }
                            .padding(16)
                            .appCard(accent: AppTheme.signalGreen)
                        }
                        .buttonStyle(.plain)
                    }
                }

                Toggle(isOn: Binding(
                    get: { viewModel.analyticsEnabled },
                    set: { viewModel.analyticsEnabled = $0 }
                )) {
                    VStack(alignment: .leading, spacing: 4) {
                        Text(L10n.Settings.analytics)
                            .font(AppTheme.bodyFont(15))
                            .foregroundStyle(AppTheme.roadNavy)
                        Text(L10n.Settings.analyticsSubtitle)
                            .font(AppTheme.captionFont(12))
                            .foregroundStyle(.secondary)
                    }
                }
                .padding(16)
                .appCard(accent: AppTheme.roadNavy)

                Button {
                    viewModel.resetOnboarding()
                } label: {
                    HStack {
                        Image(systemName: "hand.wave.fill")
                            .foregroundStyle(AppTheme.highwayTeal)
                        Text(L10n.Settings.replayOnboarding)
                            .font(AppTheme.bodyFont(15))
                            .foregroundStyle(AppTheme.roadNavy)
                        Spacer()
                        Image(systemName: "chevron.right")
                            .font(.caption.weight(.bold))
                            .foregroundStyle(.secondary)
                    }
                    .padding(16)
                    .appCard(accent: AppTheme.highwayTeal)
                }
                .buttonStyle(.plain)

                Link(destination: AppLinks.mailtoURL) {
                    HStack {
                        Image(systemName: "envelope.fill")
                            .foregroundStyle(AppTheme.roadNavy)
                        Text(L10n.Settings.contactDeveloper)
                            .font(AppTheme.bodyFont(15))
                            .foregroundStyle(AppTheme.roadNavy)
                        Spacer()
                        Image(systemName: "chevron.right")
                            .font(.caption.weight(.bold))
                            .foregroundStyle(.secondary)
                    }
                    .padding(16)
                    .appCard(accent: AppTheme.roadNavy)
                }

                if let privacyURL = AppLinks.privacyPolicyURL {
                    Link(destination: privacyURL) {
                        HStack {
                            Image(systemName: "hand.raised.fill")
                                .foregroundStyle(AppTheme.roadNavy)
                            Text(L10n.Settings.privacyPolicy)
                                .font(AppTheme.bodyFont(15))
                                .foregroundStyle(AppTheme.roadNavy)
                            Spacer()
                            Image(systemName: "arrow.up.right")
                                .font(.caption.weight(.bold))
                                .foregroundStyle(.secondary)
                        }
                        .padding(16)
                        .appCard(accent: AppTheme.roadNavy)
                    }
                    .id("privacyPolicy")
                }

                VStack(alignment: .leading, spacing: 8) {
                    Label(L10n.Settings.disclaimerTitle, systemImage: "info.circle.fill")
                        .font(AppTheme.headlineFont(14))
                        .foregroundStyle(AppTheme.roadNavy)
                    Text(L10n.Settings.disclaimer)
                        .font(AppTheme.bodyFont(13))
                        .foregroundStyle(.secondary)
                        .lineSpacing(4)
                }
                .padding(16)
                .appCard(accent: AppTheme.roadNavy)

                VStack(alignment: .leading, spacing: 8) {
                    Image(systemName: "heart.fill")
                        .foregroundStyle(AppTheme.signalRed.opacity(0.7))
                    Text(L10n.Settings.about)
                        .font(AppTheme.bodyFont(14))
                        .foregroundStyle(.secondary)
                        .lineSpacing(4)
                }
                .padding(16)
                .appCard(accent: AppTheme.signalAmber)

                VStack(alignment: .leading, spacing: 12) {
                    SectionHeader(title: L10n.Settings.otherProjects, icon: "square.grid.2x2.fill")

                    Link(destination: AppLinks.prapoDeAppStoreURL) {
                        HStack(spacing: 14) {
                            Image("PrapoDeIcon")
                                .resizable()
                                .aspectRatio(contentMode: .fill)
                                .frame(width: 52, height: 52)
                                .clipShape(RoundedRectangle(cornerRadius: 12, style: .continuous))

                            VStack(alignment: .leading, spacing: 4) {
                                Text(L10n.Settings.prapodeTitle)
                                    .font(AppTheme.headlineFont(15))
                                    .foregroundStyle(AppTheme.roadNavy)
                                Text(L10n.Settings.prapodeSubtitle)
                                    .font(AppTheme.captionFont(12))
                                    .foregroundStyle(.secondary)
                            }

                            Spacer()

                            Image(systemName: "arrow.up.right")
                                .font(.caption.weight(.bold))
                                .foregroundStyle(.secondary)
                        }
                        .padding(16)
                        .appCard(accent: AppTheme.highwayTeal)
                    }
                }
            }
            .padding(.horizontal, 20)
            .padding(.bottom, 32)
        }
        .appScreenBackground()
        .navigationBarHidden(true)
        .onAppear {
            AnalyticsService.shared.logScreen("settings")
            scrollToPrivacyIfNeeded(proxy: proxy)
        }
        .onChange(of: coordinator.scrollSettingsToPrivacy) { _, shouldScroll in
            if shouldScroll { scrollToPrivacyIfNeeded(proxy: proxy) }
        }
        .alert(L10n.Known.resetConfirmTitle, isPresented: $showResetKnownAlert) {
            Button(L10n.Known.cancel, role: .cancel) {}
            Button(L10n.Known.resetConfirm, role: .destructive) {
                viewModel.resetKnownItems()
            }
        } message: {
            Text(L10n.Known.resetConfirmMessage)
        }
        } // ScrollViewReader
    }

    private func scrollToPrivacyIfNeeded(proxy: ScrollViewProxy) {
        guard coordinator.scrollSettingsToPrivacy else { return }
        DispatchQueue.main.asyncAfter(deadline: .now() + 0.35) {
            withAnimation {
                proxy.scrollTo("privacyPolicy", anchor: .center)
            }
            coordinator.scrollSettingsToPrivacy = false
        }
    }

    private func knownStatRow(count: Int, label: String) -> some View {
        HStack {
            Text("\(count)")
                .font(AppTheme.headlineFont(18))
                .foregroundStyle(AppTheme.signalGreen)
            Text(label)
                .font(AppTheme.bodyFont(14))
                .foregroundStyle(.secondary)
            Spacer()
        }
        .padding(.horizontal, 16)
        .padding(.vertical, 12)
        .appCard(accent: AppTheme.signalGreen)
    }
}
