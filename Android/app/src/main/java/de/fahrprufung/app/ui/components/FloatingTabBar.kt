package de.fahrprufung.app.ui.components

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.navigationBarsPadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.MenuBook
import androidx.compose.material.icons.automirrored.filled.TrendingUp
import androidx.compose.material.icons.filled.Settings
import androidx.compose.material.icons.filled.Signpost
import androidx.compose.material3.Icon
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.shadow
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.unit.dp
import de.fahrprufung.app.R
import de.fahrprufung.app.navigation.Routes
import de.fahrprufung.app.theme.CardWhite
import de.fahrprufung.app.theme.RoadNavy
import de.fahrprufung.app.theme.SignalAmber
import de.fahrprufung.app.theme.captionStyle

data class TabItem(
    val route: String,
    val labelRes: Int,
    val icon: ImageVector
)

val MainTabs = listOf(
    TabItem(Routes.HOME, R.string.tab_learn, Icons.AutoMirrored.Filled.MenuBook),
    TabItem(Routes.SIGNS_LIST, R.string.tab_signs, Icons.Filled.Signpost),
    TabItem(Routes.PROGRESS, R.string.tab_progress, Icons.AutoMirrored.Filled.TrendingUp),
    TabItem(Routes.SETTINGS, R.string.tab_settings, Icons.Filled.Settings)
)

/**
 * Floating pill-shaped tab bar matching the iOS screenshots —
 * rounded capsule, soft shadow, selected tab with amber tint + light pill.
 */
@Composable
fun FloatingTabBar(
    selectedRoute: String,
    onSelect: (String) -> Unit,
    modifier: Modifier = Modifier
) {
    Box(
        modifier = modifier
            .fillMaxWidth()
            .navigationBarsPadding()
            .padding(horizontal = 16.dp, vertical = 10.dp)
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .shadow(
                    elevation = 16.dp,
                    shape = RoundedCornerShape(28.dp),
                    ambientColor = Color.Black.copy(alpha = 0.08f),
                    spotColor = Color.Black.copy(alpha = 0.14f)
                )
                .clip(RoundedCornerShape(28.dp))
                .background(CardWhite)
                .padding(horizontal = 8.dp, vertical = 8.dp),
            horizontalArrangement = Arrangement.SpaceEvenly,
            verticalAlignment = Alignment.CenterVertically
        ) {
            MainTabs.forEach { tab ->
                val selected = tab.route == selectedRoute
                TabBarItem(
                    tab = tab,
                    selected = selected,
                    onClick = { onSelect(tab.route) },
                    modifier = Modifier.weight(1f)
                )
            }
        }
    }
}

@Composable
private fun TabBarItem(
    tab: TabItem,
    selected: Boolean,
    onClick: () -> Unit,
    modifier: Modifier = Modifier
) {
    val tint = if (selected) SignalAmber else RoadNavy.copy(alpha = 0.55f)
    Column(
        modifier = modifier
            .clip(RoundedCornerShape(18.dp))
            .clickable(onClick = onClick)
            .then(
                if (selected) {
                    Modifier.background(RoadNavy.copy(alpha = 0.06f), RoundedCornerShape(18.dp))
                } else {
                    Modifier
                }
            )
            .padding(vertical = 8.dp),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Icon(
            imageVector = tab.icon,
            contentDescription = null,
            tint = tint,
            modifier = Modifier.size(22.dp)
        )
        Spacer(modifier = Modifier.height(4.dp))
        Text(
            text = stringResource(tab.labelRes),
            style = captionStyle(11),
            color = tint
        )
    }
}
