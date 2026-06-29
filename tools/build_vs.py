# -*- coding: utf-8 -*-
"""Build Vampire Savior character guides — ONE combined guide per character
(vsavior-<char>.html): beginner + advanced + every combo + single-screen cards.
(The content was short enough that the split beginner/combo files were merged.)
Reuses gen.py (6-button glyphs) + style.css + app.js. Data in vs_data.py."""
import os as _os
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_REPO = _os.path.dirname(_HERE)

from gen import keycap, mot, dirp, render_action, render_combo, M, MA, DB, SQ, SP, G, TAG, PRE
from vs_data import META, ORDER, COMBO_GROUPS, COMBOS, MOVES, ONESCREEN, SW, STRATEGY
from refs_vs import references_section

for ch in ORDER:
    go = {k: i for i, (k, _) in enumerate(COMBO_GROUPS)}
    COMBOS[ch].sort(key=lambda c: go.get(c['grp'], 99))
    for i, c in enumerate(COMBOS[ch], 1):
        c['id'] = f"{META[ch]['pfx']}-{i:02d}"

def diff_dots(d): return '●' * d + '○' * (3 - d)
def kb(t): return keycap(t)
def mv(m, b, air=False): return render_action(MA(m, b) if air else M(m, b))
def spn(n, m, b, air=False): return render_action(SP(n, m, b, air))

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

# ---- shared chrome ----
DEFS = ('<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>'
        '<linearGradient id="gp" x1="0" x2="1" y1="0" y2="0"><stop offset="50%" stop-color="#2fb84a"/>'
        '<stop offset="50%" stop-color="#2f86f0"/></linearGradient>'
        '<linearGradient id="gk" x1="0" x2="1" y1="0" y2="0"><stop offset="50%" stop-color="#f2c531"/>'
        '<stop offset="50%" stop-color="#ec3b3b"/></linearGradient></defs></svg>')
def script_tag(): return '<script>' + open(_os.path.join(_HERE, 'app.js')).read() + '</script>'
TOTOP = '<a href="#top" id="totop" aria-label="Back to top">↑</a>'
def header_bar(t): return f'<header class="bar"><span class="title">{t}</span><a class="jump" href="#toc">Contents</a></header>'
def head_doc(title, css, body):
    return ('<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            '<meta name="color-scheme" content="dark">\n'
            f'<title>{title}</title>\n<style>{css}</style>\n</head>\n<body id="top">\n{DEFS}\n{body}\n</body>\n</html>\n')

def button_legend():
    items = [('LP', 'Light Punch — green (Y)'), ('MP', 'Medium Punch — grey'), ('HP', 'Hard Punch — blue (X)'),
             ('LK', 'Light Kick — yellow (B)'), ('MK', 'Medium Kick — grey'), ('HK', 'Hard Kick — red (A)'),
             ('P', 'any Punch'), ('K', 'any Kick')]
    lg = ''.join(f'<div class="lg"><span>{keycap(t)}</span><span>{d}</span></div>' for t, d in items)
    return (f'<div class="legendwrap"><div class="leg-grid">{lg}</div>'
            f'<p class="note2">Vampire Savior is a <b>six-button</b> fighter — three punches (LP/MP/HP) and '
            f'three kicks (LK/MK/HK). Light/hard sit on your coloured Thor face buttons; the mediums go on '
            f'the grey shoulders. <b>PP/KK</b> = the ES (Especial) version of a move.</p></div>')

