# Proposed input-notation abbreviations

A pitch for replacing the directional **arrow glyphs** (`↓↘→`, `→↓↘`, `[←]→`, …) in the
fighting-game guides with short **text abbreviations** (`QCF`, `DP`, `[B]F`, …).

## Why change

Arrows are **absolute screen directions**, so they're only correct while the character faces
**right**. The moment a character is on the right side of the screen, every `→` should be read as
`←`. Letter notation fixes this because it's written **relative to the way the character faces**:

- `F` = *toward the opponent* (forward), `B` = *away* (back) — correct on either side.
- `U`/`D` (up/down) are unaffected by facing, so they stay literal.

That single property — facing-relative — is the whole reason to switch. The motion names below
(`QCF`, `DP`, etc.) are the long-established FGC standard and already half-present in the guides
(the MvC2 *All three — one screen* card has a `motlegend` that maps `↓↘→ → QCF`, `↓↙← → QCB`,
`→↓↘ → DP`, `→↘↓↙← → HCB`). This proposal makes that mapping the *single* notation everywhere.

---

## 1. Directions (1–2 chars) — the building blocks

| Token | Meaning            | Old arrow | Numpad |
|-------|--------------------|-----------|--------|
| `N`   | neutral (no input) | –         | `5`    |
| `U`   | up (jump)          | `↑`       | `8`    |
| `D`   | down (crouch)      | `↓`       | `2`    |
| `F`   | forward            | `→`       | `6`    |
| `B`   | back               | `←`       | `4`    |
| `UF`  | up-forward         | `↗`       | `9`    |
| `UB`  | up-back            | `↖`       | `7`    |
| `DF`  | down-forward       | `↘`       | `3`    |
| `DB`  | down-back          | `↙`       | `1`    |

> Single arrows currently in the guides (`→ ← ↓ ↑ ↘ ↙ ↗`) map 1:1 onto these.

## 2. Standard motions (2–3 chars) — the main replacements

| Token | Name                          | Old arrow | Numpad   | In guides now? |
|-------|-------------------------------|-----------|----------|----------------|
| `QCF` | quarter-circle forward        | `↓↘→`     | `236`    | yes            |
| `QCB` | quarter-circle back           | `↓↙←`     | `214`    | yes            |
| `HCF` | half-circle forward           | `←↙↓↘→`   | `41236`  | future         |
| `HCB` | half-circle back              | `→↘↓↙←`   | `63214`  | yes            |
| `DP`  | dragon punch (Z-motion)       | `→↓↘`     | `623`    | yes            |
| `RDP` | reverse dragon punch          | `←↓↙`     | `421`    | future         |
| `360` | full circle (a.k.a. `FC`)     | full roll | `632147` | future         |
| `720` | double full circle            | ×2 roll   | –        | future         |

Notes / judgment calls:

- **`360` over `FC`.** `360` is universally read as "spin the stick once" (grapplers: Zangief,
  Clark, Hugo). I'd keep `360` as primary and allow `FC` only if a 2-char form is needed in a
  tight one-screen card. `720` for the double.
- **`DP`** already carries the "dragon punch / Z-motion / `f,d,df`" gloss in the guides — keep that
  in the `title=`/legend.

## 3. Charge motions — the one bracketed exception

Charge moves need to show *hold this, then tap that*. The bracket **is** the notation for "hold,"
so this family keeps brackets rather than forcing a pure 2–3-letter form:

| Token  | Name                         | Old arrow | Numpad  |
|--------|------------------------------|-----------|---------|
| `[B]F` | charge back, then forward    | `[←]→`    | `[4]6`  |
| `[D]U` | charge down, then up         | `[↓]↑`    | `[2]8`  |

(Guile, Bison, Balrog, Blanka, Honda, Vega — all charge characters. The guides already use
`[←]→` with the gloss "charge (hold back, then forward)"; `[B]F` is the facing-relative version.)

## 4. Modifiers & repeats

| Token         | Meaning                                   | Example                      |
|---------------|-------------------------------------------|------------------------------|
| `×2` / `x2`   | do the motion twice (typical super input) | `QCFx2` = `↓↘→↓↘→` (super)   |
| `×3`          | three reps                                | `QCFx3`                      |

> Convention note: the wikis more commonly **prefix** the count — `2QCF` / `236236` for the double
> quarter-circle super, `22` for down-down. `QCFx2` reads fine for beginners; switch to `2QCF` if
> you want to match SuperCombo/Dustloop exactly. (360s are also written `SPD`.)
| `FF`          | tap forward twice = dash forward          | `→→` today                   |
| `BB`          | tap back twice = back-dash                | future                       |
| `air` / `j.`  | perform while jumping (air special)       | `air QCF+P` / `j.QCF+P`      |
| `[ ]`         | hold the bracketed input                  | see charge above             |
| `~`           | "then immediately / cancel into"          | `DP~P`                       |

