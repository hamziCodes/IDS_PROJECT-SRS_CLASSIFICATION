#!/bin/bash
# Strips simulator architectures from embedded frameworks inside the .app
# Usage: add this script as a Run Script build phase (before "Embed Frameworks").

set -e

APP_PATH="${TARGET_BUILD_DIR}/${WRAPPER_NAME}"

echo "Stripping simulator architectures from frameworks in $APP_PATH"

find "$APP_PATH" -name '*.framework' -type d | while read -r FRAMEWORK; do
  FRAMEWORK_EXECUTABLE_NAME=$(defaults read "$FRAMEWORK/Info.plist" CFBundleExecutable 2>/dev/null || basename "$FRAMEWORK" .framework)
  FRAMEWORK_EXECUTABLE_PATH="$FRAMEWORK/$FRAMEWORK_EXECUTABLE_NAME"
  if [ ! -f "$FRAMEWORK_EXECUTABLE_PATH" ]; then
    continue
  fi

  echo "Inspecting $FRAMEWORK_EXECUTABLE_PATH"
  ARCHS_RAW=$(lipo -info "$FRAMEWORK_EXECUTABLE_PATH" 2>/dev/null || true)
  echo "  lipo info: $ARCHS_RAW"

  # Remove Intel simulator slices
  for ARCH in i386 x86_64; do
    if lipo -info "$FRAMEWORK_EXECUTABLE_PATH" | grep -q "$ARCH"; then
      echo "  Removing $ARCH from $FRAMEWORK_EXECUTABLE_PATH"
      lipo -remove "$ARCH" -output "$FRAMEWORK_EXECUTABLE_PATH" "$FRAMEWORK_EXECUTABLE_PATH" || true
    fi
  done

  # If arm64 slice exists but seems simulator-only, attempt to thin if device slice not present
  if lipo -info "$FRAMEWORK_EXECUTABLE_PATH" | grep -q "arm64"; then
    # Check if file contains a device slice by trying to extract a device-specific architecture
    # There's no reliable way to detect simulator-vs-device arm64 slice via lipo alone.
    # We will keep arm64 but emit a warning so maintainers can produce an xcframework if needed.
    echo "  Found arm64 in $FRAMEWORK_EXECUTABLE_PATH - ensure this is a device slice (not simulator)."
  fi

done

echo "Strip script completed."
