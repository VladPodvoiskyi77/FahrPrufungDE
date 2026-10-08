package de.fahrprufung.app.data

import android.content.Context
import android.speech.tts.TextToSpeech
import android.speech.tts.UtteranceProgressListener
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import java.util.Locale

/** Speaks German text aloud using the platform TextToSpeech engine (de-DE voice). */
class GermanSpeechHelper(context: Context) {

    private var tts: TextToSpeech? = null
    private var isReady = false

    private val _speakingId = MutableStateFlow<String?>(null)
    val speakingId: StateFlow<String?> = _speakingId

    init {
        tts = TextToSpeech(context.applicationContext) { status ->
            if (status == TextToSpeech.SUCCESS) {
                tts?.language = Locale.GERMANY
                tts?.setSpeechRate(0.92f)
                isReady = true
            }
        }
        tts?.setOnUtteranceProgressListener(object : UtteranceProgressListener() {
            override fun onStart(utteranceId: String?) = Unit
            override fun onDone(utteranceId: String?) {
                _speakingId.value = null
            }

            @Deprecated("Deprecated in TextToSpeech")
            override fun onError(utteranceId: String?) {
                _speakingId.value = null
            }

            override fun onStop(utteranceId: String?, interrupted: Boolean) {
                _speakingId.value = null
            }
        })
    }

    fun isSpeaking(id: String): Boolean = _speakingId.value == id

    /** Speaks the given text; tapping the same id again stops playback (toggle behavior). */
    fun speakGerman(text: String, id: String) {
        val trimmed = text.trim()
        if (trimmed.isEmpty()) return

        if (_speakingId.value == id) {
            stop()
            return
        }

        stop()
        _speakingId.value = id
        tts?.speak(trimmed, TextToSpeech.QUEUE_FLUSH, null, id)
    }

    fun stop() {
        tts?.stop()
        _speakingId.value = null
    }

    fun shutdown() {
        tts?.shutdown()
        tts = null
    }
}
