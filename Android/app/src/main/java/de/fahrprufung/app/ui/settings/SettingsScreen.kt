package de.fahrprufung.app.ui.settings

import android.content.Intent
import android.net.Uri
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.statusBarsPadding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.TrendingUp
import androidx.compose.material.icons.filled.Book
import androidx.compose.material.icons.filled.CheckCircle
import androidx.compose.material.icons.filled.ChevronRight
import androidx.compose.material.icons.filled.Email
import androidx.compose.material.icons.filled.Favorite
import androidx.compose.material.icons.filled.Folder
import androidx.compose.material.icons.filled.Info
import androidx.compose.material.icons.filled.Lock
import androidx.compose.material.icons.filled.Refresh
import androidx.compose.material.icons.filled.Replay
import androidx.compose.material.icons.filled.Settings
import androidx.compose.material.icons.filled.Signpost
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.Icon
import androidx.compose.material3.Switch
import androidx.compose.material3.SwitchDefaults
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.unit.dp
import de.fahrprufung.app.R
import de.fahrprufung.app.data.AppContainer
import de.fahrprufung.app.theme.AppTheme
import de.fahrprufung.app.theme.HighwayTeal
import de.fahrprufung.app.theme.RoadNavy
import de.fahrprufung.app.theme.SignalAmber
import de.fahrprufung.app.theme.SignalGreen
import de.fahrprufung.app.theme.SignalRed
import de.fahrprufung.app.theme.bodyStyle
import de.fahrprufung.app.theme.captionStyle
import de.fahrprufung.app.theme.headlineStyle
import de.fahrprufung.app.theme.titleStyle
import de.fahrprufung.app.ui.components.AppCard
import de.fahrprufung.app.ui.components.AppScreenBackground
import de.fahrprufung.app.ui.components.InfoTile
import de.fahrprufung.app.ui.components.LanguagePickerRow
import de.fahrprufung.app.ui.components.SectionHeader

private const val PRIVACY_POLICY_URL = "https://eclectic-concha-6a3c68.netlify.app/privacy-policy.html"
private const val CONTACT_EMAIL = "appentwickler2025@gmail.com"

