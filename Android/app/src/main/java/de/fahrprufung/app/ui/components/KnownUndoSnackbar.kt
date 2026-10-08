package de.fahrprufung.app.ui.components

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.animation.slideInVertically
import androidx.compose.animation.slideOutVertically
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.layout.widthIn
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Icon
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import de.fahrprufung.app.R
import de.fahrprufung.app.theme.RoadNavy
import de.fahrprufung.app.theme.SignalAmber
import de.fahrprufung.app.theme.bodyStyle
import de.fahrprufung.app.theme.headlineStyle
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.VisibilityOff

/** Bottom snackbar offering to undo a "mark as known" action (mirrors iOS `KnownUndoToast`). */
@Composable
fun KnownUndoSnackbar(isVisible: Boolean, message: String, onUndo: () -> Unit) {
    AnimatedVisibility(
        visible = isVisible,
        enter = slideInVertically(initialOffsetY = { it }) + fadeIn(),
        exit = slideOutVertically(targetOffsetY = { it }) + fadeOut()
    ) {
        Row(
            modifier = Modifier
                .widthIn(max = 420.dp)
                .padding(horizontal = 20.dp)
                .clip(RoundedCornerShape(14.dp))
                .background(RoadNavy.copy(alpha = 0.92f))
                .padding(horizontal = 16.dp, vertical = 14.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Icon(
                imageVector = Icons.Filled.VisibilityOff,
                contentDescription = null,
                tint = Color.White.copy(alpha = 0.9f)
            )
            Spacer(modifier = Modifier.width(12.dp))
            Text(
                text = message,
                style = bodyStyle(14),
                color = Color.White,
                maxLines = 2,
                overflow = TextOverflow.Ellipsis,
                modifier = Modifier.weight(1f, fill = false)
            )
            Spacer(modifier = Modifier.width(8.dp))
            TextButton(onClick = onUndo) {
                Text(
                    text = stringResource(R.string.known_undoAction),
                    style = headlineStyle(14),
                    color = SignalAmber
                )
            }
        }
    }
}
