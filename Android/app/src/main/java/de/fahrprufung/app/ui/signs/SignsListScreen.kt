package de.fahrprufung.app.ui.signs

import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.statusBarsPadding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.BasicTextField
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ChevronRight
import androidx.compose.material.icons.filled.Close
import androidx.compose.material.icons.filled.Search
import androidx.compose.material.icons.filled.Signpost
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.alpha
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.shadow
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.SolidColor
import androidx.compose.ui.graphics.asImageBitmap
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import de.fahrprufung.app.R
import de.fahrprufung.app.data.AppContainer
import de.fahrprufung.app.model.AppLanguage
import de.fahrprufung.app.model.TrafficSign
import de.fahrprufung.app.theme.AppTheme
import de.fahrprufung.app.theme.CardWhite
import de.fahrprufung.app.theme.RoadNavy
import de.fahrprufung.app.theme.SignStyle
import de.fahrprufung.app.theme.SignalAmber
import de.fahrprufung.app.theme.bodyStyle
import de.fahrprufung.app.theme.captionStyle
import de.fahrprufung.app.theme.headlineStyle
import de.fahrprufung.app.theme.titleStyle
import de.fahrprufung.app.ui.components.AppCard
import de.fahrprufung.app.ui.components.AppScreenBackground
import de.fahrprufung.app.ui.components.FilterChip
import de.fahrprufung.app.ui.components.KnownMarkButton
import de.fahrprufung.app.ui.components.KnownMarkStyle
import de.fahrprufung.app.ui.components.SectionHeader

@Composable
fun SignsListScreen(
    container: AppContainer,
    onOpenSign: (TrafficSign) -> Unit
) {
    val allSigns by container.content.signs.collectAsState()
    val signCategories by container.content.signCategories.collectAsState()
    val nativeLanguage by container.nativeLanguage.collectAsState()
    val knownSignIds by container.knownSignIds.collectAsState()
    val undoMessage = stringResource(R.string.known_undoMessage)

    var query by remember { mutableStateOf("") }
    var selectedCategory by remember { mutableStateOf<String?>(null) }

    val filteredSigns = allSigns.filter { sign ->
        val matchesCategory = selectedCategory == null || sign.category == selectedCategory
        val matchesQuery = query.isBlank() ||
            sign.de.contains(query, ignoreCase = true) ||
            sign.translation(nativeLanguage).contains(query, ignoreCase = true) ||
            (sign.stvoCode?.contains(query, ignoreCase = true) == true)
        matchesCategory && matchesQuery
    }

    val heroSign = remember(allSigns) {
        allSigns.firstOrNull { it.stvoCode == "206" }
            ?: allSigns.firstOrNull { it.category == "prohibitory" }
            ?: allSigns.firstOrNull()
    }

    AppScreenBackground {
        LazyColumn(
            modifier = Modifier
                .fillMaxSize()
                .statusBarsPadding()
                .padding(horizontal = 20.dp),
            contentPadding = PaddingValues(bottom = 110.dp),
            verticalArrangement = Arrangement.spacedBy(0.dp)
        ) {
            item(key = "title") {
                Spacer(modifier = Modifier.height(24.dp))
                Text(
                    text = stringResource(R.string.signs_title),
                    style = titleStyle(28),
                    color = RoadNavy
                )
                Spacer(modifier = Modifier.height(16.dp))
            }

            if (heroSign != null) {
                item(key = "hero") {
                    AppCard(modifier = Modifier.fillMaxWidth(), accent = SignalAmber) {
                        Row(
                            modifier = Modifier.padding(16.dp),
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            SignThumbnail(sign = heroSign, size = 80.dp, bordered = true)
                            Spacer(modifier = Modifier.width(16.dp))
                            Column {
                                Text(
                                    text = stringResource(R.string.signs_count, allSigns.size),
                                    style = titleStyle(22),
                                    color = RoadNavy
                                )
                                Text(
                                    text = stringResource(R.string.signs_heroSubtitle),
                                    style = captionStyle(),
                                    color = Color.Gray
                                )
                            }
                        }
                    }
                    Spacer(modifier = Modifier.height(16.dp))
                }
            }

            item(key = "search") {
                SignsSearchField(
                    query = query,
                    onQueryChange = { query = it }
                )
                Spacer(modifier = Modifier.height(12.dp))
            }

            item(key = "filters") {
                Row(
                    modifier = Modifier.horizontalScroll(rememberScrollState()),
                    horizontalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    FilterChip(
                        title = stringResource(R.string.common_all),
                        isSelected = selectedCategory == null,
                        color = RoadNavy,
                        onClick = { selectedCategory = null }
                    )
                    signCategories.forEach { cat ->
                        FilterChip(
                            title = cat.title(nativeLanguage),
                            isSelected = selectedCategory == cat.id,
                            color = SignStyle.categoryColor(cat.id),
                            onClick = { selectedCategory = cat.id }
                        )
                    }
                }
                Spacer(modifier = Modifier.height(8.dp))
            }

            item(key = "section") {
                SectionHeader(
                    title = stringResource(R.string.signs_section, filteredSigns.size),
                    icon = Icons.Filled.Signpost
                )
            }

            if (filteredSigns.isEmpty()) {
                item(key = "empty") {
                    Column(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(top = 48.dp),
                        horizontalAlignment = Alignment.CenterHorizontally
                    ) {
                        Text(
                            text = stringResource(R.string.signs_empty_title),
                            style = headlineStyle(17),
                            color = RoadNavy
                        )
                        Spacer(modifier = Modifier.height(4.dp))
                        Text(
                            text = stringResource(R.string.signs_empty_subtitle),
                            style = bodyStyle(14),
                            color = Color.Gray,
                            textAlign = TextAlign.Center
                        )
                    }
                }
            } else {
                items(filteredSigns, key = { it.id }) { sign ->
                    val isKnown = sign.id in knownSignIds
                    Row(
                        modifier = Modifier.padding(bottom = 10.dp),
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.spacedBy(10.dp)
                    ) {
                        KnownMarkButton(
                            isKnown = isKnown,
                            style = KnownMarkStyle.COMPACT,
                            onClick = {
                                if (isKnown) {
                                    container.knownUndo.dismiss()
                                    container.setSignKnown(sign.id, false)
                                } else {
                                    container.markSignAsKnown(sign.id, undoMessage)
                                }
                            }
                        )
                        SignRow(
                            sign = sign,
                            language = nativeLanguage,
                            isKnown = isKnown,
                            onClick = { onOpenSign(sign) },
                            modifier = Modifier.weight(1f)
                        )
                    }
                }
            }
        }
    }
}

