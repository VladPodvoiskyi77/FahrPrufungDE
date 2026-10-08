package de.fahrprufung.app.ui.components

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.foundation.lazy.grid.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Check
import androidx.compose.material.icons.filled.Public
import androidx.compose.material3.Icon
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.unit.dp
import de.fahrprufung.app.R
import de.fahrprufung.app.model.AppLanguage
import de.fahrprufung.app.theme.HighwayTeal
import de.fahrprufung.app.theme.RoadNavy
import de.fahrprufung.app.theme.captionStyle
import de.fahrprufung.app.theme.headlineStyle

/** 2-column grid to pick the in-app translation language (mirrors iOS `LanguagePickerCard`). */
@Composable
fun LanguagePickerRow(
    selection: AppLanguage,
    onSelect: (AppLanguage) -> Unit,
    modifier: Modifier = Modifier
) {
    AppCard(modifier = modifier.fillMaxWidth(), accent = HighwayTeal) {
        androidx.compose.foundation.layout.Column(modifier = Modifier.padding(16.dp)) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Icon(imageVector = Icons.Filled.Public, contentDescription = null, tint = RoadNavy)
                Spacer(modifier = Modifier.width(8.dp))
                Text(text = stringResource(R.string.settings_language), style = headlineStyle(), color = RoadNavy)
            }
            Spacer(modifier = Modifier.width(12.dp))
            LazyVerticalGrid(
                columns = GridCells.Fixed(2),
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(top = 12.dp)
                    .height(((AppLanguage.entries.size / 2 + 1) * 52).dp),
                horizontalArrangement = Arrangement.spacedBy(10.dp),
                verticalArrangement = Arrangement.spacedBy(10.dp),
                userScrollEnabled = false
            ) {
                items(AppLanguage.entries.toList()) { language ->
                    LanguageOption(
                        language = language,
                        isSelected = language == selection,
                        onClick = { onSelect(language) }
                    )
                }
            }
        }
    }
}

@Composable
private fun LanguageOption(language: AppLanguage, isSelected: Boolean, onClick: () -> Unit) {
    val background = if (isSelected) RoadNavy else Color.White
    val contentColor = if (isSelected) Color.White else RoadNavy
    Row(
        modifier = Modifier
            .clip(RoundedCornerShape(12.dp))
            .background(background)
            .clickable(onClick = onClick)
            .padding(12.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Text(text = language.flag, style = headlineStyle(18))
        Spacer(modifier = Modifier.width(8.dp))
        Text(
            text = language.displayName,
            style = captionStyle(13),
            color = contentColor,
            modifier = Modifier.weight(1f)
        )
        if (isSelected) {
            Icon(
                imageVector = Icons.Filled.Check,
                contentDescription = null,
                tint = Color.White,
                modifier = Modifier.width(16.dp)
            )
        }
    }
}
