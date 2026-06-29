# tools/

The generator toolchain for the **AGGREGATE-mode** game guides in this repo (the ones
authored from community FAQs — see the playbook in `instructions/`). Each guide is still a
single self-contained HTML file; these scripts just *produce* them from data structures so a
whole set of guides stays consistent.

> **New tools go here.** Anything reusable you build while making guides (generators, scrapers,
> converters, QA scripts) belongs in `tools/`, catalogued below and in `build-map.json`.

## What built what

The authoritative mapping is **`build-map.json`** (machine-readable). Human summary:

| Guide | Built by | Data | Sources |
|---|---|---|---|
| `mvc2/…-cammy-bbhood-cyclops.html` (beginner) | — *hand-authored* | — | MvC2 FAQs |
| `mvc2/…-cammy-morrigan-cyclops.html` | — *hand-authored* | — | MvC2 FAQs |
| `mvc2/…-cammy-bbhood-cyclops-combos.html` | `build.py` | `data.py`, `refs.py` | MvC2 FAQs 7669/22878/8517/8318/7893/7945/9838 |
| `mvc2/…-cammy-bbhood-cyclops-advanced.html` | `build3.py` | `refs.py` | same MvC2 FAQs |
| `kofxi/kofxi-terry.html` | `build_kof.py` | `chardata.py`, `refs_kof.py` | KOF XI FAQs 45250, 44141 |
| `kofxi/kofxi-athena.html` | `build_kof.py` | `chardata.py`, `athena_matchups.py` | KOF XI FAQs 51436, 44141 |
| `kofxi/kofxi-bjenet.html` | `build_kof.py` | `chardata.py`, `bjenet_combos.py` | KOF XI FAQs 44220, 44141 |
| `garou/*`, `tetris/*` | — *hand-authored / ad-hoc* | — | — |

## Files

**Shared library + assets** (used by every generator)
- `gen.py` — the glyph engine: coloured SVG button keycaps, motion/direction pills, named-special
  pills, and the combo DSL (`render_combo`) + constructors (`G/M/MA/DB/SQ/SP/PRE/TAG`). Holds the
  `BTN` colour map; KOF adds A/B/C/D/E at import time.
- `style.css` — the OLED-black AYN Thor stylesheet (inlined into every generated guide).
- `app.js` — the auto-hide-chrome-on-scroll script (inlined into every generated guide).

**MvC2 — Cammy / BB Hood / Cyclops**
- `build.py` — the **combo dojo** guide. `python3 tools/build.py`
- `build3.py` — the **advanced/strategy** guide. `python3 tools/build3.py`
- `data.py` — the MvC2 combo dataset (use-case groups + IDs).
- `refs.py` — the shared "References & sources" section for the MvC2 set.

**KOF XI — Athena / Terry / B. Jenet**
- `build_kof.py` — builds all three KOF guides. `python3 tools/build_kof.py`
- `chardata.py` — per-character data (bio, movelist, combos, strategy, matchups).
- `bjenet_combos.py` — auto-generated B. Jenet combo list (from FAQ 44220).
- `athena_matchups.py` — auto-generated Athena matchup chart (from FAQ 51436).
- `refs_kof.py` — the shared "References & sources" section for the KOF set.

**Helpers (research + QA)**
- `kof_fetch.sh` — fetch a Cloudflare-walled GameFAQs FAQ as raw text via the **Wayback Machine**.
  `tools/kof_fetch.sh arcade/928580-the-king-of-fighters-xi 44141 raw.html`
- `kof_convert.py` — extract FAQ prose from a saved page, and convert specific FAQs into the
  committed `bjenet_combos.py` / `athena_matchups.py` data files. `python3 tools/kof_convert.py extract raw.html > faq.txt`
- `fitcheck.js` — render-check a guide: horizontal overflow at 411px + every `section.screenfit`
  vs the ~418px one-screen budget. `cd tools && npm i puppeteer-core && node fitcheck.js ../guides/kofxi/kofxi-terry.html`

## Regenerating a guide

```bash
python3 tools/build.py        # mvc2 combo dojo
python3 tools/build3.py       # mvc2 advanced
python3 tools/build_kof.py    # all three kof xi guides
```

Scripts resolve paths relative to themselves (assets here in `tools/`, output under `../guides/`),
so they run from anywhere. After regenerating, refresh the index fallback list:

```bash
python3 -c "import json,glob; open('manifest.json','w').write(json.dumps(sorted(glob.glob('guides/**/*.html', recursive=True)), indent=2)+'\n')"
```

## Conventions (see also `instructions/` and `CLAUDE.md`)

- Normals render as coloured keycaps; **special moves/supers render as named pills** with the input
  in the `title=` tooltip. Every combo gets a stable ID (`CA-01`, `BJ-07`…) assigned in display order.
- Combos are grouped by **use-case** and paginated into one-screen practice cards measured with
  `fitcheck.js` (≤ ~418px tall at 411px wide).
- GameFAQs is Cloudflare-walled → always fetch sources through `kof_fetch.sh` (Wayback).
- Old SNK/Capcom FAQs use 6-button naming; normalise to the game's real button count
  (MvC2 = LP/HP/LK/HK; KOF = A/B/C/D + E) and fold the duplicate routes that creates.
