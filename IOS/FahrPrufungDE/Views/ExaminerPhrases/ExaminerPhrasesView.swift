import SwiftUI

struct ExaminerPhrasesView: View {
    @StateObject var viewModel: ExaminerPhrasesViewModel
    @EnvironmentObject private var coordinator: AppCoordinator

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 16) {
                header
                modeButtons
                groupFilters
                phraseList
            }
            .padding(.horizontal, 20)
            .padding(.bottom, 32)
        }
        .appScreenBackground()
        .navigationTitle(L10n.Home.ExaminerPhrases.title)
        .navigationBarTitleDisplayMode(.inline)
        .onAppear {
            AnalyticsService.shared.logScreen("examiner_phrases")
        }
    }

    private var header: some View {
        HStack(spacing: 14) {
            ZStack {
                RoundedRectangle(cornerRadius: 16, style: .continuous)
                    .fill(LinearGradient(colors: viewModel.style.gradient, startPoint: .topLeading, endPoint: .bottomTrailing))
                    .frame(width: 56, height: 56)
                Image(systemName: "person.wave.2.fill")
                    .font(.title2)
                    .foregroundStyle(.white)
            }
            VStack(alignment: .leading, spacing: 4) {
                Text(L10n.ExaminerPhrases.listTitle)
                    .font(AppTheme.headlineFont(20))
                    .foregroundStyle(AppTheme.roadNavy)
                Text(L10n.Category.termCount(viewModel.allTerms.count))
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
        .appCard(accent: viewModel.style.color)
    }

    private var modeButtons: some View {
        HStack(spacing: 12) {
            ModeChip(
                title: L10n.ExaminerPhrases.listMode,
                icon: "list.bullet",
                color: viewModel.style.color
            )

            Button {
                coordinator.learn.show(
                    .flashcards(terms: viewModel.filteredTerms, title: L10n.Home.ExaminerPhrases.title)
                )
            } label: {
                ModeChip(
                    title: L10n.Category.cards,
                    icon: "rectangle.on.rectangle.angled",
                    color: viewModel.style.color
                )
            }
            .buttonStyle(.plain)
            .disabled(viewModel.learningTerms.isEmpty)

            Button {
                coordinator.learn.show(
                    .quiz(terms: viewModel.filteredTerms, title: L10n.Home.ExaminerPhrases.title)
                )
            } label: {
                ModeChip(title: L10n.Category.quiz, icon: "questionmark.circle.fill", color: AppTheme.signalAmber)
            }
            .buttonStyle(.plain)
            .disabled(viewModel.learningTerms.isEmpty)
        }
    }

    private var groupFilters: some View {
        ScrollView(.horizontal, showsIndicators: false) {
            HStack(spacing: 8) {
                FilterChip(
                    title: L10n.Common.all,
                    isSelected: viewModel.selectedGroup == nil,
                    color: viewModel.style.color
                ) {
                    viewModel.selectGroup(nil)
                }

                ForEach(ExaminerPhraseGroup.allCases) { group in
                    let count = viewModel.termCount(for: group)
                    if count > 0 {
                        FilterChip(
                            title: "\(group.title()) (\(count))",
                            isSelected: viewModel.selectedGroup == group,
                            color: viewModel.style.color
                        ) {
                            viewModel.selectGroup(group)
                        }
                    }
                }
            }
            .padding(.vertical, 2)
        }
    }

    @ViewBuilder
    private var phraseList: some View {
        if let selected = viewModel.selectedGroup {
            sectionBlock(group: selected, terms: viewModel.filteredTerms, showBadge: false)
        } else {
            ForEach(viewModel.groupedSections, id: \.group.id) { section in
                sectionBlock(group: section.group, terms: section.terms, showBadge: false)
            }
        }
    }

    private func sectionBlock(
        group: ExaminerPhraseGroup,
        terms: [VocabularyTerm],
        showBadge: Bool
    ) -> some View {
        VStack(alignment: .leading, spacing: 10) {
            SectionHeader(title: group.title(), icon: group.icon)

            ForEach(terms) { term in
                ExaminerPhraseRowCard(
                    term: term,
                    language: viewModel.language,
                    group: showBadge ? group : nil,
                    style: viewModel.style,
                    isKnown: viewModel.isKnown(term),
                    onToggleKnown: { viewModel.toggleKnown(term) }
                )
            }
        }
    }
}
