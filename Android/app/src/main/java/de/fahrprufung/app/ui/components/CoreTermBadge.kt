package de.fahrprufung.app.ui.components

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.layout.widthIn
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Star
import androidx.compose.material3.DropdownMenu
import androidx.compose.material3.Icon
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.unit.dp
import de.fahrprufung.app.R
import de.fahrprufung.app.theme.CardWhite
import de.fahrprufung.app.theme.RoadNavy
import de.fahrprufung.app.theme.SignalAmber
import de.fahrprufung.app.theme.bodyStyle
import de.fahrprufung.app.theme.headlineStyle

/** Star badge marking "core" exam vocabulary; taps reveal a short explanation. */
@Composable
fun CoreTermBadge(modifier: Modifier = Modifier) {
    var showHint by remember { mutableStateOf(false) }
    // Resolve outside DropdownMenu: Popup often uses the system Activity locale
    // (e.g. German phone) instead of ProvideAppLocale / in-app language.
    val title = stringResource(R.string.coreTerm_hintTitle)
    val message = stringResource(R.string.coreTerm_hintMessage)

    Box {
        Box(
            modifier = modifier
                .size(28.dp)
                .clickable { showHint = true },
            contentAlignment = Alignment.Center
        ) {
            Icon(
                imageVector = Icons.Filled.Star,
                contentDescription = title,
                tint = SignalAmber
            )
        }

        DropdownMenu(expanded = showHint, onDismissRequest = { showHint = false }) {
            Column(
                modifier = Modifier
                    .widthIn(max = 260.dp)
                    .background(CardWhite)
                    .padding(16.dp)
            ) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Icon(
                        imageVector = Icons.Filled.Star,
                        contentDescription = null,
                        tint = SignalAmber
                    )
                    Spacer(modifier = Modifier.width(8.dp))
                    Text(
                        text = title,
                        style = headlineStyle(15),
                        color = RoadNavy
                    )
                }
                Spacer(modifier = Modifier.height(8.dp))
                Text(
                    text = message,
                    style = bodyStyle(14),
                    color = androidx.compose.ui.graphics.Color.Gray
                )
            }
        }
    }
}
