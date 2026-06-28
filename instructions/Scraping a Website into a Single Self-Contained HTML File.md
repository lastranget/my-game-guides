---
aliases:
  - Scraping a Website into a Single Self-Contained HTML File
  - website-to-single-html
  - offline-archive-playbook
  - scrape site to one html
tags:
  - type/reference
  - concept/scraping
  - concept/html
  - concept/puppeteer
  - concept/ayn-thor
  - concept/fighting-games
---

# Scraping a Website into a Single Self-Contained HTML File

A playbook for the task: **"turn web content into a single, fully self-contained HTML guide — all images/content embedded, a nice table of contents at the top — that reads well on an AYN Thor handheld."** Written for an AI agent doing this cold. It covers two shapes of the task (see "Two modes" below): faithfully **porting** a whole site, and **aggregating + rewriting** several sources into a brand-new authored guide.

The output must be **portable**: open it from a file with no network, no sibling assets. That means every image is a `data:` URL (or inline SVG) inside the HTML and there are no external CSS/JS files.

> [!important] The thing that will bite you
> Modern sites (Gatsby/Next/React/etc.) render most content **client-side**, often **lazily on scroll**, and frequently hide bulk content behind **"show more / view all" toggles**. `curl` gives you a skeleton, not the content. Diagrams are often `<canvas>` (pixels, not DOM) — invisible to any HTML scraper. **You must drive a real headless browser, scroll the whole page, click every expander, and rasterize canvases — otherwise you will silently capture a fraction of the content and not notice.** Always verify captured counts against the live DOM.

> [!tip] Two modes — decide which one you're in first
> The scraping/extraction half (§2–§5) and the Thor styling half (§8–§11) are **shared**. What changes is the middle — how content becomes the document (§6):
> - **PORT mode** (e.g. the four.lol Tetris archive): the user wants *that site*, offline. **Preserve content faithfully** — keep the page DOM, embed its images, rewrite links to anchors, one `<section>` per page. Fidelity + completeness is the whole job (verify counts, no missing boards). Don't editorialize.
> - **AGGREGATE/REWRITE mode** (e.g. the MvC2 / Garou fighting-game guides): the user wants a *new guide* built **from** several sources. Here scraping is just **research**: pull the raw guides as text, **read them**, then **author original content** in your own structure (teach fundamentals, tier combos beginner→advanced, normalize notation to the facing-relative text-token scheme — §11 / `docs/input-notation.md`, draw custom SVG glyphs). You are aggregating + rewriting, **not** porting DOM. Cross-check sources against each other and fix their errors (old FAQs drift; e.g. MvC2 has no MP/MK, SNK ports use A/B/C/D).
>
> Tell which you're in from the request: "scrape this site into one file / archive it" → PORT. "make a guide for X using these sources / for a beginner / with strategy & combos" → AGGREGATE. When unsure, ask. Many requests are AGGREGATE even though they start with a URL.

---

## 1. Workflow at a glance

**PORT mode** (faithful archive of a whole site):

1. **Recon** — enumerate every URL (sitemap first), detect the framework, find the content container.
2. **Probe one page** — is content in static HTML, or client-rendered? Are images `<img>`, `<svg>`, or `<canvas>`? Is anything lazy or behind a toggle?
3. **Extract** with headless Chromium: per page → scroll to render all lazy content → click all expanders → rasterize `<canvas>`→PNG data URLs → grab the content container's HTML → strip chrome & broken overlays.
4. **Assemble** one HTML: TOC + every page as a `<section>`; embed images; rewrite internal links to in-page anchors; namespace ids to avoid collisions.
5. **Split** pathologically large pages into their own standalone files (keep the main file focused).
6. **Validate** — broken anchors = 0, blank/malformed images = 0, captured image counts == live counts.

**AGGREGATE mode** (author a new guide from sources):

1. **Find the sources** — the relevant pages/FAQs (often several per topic). Same Cloudflare-bypass tooling (§2, §4).
2. **Scrape them as plain text to read** — you don't need the DOM or images; you need the *prose/data*. (GameFAQs prose lives in `<pre id="faqtext">`/`.faqtext`; but **GameFAQs is Cloudflare-walled — pull each FAQ via the Wayback Machine**, see §4. Save to files, read them. The user often hands you the exact FAQ URLs/ids — read *all* of them.)
3. **Read & reconcile** — extract the facts you need (movelists, combos, mechanics, strategy), cross-check sources, and **correct their errors**.
4. **Decide the audience & structure** — e.g. for a beginner: **universal preface (how the *whole game* works)** → fundamentals → how-to → learning path → tiered combos → reference → one-screen card. Confirm any choice that pervades the output (e.g. button mapping) with `AskUserQuestion`. Even a guide scoped to one character or team **must** open with the game-wide preface (see callout below).
5. **Author** the HTML with a generator (data structures → repeated components); build custom glyphs/SVGs (§11) as needed.
6. **Validate** the same way (anchors, overflow, one-screen fit, render-check) — §9.

