package de.fahrprufung.app.navigation

import android.net.Uri

/** Flat route table for the single top-level `NavHost` (mirrors the iOS Learn/Signs flows). */
object Routes {
    const val ONBOARDING = "onboarding"

    const val HOME = "home"
    const val CATEGORIES = "categories"

    const val TERM_LIST_PATTERN = "terms/{categoryId}"
    fun termList(categoryId: String) = "terms/${Uri.encode(categoryId)}"

    const val EXAMINER_PHRASES = "examinerPhrases"

    const val FLASHCARDS_PATTERN = "flashcards/{sourceKey}/{title}"
    fun flashcards(sourceKey: String, title: String) =
        "flashcards/${Uri.encode(sourceKey)}/${Uri.encode(title)}"

    const val QUIZ_PATTERN = "quiz/{sourceKey}/{title}"
    fun quiz(sourceKey: String, title: String) =
        "quiz/${Uri.encode(sourceKey)}/${Uri.encode(title)}"

    const val PROGRESS = "progress"

    const val SIGNS_LIST = "signsList"

    const val SIGN_DETAIL_PATTERN = "signDetail/{signId}"
    fun signDetail(signId: String) = "signDetail/${Uri.encode(signId)}"

    const val SETTINGS = "settings"

    /** Session source keys understood by [de.fahrprufung.app.data.SessionTerms]. */
    object SourceKey {
        const val CORE = "core"
        const val EXAMINER = "examiner"
        const val ALL = "all"
        fun examinerGroup(group: String) = "examiner:$group"
        fun category(id: String) = "category:$id"
    }

    /** Top-level bottom-navigation destinations. */
    val bottomTabs = listOf(HOME, SIGNS_LIST, PROGRESS, SETTINGS)
}