> `QCFx2` is the missing abbreviation for the `↓↘→↓↘→` super motion that appears ~20× across the
> guides with no text label today.

## 5. Combining motion + button

A special move = **motion + `+` + button keycap** (button keycaps stay as the existing coloured
SVG pills — they aren't arrows, so they don't change):

```
QCF+P        Spiral Arrow (any punch)
QCFx2+KK     level-3 super (both kicks)
[B]F+K       charge special
air QCB+P    air fireball
```

## 6. Uncommon / rotated motions — spell out as a token sequence

Some moves use rotations that have **no standard 2–3-letter name** — confirmed against SuperCombo,
CritPoints, and the canonical Kao_Megura MvC2 FAQ: the named canon stops at QCF/QCB/HCF/HCB/DP/RDP/
360/720/charge, and **quarter-circles that end on _down_ are outside it**.

**Decision:** spell these out as a `-`-delimited sequence of §1 tokens (`F-DF-D`) — *not* a coined
abbreviation. (`RQCF`/"reverse QCF" was considered and rejected: "reverse" in `RDP` already means
*mirrored* — `RQCF` would read as QCB, not as a QCF traced backwards. Numpad `632`/`412` was the
runner-up but adds a second notation system.) Spelling it out is exactly what the canonical FAQs do.

| Old arrow | Spelled-out token | Move (in this repo)                 |
|-----------|-------------------|-------------------------------------|
| `→↘↓`     | `F-DF-D`          | MvC2 Cyclops **Optic Sweep** (`+P`) |
| `←↙↓`     | `B-DB-D`          | MvC2 **Variable Counter** (`+A1`)   |

> Both are *correct* canonical inputs (not drawing errors). Aside: Variable Counter is lenient and
> the modern SuperCombo wiki even notates it as plain `QCF` — but per the decision above we spell it
> `B-DB-D` to match the move's drawn motion. Put the move's name in the `title=` either way.

The same rule covers SNK "pretzel" motions (e.g. Geese/Iori Raging-Storm-style inputs) and any
one-off command — spell the path with the §1 tokens and put the move's name in the `title=`.

---

## 7. Migration map — every glyph currently in the guides → token

| Current glyph | Current gloss                     | New token   |
|---------------|-----------------------------------|-------------|
| `↓↘→`         | quarter-circle forward (QCF)      | `QCF`       |
| `↓↙←`         | quarter-circle back (QCB)         | `QCB`       |
| `→↓↘`         | dragon punch (DP / Z / f,d,df)    | `DP`        |
| `→↘↓↙←`       | half-circle back (HCB)            | `HCB`       |
| `↓↘→↓↘→`      | double quarter-circle (super)     | `QCFx2`     |
| `→↘↓`         | "Forward to down"                 | `F-DF-D`    |
| `←↙↓`         | "Back, down-back, down"           | `B-DB-D`    |
| `[←]→`        | charge (hold back, then forward)  | `[B]F`      |
| `→→`          | tap forward twice (dash)          | `FF`        |
| `→`           | forward                           | `F`         |
| `←`           | back                              | `B`         |
| `↓`           | down                              | `D`         |
| `↑`           | up                                | `U`         |
| `↘`           | down-forward                      | `DF`        |
| `↙`           | down-back                         | `DB`        |
| `↗`           | up-forward ("then up-forward")    | `UF`        |

This list covers **100% of the arrow glyphs** found across the existing guides (mvc2 + garou).
Tetris and the non-fighting archives use no move notation, so they're unaffected.

## 8. Forward-looking tokens (not used yet, included for completeness)

So a future SF/KOF/Capcom/SNK guide needs no new scheme: `HCF`, `RDP`, `360`/`FC`, `720`, `[D]U`,
`BB`, double-motion supers (`HCBx2`, `QCBx2`), and the §6 spell-out rule for pretzel motions.

---

## Open questions for you

1. **`air` vs `j.`** for "in the air" — `air` (current) is friendlier for beginners; `j.` is the
   FGC standard and more compact for one-screen cards. Pick one and use it everywhere.
2. **`360` vs `FC`** as the primary full-circle token (see §2). I lean `360`.
3. Keep the descriptive `title=` tooltips (e.g. `title="Quarter-circle forward (QCF)"`) on each
   token so hovering still explains it — recommended, since the abbreviations are terser than the
   arrows were.
