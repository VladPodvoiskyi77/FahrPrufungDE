package de.fahrprufung.app.ui.home

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
import androidx.compose.foundation.layout.statusBarsPadding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Bolt
import androidx.compose.material.icons.filled.DirectionsCarFilled
import androidx.compose.material.icons.filled.GridView
import androidx.compose.material.icons.filled.Psychology
import androidx.compose.material.icons.filled.RecordVoiceOver
import androidx.compose.material.icons.filled.Signpost
import androidx.compose.material.icons.filled.Star
import androidx.compose.material3.Icon
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.shadow
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.unit.dp
import de.fahrprufung.app.R
import de.fahrprufung.app.data.AnalyticsService
import de.fahrprufung.app.data.AppContainer
import de.fahrprufung.app.model.AppLanguage
import de.fahrprufung.app.navigation.Routes
import de.fahrprufung.app.theme.AppTheme
import de.fahrprufung.app.theme.CategoryStyle
import de.fahrprufung.app.theme.HighwayTeal
import de.fahrprufung.app.theme.RoadNavy
import de.fahrprufung.app.theme.SignalAmber
import de.fahrprufung.app.theme.SignalGreen
import de.fahrprufung.app.theme.bodyStyle
import de.fahrprufung.app.theme.captionStyle
import de.fahrprufung.app.theme.titleStyle
import de.fahrprufung.app.ui.components.ActionCard
import de.fahrprufung.app.ui.components.AppScreenBackground
import de.fahrprufung.app.ui.components.ProgressSummaryCard
import de.fahrprufung.app.ui.components.SectionHeader

@Composable
fun HomeScreen(
    container: AppContainer,
    onOpenCategories: () -> Unit,
    onOpenProgress: () -> Unit,
    onOpenExaminerPhrases: () -> Unit,
    onOpenSignsTab: () -> Unit,
    onOpenFlashcards: (String, String) -> Unit,
    onOpenQuiz: (String, String) -> Unit
) {
    val terms by container.content.terms.collectAsState()
    val categories by container.content.categories.collectAsState()
    val signs by container.content.signs.collectAsState()
    val nativeLanguage by container.nativeLanguage.collectAsState()
    val knownTermIds by container.knownTermIds.collectAsState()
    val knownSignIds by container.knownSignIds.collectAsState()

    val termCount = terms.size
    val knownTermCount = knownTermIds.size
    val knownSignCount = knownSignIds.size
    val signCount = signs.size
    val categoryCount = categories.size
    val overallPercent = if (termCount > 0) ((knownTermCount.toFloat() / termCount) * 100).toInt() else 0
    // Match iOS HomeViewModel: badges show remaining (not-yet-known) counts.
    val examinerCount = container.learningTerms(terms.filter { it.isExaminerPhrase }).size
    val coreCount = container.learningTerms(terms.filter { it.isCore }).size
    val streak = container.learningStats.studyStreak

    val topTermsTitle = stringResource(R.string.home_topTerms_title)
    val examinerTitle = stringResource(R.string.home_examinerPhrases_title)
    val quizTitle = stringResource(R.string.home_quiz_title)

    AppScreenBackground {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .statusBarsPadding()
                .verticalScroll(rememberScrollState())
                .padding(horizontal = 20.dp)
        ) {
            Spacer(modifier = Modifier.height(24.dp))

            HeroHeader(termCount = termCount, language = nativeLanguage)

            Spacer(modifier = Modifier.height(20.dp))

            ProgressSummaryCard(
                knownTerms = knownTermCount,
                totalTerms = termCount,
                knownSigns = knownSignCount,
                totalSigns = signCount,
                streak = streak,
                termPercent = overallPercent,
                onClick = {
                    AnalyticsService.logHomeAction("progress")
                    onOpenProgress()
                }
            )

            SectionHeader(title = stringResource(R.string.home_quickStart), icon = Icons.Filled.Bolt)

            Column(verticalArrangement = androidx.compose.foundation.layout.Arrangement.spacedBy(12.dp)) {
                ActionCard(
                    title = topTermsTitle,
                    subtitle = stringResource(R.string.home_topTerms_subtitle),
                    icon = Icons.Filled.Star,
                    colors = listOf(SignalAmber, de.fahrprufung.app.theme.AccentEnd),
                    badge = coreCount.toString(),
                    onClick = {
                        AnalyticsService.logHomeAction("top_terms")
                        onOpenFlashcards(Routes.SourceKey.CORE, topTermsTitle)
                    }
                )
                ActionCard(
                    title = examinerTitle,
                    subtitle = stringResource(R.string.home_examinerPhrases_subtitle),
                    icon = Icons.Filled.RecordVoiceOver,
                    colors = CategoryStyle.style("phrases").gradient,
                    badge = examinerCount.toString(),
                    onClick = {
                        AnalyticsService.logHomeAction("examiner_phrases")
                        onOpenExaminerPhrases()
                    }
                )
                ActionCard(
                    title = quizTitle,
                    subtitle = stringResource(R.string.home_quiz_subtitle),
                    icon = Icons.Filled.Psychology,
                    colors = listOf(HighwayTeal, RoadNavy),
                    onClick = {
                        AnalyticsService.logHomeAction("quiz")
                        onOpenQuiz(Routes.SourceKey.ALL, quizTitle)
                    }
                )
            }

            SectionHeader(title = stringResource(R.string.home_learnSection), icon = Icons.Filled.GridView)

            ActionCard(
                title = stringResource(R.string.home_allCategories_title),
                subtitle = stringResource(R.string.home_allCategories_subtitle),
                icon = Icons.Filled.GridView,
                colors = listOf(RoadNavy, HighwayTeal),
                badge = categoryCount.toString(),
                onClick = {
                    AnalyticsService.logHomeAction("categories")
                    onOpenCategories()
                }
            )

            SectionHeader(title = stringResource(R.string.home_signsSection), icon = Icons.Filled.Signpost)

            ActionCard(
                title = stringResource(R.string.signs_title),
                subtitle = stringResource(R.string.home_signs_subtitle, signCount),
                icon = Icons.Filled.Signpost,
                colors = listOf(SignalGreen, HighwayTeal),
                badge = signCount.toString(),
                onClick = {
                    AnalyticsService.logHomeAction("signs_tab")
                    onOpenSignsTab()
                }
            )

            Spacer(modifier = Modifier.height(120.dp))
        }
    }
}