def notation_ledger():
    mots = [('QCF', 'quarter-circle fwd'), ('QCB', 'quarter-circle back'), ('HCF', 'half-circle fwd'),
            ('HCB', 'half-circle back'), ('DP', 'dragon punch (f,d,df)')]
    dirs = [('[B]F', 'charge back→fwd'), ('[D]U', 'charge down→up'), ('F', 'forward'), ('B', 'back'),
            ('D', 'down'), ('U', 'up')]
    rows = ''.join(f'<div class="lg"><span>{mot(t)}</span><span>{d}</span></div>' for t, d in mots)
    rows += ''.join(f'<div class="lg"><span>{dirp(t)}</span><span>{d}</span></div>' for t, d in dirs)
    return (f'<div class="legendwrap" id="notation"><div class="motlegend" style="margin-top:0;line-height:1.5">'
            f'Motions are <b>facing-relative</b> — <b>F</b> = toward the opponent, <b>B</b> = away. '
            f'A named pill (e.g. {spn("Shadow Blade","DP","P")}) is a move — hover for the input.</div>'
            f'<div class="leg-grid">{rows}</div></div>')

def system_section():
    movement = ''.join([
        sysrow('Dash / backstep', 'Tap toward / away twice. Many characters can air-dash or double-jump too.',
               f'{dirp("F")}{dirp("F")} <span class="osep">/</span> {dirp("B")}{dirp("B")}'),
        sysrow('Jump / high jump', 'Tap up to jump; tap down then up for a high jump. Several cast members have a second air jump.',
               f'{dirp("D")}{dirp("U")}'),
    ])
    defense = ''.join([
        sysrow('Guard / air-guard', 'Hold back (high) or down-back (low); you <b>can</b> air-guard in VS.',
               f'{dirp("B")} <span class="osep">/</span> {dirp("DB")}'),
        sysrow('Advancing Guard (tech)', 'Tap P/K while blocking to push the attacker away.',
               f'{kb("LP")}<span class="ann">blocking</span>'),
        sysrow('Guard Cancel', 'While blocking, do your Guard-Cancel special to interrupt pressure (costs Chi).'),
        sysrow('Tech / soften throws', 'Throw the instant you’re thrown (or tap b/f + a hard button) to soften it.'),
    ])
    offense = ''.join([
        sysrow('Chain combos', 'Cancel attacks <b>weak → strong</b>, zig-zagging punches and kicks: '
               'LP → LK → MP → MK → HP → HK. Tap the next button on the hit-spark.',
               f'{kb("LP")}{kb("LK")}{kb("MP")}{kb("MK")}{kb("HP")}{kb("HK")}'),
        sysrow('Throws', 'Close <b>b/f + MP/HP or MK/HK</b>.', f'{dirp("F")}{kb("HP")}'),
        sysrow('Pursuit (OTG)', 'When the foe is down, <b>u + P/K</b> for an extra hit; do it with two buttons '
               '(ES) for more.', f'{dirp("U")}{kb("LP")}'),
        sysrow('ES (Especial) moves', 'Do a special with <b>two</b> buttons (PP/KK) for a stronger EX version — '
               'costs one Chi level.', f'{kb("P")}{kb("P")}'),
    ])
    meter = ''.join([
        sysrow('Chi (special stock)', 'Builds as you deal/​take damage (combos fill it fast). Spend it on ES '
               'moves, EX supers, Guard Cancels and Dark Force.'),
        sysrow('EX supers (Dramatic Moves)', 'Big named supers — most cost 1 Chi, some 2+.'),
        sysrow('Dark Force', 'Press the <b>same-strength P + K</b> to trigger your character’s install (mirror '
               'clone, missile mode, Kitty helper…). Costs Chi.', f'{kb("HP")}+{kb("HK")}'),
        sysrow('Energy Bats (the match)', 'One round: deplete the foe’s health to take a bat; unhit health '
               'slowly recovers. Take all their bats (2 by default) to win.'),
    ])
    return ('<section class="block" id="system"><h2>How Vampire Savior works'
            '<a href="#toc" class="bt">contents ↑</a></h2>'
            '<p class="note2">Everything you need to play, beyond this character’s own moves. VS is a fast '
            '<b>1-on-1</b> fighter with recoverable health and no rounds.</p>'
            f'<div class="sysgrp">Movement</div><div class="sys">{movement}</div>'
            f'<div class="sysgrp">Defence</div><div class="sys">{defense}</div>'
            f'<div class="sysgrp">Offence</div><div class="sys">{offense}</div>'
            f'<div class="sysgrp">Chi, supers &amp; the match</div><div class="sys">{meter}</div></section>')