> [!tip] One subject → a companion *set* of guides, not one giant file
> A team/character often warrants **several standalone guides**. This repo's Cammy/BB Hood/Cyclops set is
> **beginner** (controls, fundamentals, basic combos), a **combo dojo** (every combo, grouped + ID'd, with
> single-screen practice cards), and **advanced** (strengths/weaknesses, assists, neutral, defense,
> meter/DHC, mind-games, matchups, mistakes, boss). Each is self-contained with **no cross-file links** —
> name siblings in plain text only. Share one generator (`gen.py` glyphs + a combo DSL), one
> `style.css`/`app.js`, and one `refs.py`, so the set stays visually identical and each guide carries the
> same **References & sources** section (§9). Build later guides by *reusing* the first guide's components,
> not re-deriving them.

> [!important] A character/team guide must still teach the *whole game* up front
> "Self-contained" means **the reader needs nothing else to play** — not just to play the chosen character. So even when the scope is one character or one team, **prefix the guide with a brief, complete overview of everything required to play the game**: the full control scheme **and every universal/system mechanic**, each with its input and a one-line "what it does." Don't stop at the character's own moves.
> - For a fighting game that means the *complete command list*, not just the character's specials: all attack buttons + assists, block/air-guard, throws/air-throws, dash/run, super jump, launcher→air-combo, chain/magic series, the super meter, supers, **and all the team/system mechanics** (in MvC2: variable assist, variable attack/tag, variable counter, variable combination, snapback, delayed hyper combo, advancing guard/push-block, tech roll, taunt, order change). The test: *"Could someone who has never opened this game sit down and play, using only this file?"* If a universal mechanic is missing, it isn't self-contained.
> - Build it from a canonical system/FAQ source, **cross-check and fix errors** (old/abbreviated FAQs drift): e.g. MvC2 *does* have air-blocking, and *does not* have CvS2's "Mega Crash" — verify against the source, don't copy a half-remembered list. Reuse the same input glyphs (§11) so the preface matches the rest of the guide; mark meter costs.
> - Keep it a **prefix/overview**, not a wall — terse rows (name · input · one-line effect), grouped (movement / defense / offense / team). The deep character content still follows.

---

## 2. Recon: enumerate URLs and detect the framework

```bash
# Sitemap is the authoritative page list. Check both common locations.
curl -sL https://SITE/sitemap.xml | grep -oE '<loc>[^<]*</loc>'
curl -sL https://SITE/sitemap/sitemap-index.xml      # then fetch each child sitemap
```

> [!warning] The sitemap lies (sometimes)
> Pages can be **linked but missing from the sitemap** (WIP/unlisted). After a first pass, scan the captured HTML + landing page for internal `href="/..."` that you did **not** scrape, `curl -o /dev/null -w '%{http_code}'` each, and add any that return `200`. In practice this recovered ~5 extra pages on a ~66-page site.

Framework tells: `typography.js` / `___gatsby` / `gatsby-focus-wrapper` → Gatsby. `__next` → Next.js. `page-data.json` under `/page-data/...` → Gatsby data (often compiled MDX — not worth parsing; render instead).

---

## 3. Probe a single page before writing the extractor

```bash
# Static HTML (no JS):
curl -sL https://SITE/some/page -o static.html
# JS-rendered DOM (runs scripts):
chromium --headless --no-sandbox --disable-gpu --virtual-time-budget=8000 \
  --dump-dom https://SITE/some/page > dom.html
```

Compare them and answer:
- Is the **text** in `static.html`, or only in `dom.html`? (SSR vs CSR.)
- How are **images** represented? `grep -c '<img\|<svg\|<canvas\|data:image' dom.html`.
  - `<canvas>` → must rasterize (see §5). `<img>`/`<svg>` → already embeddable.
- What's the **content container**? Look for a stable wrapper (`<article>`, a semantic tag, or a class). Hashed CSS-in-JS class names (e.g. `sc-1klj7up-2`) are stable *within one build* and usable as selectors, but verify they appear across pages.
- Multiple stacked `<canvas>` per figure? (animation layers) → you must composite or screenshot, not replace 1:1.

---

## 4. Tooling: puppeteer-core + the system Chromium

Don't download a browser; reuse the installed one.

```bash
which chromium-browser chromium google-chrome   # find an executable
npm init -y && npm install puppeteer-core
```

```js
const puppeteer = require('puppeteer-core');
const browser = await puppeteer.launch({
  executablePath: '/usr/bin/chromium-browser',
  headless: 'new',
  args: ['--no-sandbox', '--disable-gpu', '--disable-dev-shm-usage'],
});
```

> [!warning] Sandboxed Chromium can't read your scratch dir
> A snap/apparmor-confined Chromium often **cannot open `file:///tmp/...`**. For screenshot/render checks of local output, copy the file under `$HOME` first (e.g. `~/_preview.html`) and load that. Live `https://` URLs are fine.

