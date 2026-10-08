package de.fahrprufung.app.ui.categories

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ChevronRight
import androidx.compose.material3.Icon
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.unit.dp
import de.fahrprufung.app.R
import de.fahrprufung.app.data.AppContainer
import de.fahrprufung.app.model.VocabularyCategory
import de.fahrprufung.app.theme.RoadNavy
import de.fahrprufung.app.theme.CategoryStyle
import de.fahrprufung.app.theme.captionStyle
import de.fahrprufung.app.theme.headlineStyle
import de.fahrprufung.app.ui.components.AppCard
import de.fahrprufung.app.ui.components.AppScreenBackground
import de.fahrprufung.app.ui.components.ScreenTopBar

@Composable
fun CategoryListScreen(
    container: AppContainer,
    onOpenCategory: (VocabularyCategory) -> Unit,
    onBack: () -> Unit = {}
) {
    val categories by container.content.categories.collectAsState()
    val terms by container.content.terms.collectAsState()
    val nativeLanguage by container.nativeLanguage.collectAsState()

    Scaffold(
        containerColor = Color.Transparent,
        topBar = {
            ScreenTopBar(
                title = stringResource(R.string.home_categoriesTitle),
                onBack = onBack
            )
        }
    ) { padding ->
        AppScreenBackground {
            LazyColumn(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(top = padding.calculateTopPadding())
                    .padding(horizontal = 20.dp),
                contentPadding = androidx.compose.foundation.layout.PaddingValues(vertical = 16.dp)
            ) {
                items(categories, key = { it.id }) { category ->
                    val termCount = terms.count { it.category == category.id }
                    CategoryCard(
                        category = category,
                        termCount = termCount,
                        language = nativeLanguage,
                        onClick = { onOpenCategory(category) }
                    )
                    Spacer(modifier = Modifier.size(12.dp))
                }
            }
        }
    }
}

@Composable
private fun CategoryCard(
    category: VocabularyCategory,
    termCount: Int,
    language: de.fahrprufung.app.model.AppLanguage,
    onClick: () -> Unit
) {
    val style = CategoryStyle.style(category.id)

    AppCard(
        modifier = Modifier
            .fillMaxWidth()
            .clickable(onClick = onClick),
        accent = style.color
    ) {
        Row(
            modifier = Modifier.padding(14.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Box(
                modifier = Modifier
                    .size(48.dp)
                    .clip(RoundedCornerShape(14.dp))
                    .background(Brush.linearGradient(style.gradient)),
                contentAlignment = Alignment.Center
            ) {
                Icon(imageVector = style.icon, contentDescription = null, tint = Color.White)
            }

            Spacer(modifier = Modifier.width(16.dp))

            Column(modifier = Modifier.weight(1f)) {
                Text(text = category.title(language), style = headlineStyle(), color = RoadNavy)
                Text(text = category.displayDe, style = captionStyle(), color = Color.Gray)
            }

            Box(
                modifier = Modifier
                    .clip(CircleShape)
                    .background(style.color.copy(alpha = 0.12f))
                    .padding(horizontal = 10.dp, vertical = 6.dp)
            ) {
                Text(text = termCount.toString(), style = headlineStyle(15), color = style.color)
            }

            Spacer(modifier = Modifier.width(8.dp))

            Icon(
                imageVector = Icons.Filled.ChevronRight,
                contentDescription = null,
                tint = style.color.copy(alpha = 0.6f)
            )
        }
    }
}
