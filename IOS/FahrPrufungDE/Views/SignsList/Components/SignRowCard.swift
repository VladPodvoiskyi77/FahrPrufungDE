import SwiftUI

struct SignRowCard: View {
    let sign: TrafficSign
    let language: AppLanguage
    var isKnown: Bool = false

    var body: some View {
        HStack(spacing: 16) {
            SignPlaceholderView(sign: sign, size: 72)

            VStack(alignment: .leading, spacing: 4) {
                Text(sign.translation(for: language))
                    .font(AppTheme.headlineFont(15))
                    .foregroundStyle(AppTheme.roadNavy)
                    .lineLimit(2)
                Text(sign.de)
                    .font(AppTheme.captionFont(12))
                    .foregroundStyle(.secondary)
                    .lineLimit(2)
                if let code = sign.stvoCode, code != "—" {
                    Text("StVO \(code)")
                        .font(AppTheme.captionFont(10))
                        .foregroundStyle(SignStyle.categoryColor(sign.category))
                }
            }

            Spacer(minLength: 0)

            Image(systemName: "chevron.right")
                .font(.caption.weight(.bold))
                .foregroundStyle(SignStyle.categoryColor(sign.category).opacity(0.5))
        }
        .padding(14)
        .appCard(accent: SignStyle.categoryColor(sign.category))
        .knownDimmed(isKnown)
    }
}