> [!warning] Cloudflare-walled sources (GameFAQs) → go through the Wayback Machine
> Some sources sit behind **Cloudflare** (e.g. **GameFAQs**): `curl`, the harness `WebFetch`, **and**
> even headless `chromium --dump-dom` all get the **"Just a moment…"** JS-challenge page, not the
> content. The reliable bypass is the **Internet Archive** (not Cloudflare-protected). Gotcha: the
> harness `WebFetch` *refuses* `web.archive.org`, but **Bash `curl` reaches `archive.org` fine.** Recipe:
> ```bash
> # 1) find the closest snapshot via the availability API (returns JSON with the snapshot URL+timestamp)
> curl -s "https://archive.org/wayback/available?url=<original-url>"
> # 2) fetch the RAW archived page — the `id_` after the timestamp strips the Wayback toolbar/wrappers
> curl -sA "Mozilla/5.0 …Chrome/120 Safari/537.36" "http://web.archive.org/web/<TS>id_/https://<original-url>"
> ```
> A FAQ id may be archived under a **different platform path** than the one you have (e.g. a Dreamcast
> id only archived under the `arcade`/`ps2` URL) — loop over platform paths until one returns a snapshot.
> GameFAQs FAQ prose lives in `<pre id="faqtext">` / `<div class="faqtext">`; grab that, strip tags, read it.

---

## 5. The extractor (the core of the job)

For **each** page: navigate → render everything → rasterize → extract → clean. Pseudocode of the parts that matter:

```js
await page.setViewport({ width: 1400, height: 1000, deviceScaleFactor: 2 });
await page.goto(url, { waitUntil: 'networkidle2', timeout: 90000 });

// (a) Render ALL lazy content + expand collapsed sections, until the canvas
//     count stops growing. Lazy boards mount via IntersectionObserver on scroll.
await page.evaluate(async () => {
  const sleep = ms => new Promise(r => setTimeout(r, ms));
  const fullScroll = async () => {
    const h = document.body.scrollHeight;
    for (let y = 0; y <= h; y += 500) { window.scrollTo(0, y); await sleep(30); }
    window.scrollTo(0, document.body.scrollHeight); await sleep(120);
  };
  const clickExpanders = () => {                       // adapt the regex to the site
    const els = [...document.querySelectorAll('CONTENT_SELECTOR *')]
      .filter(e => e.children.length === 0 && !e.__x && /View All \d+|Show more/i.test(e.textContent));
    els.forEach(e => { e.__x = true; try { (e.closest('div,button,a') || e).click(); } catch {} });
  };
  await fullScroll(); clickExpanders(); await sleep(400);
  let prev = -1;
  for (let i = 0; i < 15; i++) {                       // loop until stable
    await fullScroll(); clickExpanders(); await sleep(350);
    const n = document.querySelectorAll('canvas').length;
    if (n === prev) break; prev = n;
  }
  window.scrollTo(0, 0);
});
await new Promise(r => setTimeout(r, 1500));           // let last canvases paint

// (b) In-page: rasterize canvases, drop dead overlays, return container HTML.
const data = await page.evaluate(() => {
  const art = document.querySelector('CONTENT_SELECTOR');
  // canvas -> <img> data URL, preserving displayed size
  art.querySelectorAll('canvas').forEach(c => {
    try {
      const r = c.getBoundingClientRect();
      const img = document.createElement('img');
      img.src = c.toDataURL('image/png');
      img.style.width = (Math.round(r.width) || c.width) + 'px';
      img.style.height = (Math.round(r.height) || c.height) + 'px';
      img.style.imageRendering = 'pixelated';           // for blocky pixel art
      c.replaceWith(img);
    } catch { c.replaceWith(document.createTextNode('[canvas-render-failed]')); }
  });
  // Remove decorative absolute-positioned overlays. They rely on a parent's
  // position:relative from CSS-in-JS that we are NOT carrying over, so in the
  // archive they escape to <body> and cover unrelated content (e.g. the TOC).
  art.querySelectorAll('[style*="linear-gradient"]').forEach(d => d.remove());
  art.querySelectorAll('[style*="position: absolute"]').forEach(d => {
    if (!d.querySelector('img,svg,canvas,picture') && !d.textContent.trim()) d.remove();
  });
  // Remove now-defunct toggle controls (text leftovers).
  art.querySelectorAll('*').forEach(e => {
    if (!e.children.length && /^(View All \d+ Solutions|Collapse|Show (More|Less))$/i.test(e.textContent.trim())) e.remove();
  });
  const h1 = art.querySelector('h1,h2');
  return { title: h1 ? h1.textContent.trim() : document.title, html: art.innerHTML };
});
```

Notes:
- `toDataURL()` throws on **cross-origin tainted** canvases. If that happens, fall back to `elementHandle.screenshot()` of the figure wrapper.
- `deviceScaleFactor: 2` gives crisp rasters; `image-rendering: pixelated` keeps pixel-art sharp.
- **Pages with no clean container** (landing/about): score block elements by text length, drop high link-density blocks (nav/sidebar), pick the best — or hardcode a selector per odd page. Hashed classes work as a last resort.

> [!important] Always verify you captured everything
> For a sample of image-heavy pages, compare your captured `data:image` count to the **live** count after a full scroll + expand:
> `document.querySelectorAll('CONTENT_SELECTOR canvas').length`.
> On a real run this caught pages where naïve extraction got 188 of **934** boards (the rest were behind "View All" toggles). Counts must match.

Run extraction **per page, sequentially**, writing one JSON array of `{slug, url, title, html}`. ~70 pages with heavy scrolling takes 10–20 min; run it backgrounded.

---