@Composable
private fun HeroHeader(termCount: Int, language: AppLanguage) {
    Box(
        modifier = Modifier
            .fillMaxWidth()
            .height(200.dp)
            .shadow(
                elevation = 16.dp,
                shape = RoundedCornerShape(28.dp),
                ambientColor = RoadNavy.copy(alpha = 0.18f),
                spotColor = RoadNavy.copy(alpha = 0.25f)
            )
            .clip(RoundedCornerShape(28.dp))
            .background(AppTheme.heroGradient)
    ) {
        // Soft decorative circles
        Box(
            modifier = Modifier
                .align(Alignment.TopEnd)
                .padding(top = 8.dp, end = 4.dp)
                .size(120.dp)
                .clip(CircleShape)
                .background(Color.White.copy(alpha = 0.08f))
        )
        Icon(
            imageVector = Icons.Filled.DirectionsCarFilled,
            contentDescription = null,
            tint = Color.White.copy(alpha = 0.15f),
            modifier = Modifier
                .align(Alignment.TopEnd)
                .padding(top = 24.dp, end = 12.dp)
                .height(90.dp)
        )

        Column(
            modifier = Modifier
                .align(Alignment.BottomStart)
                .padding(24.dp)
        ) {
            Row(
                modifier = Modifier
                    .clip(CircleShape)
                    .background(Color.White.copy(alpha = 0.15f))
                    .padding(horizontal = 10.dp, vertical = 5.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                GermanFlagBadge()
                Spacer(modifier = Modifier.width(6.dp))
                Text(
                    text = stringResource(R.string.home_badge),
                    style = captionStyle(12),
                    color = Color.White.copy(alpha = 0.85f)
                )
            }

            Spacer(modifier = Modifier.height(10.dp))

            Text(text = stringResource(R.string.home_title), style = titleStyle(32), color = Color.White)

            Spacer(modifier = Modifier.height(4.dp))

            Text(
                text = stringResource(R.string.home_subtitle),
                style = bodyStyle(15),
                color = Color.White.copy(alpha = 0.88f)
            )

            Spacer(modifier = Modifier.height(10.dp))

            Row {
                StatChip(value = termCount.toString(), label = stringResource(R.string.home_terms))
                Spacer(modifier = Modifier.width(10.dp))
                StatChip(value = language.flag, label = language.displayName)
            }
        }
    }
}

@Composable
private fun GermanFlagBadge() {
    Column(
        modifier = Modifier
            .width(18.dp)
            .height(12.dp)
            .clip(RoundedCornerShape(2.dp))
    ) {
        Box(modifier = Modifier.weight(1f).fillMaxWidth().background(Color.Black))
        Box(modifier = Modifier.weight(1f).fillMaxWidth().background(Color(0xFFDE1C26)))
        Box(modifier = Modifier.weight(1f).fillMaxWidth().background(Color(0xFFFFCC00)))
    }
}

@Composable
private fun StatChip(value: String, label: String) {
    Column(
        modifier = Modifier
            .clip(RoundedCornerShape(10.dp))
            .background(Color.White.copy(alpha = 0.12f))
            .padding(horizontal = 12.dp, vertical = 8.dp)
    ) {
        Text(text = value, style = de.fahrprufung.app.theme.headlineStyle(16), color = Color.White)
        Text(text = label, style = captionStyle(11), color = Color.White.copy(alpha = 0.75f))
    }
}
