# Side-by-side QA 2026-10-04T23:11:09Z
- PASS: Android installed emu=92554
- PASS: Cold start no FATAL
- FAIL: Onboarding 
- PASS: a_01_home.png   537245
- PASS: a_02_settings.png   512118
- PASS: settings scrolled
- PASS: a_03_progress.png   206677
- PASS: a_04_quiz.png   537917
- PASS: a_05_flashcards.png   152060
- PASS: a_06_signs.png   302636
- PASS: a_07_examiner.png   354949
- PASS: a_08_categories.png   270336
- PASS: home ru   543304
- PASS: home uk   529173
- PASS: home fr   545978
- PASS: home tr   524010
- PASS: Privacy URL
- PASS: No PrapoDe

## Screenshot sanity
- OK: a_01_home.png uniq=153 avg=(203, 209, 211)
- OK: a_02_settings.png uniq=155 avg=(203, 209, 211)
- OK: a_02b_settings_scrolled.png uniq=68 avg=(243, 241, 236)
- OK: a_03_progress.png uniq=54 avg=(243, 241, 237)
- OK: a_04_quiz.png uniq=154 avg=(203, 209, 211)
- OK: a_05_flashcards.png uniq=46 avg=(247, 245, 241)
- OK: a_06_signs.png uniq=65 avg=(241, 238, 236)
- OK: a_07_examiner.png uniq=75 avg=(237, 233, 231)
- OK: a_08_categories.png uniq=69 avg=(245, 242, 237)
- OK: a_home_fr.png uniq=149 avg=(202, 209, 210)
- OK: a_home_ru.png uniq=151 avg=(203, 209, 210)
- OK: a_home_tr.png uniq=150 avg=(204, 210, 211)
- OK: a_home_uk.png uniq=151 avg=(203, 209, 210)
- PASS: iOS i_01_home.png  1936710
- PASS: iOS i_02_quiz.png   813605
- PASS: iOS i_03_settings.png  1584091
- PASS: iOS i_03b_privacy.png  1362698
- PASS: iOS i_04_progress.png  1261976

## Follow-up checks
- PASS: Quiz deep-link works (retry shot shows Question 1/10)
- PASS: Onboarding capture   194661
- PASS: assembleRelease SUCCESS
total 51944
drwxr-xr-x@ 5 test  staff       160 Oct  5 01:26 .
drwxr-xr-x@ 4 test  staff       128 Oct  5 01:26 ..
-rw-r--r--@ 1 test  staff  26589686 Oct  5 01:26 app-release-unsigned.apk
drwxr-xr-x@ 4 test  staff       128 Oct  5 01:26 baselineProfiles
-rw-r--r--@ 1 test  staff       735 Oct  5 01:26 output-metadata.json
- WARN: No signingConfigs in build.gradle.kts — need upload keystore / Play App Signing
- WARN: versionCode=1 versionName=1.0.0 — OK for first Play upload
- WARN: Declare Advertising ID in Play Console (Firebase Analytics)
- PASS: INTERNET + Privacy Policy + no PrapoDe

## Intentional vs iOS
- PrapoDe: iOS only (OK)
- Tab icons: Material vs SF Symbols (OK)
EMU_STOPPED
