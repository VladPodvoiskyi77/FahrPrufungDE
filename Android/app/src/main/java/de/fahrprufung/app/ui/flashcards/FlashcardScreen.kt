package de.fahrprufung.app.ui.flashcards

import androidx.compose.animation.AnimatedContent
import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.foundation.background
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
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ChevronLeft
import androidx.compose.material.icons.filled.ChevronRight
import androidx.compose.material.icons.filled.Loop
import androidx.compose.material.icons.filled.Person
import androidx.compose.material.icons.filled.Public
import androidx.compose.material.icons.filled.Style
import androidx.compose.material3.Icon
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.DisposableEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.shadow
import androidx.compose.ui.graphics.Color
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.lifecycle.viewmodel.initializer
import androidx.lifecycle.viewmodel.viewModelFactory
import de.fahrprufung.app.R
import de.fahrprufung.app.data.AppContainer
import de.fahrprufung.app.model.VocabularyTerm
import de.fahrprufung.app.theme.AppTheme
import de.fahrprufung.app.theme.CardWhite
import de.fahrprufung.app.theme.CategoryStyle
import de.fahrprufung.app.theme.RoadNavy
import de.fahrprufung.app.theme.SignalAmber
import de.fahrprufung.app.theme.bodyStyle
import de.fahrprufung.app.theme.captionStyle
import de.fahrprufung.app.theme.titleStyle
import de.fahrprufung.app.ui.components.AppScreenBackground
import de.fahrprufung.app.ui.components.CircularIconButton
import de.fahrprufung.app.ui.components.DashedLine
import de.fahrprufung.app.ui.components.KnownMarkButton
import de.fahrprufung.app.ui.components.ScreenTopBar

@Composable
fun FlashcardScreen(
    container: AppContainer,
    sessionTitle: String,
    rawTerms: List<VocabularyTerm>,
    onBack: () -> Unit
) {
    val learningTerms = remember(rawTerms) { container.learningTerms(rawTerms) }
    val viewModel: FlashcardViewModel = viewModel(
        factory = viewModelFactory {
            initializer { FlashcardViewModel(learningTerms, container, sessionTitle) }
        }
    )

    val nativeLanguage by container.nativeLanguage.collectAsState()
    val deck by viewModel.deck.collectAsState()
    val index by viewModel.index.collectAsState()
    val isFlipped by viewModel.isFlipped.collectAsState()
    val undoMessage = stringResource(R.string.known_undoMessage)

    DisposableEffect(Unit) {
        onDispose { viewModel.finishSessionIfNeeded() }
    }

    Scaffold(
        containerColor = Color.Transparent,
        topBar = {
            ScreenTopBar(
                title = sessionTitle,
                subtitle = if (deck.isNotEmpty()) {
                    stringResource(R.string.flashcards_counter, index + 1, deck.size)
                } else null,
                onBack = onBack
            )
        }
    ) { padding ->
        AppScreenBackground {
            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(top = padding.calculateTopPadding()),
                horizontalAlignment = Alignment.CenterHorizontally
            ) {
                val current = deck.getOrNull(index)

                if (current != null) {
                    Spacer(modifier = Modifier.height(16.dp))

                    AnimatedContent(
                        targetState = index,
                        label = "flashcard"
                    ) { _ ->
                        FlashcardSurface(
                            term = current,
                            language = nativeLanguage,
                            isFlipped = isFlipped,
                            progress = viewModel.progress,
                            onFlip = viewModel::flip,
                            modifier = Modifier.padding(horizontal = 20.dp)
                        )
                    }

                    Spacer(modifier = Modifier.height(24.dp))

                    Row(horizontalArrangement = androidx.compose.foundation.layout.Arrangement.spacedBy(40.dp)) {
                        CircularIconButton(
                            onClick = { viewModel.move(-1) },
                            enabled = viewModel.canGoBack,
                            modifier = Modifier.size(56.dp)
                        ) {
                            Icon(
                                imageVector = Icons.Filled.ChevronLeft,
                                contentDescription = null,
                                tint = if (viewModel.canGoBack) RoadNavy else Color.Gray.copy(alpha = 0.4f)
                            )
                        }
                        CircularIconButton(
                            onClick = { viewModel.resetFlip() },
                            modifier = Modifier.size(56.dp)
                        ) {
                            Icon(imageVector = Icons.Filled.Loop, contentDescription = null, tint = RoadNavy)
                        }
                        CircularIconButton(
                            onClick = { viewModel.move(1) },
                            enabled = viewModel.canGoForward,
                            modifier = Modifier.size(56.dp)
                        ) {
                            Icon(
                                imageVector = Icons.Filled.ChevronRight,
                                contentDescription = null,
                                tint = if (viewModel.canGoForward) RoadNavy else Color.Gray.copy(alpha = 0.4f)
                            )
                        }
                    }

                    Spacer(modifier = Modifier.height(20.dp))

                    KnownMarkButton(
                        isKnown = viewModel.isCurrentKnown(),
                        modifier = Modifier.padding(horizontal = 20.dp)
                    ) {
                        viewModel.toggleKnownForCurrent(undoMessage)
                    }
                } else if (deck.isEmpty() && learningTerms.isEmpty()) {
                    EmptyState(text = stringResource(R.string.known_allKnownFlashcards))
                } else {
                    EmptyState(text = stringResource(R.string.flashcards_empty))
                }

                Spacer(modifier = Modifier.height(110.dp))
            }
        }
    }
}

