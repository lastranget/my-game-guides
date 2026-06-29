# -*- coding: utf-8 -*-
"""Assemble mvc2-cammy-bbhood-cyclops-combos.html (AGGREGATE mode, combo-focused)."""
import os as _os
_HERE=_os.path.dirname(_os.path.abspath(__file__))
_REPO=_os.path.dirname(_HERE)
import math
from gen import (keycap, mot, dirp, render_action, render_combo,
                 G, GP, GC, JG, M, MA, DB, CH, SQ, DIR, SP, PRE, TAG, PLUS, AIR)
from data import COMBOS, GROUPS, META, ORDER
from refs import references_section

OUT = _os.path.join(_REPO,'guides','mvc2','mvc2-cammy-bbhood-cyclops-combos.html')

# Re-assign IDs contiguously in display order (group order, stable within group)
# so detailed listing and single-screen pages share one ascending, gap-free scheme.
PREFIX = {'cammy': 'CA', 'bbhood': 'BB', 'cyclops': 'CY'}
GORDER = {k: i for i, (k, _) in enumerate(GROUPS)}
for _ch in ORDER:
    COMBOS[_ch].sort(key=lambda c: GORDER[c['grp']])
    for _i, _c in enumerate(COMBOS[_ch], 1):
        _c['id'] = f"{PREFIX[_ch]}-{_i:02d}"

# ---- raw helper for odd moveset inputs (Stalking) ----
def raw(h): return ('raw', h)

def render_action2(pc):
    if pc[0] == 'raw':
        return pc[1]
    return render_action(pc)

def render_moveinput(pieces):
    parts = []
    for pc in pieces:
        if pc[0] in ('tag', 'pre'):
            parts.append(f'<span class="ann">{pc[1]}</span>')
        else:
            parts.append(render_action2(pc))
    return '<span class="in">' + ''.join(parts) + '</span>'

STALK = raw('<span class="grp"><span class="dir" title="down, down">D</span>'
            '<span class="dir" title="down">D</span><span class="plus">+</span>'
            + keycap('LK') + keycap('HK') + '</span>')

# ---- moveset data (verbatim content from the sibling guide's reference) ----
MOVES = {
 'cammy': [
   ('Spiral Arrow / Cannon Drill', 'air OK · OTGs', [M('QCF','K')]),
   ('Cannon Spike', 'anti-air', [M('DP','K')]),
   ('Cannon Strike (divekick)', '', [MA('QCB','K')]),
   ('Axel Spin Knuckle', '', [M('QCF','P')]),
   ('Cannon Revenge (counter)', '', [M('HCB','P')]),
   ('Launcher', '', [G('HK'), TAG('or'), DB('D','HP')]),
   ('SUPER · Spin Drive Smasher', '', [M('QCF','KK')]),
   ('SUPER · Killer Bee Assault', 'air OK', [MA('QCB','PP')]),
   ('SUPER · Reverse Shaft Breaker', 'mash', [M('QCB','KK')]),
   ('Assist (α) Cannon Spike', 'AAA / counter', [G('A1')]),
 ],
 'bbhood': [
   ('Smile &amp; Missile (missiles)', 'charge · HP knocks down · K = low', [CH('[B]F','P')]),
   ('Hop &amp; Missile', 'charge · air missile, situational', [CH('[D]U','P')]),
   ('Cheer &amp; Fire (flame)', 'her anti-air · K = straight shot', [M('DP','P')]),
   ('Shyness Strike (basket)', 'knockdown · cancels into super', [M('QCB','P')]),
   ('Stalking (crawl)', 'crawl under fireballs &amp; cross up', [STALK]),
   ('Basket Swing', 'one of her longer-range pokes', [DB('F','HP')]),
   ('Launcher', 'weak — air combos are minor', [DB('DF','HK')]),
   ('SUPER · Cool Hunting (guns)', 'combos · huge block damage', [M('QCF','PP')]),
   ('SUPER · Beautiful Memory', 'big damage · all-or-nothing', [M('HCF','KK')]),
   ('SUPER · Hyper Apple For You', 'unblockable grab · vs turtles', [M('HCB','KK')]),
   ('Assist (α) Fierce Missile', 'knockdown projectile', [G('A1')]),
 ],
 'cyclops': [
   ('Optic Blast (beam)', 'air OK · HP angles up', [M('QCF','P')]),
   ('Gene Splice', 'anti-air · mash', [M('DP','P')]),
   ('Cyclone Kick', 'combo finisher', [M('QCB','K')]),
   ('Optic Sweep', 'OTG', [SQ('F-DF-D','P')]),
   ('Running Tackle', 'unblockable', [CH('[B]F','K')]),
   ('Charging Punches', 'mash', [CH('[B]F','P')]),
   ('Launcher', '', [DB('DF','HP'), TAG('or'), DB('DF','HK')]),
   ('SUPER · Mega Optic Blast', 'the DHC ender', [M('QCF','PP')]),
   ('SUPER · Super Optic Blast', 'aimable', [M('QCF','KK')]),
   ('Assist (β) Gene Splice', 'elite AAA', [G('A1')]),
 ],
}

