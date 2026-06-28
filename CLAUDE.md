# CLAUDE.md

Guidance for working in this repo. It hosts a collection of **self-contained, offline-ready
HTML game guides** plus a browsable index, deployed as a GitHub Pages site
(`https://lastranget.github.io/my-game-guides/`).

## Repository layout

- **`guides/`** — the guides themselves, grouped by game in subfolders (`garou/`, `mvc2/`,
  `tetris/`, …). **Each `.html` file is fully standalone**: all CSS/JS/images are inlined
  (images as `data:` URLs / inline SVG), no external assets, no network needed, and **no
  hyperlinks between files**. A guide must work opened directly from disk. The index discovers
  these recursively, so new games just need a new subfolder. One team/character can have a
  **companion set** of guides rather than one giant file — e.g. the MvC2 Cammy/BB&nbsp;Hood/Cyclops
  set is `…-cammy-bbhood-cyclops.html` (beginner), `…-combos.html` (combo dojo), and
  `…-advanced.html` (strategy). They stay standalone (reference siblings by **plain-text filename**,
  never a link) and each carries a **"References & sources"** section citing the source FAQs
  (external `http(s)` citation links are allowed; cross-*file* `.html` links are not).
- **`instructions/`** — the authoring playbook
  (`Scraping a Website into a Single Self-Contained HTML File.md`). It is the **style guide and
  process** every guide follows: PORT vs AGGREGATE modes, the headless-Chromium scraping/extraction
  flow, the OLED-black AYN Thor visual style (palette, collapsible TOC, overflow guards,
  auto-hide chrome), validation steps, and the fighting-game input glyphs. **Read it before
  creating or editing a guide**, and keep new guides consistent with it.
- **`docs/`** — internal design notes. **`input-notation.md`** is the **canonical fighting-game
  input-notation scheme**: facing-relative text tokens (`QCF`, `DP`, `[B]F`, `F-DF-D`…) that
  replaced the old directional arrows (arrows are only correct while a character faces right).
  Every fighting-game guide renders move inputs with these tokens and carries a **notation ledger**
  near the top mapping the tokens it uses. New/edited fighting-game guides must follow it (see also
  §11 of the playbook).
- **`index.html`** — the landing page (see below).
- **`manifest.json`** — fallback file list for the index (see below).
- **`README.md`** — short public overview.

## `index.html` (the landing page)

A single self-contained page that lists every `guides/**/*.html` file, each with a **View**
(open in same tab) and **Download** (native `<a download>`, saves the real filename) action.
It follows the same OLED-black Thor style as the guides (collapsible category cards grouped by
top-level folder, no horizontal overflow at 411px).

**How it lists files:** GitHub Pages serves static files only — there is **no server-side
directory listing**, so a folder can't be `fetch()`ed. Instead the page enumerates the repo at
runtime via the **GitHub git-trees API**
(`/repos/lastranget/my-game-guides/git/trees/main?recursive=1`, which is CORS-enabled) and filters
to `guides/**/*.html`. Display names are upgraded progressively by reading each file's `<title>`.

- Repo/branch is set in the `CONFIG` constant near the top of the inline script, with auto-detection
  from the URL and `?owner=&repo=&branch=` overrides as fallbacks. If the repo is renamed/forked,
  update `CONFIG`.
- Folder → friendly category names live in the `CAT_NAMES` map; unknown folders are title-cased
  automatically, so adding a guide needs no code change.
- Because discovery is live, **adding a guide and committing is enough — it appears automatically.**

## Updating `manifest.json` (do this when guides change)

`manifest.json` is the **offline/rate-limit fallback** the index uses when the GitHub API is
unavailable. The live API is the primary source, but the manifest can go stale, so **regenerate it
whenever you add, remove, or rename a guide** (then commit it alongside the guide):

```bash
python3 -c "import json,glob; open('manifest.json','w').write(json.dumps(sorted(glob.glob('guides/**/*.html', recursive=True)), indent=2)+'\n')"
```

## Testing the index

The index can be verified with headless Chromium (`puppeteer-core` + system
`/usr/bin/chromium-browser`). Notes specific to this environment:

- Serve over HTTP (e.g. `python3 -m http.server`); `file://` blocks `fetch()`. Use a
  **threaded** server if exercising downloads/aborted range requests.
- Snap-confined Chromium's "home" interface **blocks hidden dirs** (`~/.cache/...`) — point the
  profile dir and any download dir at **non-hidden** paths under `$HOME`, or downloads silently cancel.
- On `localhost` the `CONFIG` repo still points at the real public repo, so the live API path is
  exercisable end-to-end.

## Deployment

Served via GitHub Pages from `main` / root. Just commit and push to `main`; the site updates on the
next Pages build.
