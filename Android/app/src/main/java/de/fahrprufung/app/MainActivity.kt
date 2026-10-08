package de.fahrprufung.app

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.runtime.LaunchedEffect
import de.fahrprufung.app.data.AppContainer
import de.fahrprufung.app.debug.ScreenshotSeed
import de.fahrprufung.app.navigation.AppRoot
import de.fahrprufung.app.theme.FahrPrufungTheme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()

        val container = AppContainer.getInstance(applicationContext)
        ScreenshotSeed.prepare(intent)

        setContent {
            FahrPrufungTheme {
                LaunchedEffect(Unit) {
                    ScreenshotSeed.awaitSeed(container)
                }
                AppRoot(container = container)
            }
        }
    }
}
