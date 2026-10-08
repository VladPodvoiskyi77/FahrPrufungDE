package de.fahrprufung.app.ui.components

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ChevronRight
import androidx.compose.material.icons.filled.LocalFireDepartment
import androidx.compose.material.icons.filled.QueryStats
import androidx.compose.material3.Icon
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.unit.dp
import de.fahrprufung.app.R
import de.fahrprufung.app.theme.HighwayTeal
import de.fahrprufung.app.theme.RoadNavy
import de.fahrprufung.app.theme.SignalAmber
import de.fahrprufung.app.theme.bodyStyle
import de.fahrprufung.app.theme.captionStyle
import de.fahrprufung.app.theme.headlineStyle
import de.fahrprufung.app.theme.titleStyle

@Composable
fun ProgressSummaryCard(
    knownTerms: Int,
    totalTerms: Int,
    knownSigns: Int,
    totalSigns: Int,
    streak: Int,
    termPercent: Int,
    onClick: () -> Unit
) {
    AppCard(
        modifier = Modifier
            .fillMaxWidth()
            .clickable(onClick = onClick),
        accent = HighwayTeal
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Box(
                    modifier = Modifier
                        .size(48.dp)
                        .clip(RoundedCornerShape(14.dp))
                        .background(Brush.linearGradient(listOf(HighwayTeal, RoadNavy))),
                    contentAlignment = Alignment.Center
                ) {
                    Icon(imageVector = Icons.Filled.QueryStats, contentDescription = null, tint = Color.White)
                }
                Spacer(modifier = Modifier.width(12.dp))
                Column(modifier = Modifier.weight(1f)) {
                    Text(text = stringResource(R.string.progress_title), style = headlineStyle(), color = RoadNavy)
                    Text(
                        text = stringResource(R.string.progress_homeTapHint),
                        style = captionStyle(11),
                        color = Color.Gray
                    )
                }
                Text(text = "$termPercent%", style = titleStyle(22), color = HighwayTeal)
                Spacer(modifier = Modifier.width(8.dp))
                Icon(imageVector = Icons.Filled.ChevronRight, contentDescription = null, tint = SignalAmber)
            }

            Spacer(modifier = Modifier.height(14.dp))

            Text(
                text = stringResource(R.string.progress_homeSummary, knownTerms, totalTerms),
                style = bodyStyle(14),
                color = RoadNavy.copy(alpha = 0.85f)
            )
            Text(
                text = stringResource(R.string.progress_homeSignsSummary, knownSigns, totalSigns),
                style = captionStyle(),
                color = Color.Gray
            )

            Spacer(modifier = Modifier.height(10.dp))

            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(8.dp)
                    .clip(CircleShape)
                    .background(HighwayTeal.copy(alpha = 0.12f))
            ) {
                Box(
                    modifier = Modifier
                        .fillMaxWidth(fraction = (termPercent / 100f).coerceIn(0f, 1f))
                        .height(8.dp)
                        .clip(CircleShape)
                        .background(HighwayTeal)
                )
            }

            if (streak > 0) {
                Spacer(modifier = Modifier.height(10.dp))
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Icon(
                        imageVector = Icons.Filled.LocalFireDepartment,
                        contentDescription = null,
                        tint = SignalAmber,
                        modifier = Modifier.size(16.dp)
                    )
                    Spacer(modifier = Modifier.width(6.dp))
                    Text(
                        text = stringResource(R.string.progress_streakDays, streak),
                        style = captionStyle(12),
                        color = SignalAmber
                    )
                }
            }
        }
    }
}
