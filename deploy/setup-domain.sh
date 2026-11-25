#!/usr/bin/env bash
# Install nginx + Let's Encrypt for arxiv261007152.piersonl.com
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
REMOTE_HOST="${REMOTE_HOST:-rack}"
SITE_NAME="arxiv261007152.piersonl.com"

chmod +x "$ROOT/deploy/setup-domain.sh" "$ROOT/deploy/deploy.sh"

echo "Checking DNS for ${SITE_NAME} → VPS..."
ssh "$REMOTE_HOST" "bash -c '
set -euo pipefail
VPS_IP=\$(hostname -I | awk \"{print \\\$1}\")
RESOLVED=\$(getent ahostsv4 ${SITE_NAME} | awk \"{print \\\$1; exit}\" || true)
echo \"VPS IP: \$VPS_IP\"
echo \"DNS  : \${RESOLVED:-<unresolved>}\"
if [[ -z \"\${RESOLVED:-}\" || \"\$RESOLVED\" != \"\$VPS_IP\" ]]; then
  echo \"ERROR: Point an A record for ${SITE_NAME} to \$VPS_IP, wait for DNS, then re-run.\"
  exit 1
fi
'"

scp "$ROOT/deploy/nginx.http-bootstrap.conf" \
  "${REMOTE_HOST}:/tmp/nginx-arxiv.http-bootstrap.conf"
scp "$ROOT/deploy/nginx.arxiv261007152.piersonl.com.conf" \
  "${REMOTE_HOST}:/tmp/nginx-arxiv.piersonl.com.conf"

ssh "$REMOTE_HOST" "bash -c '
set -euo pipefail
SITE_NAME=${SITE_NAME}

sudo mkdir -p /var/www/html /var/www/arxiv261007152
sudo cp /tmp/nginx-arxiv.http-bootstrap.conf /etc/nginx/sites-available/\${SITE_NAME}
sudo ln -sfn /etc/nginx/sites-available/\${SITE_NAME} /etc/nginx/sites-enabled/\${SITE_NAME}
sudo nginx -t
sudo systemctl reload nginx

sudo certbot certonly --webroot -w /var/www/html \
  -d \${SITE_NAME} \
  --non-interactive --agree-tos --keep-until-expiring \
  -m piersonlipschultz@gmail.com

sudo cp /tmp/nginx-arxiv.piersonl.com.conf /etc/nginx/sites-available/\${SITE_NAME}
sudo ln -sfn /etc/nginx/sites-available/\${SITE_NAME} /etc/nginx/sites-enabled/\${SITE_NAME}
sudo nginx -t
sudo systemctl reload nginx
echo \"nginx OK for \${SITE_NAME}\"
curl -sI https://\${SITE_NAME}/ | head -8 || true
'"

echo "TLS ready. https://${SITE_NAME}/"
