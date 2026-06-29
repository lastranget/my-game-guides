---
aliases:
  - Fighting-game guide sets
  - beginner combo advanced guide set
  - mvc2 three-guide method
tags:
  - type/reference
  - concept/fighting-games
  - concept/guide-structure
---

# Fighting-game guide sets — beginner, combo, advanced

How this repo builds a **set of three companion guides** for a fighting-game character or team
(MvC2 so far; KOF XI uses the same shape). It is the AGGREGATE-mode output format that sits on top
of the main playbook (*Scraping a Website into a Single Self-Contained HTML File*) — read that first
for sourcing (Wayback/Cloudflare), the OLED-black Thor styling, the input glyphs (§11), and the
facing-relative notation (`docs/input-notation.md`). This doc is only about **what the three guides
are and what each must contain.**

> [!important] One subject → three standalone guides
> A character or team gets **three separate, self-contained HTML files** (no cross-file links — name
> siblings in plain text only):
> 1. **Beginner** — `…-<team>.html`: learn the game and the team from zero.
> 2. **Combo dojo** — `…-<team>-combos.html`: every combo, grouped + ID'd, with single-screen practice cards.
> 3. **Advanced** — `…-<team>-advanced.html`: strategy, team-building, matchups, habits.
>
> They share one toolchain in `tools/` (a `gen.py` glyph/DSL library, one `style.css`/`app.js`, a
> per-set `refs_*.py`, a data module, and a builder). Build later guides by **reusing** those
> components, not re-deriving them. Record each guide in `tools/build-map.json`.

> [!tip] Variants — adapt the set to the game
> The three-guide split is the default, but match it to the subject:
> - **1-on-1 game (no team), per-character** (e.g. Vampire Savior — B.B. Hood / Morrigan / Lilith /
>   Felicia): the advanced material is thinner (no assists/DHC), so **combine beginner + advanced**
>   into one guide. Drop the team sections; the "system overview" still teaches the whole game. **If
>   the per-section content is short, fold the combos in too** — one self-contained `vsavior-<char>.html`
>   per character (the VS set ended up as a single file each: system → strengths/weaknesses → movelist
>   → strategy → combos-by-use-case → combo screens → one-screen specials → references). Split into a
>   separate `-combos.html` only when the combo list is big enough to warrant its own file.
> - **6-button games** (Vampire Savior: LP/MP/HP, LK/MK/HK): keep the established colours — light/hard
>   punch = green/blue, light/hard kick = yellow/red on the face buttons — and put the **mediums (MP/MK)
>   on the grey shoulders** (`gen.py` has `MP`/`MK` keycaps). KOF's blowback `E` is likewise grey.
> - **When a source has no combo list** (movelist-only FAQs), author combos from the game's documented
>   chain/cancel rules + the verified movelist, and **say so** in the guide and the References note.

---

## Cross-cutting requirements (all three)

- **Self-contained.** Every file works opened from disk: inline CSS/JS, no external assets, no
  cross-file links. The only off-file links allowed are the **external citation links** in the
  References section.
- **References & sources section** (`id="refs"`, in the TOC) in **all three** guides: the source FAQs
  by title + author with live links, plus a one-line note that inputs were normalised and read via
  the Wayback Machine. (One shared `refs_*.py` renders it.)
- **Notation.** Facing-relative text tokens (`QCF`/`DP`/`[B]F`…, per `docs/input-notation.md`) with a
  **notation ledger** + button-colour legend near the top. Normalise old 6-button FAQ naming to the
  game's real button count (MvC2 = LP/HP/LK/HK; KOF = A/B/C/D + E) and fold the duplicate routes that
  creates.
- **Specials by name.** In combos, render special moves/supers as **named accent-coloured pills**
  (input in the `title=` tooltip); keep normals as coloured keycaps.
- **Validate** every file (see the playbook §9): broken anchors = 0; no horizontal overflow at 411px;
  one-screen sections within budget (below); no leaked local paths; render-check with `tools/fitcheck.js`.

