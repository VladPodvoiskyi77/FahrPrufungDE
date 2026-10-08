package de.fahrprufung.app.data

import android.content.Context
import de.fahrprufung.app.model.SignCategoryInfo
import de.fahrprufung.app.model.SignsBundle
import de.fahrprufung.app.model.TrafficSign
import de.fahrprufung.app.model.VocabularyBundle
import de.fahrprufung.app.model.VocabularyCategory
import de.fahrprufung.app.model.VocabularyTerm
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.withContext
import kotlinx.serialization.json.Json

/** Loads `vocabulary.json` and `signs.json` from assets and exposes them reactively. */
class ContentRepository(private val context: Context) {

    private val json = Json { ignoreUnknownKeys = true }

    private val _categories = MutableStateFlow<List<VocabularyCategory>>(emptyList())
    val categories: StateFlow<List<VocabularyCategory>> = _categories

    private val _terms = MutableStateFlow<List<VocabularyTerm>>(emptyList())
    val terms: StateFlow<List<VocabularyTerm>> = _terms

    private val _signs = MutableStateFlow<List<TrafficSign>>(emptyList())
    val signs: StateFlow<List<TrafficSign>> = _signs

    private val _signCategories = MutableStateFlow<List<SignCategoryInfo>>(emptyList())
    val signCategories: StateFlow<List<SignCategoryInfo>> = _signCategories

    private val _isLoading = MutableStateFlow(false)
    val isLoading: StateFlow<Boolean> = _isLoading

    private val _loadError = MutableStateFlow<String?>(null)
    val loadError: StateFlow<String?> = _loadError

    private var loaded = false

    suspend fun loadIfNeeded() {
        if (loaded) return
        // Another caller may already be loading — wait, then retry if it failed.
        if (_isLoading.value) {
            while (_isLoading.value) {
                kotlinx.coroutines.delay(20)
            }
            if (loaded) return
        }
        _isLoading.value = true
        try {
            val (vocabulary, signsBundle, resolvedSignCategories) = withContext(Dispatchers.IO) {
                val vocabulary = readAsset<VocabularyBundle>("vocabulary.json")
                val signsBundle = readAsset<SignsBundle>("signs.json")
                val resolvedSignCategories = signsBundle.categories
                    ?: defaultSignCategories(signsBundle.signs)
                Triple(vocabulary, signsBundle, resolvedSignCategories)
            }
            _categories.value = vocabulary.categories
            _terms.value = vocabulary.terms
            _signs.value = signsBundle.signs
            _signCategories.value = resolvedSignCategories
            _loadError.value = null
            loaded = true
        } catch (t: Throwable) {
            _loadError.value = t.message ?: "Failed to load content"
        } finally {
            _isLoading.value = false
        }
    }

    /** Clears a failed load so [loadIfNeeded] can run again. */
    suspend fun retryLoad() {
        if (loaded) return
        _loadError.value = null
        loadIfNeeded()
    }

    fun termsForCategory(categoryId: String): List<VocabularyTerm> =
        _terms.value.filter { it.category == categoryId }

    fun category(id: String): VocabularyCategory? = _categories.value.firstOrNull { it.id == id }

    fun sign(id: String): TrafficSign? = _signs.value.firstOrNull { it.id == id }

    /** Terms not marked known (learning pool). */
    fun learningTerms(source: List<VocabularyTerm>, knownIds: Set<String>): List<VocabularyTerm> =
        source.filter { it.id !in knownIds }

    fun learningSigns(source: List<TrafficSign>, knownIds: Set<String>): List<TrafficSign> =
        source.filter { it.id !in knownIds }

    private inline fun <reified T> readAsset(name: String): T {
        val text = context.assets.open(name).bufferedReader().use { it.readText() }
        return json.decodeFromString(text)
    }

    private fun defaultSignCategories(signs: List<TrafficSign>): List<SignCategoryInfo> {
        val ids = signs.map { it.category }.toSortedSet()
        return ids.map { id -> SignCategoryInfo(id = id, de = id, ru = id, en = id, uk = id, fr = id, tr = id) }
    }
}
