# Slipstream for Jellyfin

The complete Jellyfin front-end setup I run at home, packaged so you can get
**the same thing** — built around **navigation that never blinks**.

Stock Jellyfin renders every route change as a hard swap: the old page is
hidden, the new one appears, and in between you get white flashes, rows that
slide in one at a time, a header that changes height, and a hero image that
re-fades every time you press Back. Slipstream replaces that with a single
motion system, a page lifecycle that holds nothing back, and a detail page laid
out like a streaming app instead of a database record.

It sits **on top of** the excellent [Abyss theme][abyss] — Abyss owns the
colours and glass; Slipstream owns the motion, the layout and the behaviour.

```
git clone https://github.com/lu-tommy/slipstream-jellyfin.git
cd slipstream-jellyfin
./install.sh --cron --write-css
```

That is the whole install: **91 patch blocks**, the stylesheet, and the theme.
Add `--plugins` and it will set up the plugins too.

---

## Contents

- [What it changes](#what-it-changes)
- [Requirements](#requirements)
- [Install](#install)
- [Plugins](#plugins)
- [The stylesheet](#the-stylesheet)
- [Keeping it through Jellyfin updates](#keeping-it-through-jellyfin-updates)
- [Configuration](#configuration)
- [Uninstall](#uninstall)
- [How it works](#how-it-works)
- [Companion services](#companion-services)
- [Troubleshooting](#troubleshooting)
- [Credits](#credits)
- [License](#license)

---

## What it changes

### Navigation and motion

The part most of the work went into.

- **One motion system.** Every entrance in the app runs off the same tokens —
  `--sf-dur`, `--sf-ease`, `--sf-lift`, `--sf-stagger` — instead of four
  competing animations. Change one variable, change the whole app.
- **No black gaps between pages.** Measured 0 ms of blank frame across
  repeated navigation, where stock showed a visible flash on most hops.
- **Back doesn't re-animate.** Returning to Home no longer re-fades the hero
  or replays the row entrance. Cached pages stay put.
- **Rows reveal together**, not one-by-one with the first row jumping.
- **A stable header.** The header no longer changes height depending on which
  route you are on.
- **`prefers-reduced-motion` is honoured** throughout.

### Detail pages (movies and shows)

- Laid out as **hero → actions → facts → plot → cast**, with the plot placed
  **below the first viewport** so the artwork gets a clean opening frame.
- On a series, the plot sits **above** seasons and episodes, where you'd
  actually read it.
- Seasons / episodes counts surface as metadata pills.
- The action row reveals as one unit instead of buttons popping in.
- Backdrops transition instead of cutting.

### Home

- Hero artwork is measure-based and works at any viewport.
- The hero's empty slide container no longer swallows your clicks.
- The loading skeleton is kept (removing it measurably *doubles* layout shift).
- Favourites pill becomes **My Stuff**.

### Player and mobile

- Subtitles stay above the control bar, in one uniform style.
- The mobile now-playing bar drops 110px → 84px and gets play/pause back.
- A paused tab can no longer rewind your saved position — a real data-loss bug
  in stock behaviour, where progress reports kept firing while paused and
  overwrote a newer position.
- Volume opens from the speaker button.
- Phone card controls are decluttered and themed.

### Music and audiobooks

- Full album page with the track list it never had.
- A full-screen audiobook player, chapter-aware controls, lock-screen
  metadata and 30-second seek.
- Music playlists filtered to audio; Album Artists folded into Artists.

### Search, requests and language

- Search results are re-ranked so an artist search returns that artist's own
  albums instead of covers and mashups, with a skeleton instead of a spinner.
- Optional request UI: search for something you don't have and request it,
  including "get everything by this artist" — needs the request bridge below.
- A full UI translation layer with a language toggle, plus per-user translated
  titles and plot summaries.

### Live TV

- A guide that filters to what you actually get, channel cards with artwork,
  "ends at" times on a 12-hour clock, and a resume path back into a live
  channel.

### Audiobooks

- A dedicated audiobook library treatment: shelves, chapter list, a
  full-screen player with speed, skip, sleep timer and auto-rewind, lock-screen
  metadata, and read-along when an aligned text is available.

The installer prints every block it applies — **91** of them.

---

## Requirements

| | |
|---|---|
| **Jellyfin** | 10.11.x — developed and tested against **10.11.11** |
| **Deployment** | Jellyfin running in **Docker** |
| **Host access** | a shell on the Docker host, with permission to run `docker` |
| **Tools** | `docker`, `python3`, `curl` (all standard). `node` optional but strongly recommended — it enables the syntax check that refuses to deploy a broken build |

**Plugins.** Several blocks build on Jellyfin plugins. `./install.sh --plugins`
sets them up for you — see [Plugins](#plugins). Anything missing simply means
the blocks that use it stay inert; nothing breaks.

> **Why this needs shell access.** Abyss is pure CSS, so it installs by pasting
> into Jellyfin's Custom CSS box. Most of Slipstream is **JavaScript**, and
> that box cannot run JavaScript. The only way to add JS to the Jellyfin web
> client is to modify `index.html` in the web root — which means reaching the
> container. The installer makes that one command, but it cannot be done from
> the Jellyfin admin UI alone.

---

## Install

```bash
git clone https://github.com/lu-tommy/slipstream-jellyfin.git
cd slipstream-jellyfin
./install.sh --cron
```

That's it. The installer:

1. finds your Jellyfin container (or takes `--container NAME`)
2. locates the web root inside it
3. **saves your original `index.html`** to `backups/original/` — kept forever,
   and what `uninstall.sh` restores
4. downloads the [Abyss theme][abyss] and the [Media Bar][mediabar] stylesheet
   from their own upstreams
5. builds the payload and **verifies the generated JavaScript parses**
6. copies everything into the container

Expected output:

```
  ✓ dependencies
  ✓ container: jellyfin
  ✓ web root: /jellyfin/jellyfin-web
  ✓ saved the original index.html -> backups/original/ (5331 bytes)
  ✓ Abyss theme installed (51676 bytes, AumGupta/abyss-jellyfin)
  ✓ Media Bar stylesheet installed (optional plugin, IAmParadox27)
  ✓ built 91 blocks + sf-livesports.js (726805 bytes)
  ✓ syntax check passed
  ✓ deployed to jellyfin
```

### Options

| Flag | Effect |
|---|---|
| `--container NAME` | target a specific container instead of auto-detecting |
| `--cron` | install a 10-minute re-apply job (see below) — Linux hosts; on macOS `crontab` may prompt for Full Disk Access |
| `--write-css` | write the stylesheet into Custom CSS for you, and restart |
| `--force` | rebuild even when the deployed build is already current |
| `--yes` | never prompt |

Re-running is safe and cheap: if the deployed build already matches your
checkout, it says `already up to date` and does nothing.

---

## Plugins

Several blocks build on plugins. The installer can add the repositories and
install them for you:

```bash
./install.sh --plugins \
  --jellyfin-url http://localhost:8096 \
  --api-key YOUR_KEY
```

Create the key in **Dashboard → API Keys**. It is used only against the server
you name and is never written to disk. Restart Jellyfin afterwards, then re-run
`./install.sh`.

**Used by the UI** — install these to get everything:

| Plugin | What depends on it |
|---|---|
| [Media Bar][mediabar] | the home hero / spotlight |
| Jellyfin Enhanced | shortcuts, bookmarks, hidden content, subtitle styling |
| Home Screen Sections | the custom home rows |
| File Transformation | how several plugins inject into the web client |
| Plugin Pages | plugin settings pages (and the request-count dedupe) |
| Collection Sections | collection rows on home |
| LogoSwap | replaces the Jellyfin wordmark with your own logo |

**The rest of my setup** — metadata and quality-of-life, safe to skip:
AudioDB, Fanart, InPlayerEpisodePreview, Intro Skipper, LrcLib Lyrics,
MusicBrainz, OMDb, Open Subtitles, Playback Reporting, Studio Images, TMDb,
TheTVDB.

`plugins.json` records the exact versions this was built against.

> **LogoSwap note.** The stylesheet does *not* ship my logo. Upload your own in
> the LogoSwap plugin and it appears automatically.

---

## The stylesheet

Slipstream is two halves — the JavaScript above, and one stylesheet.

**Option A — let the installer do it:**

```bash
./install.sh --write-css
```

It backs up `branding.xml`, writes the CSS into it, and restarts Jellyfin.

**Option B — paste it (the Abyss way):**

1. **Dashboard → General → Custom CSS**
2. Paste the contents of `assets/slipstream.css`
3. Save, then hard-refresh (<kbd>Ctrl/Cmd</kbd>+<kbd>Shift</kbd>+<kbd>R</kbd>)

> **Don't move this into a `<link>` tag.** Jellyfin fetches Custom CSS at
> runtime, so it lands *after* the `<head>` blocks and deliberately wins on
> source order. Loading it from the head silently inverts that and breaks the
> overrides.

The first line is `@import url("theme/abyss.css")` — a **relative** URL that
resolves inside the container. `install.sh` puts Abyss there. Without it the UI
loads unstyled.

---

## Keeping it through Jellyfin updates

Files copied into a container live in its **writable layer**. A
`docker compose pull && up -d` — anything that *recreates* the container —
throws them away and you are back to stock.

`--cron` installs a job that re-applies every 10 minutes:

```
*/10 * * * * CONTAINER=jellyfin /path/to/slipstream-jellyfin/install.sh --yes
```

It exits in well under a second when nothing has changed — no rebuild, no
downloads, no new backups.

---

## Configuration

Entirely optional. A few features need an id that only exists on *your*
server. Copy the example and fill in what you want:

```bash
cp config.example.json build/config.json
./install.sh --force
```

| Key | Purpose |
|---|---|
| `musicLibraryId` | scopes the Artists list to your Music library |
| `audiobookLibraryId` | enables the audiobook library shelves |
| `sportsBridgeUrl` | live sports channel feed — see [Companion services](#companion-services) |
| `lusertubeUrl` | drawer shortcut to a self-hosted app (omit to hide the entry) |
| `swiparrUrl` | drawer shortcut to a self-hosted app (omit to hide the entry) |
| `drawerHideHrefs` | extra sidebar entries to hide, matched on `href` |

Every value defaults to empty and every consumer guards for that, so skipping
this file is fine. Find a library id by opening the library and reading
`topParentId` out of the URL.

---

## Uninstall

```bash
./uninstall.sh
```

Restores your original `index.html` and `branding.xml`, removes the files it
added, and drops the cron job. If the backup is ever missing, recreating the
container gives you a clean web root:

```bash
docker compose up -d --force-recreate jellyfin
```

---

## How it works

```
build/jfblocks/*.py        payload constants (JS + CSS), grouped by area
        |
build/jf_patch.py          applies 91 blocks to a copy of index.html,
        |                  and writes the ~726 KB runtime as a separate file
        v
index.html + sf-livesports.js  -->  docker cp  -->  container web root
```

A few design decisions worth knowing:

- **The runtime is a separate file, not inline.** It is ~726 KB; `index.html`
  is served `no-cache`, so inlining it re-downloaded and re-parsed the whole
  thing on every page load. As `sf-livesports.js?v=<hash>` the browser caches
  it by ETag, and the hash busts that cache on edit.
- **Every block strips its own previous version before injecting.** Patching an
  already-patched file is idempotent, so nothing stacks up.
- **The build never deploys unverified JavaScript.** A syntax error here throws
  no visible error — it silently kills the *entire* custom UI. `node --check`
  runs before anything is copied, and a failure aborts with your install
  untouched.
- **Install-specific ids live in config, never in code**, and every consumer
  guards the empty case — a blank id passed to `indexOf()` returns `0`, which
  would otherwise match every element on the page.

The `.py` files are heavily commented, and deliberately so: they record *why*
each workaround exists, which browser it was measured in, and which
approaches were tried and failed. If you are going to change something, read
the comment above it first.

---

## Companion services

A few features talk to small self-hosted services that are **not** part of this
repo. Each one is optional and inert when unconfigured — the UI never shows a
dead control:

| Feature | Needs | How it is found |
|---|---|---|
| Request / "get all by artist", music search rows, audiobook requests | a request-bridge service on port **8099** | automatically: `/requestbridge` on the same origin, or port 8099 on a direct LAN connection |
| Live sports channel cards | a channel feed | `sportsBridgeUrl` in config |
| Drawer shortcuts to other apps | your own URLs | `lusertubeUrl`, `swiparrUrl` in config |
| Read-along (text synced to audiobook narration) | pre-aligned data served by the bridge | via the request bridge |

Everything else — the whole UI, motion system, detail pages, Live TV, music,
audiobook playback, search ranking and translations — runs against a stock
Jellyfin with no extra services.

---

## Troubleshooting

**The whole custom UI vanished.**
Almost always a broken or missing `sf-livesports.js`. Re-run
`./install.sh --force`; it will refuse to deploy if the build does not parse.

**Everything is unstyled / the layout looks broken.**
`theme/abyss.css` is missing from the web root — usually a container recreate.
Re-run the installer, and use `--cron` so it heals itself.

**The hero is there but the home rows overlap it.**
Media Bar's stylesheet did not load. Re-run the installer.

**It worked, then reverted after an update.**
Expected — see [Keeping it through Jellyfin updates](#keeping-it-through-jellyfin-updates).

**`no running Jellyfin container found`**
Pass it explicitly: `./install.sh --container my-jellyfin`.

**Changes don't show up.**
Hard-refresh (<kbd>Ctrl/Cmd</kbd>+<kbd>Shift</kbd>+<kbd>R</kbd>). The web client
only fetches `index.html` at launch.

---

## Credits

- **[Abyss][abyss]** by [AumGupta](https://github.com/AumGupta) — the theme
  Slipstream builds on. Downloaded at install time, not redistributed here.
- **[Jellyfin Media Bar][mediabar]** by
  [IAmParadox27](https://github.com/IAmParadox27) — the home hero.
- **[Jellyfin](https://jellyfin.org)** itself.

Slipstream is an unofficial modification of the Jellyfin web client. It is not
affiliated with or endorsed by the Jellyfin project.

## License

[MIT](LICENSE).

[abyss]: https://github.com/AumGupta/abyss-jellyfin
[mediabar]: https://github.com/IAmParadox27/jellyfin-plugin-media-bar
