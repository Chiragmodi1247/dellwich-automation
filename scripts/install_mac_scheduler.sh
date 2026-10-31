#!/bin/bash
# Run the link opener in the background every N minutes on macOS (default 30).
#
#   ./scripts/install_mac_scheduler.sh          # every 30 minutes
#   ./scripts/install_mac_scheduler.sh 15       # every 15 minutes
#   ./scripts/install_mac_scheduler.sh uninstall
#
# Each run reads links.txt from GitHub, so pushing changes to the repo updates
# what opens. If GitHub can't be reached, it falls back to a local copy.
set -euo pipefail

LABEL="com.chirag.dellwich-links"
PLIST="$HOME/Library/LaunchAgents/$LABEL.plist"
APP_DIR="$HOME/Library/Application Support/dellwich-automation"
LOG="$APP_DIR/run.log"
REMOTE_LINKS="https://raw.githubusercontent.com/Chiragmodi1247/dellwich-automation/main/public/links.txt"
REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"

if [[ "${1:-}" == "uninstall" ]]; then
  launchctl bootout "gui/$(id -u)/$LABEL" 2>/dev/null || true
  rm -f "$PLIST"
  echo "Removed the background job. (Files in $APP_DIR were kept.)"
  exit 0
fi

MINUTES="${1:-30}"
[[ "$MINUTES" =~ ^[0-9]+$ && "$MINUTES" -ge 1 ]] || { echo "Minutes must be a positive number."; exit 1; }
PYTHON="$(command -v python3)"

# Copy the files out of ~/Desktop: macOS often blocks background jobs from reading it.
mkdir -p "$APP_DIR"
cp "$REPO_DIR/scripts/open_links_in_chrome.py" "$APP_DIR/"
cp "$REPO_DIR/public/links.txt" "$APP_DIR/links.txt"

cat > "$PLIST" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>$LABEL</string>

    <key>ProgramArguments</key>
    <array>
        <string>$PYTHON</string>
        <string>$APP_DIR/open_links_in_chrome.py</string>
        <string>$REMOTE_LINKS</string>
        <string>$APP_DIR/links.txt</string>
    </array>

    <key>StartInterval</key>
    <integer>$((MINUTES * 60))</integer>

    <key>StandardOutPath</key>
    <string>$LOG</string>

    <key>StandardErrorPath</key>
    <string>$LOG</string>

    <key>RunAtLoad</key>
    <false/>
</dict>
</plist>
EOF

launchctl bootout "gui/$(id -u)/$LABEL" 2>/dev/null || true
launchctl bootstrap "gui/$(id -u)" "$PLIST"

echo "Installed: links open every $MINUTES minutes."
echo "Run now:   launchctl kickstart gui/$(id -u)/$LABEL"
echo "Log:       $LOG"
echo "Remove:    ./scripts/install_mac_scheduler.sh uninstall"
