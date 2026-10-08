package de.fahrprufung.app.ui.components

import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.CornerRadius
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.platform.LocalDensity
import androidx.compose.ui.unit.dp
import de.fahrprufung.app.theme.AppTheme
import de.fahrprufung.app.theme.Asphalt
import de.fahrprufung.app.theme.SignalAmber

/** Cream gradient backdrop with a subtle "road" decoration, used on every screen. */
@Composable
fun AppScreenBackground(modifier: Modifier = Modifier, content: @Composable () -> Unit) {
    Box(
        modifier = modifier
            .fillMaxSize()
            .background(AppTheme.screenBackground)
    ) {
        RoadDecoration()
        content()
    }
}

@Composable
private fun RoadDecoration() {
    val density = LocalDensity.current
    val stripHeightPx = with(density) { 56.dp.toPx() }
    val bottomInsetPx = with(density) { 34.dp.toPx() }
    val horizontalPaddingPx = with(density) { 32.dp.toPx() }
    val dashWidthPx = with(density) { 18.dp.toPx() }
    val dashGapPx = with(density) { 14.dp.toPx() }
    val dashHeightPx = with(density) { 3.dp.toPx() }
    val cornerPx = with(density) { 24.dp.toPx() }

    Canvas(modifier = Modifier.fillMaxSize()) {
        val stripTop = size.height - bottomInsetPx - stripHeightPx
        drawRoundRect(
            brush = Brush.verticalGradient(
                colors = listOf(Asphalt.copy(alpha = 0.04f), Asphalt.copy(alpha = 0.08f))
            ),
            topLeft = Offset(horizontalPaddingPx, stripTop),
            size = Size((size.width - horizontalPaddingPx * 2).coerceAtLeast(0f), stripHeightPx),
            cornerRadius = CornerRadius(cornerPx, cornerPx)
        )

        val dashY = size.height - bottomInsetPx - stripHeightPx / 2f
        var x = horizontalPaddingPx + 8f
        while (x < size.width - horizontalPaddingPx) {
            drawRoundRect(
                color = SignalAmber.copy(alpha = 0.35f),
                topLeft = Offset(x, dashY - dashHeightPx / 2f),
                size = Size(dashWidthPx, dashHeightPx),
                cornerRadius = CornerRadius(dashHeightPx / 2f, dashHeightPx / 2f)
            )
            x += dashWidthPx + dashGapPx
        }
    }
}
