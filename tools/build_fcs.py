# -*- coding: utf-8 -*-
"""Build the Felicia / Cyclops / Storm MvC2 guide set: beginner, combo, advanced.
Reuses gen.py (glyphs + combo DSL) + style.css + app.js. Data in fcs_data.py."""
import os as _os
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_REPO = _os.path.dirname(_HERE)

from gen import keycap, mot, dirp, render_action, render_combo, M, MA, DB, SQ, SP, G, TAG, PRE
from fcs_data import META, ORDER, COMBO_GROUPS, COMBOS, MOVES, ONESCREEN
from storm_matchups import STORM_MATCHUPS
from refs_fcs import references_section

# ---- assign combo IDs in display (group) order ----
for ch in ORDER:
    go = {k: i for i, (k, _) in enumerate(COMBO_GROUPS)}
    COMBOS[ch].sort(key=lambda c: go.get(c['grp'], 99))
    for i, c in enumerate(COMBOS[ch], 1):
        c['id'] = f"{META[ch]['pfx']}-{i:02d}"

# ---- render helpers ----
def diff_dots(d): return '●' * d + '○' * (3 - d)
def kb(t): return keycap(t)
def mv(m, b, air=False): return render_action(MA(m, b) if air else M(m, b))
def spn(n, m, b, air=False): return render_action(SP(n, m, b, air))
def dbtn(d, b): return render_action(DB(d, b))

def render_moveinput(pieces):
    out = []
    for pc in pieces:
        if pc[0] in ('tag', 'pre'):
            out.append(f'<span class="ann">{pc[1]}</span>')
        elif pc[0] == 'raw':
            out.append(pc[1])
        else:
            out.append(render_action(pc))
    return '<span class="in">' + ''.join(out) + '</span>'

def sysrow(nm, dsc, inn=''):
    intop = f'<span class="in">{inn}</span>' if inn else ''
    return (f'<div class="sysrow"><div class="top"><span class="nm">{nm}</span>{intop}</div>'
            f'<div class="dsc">{dsc}</div></div>')

def combo_card(c, compact=False):
    badge = ' <span class="corez">core</span>' if c.get('core') else ''
    hits = f' <span class="hits">{c["hits"]}</span>' if c.get('hits') else ''
    head = (f'<div class="cmb-h"><span class="cid">{c["id"]}</span><b>{c["name"]}</b>'
            f'<span class="diff" title="difficulty {c["diff"]}/3">{diff_dots(c["diff"])}</span>{hits}{badge}</div>')
    body = render_combo(c['seq'])
    if compact:
        return f'<div class="cmb">{head}{body}</div>'
    note = f'<div class="cmb-note">{c["note"]}</div>' if c.get('note') else ''
    return f'<div class="cmb">{head}{body}{note}</div>'

# ---- legends + shared chrome ----
def button_legend():
    items = [('LP', 'Light Punch — green (Y)'), ('HP', 'Hard Punch — blue (X)'),
             ('LK', 'Light Kick — yellow (B)'), ('HK', 'Hard Kick — red (A)'),
             ('A1', 'Assist 1 — grey'), ('A2', 'Assist 2 — grey'),
             ('P', 'any Punch'), ('K', 'any Kick'), ('PP', 'both Punches'), ('KK', 'both Kicks')]
    lg = ''.join(f'<div class="lg"><span>{keycap(t)}</span><span>{d}</span></div>' for t, d in items)
    return (f'<div class="legendwrap"><div class="leg-grid">{lg}</div>'
            f'<p class="note2">MvC2 has four attack buttons — two punches (LP/HP), two kicks (LK/HK) — '
            f'plus two assists. There is no medium button; old FAQ "strong/forward" attacks are reached '
            f'by tapping a light twice in a chain.</p></div>')

def notation_ledger():
    mots = [('QCF', 'quarter-circle fwd'), ('QCB', 'quarter-circle back'), ('HCF', 'half-circle fwd'),
            ('HCB', 'half-circle back'), ('DP', 'dragon punch'), ('F-DF-D', 'fwd, down-fwd, down')]
    dirs = [('[B]F', 'charge back→fwd'), ('F', 'forward'), ('B', 'back'), ('U', 'up'),
            ('D', 'down'), ('DF', 'down-fwd')]
    rows = ''.join(f'<div class="lg"><span>{mot(t)}</span><span>{d}</span></div>' for t, d in mots)
    rows += ''.join(f'<div class="lg"><span>{dirp(t)}</span><span>{d}</span></div>' for t, d in dirs)
    return (f'<div class="legendwrap" id="notation"><div class="motlegend" style="margin-top:0;line-height:1.5">'
            f'Motions are <b>facing-relative</b> — <b>F</b> = toward the opponent, <b>B</b> = away. '
            f'A named pill (e.g. {spn("Sand Splash","QCF","K")}) is a special move — hover for the input.</div>'
            f'<div class="leg-grid">{rows}</div></div>')