# ============================================================= renderers
def diff_dots(d):
    return '●' * d + '○' * (3 - d)

def n_actions(seq):
    return sum(1 for pc in seq if pc[0] in ('grp','mot','dir','chg','seq','sp','dir1'))

def combo_card(c, compact=False):
    badge = ' <span class="corez" title="also in the beginner guide">core</span>' if c['core'] else ''
    head = (f'<div class="cmb-h"><span class="cid">{c["id"]}</span><b>{c["name"]}</b>'
            f'<span class="diff" title="difficulty {c["diff"]}/3">{diff_dots(c["diff"])}</span>{badge}</div>')
    body = render_combo(c['seq'])
    if compact:
        return f'<div class="cmb">{head}{body}</div>'
    note = f'<div class="cmb-note">{c["note"]}</div>' if c.get('note') else ''
    return f'<div class="cmb">{head}{body}{note}</div>'

def detailed_block(char):
    m = META[char]
    out = [f'<div class="ccombo" id="d-{char}" style="--ca:{m["ca"]}">'
           f'<h3>{m["name"]} <span class="role">· {m["role"]}</span></h3>']
    combos = COMBOS[char]
    for gkey, glabel in GROUPS:
        grp = [c for c in combos if c['grp'] == gkey]
        if not grp:
            continue
        out.append(f'<div class="ucg">{glabel}</div>')
        for c in grp:
            out.append(combo_card(c, compact=False))
    out.append('</div>')
    return ''.join(out)

def chunk_pages(combos, budget=8):
    pages, cur, w = [], [], 0
    for c in combos:
        na = n_actions(c['seq'])
        wt = 1 if na <= 4 else (2 if na <= 7 else 3)
        if cur and w + wt > budget:
            pages.append(cur); cur, w = [], 0
        cur.append(c); w += wt
    if cur:
        pages.append(cur)
    return pages

def screen_sections(char, budget=8):
    m = META[char]
    pages = chunk_pages(COMBOS[char], budget)
    n = len(pages)
    secs = []
    for i, page in enumerate(pages, 1):
        first = ' id="screens-%s"' % char if i == 1 else ''
        cards = ''.join(combo_card(c, compact=True) for c in page)
        secs.append(
            f'<section class="block screenfit"{first}>'
            f'<h2>{m["name"]} — combo screen {i}/{n}'
            f'<a href="#toc" class="bt">contents ↑</a></h2>'
            f'<div class="card combo-screen" style="--ca:{m["ca"]}">'
            f'<div class="card-h"><b>{m["name"]}</b><span>combos {page[0]["id"]}–{page[-1]["id"]}</span></div>'
            f'<div class="cscreen">{cards}</div></div></section>')
    return ''.join(secs), n

