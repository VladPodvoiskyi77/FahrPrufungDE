package de.fahrprufung.app.model

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

@Serializable
data class SignCategoryInfo(
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
data class SignNotes(
    val de: String = "",
    val ru: String = "",
    val en: String = "",
    val uk: String = "",
    val fr: String = "",
    val tr: String = ""
) {
    fun text(language: AppLanguage): String = when (language) {
        AppLanguage.RU -> ru
        AppLanguage.EN -> en
        AppLanguage.UK -> uk
        AppLanguage.FR -> fr
        AppLanguage.TR -> tr
    }
}

@Serializable
data class TrafficSign(
    val id: String,
    @SerialName("stvo_code") val stvoCode: String? = null,
    val shape: String? = null,
    val image: String? = null,
    val svg: String? = null,
    val de: String = "",
    val ru: String = "",
    val en: String = "",
    val uk: String = "",
    val fr: String = "",
    val tr: String = "",
    val category: String = "",
    @SerialName("source_url") val sourceUrl: String? = null,
    val license: String? = null,
    val notes: SignNotes? = null
) {
    fun translation(language: AppLanguage): String = when (language) {
        AppLanguage.RU -> ru
        AppLanguage.EN -> en
        AppLanguage.UK -> uk
        AppLanguage.FR -> fr
        AppLanguage.TR -> tr
    }.withLeadingCapital()

    val displayDe: String get() = de.withLeadingCapital()

    fun note(language: AppLanguage): String? =
        notes?.text(language)?.takeIf { it.isNotBlank() }?.withLeadingCapital()
}

@Serializable
data class SignsBundle(
    val version: String = "",
    val description: String? = null,
    val source: String? = null,
    @SerialName("source_note") val sourceNote: String? = null,
    val categories: List<SignCategoryInfo>? = null,
    val signs: List<TrafficSign> = emptyList()
)
