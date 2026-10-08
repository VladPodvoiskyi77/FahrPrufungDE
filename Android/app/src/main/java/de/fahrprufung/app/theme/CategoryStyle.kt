package de.fahrprufung.app.theme

import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Bolt
import androidx.compose.material.icons.filled.Build
import androidx.compose.material.icons.filled.CarRepair
import androidx.compose.material.icons.filled.Description
import androidx.compose.material.icons.filled.DirectionsCar
import androidx.compose.material.icons.filled.Error
import androidx.compose.material.icons.filled.Folder
import androidx.compose.material.icons.filled.Info
import androidx.compose.material.icons.filled.Lightbulb
import androidx.compose.material.icons.filled.Memory
import androidx.compose.material.icons.filled.NotListedLocation
import androidx.compose.material.icons.filled.RecordVoiceOver
import androidx.compose.material.icons.filled.Shield
import androidx.compose.material.icons.filled.Signpost
import androidx.compose.material.icons.filled.SyncAlt
import androidx.compose.material.icons.filled.TaskAlt
import androidx.compose.material.icons.filled.Warning
import androidx.compose.material.icons.filled.WaterDrop
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector

/** Icon + gradient pairing for a vocabulary category id (mirrors iOS `CategoryStyle`). */
data class CategoryStyle(
    val icon: ImageVector,
    val color: Color,
    val gradient: List<Color>
) {
    companion object {
        fun style(categoryId: String): CategoryStyle = when (categoryId) {
            "exam" -> CategoryStyle(
                icon = Icons.Filled.TaskAlt,
                color = RoadNavy,
                gradient = listOf(RoadNavy, HighwayTeal)
            )
            "technik" -> CategoryStyle(
                icon = Icons.Filled.Build,
                color = Color(0xFF736B61),
                gradient = listOf(Color(0xFF8C8073), Color(0xFF666059))
            )
            "car" -> CategoryStyle(
                icon = Icons.Filled.DirectionsCar,
                color = HighwayTeal,
                gradient = listOf(HighwayTeal, Color(0xFF338C99))
            )
            "lights" -> CategoryStyle(
                icon = Icons.Filled.Lightbulb,
                color = SignalAmber,
                gradient = listOf(SignalAmber, Color(0xFFF2BF33))
            )
            "brakes" -> CategoryStyle(
                icon = Icons.Filled.CarRepair,
                color = SignalRed,
                gradient = listOf(SignalRed, Color(0xFFBF3838))
            )
            "fluids" -> CategoryStyle(
                icon = Icons.Filled.WaterDrop,
                color = Color(0xFF408CD9),
                gradient = listOf(Color(0xFF4D99E6), Color(0xFF3373BF))
            )
            "safety" -> CategoryStyle(
                icon = Icons.Filled.Shield,
                color = SignalGreen,
                gradient = listOf(SignalGreen, Color(0xFF1F9461))
            )
            "assist" -> CategoryStyle(
                icon = Icons.Filled.Memory,
                color = Color(0xFF7359BF),
                gradient = listOf(Color(0xFF8066CC), Color(0xFF5947A6))
            )
            "maneuvers" -> CategoryStyle(
                icon = Icons.Filled.SyncAlt,
                color = Color(0xFFD97333),
                gradient = listOf(Color(0xFFE68040), Color(0xFFBF612E))
            )
            "grundaufgaben" -> CategoryStyle(
                icon = Icons.Filled.NotListedLocation,
                color = Color(0xFF337AB8),
                gradient = listOf(Color(0xFF4085C7), Color(0xFF2661A0))
            )
            "traffic" -> CategoryStyle(
                icon = Icons.Filled.Signpost,
                color = SignalAmber,
                gradient = listOf(SignalAmber, Color(0xFFE08C1A))
            )
            "phrases" -> CategoryStyle(
                icon = Icons.Filled.RecordVoiceOver,
                color = Color(0xFF8C52AD),
                gradient = listOf(Color(0xFF9961B8), Color(0xFF733F94))
            )
            "documents" -> CategoryStyle(
                icon = Icons.Filled.Description,
                color = Color(0xFF59738C),
                gradient = listOf(Color(0xFF6680A0), Color(0xFF47617A))
            )
            "emergency" -> CategoryStyle(
                icon = Icons.Filled.Warning,
                color = SignalRed,
                gradient = listOf(SignalRed, Color(0xFFB33330))
            )
            else -> CategoryStyle(
                icon = Icons.Filled.Folder,
                color = HighwayTeal,
                gradient = listOf(HighwayTeal, RoadNavy)
            )
        }
    }
}

/** Icon + color for a traffic-sign category id. */
object SignStyle {
    fun categoryColor(category: String): Color = when (category) {
        "warning" -> SignalAmber
        "prohibitory" -> SignalRed
        "mandatory" -> HighwayTeal
        "information" -> SignalGreen
        "additional" -> RoadNavy
        else -> RoadNavy
    }

    fun categoryIcon(category: String): ImageVector = when (category) {
        "warning" -> Icons.Filled.Warning
        "prohibitory" -> Icons.Filled.Error
        "mandatory" -> Icons.Filled.Signpost
        "information" -> Icons.Filled.Info
        "additional" -> Icons.Filled.Bolt
        else -> Icons.Filled.Signpost
    }
}
