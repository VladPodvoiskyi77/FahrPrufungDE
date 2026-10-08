package de.fahrprufung.app.ui.onboarding

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
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
import androidx.compose.foundation.pager.HorizontalPager
import androidx.compose.foundation.pager.rememberPagerState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.DirectionsCar
import androidx.compose.material.icons.filled.Public
import androidx.compose.material.icons.filled.QuestionAnswer
import androidx.compose.material.icons.filled.RecordVoiceOver
import androidx.compose.material.icons.filled.Signpost
import androidx.compose.material.icons.filled.ViewCarousel
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Icon
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.unit.dp
import de.fahrprufung.app.R
import de.fahrprufung.app.data.AnalyticsService
import de.fahrprufung.app.data.AppContainer
import de.fahrprufung.app.model.AppLanguage
import de.fahrprufung.app.theme.AppTheme
import de.fahrprufung.app.theme.RoadNavy
import de.fahrprufung.app.theme.SignalAmber
import de.fahrprufung.app.theme.bodyStyle
import de.fahrprufung.app.theme.headlineStyle
import de.fahrprufung.app.theme.titleStyle
import de.fahrprufung.app.ui.components.AppScreenBackground
import de.fahrprufung.app.ui.components.LanguagePickerRow
import kotlinx.coroutines.launch

@Composable
fun OnboardingScreen(container: AppContainer) {
    val nativeLanguage by container.nativeLanguage.collectAsState()
    var draftLanguage by remember { mutableStateOf(nativeLanguage) }
    val pagerState = rememberPagerState(pageCount = { 3 })
    val scope = rememberCoroutineScope()

    fun complete(savingLanguage: Boolean) {
        if (savingLanguage) {
            container.setNativeLanguage(draftLanguage)
            AnalyticsService.logOnboardingCompleted(draftLanguage)
        } else {
            // Keep current/system language; still record it so analytics has ui_language.
            AnalyticsService.logOnboardingSkipped(nativeLanguage)
        }
        AnalyticsService.syncEngagementProperties(
            onboardingCompleted = true,
            studyStreak = container.learningStats.studyStreak,
            knownTermCount = container.knownTermIds.value.size
        )
        container.setHasCompletedOnboarding(true)
    }

    AppScreenBackground {
        Column(modifier = Modifier.fillMaxSize()) {
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 24.dp, vertical = 16.dp),
                horizontalArrangement = Arrangement.End
            ) {
                if (pagerState.currentPage < 2) {
                    TextButton(onClick = { complete(false) }) {
                        Text(text = stringResource(R.string.common_skip), color = Color.Gray)
                    }
                }
            }

            HorizontalPager(
                state = pagerState,
                modifier = Modifier.weight(1f)
            ) { page ->
                when (page) {
                    0 -> WelcomePage(draftLanguage) { draftLanguage = it }
                    1 -> FeaturesPage()
                    else -> LanguagePage(draftLanguage) { draftLanguage = it }
                }
            }

            PageIndicator(currentPage = pagerState.currentPage, pageCount = 3)

            Button(
                onClick = {
                    if (pagerState.currentPage >= 2) {
                        complete(true)
                    } else {
                        scope.launch { pagerState.animateScrollToPage(pagerState.currentPage + 1) }
                    }
                },
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 24.dp, vertical = 16.dp)
                    .height(52.dp),
                shape = RoundedCornerShape(12.dp),
                colors = ButtonDefaults.buttonColors(containerColor = SignalAmber)
            ) {
                Text(
                    text = stringResource(
                        if (pagerState.currentPage >= 2) R.string.onboarding_start else R.string.common_next
                    ),
                    style = headlineStyle(),
                    color = Color.White
                )
            }
        }
    }
}

@Composable
private fun PageIndicator(currentPage: Int, pageCount: Int) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .padding(vertical = 8.dp),
        horizontalArrangement = Arrangement.Center
    ) {
        repeat(pageCount) { index ->
            Box(
                modifier = Modifier
                    .padding(horizontal = 4.dp)
                    .size(if (index == currentPage) 9.dp else 7.dp)
                    .clip(CircleShape)
                    .background(if (index == currentPage) SignalAmber else RoadNavy.copy(alpha = 0.2f))
            )
        }
    }
}

