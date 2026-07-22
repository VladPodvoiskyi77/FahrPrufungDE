import SwiftUI

struct TermRowCard: View {
    let term: VocabularyTerm
    let language: AppLanguage
    var style: CategoryStyle = CategoryStyle.style(for: "exam")
    var isKnown: Bool = false
    var onToggleKnown: (() -> Void)?

    var body: some View {
        HStack(alignment: .top, spacing: 10) {
            if let onToggleKnown {
                KnownMarkButton(isKnown: isKnown, style: .compact, action: onToggleKnown)
                    .padding(.top, 2)
            }

            VStack(alignment: .leading, spacing: 8) {
                HStack(alignment: .top) {
                    Text(term.displayDe)
                        .font(AppTheme.headlineFont())
                        .foregroundStyle(AppTheme.roadNavy)
                    Spacer()
                    if term.isCore {
                        CoreTermBadge()
                    }
                }

                Text(term.displayTranslation(for: language))
                    .font(AppTheme.bodyFont(15))
                    .foregroundStyle(.secondary)

                if let phrase = term.displayExamPhraseDe {
                    HStack(alignment: .top, spacing: 6) {
                        Image(systemName: "person.wave.2.fill")
                            .font(.caption)
                            .foregroundStyle(style.color)
                        Text(phrase)
                            .font(AppTheme.captionFont(12))
                            .foregroundStyle(style.color)
                            .italic()
                    }
                    .padding(10)
                    .frame(maxWidth: .infinity, alignment: .leading)
                    .background(
                        RoundedRectangle(cornerRadius: 10, style: .continuous)
                            .fill(style.color.opacity(0.08))
                    )
                }
            }
        }
        .padding(14)
        .appCard(accent: style.color)
        .knownDimmed(isKnown)
    }
}