def moveset_card(char, onescreen=True):
    m = META[char]
    cls = 'card onescreen' if onescreen else 'card'
    rows = []
    for name, note, pieces in MOVES[char]:
        notespan = f' <span class="note">{note}</span>' if note else ''
        rows.append(f'<div class="mv"><span class="nm">{name}{notespan}</span>'
                    f'{render_moveinput(pieces)}</div>')
    return (f'<div class="{cls}" style="--ca:{m["ca"]}">'
            f'<div class="card-h"><b>{m["name"]}</b><span>{m["role"]}</span></div>'
            f'<div class="ms">{"".join(rows)}</div></div>')

def trio_card(char):
    m = META[char]
    rows = []
    for name, note, pieces in MOVES[char]:
        rows.append(f'<div class="mv"><span class="nm">{name}</span>{render_moveinput(pieces)}</div>')
    return (f'<div class="card tiny" style="--ca:{m["ca"]}">'
            f'<div class="card-h"><b>{m["name"]}</b><span>{m["role"]}</span></div>'
            f'<div class="ms">{"".join(rows)}</div></div>')

# ============================================================= legends
def button_legend():
    items = [
        ('LP','Light Punch — green (Y)'), ('HP','Hard Punch — blue (X)'),
        ('LK','Light Kick — yellow (B)'), ('HK','Hard Kick — red (A)'),
        ('A1','Assist 1 — grey trigger'), ('A2','Assist 2 — grey trigger'),
        ('P','any Punch'), ('K','any Kick'),
        ('PP','both Punches (super)'), ('KK','both Kicks (super)'),
    ]
    lg = ''.join(f'<div class="lg"><span>{keycap(t)}</span><span>{d}</span></div>' for t, d in items)
    return (f'<div class="legendwrap"><div class="leg-grid">{lg}</div>'
            f'<p class="note2">MvC2 has only four attack buttons — two punches (LP/HP) and two kicks '
            f'(LK/HK) — plus two assists. There is <b>no medium attack</b> like in Street Fighter, so '
            f'old 6-button FAQ notation (jab/strong/fierce) is folded onto these four here.</p></div>')

def notation_ledger():
    mots = [('QCF','quarter-circle fwd'), ('QCB','quarter-circle back'), ('HCF','half-circle fwd'),
            ('HCB','half-circle back'), ('DP','dragon punch'), ('F-DF-D','fwd, down-fwd, down')]
    dirs = [('[B]F','charge back→fwd'), ('[D]U','charge down→up'), ('F','forward (to foe)'),
            ('B','back (away)'), ('U','up'), ('D','down'), ('DF','down-fwd'), ('DB','down-back')]
    rows = ''.join(f'<div class="lg"><span>{mot(t)}</span><span>{d}</span></div>' for t, d in mots)
    rows += ''.join(f'<div class="lg"><span>{dirp(t)}</span><span>{d}</span></div>' for t, d in dirs)
    return (f'<div class="legendwrap" id="notation">'
            f'<div class="motlegend" style="margin-top:0;line-height:1.5">Motions are written '
            f'<b>relative to your facing</b> — <b>F</b> = toward the opponent, <b>B</b> = away — so they '
            f'read correctly on <b>both</b> sides of the screen.</div>'
            f'<div class="leg-grid">{rows}</div></div>')

