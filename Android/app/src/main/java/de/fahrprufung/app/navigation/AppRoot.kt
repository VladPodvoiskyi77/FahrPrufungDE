package de.fahrprufung.app.navigation

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.core.tween
import androidx.compose.animation.fadeOut
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.shadow
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.navigation.NavGraph.Companion.findStartDestination
import de.fahrprufung.app.theme.RoadNavy
import de.fahrprufung.app.theme.SignalAmber
import de.fahrprufung.app.theme.bodyStyle
import kotlinx.coroutines.launch
import androidx.navigation.NavHostController
import androidx.navigation.NavType
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.currentBackStackEntryAsState
import androidx.navigation.compose.rememberNavController
import androidx.navigation.navArgument
import de.fahrprufung.app.R
import de.fahrprufung.app.data.AnalyticsService
import de.fahrprufung.app.data.AppContainer
import de.fahrprufung.app.data.rawTermsForSourceKey
import de.fahrprufung.app.debug.ScreenshotSeed
import de.fahrprufung.app.theme.AppTheme
import de.fahrprufung.app.theme.titleStyle
import de.fahrprufung.app.ui.ProvideAppLocale
import de.fahrprufung.app.ui.categories.CategoryListScreen
import de.fahrprufung.app.ui.components.FloatingTabBar
import de.fahrprufung.app.ui.components.KnownUndoSnackbar
import de.fahrprufung.app.ui.examiner.ExaminerPhrasesScreen
import de.fahrprufung.app.ui.flashcards.FlashcardScreen
import de.fahrprufung.app.ui.home.HomeScreen
import de.fahrprufung.app.ui.onboarding.OnboardingScreen
import de.fahrprufung.app.ui.progress.ProgressScreen
import de.fahrprufung.app.ui.quiz.QuizScreen
import de.fahrprufung.app.ui.settings.SettingsScreen
import de.fahrprufung.app.ui.signs.SignDetailScreen
import de.fahrprufung.app.ui.signs.SignsListScreen
import de.fahrprufung.app.ui.terms.TermListScreen
import kotlinx.coroutines.delay

/** Splash (1.5s) -> Onboarding (if needed) -> main tabbed app. */
@Composable
fun AppRoot(container: AppContainer) {
    val nativeLanguage by container.nativeLanguage.collectAsState()
    // Skip splash when capturing store screenshots so deep-links land faster.
    var showSplash by remember { mutableStateOf(!ScreenshotSeed.isSeedRequested()) }

    LaunchedEffect(Unit) {
        if (!showSplash) return@LaunchedEffect
        delay(1500)
        showSplash = false
    }

    val loadError by container.content.loadError.collectAsState()
    val isLoading by container.content.isLoading.collectAsState()
    val terms by container.content.terms.collectAsState()
    val hasCompletedOnboarding by container.hasCompletedOnboarding.collectAsState()
    val knownTermIds by container.knownTermIds.collectAsState()
    val scope = rememberCoroutineScope()
    var didSyncEngagement by remember { mutableStateOf(false) }

    // Cold-start engagement props — mirrors iOS ContentView.onAppear (once).
    LaunchedEffect(terms.isNotEmpty(), hasCompletedOnboarding) {
        if (terms.isEmpty() || didSyncEngagement) return@LaunchedEffect
        didSyncEngagement = true
        AnalyticsService.logScreen("root")
        AnalyticsService.syncEngagementProperties(
            onboardingCompleted = hasCompletedOnboarding,
            studyStreak = container.learningStats.studyStreak,
            knownTermCount = knownTermIds.size
        )
    }

    ProvideAppLocale(language = nativeLanguage) {
        Box(modifier = Modifier.fillMaxSize()) {
            LaunchedEffect(hasCompletedOnboarding) {
                if (!hasCompletedOnboarding) AnalyticsService.logScreen("onboarding")
            }

            when {
                loadError != null && terms.isEmpty() -> {
                    ContentLoadError(
                        message = loadError ?: "",
                        onRetry = { scope.launch { container.content.retryLoad() } }
                    )
                }
                isLoading && terms.isEmpty() && !showSplash -> {
                    Box(Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                        CircularProgressIndicator(color = SignalAmber)
                    }
                }
                !hasCompletedOnboarding -> OnboardingScreen(container = container)
                else -> MainScaffold(container = container)
            }

            AnimatedVisibility(
                visible = showSplash,
                exit = fadeOut(animationSpec = tween(350))
            ) {
                SplashScreen()
            }
        }
    }
}