@Composable
private fun EmptyState(text: String) {
    Box(
        modifier = Modifier
            .fillMaxWidth()
            .padding(32.dp),
        contentAlignment = Alignment.Center
    ) {
        Text(text = text, style = bodyStyle(16), color = RoadNavy, textAlign = TextAlign.Center)
    }
}

@Composable
private fun FlashcardSurface(
    term: VocabularyTerm,
    language: de.fahrprufung.app.model.AppLanguage,
    isFlipped: Boolean,
    progress: Float,
    onFlip: () -> Unit,
    modifier: Modifier = Modifier
) {
    val animatedProgress by animateFloatAsState(targetValue = progress, label = "progress")

    Column(
        modifier = modifier
            .fillMaxWidth()
            .shadow(
                elevation = 14.dp,
                shape = RoundedCornerShape(28.dp),
                ambientColor = Color.Black.copy(alpha = 0.08f),
                spotColor = Color.Black.copy(alpha = 0.12f)
            )
            .clip(RoundedCornerShape(28.dp))
            .background(CardWhite)
            .clickable(onClick = onFlip)
            .padding(vertical = 24.dp)
    ) {
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 20.dp)
                .height(5.dp)
                .clip(CircleShape)
                .background(RoadNavy.copy(alpha = 0.08f))
        ) {
            Box(
                modifier = Modifier
                    .fillMaxWidth(fraction = animatedProgress.coerceIn(0f, 1f))
                    .height(5.dp)
                    .clip(CircleShape)
                    .background(AppTheme.accentGradient)
            )
        }

        Spacer(modifier = Modifier.height(28.dp))

        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 24.dp)
                .height(220.dp),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = androidx.compose.foundation.layout.Arrangement.Center
        ) {
            Icon(
                imageVector = if (isFlipped) Icons.Filled.Public else Icons.Filled.Style,
                contentDescription = null,
                tint = SignalAmber,
                modifier = Modifier.size(28.dp)
            )
            Spacer(modifier = Modifier.height(16.dp))

            if (isFlipped) {
                Text(
                    text = term.displayTranslation(language),
                    style = titleStyle(26),
                    color = RoadNavy,
                    textAlign = TextAlign.Center
                )
                Spacer(modifier = Modifier.height(14.dp))
                DashedLine(modifier = Modifier.fillMaxWidth(0.45f), color = SignalAmber)
                Spacer(modifier = Modifier.height(14.dp))
                Text(
                    text = term.displayDe,
                    style = bodyStyle(17),
                    color = Color.Gray,
                    textAlign = TextAlign.Center
                )
            } else {
                if (term.article != null) {
                    Box(
                        modifier = Modifier
                            .clip(CircleShape)
                            .background(de.fahrprufung.app.theme.HighwayTeal.copy(alpha = 0.12f))
                            .padding(horizontal = 12.dp, vertical = 5.dp)
                    ) {
                        Text(text = term.article, style = captionStyle(), color = de.fahrprufung.app.theme.HighwayTeal)
                    }
                    Spacer(modifier = Modifier.height(8.dp))
                }
                Text(text = term.displayDe, style = titleStyle(28), color = RoadNavy, textAlign = TextAlign.Center)
                Spacer(modifier = Modifier.height(10.dp))
                Text(
                    text = stringResource(R.string.flashcards_tapToFlip),
                    style = captionStyle(),
                    color = SignalAmber
                )
            }

            val phrase = term.displayExamPhraseDe
            if (phrase != null) {
                Spacer(modifier = Modifier.height(16.dp))
                ExaminerPhraseBubble(phrase)
            }
        }
    }
}

@Composable
private fun ExaminerPhraseBubble(text: String) {
    val gradientColors = CategoryStyle.style("phrases").gradient
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(16.dp))
            .background(Color(0xFFF2EDFA))
            .padding(14.dp)
    ) {
        Box(
            modifier = Modifier
                .size(36.dp)
                .clip(CircleShape)
                .background(androidx.compose.ui.graphics.Brush.linearGradient(gradientColors)),
            contentAlignment = Alignment.Center
        ) {
            Icon(imageVector = Icons.Filled.Person, contentDescription = null, tint = Color.White)
        }
        Spacer(modifier = Modifier.width(10.dp))
        Column {
            Text(
                text = stringResource(R.string.flashcards_examinerSays),
                style = captionStyle(11),
                color = Color.Gray
            )
            Text(text = text, style = bodyStyle(14), color = RoadNavy)
        }
    }
}
