import SwiftUI

struct TermListView: View {
    @StateObject var viewModel: TermListViewModel
    @EnvironmentObject private var store: DataStore
    @EnvironmentObject private var coordinator: AppCoordinator

    private var style: CategoryStyle {
        CategoryStyle.style(for: viewModel.category.id)
    }

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 16) {
                header

                HStack(spacing: 12) {
                    Button {
                        coordinator.learn.show(
                            .flashcards(terms: viewModel.terms, title: viewModel.categoryTitle)
                        )
                    } label: {
                        ModeChip(title: L10n.Category.cards, icon: "rectangle.on.rectangle.angled", color: style.color)
                    }
                    .buttonStyle(.plain)
                    .disabled(viewModel.learningTerms.isEmpty)

                    Button {
                        coordinator.learn.show(
                            .quiz(terms: viewModel.terms, title: viewModel.categoryTitle)
                        )
                    } label: {
                        ModeChip(title: L10n.Category.quiz, icon: "questionmark.circle.fill", color: AppTheme.signalAmber)
                    }
                    .buttonStyle(.plain)
                    .disabled(viewModel.learningTerms.isEmpty)
                }

                SectionHeader(title: L10n.Category.terms)

                ForEach(viewModel.terms) { term in
                    TermRowCard(
                        term: term,
                        language: viewModel.language,
                        style: style,
                        isKnown: viewModel.isKnown(term),
                        onToggleKnown: { viewModel.toggleKnown(term) }
                    )
                }
            }
            .padding(.horizontal, 20)
            .padding(.bottom, 32)
        }
        .appScreenBackground()
        .navigationTitle(viewModel.categoryTitle)
        .navigationBarTitleDisplayMode(.inline)
        .onAppear {
            AnalyticsService.shared.logScreen("term_list", parameters: ["category_id": viewModel.category.id])
        }
    }

    private var header: some View {
        HStack(spacing: 14) {
            ZStack {
                RoundedRectangle(cornerRadius: 16, style: .continuous)
                    .fill(LinearGradient(colors: style.gradient, startPoint: .topLeading, endPoint: .bottomTrailing))
                    .frame(width: 56, height: 56)
                Image(systemName: style.icon)
                    .font(.title2)
                    .foregroundStyle(.white)
            }
            VStack(alignment: .leading, spacing: 4) {
                Text(viewModel.category.displayDe)
                    .font(AppTheme.headlineFont(20))
                    .foregroundStyle(AppTheme.roadNavy)
                Text(L10n.Category.termCount(viewModel.terms.count))
                    .font(AppTheme.captionFont())
                    .foregroundStyle(.secondary)
                if viewModel.knownCount > 0 {
                    Text(L10n.Known.listHiddenCount(viewModel.knownCount))
                        .font(AppTheme.captionFont(11))
                        .foregroundStyle(AppTheme.signalGreen)
                }
            }
            Spacer()
        }
        .padding(16)
        .appCard(accent: style.color)
    }
}
