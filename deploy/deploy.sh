#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
REMOTE_HOST="${REMOTE_HOST:-rack}"
REMOTE_DIR="${REMOTE_DIR:-/var/www/arxiv261007152}"
SITE_NAME="arxiv261007152.piersonl.com"

cd "$ROOT"
chmod +x deploy/deploy.sh deploy/setup-domain.sh

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

# Static explainer: index + referenced assets only
mkdir -p "$TMP/assets"
cp "$ROOT/index.html" "$TMP/"
cp "$ROOT/assets/astronomer-periodic-table.png" "$TMP/assets/"
cp "$ROOT/assets/crescent-nebula.jpg" "$TMP/assets/"
cp "$ROOT/assets/xrb.jpg" "$TMP/assets/"
cp "$ROOT/assets/roche-lobe.svg" "$TMP/assets/"

echo "Syncing to ${REMOTE_HOST}:${REMOTE_DIR}..."
ssh "$REMOTE_HOST" "mkdir -p ${REMOTE_DIR}/assets"
rsync -az --delete \
  --exclude ".git" \
  "$TMP/" "${REMOTE_HOST}:${REMOTE_DIR}/"

ssh "$REMOTE_HOST" "chown -R www-data:www-data ${REMOTE_DIR} && chmod 755 ${REMOTE_DIR} ${REMOTE_DIR}/assets && nginx -t && systemctl reload nginx"

echo "Deployed. https://${SITE_NAME}/"
curl -sI "https://${SITE_NAME}/" | head -12 || true
