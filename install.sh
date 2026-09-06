#!/usr/bin/env bash
# Slipstream for Jellyfin -- installer.
#
# Patches the Jellyfin web client inside your Docker container: builds the
# JS/CSS payload, verifies it parses, copies it in, and (optionally) installs a
# cron job that re-applies it after a container update wipes the web root.
#
# Everything it touches is reversible with ./uninstall.sh.
set -euo pipefail

CONTAINER="${CONTAINER:-}"
DO_CRON=0
DO_CSS=0
ASSUME_YES=0
FORCE=0
DO_PLUGINS=0
JF_URL="${JELLYFIN_URL:-}"
JF_KEY="${JELLYFIN_API_KEY:-}"
WEBROOT=""

say()  { printf '  %s\n' "$*"; }
ok()   { printf '  \033[32m✓\033[0m %s\n' "$*"; }
warn() { printf '  \033[33m!\033[0m %s\n' "$*"; }
die()  { printf '\n  \033[31m✗ %s\033[0m\n\n' "$*" >&2; exit 1; }

usage() {
  cat <<EOF
Slipstream for Jellyfin

  ./install.sh [options]

  --container NAME   Jellyfin container (default: auto-detect)
  --cron             also install a 10-minute re-apply cron job (recommended:
                     a Jellyfin image update resets the web root and undoes this)
  --write-css        write the stylesheet into Jellyfin's Custom CSS for you
                     (edits branding.xml and restarts the container)
  --plugins          add the plugin repositories and install the plugins this
                     UI expects. Needs --jellyfin-url and --api-key (or the
                     JELLYFIN_URL / JELLYFIN_API_KEY environment variables).
                     Create a key in Dashboard > API Keys.
  --force            rebuild even if the deployed build is current
  --yes              do not prompt
  -h, --help         this message
EOF
}

while [ $# -gt 0 ]; do
  case "$1" in
    --container) CONTAINER="${2:-}"; shift 2 ;;
    --cron)      DO_CRON=1; shift ;;
    --write-css) DO_CSS=1; shift ;;
    --yes|-y)    ASSUME_YES=1; shift ;;
    --force)     FORCE=1; shift ;;
    --plugins)   DO_PLUGINS=1; shift ;;
    --jellyfin-url) JF_URL="${2:-}"; shift 2 ;;
    --api-key)   JF_KEY="${2:-}"; shift 2 ;;
    -h|--help)   usage; exit 0 ;;
    *) die "unknown option: $1 (try --help)" ;;
  esac
done

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
printf '\n  \033[1mSlipstream for Jellyfin\033[0m\n\n'

# ---------------------------------------------------------------- 1. deps
for c in docker python3; do
  command -v "$c" >/dev/null 2>&1 || die "'$c' is required but not on PATH."
done
docker info >/dev/null 2>&1 || die "cannot talk to Docker. Run as a user in the docker group, or with sudo."
HAVE_NODE=0
command -v node >/dev/null 2>&1 && HAVE_NODE=1
[ "$HAVE_NODE" = 1 ] || warn "node not found -- skipping the JS syntax check (install Node to enable it)."
ok "dependencies"

# ------------------------------------------------------- 2. find container
if [ -z "$CONTAINER" ]; then
  CONTAINER="$(docker ps --format '{{.Names}}\t{{.Image}}' \
    | awk 'tolower($0) ~ /jellyfin/ {print $1; exit}')"
fi
[ -n "$CONTAINER" ] || die "no running Jellyfin container found. Pass --container NAME."
docker exec "$CONTAINER" true 2>/dev/null || die "container '$CONTAINER' is not running."
ok "container: $CONTAINER"

# --------------------------------------------------------- 3. find webroot
for p in /jellyfin/jellyfin-web /usr/share/jellyfin/web /app/jellyfin/jellyfin-web /usr/lib/jellyfin/bin/jellyfin-web; do
  if docker exec "$CONTAINER" test -f "$p/index.html" 2>/dev/null; then WEBROOT="$p"; break; fi
