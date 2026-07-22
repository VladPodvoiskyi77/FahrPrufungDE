import SwiftUI

enum AppTheme {
    // MARK: - Brand palette (Open Road)

    static let roadNavy = Color(red: 0.11, green: 0.20, blue: 0.34)
    static let highwayTeal = Color(red: 0.16, green: 0.44, blue: 0.50)
    static let signalAmber = Color(red: 0.96, green: 0.65, blue: 0.14)
    static let signalGreen = Color(red: 0.18, green: 0.72, blue: 0.45)
    static let signalRed = Color(red: 0.90, green: 0.28, blue: 0.28)
    static let warmCream = Color(red: 0.97, green: 0.95, blue: 0.91)
    static let asphalt = Color(red: 0.14, green: 0.15, blue: 0.17)
    static let cardWhite = Color(red: 1.0, green: 0.99, blue: 0.97)

    static let heroGradient = LinearGradient(
        colors: [roadNavy, highwayTeal.opacity(0.92)],
        startPoint: .topLeading,
        endPoint: .bottomTrailing
    )

    static let accentGradient = LinearGradient(
        colors: [signalAmber, Color(red: 0.98, green: 0.78, blue: 0.22)],
        startPoint: .leading,
        endPoint: .trailing
    )

    static let screenBackground = LinearGradient(
        colors: [
            warmCream,
            Color(red: 0.94, green: 0.96, blue: 0.98)
        ],
        startPoint: .top,
        endPoint: .bottom
    )

    // MARK: - Typography

    static func titleFont(_ size: CGFloat = 28) -> Font {
        .system(size: size, weight: .bold, design: .rounded)
    }

    static func headlineFont(_ size: CGFloat = 17) -> Font {
        .system(size: size, weight: .semibold, design: .rounded)
    }

    static func bodyFont(_ size: CGFloat = 16) -> Font {
        .system(size: size, weight: .regular, design: .rounded)
    }

    static func captionFont(_ size: CGFloat = 13) -> Font {
        .system(size: size, weight: .medium, design: .rounded)
    }

    // MARK: - Layout

    static let cardRadius: CGFloat = 20
    static let chipRadius: CGFloat = 12
    static let cardShadow = Color.black.opacity(0.08)
}

// MARK: - Motion

enum AppMotion {
    static let spring = Animation.spring(response: 0.45, dampingFraction: 0.82)
    static let quick = Animation.spring(response: 0.32, dampingFraction: 0.78)
    static let gentle = Animation.easeOut(duration: 0.35)
}

struct StaggeredAppearModifier: ViewModifier {
    let index: Int
    @State private var visible = false

    func body(content: Content) -> some View {
        content
            .opacity(visible ? 1 : 0)
            .offset(y: visible ? 0 : 18)
            .onAppear {
                withAnimation(AppMotion.spring.delay(Double(index) * 0.07)) {
                    visible = true
                }
            }
    }
}

struct ScalePressButtonStyle: ButtonStyle {
    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .scaleEffect(configuration.isPressed ? 0.97 : 1)
            .animation(AppMotion.quick, value: configuration.isPressed)
    }
}

// MARK: - View modifiers

struct AppScreenBackground: ViewModifier {
    func body(content: Content) -> some View {
        ZStack {
            AppTheme.screenBackground.ignoresSafeArea()
            RoadDecoration()
                .ignoresSafeArea()
                .allowsHitTesting(false)
            content
        }
    }
}

struct AppCardStyle: ViewModifier {
    var accent: Color = AppTheme.highwayTeal

    func body(content: Content) -> some View {
        content
            .background {
                RoundedRectangle(cornerRadius: AppTheme.cardRadius, style: .continuous)
                    .fill(AppTheme.cardWhite)
                    .shadow(color: AppTheme.cardShadow, radius: 12, y: 4)
                    .overlay(alignment: .leading) {
                        RoundedRectangle(cornerRadius: 4, style: .continuous)
                            .fill(accent)
                            .frame(width: 4)
                            .padding(.vertical, 12)
                            .padding(.leading, 4)
                    }
            }
    }
}

struct PrimaryButtonStyle: ButtonStyle {
    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .font(AppTheme.headlineFont())
            .foregroundStyle(.white)
            .frame(maxWidth: .infinity)
            .padding(.vertical, 16)
            .background {
                RoundedRectangle(cornerRadius: AppTheme.chipRadius, style: .continuous)
                    .fill(AppTheme.accentGradient)
                    .opacity(configuration.isPressed ? 0.85 : 1)
            }
            .scaleEffect(configuration.isPressed ? 0.98 : 1)
            .animation(.easeOut(duration: 0.15), value: configuration.isPressed)
    }
}

extension View {
    func appScreenBackground() -> some View {
        modifier(AppScreenBackground())
    }

    func appCard(accent: Color = AppTheme.highwayTeal) -> some View {
        modifier(AppCardStyle(accent: accent))
    }

    func staggeredAppear(index: Int) -> some View {
        modifier(StaggeredAppearModifier(index: index))
    }
}
