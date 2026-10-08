package de.fahrprufung.app.ui.quiz

import androidx.activity.compose.BackHandler
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Cancel
import androidx.compose.material.icons.filled.CheckCircle
import androidx.compose.material.icons.filled.DirectionsCar
import androidx.compose.material.icons.filled.EmojiEvents
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Icon
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.shadow
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.lifecycle.viewmodel.initializer
import androidx.lifecycle.viewmodel.viewModelFactory
import de.fahrprufung.app.R
import de.fahrprufung.app.data.AnalyticsService
import de.fahrprufung.app.data.AppContainer
import de.fahrprufung.app.model.AppLanguage
import de.fahrprufung.app.model.VocabularyTerm
import de.fahrprufung.app.theme.CardWhite
import de.fahrprufung.app.theme.HighwayTeal
import de.fahrprufung.app.theme.RoadNavy
import de.fahrprufung.app.theme.SignalAmber
import de.fahrprufung.app.theme.SignalGreen
import de.fahrprufung.app.theme.SignalRed
import de.fahrprufung.app.theme.bodyStyle
import de.fahrprufung.app.theme.captionStyle
import de.fahrprufung.app.theme.headlineStyle
import de.fahrprufung.app.theme.titleStyle
import de.fahrprufung.app.ui.components.AppCard
import de.fahrprufung.app.ui.components.AppScreenBackground
import de.fahrprufung.app.ui.components.ScreenTopBar

@Composable
fun QuizScreen(
    container: AppContainer,
    sessionTitle: String,
    sourceTerms: List<VocabularyTerm>,
    onBack: () -> Unit
) {
    val viewModel: QuizViewModel = viewModel(
        factory = viewModelFactory {
            initializer { QuizViewModel(sourceTerms, container, sessionTitle) }
        }
    )
    val nativeLanguage by container.nativeLanguage.collectAsState()
    val questions by viewModel.questions.collectAsState()
    var showReview by remember { mutableStateOf(false) }

    LaunchedEffect(Unit) { viewModel.startIfNeeded() }
    LaunchedEffect(showReview) {
        if (showReview) {
            AnalyticsService.logQuizReviewOpened()
            AnalyticsService.logScreen("quiz_review")
        }
    }

    BackHandler(enabled = showReview) { showReview = false }

    Scaffold(
        containerColor = Color.Transparent,
        topBar = { ScreenTopBar(title = sessionTitle, onBack = onBack) }
    ) { padding ->
        AppScreenBackground {
            Box(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(top = padding.calculateTopPadding())
            ) {
                when {
                    questions.isEmpty() && viewModel.isAllKnown -> {
                        Box(modifier = Modifier.fillMaxSize().padding(32.dp), contentAlignment = Alignment.Center) {
                            Text(
                                text = stringResource(R.string.known_allKnownQuiz),
                                style = bodyStyle(16),
                                color = RoadNavy,
                                textAlign = TextAlign.Center
                            )
                        }
                    }
                    questions.isEmpty() -> {
                        Box(modifier = Modifier.fillMaxSize().padding(32.dp), contentAlignment = Alignment.Center) {
                            Text(
                                text = stringResource(R.string.quiz_tooFew),
                                style = bodyStyle(16),
                                color = RoadNavy,
                                textAlign = TextAlign.Center
                            )
                        }
                    }
                    else -> {
                        val isFinished by viewModel.isFinished.collectAsState()
                        when {
                            showReview -> QuizReviewView(viewModel = viewModel, language = nativeLanguage)
                            isFinished -> QuizResultView(
                                viewModel = viewModel,
                                language = nativeLanguage,
                                onReview = { showReview = true },
                                onRetry = {
                                    showReview = false
                                    viewModel.start()
                                }
                            )
                            else -> QuizQuestionView(viewModel = viewModel, language = nativeLanguage)
                        }
                    }
                }
            }
        }
    }
}

