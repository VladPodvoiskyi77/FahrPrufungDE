package de.fahrprufung.app.data

import de.fahrprufung.app.model.ExaminerPhraseGroup
import de.fahrprufung.app.model.VocabularyTerm

/**
 * Resolves the raw (unfiltered) term pool for a flashcard/quiz session `sourceKey`
 * produced by `Routes.SourceKey`.
 */
fun AppContainer.rawTermsForSourceKey(key: String): List<VocabularyTerm> {
    val allTerms = content.terms.value
    return when {
        key == "core" -> allTerms.filter { it.isCore }
        key == "examiner" -> allTerms.filter { it.isExaminerPhrase }
        key.startsWith("examiner:") -> {
            val groupTag = key.removePrefix("examiner:")
            val group = ExaminerPhraseGroup.entries.firstOrNull { it.tag == groupTag }
            allTerms.filter { it.isExaminerPhrase && (group == null || it.examinerGroup == group) }
        }
        key == "all" -> allTerms
        key.startsWith("category:") -> {
            val categoryId = key.removePrefix("category:")
            allTerms.filter { it.category == categoryId }
        }
        else -> emptyList()
    }
}
