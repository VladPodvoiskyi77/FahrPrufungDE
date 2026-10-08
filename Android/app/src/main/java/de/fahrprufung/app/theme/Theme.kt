package de.fahrprufung.app.theme

import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Shapes
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp

val AppLightColorScheme = lightColorScheme(
    primary = SignalAmber,
    onPrimary = RoadNavy,
    secondary = HighwayTeal,
    onSecondary = Color.White,
    tertiary = SignalGreen,
    background = WarmCream,
    onBackground = RoadNavy,
    surface = CardWhite,
    onSurface = RoadNavy,
    surfaceVariant = ScreenBottom,
    error = SignalRed,
    onError = Color.White
)

val AppShapes = Shapes(
    extraSmall = RoundedCornerShape(8.dp),
    small = RoundedCornerShape(12.dp),
    medium = RoundedCornerShape(16.dp),
    large = RoundedCornerShape(20.dp),
    extraLarge = RoundedCornerShape(28.dp)
)

/** Static design tokens mirroring the iOS `AppTheme` enum. */
object AppTheme {
    const val cardRadius = 20
    const val chipRadius = 12

    val heroGradient: Brush
        get() = Brush.linearGradient(listOf(RoadNavy, HighwayTeal.copy(alpha = 0.92f)))

    val accentGradient: Brush
        get() = Brush.linearGradient(listOf(SignalAmber, AccentEnd))

    val screenBackground: Brush
        get() = Brush.verticalGradient(listOf(WarmCream, ScreenBottom))

    val cardShadow: Color = Color.Black.copy(alpha = 0.08f)
}

/** Light theme only — the app never follows the system dark mode. */
@Composable
fun FahrPrufungTheme(content: @Composable () -> Unit) {
    MaterialTheme(
        colorScheme = AppLightColorScheme,
        typography = AppTypography,
        shapes = AppShapes,
        content = content
    )
}
