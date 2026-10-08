package de.fahrprufung.app.ui.signs

import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Description
import androidx.compose.material.icons.filled.Lightbulb
import androidx.compose.material3.Icon
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.shadow
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.asImageBitmap
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp
import de.fahrprufung.app.R
import de.fahrprufung.app.data.AppContainer
import de.fahrprufung.app.model.AppLanguage
import de.fahrprufung.app.model.TrafficSign
import de.fahrprufung.app.theme.AppTheme
import de.fahrprufung.app.theme.HighwayTeal
import de.fahrprufung.app.theme.RoadNavy
import de.fahrprufung.app.theme.SignStyle
import de.fahrprufung.app.theme.bodyStyle
import de.fahrprufung.app.theme.captionStyle
import de.fahrprufung.app.theme.headlineStyle
import de.fahrprufung.app.theme.titleStyle
import de.fahrprufung.app.ui.components.AppCard
import de.fahrprufung.app.ui.components.AppScreenBackground
import de.fahrprufung.app.ui.components.KnownMarkButton
import de.fahrprufung.app.ui.components.ScreenTopBar

@Composable
fun SignDetailScreen(
    container: AppContainer,
    signId: String,
    onBack: () -> Unit
) {
    val allSigns by container.content.signs.collectAsState()
    val signCategories by container.content.signCategories.collectAsState()
    val sign = allSigns.firstOrNull { it.id == signId }
    val nativeLanguage by container.nativeLanguage.collectAsState()
    val knownSignIds by container.knownSignIds.collectAsState()
    val undoMessage = stringResource(R.string.known_undoMessage)

    val categoryLabel = sign?.let { s ->
        signCategories.firstOrNull { it.id == s.category }?.title(nativeLanguage)
            ?: s.category.replaceFirstChar { it.uppercase() }
    }.orEmpty()

    Scaffold(
        containerColor = Color.Transparent,
        topBar = { ScreenTopBar(title = "", onBack = onBack) }
    ) { padding ->
        AppScreenBackground {
            if (sign == null) {
                Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                    Text(text = stringResource(R.string.signs_empty_title), color = RoadNavy)
                }
            } else {
                SignDetailContent(
                    container = container,
                    sign = sign,
                    nativeLanguage = nativeLanguage,
                    categoryLabel = categoryLabel,
                    isKnown = sign.id in knownSignIds,
                    undoMessage = undoMessage,
                    topPadding = padding.calculateTopPadding()
                )
            }
        }
    }
}