def movelist_section(ch):
    blocks = []
    for label, rows in MOVES[ch]:
        rws = ''.join(
            f'<div class="mv"><span class="nm">{nm}{(" <span class=\"note\">"+note+"</span>") if note else ""}</span>'
            f'{render_moveinput(p)}</div>' for nm, note, p in rows)
        blocks.append(f'<div class="mlgrp"><h4>{label}</h4><div class="ms">{rws}</div></div>')
    m = META[ch]
    return (f'<section class="block" id="moves"><h2>Movelist — full reference<a href="#toc" class="bt">contents ↑</a></h2>'
            f'<div class="card" style="--ca:{m["ca"]}"><div class="card-h"><b>{m["name"]}</b>'
            f'<span>{m["role"]}</span></div>{"".join(blocks)}</div></section>')

def onescreen_section(ch):
    m = META[ch]
    rows = ''.join(
        f'<div class="mv"><span class="nm">{nm}{(" <span class=\"note\">"+note+"</span>") if note else ""}</span>'
        f'{render_moveinput(p)}</div>' for nm, note, p in ONESCREEN[ch])
    return (f'<section class="block screenfit" id="moves-1"><h2>{m["name"]} — special moves (one screen)'
            f'<a href="#toc" class="bt">contents ↑</a></h2>'
            f'<div class="card onescreen" style="--ca:{m["ca"]}"><div class="card-h"><b>{m["name"]}</b>'
            f'<span>{m["role"]}</span></div><div class="ms">{rows}</div></div></section>')

def sw_section(ch):
    pros, cons = SW[ch]; m = META[ch]
    pl = ''.join(f'<li>{x}</li>' for x in pros); cl = ''.join(f'<li>{x}</li>' for x in cons)
    return (f'<section class="block" id="sw"><h2>Strengths &amp; weaknesses<a href="#toc" class="bt">contents ↑</a></h2>'
            f'<div class="ccombo" style="--ca:{m["ca"]}"><h3>{m["name"]} <span class="role">· {m["role"]}</span></h3>'
            f'<div class="sw"><div><h4 class="pro">Strengths</h4><ul>{pl}</ul></div>'
            f'<div><h4 class="con">Weaknesses</h4><ul>{cl}</ul></div></div></div></section>')

def strategy_section(ch):
    rows = ''.join(sysrow(n, d) for n, d in STRATEGY[ch])
    return (f'<section class="block" id="strategy"><h2>Strategy &amp; game plan<a href="#toc" class="bt">contents ↑</a></h2>'
            f'<div class="ccombo" style="--ca:{META[ch]["ca"]}"><div class="sys">{rows}</div></div></section>')

def n_actions(c):
    return sum(1 for pc in c['seq'] if pc[0] in ('grp', 'mot', 'dir', 'chg', 'seq', 'sp', 'dir1'))

def detailed_combos(ch):
    m = META[ch]
    out = ['<section class="block" id="combos"><h2>Combos — by use-case<a href="#toc" class="bt">contents ↑</a></h2>'
           '<p class="note2">Grouped by use-case with reference IDs. Specials are named pills (hover for input). '
           'Felicia/Morrigan/Lilith routes are built from the chain system + movelists where the source had no '
           'explicit list.</p>'
           f'<div class="ccombo" style="--ca:{m["ca"]}"><h3>{m["name"]} <span class="role">· {m["role"]}</span></h3>']
    for gk, gl in COMBO_GROUPS:
        grp = [c for c in COMBOS[ch] if c['grp'] == gk]
        if not grp:
            continue
        out.append(f'<div class="ucg">{gl}</div>')
        out += [combo_card(c) for c in grp]
    out.append('</div></section>')
    return ''.join(out)

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
        first = ' id="screens-combos"' if i == 1 else ''
        cards = ''.join(combo_card(c, compact=True) for c in page)
        secs.append(f'<section class="block screenfit"{first}><h2>{m["name"]} — combo screen {i}/{n}'
                    f'<a href="#toc" class="bt">contents ↑</a></h2>'
                    f'<div class="card combo-screen" style="--ca:{m["ca"]}"><div class="card-h"><b>{m["name"]}</b>'
                    f'<span>{page[0]["id"]}–{page[-1]["id"]}</span></div><div class="cscreen">{cards}</div></div></section>')
    return ''.join(secs), n