# combo vocabulary (system mechanics combos rely on) — keeps the file self-contained
VOCAB = [
 ('Magic series', 'The ground/air chain. Press attacks weak→strong — <b>LP → LK → HP → HK</b> — '
                  'each link cancels into the next. Tapping a light twice climbs the series.'),
 ('Launcher', 'A <b>HK</b> or <b>D/DF+HP</b> hit that pops the foe up; you auto-<b>super-jump</b> after to '
              'chase them — that is an <b>Aerial Rave</b>.'),
 ('Super jump (SJ)', 'Flick <span class="dir">D</span>→<span class="dir">U</span> to leap high after a launch.'),
 ('Double jump (dj)', 'Press <span class="dir">U</span> again in the air. Only some characters (Cyclops, BB Hood) have it.'),
 ('XX — cancel', 'Interrupt a move’s recovery into a special or super, e.g. a chain <b>XX</b> Cyclone Kick.'),
 ('Super-cancel', 'Cancel a <i>special</i> into a <i>super</i> (e.g. basket <b>XX</b> Cool Hunting).'),
 ('OTG', '“Off the ground.” Some moves hit a downed foe — letting you OTG-relaunch for more.'),
 ('DHC', 'Delayed Hyper Combo — cancel one character’s super into a partner’s super for team damage.'),
 ('Charge', '<span class="dir">[B]F</span> = hold back ~1s then press forward+button. <span class="dir">[D]U</span> = hold down, then up.'),
 ('mash', 'Tap the button rapidly to add hits (Gene Splice, Charging Punches, Reverse Shaft Breaker).'),
 ('Assist / snapback', 'A1/A2 call a partner. <b>QCF+A</b> (1 bar) snaps the foe’s point character out.'),
]
def vocab_block():
    rows = ''.join(f'<div class="sysrow"><div class="top"><span class="nm">{n}</span></div>'
                   f'<div class="dsc">{d}</div></div>' for n, d in VOCAB)
    return f'<div class="sys">{rows}</div>'

