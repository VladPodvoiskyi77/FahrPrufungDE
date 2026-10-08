package de.fahrprufung.app.model

import android.os.Build
import android.os.LocaleList
import java.util.Locale

/** Supported translation languages. German is content-only and never a UI language. */
enum class AppLanguage(val code: String, val displayName: String, val flag: String) {
    RU("ru", "Русский", "\uD83C\uDDF7\uD83C\uDDFA"),
    EN("en", "English", "\uD83C\uDDEC\uD83C\uDDE7"),
    UK("uk", "Українська", "\uD83C\uDDFA\uD83C\uDDE6"),
    FR("fr", "Français", "\uD83C\uDDEB\uD83C\uDDF7"),
    TR("tr", "Türkçe", "\uD83C\uDDF9\uD83C\uDDF7");

    companion object {
        fun fromCode(code: String?): AppLanguage? = entries.firstOrNull { it.code == code }

        /**
         * First-launch default — mirrors iOS `AppLanguage.systemDefault`
         * (walk preferred locales, fall back to English).
         */
        fun systemDefault(): AppLanguage {
            val preferred = linkedSetOf<String>()
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.N) {
                val locales: LocaleList = LocaleList.getDefault()
                for (i in 0 until locales.size()) {
                    preferred += locales[i].language
                }
            } else {
                preferred += Locale.getDefault().language
            }
            for (language in preferred) {
                fromCode(language.lowercase(Locale.ROOT))?.let { return it }
            }
            return EN
        }
    }
}