def how_section(combo=False):
    extra = ('Combos read left→right with a faint <span class="cs">›</span> between steps; '
             '<span class="ann">italics</span> are notes. ' if combo else '')
    return (f'<section class="block" id="how"><h2>How to read this guide<a href="#toc" class="bt">contents ↑</a></h2>'
            f'<p>{extra}Inputs use coloured buttons matching your AYN&nbsp;Thor and short, facing-relative '
            f'motion tokens. Difficulty is <span class="diff">●○○</span>–<span class="diff">●●●</span>.</p>'
            f'{button_legend()}{notation_ledger()}</section>')

def build_one(ch):
    """One self-contained guide per character: beginner + advanced + all combos."""
    css = open(_os.path.join(_HERE, 'style.css')).read()
    m = META[ch]
    screens, n = combo_screens(ch)
    toc = ('<nav id="toc"><div class="toc-head"><h2>Contents</h2></div><ul class="toc-top">'
           '<li><a href="#how">How to read this guide</a></li>'
           '<li><a href="#system">How Vampire Savior works</a></li>'
           '<li><a href="#sw">Strengths &amp; weaknesses</a></li>'
           '<li><a href="#moves">Movelist — full reference</a></li>'
           '<li><a href="#strategy">Strategy &amp; game plan</a></li>'
           '<li><a href="#combos">Combos — by use-case</a></li>'
           f'<li><a href="#screens-combos">Combo screens (×{n})</a></li>'
           '<li><a href="#moves-1">Special moves (one screen)</a></li>'
           '<li><a href="#refs">References &amp; sources</a></li></ul></nav>')
    body = (header_bar(f'Vampire Savior — {m["name"]}')
            + f'<div class="wrap"><h1>{m["name"]} ({m["long"]}) — Vampire Savior guide</h1>'
            f'<p class="intro">A complete guide for <b>{m["name"]}</b> in <b>Vampire Savior: The Lord of '
            f'Vampire</b> (Darkstalkers 3) — controls, the full movelist, strengths, a game plan, and '
            f'<b>every combo</b> with single-screen practice cards for your AYN&nbsp;Thor.</p>'
            f'{toc}{how_section(combo=True)}{system_section()}{sw_section(ch)}{movelist_section(ch)}'
            f'{strategy_section(ch)}{detailed_combos(ch)}{screens}{onescreen_section(ch)}'
            f'{references_section(ch)}</div>{TOTOP}{script_tag()}')
    out = _os.path.join(_REPO, 'guides', 'vsavior', f'vsavior-{ch}.html')
    _os.makedirs(_os.path.dirname(out), exist_ok=True)
    open(out, 'w').write(head_doc(f'Vampire Savior — {m["name"]} (guide)', css, body))
    print('wrote', out, f'({len(COMBOS[ch])} combos, {n} combo screens)')

if __name__ == '__main__':
    import glob as _glob
    # remove the old split combo files — content now lives in the single per-character guide
    for _f in _glob.glob(_os.path.join(_REPO, 'guides', 'vsavior', 'vsavior-*-combos.html')):
        _os.remove(_f)
    for ch in ORDER:
        build_one(ch)