done
[ -n "$WEBROOT" ] || die "could not locate jellyfin-web/index.html inside '$CONTAINER'."
ok "web root: $WEBROOT"

# ------------------------------------------------------------- 4. back up
# The pristine index.html is the one thing that cannot be regenerated, so it is
# kept forever under backups/original/. Later runs do NOT make a new copy --
# with --cron this runs every 10 minutes and would otherwise fill the disk.
mkdir -p "$HERE/backups"
ORIG="$HERE/backups/original/index.html"
CUR="$(mktemp)"
trap 'rm -f "$CUR"' EXIT
docker cp "$CONTAINER:$WEBROOT/index.html" "$CUR" >/dev/null
[ -s "$CUR" ] || die "read of index.html came back empty -- refusing to continue."

SRC_HTML=""
if [ -f "$ORIG" ]; then
  ok "original index.html already saved"
  SRC_HTML="$ORIG"
elif grep -q 'window.SF_CONFIG' "$CUR"; then
  # Already patched, but the pristine copy is gone (a re-clone, usually). Every
  # block strips its own previous version before injecting, so re-patching a
  # patched file is safe and idempotent -- it is just not a backup we can
  # restore from, so do not record it as "original".
  warn "index.html is already patched and backups/original/ is missing."
  say  "rebuilding in place. To fully revert later you will need:"
  say  "    docker compose up -d --force-recreate $CONTAINER"
  mkdir -p "$HERE/backups"
  cp "$CUR" "$HERE/backups/patched-$(date +%Y%m%d-%H%M%S).html"
  SRC_HTML="$CUR"
else
  mkdir -p "$HERE/backups/original"
  cp "$CUR" "$ORIG"
  ok "saved the original index.html -> backups/original/ ($(wc -c <"$ORIG" | tr -d ' ') bytes)"
  SRC_HTML="$ORIG"
fi

# Fast path for the cron job: if the deployed build already matches what this
# checkout would produce, there is nothing to do and nothing to download.
BUILD_ID="$(cat "$HERE/build/jf_patch.py" "$HERE"/build/jfblocks/*.py 2>/dev/null | shasum | cut -c1-12)"
SKIP_BUILD=0
if [ "$FORCE" = 0 ] \
   && docker exec "$CONTAINER" test -f "$WEBROOT/sf-livesports.js" 2>/dev/null \
   && docker exec "$CONTAINER" grep -q "slipstream-build:$BUILD_ID" "$WEBROOT/index.html" 2>/dev/null; then
  SKIP_BUILD=1
  ok "already up to date (build $BUILD_ID)"
fi

if [ "$SKIP_BUILD" = 0 ]; then
# ------------------------------------------------- 5. third-party stylesheets
# These are NOT redistributed with Slipstream. They are fetched from their own
# upstreams at install time so their authors keep their licences and credit.
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"; rm -f "$CUR"' EXIT

ABYSS_URL="https://cdn.jsdelivr.net/gh/AumGupta/abyss-jellyfin@main/abyss.css"
if curl -fsSL --max-time 30 "$ABYSS_URL" -o "$TMP/abyss.css" && [ -s "$TMP/abyss.css" ]; then
  grep -q -- '--abyss-accent' "$TMP/abyss.css" \
    || die "downloaded abyss.css does not define --abyss-accent; refusing to install a broken theme."
  docker exec "$CONTAINER" mkdir -p "$WEBROOT/theme"
  docker cp "$TMP/abyss.css" "$CONTAINER:$WEBROOT/theme/abyss.css" >/dev/null
  docker exec "$CONTAINER" chmod 644 "$WEBROOT/theme/abyss.css"
  ok "Abyss theme installed ($(wc -c <"$TMP/abyss.css" | tr -d ' ') bytes, AumGupta/abyss-jellyfin)"
else
  die "could not download the Abyss theme. The stylesheet @imports it; without it the UI is unstyled."
fi

