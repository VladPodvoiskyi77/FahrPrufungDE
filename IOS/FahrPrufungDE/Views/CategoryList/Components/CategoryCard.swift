import SwiftUI

struct CategoryCard: View {
    let category: VocabularyCategory
    let termCount: Int
    let language: AppLanguage

    private var style: CategoryStyle {
        CategoryStyle.style(for: category.id)
    }

    var body: some View {
        HStack(spacing: 16) {
            ZStack {
                RoundedRectangle(cornerRadius: 14, style: .continuous)
                    .fill(
                        LinearGradient(
                            colors: style.gradient,
                            startPoint: .topLeading,
                            endPoint: .bottomTrailing
                        )
                    )
                    .frame(width: 48, height: 48)
                Image(systemName: style.icon)
                    .font(.body.weight(.semibold))
                    .foregroundStyle(.white)
            }

            VStack(alignment: .leading, spacing: 4) {
                Text(category.title(for: language))
                    .font(AppTheme.headlineFont())
                    .foregroundStyle(AppTheme.roadNavy)
                Text(category.displayDe)
                    .font(AppTheme.captionFont())
                    .foregroundStyle(.secondary)
            }

            Spacer()

            Text("\(termCount)")
                .font(AppTheme.headlineFont(15))
                .foregroundStyle(style.color)
                .frame(minWidth: 32)
                .padding(.horizontal, 10)
                .padding(.vertical, 6)
                .background(
                    Capsule().fill(style.color.opacity(0.12))
                )

            Image(systemName: "chevron.right")
                .font(.caption.weight(.bold))
                .foregroundStyle(style.color.opacity(0.6))
        }
        .padding(14)
        .appCard(accent: style.color)
    }
}
