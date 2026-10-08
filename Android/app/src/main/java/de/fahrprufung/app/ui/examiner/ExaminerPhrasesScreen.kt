package de.fahrprufung.app.ui.examiner

import androidx.compose.foundation.background
import androidx.compose.foundation.horizontalScroll
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
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.List
import androidx.compose.material.icons.filled.QuestionMark
import androidx.compose.material.icons.filled.RecordVoiceOver
import androidx.compose.material.icons.filled.ViewCarousel
import androidx.compose.material.icons.filled.VolumeUp
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.Scaffold
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
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.unit.dp
import de.fahrprufung.app.R
import de.fahrprufung.app.data.AppContainer
import de.fahrprufung.app.model.ExaminerPhraseGroup
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
import de.fahrprufung.app.ui.components.FilterChip
import de.fahrprufung.app.ui.components.KnownMarkButton
import de.fahrprufung.app.ui.components.KnownMarkStyle
import de.fahrprufung.app.ui.components.ModeChip
import de.fahrprufung.app.ui.components.ScreenTopBar
import de.fahrprufung.app.ui.components.SectionHeader

@Composable
fun ExaminerPhrasesScreen(
    container: AppContainer,
    onOpenFlashcards: (String, String) -> Unit,
    onOpenQuiz: (String, String) -> Unit,
    onBack: () -> Unit
) {
    val allTerms by container.content.terms.collectAsState()
    val nativeLanguage by container.nativeLanguage.collectAsState()
    val knownTermIds by container.knownTermIds.collectAsState()
    val speakingId by container.speech.speakingId.collectAsState()

    var selectedGroup by remember { mutableStateOf<ExaminerPhraseGroup?>(null) }

    val examinerTerms = allTerms.filter { it.isExaminerPhrase }
    val filteredTerms = selectedGroup?.let { group -> examinerTerms.filter { it.examinerGroup == group } }
        ?: examinerTerms
    val learningTerms = filteredTerms.filter { it.id !in knownTermIds }
    val knownCount = examinerTerms.count { it.id in knownTermIds }
    val style = CategoryStyle.style("phrases")
    val title = stringResource(R.string.home_examinerPhrases_title)
    val undoMessage = stringResource(R.string.known_undoMessage)

    val sourceKey = selectedGroup?.let { Routes.SourceKey.examinerGroup(it.tag) } ?: Routes.SourceKey.EXAMINER

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

                AppCard(modifier = Modifier.fillMaxWidth(), accent = style.color) {
                    Row(modifier = Modifier.padding(16.dp), verticalAlignment = Alignment.CenterVertically) {
                        Box(
                            modifier = Modifier
                                .size(56.dp)
                                .clip(RoundedCornerShape(16.dp))
                                .background(Brush.linearGradient(style.gradient)),
                            contentAlignment = Alignment.Center
                        ) {
                            Icon(imageVector = Icons.Filled.RecordVoiceOver, contentDescription = null, tint = Color.White)
                        }
                        Spacer(modifier = Modifier.width(14.dp))
                        Column {
                            Text(
                                text = stringResource(R.string.examinerPhrases_listTitle),
                                style = headlineStyle(20),
                                color = RoadNavy
                            )
                            Text(
                                text = stringResource(R.string.category_termCount, examinerTerms.size),
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

                Spacer(modifier = Modifier.height(16.dp))

                Row(horizontalArrangement = androidx.compose.foundation.layout.Arrangement.spacedBy(12.dp)) {
                    Box(modifier = Modifier.weight(1f)) {
                        ModeChip(
                            title = stringResource(R.string.examinerPhrases_listMode),
                            icon = Icons.Filled.List,
                            color = style.color
                        )
                    }
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

                Spacer(modifier = Modifier.height(12.dp))

                Row(
                    modifier = Modifier.horizontalScroll(rememberScrollState()),
                    horizontalArrangement = androidx.compose.foundation.layout.Arrangement.spacedBy(8.dp)
                ) {
                    FilterChip(
                        title = stringResource(R.string.common_all),
                        isSelected = selectedGroup == null,
                        color = style.color,
                        onClick = { selectedGroup = null }
                    )
                    ExaminerPhraseGroup.entries.forEach { group ->
                        val count = examinerTerms.count { it.examinerGroup == group }
                        if (count > 0) {
                            FilterChip(
                                title = "${groupTitle(group)} ($count)",
                                isSelected = selectedGroup == group,
                                color = style.color,
                                onClick = { selectedGroup = group }
                            )
                        }
                    }
                }

                Spacer(modifier = Modifier.height(8.dp))

                if (selectedGroup != null) {
                    SectionHeader(title = groupTitle(selectedGroup!!))
                    filteredTerms.forEach { term ->
                        ExaminerPhraseRow(
                            term = term,
                            language = nativeLanguage,
                            style = style,
                            isKnown = term.id in knownTermIds,
                            isSpeaking = speakingId == term.id,
                            onSpeak = { container.speech.speakGerman(term.displayDe, term.id) },
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
                } else {
                    ExaminerPhraseGroup.entries.forEach { group ->
                        val groupTerms = examinerTerms.filter { it.examinerGroup == group }
                        if (groupTerms.isNotEmpty()) {
                            SectionHeader(title = groupTitle(group))
                            groupTerms.forEach { term ->
                                ExaminerPhraseRow(
                                    term = term,
                                    language = nativeLanguage,
                                    style = style,
                                    isKnown = term.id in knownTermIds,
                                    isSpeaking = speakingId == term.id,
                                    onSpeak = { container.speech.speakGerman(term.displayDe, term.id) },
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
                        }
                    }
                }

                Spacer(modifier = Modifier.height(24.dp))
            }
        }
    }
}

@Composable
private fun groupTitle(group: ExaminerPhraseGroup): String = when (group) {
    ExaminerPhraseGroup.START -> stringResource(R.string.examinerPhrases_group_start)
    ExaminerPhraseGroup.DIRECTION -> stringResource(R.string.examinerPhrases_group_direction)
    ExaminerPhraseGroup.MANEUVER -> stringResource(R.string.examinerPhrases_group_maneuver)
    ExaminerPhraseGroup.SAFETY -> stringResource(R.string.examinerPhrases_group_safety)
    ExaminerPhraseGroup.HINT -> stringResource(R.string.examinerPhrases_group_hint)
    ExaminerPhraseGroup.RESULT -> stringResource(R.string.examinerPhrases_group_result)
}

@Composable
private fun ExaminerPhraseRow(
    term: VocabularyTerm,
    language: de.fahrprufung.app.model.AppLanguage,
    style: de.fahrprufung.app.theme.CategoryStyle,
    isKnown: Boolean,
    isSpeaking: Boolean,
    onSpeak: () -> Unit,
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
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Icon(
                        imageVector = Icons.Filled.RecordVoiceOver,
                        contentDescription = null,
                        tint = style.color,
                        modifier = Modifier.size(16.dp)
                    )
                    Spacer(modifier = Modifier.width(8.dp))
                    Text(
                        text = term.displayDe,
                        style = headlineStyle(16),
                        color = RoadNavy,
                        modifier = Modifier.weight(1f)
                    )
                    IconButton(onClick = onSpeak) {
                        Icon(
                            imageVector = Icons.Filled.VolumeUp,
                            contentDescription = stringResource(R.string.common_listen),
                            tint = if (isSpeaking) style.color else RoadNavy.copy(alpha = 0.45f)
                        )
                    }
                }
                Text(
                    text = term.displayTranslation(language),
                    style = bodyStyle(15),
                    color = Color.Gray,
                    modifier = Modifier.padding(start = 24.dp)
                )
            }
        }
    }
}
