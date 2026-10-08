package de.fahrprufung.app.debug

import android.content.Intent
import android.util.Log
import de.fahrprufung.app.BuildConfig
import de.fahrprufung.app.data.AppContainer
import de.fahrprufung.app.model.AppLanguage
import de.fahrprufung.app.model.LearningStatsData
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.sync.Mutex
import kotlinx.coroutines.sync.withLock
import kotlinx.coroutines.withContext
import java.text.SimpleDateFormat
import java.util.Calendar
import java.util.Locale

/**
 * Debug-only helper for Play Store / marketing screenshots.
 *
 * adb shell am start -n de.fahrprufung.app/.MainActivity \
 *   --ez seed_screenshots true --es lang en \
 *   --es open_route "flashcards/core/Top%20terms"
 */
object ScreenshotSeed {
    const val EXTRA_SEED = "seed_screenshots"
    const val EXTRA_LANG = "lang"
    const val EXTRA_OPEN_ROUTE = "open_route"

    private const val TAG = "ScreenshotSeed"

    @Volatile
    var pendingRoute: String? = null
        private set

    @Volatile
    private var seedRequested = false

    @Volatile
    private var seedLanguage: AppLanguage = AppLanguage.EN

    @Volatile
    private var seeded = false

    private val mutex = Mutex()

    fun consumePendingRoute(): String? {
        val route = pendingRoute
        pendingRoute = null
        return route
    }

    fun isSeedRequested(): Boolean = seedRequested

    fun prepare(intent: Intent?) {
        if (!BuildConfig.DEBUG || intent == null) return
        intent.getStringExtra(EXTRA_OPEN_ROUTE)?.takeIf { it.isNotBlank() }?.let {
            pendingRoute = it
        }
        if (intent.getBooleanExtra(EXTRA_SEED, false)) {
            seedRequested = true
            seedLanguage = AppLanguage.fromCode(intent.getStringExtra(EXTRA_LANG)) ?: AppLanguage.EN
        }
    }

    /** Apply screenshot prefs. Safe to call from LaunchedEffect; heavy work off Main. */
    suspend fun awaitSeed(container: AppContainer) {
        if (!seedRequested) return
        mutex.withLock {
            if (seeded) return
            withContext(Dispatchers.IO) {
                var attempts = 0
                while (attempts < 200) {
                    container.content.loadIfNeeded()
                    if (container.content.terms.value.isNotEmpty() &&
                        container.content.signs.value.isNotEmpty()
                    ) {
                        break
                    }
                    kotlinx.coroutines.delay(50)
                    attempts++
                }
                val terms = container.content.terms.value
                val signs = container.content.signs.value
                if (terms.isEmpty() || signs.isEmpty()) {
                    Log.e(TAG, "Content not loaded (terms=${terms.size}, signs=${signs.size})")
                    return@withContext
                }

                val termIds = terms.take(31).map { it.id }.toSet()
                val signIds = signs.take(30).map { it.id }.toSet()

                val dayFormat = SimpleDateFormat("yyyy-MM-dd", Locale.US)
                val cal = Calendar.getInstance()
                val today = dayFormat.format(cal.time)
                cal.add(Calendar.DAY_OF_YEAR, -1)
                val yesterday = dayFormat.format(cal.time)
                val stats = LearningStatsData(studyDayKeys = setOf(today, yesterday))

                container.preferences.setNativeLanguage(seedLanguage)
                container.preferences.setHasCompletedOnboarding(true)
                container.preferences.setKnownTermIds(termIds)
                container.preferences.setKnownSignIds(signIds)
                container.learningStats.replaceForScreenshots(stats)
                seeded = true
                Log.i(TAG, "Seeded lang=${seedLanguage.code} terms=${termIds.size} signs=${signIds.size}")
            }
        }
    }
}
