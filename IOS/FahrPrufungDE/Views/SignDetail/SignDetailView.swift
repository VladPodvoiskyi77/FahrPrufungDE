import SwiftUI

struct SignDetailView: View {
    @StateObject var viewModel: SignDetailViewModel
    @EnvironmentObject private var store: DataStore

    private var sign: TrafficSign { viewModel.sign }

    var body: some View {
        ScrollView {
            VStack(spacing: 24) {
                SignPlaceholderView(sign: sign, size: 180)
                    .padding(.top, 16)
                    .shadow(color: AppTheme.cardShadow, radius: 16, y: 6)

                VStack(spacing: 8) {
                    Text(viewModel.title)
                        .font(AppTheme.titleFont(24))
                        .foregroundStyle(AppTheme.roadNavy)
                        .multilineTextAlignment(.center)

                    Text(sign.de)
                        .font(AppTheme.headlineFont(17))
                        .foregroundStyle(.secondary)
                        .multilineTextAlignment(.center)
                }

                HStack(spacing: 10) {
                    if let code = sign.stvoCode, code != "—" {
                        Label("StVO \(code)", systemImage: "doc.text")
                            .font(AppTheme.captionFont(11))
                            .foregroundStyle(SignStyle.categoryColor(sign.category))
                            .padding(.horizontal, 12)
                            .padding(.vertical, 6)
                            .background(Capsule().fill(SignStyle.categoryColor(sign.category).opacity(0.12)))
                    }

                    Text(viewModel.categoryLabel)
                        .font(AppTheme.captionFont(11))
                        .foregroundStyle(AppTheme.highwayTeal)
                        .padding(.horizontal, 12)
                        .padding(.vertical, 6)
                        .background(Capsule().fill(AppTheme.highwayTeal.opacity(0.12)))
                }

                if let note = viewModel.note {
                    VStack(alignment: .leading, spacing: 10) {
                        Label(L10n.Signs.explanation, systemImage: "lightbulb.fill")
                            .font(AppTheme.headlineFont())
                            .foregroundStyle(AppTheme.roadNavy)

                        Text(note)
                            .font(AppTheme.bodyFont(15))
                            .foregroundStyle(.secondary)
                            .lineSpacing(4)
                    }
                    .padding(18)
                    .frame(maxWidth: .infinity, alignment: .leading)
                    .appCard(accent: SignStyle.categoryColor(sign.category))
                }

                germanNoteCard

                KnownMarkButton(isKnown: store.isSignKnown(sign.id)) {
                    if store.isSignKnown(sign.id) {
                        store.knownUndo.dismiss()
                        store.setSignKnown(sign.id, known: false)
                    } else {
                        store.markSignAsKnown(sign.id)
                    }
                }
            }
            .padding(.horizontal, 20)
            .padding(.bottom, 32)
        }
        .appScreenBackground()
        .navigationBarTitleDisplayMode(.inline)
        .onAppear {
            AnalyticsService.shared.logScreen(
                "sign_detail",
                parameters: ["stvo_code": sign.stvoCode ?? "unknown"]
            )
        }
    }

    private var germanNoteCard: some View {
        VStack(alignment: .leading, spacing: 8) {
            HStack {
                Text("🇩🇪")
                Text(L10n.Signs.inGerman)
                    .font(AppTheme.captionFont())
                    .foregroundStyle(.secondary)
            }
            Text(sign.de)
                .font(AppTheme.bodyFont(15))
                .foregroundStyle(AppTheme.roadNavy)
        }
        .padding(16)
        .frame(maxWidth: .infinity, alignment: .leading)
        .background(
            RoundedRectangle(cornerRadius: 16, style: .continuous)
                .fill(AppTheme.highwayTeal.opacity(0.06))
        )
    }
}
