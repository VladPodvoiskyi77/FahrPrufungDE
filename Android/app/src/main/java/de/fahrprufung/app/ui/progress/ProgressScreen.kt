package de.fahrprufung.app.ui.progress

import androidx.compose.foundation.Canvas
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
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.TrendingUp
import androidx.compose.material.icons.filled.EmojiEvents
import androidx.compose.material.icons.filled.Folder
import androidx.compose.material.icons.filled.LocalFireDepartment
import androidx.compose.material.icons.filled.QueryStats
import androidx.compose.material3.Icon
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import de.fahrprufung.app.R
import de.fahrprufung.app.data.AnalyticsService
import de.fahrprufung.app.data.AppContainer
import de.fahrprufung.app.model.QuizResultRecord
import de.fahrprufung.app.theme.CategoryStyle
import de.fahrprufung.app.theme.HighwayTeal
import de.fahrprufung.app.theme.RoadNavy
import de.fahrprufung.app.theme.SignalAmber
import de.fahrprufung.app.theme.SignalGreen
import de.fahrprufung.app.theme.bodyStyle
import de.fahrprufung.app.theme.captionStyle
import de.fahrprufung.app.theme.headlineStyle
import de.fahrprufung.app.theme.titleStyle
import de.fahrprufung.app.ui.components.AppCard
import de.fahrprufung.app.ui.components.AppScreenBackground
import de.fahrprufung.app.ui.components.SectionHeader
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale
import kotlin.math.min

@Composable
fun ProgressScreen(container: AppContainer) {
    val terms by container.content.terms.collectAsState()
    val categories by container.content.categories.collectAsState()
    val signs by container.content.signs.collectAsState()
    val knownTermIds by container.knownTermIds.collectAsState()
    val knownSignIds by container.knownSignIds.collectAsState()
    val statsData by container.learningStats.data.collectAsState()

    val termCount = terms.size
    val knownTermCount = knownTermIds.size
    val signCount = signs.size
    val knownSignCount = knownSignIds.size
    val termPercent = if (termCount > 0) ((knownTermCount.toFloat() / termCount) * 100).toInt() else 0
    val signPercent = if (signCount > 0) ((knownSignCount.toFloat() / signCount) * 100).toInt() else 0
    val streak = container.learningStats.studyStreak

    LaunchedEffect(Unit) { AnalyticsService.logProgressViewed() }

    AppScreenBackground {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .statusBarsPadding()
                .verticalScroll(rememberScrollState())
                .padding(horizontal = 20.dp)
        ) {
            Spacer(modifier = Modifier.height(24.dp))

            Text(text = stringResource(R.string.progress_title), style = titleStyle(28), color = RoadNavy)

            Spacer(modifier = Modifier.height(16.dp))

            SectionHeader(title = stringResource(R.string.progress_overall), icon = Icons.Filled.QueryStats)

            ProgressRingRow(
                title = stringResource(R.string.progress_terms),
                known = knownTermCount,
                total = termCount,
                percent = termPercent,
                color = HighwayTeal
            )
            Spacer(modifier = Modifier.height(10.dp))
            ProgressRingRow(
                title = stringResource(R.string.progress_signs),
                known = knownSignCount,
                total = signCount,
                percent = signPercent,
                color = SignalAmber
            )

            if (streak > 0) {
                Spacer(modifier = Modifier.height(14.dp))
                AppCard(modifier = Modifier.fillMaxWidth(), accent = SignalAmber) {
                    Row(
                        modifier = Modifier.padding(16.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Icon(
                            imageVector = Icons.Filled.LocalFireDepartment,
                            contentDescription = null,
                            tint = SignalAmber,
                            modifier = Modifier.size(28.dp)
                        )
                        Spacer(modifier = Modifier.width(14.dp))
                        Column {
                            Text(text = stringResource(R.string.progress_streak), style = captionStyle(), color = Color.Gray)
                            Text(
                                text = stringResource(R.string.progress_streakDays, streak),
                                style = headlineStyle(),
                                color = RoadNavy
                            )
                        }
                    }
                }
            }

            SectionHeader(title = stringResource(R.string.progress_byCategory), icon = Icons.Filled.Folder)

            categories.forEach { category ->
                val (known, total) = container.categoryProgress(category.id)
                if (total > 0) {
                    CategoryProgressRow(
                        title = category.title(container.nativeLanguage.value),
                        known = known,
                        total = total,
                        style = CategoryStyle.style(category.id)
                    )
                    Spacer(modifier = Modifier.height(10.dp))
                }
            }

            SectionHeader(title = stringResource(R.string.progress_recentQuizzes), icon = Icons.Filled.EmojiEvents)

            if (statsData.quizResults.isEmpty()) {
                AppCard(modifier = Modifier.fillMaxWidth(), accent = RoadNavy) {
                    Box(modifier = Modifier.fillMaxWidth().padding(16.dp), contentAlignment = Alignment.CenterStart) {
                        Text(
                            text = stringResource(R.string.progress_noQuizzesYet),
                            style = bodyStyle(15),
                            color = Color.Gray,
                            textAlign = TextAlign.Start
                        )
                    }
                }
            } else {
                statsData.quizResults.take(5).forEach { result ->
                    QuizResultRow(result = result)
                    Spacer(modifier = Modifier.height(10.dp))
                }
            }

            Spacer(modifier = Modifier.height(110.dp))
        }
    }
}