@Composable
fun SettingsScreen(
    container: AppContainer,
    onOpenProgress: () -> Unit
) {
    val context = LocalContext.current
    val nativeLanguage by container.nativeLanguage.collectAsState()
    val terms by container.content.terms.collectAsState()
    val categories by container.content.categories.collectAsState()
    val signs by container.content.signs.collectAsState()
    val knownTermIds by container.knownTermIds.collectAsState()
    val knownSignIds by container.knownSignIds.collectAsState()
    val analyticsEnabled by container.analyticsEnabled.collectAsState()

    var showResetDialog by remember { mutableStateOf(false) }
    val hasKnownItems = knownTermIds.isNotEmpty() || knownSignIds.isNotEmpty()

    AppScreenBackground {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .statusBarsPadding()
                .verticalScroll(rememberScrollState())
                .padding(horizontal = 20.dp)
        ) {
            Spacer(modifier = Modifier.height(16.dp))

            SettingsHeroHeader()

            Spacer(modifier = Modifier.height(20.dp))

            LanguagePickerRow(
                selection = nativeLanguage,
                onSelect = { container.setNativeLanguage(it) }
            )

            Spacer(modifier = Modifier.height(12.dp))

            AppCard(
                modifier = Modifier
                    .fillMaxWidth()
                    .clickable(onClick = onOpenProgress),
                accent = HighwayTeal
            ) {
                Row(
                    modifier = Modifier
                        .padding(16.dp)
                        .fillMaxWidth(),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Icon(
                        imageVector = Icons.AutoMirrored.Filled.TrendingUp,
                        contentDescription = null,
                        tint = HighwayTeal
                    )
                    Spacer(modifier = Modifier.width(12.dp))
                    Text(
                        text = stringResource(R.string.settings_viewProgress),
                        style = bodyStyle(15),
                        color = RoadNavy,
                        modifier = Modifier.weight(1f)
                    )
                    Icon(
                        imageVector = Icons.Filled.ChevronRight,
                        contentDescription = null,
                        tint = Color.Gray
                    )
                }
            }

            SectionHeader(title = stringResource(R.string.settings_statistics))

            Row(modifier = Modifier.fillMaxWidth()) {
                InfoTile(
                    value = terms.size.toString(),
                    label = stringResource(R.string.settings_terms),
                    icon = Icons.Filled.Book,
                    color = HighwayTeal,
                    modifier = Modifier.weight(1f)
                )
                Spacer(modifier = Modifier.width(12.dp))
                InfoTile(
                    value = categories.size.toString(),
                    label = stringResource(R.string.settings_categories),
                    icon = Icons.Filled.Folder,
                    color = RoadNavy,
                    modifier = Modifier.weight(1f)
                )
            }

            Spacer(modifier = Modifier.height(12.dp))

            InfoTile(
                value = signs.size.toString(),
                label = stringResource(R.string.settings_signs),
                icon = Icons.Filled.Signpost,
                color = SignalAmber,
                wide = true
            )

            if (hasKnownItems) {
                SectionHeader(
                    title = stringResource(R.string.known_settingsSection),
                    icon = Icons.Filled.CheckCircle
                )

                if (knownTermIds.isNotEmpty()) {
                    KnownStatRow(
                        count = knownTermIds.size,
                        label = stringResource(R.string.known_termsMarked)
                    )
                    Spacer(modifier = Modifier.height(8.dp))
                }
                if (knownSignIds.isNotEmpty()) {
                    KnownStatRow(
                        count = knownSignIds.size,
                        label = stringResource(R.string.known_signsMarked)
                    )
                    Spacer(modifier = Modifier.height(8.dp))
                }

                AppCard(
                    modifier = Modifier
                        .fillMaxWidth()
                        .clickable { showResetDialog = true },
                    accent = SignalGreen
                ) {
                    Row(
                        modifier = Modifier.padding(16.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Icon(
                            imageVector = Icons.Filled.Refresh,
                            contentDescription = null,
                            tint = SignalGreen
                        )
                        Spacer(modifier = Modifier.width(12.dp))
                        Text(
                            text = stringResource(R.string.known_resetTitle),
                            style = bodyStyle(15),
                            color = RoadNavy
                        )
                    }
                }
            }

            Spacer(modifier = Modifier.height(12.dp))

            AppCard(modifier = Modifier.fillMaxWidth(), accent = RoadNavy) {
                Row(
                    modifier = Modifier
                        .padding(16.dp)
                        .fillMaxWidth(),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Column(modifier = Modifier.weight(1f)) {
                        Text(
                            text = stringResource(R.string.settings_analytics),
                            style = bodyStyle(15),
                            color = RoadNavy
                        )
                        Text(
                            text = stringResource(R.string.settings_analyticsSubtitle),
                            style = captionStyle(12),
                            color = Color.Gray
                        )
                    }
                    Switch(
                        checked = analyticsEnabled,
                        onCheckedChange = { container.setAnalyticsEnabled(it) },
                        colors = SwitchDefaults.colors(checkedTrackColor = SignalGreen)
                    )
                }
            }

            Spacer(modifier = Modifier.height(10.dp))

            SettingsActionRow(
                icon = Icons.Filled.Replay,
                title = stringResource(R.string.settings_replayOnboarding),
                color = HighwayTeal,
                onClick = { container.setHasCompletedOnboarding(false) }
            )
            SettingsActionRow(
                icon = Icons.Filled.Email,
                title = stringResource(R.string.settings_contactDeveloper),
                color = RoadNavy,
                onClick = { openEmail(context) }
            )
            SettingsActionRow(
                icon = Icons.Filled.Lock,
                title = stringResource(R.string.settings_privacyPolicy),
                color = RoadNavy,
                onClick = { openUrl(context, PRIVACY_POLICY_URL) }
            )

            Spacer(modifier = Modifier.height(10.dp))

            AppCard(modifier = Modifier.fillMaxWidth(), accent = RoadNavy) {
                Column(modifier = Modifier.padding(16.dp)) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Icon(
                            imageVector = Icons.Filled.Info,
                            contentDescription = null,
                            tint = RoadNavy,
                            modifier = Modifier.size(18.dp)
                        )
                        Spacer(modifier = Modifier.width(8.dp))
                        Text(
                            text = stringResource(R.string.settings_disclaimerTitle),
                            style = headlineStyle(14),
                            color = RoadNavy
                        )
                    }
                    Spacer(modifier = Modifier.height(8.dp))
                    Text(
                        text = stringResource(R.string.settings_disclaimer),
                        style = bodyStyle(13),
                        color = Color.Gray
                    )
                }
            }

            Spacer(modifier = Modifier.height(10.dp))

            AppCard(modifier = Modifier.fillMaxWidth(), accent = SignalAmber) {
                Column(modifier = Modifier.padding(16.dp)) {
                    Icon(
                        imageVector = Icons.Filled.Favorite,
                        contentDescription = null,
                        tint = SignalRed.copy(alpha = 0.7f),
                        modifier = Modifier.size(20.dp)
                    )
                    Spacer(modifier = Modifier.height(8.dp))
                    Text(
                        text = stringResource(R.string.settings_about),
                        style = bodyStyle(14),
                        color = Color.Gray
                    )
                }
            }

            Spacer(modifier = Modifier.height(120.dp))
        }
    }

    if (showResetDialog) {
        AlertDialog(
            onDismissRequest = { showResetDialog = false },
            title = { Text(stringResource(R.string.known_resetConfirmTitle)) },
            text = { Text(stringResource(R.string.known_resetConfirmMessage)) },
            confirmButton = {
                TextButton(onClick = {
                    container.resetKnownItems()
                    showResetDialog = false
                }) {
                    Text(stringResource(R.string.known_resetConfirm), color = SignalRed)
                }
            },
            dismissButton = {
                TextButton(onClick = { showResetDialog = false }) {
                    Text(stringResource(R.string.known_cancel))
                }
            }
        )
    }
}

