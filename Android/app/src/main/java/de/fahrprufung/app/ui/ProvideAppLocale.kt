package de.fahrprufung.app.ui

import android.content.res.Configuration
import androidx.compose.runtime.Composable
import androidx.compose.runtime.CompositionLocalProvider
import androidx.compose.runtime.remember
import androidx.compose.ui.platform.LocalConfiguration
import androidx.compose.ui.platform.LocalContext
import de.fahrprufung.app.model.AppLanguage
import java.util.Locale

/**
 * Applies the in-app language to Compose string resources immediately,
 * without requiring an Activity recreate (mirrors iOS LocalizationManager).
 */
@Composable
fun ProvideAppLocale(
    language: AppLanguage,
    content: @Composable () -> Unit
) {
    val baseContext = LocalContext.current
    val localizedContext = remember(language, baseContext) {
        val config = Configuration(baseContext.resources.configuration)
        val locale = Locale.forLanguageTag(language.code)
        config.setLocale(locale)
        baseContext.createConfigurationContext(config)
    }
    val localizedConfiguration = remember(language) {
        Configuration().apply {
            setLocale(Locale.forLanguageTag(language.code))
        }
    }

    CompositionLocalProvider(
        LocalContext provides localizedContext,
        LocalConfiguration provides localizedConfiguration,
        content = content
    )
}
