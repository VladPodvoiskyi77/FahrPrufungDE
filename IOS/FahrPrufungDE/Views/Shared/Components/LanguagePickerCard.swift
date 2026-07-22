import SwiftUI

struct LanguagePickerCard: View {
    @Binding var selection: AppLanguage

    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            Label(L10n.Settings.language, systemImage: "globe")
                .font(AppTheme.headlineFont())
                .foregroundStyle(AppTheme.roadNavy)

            LazyVGrid(columns: [GridItem(.flexible()), GridItem(.flexible())], spacing: 10) {
                ForEach(AppLanguage.allCases) { language in
                    Button {
                        withAnimation(.spring(response: 0.3)) {
                            selection = language
                        }
                    } label: {
                        HStack(spacing: 8) {
                            Text(language.flag)
                                .font(.title3)
                            Text(language.displayName)
                                .font(AppTheme.captionFont(13))
                                .foregroundStyle(
                                    selection == language ? .white : AppTheme.roadNavy
                                )
                            Spacer()
                            if selection == language {
                                Image(systemName: "checkmark")
                                    .font(.caption.bold())
                                    .foregroundStyle(.white)
                            }
                        }
                        .padding(12)
                        .background(
                            RoundedRectangle(cornerRadius: 12, style: .continuous)
                                .fill(
                                    selection == language
                                        ? AnyShapeStyle(AppTheme.heroGradient)
                                        : AnyShapeStyle(AppTheme.cardWhite)
                                )
                                .shadow(
                                    color: selection == language
                                        ? AppTheme.roadNavy.opacity(0.2) : AppTheme.cardShadow,
                                    radius: selection == language ? 8 : 4,
                                    y: 2
                                )
                        )
                    }
                    .buttonStyle(.plain)
                }
            }
        }
        .padding(16)
        .appCard(accent: AppTheme.highwayTeal)
    }
}
