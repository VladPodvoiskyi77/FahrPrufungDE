import SwiftUI

struct CategoryListView: View {
    @StateObject var viewModel: CategoryListViewModel
    @EnvironmentObject private var store: DataStore
    @EnvironmentObject private var coordinator: AppCoordinator

    var body: some View {
        ScrollView {
            VStack(spacing: 12) {
                ForEach(Array(viewModel.categories.enumerated()), id: \.element.id) { index, category in
                    Button {
                        if category.id == "phrases" {
                            coordinator.learn.show(.examinerPhrases)
                        } else {
                            coordinator.learn.show(.terms(category))
                        }
                    } label: {
                        CategoryCard(
                            category: category,
                            termCount: viewModel.termCount(for: category),
                            language: viewModel.language
                        )
                    }
                    .buttonStyle(ScalePressButtonStyle())
                    .staggeredAppear(index: index)
                }
            }
            .padding(.horizontal, 20)
            .padding(.vertical, 16)
        }
        .appScreenBackground()
        .navigationTitle(L10n.Home.categoriesTitle)
        .navigationBarTitleDisplayMode(.large)
        .toolbarBackground(AppTheme.warmCream.opacity(0.9), for: .navigationBar)
        .onAppear {
            AnalyticsService.shared.logScreen("categories")
        }
    }
}
