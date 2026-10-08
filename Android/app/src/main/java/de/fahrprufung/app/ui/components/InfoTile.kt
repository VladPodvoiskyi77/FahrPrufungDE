package de.fahrprufung.app.ui.components

import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.material3.Icon
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.unit.dp
import de.fahrprufung.app.theme.RoadNavy
import de.fahrprufung.app.theme.captionStyle
import de.fahrprufung.app.theme.headlineStyle

/** Compact stats tile — mirrors iOS `InfoTile`. */
@Composable
fun InfoTile(
    value: String,
    label: String,
    icon: ImageVector,
    color: Color,
    modifier: Modifier = Modifier,
    wide: Boolean = false
) {
    AppCard(
        modifier = if (wide) modifier.fillMaxWidth() else modifier,
        accent = color
    ) {
        Row(
            modifier = Modifier.padding(14.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Icon(
                imageVector = icon,
                contentDescription = null,
                tint = color,
                modifier = Modifier.width(36.dp)
            )
            Spacer(modifier = Modifier.width(12.dp))
            Column(modifier = if (!wide) Modifier.weight(1f) else Modifier) {
                Text(text = value, style = headlineStyle(18), color = RoadNavy)
                Text(text = label, style = captionStyle(11), color = Color.Gray)
            }
        }
    }
}