@Composable
private fun ContentLoadError(message: String, onRetry: () -> Unit) {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(32.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = androidx.compose.foundation.layout.Arrangement.Center
    ) {
        Text(
            text = message.ifBlank { stringResource(R.string.common_retry) },
            style = bodyStyle(16),
            color = RoadNavy,
            textAlign = TextAlign.Center
        )
        Spacer(modifier = Modifier.size(20.dp))
        Button(
            onClick = onRetry,
            colors = ButtonDefaults.buttonColors(containerColor = SignalAmber, contentColor = RoadNavy)
        ) {
            Text(stringResource(R.string.common_retry))
        }
    }
}

@Composable
private fun SplashScreen() {
    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(AppTheme.heroGradient),
        contentAlignment = Alignment.Center
    ) {
        Column(horizontalAlignment = Alignment.CenterHorizontally) {
            Image(
                painter = painterResource(R.drawable.splash_logo),
                contentDescription = null,
                contentScale = ContentScale.Crop,
                modifier = Modifier
                    .size(120.dp)
                    .shadow(
                        elevation = 12.dp,
                        shape = RoundedCornerShape(28.dp),
                        ambientColor = Color.Black.copy(alpha = 0.2f),
                        spotColor = Color.Black.copy(alpha = 0.25f)
                    )
                    .clip(RoundedCornerShape(28.dp))
            )
            Spacer(modifier = Modifier.size(20.dp))
            Text(
                text = stringResource(R.string.home_title),
                color = Color.White,
                style = titleStyle(28)
            )
        }
    }
}

@Composable
private fun MainScaffold(container: AppContainer) {
    val navController = rememberNavController()
    val undoState by container.knownUndo.state.collectAsState()
    val backStackEntry by navController.currentBackStackEntryAsState()
    val currentRoot = currentRootRoute(backStackEntry?.destination?.route)
    // Space for the floating pill tab bar (~72dp) + system nav insets.
    val bottomContentPadding = PaddingValues(bottom = 88.dp)

    LaunchedEffect(navController) {
        if (ScreenshotSeed.isSeedRequested()) {
            // Wait until seed prefs are applied so language + known counts match the shot.
            ScreenshotSeed.awaitSeed(container)
            delay(250)
        }
        ScreenshotSeed.consumePendingRoute()?.let { route ->
            runCatching { navController.navigate(route) }
        }
    }

    LaunchedEffect(backStackEntry?.destination?.route, backStackEntry?.arguments) {
        val route = backStackEntry?.destination?.route ?: return@LaunchedEffect
        val args = backStackEntry?.arguments
        val (name, params) = analyticsScreenForRoute(route, args, container)
        AnalyticsService.logScreen(name, params)
    }

    Box(modifier = Modifier.fillMaxSize()) {
        AppNavHost(
            navController = navController,
            container = container,
            contentPadding = bottomContentPadding
        )

        Column(
            modifier = Modifier.align(Alignment.BottomCenter)
        ) {
            KnownUndoSnackbar(
                isVisible = undoState.isVisible,
                message = undoState.message,
                onUndo = { container.knownUndo.performUndo() }
            )
            FloatingTabBar(
                selectedRoute = currentRoot,
                onSelect = { route -> navigateToTab(navController, route) }
            )
        }
    }
}

/** Maps Nav destinations to Firebase screen names (parity with iOS). */
private fun analyticsScreenForRoute(
    route: String,
    args: android.os.Bundle?,
    container: AppContainer
): Pair<String, Map<String, Any?>> {
    return when {
        route == Routes.HOME -> "home" to emptyMap()
        route == Routes.CATEGORIES -> "categories" to emptyMap()
        route.startsWith("terms/") -> {
            val id = args?.getString("categoryId") ?: ""
            "term_list" to mapOf("category_id" to id)
        }
        route == Routes.EXAMINER_PHRASES -> "examiner_phrases" to emptyMap()
        route.startsWith("flashcards/") -> "flashcards" to emptyMap()
        route.startsWith("quiz/") -> "quiz" to emptyMap()
        route == Routes.PROGRESS -> "progress" to emptyMap()
        route == Routes.SIGNS_LIST -> "signs_list" to emptyMap()
        route.startsWith("signDetail/") -> {
            val id = args?.getString("signId") ?: ""
            val stvo = container.content.sign(id)?.stvoCode ?: "unknown"
            "sign_detail" to mapOf("stvo_code" to stvo)
        }
        route == Routes.SETTINGS -> "settings" to emptyMap()
        else -> route to emptyMap()
    }
}

/** Maps any route (including ones with args) back to its owning bottom-tab root. */
private fun currentRootRoute(route: String?): String {
    if (route == null) return Routes.HOME
    return when {
        route == Routes.HOME || route == Routes.CATEGORIES ||
            route.startsWith("terms/") || route == Routes.EXAMINER_PHRASES ||
            route.startsWith("flashcards/") || route.startsWith("quiz/") -> Routes.HOME
        route == Routes.SIGNS_LIST || route.startsWith("signDetail/") -> Routes.SIGNS_LIST
        route == Routes.PROGRESS -> Routes.PROGRESS
        route == Routes.SETTINGS -> Routes.SETTINGS
        else -> Routes.HOME
    }
}

