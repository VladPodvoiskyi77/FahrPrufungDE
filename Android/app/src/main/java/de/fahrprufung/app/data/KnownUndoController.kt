package de.fahrprufung.app.data

import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Job
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch

data class KnownUndoState(val isVisible: Boolean = false, val message: String = "")

/** Drives the "marked as known" undo snackbar, auto-dismissing after a few seconds. */
class KnownUndoController(private val scope: CoroutineScope) {

    private val _state = MutableStateFlow(KnownUndoState())
    val state: StateFlow<KnownUndoState> = _state

    private var undoAction: (() -> Unit)? = null
    private var dismissJob: Job? = null

    fun offerUndo(message: String, undo: () -> Unit) {
        dismissJob?.cancel()
        undoAction = undo
        _state.value = KnownUndoState(isVisible = true, message = message)
        dismissJob = scope.launch {
            delay(3_000)
            dismiss()
        }
    }

    fun performUndo() {
        undoAction?.invoke()
        dismiss()
    }

    fun dismiss() {
        dismissJob?.cancel()
        dismissJob = null
        undoAction = null
        if (_state.value.isVisible) {
            _state.value = KnownUndoState()
        }
    }
}