@Composable
private fun WelcomePage(draftLanguage: AppLanguage, onSelect: (AppLanguage) -> Unit) {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(horizontal = 24.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        Box(
            modifier = Modifier
                .size(140.dp)
                .clip(CircleShape)
                .background(AppTheme.heroGradient),
            contentAlignment = Alignment.Center
        ) {
            Icon(
                imageVector = Icons.Filled.DirectionsCar,
                contentDescription = null,
                tint = Color.White,
                modifier = Modifier.size(56.dp)
            )
        }

        Spacer(modifier = Modifier.height(24.dp))

        Text(
            text = stringResource(R.string.onboarding_welcomeTitle),
            style = titleStyle(32),
            color = RoadNavy,
            textAlign = androidx.compose.ui.text.style.TextAlign.Center
        )
        Spacer(modifier = Modifier.height(12.dp))
        Text(
            text = stringResource(R.string.onboarding_welcomeSubtitle),
            style = bodyStyle(16),
            color = Color.Gray,
            textAlign = androidx.compose.ui.text.style.TextAlign.Center
        )

        Spacer(modifier = Modifier.height(20.dp))

        Row(horizontalArrangement = Arrangement.spacedBy(10.dp)) {
            AppLanguage.entries.forEach { language ->
                val selected = language == draftLanguage
                Box(
                    modifier = Modifier
                        .size(44.dp)
                        .clip(CircleShape)
                        .background(if (selected) SignalAmber.copy(alpha = 0.25f) else Color.White)
                        .clickable { onSelect(language) },
                    contentAlignment = Alignment.Center
                ) {
                    Text(text = language.flag, style = titleStyle(20))
                }
            }
        }

        Spacer(modifier = Modifier.height(20.dp))

        Text(
            text = stringResource(R.string.settings_disclaimer),
            style = de.fahrprufung.app.theme.captionStyle(11),
            color = Color.Gray,
            textAlign = androidx.compose.ui.text.style.TextAlign.Center
        )
    }
}

@Composable
private fun FeaturesPage() {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(horizontal = 24.dp),
        verticalArrangement = Arrangement.Center
    ) {
        Text(text = stringResource(R.string.onboarding_featuresTitle), style = titleStyle(28), color = RoadNavy)
        Spacer(modifier = Modifier.height(20.dp))
        FeatureRow(Icons.Filled.ViewCarousel, stringResource(R.string.onboarding_featureCards), listOf(de.fahrprufung.app.theme.HighwayTeal, RoadNavy))
        FeatureRow(Icons.Filled.QuestionAnswer, stringResource(R.string.onboarding_featureQuiz), listOf(SignalAmber, de.fahrprufung.app.theme.AccentEnd))
        FeatureRow(Icons.Filled.RecordVoiceOver, stringResource(R.string.onboarding_featureExaminer), listOf(de.fahrprufung.app.theme.SignalGreen, de.fahrprufung.app.theme.HighwayTeal))
        FeatureRow(Icons.Filled.Signpost, stringResource(R.string.onboarding_featureSigns), listOf(de.fahrprufung.app.theme.SignalGreen, RoadNavy))
    }
}

@Composable
private fun FeatureRow(icon: ImageVector, text: String, colors: List<Color>) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .padding(vertical = 8.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Box(
            modifier = Modifier
                .size(44.dp)
                .clip(RoundedCornerShape(12.dp))
                .background(androidx.compose.ui.graphics.Brush.linearGradient(colors)),
            contentAlignment = Alignment.Center
        ) {
            Icon(imageVector = icon, contentDescription = null, tint = Color.White)
        }
        Spacer(modifier = Modifier.width(16.dp))
        Text(text = text, style = bodyStyle(15), color = RoadNavy, modifier = Modifier.weight(1f))
    }
}

@Composable
private fun LanguagePage(draftLanguage: AppLanguage, onSelect: (AppLanguage) -> Unit) {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(horizontal = 20.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        Icon(
            imageVector = Icons.Filled.Public,
            contentDescription = null,
            tint = de.fahrprufung.app.theme.HighwayTeal,
            modifier = Modifier.size(48.dp)
        )
        Spacer(modifier = Modifier.height(16.dp))
        Text(text = stringResource(R.string.onboarding_languageTitle), style = titleStyle(28), color = RoadNavy)
        Spacer(modifier = Modifier.height(20.dp))
        LanguagePickerRow(selection = draftLanguage, onSelect = onSelect)
    }
}