def head_doc(title, css, body):
    return ('<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            '<meta name="color-scheme" content="dark">\n'
            f'<title>{title}</title>\n<style>{css}</style>\n</head>\n<body id="top">\n{DEFS}\n{body}\n</body>\n</html>\n')

DEFS = ('<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>'
        '<linearGradient id="gp" x1="0" x2="1" y1="0" y2="0"><stop offset="50%" stop-color="#2fb84a"/>'
        '<stop offset="50%" stop-color="#2f86f0"/></linearGradient>'
        '<linearGradient id="gk" x1="0" x2="1" y1="0" y2="0"><stop offset="50%" stop-color="#f2c531"/>'
        '<stop offset="50%" stop-color="#ec3b3b"/></linearGradient></defs></svg>')

def header_bar(short_title):
    return (f'<header class="bar"><span class="title">{short_title}</span>'
            f'<a class="jump" href="#toc">Contents</a></header>')

TOTOP = '<a href="#top" id="totop" aria-label="Back to top">↑</a>'

def script_tag():
    return '<script>' + open(_os.path.join(_HERE, 'app.js')).read() + '</script>'

# ---- moveset rendering (full reference + one-screen) ----
def movelist_section(ch):
    blocks = []
    for label, rows in MOVES[ch]:
        rws = ''.join(
            f'<div class="mv"><span class="nm">{nm}{(" <span class=\"note\">"+note+"</span>") if note else ""}</span>'
            f'{render_moveinput(p)}</div>' for nm, note, p in rows)
        blocks.append(f'<div class="mlgrp"><h4>{label}</h4><div class="ms">{rws}</div></div>')
    m = META[ch]
    return (f'<div class="card" style="--ca:{m["ca"]}">'
            f'<div class="card-h"><b>{m["name"]}</b><span>{m["role"]}</span></div>{"".join(blocks)}</div>')

def onescreen_section(ch):
    m = META[ch]
    rows = ''.join(
        f'<div class="mv"><span class="nm">{nm}{(" <span class=\"note\">"+note+"</span>") if note else ""}</span>'
        f'{render_moveinput(p)}</div>' for nm, note, p in ONESCREEN[ch])
    return (f'<section class="block screenfit" id="moves-{ch}">'
            f'<h2>{m["name"]} — special moves (one screen)<a href="#toc" class="bt">contents ↑</a></h2>'
            f'<div class="card onescreen" style="--ca:{m["ca"]}">'
            f'<div class="card-h"><b>{m["name"]}</b><span>{m["role"]}</span></div>'
            f'<div class="ms">{rows}</div></div></section>')

def trio_section():
    cards = []
    for ch in ORDER:
        m = META[ch]
        rows = ''.join(f'<div class="mv"><span class="nm">{nm}</span>{render_moveinput(p)}</div>'
                       for nm, note, p in ONESCREEN[ch])
        cards.append(f'<div class="card tiny" style="--ca:{m["ca"]}">'
                     f'<div class="card-h"><b>{m["name"]}</b><span>{m["role"]}</span></div>'
                     f'<div class="ms">{rows}</div></div>')
    return ('<section class="block screenfit trio-sec" id="moves-all">'
            '<h2>All three — special moves on one screen<a href="#toc" class="bt">contents ↑</a></h2>'
            f'<div class="trio">{"".join(cards)}</div></section>')

