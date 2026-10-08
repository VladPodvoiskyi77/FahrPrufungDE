package de.fahrprufung.app.ui.components

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import de.fahrprufung.app.theme.RoadNavy
import de.fahrprufung.app.theme.captionStyle

/** A single pill-shaped filter chip, used for sign/examiner category filters. */
@Composable
fun FilterChip(
    title: String,
    isSelected: Boolean,
    color: Color,
    onClick: () -> Unit
) {
    val background = if (isSelected) color else Color.White
    val border = if (isSelected) Color.Transparent else color.copy(alpha = 0.3f)
    val textColor = if (isSelected) Color.White else RoadNavy

    androidx.compose.material3.Surface(
        modifier = Modifier.clip(CircleShape),
        color = background,
        contentColor = textColor,
        shape = CircleShape
    ) {
        Text(
            text = title,
            style = captionStyle(12),
            color = textColor,
            modifier = Modifier
                .border(width = 1.dp, color = border, shape = CircleShape)
                .clickable(onClick = onClick)
                .padding(horizontal = 14.dp, vertical = 8.dp)
        )
    }
}
