package de.fahrprufung.app.theme

import androidx.compose.material3.Typography
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.Font
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.sp

// Rounded-ish look using the platform default rounded system font stand-in.
val AppFontFamily: FontFamily = FontFamily.SansSerif

fun titleStyle(size: Int = 28): TextStyle = TextStyle(
    fontFamily = AppFontFamily,
    fontWeight = FontWeight.Bold,
    fontSize = size.sp
)

fun headlineStyle(size: Int = 17): TextStyle = TextStyle(
    fontFamily = AppFontFamily,
    fontWeight = FontWeight.SemiBold,
    fontSize = size.sp
)

fun bodyStyle(size: Int = 16): TextStyle = TextStyle(
    fontFamily = AppFontFamily,
    fontWeight = FontWeight.Normal,
    fontSize = size.sp
)

fun captionStyle(size: Int = 13): TextStyle = TextStyle(
    fontFamily = AppFontFamily,
    fontWeight = FontWeight.Medium,
    fontSize = size.sp
)

val AppTypography = Typography(
    displaySmall = titleStyle(32),
    headlineLarge = titleStyle(28),
    headlineMedium = titleStyle(24),
    headlineSmall = headlineStyle(20),
    titleLarge = headlineStyle(18),
    titleMedium = headlineStyle(17),
    titleSmall = headlineStyle(15),
    bodyLarge = bodyStyle(16),
    bodyMedium = bodyStyle(15),
    bodySmall = bodyStyle(14),
    labelLarge = captionStyle(14),
    labelMedium = captionStyle(13),
    labelSmall = captionStyle(11)
)
