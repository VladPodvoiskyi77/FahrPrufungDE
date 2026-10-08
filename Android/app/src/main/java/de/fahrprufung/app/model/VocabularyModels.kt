package de.fahrprufung.app.model

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

@Serializable
data class VocabularyCategory(
    val id: String,
    val de: String,
    val ru: String,
    val en: String,
    val uk: String,
    val fr: String,
    val tr: String
) {
    fun title(language: AppLanguage): String = when (language) {
        AppLanguage.RU -> ru
        AppLanguage.EN -> en
        AppLanguage.UK -> uk
        AppLanguage.FR -> fr
        AppLanguage.TR -> tr
    }.withLeadingCapital()

    val displayDe: String get() = de.withLeadingCapital()
}

@Serializable
data class VocabularyTerm(
    val id: String,
    val de: String,
    val article: String? = null,
    @SerialName("de_base") val deBase: String = "",
    val ru: String = "",
    val en: String = "",
    val uk: String = "",
    val fr: String = "",
    val tr: String = "",
    val category: String = "",
    val tags: List<String> = emptyList(),
    @SerialName("exam_phrase_de") val examPhraseDe: String? = null
) {
    fun translation(language: AppLanguage): String = when (language) {
        AppLanguage.RU -> ru
        AppLanguage.EN -> en
        AppLanguage.UK -> uk
        AppLanguage.FR -> fr
        AppLanguage.TR -> tr
    }

    val displayDe: String get() = de.withLeadingCapital()
    fun displayTranslation(language: AppLanguage): String = translation(language).withLeadingCapital()
    val displayExamPhraseDe: String? get() = examPhraseDe?.withLeadingCapital()

    val isCore: Boolean get() = tags.contains("core")
    val isExaminerPhrase: Boolean get() = tags.contains("examiner")

    /** Which examiner-phrase group this term belongs to, based on its tags. */
    val examinerGroup: ExaminerPhraseGroup
        get() {
            if (!isExaminerPhrase) return ExaminerPhraseGroup.START
            return ExaminerPhraseGroup.entries.firstOrNull { tags.contains(it.tag) }
                ?: ExaminerPhraseGroup.START
        }
}

@Serializable
data class VocabularyBundle(
    val version: String = "",
    val categories: List<VocabularyCategory> = emptyList(),
    val terms: List<VocabularyTerm> = emptyList()
)

enum class ExaminerPhraseGroup(val tag: String) {
    START("start"),
    DIRECTION("direction"),
    MANEUVER("maneuver"),
    SAFETY("safety"),
    HINT("hint"),
    RESULT("result");

    val id: String get() = tag
}

/** First letter/digit uppercased for UI display (lists, flashcards, quiz). */
fun String.withLeadingCapital(): String {
    val index = indexOfFirst { it.isLetter() || it.isDigit() }
    if (index < 0) return this
    return substring(0, index) + this[index].uppercaseChar() + substring(index + 1)
}