> [!important] Single-screen views — the rule
> A "single-screen" card must fit the AYN Thor bottom screen: at **411px wide**, the section's
> `h2-top → section-bottom` height must be **≤ ~418px** (viewport 472 − the 54px `scroll-padding-top`).
> Always **measure** with `tools/fitcheck.js`, never eyeball.
> - **Special-move one-screen card — one per character, in the beginner *and* combo guides.** Specials
>   + supers + launcher + assist, shrunk (`.card.onescreen`) to fit. This is the "copy the final
>   section" deliverable.
> - **All-three trio card** (`.card.tiny`, 3 columns) — include it as the *last* one-screen section.
>   It is allowed to exceed 418px because it targets the **853px top screen** (verify ≤ ~426px there).
> - **Combo practice cards — in the combo dojo only.** Paginate *every* combo into compact
>   single-screen pages (`.card.combo-screen`); chunk by a weight budget (short = 1, medium = 2,
>   long = 3 action pieces; ~6 per page) and measure each page. Title them "X — combo screen i/n" so
>   the user can flip through them. Multiple screens per character is expected and fine.

---

## 1. Beginner guide (`…-<team>.html`)

**Purpose:** someone who has never opened the game can sit down and play this team using only this file.

Required sections (in order):
1. **Start here / controls** — button-colour legend + notation ledger.
2. **How the game works** — the *complete* command list and **every** universal/system mechanic
   (movement, block/air-guard, advancing guard, throws, super jump, launcher→aerial-rave, magic
   series, OTG, tech roll; and team mechanics: variable assist, variable counter, variable
   combination, snapback, DHC, super meter). Terse rows grouped Movement / Defence / Offence / Team.
   This is the "teach the whole game" prefix the main playbook mandates.
3. **How to play this team** — each character's role, the team order, the chosen assists (α/β/γ) and
   *why*, the glue (usually anti-air), and a first-day game plan.
4. **Learning path** — an ordered list of what to drill first → last.
5. **First combos** — one to three **core** combos per character (the full set lives in the dojo).
6. **Movesets — full reference** — grouped per character (command / special / hyper / normals).
7. **Single-screen specials** — one card per character + the trio (see the single-screen rule).
8. **References.**

## 2. Combo dojo (`…-<team>-combos.html`)

**Purpose:** every combo to drill, organised and addressable.

Required:
1. **How to read** — legend + notation + a short combo-vocabulary note.
2. **All combos by use-case** — *every* combo from the sources, grouped by what it's *for*
   (Ground BnB / anti-air / into-super / aerial-rave / OTG-relaunch / special-cancel & links /
   corner & loops / throws & resets / team-DHC), each with a **stable unique ID** (`FE-01`, `CY-07`…)
   assigned in display order, a difficulty marker (`●○○`), hit count where known, and a `core` badge
   on staples.
3. **Single-screen combo cards** — the paginated practice pages (see the rule). Every combo ID that
   appears in the detailed listing must also appear on a combo screen.
4. **Single-screen specials** — the per-character cards + trio (so the dojo is usable standalone).
5. **References.**

## 3. Advanced guide (`…-<team>-advanced.html`)

**Purpose:** strategy and team mastery once moves + combos are known.

Required (include the ones the sources actually support; skip a per-character block if a source has
nothing):
1. **How to read** — legend.
2. **Strengths & weaknesses** — a card per character (green pros / red cons).
3. **Assist reference** — α/β/γ per character with the input and *why*, and the team's pick.
4. **Neutral & spacing** — per character: pokes, anti-airs, approach/zoning.
5. **Defense & escaping pressure** — push-block, variable counter, reversals, air-guard limits,
   tech roll, safe DHC bail, snapback.
6. **Meter & DHC routes** — when to spend; the team's specific DHC kill / rescue routes (rendered as
   combos).
7. **Mind games & resets** — tick-throws, cross-ups, OTG resets, pattern-breakers.
8. **Matchups** — whatever the sources give (often only the anchor / point character has a real
   matchup chart; condense long paragraphs and say so). Note where matchup data is thin.
9. **Common mistakes** — a "habits to break" list.
10. **References.**

---

## Process checklist ➕ 2026-06-28

- [ ] Decide the set: which three characters, who's point/glue/anchor, the assists. Confirm the
  button→Thor mapping only if no convention exists yet (there's a standing one — reuse it).
- [ ] Fetch + read **all** the source FAQs (Wayback). Auto-convert regular combo/matchup lists with a
  `tools/`-style script; hand-transcribe prose-described ones.
- [ ] Author data module + reuse the builder; assign combo IDs in display order; group by use-case.
- [ ] Build all three; add the References section to each.
- [ ] Make the single-screen views per the rule; **measure** with `fitcheck.js` and paginate combos.
- [ ] Validate (anchors, 411px overflow, one-screen fit, no leaks); regenerate `manifest.json`.
- [ ] Record the guides in `tools/build-map.json` and the README table; commit + push.
