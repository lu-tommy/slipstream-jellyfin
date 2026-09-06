#!/usr/bin/env bash
# Slipstream for Jellyfin -- uninstaller. Restores the original index.html,
# removes the files we added, and drops the cron job.
set -euo pipefail

CONTAINER="${CONTAINER:-}"
say()  { printf '  %s\n' "$*"; }
ok()   { printf '  \033[32m✓\033[0m %s\n' "$*"; }
warn() { printf '  \033[33m!\033[0m %s\n' "$*"; }
die()  { printf '\n  \033[31m✗ %s\033[0m\n\n' "$*" >&2; exit 1; }

[ "${1:-}" = "--container" ] && { CONTAINER="${2:-}"; shift 2; }
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
printf '\n  \033[1mUninstalling Slipstream\033[0m\n\n'

command -v docker >/dev/null 2>&1 || die "'docker' is required."
if [ -z "$CONTAINER" ]; then
  CONTAINER="$(docker ps --format '{{.Names}}\t{{.Image}}' | awk 'tolower($0) ~ /jellyfin/ {print $1; exit}')"
fi
[ -n "$CONTAINER" ] || die "no running Jellyfin container found. Pass --container NAME."

WEBROOT=""
for p in /jellyfin/jellyfin-web /usr/share/jellyfin/web /app/jellyfin/jellyfin-web /usr/lib/jellyfin/bin/jellyfin-web; do
  if docker exec "$CONTAINER" test -f "$p/index.html" 2>/dev/null; then WEBROOT="$p"; break; fi
done
[ -n "$WEBROOT" ] || die "could not locate jellyfin-web inside '$CONTAINER'."

ORIG="$HERE/backups/original/index.html"
if [ -f "$ORIG" ]; then
  docker cp "$ORIG" "$CONTAINER:$WEBROOT/index.html" >/dev/null
  docker exec "$CONTAINER" chmod 644 "$WEBROOT/index.html"
  ok "restored the original index.html"
else
  warn "no saved original found. Recreating the container will restore a clean web root:"
  say  "    docker compose up -d --force-recreate $CONTAINER"
fi

for f in sf-livesports.js sf-mediabar.css theme/abyss.css; do
  docker exec "$CONTAINER" rm -f "$WEBROOT/$f" 2>/dev/null && ok "removed $f" || true
done

BRAND_BK="$HERE/backups/original/branding.xml"
if [ -f "$BRAND_BK" ]; then
  CFG_DIR="$(docker inspect -f '{{range .Mounts}}{{if eq .Destination "/config"}}{{.Source}}{{end}}{{end}}' "$CONTAINER" 2>/dev/null || true)"
  if [ -n "$CFG_DIR" ] && [ -f "$CFG_DIR/config/branding.xml" ]; then
    cp "$BRAND_BK" "$CFG_DIR/config/branding.xml"
    ok "restored the original branding.xml (Custom CSS)"
    docker restart "$CONTAINER" >/dev/null && ok "restarted $CONTAINER"
  fi
else
  say "If you pasted the CSS by hand, clear Dashboard > General > Custom CSS."
fi

if crontab -l 2>/dev/null | grep -Fq "$HERE/install.sh"; then
  crontab -l 2>/dev/null | grep -Fv "$HERE/install.sh" | crontab -
  ok "removed the cron job"
fi

printf '\n  \033[1mDone.\033[0m Hard-refresh your browser.\n\n'