# Media Bar's own stylesheet, served locally so a CDN outage cannot leave the
# hero unstyled (which makes the home rows overlap it).
MB_URL="https://cdn.jsdelivr.net/gh/IAmParadox27/jellyfin-plugin-media-bar@2.4.12.0/slideshowpure.css"
if curl -fsSL --max-time 30 "$MB_URL" -o "$TMP/sf-mediabar.css" && [ -s "$TMP/sf-mediabar.css" ]; then
  docker cp "$TMP/sf-mediabar.css" "$CONTAINER:$WEBROOT/sf-mediabar.css" >/dev/null
  docker exec "$CONTAINER" chmod 644 "$WEBROOT/sf-mediabar.css"
  ok "Media Bar stylesheet installed (optional plugin, IAmParadox27)"
else
  warn "could not fetch the Media Bar stylesheet -- fine unless you use that plugin."
fi

# ------------------------------------------------------------- 6. build
cp "$SRC_HTML" "$TMP/index.html"
rm -f "$CUR"
SF_JS_OUT="$TMP/sf-livesports.js" python3 "$HERE/build/jf_patch.py" "$TMP/index.html" >"$TMP/build.log" 2>&1 \
  || { cat "$TMP/build.log"; die "the build failed (see the output above)."; }
BLOCKS="$(grep -c '^patched:' "$TMP/build.log" || true)"
[ -s "$TMP/sf-livesports.js" ] || die "the build produced no sf-livesports.js."
ok "built $BLOCKS blocks + sf-livesports.js ($(wc -c <"$TMP/sf-livesports.js" | tr -d ' ') bytes)"

# --------------------------------------------------------- 7. verify syntax
# A syntax error here does not throw an error the user can see -- it silently
# kills the WHOLE custom UI. Never deploy an unverified build.
if [ "$HAVE_NODE" = 1 ]; then
  node --check "$TMP/sf-livesports.js" >/dev/null 2>&1 \
    || die "generated JavaScript does not parse -- refusing to deploy. Nothing was changed."
  ok "syntax check passed"
fi
grep -q '</body>' "$TMP/index.html" || die "generated index.html looks malformed."
# stamp the build id so a later run can detect "already up to date"
printf '%s' "$(sed "s|</body>|<!-- slipstream-build:$BUILD_ID --></body>|" "$TMP/index.html")" > "$TMP/index.stamped"
mv "$TMP/index.stamped" "$TMP/index.html"

# ------------------------------------------------------------- 8. deploy
docker cp "$TMP/sf-livesports.js" "$CONTAINER:$WEBROOT/sf-livesports.js" >/dev/null
docker exec "$CONTAINER" chmod 644 "$WEBROOT/sf-livesports.js"
docker cp "$TMP/index.html" "$CONTAINER:$WEBROOT/index.html" >/dev/null
docker exec "$CONTAINER" chmod 644 "$WEBROOT/index.html"
ok "deployed to $CONTAINER"
fi   # SKIP_BUILD

# -------------------------------------------------------------- 9. the CSS
CSS="$HERE/assets/slipstream.css"
if [ "$DO_CSS" = 1 ]; then
  CFG_DIR="$(docker inspect -f '{{range .Mounts}}{{if eq .Destination "/config"}}{{.Source}}{{end}}{{end}}' "$CONTAINER" 2>/dev/null || true)"
  BRAND=""
  if [ -n "$CFG_DIR" ] && [ -d "$CFG_DIR/config" ]; then
    BRAND="$CFG_DIR/config/branding.xml"
    # Jellyfin only writes branding.xml once branding has been saved in the
    # dashboard, so on a fresh server it does not exist yet. Create a valid
    # empty one rather than telling the user to go and click Save first.
    if [ ! -f "$BRAND" ]; then
      cat > "$BRAND" <<'XML'
<?xml version="1.0" encoding="utf-8"?>
<BrandingOptions xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
  <LoginDisclaimer />
  <CustomCss></CustomCss>
  <SplashscreenEnabled>false</SplashscreenEnabled>