@Composable
private fun SignsSearchField(
    query: String,
    onQueryChange: (String) -> Unit
) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .shadow(
                elevation = 6.dp,
                shape = RoundedCornerShape(AppTheme.chipRadius.dp),
                ambientColor = AppTheme.cardShadow,
                spotColor = AppTheme.cardShadow
            )
            .clip(RoundedCornerShape(AppTheme.chipRadius.dp))
            .background(CardWhite)
            .padding(horizontal = 14.dp, vertical = 14.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Icon(
            imageVector = Icons.Filled.Search,
            contentDescription = null,
            tint = Color.Gray,
            modifier = Modifier.size(20.dp)
        )
        Spacer(modifier = Modifier.width(10.dp))
        Box(modifier = Modifier.weight(1f)) {
            if (query.isEmpty()) {
                Text(
                    text = stringResource(R.string.signs_searchPlaceholder),
                    style = bodyStyle(15),
                    color = Color.Gray
                )
            }
            BasicTextField(
                value = query,
                onValueChange = onQueryChange,
                singleLine = true,
                textStyle = bodyStyle(15).copy(color = RoadNavy),
                cursorBrush = SolidColor(RoadNavy),
                modifier = Modifier.fillMaxWidth()
            )
        }
        if (query.isNotEmpty()) {
            IconButton(
                onClick = { onQueryChange("") },
                modifier = Modifier.size(28.dp)
            ) {
                Icon(
                    imageVector = Icons.Filled.Close,
                    contentDescription = null,
                    tint = Color.Gray,
                    modifier = Modifier.size(18.dp)
                )
            }
        }
    }
}

@Composable
private fun SignRow(
    sign: TrafficSign,
    language: AppLanguage,
    isKnown: Boolean,
    onClick: () -> Unit,
    modifier: Modifier = Modifier
) {
    val style = SignStyle.categoryColor(sign.category)

    AppCard(
        modifier = modifier
            .fillMaxWidth()
            .alpha(if (isKnown) 0.42f else 1f)
            .clickable(onClick = onClick),
        accent = style
    ) {
        Row(
            modifier = Modifier.padding(14.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            SignThumbnail(sign = sign, size = 72.dp, bordered = true)
            Spacer(modifier = Modifier.width(16.dp))
            Column(modifier = Modifier.weight(1f)) {
                Text(
                    text = sign.translation(language),
                    style = headlineStyle(15),
                    color = RoadNavy,
                    maxLines = 2,
                    overflow = TextOverflow.Ellipsis
                )
                Text(
                    text = sign.displayDe,
                    style = captionStyle(12),
                    color = Color.Gray,
                    maxLines = 2,
                    overflow = TextOverflow.Ellipsis
                )
                if (!sign.stvoCode.isNullOrBlank() && sign.stvoCode != "—") {
                    Text(
                        text = "StVO ${sign.stvoCode}",
                        style = captionStyle(10),
                        color = style
                    )
                }
            }
            Icon(
                imageVector = Icons.Filled.ChevronRight,
                contentDescription = null,
                tint = style.copy(alpha = 0.5f),
                modifier = Modifier.size(16.dp)
            )
        }
    }
}

@Composable
fun SignThumbnail(
    sign: TrafficSign,
    size: androidx.compose.ui.unit.Dp = 48.dp,
    bordered: Boolean = false
) {
    val context = LocalContext.current
    val tint = SignStyle.categoryColor(sign.category)
    val bitmap = remember(sign.image) {
        sign.image?.let { imageName ->
            runCatching {
                context.assets.open("Signs/$imageName").use { stream ->
                    android.graphics.BitmapFactory.decodeStream(stream)
                }
            }.getOrNull()
        }
    }

    Box(
        modifier = Modifier
            .size(size)
            .clip(RoundedCornerShape(12.dp))
            .background(Color.White)
            .then(
                if (bordered) {
                    Modifier.border(1.dp, RoadNavy.copy(alpha = 0.08f), RoundedCornerShape(12.dp))
                } else {
                    Modifier
                }
            ),
        contentAlignment = Alignment.Center
    ) {
        if (bitmap != null) {
            Image(
                bitmap = bitmap.asImageBitmap(),
                contentDescription = null,
                contentScale = ContentScale.Fit,
                modifier = Modifier.size(size * 0.82f)
            )
        } else {
            Icon(
                imageVector = SignStyle.categoryIcon(sign.category),
                contentDescription = null,
                tint = tint
            )
        }
    }
}