@Composable
private fun SignDetailContent(
    container: AppContainer,
    sign: TrafficSign,
    nativeLanguage: AppLanguage,
    categoryLabel: String,
    isKnown: Boolean,
    undoMessage: String,
    topPadding: Dp
) {
    val style = SignStyle.categoryColor(sign.category)

    Column(
        modifier = Modifier
            .fillMaxSize()
            .verticalScroll(rememberScrollState())
            .padding(top = topPadding)
            .padding(horizontal = 20.dp),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Spacer(modifier = Modifier.height(8.dp))

        SignImageCard(imageName = sign.image, tint = style)

        Spacer(modifier = Modifier.height(20.dp))

        Text(
            text = sign.translation(nativeLanguage),
            style = titleStyle(24),
            color = RoadNavy,
            textAlign = TextAlign.Center
        )

        Spacer(modifier = Modifier.height(8.dp))

        Text(
            text = sign.displayDe,
            style = headlineStyle(17),
            color = Color.Gray,
            textAlign = TextAlign.Center
        )

        Spacer(modifier = Modifier.height(14.dp))

        Row(
            horizontalArrangement = Arrangement.spacedBy(10.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            if (!sign.stvoCode.isNullOrBlank() && sign.stvoCode != "—") {
                Row(
                    modifier = Modifier
                        .clip(CircleShape)
                        .background(style.copy(alpha = 0.12f))
                        .padding(horizontal = 12.dp, vertical = 6.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Icon(
                        imageVector = Icons.Filled.Description,
                        contentDescription = null,
                        tint = style,
                        modifier = Modifier.size(14.dp)
                    )
                    Spacer(modifier = Modifier.width(4.dp))
                    Text(
                        text = "StVO ${sign.stvoCode}",
                        style = captionStyle(11),
                        color = style
                    )
                }
            }
            if (categoryLabel.isNotBlank()) {
                Text(
                    text = categoryLabel,
                    style = captionStyle(11),
                    color = HighwayTeal,
                    modifier = Modifier
                        .clip(CircleShape)
                        .background(HighwayTeal.copy(alpha = 0.12f))
                        .padding(horizontal = 12.dp, vertical = 6.dp)
                )
            }
        }

        val note = sign.note(nativeLanguage)
        if (!note.isNullOrBlank()) {
            Spacer(modifier = Modifier.height(20.dp))
            AppCard(modifier = Modifier.fillMaxWidth(), accent = style) {
                Column(modifier = Modifier.padding(18.dp)) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Icon(
                            imageVector = Icons.Filled.Lightbulb,
                            contentDescription = null,
                            tint = RoadNavy,
                            modifier = Modifier.size(18.dp)
                        )
                        Spacer(modifier = Modifier.width(8.dp))
                        Text(
                            text = stringResource(R.string.signs_explanation),
                            style = headlineStyle(),
                            color = RoadNavy
                        )
                    }
                    Spacer(modifier = Modifier.height(10.dp))
                    Text(text = note, style = bodyStyle(15), color = Color.Gray)
                }
            }
        }

        Spacer(modifier = Modifier.height(14.dp))

        Box(
            modifier = Modifier
                .fillMaxWidth()
                .clip(RoundedCornerShape(16.dp))
                .background(HighwayTeal.copy(alpha = 0.06f))
                .padding(16.dp)
        ) {
            Column {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Text(text = "🇩🇪", style = captionStyle())
                    Spacer(modifier = Modifier.width(6.dp))
                    Text(
                        text = stringResource(R.string.signs_inGerman),
                        style = captionStyle(),
                        color = Color.Gray
                    )
                }
                Spacer(modifier = Modifier.height(8.dp))
                Text(text = sign.displayDe, style = bodyStyle(15), color = RoadNavy)
            }
        }

        Spacer(modifier = Modifier.height(20.dp))

        KnownMarkButton(isKnown = isKnown) {
            if (isKnown) {
                container.knownUndo.dismiss()
                container.setSignKnown(sign.id, false)
            } else {
                container.markSignAsKnown(sign.id, undoMessage)
            }
        }

        Spacer(modifier = Modifier.height(32.dp))
    }
}

@Composable
private fun SignImageCard(imageName: String?, tint: Color) {
    val context = LocalContext.current
    val bitmap = remember(imageName) {
        imageName?.let { name ->
            runCatching {
                context.assets.open("Signs/$name").use { stream ->
                    android.graphics.BitmapFactory.decodeStream(stream)
                }
            }.getOrNull()
        }
    }

    Box(
        modifier = Modifier
            .size(180.dp)
            .shadow(
                elevation = 16.dp,
                shape = RoundedCornerShape(24.dp),
                ambientColor = AppTheme.cardShadow,
                spotColor = AppTheme.cardShadow
            )
            .clip(RoundedCornerShape(24.dp))
            .background(Color.White),
        contentAlignment = Alignment.Center
    ) {
        if (bitmap != null) {
            Image(
                bitmap = bitmap.asImageBitmap(),
                contentDescription = null,
                contentScale = ContentScale.Fit,
                modifier = Modifier.size(140.dp)
            )
        } else {
            Icon(
                imageVector = SignStyle.categoryIcon(""),
                contentDescription = null,
                tint = tint,
                modifier = Modifier.size(72.dp)
            )
        }
    }
}