# ============================================================ MvC2 system overview (beginner)
def system_section():
    movement = ''.join([
        sysrow('Dash / run', 'Tap toward the foe twice (or press both punches). Back-back dashes away.',
               f'{dirp("F")}{dirp("F")} <span class="osep">/</span> {kb("PP")}'),
        sysrow('Super jump', 'Flick down→up to leap high — this is how you chase a launched foe for an air combo.',
               f'{dirp("D")}{dirp("U")}'),
        sysrow('Air mobility', '<b>Storm</b> has an 8-way air-dash, flight and a tri-jump; Felicia &amp; '
               'Cyclops rely on normal + super jumps (Cyclops has a double jump).', ''),
    ])
    defense = ''.join([
        sysrow('Block / air-guard', 'Hold back (high) or down-back (low). You <b>can</b> air-block air '
               'attacks/projectiles/supers — but not a grounded normal.', f'{dirp("B")} <span class="osep">/</span> {dirp("DB")}'),
        sysrow('Advancing Guard (push-block)', 'Press both punches as you block to shove the attacker off — '
               'your #1 escape from pressure.', f'{kb("PP")} <span class="ann">blocking</span>'),
        sysrow('Variable Counter', 'Tag a partner in with a counter-attack while blocking — 1 bar.',
               f'{mot("B-DB-D") if False else dirp("B")}<span class="osep">→</span>{dirp("DB")}<span class="osep">→</span>{dirp("D")}+{kb("A1")}'),
        sysrow('Tech roll', 'Tap toward/away as you land from a knockdown to roll and avoid an OTG.', ''),
    ])
    offense = ''.join([
        sysrow('Magic series', 'The chain: press attacks weak→strong (LP → LK → HP → HK); each cancels into '
               'the next. Tapping a light twice climbs the series.', f'{kb("LP")}{kb("LK")}{kb("HP")}{kb("HK")}'),
        sysrow('Launcher → Aerial Rave', 'A launching normal (often HK / DF+HP) pops them up; super-jump after '
               'to chase with an air chain.', ''),
        sysrow('OTG', '“Off the ground” — some moves hit a downed foe, letting you relaunch (Felicia &amp; '
               'Cyclops live on this).', ''),
        sysrow('Throws / snapback', 'Close f/b + HP or HK throws. <b>QCF + assist</b> (1 bar) snaps the foe’s '
               'point character out.', f'{dirp("F")}{kb("HP")}'),
    ])
    team = ''.join([
        sysrow('Variable Assist', 'Press <b>A1 / A2</b> to call a partner’s assist move (set by their α/β/γ '
               'type). The backbone of the team.', f'{kb("A1")} <span class="osep">/</span> {kb("A2")}'),
        sysrow('Variable Attack / tag', 'Tag a partner in (they enter with an attack). Order: who’s in front '
               'fights; the rest assist.', ''),
        sysrow('Variable Combination', 'Both/all on-screen supers at once (costs a bar each).', ''),
        sysrow('Delayed Hyper Combo (DHC)', 'Cancel one character’s super into a partner’s super — the team’s '
               'damage + the safe way to bring a fresh character in.', ''),
        sysrow('Super meter', 'Fills as you fight (up to 5 bars). Supers cost 1; spend on DHCs, snapbacks, or '
               'big single supers.', ''),
    ])
    return ('<section class="block" id="system"><h2>How MvC2 works — controls &amp; team mechanics'
            '<a href="#toc" class="bt">contents ↑</a></h2>'
            '<p class="note2">Everything you need to play, beyond these three characters’ own moves. '
            'MvC2 is <b>3-on-3 tag</b>: one fights, two assist.</p>'
            f'<div class="sysgrp">Movement</div><div class="sys">{movement}</div>'
            f'<div class="sysgrp">Defence</div><div class="sys">{defense}</div>'
            f'<div class="sysgrp">Offence</div><div class="sys">{offense}</div>'
            f'<div class="sysgrp">Team mechanics</div><div class="sys">{team}</div></section>')

# ============================================================ combo guide
def detailed_combos():
    out = ['<section class="block" id="combos"><h2>All combos — by use-case'
           '<a href="#toc" class="bt">contents ↑</a></h2>'
           '<p class="note2">Grouped by what each combo is <i>for</i>; reference any by its ID. Specials '
           'are shown by name (hover for the input).</p>']
    for ch in ORDER:
        m = META[ch]
        out.append(f'<div class="ccombo" id="d-{ch}" style="--ca:{m["ca"]}"><h3>{m["name"]} '
                   f'<span class="role">· {m["role"]}</span></h3>')
        for gk, gl in COMBO_GROUPS:
            grp = [c for c in COMBOS[ch] if c['grp'] == gk]
            if not grp:
                continue
            out.append(f'<div class="ucg">{gl}</div>')
            out += [combo_card(c) for c in grp]
        out.append('</div>')
    out.append('</section>')
    return ''.join(out)

def n_actions(c):
    return sum(1 for pc in c['seq'] if pc[0] in ('grp', 'mot', 'dir', 'chg', 'seq', 'sp', 'dir1'))

