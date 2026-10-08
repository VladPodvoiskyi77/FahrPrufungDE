package de.fahrprufung.app.ui.components

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.statusBarsPadding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material3.Icon
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.shadow
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import de.fahrprufung.app.theme.CardWhite
import de.fahrprufung.app.theme.RoadNavy
import de.fahrprufung.app.theme.captionStyle
import de.fahrprufung.app.theme.headlineStyle

/**
 * Title bar with status-bar inset and optional circular back button (matches iOS nav chrome).
 */
@Composable
fun ScreenTopBar(
    title: String,
    subtitle: String? = null,
    onBack: (() -> Unit)? = null
) {
    Box(
        modifier = Modifier
            .fillMaxWidth()
            .statusBarsPadding()
            .padding(start = 16.dp, top = 16.dp, end = 16.dp, bottom = 8.dp)
    ) {
        if (onBack != null) {
            CircularIconButton(
                onClick = onBack,
                modifier = Modifier.align(Alignment.CenterStart)
            ) {
                Icon(
                    imageVector = Icons.AutoMirrored.Filled.ArrowBack,
                    contentDescription = null,
                    tint = RoadNavy,
                    modifier = Modifier.size(22.dp)
                )
            }
        }

        Column(
            modifier = Modifier
                .align(Alignment.Center)
                .padding(horizontal = if (onBack != null) 52.dp else 0.dp),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            if (title.isNotBlank()) {
                Text(
                    text = title,
                    style = headlineStyle(17),
                    color = RoadNavy,
                    textAlign = TextAlign.Center
                )
            }
            if (subtitle != null) {
                Spacer(modifier = Modifier.height(2.dp))
                Text(
                    text = subtitle,
                    style = captionStyle(12),
                    color = Color.Gray,
                    textAlign = TextAlign.Center
                )
            }
        }

        if (onBack != null) {
            Spacer(modifier = Modifier.width(44.dp).align(Alignment.CenterEnd))
        }
    }
}

/** Circular white button with soft shadow — used for flashcard prev/next/flip. */
@Composable
fun CircularIconButton(
    onClick: () -> Unit,
    enabled: Boolean = true,
    modifier: Modifier = Modifier,
    content: @Composable () -> Unit
) {
    Box(
        modifier = modifier
            .size(44.dp)
            .shadow(
                elevation = 8.dp,
                shape = CircleShape,
                ambientColor = Color.Black.copy(alpha = 0.08f),
                spotColor = Color.Black.copy(alpha = 0.12f)
            )
            .clip(CircleShape)
            .background(CardWhite)
            .clickable(enabled = enabled, onClick = onClick),
        contentAlignment = Alignment.Center
    ) {
        content()
    }
}
