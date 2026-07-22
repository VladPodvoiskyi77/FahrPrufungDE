import SwiftUI

struct SignsListView: View {
    @StateObject var viewModel: SignsListViewModel
    @EnvironmentObject private var store: DataStore
    @EnvironmentObject private var coordinator: AppCoordinator

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 16) {
                signsHero
                searchField
                categoryFilter

                SectionHeader(
                    title: L10n.Signs.section(viewModel.filteredSigns.count),
                    icon: "signpost.right.fill"
                )

                if viewModel.filteredSigns.isEmpty {
                    ContentUnavailableView(
                        L10n.Signs.Empty.title,
                        systemImage: "magnifyingglass",
                        description: Text(L10n.Signs.Empty.subtitle)
                    )
                    .padding(.top, 24)
                } else {
                    LazyVStack(spacing: 10) {
                        ForEach(Array(viewModel.filteredSigns.enumerated()), id: \.element.id) { index, sign in
                            HStack(spacing: 10) {
                                KnownMarkButton(
                                    isKnown: viewModel.isKnown(sign),
                                    style: .compact
                                ) {
                                    viewModel.toggleKnown(sign)
                                }

                                Button {
                                    coordinator.signs.show(.detail(sign))
                                } label: {
                                    SignRowCard(
                                        sign: sign,
                                        language: viewModel.language,
                                        isKnown: viewModel.isKnown(sign)
                                    )
                                }
                                .buttonStyle(ScalePressButtonStyle())
                            }
                            .staggeredAppear(index: min(index, 8))
                        }
                    }
                }
            }
            .padding(.horizontal, 20)
            .padding(.bottom, 32)
        }
        .appScreenBackground()
        .navigationTitle(L10n.Signs.title)
        .navigationBarTitleDisplayMode(.large)
        .onAppear {
            AnalyticsService.shared.logScreen("signs_list")
        }
    }

    @ViewBuilder
    private var signsHero: some View {
        if let heroSign = viewModel.heroSign {
            HStack(spacing: 16) {
                SignPlaceholderView(sign: heroSign, size: 80)
                VStack(alignment: .leading, spacing: 6) {
                    Text(L10n.Signs.count(viewModel.signCount))
                        .font(AppTheme.titleFont(22))
                        .foregroundStyle(AppTheme.roadNavy)
                    Text(L10n.Signs.heroSubtitle)
                        .font(AppTheme.captionFont())
                        .foregroundStyle(.secondary)
                }
                Spacer()
            }
            .padding(16)
            .appCard(accent: AppTheme.signalAmber)
            .staggeredAppear(index: 0)
        }
    }

    private var searchField: some View {
        HStack(spacing: 10) {
            Image(systemName: "magnifyingglass")
                .foregroundStyle(.secondary)
            TextField(L10n.Signs.searchPlaceholder, text: $viewModel.searchText)
                .font(AppTheme.bodyFont(15))
            if !viewModel.searchText.isEmpty {
                Button {
                    viewModel.searchText = ""
                } label: {
                    Image(systemName: "xmark.circle.fill")
                        .foregroundStyle(.secondary)
                }
            }
        }
        .padding(14)
        .background(
            RoundedRectangle(cornerRadius: AppTheme.chipRadius, style: .continuous)
                .fill(AppTheme.cardWhite)
                .shadow(color: AppTheme.cardShadow, radius: 6, y: 2)
        )
    }

    private var categoryFilter: some View {
        ScrollView(.horizontal, showsIndicators: false) {
            HStack(spacing: 8) {
                FilterChip(
                    title: L10n.Common.all,
                    isSelected: viewModel.selectedCategory == nil,
                    color: AppTheme.roadNavy
                ) {
                    viewModel.selectedCategory = nil
                }

                ForEach(viewModel.categories) { category in
                    FilterChip(
                        title: category.title(for: viewModel.language),
                        isSelected: viewModel.selectedCategory == category.id,
                        color: SignStyle.categoryColor(category.id)
                    ) {
                        viewModel.selectedCategory = category.id
                    }
                }
            }
        }
    }
}