def combo_screens(ch, budget=6):
    pages, cur, w = [], [], 0
    for c in COMBOS[ch]:
        na = n_actions(c); wt = 1 if na <= 4 else (2 if na <= 7 else 3)
        if cur and w + wt > budget:
            pages.append(cur); cur, w = [], 0
        cur.append(c); w += wt
    if cur:
        pages.append(cur)
    m = META[ch]; n = len(pages); secs = []
    for i, page in enumerate(pages, 1):
        first = f' id="screens-{ch}"' if i == 1 else ''
        cards = ''.join(combo_card(c, compact=True) for c in page)
        secs.append(f'<section class="block screenfit"{first}><h2>{m["name"]} — combo screen {i}/{n}'
                    f'<a href="#toc" class="bt">contents ↑</a></h2>'
                    f'<div class="card combo-screen" style="--ca:{m["ca"]}">'
                    f'<div class="card-h"><b>{m["name"]}</b><span>{page[0]["id"]}–{page[-1]["id"]}</span></div>'
                    f'<div class="cscreen">{cards}</div></div></section>')
    return ''.join(secs), n


# data imported lazily to keep this file readable
import fcs_text as T  # noqa


def build_combo():
    css = open(_os.path.join(_HERE, 'style.css')).read()
    total = sum(len(COMBOS[c]) for c in ORDER)
    screens = {}; counts = {}
    for ch in ORDER:
        screens[ch], counts[ch] = combo_screens(ch)
    toc = ('<nav id="toc"><div class="toc-head"><h2>Contents</h2></div><ul class="toc-top">'
           '<li><a href="#how">How to read these combos</a></li>'
           '<li><a href="#combos">All combos by use-case</a></li>'
           '<li><a href="#d-felicia">— Felicia combos</a></li>'
           '<li><a href="#d-cyclops">— Cyclops combos</a></li>'
           '<li><a href="#d-storm">— Storm combos</a></li>'
           f'<li><a href="#screens-felicia">Felicia — combo screens (×{counts["felicia"]})</a></li>'
           f'<li><a href="#screens-cyclops">Cyclops — combo screens (×{counts["cyclops"]})</a></li>'
           f'<li><a href="#screens-storm">Storm — combo screens (×{counts["storm"]})</a></li>'
           '<li><a href="#moves-felicia">Felicia — special moves</a></li>'
           '<li><a href="#moves-cyclops">Cyclops — special moves</a></li>'
           '<li><a href="#moves-storm">Storm — special moves</a></li>'
           '<li><a href="#moves-all">All three — special moves</a></li>'
           '<li><a href="#refs">References &amp; sources</a></li></ul></nav>')
    how = ('<section class="block" id="how"><h2>How to read these combos<a href="#toc" class="bt">contents ↑</a></h2>'
           '<p>Combos read left→right with a faint <span class="cs">›</span> between steps; '
           '<span class="ann">italics</span> are notes. Difficulty is '
           '<span class="diff">●○○</span>–<span class="diff">●●●</span>; <span class="corez">core</span> marks '
           'the staples. Specials are named pills (hover for input); the raw inputs are in the '
           '<a href="#moves-felicia">special-move screens</a> below.</p>'
           + button_legend() + notation_ledger() + '</section>')
    body = (header_bar('MvC2 Combos — Felicia · Cyclops · Storm')
            + f'<div class="wrap"><h1>Felicia / Cyclops / Storm — the combo dojo</h1>'
            f'<p class="intro">A combo companion for the team — <b>{total} combos</b>, each with a reference '
            f'ID, grouped by use-case, plus single-screen practice cards for your AYN&nbsp;Thor.</p>'
            f'{toc}{how}{detailed_combos()}'
            f'{screens["felicia"]}{screens["cyclops"]}{screens["storm"]}'
            f'{onescreen_section("felicia")}{onescreen_section("cyclops")}{onescreen_section("storm")}{trio_section()}'
            f'{references_section()}</div>{TOTOP}{script_tag()}')
    out = _os.path.join(_REPO, 'guides', 'mvc2', 'mvc2-felicia-cyclops-storm-combos.html')
    open(out, 'w').write(head_doc('MvC2 — Felicia / Cyclops / Storm (combo dojo)', css, body))
    print('wrote', out, f'({total} combos, screens={counts})')


