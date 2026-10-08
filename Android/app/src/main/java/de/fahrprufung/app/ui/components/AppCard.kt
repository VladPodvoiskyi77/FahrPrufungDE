package de.fahrprufung.app.ui.components

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.shadow
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import de.fahrprufung.app.theme.AppTheme
import de.fahrprufung.app.theme.CardWhite
import de.fahrprufung.app.theme.HighwayTeal

/**
 * White rounded card with soft shadow and a colored accent bar on the leading edge —
 * mirrors the iOS `appCard` modifier from the screenshots.
 */
@Composable
fun AppCard(
    modifier: Modifier = Modifier,
    accent: Color = HighwayTeal,
    content: @Composable () -> Unit
) {
    Box(
        modifier = modifier
            .shadow(
                elevation = 10.dp,
                shape = RoundedCornerShape(AppTheme.cardRadius.dp),
                ambientColor = AppTheme.cardShadow,
                spotColor = AppTheme.cardShadow
            )
            .clip(RoundedCornerShape(AppTheme.cardRadius.dp))
            .background(CardWhite)
    ) {
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .padding(start = 8.dp)
        ) {
            content()
        }
        Box(
            modifier = Modifier
                .align(Alignment.CenterStart)
                .padding(start = 4.dp, top = 12.dp, bottom = 12.dp)
                .width(4.dp)
                .fillMaxHeight()
                .clip(RoundedCornerShape(4.dp))
                .background(accent)
        )
    }
}
