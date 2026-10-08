package de.fahrprufung.app.ui.components

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material3.Icon
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.unit.dp
import de.fahrprufung.app.theme.SignalAmber
import de.fahrprufung.app.theme.captionStyle

/** Small uppercase label with an optional icon and a trailing dashed line. */
@Composable
fun SectionHeader(title: String, icon: ImageVector? = null, modifier: Modifier = Modifier) {
    Row(
        modifier = modifier.padding(top = 8.dp, bottom = 4.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        if (icon != null) {
            Icon(imageVector = icon, contentDescription = null, tint = SignalAmber, modifier = Modifier.height(16.dp))
            Spacer(modifier = Modifier.width(8.dp))
        }
        Text(
            text = title.uppercase(),
            style = captionStyle(12),
            color = SignalAmber
        )
        Spacer(modifier = Modifier.width(8.dp))
        Box(modifier = Modifier.weight(1f)) {
            DashedLine(modifier = Modifier.fillMaxWidth())
        }
    }
}

@Composable
fun DashedLine(modifier: Modifier = Modifier, color: Color = SignalAmber) {
    androidx.compose.foundation.Canvas(modifier = modifier.height(4.dp)) {
        val dashWidth = 12.dp.toPx()
        val gap = 8.dp.toPx()
        var x = 0f
        while (x < size.width) {
            drawRoundRect(
                color = color.copy(alpha = 0.5f),
                topLeft = androidx.compose.ui.geometry.Offset(x, size.height / 2f - 1f),
                size = androidx.compose.ui.geometry.Size(dashWidth, 2f),
                cornerRadius = androidx.compose.ui.geometry.CornerRadius(1f, 1f)
            )
            x += dashWidth + gap
        }
    }
}