@Composable
private fun QuizQuestionView(viewModel: QuizViewModel, language: AppLanguage) {
    val index by viewModel.currentIndex.collectAsState()
    val selected by viewModel.selected.collectAsState()
    val questions by viewModel.questions.collectAsState()
    val question = questions.getOrNull(index) ?: return
    val total = questions.size
    val letters = listOf("A", "B", "C", "D")

    Column(
        modifier = Modifier
            .fillMaxSize()
            .verticalScroll(rememberScrollState())
            .padding(horizontal = 20.dp)
    ) {
        Spacer(modifier = Modifier.height(8.dp))

        Row(
            modifier = Modifier.fillMaxWidth(),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Text(
                text = stringResource(R.string.quiz_question, index + 1, total),
                style = captionStyle(),
                color = Color.Gray,
                modifier = Modifier.weight(1f)
            )
            Icon(
                imageVector = Icons.Filled.DirectionsCar,
                contentDescription = null,
                tint = SignalAmber,
                modifier = Modifier.size(22.dp)
            )
        }

        Spacer(modifier = Modifier.height(8.dp))

        Box(
            modifier = Modifier
                .fillMaxWidth()
                .height(6.dp)
                .clip(CircleShape)
                .background(RoadNavy.copy(alpha = 0.08f))
        ) {
            Box(
                modifier = Modifier
                    .fillMaxWidth(fraction = (index + 1f) / total.coerceAtLeast(1))
                    .height(6.dp)
                    .clip(CircleShape)
                    .background(androidx.compose.ui.graphics.Brush.horizontalGradient(
                        listOf(SignalAmber, de.fahrprufung.app.theme.AccentEnd)
                    ))
            )
        }

        Spacer(modifier = Modifier.height(24.dp))

        AppCard(modifier = Modifier.fillMaxWidth(), accent = SignalAmber) {
            Column(modifier = Modifier.padding(20.dp)) {
                Text(text = stringResource(R.string.quiz_whatMeans), style = captionStyle(), color = Color.Gray)
                Spacer(modifier = Modifier.height(8.dp))
                Text(text = question.term.displayDe, style = titleStyle(26), color = RoadNavy)
            }
        }

        Spacer(modifier = Modifier.height(20.dp))

        question.choices.forEachIndexed { choiceIndex, choice ->
            Spacer(modifier = Modifier.height(10.dp))
            QuizChoiceRow(
                letter = letters.getOrElse(choiceIndex) { "?" },
                text = choice.displayTranslation(language),
                isSelected = selected?.id == choice.id,
                isCorrect = choice.id == question.term.id,
                isRevealed = selected != null,
                onClick = { viewModel.selectAnswer(choice) }
            )
        }

        Spacer(modifier = Modifier.height(20.dp))

        if (selected != null) {
            Button(
                onClick = { viewModel.goToNext() },
                modifier = Modifier.fillMaxWidth().height(52.dp),
                colors = ButtonDefaults.buttonColors(containerColor = SignalAmber, contentColor = RoadNavy),
                shape = RoundedCornerShape(14.dp)
            ) {
                Text(
                    text = if (index + 1 >= total) stringResource(R.string.common_continue) else stringResource(R.string.common_next),
                    fontWeight = FontWeight.SemiBold
                )
            }
        }

        Spacer(modifier = Modifier.height(100.dp))
    }
}

