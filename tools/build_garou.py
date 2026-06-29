# -*- coding: utf-8 -*-
"""Build Garou: Mark of the Wolves combo guides (Terry, B. Jenet).
Combo-dojo format. 4-button game (A/B/C/D = LP/LK/HP/HK). Reuses gen.py +
style.css + app.js. Data in garou_data.py."""
import os as _os
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_REPO = _os.path.dirname(_HERE)

from gen import keycap, mot, dirp, render_action, render_combo, M, MA, DB, SQ, SP, G, TAG, PRE
from garou_data import META, ORDER, COMBO_GROUPS, COMBOS, MOVES, ONESCREEN
from refs_garou import references_section

for ch in ORDER:
    go = {k: i for i, (k, _) in enumerate(COMBO_GROUPS)}
    COMBOS[ch].sort(key=lambda c: go.get(c['grp'], 99))
    for i, c in enumerate(COMBOS[ch], 1):
        c['id'] = f"{META[ch]['pfx']}-{i:02d}"

def diff_dots(d): return '●' * d + '○' * (3 - d)
def kb(t): return keycap(t)
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

DEFS = ('<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>'
        '<linearGradient id="gp" x1="0" x2="1" y1="0" y2="0"><stop offset="50%" stop-color="#2fb84a"/>'
        '<stop offset="50%" stop-color="#2f86f0"/></linearGradient>'
        '<linearGradient id="gk" x1="0" x2="1" y1="0" y2="0"><stop offset="50%" stop-color="#f2c531"/>'
        '<stop offset="50%" stop-color="#ec3b3b"/></linearGradient></defs></svg>')
TOTOP = '<a href="#top" id="totop" aria-label="Back to top">↑</a>'
def script_tag(): return '<script>' + open(_os.path.join(_HERE, 'app.js')).read() + '</script>'
def head_doc(title, css, body):
    return ('<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            '<meta name="color-scheme" content="dark">\n'
            f'<title>{title}</title>\n<style>{css}</style>\n</head>\n<body id="top">\n{DEFS}\n{body}\n</body>\n</html>\n')

def button_legend():
    items = [('A', 'Weak Punch — green (Y)'), ('C', 'Hard Punch — blue (X)'),
             ('B', 'Weak Kick — yellow (B)'), ('D', 'Hard Kick — red (A)'),
             ('P', 'any Punch'), ('K', 'any Kick')]
    lg = ''.join(f'<div class="lg"><span>{keycap(t)}</span><span>{d}</span></div>' for t, d in items)
    return (f'<div class="legendwrap"><div class="leg-grid">{lg}</div>'
            f'<p class="note2">Garou uses four buttons — <b>A</b> weak punch, <b>B</b> weak kick, '
            f'<b>C</b> hard punch, <b>D</b> hard kick. <b>AC</b> = a Feint; <b>CD</b> = blowback / the '
            f'T.O.P. attack. <b>(Brake)</b> = cancel a special’s recovery with A+B.</p></div>')

def notation_ledger():
    mots = [('QCF', 'quarter-circle fwd'), ('QCB', 'quarter-circle back'), ('HCF', 'half-circle fwd'),
            ('DP', 'dragon punch (f,d,df)'), ('QCFx2', 'double QCF (super)')]
    dirs = [('F', 'forward'), ('B', 'back'), ('D', 'down'), ('U', 'up')]
    rows = ''.join(f'<div class="lg"><span>{mot(t)}</span><span>{d}</span></div>' for t, d in mots)
    rows += ''.join(f'<div class="lg"><span>{dirp(t)}</span><span>{d}</span></div>' for t, d in dirs)
    return (f'<div class="legendwrap" id="notation"><div class="motlegend" style="margin-top:0;line-height:1.5">'
            f'Motions are <b>facing-relative</b>. A named pill (e.g. {spn("The Hind","QCF","D")}) is a special '
            f'move — hover for the input. Supers cost <b>S.Power</b> (1 stock); <b>Potentials</b> the P.Power '
            f'(2 stocks). In your <b>T.O.P.</b> zone you also get the CD T.O.P. attack + a damage buff.</div>'
            f'<div class="leg-grid">{rows}</div></div>')

