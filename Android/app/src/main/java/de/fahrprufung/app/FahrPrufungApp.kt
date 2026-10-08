package de.fahrprufung.app

import android.app.Application
import de.fahrprufung.app.data.AnalyticsService
import de.fahrprufung.app.data.AppContainer
import de.fahrprufung.app.data.AppLifecycleAnalytics
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.launch
import kotlinx.coroutines.runBlocking

class FahrPrufungApp : Application() {
    lateinit var container: AppContainer

    override fun onCreate() {
        super.onCreate()
        container = AppContainer.getInstance(this)
        // Sync opt-out before any events fire.
        val enabled = runBlocking { container.preferences.analyticsEnabled.first() }
        AnalyticsService.setEnabled(enabled)
        container.appScope.launch {
            container.analyticsEnabled.collect { AnalyticsService.setEnabled(it) }
        }
        AppLifecycleAnalytics.start()
    }
}
