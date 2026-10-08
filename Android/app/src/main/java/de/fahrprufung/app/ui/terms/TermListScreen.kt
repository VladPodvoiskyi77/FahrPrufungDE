package de.fahrprufung.app.ui.terms

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.QuestionMark
import androidx.compose.material.icons.filled.ViewCarousel
import androidx.compose.material3.Icon
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.alpha
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.unit.dp
import de.fahrprufung.app.R
import de.fahrprufung.app.data.AppContainer
import de.fahrprufung.app.model.VocabularyTerm
import de.fahrprufung.app.navigation.Routes
import de.fahrprufung.app.theme.CategoryStyle
import de.fahrprufung.app.theme.RoadNavy
import de.fahrprufung.app.theme.SignalAmber
import de.fahrprufung.app.theme.SignalGreen
import de.fahrprufung.app.theme.bodyStyle
import de.fahrprufung.app.theme.captionStyle
import de.fahrprufung.app.theme.headlineStyle
import de.fahrprufung.app.ui.components.AppCard
import de.fahrprufung.app.ui.components.AppScreenBackground
import de.fahrprufung.app.ui.components.CoreTermBadge
import de.fahrprufung.app.ui.components.KnownMarkButton
import de.fahrprufung.app.ui.components.KnownMarkStyle
import de.fahrprufung.app.ui.components.ModeChip
import de.fahrprufung.app.ui.components.ScreenTopBar
import de.fahrprufung.app.ui.components.SectionHeader

@Composable
fun TermListScreen(
    container: AppContainer,
    categoryId: String,
    onOpenFlashcards: (String, String) -> Unit,
    onOpenQuiz: (String, String) -> Unit,
    onBack: () -> Unit
) {
    val allCategories by container.content.categories.collectAsState()
    val category = allCategories.firstOrNull { it.id == categoryId }
    val allTerms by container.content.terms.collectAsState()
    val nativeLanguage by container.nativeLanguage.collectAsState()
    val knownTermIds by container.knownTermIds.collectAsState()

    val terms = allTerms.filter { it.category == categoryId }
    val learningTerms = terms.filter { it.id !in knownTermIds }
    val knownCount = terms.count { it.id in knownTermIds }
    val style = CategoryStyle.style(categoryId)
    val title = category?.title(nativeLanguage) ?: categoryId
    val sourceKey = Routes.SourceKey.category(categoryId)
    val undoMessage = stringResource(R.string.known_undoMessage)

    Scaffold(
        containerColor = Color.Transparent,
        topBar = { ScreenTopBar(title = title, onBack = onBack) }
    ) { padding ->
        AppScreenBackground {
            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .verticalScroll(rememberScrollState())
                    .padding(top = padding.calculateTopPadding())
                    .padding(horizontal = 20.dp)
            ) {
                Spacer(modifier = Modifier.height(16.dp))

                CategoryHeaderCard(
                    displayDe = category?.displayDe ?: categoryId,
                    termCount = terms.size,
                    knownCount = knownCount,
                    style = style
                )

                Spacer(modifier = Modifier.height(16.dp))

                Row(
                    horizontalArrangement = androidx.compose.foundation.layout.Arrangement.spacedBy(12.dp)
                ) {
                    Box(modifier = Modifier.weight(1f)) {
                        ModeChip(
                            title = stringResource(R.string.category_cards),
                            icon = Icons.Filled.ViewCarousel,
                            color = style.color,
                            enabled = learningTerms.isNotEmpty(),
                            onClick = { onOpenFlashcards(sourceKey, title) }
                        )
                    }
                    Box(modifier = Modifier.weight(1f)) {
                        ModeChip(
                            title = stringResource(R.string.category_quiz),
                            icon = Icons.Filled.QuestionMark,
                            color = SignalAmber,
                            enabled = learningTerms.isNotEmpty(),
                            onClick = { onOpenQuiz(sourceKey, title) }
                        )
                    }
                }

                SectionHeader(title = stringResource(R.string.category_terms))

                terms.forEach { term ->
                    TermRowCard(
                        term = term,
                        language = nativeLanguage,
                        style = style,
                        isKnown = term.id in knownTermIds,
                        onToggleKnown = {
                            if (term.id in knownTermIds) {
                                container.knownUndo.dismiss()
                                container.setTermKnown(term.id, false)
                            } else {
                                container.markTermAsKnown(term.id, undoMessage)
                            }
                        }
                    )
                    Spacer(modifier = Modifier.height(10.dp))
                }

                Spacer(modifier = Modifier.height(24.dp))
            }
        }
    }
}

@Composable
private fun CategoryHeaderCard(
    displayDe: String,
    termCount: Int,
    knownCount: Int,
    style: de.fahrprufung.app.theme.CategoryStyle
) {
    AppCard(modifier = Modifier.fillMaxWidth(), accent = style.color) {
        Row(modifier = Modifier.padding(16.dp), verticalAlignment = Alignment.CenterVertically) {
            Box(
                modifier = Modifier
                    .size(56.dp)
                    .clip(RoundedCornerShape(16.dp))
                    .background(Brush.linearGradient(style.gradient)),
                contentAlignment = Alignment.Center
            ) {
                Icon(imageVector = style.icon, contentDescription = null, tint = Color.White)
            }
            Spacer(modifier = Modifier.width(14.dp))
            Column {
                Text(text = displayDe, style = headlineStyle(20), color = RoadNavy)
                Text(
                    text = stringResource(R.string.category_termCount, termCount),
                    style = captionStyle(),
                    color = Color.Gray
                )
                if (knownCount > 0) {
                    Text(
                        text = stringResource(R.string.known_listHiddenCount, knownCount),
                        style = captionStyle(11),
                        color = SignalGreen
                    )
                }
            }
        }
    }
}

@Composable
private fun TermRowCard(
    term: VocabularyTerm,
    language: de.fahrprufung.app.model.AppLanguage,
    style: de.fahrprufung.app.theme.CategoryStyle,
    isKnown: Boolean,
    onToggleKnown: () -> Unit
) {
    AppCard(
        modifier = Modifier.fillMaxWidth().alpha(if (isKnown) 0.42f else 1f),
        accent = style.color
    ) {
        Row(modifier = Modifier.padding(14.dp), verticalAlignment = Alignment.Top) {
            KnownMarkButton(isKnown = isKnown, style = KnownMarkStyle.COMPACT, onClick = onToggleKnown)
            Spacer(modifier = Modifier.width(8.dp))
            Column(modifier = Modifier.weight(1f)) {
                Row(verticalAlignment = Alignment.Top) {
                    Text(
                        text = term.displayDe,
                        style = headlineStyle(),
                        color = RoadNavy,
                        modifier = Modifier.weight(1f)
                    )
                    if (term.isCore) CoreTermBadge()
                }
                Text(
                    text = term.displayTranslation(language),
                    style = bodyStyle(15),
                    color = Color.Gray
                )
                val phrase = term.displayExamPhraseDe
                if (phrase != null) {
                    Spacer(modifier = Modifier.height(8.dp))
                    Box(
                        modifier = Modifier
                            .fillMaxWidth()
                            .clip(RoundedCornerShape(10.dp))
                            .background(style.color.copy(alpha = 0.08f))
                            .padding(10.dp)
                    ) {
                        Text(text = phrase, style = captionStyle(12), color = style.color)
                    }
                }
            }
        }
    }
}