private fun navigateToTab(navController: NavHostController, route: String) {
    navController.navigate(route) {
        popUpTo(navController.graph.findStartDestination().id) { saveState = true }
        launchSingleTop = true
        restoreState = true
    }
}

@Composable
private fun AppNavHost(
    navController: NavHostController,
    container: AppContainer,
    contentPadding: PaddingValues
) {
    NavHost(
        navController = navController,
        startDestination = Routes.HOME,
        modifier = Modifier.padding(bottom = contentPadding.calculateBottomPadding())
    ) {
        composable(Routes.HOME) {
            HomeScreen(
                container = container,
                onOpenCategories = { navController.navigate(Routes.CATEGORIES) },
                onOpenProgress = { navController.navigate(Routes.PROGRESS) },
                onOpenExaminerPhrases = { navController.navigate(Routes.EXAMINER_PHRASES) },
                onOpenSignsTab = { navigateToTab(navController, Routes.SIGNS_LIST) },
                onOpenFlashcards = { key, title -> navController.navigate(Routes.flashcards(key, title)) },
                onOpenQuiz = { key, title -> navController.navigate(Routes.quiz(key, title)) }
            )
        }
        composable(Routes.CATEGORIES) {
            CategoryListScreen(
                container = container,
                onOpenCategory = { category ->
                    if (category.id == "phrases") {
                        navController.navigate(Routes.EXAMINER_PHRASES)
                    } else {
                        navController.navigate(Routes.termList(category.id))
                    }
                },
                onBack = { navController.popBackStack() }
            )
        }
        composable(
            route = Routes.TERM_LIST_PATTERN,
            arguments = listOf(navArgument("categoryId") { type = NavType.StringType })
        ) { entry ->
            val categoryId = entry.arguments?.getString("categoryId") ?: return@composable
            TermListScreen(
                container = container,
                categoryId = categoryId,
                onOpenFlashcards = { key, title -> navController.navigate(Routes.flashcards(key, title)) },
                onOpenQuiz = { key, title -> navController.navigate(Routes.quiz(key, title)) },
                onBack = { navController.popBackStack() }
            )
        }
        composable(Routes.EXAMINER_PHRASES) {
            ExaminerPhrasesScreen(
                container = container,
                onOpenFlashcards = { key, title -> navController.navigate(Routes.flashcards(key, title)) },
                onOpenQuiz = { key, title -> navController.navigate(Routes.quiz(key, title)) },
                onBack = { navController.popBackStack() }
            )
        }
        composable(
            route = Routes.FLASHCARDS_PATTERN,
            arguments = listOf(
                navArgument("sourceKey") { type = NavType.StringType },
                navArgument("title") { type = NavType.StringType }
            )
        ) { entry ->
            val sourceKey = entry.arguments?.getString("sourceKey") ?: return@composable
            val title = entry.arguments?.getString("title") ?: ""
            val rawTerms = remember(sourceKey) { container.rawTermsForSourceKey(sourceKey) }
            FlashcardScreen(
                container = container,
                sessionTitle = title,
                rawTerms = rawTerms,
                onBack = { navController.popBackStack() }
            )
        }
        composable(
            route = Routes.QUIZ_PATTERN,
            arguments = listOf(
                navArgument("sourceKey") { type = NavType.StringType },
                navArgument("title") { type = NavType.StringType }
            )
        ) { entry ->
            val sourceKey = entry.arguments?.getString("sourceKey") ?: return@composable
            val title = entry.arguments?.getString("title") ?: ""
            val rawTerms = remember(sourceKey) { container.rawTermsForSourceKey(sourceKey) }
            QuizScreen(
                container = container,
                sessionTitle = title,
                sourceTerms = rawTerms,
                onBack = { navController.popBackStack() }
            )
        }
        composable(Routes.PROGRESS) {
            ProgressScreen(container = container)
        }
        composable(Routes.SIGNS_LIST) {
            SignsListScreen(
                container = container,
                onOpenSign = { sign -> navController.navigate(Routes.signDetail(sign.id)) }
            )
        }
        composable(
            route = Routes.SIGN_DETAIL_PATTERN,
            arguments = listOf(navArgument("signId") { type = NavType.StringType })
        ) { entry ->
            val signId = entry.arguments?.getString("signId") ?: return@composable
            SignDetailScreen(
                container = container,
                signId = signId,
                onBack = { navController.popBackStack() }
            )
        }
        composable(Routes.SETTINGS) {
            SettingsScreen(
                container = container,
                onOpenProgress = { navController.navigate(Routes.PROGRESS) }
            )
        }
    }
}