## 6. Assemble the single HTML file

> [!note] Mode split
> This section is mostly **PORT mode** (you're stitching real page DOM together, so link-rewriting and id-namespacing matter). In **AGGREGATE mode** you instead **author** the body from your own data structures (see §1 AGGREGATE) — a Python generator with one function per component (move row, combo line, glyph) keeps it consistent and lets you size things to the screen. The shared pieces either way: a generator script, **id-namespacing** if you concatenate many blocks, and all of §8 (Thor styling). For aggregate guides the "embed images" step is usually **inline SVG glyphs** (§11) rather than fetched bitmaps.

Build with a small script (Python is convenient). Key transforms:

**Embedded images** — already done in §5 (canvas→data URL). If the source uses real `<img src="/foo.png">`, fetch each and inline as base64 too.

**Internal link rewriting** — turn `href="/methods/x"` into in-page anchors `href="#methods-x"`. Leave `http(s)://`, `mailto:`, and `#…` links alone. Map each slug → a slug-derived anchor; unknown internal links → anchor anyway (harmless) or unwrap.

**Namespace ids (critical when concatenating many pages).** Auto-generated heading ids (`overview`, `notes`, `summary-table`) **collide** across pages once merged, breaking in-page jumps. For each page, prefix every `id` and every intra-page `href="#…"` with the page's anchor, *before* rewriting cross-page links:

```python
def namespace(body, prefix):                 # prefix = page-anchor + "--"
    body = re.sub(r'(\sid=")([^"]+)(")',     lambda m: m[1]+prefix+m[2]+m[3], body)
    body = re.sub(r'(href="#)([^"]+)(")',    lambda m: m[1]+prefix+m[2]+m[3], body)
    return body
```

This alone took broken anchors from dozens → **0** across a 66-page merge.

**Page order** — group by category in a sensible order; home/about first, misc last.

**Each page becomes** `<section class="article" id="ANCHOR">` with a small source-link + "back to contents" row, then the cleaned HTML.

---

## 7. Split pathologically large pages into standalone files

If a few pages dwarf the rest (e.g. solution-dump pages with 900–1100 diagrams each), **give each its own standalone HTML file** so the main file stays focused and fast.

> [!important] Standalone means standalone — no cross-file links
> The user's rule (and a good default): **every file must work in isolation; do not hyperlink between files.** When rewriting links, links pointing at a *different* output file are **unwrapped to plain text** (keep the words, drop the `<a>`). You may still *name* the other file in plain text so it's discoverable (e.g. a TOC note: "Large solution pages kept in separate files: `four-lol-pc-4th.html`"). Each split file gets its own mini-TOC from its `<h2>` groups, its own header/back-to-top, and a plain-text note of which file is the main one.

Implementation: a single builder that knows every page's home file. `process_anchors(body, same_file_slugs)` keeps+retargets links whose destination is in *this* file and unwraps the rest.

---

## 8. Make it read well on the AYN Thor

**Screens** (design mobile-first for the small one; it must also work on the wide one):
- **Bottom (primary):** 3.92" AMOLED, **1080×1240** px, ~31:27 (nearly square, slight portrait), ~419 DPI → roughly **~410×470 CSS px** in an Android browser.
- **Top (occasional):** 6", **1920×1080** landscape → roughly **~850×480 CSS px**.

Both are **short**. Design implications:
- Single column, `max-width` ~760px centered (fits the top screen, full-bleed on the bottom).
- Comfortable base **17px / line-height 1.7**; generous tap targets (TOC links `display:block; padding:9px`).
- **Collapsible TOC**: each category in a `<details>` (collapsed by default so the whole TOC fits the short screen) + an "Expand all" button. `columns:2` only at `min-width:560px`.
- Sticky compact header with a "Contents" jump; a **floating back-to-top** button (short screens scroll a lot).
- **Auto-hide chrome on scroll** (preferred): hide the sticky header *and* the back-to-top button while scrolling **down**, reveal them on scroll **up** — maximizes reading area on the short screen. Toggle one `body.hide-chrome` class from a throttled scroll listener and animate with `transform`/`opacity` transitions (see snippet).
- `html{scroll-behavior:smooth; scroll-padding-top:54px}` so anchors don't hide under the sticky bar.
- **Theme: force OLED black** (see callout) — set colors directly, don't depend on `prefers-color-scheme`; add `<meta name="color-scheme" content="dark">`.
- `<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">` — **do not** disable zoom (users pinch-zoom diagrams).
- Let figure groups **flow inline-block and wrap** (1–2 across on the bottom screen, 3 across on the top) instead of one giant per-screen image. Target the figure wrapper class: `[class~="sc-...-2"]{display:inline-block;vertical-align:top;margin:5px}`.
- Clamp **all** media: `img,video,iframe,embed,object{max-width:100%;height:auto}`; `image-rendering:pixelated` for pixel art.

> [!important] OLED black theme (preferred for the Thor's AMOLED)
> **White text on perfect black `#000000`.** Use `#f2f2f2` for body text (reads white, slightly less halation than `#fff`). Keep most surfaces pure black; **differentiate background only where it aids structure** — the TOC container, the dropdown summaries, and code blocks. A working palette:
> ```
> --bg:#000000  --fg:#f2f2f2  --muted:#9a9aa2  --accent:#7cc0ff   (light-blue links pop on black)
> --card:#0d0d11   (TOC container, code)   --card2:#17171d (dropdown summaries, buttons, hover)
> --border:#2b2b33 (subtle separators)
> ```
> Notes: **box-shadows are invisible on black** — use a 1px ring (`box-shadow:0 0 0 1px var(--border)`) or border for elevation/figure outlines instead. Give each `<details>` a border + `card2` summary so the dropdowns read as interactive cards (the user explicitly likes the TOC dropdowns). The board diagrams have light backgrounds, so they show as bright cards on black — that's fine and high-contrast.

> [!warning] The "swipe left into blank space" overflow (narrow screen)
> Symptom: content is centered fine, but on the small screen you can **swipe left and the whole page slides off, revealing blank space on the right.** Cause: an element is **wider than the viewport**, so the document's `scrollWidth > clientWidth` and the page scrolls horizontally. The usual culprit is **embedded `<video>`/`<iframe>`** captured at the desktop layout width (e.g. an 853px video on a 411px screen) — `img{max-width:100%}` alone doesn't cover them. Diagnose, don't guess:
> ```js
> // at the target viewport: list elements whose right edge exceeds the viewport
> const vw=document.documentElement.clientWidth;
> [...document.querySelectorAll('*')].filter(e=>e.getBoundingClientRect().right>vw+1)
>   .map(e=>({tag:e.tagName,w:Math.round(e.getBoundingClientRect().width)}));
> // success = document.documentElement.scrollWidth === clientWidth
> ```
> Fix (do all three): (1) clamp **every** medium `img,video,iframe,embed,object{max-width:100%;height:auto}`; (2) `overflow-x:clip` on `html` and `body` (use **`clip`, not `hidden`** — `hidden` can break `position:sticky`); (3) for flex rows with long text/URLs (e.g. a source-link bar), add `min-width:0` to the flex children and `overflow-wrap:anywhere` so a long unbreakable URL can't force width. Keep `<pre>`/`<table>` as their own internal scroll containers (`overflow:auto`) so they never widen the page.

A compact OLED-black CSS skeleton with the overflow guard, that delivered all of the above:

```css
:root{--bg:#000;--fg:#f2f2f2;--muted:#9a9aa2;--accent:#7cc0ff;
  --card:#0d0d11;--card2:#17171d;--border:#2b2b33;--maxw:760px}
html{scroll-behavior:smooth;scroll-padding-top:54px;-webkit-text-size-adjust:100%;overflow-x:clip}
body{margin:0;background:var(--bg);color:var(--fg);font-size:17px;line-height:1.7;
  font-family:-apple-system,"Segoe UI",Roboto,system-ui,sans-serif;
  overflow-wrap:break-word;overflow-x:clip;max-width:100%}
.wrap{max-width:var(--maxw);margin:0 auto;padding:12px 14px 96px;width:100%}
a{color:var(--accent);text-decoration:none}
img,video,iframe,embed,object{max-width:100%;height:auto}            /* overflow guard */
img{image-rendering:pixelated;vertical-align:top}
code,pre{background:var(--card);border:1px solid var(--border);border-radius:5px}
header.bar{position:sticky;top:0;z-index:50;display:flex;justify-content:space-between;
  align-items:center;background:var(--bg);border-bottom:1px solid var(--border);padding:8px 14px}
nav#toc{background:var(--card);border:1px solid var(--border);border-radius:12px;padding:10px 12px;margin:14px 0 34px}
nav#toc li a{display:block;padding:9px 8px;border-radius:7px}
nav#toc details{border:1px solid var(--border);border-radius:8px;overflow:hidden;margin:4px 0}
.toc-cat>summary{cursor:pointer;list-style:none;padding:10px 8px;font-weight:700;background:var(--card2)}
.src-link{display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap}
.src-link>*{min-width:0}.src-link a{overflow-wrap:anywhere}             /* overflow guard */
[class~="sc-...-2"] img{box-shadow:0 0 0 1px var(--border);border-radius:3px} /* 1px ring, not shadow */
#totop{position:fixed;right:14px;bottom:14px;width:46px;height:46px;border-radius:50%;
  background:var(--accent);color:#000;display:flex;align-items:center;justify-content:center;text-decoration:none;opacity:.92}
@media (min-width:560px){nav#toc ul.toc-top{columns:2;column-gap:26px}}
```

**Auto-hide-on-scroll** — the CSS transitions + the throttled scroll listener:

```css
header.bar{transition:transform .25s ease;will-change:transform}
#totop{transition:opacity .25s ease,transform .25s ease}
body.hide-chrome header.bar{transform:translateY(-100%)}
body.hide-chrome #totop{opacity:0;transform:translateY(72px);pointer-events:none}
```
```js
var lastY=window.pageYOffset||0,ticking=false;
function upd(){
  var y=window.pageYOffset||0;
  if(Math.abs(y-lastY)>4){document.body.classList.toggle('hide-chrome', y>lastY && y>60); lastY=y;}
  ticking=false;
}
window.addEventListener('scroll',function(){
  if(!ticking){requestAnimationFrame(upd);ticking=true;}
},{passive:true});
```
The `y>60` guard keeps the header visible near the top (nothing to scroll up to); the `>4px` dead-zone and `requestAnimationFrame` throttle prevent jitter. Verify by scripting `window.scrollTo` down/up and asserting `body.classList.contains('hide-chrome')` flips.

Inline the CSS in a `<style>` tag and the JS (expand-all + auto-hide) in a `<script>` tag — keep it **one file**.

---

## 9. Validate before declaring done

```python
# Broken anchors: every href="#x" must have a matching id="x" (browsers
# percent-decode fragments, so also test the decoded form).
# Off-file links: in a "standalone" file the only allowed off-file links are EXTERNAL http(s) —
#   including a "References & sources" section citing the source FAQs. Cross-FILE *.html links are
#   banned; the self-containment audit must WHITELIST those citation hosts (don't flag them as leaks).
# Image integrity: decode every data:image; none should be malformed or single-color (blank).
```

- `broken anchors == 0` in every file.
- `blank/malformed images == 0` (decode with PIL; a 1-color PNG = a canvas that never painted → you scrolled/​waited too little).
- Per-page captured image count `==` live count for image-heavy pages.
- **No horizontal overflow** on the narrow screen: at 411px wide, `document.documentElement.scrollWidth === clientWidth` (no swipe-into-blank-space).
- Render-check at **411×472** and **853×480** viewports (copy file under `$HOME` first, screenshot via puppeteer) and actually *look*: black background is `rgb(0,0,0)`, TOC/dropdowns are differentiated, TOC collapses, boards wrap, nothing overlays the TOC.
- **External citation links are allowed** (a References section linking the source FAQs). Whitelist those hosts in the self-containment audit and only flag *other* `http/file/local` refs as asset leaks — and confirm `scratchpad`/`/tmp` paths never leaked into the output.
- **One-screen cards fit the budget**: at 411px each `section.screenfit` must measure `h2-top → section-bottom ≤ ~418px` (viewport 472 − the 54px `scroll-padding-top`). For paginated combo cards, chunk by a weight budget (short=1, medium=2, long=3 *action* pieces; ~6/screen fits) and **measure every page** in puppeteer, then tune the budget. The wide-screen "all-three" trio card is allowed to exceed this (it targets the 853px top screen, ~≤426px there).

> [!note] Honest reporting
> A puppeteer "N-1 of N images loaded" is usually a render-timing artifact, not corruption — confirm with the PIL decode audit before claiming completeness, and say which check you trust.

---

## 10. Gotchas checklist

- [ ] Decide **PORT vs AGGREGATE** first (§ Two modes) — porting DOM vs. reading sources to author a new guide. A URL in the request doesn't mean PORT. ➕ 2026-06-25
- [ ] AGGREGATE mode → scrape as **text to read**, cross-check sources, fix their errors; author original tiered/teaching content, don't copy verbatim. ➕ 2026-06-25
- [ ] Character/team-scoped guide → still prefix it with a **game-wide overview**: the full controls + **every** universal/system mechanic (input + one-line effect), not just that character's moves. "Self-contained" = playable from this file alone. ➕ 2026-06-27
- [ ] Fighting-game inputs → use the **facing-relative text-token notation** (`QCF`/`DP`/`[B]F`/`F-DF-D`…, per `docs/input-notation.md`), **not** screen arrows; add a **notation ledger** at the top of the guide and drop redundant per-card mini-legends. ➕ 2026-06-28
- [ ] Content is client-rendered → use headless Chromium, not curl. ➕ 2026-06-25
- [ ] Lazy-on-scroll content → full-scroll until canvas count stabilizes. ➕ 2026-06-25
- [ ] "View All / Show more" toggles → click them all, then re-scroll. ➕ 2026-06-25
- [ ] Diagrams are `<canvas>` → `toDataURL()` (or screenshot if tainted). ➕ 2026-06-25
- [ ] Decorative `position:absolute`/gradient overlays → remove (they escape without their CSS). ➕ 2026-06-25
- [ ] Merging pages → namespace ids to avoid anchor collisions. ➕ 2026-06-25
- [ ] Pages linked but not in sitemap → discover and add. ➕ 2026-06-25
- [ ] Huge pages → split into standalone files, **no cross-file links**. ➕ 2026-06-25
- [ ] Sandboxed Chromium can't read `/tmp` → render local files from `$HOME`. ➕ 2026-06-25
- [ ] Wide embedded media (`<video>`/`<iframe>`) → clamp all media + `overflow-x:clip` (fixes swipe-into-blank-space). ➕ 2026-06-25
- [ ] OLED target → force black `#000` + white text; differentiate only TOC/dropdowns/code; 1px rings not shadows. ➕ 2026-06-25
- [ ] Auto-hide the header + back-to-top on scroll-down, reveal on scroll-up (`body.hide-chrome` toggle). ➕ 2026-06-25
- [ ] Verify captured counts vs live; audit for blank images; confirm `scrollWidth==clientWidth` at 411px. ➕ 2026-06-25
- [ ] Cloudflare-walled source (GameFAQs) → fetch via the **Wayback Machine** (`archive.org` availability API + raw `…<TS>id_/…`); harness `WebFetch` refuses archive.org but Bash `curl` works; fall back across platform paths for an id. ➕ 2026-06-28
- [ ] One subject can be a **companion set** (beginner / combo / advanced) — separate standalone files, no cross-file links, shared generator + `style.css`/`app.js` + `refs.py`, each with a References section. ➕ 2026-06-28
- [ ] Combo guide → name specials as accent pills (input in `title=`), keep normals as keycaps; ID every combo (`CA-01`…) in display order; group by use-case; paginate one-screen cards by weight + measure ≤418px. ➕ 2026-06-28
- [ ] Old fighting-game FAQs use 6-button naming → normalise to MvC2's 4 buttons (`LP→LK→HP→HK`), fold phantom-medium duplicates, note the merge. ➕ 2026-06-28
- [ ] References/citations: external `http(s)` links to sources are allowed in standalone files — whitelist those hosts in the self-containment audit (don't flag as asset leaks). ➕ 2026-06-28

---

## 11. Fighting-game input glyphs (AYN Thor button colours)

> [!warning] Only for fighting-game move inputs
> Coloured button glyphs are **exclusively** for **fighting-game guide content where you render move inputs / combos** (MvC2, SF, etc.). Do **not** use them anywhere else — in a Tetris/Calibre/general archive they're meaningless and distracting. If a guide isn't about fighting-game inputs, skip this entire section.

> [!important] Notation: facing-relative text tokens + a top-of-guide ledger
> Render stick motions as **short text tokens** (`QCF`, `QCB`, `DP`, `HCB`, `[B]F`, `F-DF-D`…), **not** screen-direction arrows (`↓↘→`). Tokens are **facing-relative** (`F`/`B` = *toward / away from* the opponent), so they stay correct on **both** sides of the screen — arrows are only right while the character faces right. The complete, canonical scheme (directions, named motions, charge, modifiers, the spell-out rule for unnamed motions, and a glyph→token migration map) lives in **[`docs/input-notation.md`](../docs/input-notation.md)** — use those exact tokens, don't invent new ones.
> - **Add a notation ledger near the top of every fighting-game guide** (right beside the button-colour `leg-grid`) mapping each token used → its meaning. This is what keeps the guide self-contained now that pills are abbreviations.
> - Because the tokens are self-documenting and the top ledger explains them once, the old per-card inline mini-legends (`motlegend`/`minileg`) are **redundant — drop them.**

> [!important] Combo-guide content: name the specials, ID every combo, group by use-case
> A dedicated **combo guide** has conventions beyond a movelist that keep it readable and one-screen-friendly:
> - **Refer to special moves by name, not raw motion.** Render a special/super as a small **named pill**
>   tinted in the character's accent (`.sp{color:var(--ca)}`) with the full input in the `title=` tooltip
>   (e.g. *Cyclone Kick*, hover → `QCB + K`). Keep **normals** (LP/LK/HP/HK and directional launchers like
>   `D+HP`) as the coloured keycaps — those are what you're drilling. Far more compact than `motion+button`
>   everywhere, and it's what lets long combos fit one screen. (The raw inputs still live once in the
>   copied one-screen movesets + the top notation ledger.)
> - **Give every combo a stable unique ID** — char prefix + number (`CA-01`, `BB-07`, `CY-23`). Assign them
>   in **display order** (use-case group order, stable within group) so they're contiguous & gap-free, and
>   show the same ID in *both* the detailed listing and the single-screen practice cards so the user can say
>   "drill CY-11." Render `cr.`/`j.` prefixes *inside* the button group (no stray separators).
> - **Group by use-case**, not just difficulty — Ground BnB / anti-air & quick confirms / hit-confirm into
>   super / launcher→Aerial-Rave / OTG & relaunch / special-cancel & beam-links / corner & loops / throws &
>   resets / team-DHC. Add a difficulty marker (`●○○`) and a small badge for staples shared with a sibling guide.
> - **Normalise old movelists to the real button count.** Old MvC2 FAQs use 6-button SF naming
>   (jab/strong/fierce, short/forward/roundhouse, or `WP/WK/Strong/Forward/HP/HK`) but **MvC2 has only
>   `LP/HP/LK/HK`** — the magic series is `LP → LK → HP → HK`, and tapping a light twice climbs it. Map the
>   phantom "medium" onto the real chain and **fold the true duplicates that creates** (that's correcting the
>   source, not dropping combos) — say so in prose. Cross-check several FAQs against each other.

**The AYN Thor has a Nintendo-style ABXY face cluster with coloured buttons; the shoulders/triggers are grey.** Positions and colours:

```
        X = blue            shoulders / triggers = GREY
   Y = green   A = red
        B = yellow
```

| Physical button | Colour | Hex (bg / text) |
| --- | --- | --- |
| X (top) | blue | `#2f86f0` / white |
| A (right) | red | `#ec3b3b` / white |
| Y (left) | green | `#2fb84a` / white |
| B (bottom) | yellow | `#f2c531` / **black** |
| L/R/ZL/ZR triggers | grey | `#6c7079` / white |

> [!important] The colour is the *physical button*; the game-button mapping is the user's call — confirm it
> The user maps these physical buttons to a game's attacks, and the mapping differs per game. **Ask which scheme they want** (see the `AskUserQuestion` in the MvC2 build). MvC2 has only **LP/HP/LK/HK + 2 assists** (no MP/MK); the user chose **MvC2-native**: `LP=green(Y)  HP=blue(X)  LK=yellow(B)  HK=red(A)`, assists/triggers grey. Whatever the mapping, **anything not on a coloured face button is grey.**

### How to make the glyphs (SVG keycaps + CSS pills)

Three glyph types: a colored **keycap** (the attack button), a **split keycap** for two-button inputs (`PP`/`KK` supers), and grey **pills** for stick motions/directions. Keycaps are inline SVG (the "really nice" look the user asked for); motions are CSS spans.

**Keycap SVG** — size it in `em` so it scales with the surrounding font (this is what lets a whole moveset shrink to fit one screen):
```python
BTN = {'LP':('#2fb84a','#fff'),'HP':('#2f86f0','#fff'),
       'LK':('#f2c531','#1a1505'),'HK':('#ec3b3b','#fff'),
       'A1':('#6c7079','#fff'),'A2':('#6c7079','#fff')}
def keycap(tok):
    fill,txt = BTN[tok]
    return (f'<svg class="key" viewBox="0 0 38 27" role="img" aria-label="{tok}">'
            f'<rect x="1.5" y="1.5" width="35" height="24" rx="6" fill="{fill}" stroke="rgba(0,0,0,.4)"/>'
            f'<text x="19" y="19" text-anchor="middle" font-size="14" font-weight="800" '
            f'fill="{txt}" font-family="Arial,Helvetica,sans-serif">{tok}</text></svg>')
```

**Split keycaps** for `P/K/PP/KK` (any-punch / both-punches etc.) use two shared `linearGradient`s with a **hard 50% stop**, defined once in a hidden `<svg>` and referenced by id (one defs block, no per-glyph id collisions):
```html
<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
 <linearGradient id="gp" x1="0" x2="1" y1="0" y2="0">
   <stop offset="50%" stop-color="#2fb84a"/><stop offset="50%" stop-color="#2f86f0"/></linearGradient>  <!-- punch: green|blue -->
 <linearGradient id="gk" x1="0" x2="1" y1="0" y2="0">
   <stop offset="50%" stop-color="#f2c531"/><stop offset="50%" stop-color="#ec3b3b"/></linearGradient>  <!-- kick: yellow|red -->
</defs></svg>
```
…then the keycap `<rect>` uses `fill="url(#gp)"` (P/PP) or `fill="url(#gk)"` (K/KK); give the label a thin dark outline via `style="paint-order:stroke" stroke="rgba(0,0,0,.45)" stroke-width="0.7"` so white text stays legible over the seam.

**Motion / direction pills** (grey) — render each motion as a **text token** (facing-relative, per
[`docs/input-notation.md`](../docs/input-notation.md)), **not** an arrow path. Put the full name in `title=`:
```python
def mot(tok,title): return f'<span class="mot" title="{title}">{tok}</span>'   # mot('QCF','Quarter-circle forward')
def dir_(tok):      return f'<span class="dir">{tok}</span>'                    # single F/B/U/D/UF/DF… or charge [B]F
# an "air" tag for air-only moves:  <span class="air">air</span>
```
A special move = motion pill + `+` + keycap (e.g. *Spiral Arrow* = `mot('QCF','Quarter-circle forward') + '+' + keycap('K')`). Motions with no standard name are spelled out with `-` between direction tokens (e.g. `F-DF-D`). Combos = a flex row of these with a faint `›` between steps and italic annotations (`launch`, `SJ`, `OTG`, `XX`, `→DHC`).

**CSS** (OLED-friendly; keycaps scale with font-size):
```css
.key{height:1.5em;width:auto;vertical-align:-0.34em}
.mot{display:inline-block;background:#26282e;color:#dfe2ea;border:1px solid var(--border);
  border-radius:6px;padding:0 .45em;font-size:.86em;letter-spacing:.06em;vertical-align:middle}
.dir{display:inline-block;background:#3a3e46;color:#fff;border:1px solid rgba(0,0,0,.4);
  border-radius:6px;padding:0 .4em;font-weight:700;font-size:.82em;vertical-align:middle}
.air{background:#1d2733;color:#9fd0ff;border:1px solid #2a3a4d;border-radius:5px;font-size:.66em;
  padding:0 .35em;text-transform:uppercase}
.grp{display:inline-flex;align-items:center;gap:.12em;white-space:nowrap}  /* keep motion+button together */
```

**Fitting a moveset to one screen:** because `.key` is sized in `em`, a whole moveset card scales by setting the container `font-size` (e.g. `13.5px` for a per-character card, `~10px` + a 3-column grid for an "all characters at once" card). Verify each fits: at 411px wide, the section's `heading→bottom` height must be `≤ ~418px` (viewport minus the `scroll-padding-top` so it's fully visible after a TOC jump). Drop redundant legends from the one-screen cards — the text-token pills are self-documenting and the top-of-guide notation ledger explains them once.