</BrandingOptions>
XML
      ok "created branding.xml (Jellyfin had not written one yet)"
    fi
  fi
  if [ -n "$BRAND" ]; then
    mkdir -p "$HERE/backups/original"
    [ -f "$HERE/backups/original/branding.xml" ] || cp "$BRAND" "$HERE/backups/original/branding.xml"
    python3 - "$BRAND" "$CSS" <<'PY'
import sys, html, re
brand, css = sys.argv[1], sys.argv[2]
body = open(css, encoding='utf-8').read()
doc  = open(brand, encoding='utf-8').read()
esc  = html.escape(body, quote=False)
# NB: the replacement must be a FUNCTION. CSS is full of escape sequences
# (content:"\e5cd"), and re.sub interprets backslashes in a string replacement
# -- which raises "bad escape \e" and, worse, would silently corrupt others.
new = '<CustomCss>' + esc + '</CustomCss>'
if '<CustomCss>' in doc:
    doc = re.sub(r'<CustomCss\s*/>|<CustomCss>.*?</CustomCss>', lambda m: new, doc, flags=re.S)
else:
    doc = re.sub(r'(<BrandingOptions[^>]*>)', lambda m: m.group(1) + new, doc, count=1)
open(brand, 'w', encoding='utf-8').write(doc)
PY
    ok "wrote Custom CSS into branding.xml (backup in backups/original/)"
    docker restart "$CONTAINER" >/dev/null && ok "restarted $CONTAINER"
  else
    warn "could not find branding.xml -- paste the CSS manually (see below)."
    DO_CSS=0
  fi
fi

# ------------------------------------------------------------ 9b. plugins
if [ "$DO_PLUGINS" = 1 ]; then
  if [ -z "$JF_URL" ] || [ -z "$JF_KEY" ]; then
    warn "--plugins needs --jellyfin-url and --api-key (Dashboard > API Keys)."
    say  "    ./install.sh --plugins --jellyfin-url http://localhost:8096 --api-key KEY"
  elif [ ! -f "$HERE/plugins.json" ]; then
    warn "plugins.json is missing -- skipping plugin setup."
  else
    # The key is read from the argument/environment and used only against the
    # server you named. It is never written to disk by this script.
    python3 "$HERE/tools/plugins.py" "$JF_URL" "$JF_KEY" "$HERE/plugins.json" || \
      warn "plugin setup did not complete -- see the messages above."
  fi
fi

# ------------------------------------------------------------- 10. cron
if [ "$DO_CRON" = 1 ]; then
  LINE="*/10 * * * * CONTAINER=$CONTAINER $HERE/install.sh --yes >/dev/null 2>&1"
  if ! command -v crontab >/dev/null 2>&1; then
    warn "no crontab on this host -- add this line to your scheduler yourself:"
    say  "    $LINE"
  elif crontab -l 2>/dev/null | grep -Fq "$HERE/install.sh"; then
    ok "cron job already present"
  else
    # On macOS this can block on a Full Disk Access prompt, so never let the
    # installer hang on it -- print the line and move on if it does not return.
    if ( crontab -l 2>/dev/null; echo "$LINE" ) | crontab - 2>/dev/null; then
      ok "installed a 10-minute re-apply cron job"
    else
      warn "could not write crontab. Add this line yourself:"
      say  "    $LINE"
    fi
  fi
fi

printf '\n  \033[1mDone.\033[0m\n\n'
if [ "$DO_CSS" != 1 ]; then
  cat <<EOF
  One step left -- the stylesheet:

    1. Open  Dashboard > General > Custom CSS
    2. Paste the contents of:
         assets/slipstream.css
    3. Save, then hard-refresh your browser (Ctrl/Cmd-Shift-R)

  (or re-run with --write-css to have this done for you)

EOF
else
  say "Hard-refresh your browser (Ctrl/Cmd-Shift-R)."
  echo
fi