def onescreen_section(ch):
    m = META[ch]
    rows = ''.join(
        f'<div class="mv"><span class="nm">{nm}{(" <span class=\"note\">"+note+"</span>") if note else ""}</span>'
        f'{render_moveinput(p)}</div>' for nm, note, p in ONESCREEN[ch])
    return (f'<section class="block screenfit" id="moves-1"><h2>{m["name"]} — special moves (one screen)'
            f'<a href="#toc" class="bt">contents ↑</a></h2>'
            f'<div class="card onescreen" style="--ca:{m["ca"]}"><div class="card-h"><b>{m["name"]}</b>'
            f'<span>{m["role"]}</span></div><div class="ms">{rows}</div></div></section>')

def n_actions(c):
    return sum(1 for pc in c['seq'] if pc[0] in ('grp', 'mot', 'dir', 'chg', 'seq', 'sp', 'dir1'))

def detailed_combos(ch):
    m = META[ch]
    out = ['<section class="block" id="combos"><h2>Combos — by use-case<a href="#toc" class="bt">contents ↑</a></h2>'
           '<p class="note2">Grouped by use-case with reference IDs. Specials are named pills (hover for input). '
           'Built from MGA’s Combo FAQ + the movelists + Garou’s Brake/Break &amp; super-cancel rules.</p>'
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

def build(ch):
    css = open(_os.path.join(_HERE, 'style.css')).read()
    m = META[ch]
    screens, n = combo_screens(ch)
    toc = ('<nav id="toc"><div class="toc-head"><h2>Contents</h2></div><ul class="toc-top">'
           '<li><a href="#how">How to read these combos</a></li>'
           '<li><a href="#combos">All combos by use-case</a></li>'
           f'<li><a href="#screens-combos">Combo screens (×{n})</a></li>'
           '<li><a href="#moves-1">Special moves (one screen)</a></li>'
           '<li><a href="#refs">References &amp; sources</a></li></ul></nav>')
    how = ('<section class="block" id="how"><h2>How to read these combos<a href="#toc" class="bt">contents ↑</a></h2>'
           '<p>Combos read left→right with a faint <span class="cs">›</span> between steps; '
           '<span class="ann">italics</span> are notes (Brake, T.O.P., land…). Difficulty is '
           '<span class="diff">●○○</span>–<span class="diff">●●●</span>; <span class="corez">core</span> marks '
           'the staples.</p>' + button_legend() + notation_ledger() + '</section>')
    body = (f'<header class="bar"><span class="title">Garou Combos — {m["name"]}</span>'
            f'<a class="jump" href="#toc">Contents</a></header>'
            f'<div class="wrap"><h1>{m["name"]} — Garou combo dojo</h1>'
            f'<p class="intro">A combo guide for <b>{m["name"]}</b> in <b>Garou: Mark of the Wolves</b> — '
            f'every route grouped by use-case with reference IDs, plus single-screen practice cards for your '
            f'AYN&nbsp;Thor. Companion to the beginner guide.</p>'
            f'{toc}{how}{detailed_combos(ch)}{screens}{onescreen_section(ch)}{references_section(ch)}'
            f'</div>{TOTOP}{script_tag()}')
    stem = {'bjenet': 'b-jenet', 'terry': 'terry'}[ch]  # match existing sibling filenames
    out = _os.path.join(_REPO, 'guides', 'garou', f'garou-{stem}-combos.html')
    open(out, 'w').write(head_doc(f'Garou — {m["name"]} (combos)', css, body))
    print('wrote', out, f'({len(COMBOS[ch])} combos, {n} screens)')

if __name__ == '__main__':
    for ch in ORDER:
        build(ch)