def build_beginner():
    css = open(_os.path.join(_HERE, 'style.css')).read()
    toc = ('<nav id="toc"><div class="toc-head"><h2>Contents</h2></div><ul class="toc-top">'
           '<li><a href="#start">Start here (controls)</a></li>'
           '<li><a href="#system">How MvC2 works</a></li>'
           '<li><a href="#team">How to play this team</a></li>'
           '<li><a href="#path">Learning path</a></li>'
           '<li><a href="#combos-basic">First combos</a></li>'
           '<li><a href="#moves">Movesets — full reference</a></li>'
           '<li><a href="#moves-felicia">Felicia — one screen</a></li>'
           '<li><a href="#moves-cyclops">Cyclops — one screen</a></li>'
           '<li><a href="#moves-storm">Storm — one screen</a></li>'
           '<li><a href="#moves-all">All three — one screen</a></li>'
           '<li><a href="#refs">References</a></li></ul></nav>')
    start = ('<section class="block" id="start"><h2>Start here — the controls'
             '<a href="#toc" class="bt">contents ↑</a></h2>'
             '<p class="intro">A beginner-friendly guide to the <b>Felicia / Cyclops / Storm</b> team in '
             '<b>Marvel vs. Capcom 2</b>. Buttons are coloured to match your AYN&nbsp;Thor face buttons.</p>'
             + button_legend() + notation_ledger() + '</section>')
    basic = '<section class="block" id="combos-basic"><h2>Your first combos<a href="#toc" class="bt">contents ↑</a></h2>'
    basic += '<p class="note2">One core combo per character to start with — the full set is in the combo dojo.</p>'
    for ch in ORDER:
        m = META[ch]
        cores = [c for c in COMBOS[ch] if c.get('core')][:3]
        basic += f'<div class="ccombo" style="--ca:{m["ca"]}"><h3>{m["name"]}</h3>'
        basic += ''.join(combo_card(c) for c in cores) + '</div>'
    basic += '</section>'
    moves = '<section class="block" id="moves"><h2>Movesets — full reference<a href="#toc" class="bt">contents ↑</a></h2>'
    moves += ''.join(movelist_section(ch) for ch in ORDER) + '</section>'
    body = (header_bar('MvC2 — Felicia · Cyclops · Storm')
            + '<div class="wrap"><h1>Felicia / Cyclops / Storm — a beginner’s team guide</h1>'
            + f'{toc}{start}{system_section()}{T.team_section()}{T.path_section()}{basic}{moves}'
            + onescreen_section('felicia') + onescreen_section('cyclops') + onescreen_section('storm') + trio_section()
            + references_section() + '</div>' + TOTOP + script_tag())
    out = _os.path.join(_REPO, 'guides', 'mvc2', 'mvc2-felicia-cyclops-storm.html')
    open(out, 'w').write(head_doc('MvC2 — Felicia / Cyclops / Storm (beginner guide)', css, body))
    print('wrote', out)


def build_advanced():
    css = open(_os.path.join(_HERE, 'style.css')).read()
    toc = ('<nav id="toc"><div class="toc-head"><h2>Contents</h2></div><ul class="toc-top">'
           '<li><a href="#how">How to read this guide</a></li>'
           '<li><a href="#sw">Strengths &amp; weaknesses</a></li>'
           '<li><a href="#assists">Assist reference (α/β/γ)</a></li>'
           '<li><a href="#neutral">Neutral &amp; spacing</a></li>'
           '<li><a href="#defense">Defense &amp; escaping pressure</a></li>'
           '<li><a href="#meter">Meter &amp; DHC routes</a></li>'
           '<li><a href="#mixups">Mind games &amp; resets</a></li>'
           '<li><a href="#matchups">Storm matchups</a></li>'
           '<li><a href="#mistakes">Common mistakes</a></li>'
           '<li><a href="#refs">References</a></li></ul></nav>')
    how = ('<section class="block" id="how"><h2>How to read this guide<a href="#toc" class="bt">contents ↑</a></h2>'
           '<p>The advanced companion — team-building, neutral, matchups and habits, for when you already '
           'know the moves and combos. Specials are named pills (hover for input).</p>'
           + button_legend() + '</section>')
    body = (header_bar('MvC2 Advanced — Felicia · Cyclops · Storm')
            + '<div class="wrap"><h1>Felicia / Cyclops / Storm — the advanced guide</h1>'
            + f'{toc}{how}{T.sw_section()}{T.assists_section()}{T.neutral_section()}{T.defense_section()}'
            + f'{T.meter_section()}{T.mixups_section()}{T.matchups_section(STORM_MATCHUPS)}{T.mistakes_section()}'
            + references_section() + '</div>' + TOTOP + script_tag())
    out = _os.path.join(_REPO, 'guides', 'mvc2', 'mvc2-felicia-cyclops-storm-advanced.html')
    open(out, 'w').write(head_doc('MvC2 — Felicia / Cyclops / Storm (advanced guide)', css, body))
    print('wrote', out)


if __name__ == '__main__':
    build_beginner()
    build_combo()
    build_advanced()