@Composable
private fun ProgressRingRow(
    title: String,
    known: Int,
    total: Int,
    percent: Int,
    color: Color
) {
    AppCard(modifier = Modifier.fillMaxWidth(), accent = color) {
        Row(
            modifier = Modifier.padding(14.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Box(modifier = Modifier.size(52.dp), contentAlignment = Alignment.Center) {
                Canvas(modifier = Modifier.fillMaxSize()) {
                    val stroke = 6.dp.toPx()
                    drawCircle(
                        color = color.copy(alpha = 0.15f),
                        style = Stroke(width = stroke)
                    )
                    drawArc(
                        color = color,
                        startAngle = -90f,
                        sweepAngle = 360f * (percent / 100f).coerceIn(0f, 1f),
                        useCenter = false,
                        style = Stroke(width = stroke, cap = StrokeCap.Round)
                    )
                }
                Text(text = "$percent%", style = captionStyle(12), color = RoadNavy)
            }
            Spacer(modifier = Modifier.width(16.dp))
            Column {
                Text(text = title, style = headlineStyle(), color = RoadNavy)
                Text(
                    text = stringResource(R.string.progress_learnedCount, known, total),
                    style = captionStyle(),
                    color = Color.Gray
                )
            }
        }
    }
}

@Composable
private fun CategoryProgressRow(title: String, known: Int, total: Int, style: CategoryStyle) {
    val percent = if (total > 0) known.toFloat() / total else 0f
    AppCard(modifier = Modifier.fillMaxWidth(), accent = style.color) {
        Column(modifier = Modifier.padding(14.dp)) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Text(text = title, style = bodyStyle(15), color = RoadNavy, modifier = Modifier.weight(1f))
                Text(
                    text = stringResource(R.string.progress_learnedCount, known, total),
                    style = captionStyle(),
                    color = Color.Gray
                )
            }
            Spacer(modifier = Modifier.height(8.dp))
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(8.dp)
                    .clip(CircleShape)
                    .background(style.color.copy(alpha = 0.12f))
            ) {
                Box(
                    modifier = Modifier
                        .fillMaxWidth(fraction = percent.coerceIn(0f, 1f))
                        .height(8.dp)
                        .clip(CircleShape)
                        .background(style.color)
                )
            }
        }
    }
}

@Composable
private fun QuizResultRow(result: QuizResultRecord) {
    val dateText = remember(result.dateMillis) {
        SimpleDateFormat("dd.MM.yyyy", Locale.getDefault()).format(Date(result.dateMillis))
    }
    val color = if (result.score == result.total) SignalGreen else HighwayTeal

    AppCard(modifier = Modifier.fillMaxWidth(), accent = HighwayTeal) {
        Row(
            modifier = Modifier
                .padding(14.dp)
                .fillMaxWidth(),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Column(modifier = Modifier.weight(1f)) {
                Text(
                    text = result.sessionTitle,
                    style = bodyStyle(15),
                    color = RoadNavy,
                    maxLines = 1
                )
                Text(text = dateText, style = captionStyle(11), color = Color.Gray)
            }
            Text(
                text = stringResource(R.string.progress_quizScore, result.score, result.total),
                style = headlineStyle(15),
                color = color
            )
        }
    }
}
