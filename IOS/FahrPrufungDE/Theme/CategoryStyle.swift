import SwiftUI

struct CategoryStyle {
    let icon: String
    let color: Color
    let gradient: [Color]

    static func style(for categoryID: String) -> CategoryStyle {
        switch categoryID {
        case "exam":
            return CategoryStyle(
                icon: "checkmark.seal.fill",
                color: AppTheme.roadNavy,
                gradient: [AppTheme.roadNavy, AppTheme.highwayTeal]
            )
        case "technik":
            return CategoryStyle(
                icon: "wrench.and.screwdriver.fill",
                color: Color(red: 0.45, green: 0.42, blue: 0.38),
                gradient: [Color(red: 0.55, green: 0.50, blue: 0.45), Color(red: 0.40, green: 0.38, blue: 0.35)]
            )
        case "car":
            return CategoryStyle(
                icon: "car.fill",
                color: AppTheme.highwayTeal,
                gradient: [AppTheme.highwayTeal, Color(red: 0.20, green: 0.55, blue: 0.60)]
            )
        case "lights":
            return CategoryStyle(
                icon: "lightbulb.max.fill",
                color: AppTheme.signalAmber,
                gradient: [AppTheme.signalAmber, Color(red: 0.95, green: 0.75, blue: 0.20)]
            )
        case "brakes":
            return CategoryStyle(
                icon: "brakesignal",
                color: AppTheme.signalRed,
                gradient: [AppTheme.signalRed, Color(red: 0.75, green: 0.22, blue: 0.22)]
            )
        case "fluids":
            return CategoryStyle(
                icon: "drop.fill",
                color: Color(red: 0.25, green: 0.55, blue: 0.85),
                gradient: [Color(red: 0.30, green: 0.60, blue: 0.90), Color(red: 0.20, green: 0.45, blue: 0.75)]
            )
        case "safety":
            return CategoryStyle(
                icon: "shield.checkered",
                color: AppTheme.signalGreen,
                gradient: [AppTheme.signalGreen, Color(red: 0.12, green: 0.58, blue: 0.38)]
            )
        case "assist":
            return CategoryStyle(
                icon: "cpu.fill",
                color: Color(red: 0.45, green: 0.35, blue: 0.75),
                gradient: [Color(red: 0.50, green: 0.40, blue: 0.80), Color(red: 0.35, green: 0.28, blue: 0.65)]
            )
        case "maneuvers":
            return CategoryStyle(
                icon: "arrow.triangle.turn.up.right.diamond.fill",
                color: Color(red: 0.85, green: 0.45, blue: 0.20),
                gradient: [Color(red: 0.90, green: 0.50, blue: 0.25), Color(red: 0.75, green: 0.38, blue: 0.18)]
            )
        case "grundaufgaben":
            return CategoryStyle(
                icon: "parkingsign.circle.fill",
                color: Color(red: 0.20, green: 0.48, blue: 0.72),
                gradient: [Color(red: 0.25, green: 0.52, blue: 0.78), Color(red: 0.15, green: 0.38, blue: 0.62)]
            )
        case "traffic":
            return CategoryStyle(
                icon: "signpost.right.fill",
                color: AppTheme.signalAmber,
                gradient: [AppTheme.signalAmber, Color(red: 0.88, green: 0.55, blue: 0.10)]
            )
        case "phrases":
            return CategoryStyle(
                icon: "person.wave.2.fill",
                color: Color(red: 0.55, green: 0.32, blue: 0.68),
                gradient: [Color(red: 0.60, green: 0.38, blue: 0.72), Color(red: 0.45, green: 0.25, blue: 0.58)]
            )
        case "documents":
            return CategoryStyle(
                icon: "doc.text.fill",
                color: Color(red: 0.35, green: 0.45, blue: 0.55),
                gradient: [Color(red: 0.40, green: 0.50, blue: 0.60), Color(red: 0.28, green: 0.38, blue: 0.48)]
            )
        case "emergency":
            return CategoryStyle(
                icon: "exclamationmark.triangle.fill",
                color: AppTheme.signalRed,
                gradient: [AppTheme.signalRed, Color(red: 0.70, green: 0.20, blue: 0.18)]
            )
        default:
            return CategoryStyle(
                icon: "folder.fill",
                color: AppTheme.highwayTeal,
                gradient: [AppTheme.highwayTeal, AppTheme.roadNavy]
            )
        }
    }
}