@Composable
private fun SettingsHeroHeader() {
    Box(
        modifier = Modifier
            .fillMaxWidth()
            .height(120.dp)
            .clip(RoundedCornerShape(24.dp))
            .background(AppTheme.heroGradient)
    ) {
        Column(
            modifier = Modifier
                .align(Alignment.BottomStart)
                .padding(24.dp)
        ) {
            Icon(
                imageVector = Icons.Filled.Settings,
                contentDescription = null,
                tint = Color.White.copy(alpha = 0.8f),
                modifier = Modifier.size(28.dp)
            )
            Spacer(modifier = Modifier.height(6.dp))
            Text(
                text = stringResource(R.string.settings_title),
                style = titleStyle(26),
                color = Color.White
            )
        }
    }
}

@Composable
private fun KnownStatRow(count: Int, label: String) {
    AppCard(modifier = Modifier.fillMaxWidth(), accent = SignalGreen) {
        Row(
            modifier = Modifier.padding(horizontal = 16.dp, vertical = 12.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Text(text = count.toString(), style = headlineStyle(18), color = SignalGreen)
            Spacer(modifier = Modifier.width(8.dp))
            Text(text = label, style = bodyStyle(14), color = Color.Gray)
        }
    }
}

@Composable
private fun SettingsActionRow(
    icon: androidx.compose.ui.graphics.vector.ImageVector,
    title: String,
    color: Color,
    onClick: () -> Unit
) {
    AppCard(
        modifier = Modifier
            .fillMaxWidth()
            .clickable(onClick = onClick),
        accent = color
    ) {
        Row(
            modifier = Modifier
                .padding(16.dp)
                .fillMaxWidth(),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Icon(imageVector = icon, contentDescription = null, tint = color, modifier = Modifier.size(20.dp))
            Spacer(modifier = Modifier.width(12.dp))
            Text(text = title, style = bodyStyle(15), color = RoadNavy, modifier = Modifier.weight(1f))
            Icon(
                imageVector = Icons.Filled.ChevronRight,
                contentDescription = null,
                tint = Color.Gray
            )
        }
    }
    Spacer(modifier = Modifier.height(10.dp))
}

private fun openUrl(context: android.content.Context, url: String) {
    runCatching {
        context.startActivity(Intent(Intent.ACTION_VIEW, Uri.parse(url)))
    }
}

private fun openEmail(context: android.content.Context) {
    runCatching {
        val intent = Intent(Intent.ACTION_SENDTO, Uri.parse("mailto:$CONTACT_EMAIL"))
        context.startActivity(intent)
    }
}
