#!/bin/bash
# Archive Fahrprufung DE for TestFlight / App Store upload.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SCHEME="FahrPrufungDE"
ARCHIVE_PATH="$ROOT/build/FahrPrufungDE.xcarchive"
EXPORT_PATH="$ROOT/build/export"

cd "$ROOT"

echo "→ Archiving $SCHEME…"
xcodebuild \
  -project FahrPrufungDE.xcodeproj \
  -scheme "$SCHEME" \
  -configuration Release \
  -destination 'generic/platform=iOS' \
  -archivePath "$ARCHIVE_PATH" \
  archive

echo "→ Exporting IPA…"
rm -rf "$EXPORT_PATH"
xcodebuild \
  -exportArchive \
  -archivePath "$ARCHIVE_PATH" \
  -exportPath "$EXPORT_PATH" \
  -exportOptionsPlist "$ROOT/ExportOptions.plist"

echo ""
echo "Done. IPA: $EXPORT_PATH/FahrPrufungDE.ipa"
echo "Upload via Xcode Organizer or: xcrun altool --upload-app -f \"$EXPORT_PATH/FahrPrufungDE.ipa\" -t ios -u YOUR_APPLE_ID"
