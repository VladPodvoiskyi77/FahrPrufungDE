import SwiftUI

struct FlashcardView: View {
    @StateObject var viewModel: FlashcardViewModel
    let title: String

    @EnvironmentObject private var store: DataStore

    var body: some View {
        VStack(spacing: 24) {
            if let term = viewModel.current {
                Text(L10n.Flashcards.counter(viewModel.index + 1, viewModel.deck.count))
                    .font(AppTheme.captionFont())
                    .foregroundStyle(.secondary)
                    .padding(.top, 8)
                    .contentTransition(.numericText())
                    .animation(AppMotion.quick, value: viewModel.index)

                Button {
                    withAnimation(.spring(response: 0.4, dampingFraction: 0.75)) {
                        viewModel.flip()
                    }
                } label: {
                    FlashcardSurface(
                        term: term,
                        language: store.nativeLanguage,
                        isFlipped: viewModel.isFlipped,
                        progress: viewModel.progress
                    )
                }
                .buttonStyle(.plain)
                .padding(.horizontal, 20)
                .id(viewModel.index)
                .transition(.asymmetric(
                    insertion: .move(edge: .trailing).combined(with: .opacity),
                    removal: .move(edge: .leading).combined(with: .opacity)
                ))

                HStack(spacing: 40) {
                    NavCircleButton(icon: "chevron.left", enabled: viewModel.canGoBack) {
                        withAnimation(.spring(response: 0.35)) {
                            viewModel.move(by: -1)
                        }
                    }
                    NavCircleButton(icon: "arrow.triangle.2.circlepath", enabled: true) {
                        withAnimation(.spring(response: 0.35)) {
                            viewModel.resetFlip()
                        }
                    }
                    NavCircleButton(icon: "chevron.right", enabled: viewModel.canGoForward) {
                        withAnimation(.spring(response: 0.35)) {
                            viewModel.move(by: 1)
                        }
                    }
                }

                KnownMarkButton(isKnown: viewModel.isCurrentKnown) {
                    withAnimation(.spring(response: 0.35)) {
                        viewModel.toggleKnownForCurrent()
                    }
                }
                .padding(.horizontal, 20)
            } else if viewModel.deck.isEmpty {
                ContentUnavailableView(
                    L10n.Known.allKnownFlashcards,
                    systemImage: "checkmark.circle.fill"
                )
            } else {
                ContentUnavailableView(L10n.Flashcards.empty, systemImage: "text.book.closed")
            }

            Spacer(minLength: 0)
        }
        .appScreenBackground()
        .navigationTitle(title)
        .navigationBarTitleDisplayMode(.inline)
        .animation(AppMotion.spring, value: viewModel.index)
        .onAppear {
            AnalyticsService.shared.logScreen("flashcards")
        }
        .onDisappear {
            viewModel.finishSessionIfNeeded()
        }
    }
}
