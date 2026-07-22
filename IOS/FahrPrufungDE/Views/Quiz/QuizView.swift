import SwiftUI

struct QuizView: View {
    @StateObject var viewModel: QuizViewModel
    @EnvironmentObject private var store: DataStore
    @State private var showsReview = false
    let title: String

    var body: some View {
        Group {
            if viewModel.isFinished {
                QuizResultView(
                    score: viewModel.score,
                    total: viewModel.questions.count,
                    onReview: { showsReview = true },
                    onRetry: {
                        showsReview = false
                        viewModel.start()
                    }
                )
                .transition(.scale(scale: 0.92).combined(with: .opacity))
            } else if let question = viewModel.currentQuestion {
                questionView(question)
                    .id(viewModel.currentIndex)
                    .transition(.asymmetric(
                        insertion: .move(edge: .trailing).combined(with: .opacity),
                        removal: .move(edge: .leading).combined(with: .opacity)
                    ))
            } else if viewModel.learningTerms.isEmpty {
                ContentUnavailableView(L10n.Known.allKnownQuiz, systemImage: "checkmark.circle.fill")
            } else {
                ContentUnavailableView(L10n.Quiz.tooFew, systemImage: "questionmark.circle")
            }
        }
        .appScreenBackground()
        .navigationTitle(title)
        .navigationBarTitleDisplayMode(.inline)
        .onAppear(perform: viewModel.startIfNeeded)
        .onAppear {
            AnalyticsService.shared.logScreen("quiz")
        }
        .onChange(of: store.nativeLanguage) { _, _ in
            viewModel.refreshTranslations()
        }
        .onChange(of: showsReview) { _, isShowing in
            if isShowing {
                AnalyticsService.shared.logQuizReviewOpened()
                AnalyticsService.shared.logScreen("quiz_review")
            }
        }
        .animation(AppMotion.spring, value: viewModel.currentIndex)
        .animation(AppMotion.spring, value: viewModel.isFinished)
        .sheet(isPresented: $showsReview) {
            NavigationStack {
                QuizReviewView(records: viewModel.answerRecords)
                    .toolbar {
                        ToolbarItem(placement: .cancellationAction) {
                            Button {
                                showsReview = false
                            } label: {
                                Image(systemName: "xmark.circle.fill")
                                    .font(.title3)
                                    .symbolRenderingMode(.hierarchical)
                                    .foregroundStyle(.secondary)
                            }
                        }
                    }
            }
            .presentationDetents([.large])
        }
    }

    private func questionView(_ question: QuizQuestion) -> some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 20) {
                QuizProgressHeader(
                    current: viewModel.currentIndex + 1,
                    total: viewModel.questions.count
                )

                VStack(alignment: .leading, spacing: 12) {
                    Text(L10n.Quiz.whatMeans)
                        .font(AppTheme.captionFont())
                        .foregroundStyle(.secondary)
                    Text(question.prompt)
                        .font(AppTheme.titleFont(24))
                        .foregroundStyle(AppTheme.roadNavy)
                }
                .padding(20)
                .frame(maxWidth: .infinity, alignment: .leading)
                .appCard(accent: AppTheme.signalAmber)

                ForEach(Array(question.options.enumerated()), id: \.element.id) { offset, option in
                    Button {
                        withAnimation(AppMotion.quick) {
                            viewModel.answer(option)
                        }
                    } label: {
                        QuizOptionCard(
                            text: option.text,
                            letter: viewModel.optionLetter(offset),
                            state: viewModel.optionState(for: option)
                        )
                    }
                    .buttonStyle(.plain)
                    .disabled(viewModel.hasAnswered)
                }

                if viewModel.hasAnswered {
                    Button(L10n.Common.continue) {
                        withAnimation(AppMotion.spring) {
                            viewModel.next()
                        }
                    }
                    .buttonStyle(PrimaryButtonStyle())
                    .transition(.move(edge: .bottom).combined(with: .opacity))
                }
            }
            .padding(20)
            .animation(AppMotion.spring, value: viewModel.hasAnswered)
        }
    }
}
