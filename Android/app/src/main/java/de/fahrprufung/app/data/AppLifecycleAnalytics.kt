package de.fahrprufung.app.data

import androidx.lifecycle.DefaultLifecycleObserver
import androidx.lifecycle.LifecycleOwner
import androidx.lifecycle.ProcessLifecycleOwner

/** Tracks process foreground/background for analytics (app open / leave). */
object AppLifecycleAnalytics : DefaultLifecycleObserver {
    @Volatile
    private var started = false

    @Volatile
    private var hasOpened = false

    fun start() {
        if (started) return
        started = true
        ProcessLifecycleOwner.get().lifecycle.addObserver(this)
    }

    override fun onStart(owner: LifecycleOwner) {
        if (!hasOpened) {
            hasOpened = true
            AnalyticsService.logAppOpen()
        } else {
            AnalyticsService.logAppForeground()
        }
    }

    override fun onStop(owner: LifecycleOwner) {
        AnalyticsService.logAppBackground()
    }
}