@Composable
private fun QuizChoiceRow(
    letter: String,
    text: String,
    isSelected: Boolean,
    isCorrect: Boolean,
    isRevealed: Boolean,
    onClick: () -> Unit
) {
    val backgroundColor = when {
        isRevealed && isCorrect -> SignalGreen.copy(alpha = 0.12f)
        isRevealed && isSelected && !isCorrect -> SignalRed.copy(alpha = 0.10f)
        else -> CardWhite
    }
    val borderColor = when {
        isRevealed && isCorrect -> SignalGreen
        isRevealed && isSelected && !isCorrect -> SignalRed
        else -> Color.Transparent
    }
    val letterBg = when {
        !isRevealed -> HighwayTeal.copy(alpha = 0.12f)
        isCorrect -> SignalGreen
        isSelected -> SignalRed
        else -> HighwayTeal.copy(alpha = 0.12f)
    }
    val letterFg = when {
        !isRevealed -> HighwayTeal
        isCorrect || (isSelected && !isCorrect) -> Color.White
        else -> HighwayTeal
    }

    Row(
        modifier = Modifier
            .fillMaxWidth()
            .shadow(
                elevation = 8.dp,
                shape = RoundedCornerShape(14.dp),
                ambientColor = Color.Black.copy(alpha = 0.06f),
                spotColor = Color.Black.copy(alpha = 0.08f)
            )
            .clip(RoundedCornerShape(14.dp))
            .background(backgroundColor)
            .border(width = if (borderColor == Color.Transparent) 0.dp else 2.dp, color = borderColor, shape = RoundedCornerShape(14.dp))
            .clickable(enabled = !isRevealed, onClick = onClick)
            .padding(16.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Box(
            modifier = Modifier
                .size(32.dp)
                .clip(CircleShape)
                .background(letterBg),
            contentAlignment = Alignment.Center
        ) {
            Text(text = letter, style = headlineStyle(14), color = letterFg)
        }
        Spacer(modifier = Modifier.size(14.dp))
        Text(text = text, style = bodyStyle(15), color = RoadNavy, modifier = Modifier.weight(1f))
        if (isRevealed && isCorrect) {
            Icon(imageVector = Icons.Filled.CheckCircle, contentDescription = null, tint = SignalGreen)
        } else if (isRevealed && isSelected && !isCorrect) {
            Icon(imageVector = Icons.Filled.Cancel, contentDescription = null, tint = SignalRed)
        }
    }
}

@Composable
private fun QuizResultView(
    viewModel: QuizViewModel,
    language: AppLanguage,
    onReview: () -> Unit,
    onRetry: () -> Unit
) {
    val score = viewModel.score
    val total = viewModel.total
    val ratio = if (total == 0) 0f else score.toFloat() / total

    Column(
        modifier = Modifier
            .fillMaxSize()
            .verticalScroll(rememberScrollState())
            .padding(24.dp),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Spacer(modifier = Modifier.height(24.dp))
        Icon(
            imageVector = Icons.Filled.EmojiEvents,
            contentDescription = null,
            tint = SignalAmber,
            modifier = Modifier.size(64.dp)
        )
        Spacer(modifier = Modifier.height(16.dp))
        Text(
            text = stringResource(R.string.progress_quizScore, score, total),
            style = titleStyle(32),
            color = RoadNavy
        )
        Spacer(modifier = Modifier.height(8.dp))
        Text(text = "${score} ${stringResource(R.string.quiz_correct)}", style = bodyStyle(16), color = Color.Gray)
        Spacer(modifier = Modifier.height(16.dp))
        Text(
            text = resultMessage(ratio),
            style = headlineStyle(18),
            color = RoadNavy,
            textAlign = TextAlign.Center
        )
        Spacer(modifier = Modifier.height(28.dp))
        Button(
            onClick = onReview,
            modifier = Modifier.fillMaxWidth().height(52.dp),
            colors = ButtonDefaults.buttonColors(containerColor = SignalAmber, contentColor = RoadNavy),
            shape = RoundedCornerShape(14.dp)
        ) {
            Text(text = stringResource(R.string.quiz_reviewAnswers), fontWeight = FontWeight.SemiBold)
        }
        Spacer(modifier = Modifier.height(12.dp))
        Button(
            onClick = onRetry,
            modifier = Modifier.fillMaxWidth().height(52.dp),
            colors = ButtonDefaults.buttonColors(containerColor = HighwayTeal, contentColor = Color.White),
            shape = RoundedCornerShape(14.dp)
        ) {
            Text(text = stringResource(R.string.common_retry), fontWeight = FontWeight.SemiBold)
        }
        Spacer(modifier = Modifier.height(100.dp))
    }
}

@Composable
private fun resultMessage(ratio: Float): String = when {
    ratio >= 0.95f -> stringResource(R.string.quiz_result_perfect)
    ratio >= 0.75f -> stringResource(R.string.quiz_result_great)
    ratio >= 0.5f -> stringResource(R.string.quiz_result_good)
    else -> stringResource(R.string.quiz_result_keepGoing)
}

@Composable
private fun QuizReviewView(viewModel: QuizViewModel, language: AppLanguage) {
    val answers by viewModel.answers.collectAsState()

    Column(
        modifier = Modifier
            .fillMaxSize()
            .verticalScroll(rememberScrollState())
            .padding(horizontal = 20.dp)
    ) {
        Spacer(modifier = Modifier.height(16.dp))
        Text(text = stringResource(R.string.quiz_reviewTitle), style = titleStyle(22), color = RoadNavy)
        Spacer(modifier = Modifier.height(16.dp))

        answers.forEachIndexed { i, answer ->
            AppCard(
                modifier = Modifier.fillMaxWidth(),
                accent = if (answer.isCorrect) SignalGreen else SignalRed
            ) {
                Column(modifier = Modifier.padding(16.dp)) {
                    Text(
                        text = stringResource(R.string.quiz_reviewQuestion, i + 1),
                        style = captionStyle(),
                        color = Color.Gray
                    )
                    Spacer(modifier = Modifier.height(4.dp))
                    Text(text = answer.question.term.displayDe, style = headlineStyle(17), color = RoadNavy)
                    Spacer(modifier = Modifier.height(8.dp))
                    Text(
                        text = "${stringResource(R.string.quiz_yourAnswer)}: ${answer.selected?.displayTranslation(language) ?: "—"}",
                        style = bodyStyle(14),
                        color = if (answer.isCorrect) SignalGreen else SignalRed
                    )
                    if (!answer.isCorrect) {
                        Text(
                            text = "${stringResource(R.string.quiz_correctAnswer)}: ${answer.question.term.displayTranslation(language)}",
                            style = bodyStyle(14),
                            color = SignalGreen
                        )
                    }
                }
            }
            Spacer(modifier = Modifier.height(10.dp))
        }

        Spacer(modifier = Modifier.height(24.dp))
    }
}
