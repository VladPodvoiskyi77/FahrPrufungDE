package de.fahrprufung.app.ui.components

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.CheckCircle
import androidx.compose.material.icons.outlined.Circle
import androidx.compose.material3.Icon
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.shadow
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.unit.dp
import de.fahrprufung.app.R
import de.fahrprufung.app.theme.CardWhite
import de.fahrprufung.app.theme.RoadNavy
import de.fahrprufung.app.theme.SignalGreen
import de.fahrprufung.app.theme.captionStyle
import de.fahrprufung.app.theme.headlineStyle

enum class KnownMarkStyle { PROMINENT, COMPACT }

/** Toggle used everywhere to mark a term/sign as already known (mirrors iOS `KnownMarkButton`). */
@Composable
fun KnownMarkButton(
    isKnown: Boolean,
    style: KnownMarkStyle = KnownMarkStyle.PROMINENT,
    modifier: Modifier = Modifier,
    onClick: () -> Unit
) {
    when (style) {
        KnownMarkStyle.COMPACT -> CompactKnownMarkButton(isKnown, modifier, onClick)
        KnownMarkStyle.PROMINENT -> ProminentKnownMarkButton(isKnown, modifier, onClick)
    }
}

@Composable
private fun CompactKnownMarkButton(isKnown: Boolean, modifier: Modifier, onClick: () -> Unit) {
    androidx.compose.foundation.layout.Box(
        modifier = modifier
            .size(36.dp)
            .clip(CircleShape)
            .clickable(onClick = onClick),
        contentAlignment = Alignment.Center
    ) {
        if (isKnown) {
            Icon(imageVector = Icons.Filled.CheckCircle, contentDescription = null, tint = SignalGreen)
        } else {
            Icon(
                imageVector = Icons.Outlined.Circle,
                contentDescription = null,
                tint = RoadNavy.copy(alpha = 0.25f)
            )
        }
    }
}

@Composable
private fun ProminentKnownMarkButton(isKnown: Boolean, modifier: Modifier, onClick: () -> Unit) {
    val markTitle = stringResource(if (isKnown) R.string.known_unmarkTitle else R.string.known_markTitle)
    androidx.compose.foundation.layout.Box(
        modifier = modifier
            .fillMaxWidth()
            .shadow(
                elevation = 8.dp,
                shape = RoundedCornerShape(16.dp),
                ambientColor = Color.Black.copy(alpha = 0.06f),
                spotColor = Color.Black.copy(alpha = 0.1f)
            )
            .clip(RoundedCornerShape(16.dp))
            .background(if (isKnown) SignalGreen.copy(alpha = 0.08f) else CardWhite)
            .clickable(onClick = onClick)
            .padding(14.dp)
    ) {
        Row(verticalAlignment = Alignment.CenterVertically) {
            Icon(
                imageVector = if (isKnown) Icons.Filled.CheckCircle else Icons.Outlined.Circle,
                contentDescription = null,
                tint = if (isKnown) SignalGreen else RoadNavy.copy(alpha = 0.35f),
                modifier = Modifier.size(28.dp)
            )
            Spacer(modifier = Modifier.width(12.dp))
            Column {
                Text(text = markTitle, style = headlineStyle(15), color = RoadNavy)
                if (!isKnown) {
                    Text(
                        text = stringResource(R.string.known_markSubtitle),
                        style = captionStyle(12),
                        color = Color.Gray
                    )
                }
            }
        }
    }
}