# ============================================================= page
def build():
    css = open(_os.path.join(_HERE,'style.css')).read()
    js = open(_os.path.join(_HERE,'app.js')).read()
    defs = ('<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>'
            '<linearGradient id="gp" x1="0" x2="1" y1="0" y2="0"><stop offset="50%" stop-color="#2fb84a"/>'
            '<stop offset="50%" stop-color="#2f86f0"/></linearGradient>'
            '<linearGradient id="gk" x1="0" x2="1" y1="0" y2="0"><stop offset="50%" stop-color="#f2c531"/>'
            '<stop offset="50%" stop-color="#ec3b3b"/></linearGradient></defs></svg>')

    # detailed combos
    detailed = ''.join(detailed_block(c) for c in ORDER)
    total = sum(len(COMBOS[c]) for c in ORDER)

    # single-screen combo pages
    screens, screen_counts = {}, {}
    for c in ORDER:
        s, n = screen_sections(c, budget=6)
        screens[c] = s; screen_counts[c] = n

    # one-screen movesets
    move_secs = ''.join(
        f'<section class="block screenfit" id="moves-{c}">'
        f'<h2>{META[c]["name"]} — special moves (one screen)<a href="#toc" class="bt">contents ↑</a></h2>'
        f'{moveset_card(c)}</section>' for c in ORDER)
    trio_sec = (f'<section class="block screenfit trio-sec" id="moves-all">'
                f'<h2>All three — special moves on one screen<a href="#toc" class="bt">contents ↑</a></h2>'
                f'<div class="trio">{"".join(trio_card(c) for c in ORDER)}</div></section>')

    # TOC
    toc = (
      '<nav id="toc"><div class="toc-head"><h2>Contents</h2></div><ul class="toc-top">'
      '<li><a href="#how">How to read these combos</a></li>'
      '<li><a href="#combos">All combos by use-case</a></li>'
      '<li><a href="#d-cammy">— Cammy combos</a></li>'
      '<li><a href="#d-bbhood">— BB Hood combos</a></li>'
      '<li><a href="#d-cyclops">— Cyclops combos</a></li>'
      f'<li><a href="#screens-cammy">Cammy — combo screens (×{screen_counts["cammy"]})</a></li>'
      f'<li><a href="#screens-bbhood">BB Hood — combo screens (×{screen_counts["bbhood"]})</a></li>'
      f'<li><a href="#screens-cyclops">Cyclops — combo screens (×{screen_counts["cyclops"]})</a></li>'
      '<li><a href="#moves-cammy">Cammy — special moves</a></li>'
      '<li><a href="#moves-bbhood">BB Hood — special moves</a></li>'
      '<li><a href="#moves-cyclops">Cyclops — special moves</a></li>'
      '<li><a href="#moves-all">All three — special moves</a></li>'
      '<li><a href="#refs">References &amp; sources</a></li>'
      '</ul></nav>')

    intro = (
      '<p class="intro">A <b>combo dojo</b> for the <b>Cammy / BB Hood / Cyclops</b> team in '
      '<b>Marvel vs. Capcom 2</b> — a companion to the beginner guide, focused entirely on things to '
      f'practice. <b>{total} combos</b>, each with a reference <b>ID</b> (e.g. '
      '<span class="cid" style="--ca:#7cc0ff">CY-01</span>), grouped by what they are <i>for</i>. '
      'Specials are shown by <b>name</b> (hover for the input); the raw inputs are in the '
      '<a href="#moves-cammy">special-move screens</a> at the end. After the full listing, each '
      'character has <b>single-screen practice cards</b> sized to your AYN&nbsp;Thor — flip through them '
      'in training mode.</p>')

    how = (
      f'<section class="block" id="how"><h2>How to read these combos<a href="#toc" class="bt">contents ↑</a></h2>'
      f'<p>Combos read left → right; a faint <span class="cs">›</span> separates steps, '
      f'<span class="ann">italics</span> are notes (<span class="ann">launch</span>, '
      f'<span class="ann">SJ</span>, <span class="ann">OTG</span>, <span class="ann">XX</span>, '
      f'<span class="ann">dash</span>). Normals are coloured buttons that match your Thor face buttons; '
      f'a named pill like a special move means “do that move” (hover it for the motion). '
      f'Difficulty is <span class="diff">●○○</span>–<span class="diff">●●●</span>; '
      f'<span class="corez">core</span> marks the staples carried over from the beginner guide.</p>'
      f'{button_legend()}{notation_ledger()}'
      f'<h3>Combo vocabulary &amp; the mechanics they use</h3>'
      f'<p class="note2">Everything the routes below rely on. (The full command list &amp; all team/'
      f'system mechanics live in the sibling beginner guide, <i>mvc2-cammy-bbhood-cyclops.html</i>.)</p>'
      f'{vocab_block()}</section>')

    combos_sec = (
      f'<section class="block" id="combos"><h2>All {total} combos — by use-case'
      f'<a href="#toc" class="bt">contents ↑</a></h2>'
      f'<p class="note2">Grouped by what each combo is <i>for</i>. Reference any by its ID. '
      f'Sourced from the GameFAQs character guides (Johmeriquai, The&nbsp;fireboy, ABrea, G-Boy, '
      f'Z-Force, PhatDan81, TBui) and normalised to MvC2’s four buttons.</p>'
      f'{detailed}</section>')

    body = (
      f'<header class="bar"><span class="title">MvC2 Combos — Cammy · BB Hood · Cyclops</span>'
      f'<a class="jump" href="#toc">Contents</a></header>'
      f'<div class="wrap">'
      f'<h1>Cammy / BB Hood / Cyclops — the combo dojo</h1>'
      f'{intro}{toc}{how}{combos_sec}'
      f'{screens["cammy"]}{screens["bbhood"]}{screens["cyclops"]}'
      f'{move_secs}{trio_sec}{references_section()}'
      f'</div>'
      f'<a href="#top" id="totop" aria-label="Back to top">↑</a>'
      f'<script>{js}</script>')

    doc = (
      '<!DOCTYPE html>\n<html lang="en">\n<head>\n'
      '<meta charset="utf-8">\n'
      '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
      '<meta name="color-scheme" content="dark">\n'
      '<title>MvC2 — Cammy / BB Hood / Cyclops (combo dojo)</title>\n'
      f'<style>{css}</style>\n</head>\n<body id="top">\n{defs}\n{body}\n</body>\n</html>\n')

    with open(OUT, 'w') as f:
        f.write(doc)
    print('combos:', {c: len(COMBOS[c]) for c in ORDER}, 'total', total)
    print('screens:', screen_counts)
    print('wrote', OUT, len(doc), 'bytes')

if __name__ == '__main__':
    build()