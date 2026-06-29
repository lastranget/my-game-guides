# -*- coding: utf-8 -*-
"""Build KOF XI character guides (Athena, Terry, B. Jenet) — AGGREGATE mode.
Reuses gen.py glyphs/DSL + style.css/app.js; KOF buttons A/B/C/D/E."""
import os as _os
_HERE=_os.path.dirname(_os.path.abspath(__file__))
_REPO=_os.path.dirname(_HERE)
import re
import gen
from gen import (keycap, mot, dirp, render_action, render_combo,
                 G, GP, GC, JG, M, MA, DB, SQ, SP, PRE, TAG)
from refs_kof import references_section

# ---- KOF button glyphs (A/B/C/D/E) mapped to Thor colours (MvC2-consistent) ----
gen.BTN.update({
    'A': ('#2fb84a', '#ffffff', 14),  # light punch  -> green (Y)
    'C': ('#2f86f0', '#ffffff', 14),  # hard punch   -> blue (X)
    'B': ('#f2c531', '#1a1505', 14),  # light kick   -> yellow (B)
    'D': ('#ec3b3b', '#ffffff', 14),  # hard kick    -> red (A)
    'E': ('#6c7079', '#ffffff', 14),  # blowback (CD) -> grey
})
gen.MOT_TITLE.update({
    'QCFx2': 'double quarter-circle forward (super)',
    'QCBx2': 'double quarter-circle back (super)',
    'HCBx2': 'double half-circle back (super)',
    'DP': 'dragon-punch motion (F, D, DF)',
    'F-D-DF': 'forward, down, down-forward',
    'QCB-DB-F': 'quarter-circle back, down-back, forward',
    'QCB-HCF': 'quarter-circle back, then half-circle forward',
})

# ---------------------------------------------------------------- combo parser
# clean DSL: steps joined by ' > '.  tokens:
#   cA sB fC jD shC cxD  -> prefixed normal (c=cr. s=(near) f=far j=j. sh=hop cx=cross-up)
#   E sE jE / CD sCD jCD -> blowback (E)
#   df+D f+B uf+C        -> command normal (dir+button)
#   @key  @key.D         -> named special (registry), optional button variant
#   (text)               -> annotation; (C)->corner, (land)/(dash)/(QS x)->glued connector
PFX = {'c': 'cr.', 's': '', 'f': '(far) ', 'j': 'j.', 'sh': 'hop ', 'cx': 'cross-up ', 'sj': 'sj.'}

def parse_combo(s, specials):
    pieces = []
    for tok in [t.strip() for t in s.split('>') if t.strip()]:
        m = re.fullmatch(r'\((.+)\)', tok)
        if m:
            c = m.group(1)
            if c == 'C':
                pieces.append(TAG('corner'))
            elif c in ('land', 'dash') or c.startswith('QS') or c == '...':
                pieces.append(PRE(c))
            else:
                pieces.append(TAG(c))
            continue
        if tok.startswith('@'):
            mm = re.fullmatch(r'@(\w+)(?:\.([ABCDE]))?\s*(\(.+\))?', tok)
            key, btn, ann = mm.group(1), mm.group(2), mm.group(3)
            disp, mo, defb, air = specials[key]
            pieces.append(SP(disp, mo, btn or defb, air))
            if ann:
                c = ann[1:-1]
                pieces.append(TAG('corner' if c == 'C' else c))
            continue
        m = re.fullmatch(r'([dfubDFUB]{1,2})\+([ABCDE])', tok)
        if m:
            pieces.append(DB(m.group(1).upper(), m.group(2)))
            continue
        m = re.fullmatch(r'(c|s|f|j|sh|cx|sj)?CD', tok)  # blowback combos
        if m:
            pieces.append(('grp', ['E'], PFX.get(m.group(1) or '', None)))
            continue
        m = re.fullmatch(r'(c|s|f|j|sh|cx|sj)?([ABCDE])', tok)
        if m:
            pre = PFX.get(m.group(1) or '', None) or None
            pieces.append(('grp', [m.group(2)], pre))
            continue
        pieces.append(TAG(tok))  # fallback
    return render_combo(pieces)

# ---------------------------------------------------------------- render helpers
def kb(t): return keycap(t)
def mv(m, b, air=False): return render_action(MA(m, b) if air else M(m, b))
def spn(n, m, b, air=False): return render_action(SP(n, m, b, air))
def dbtn(d, b): return render_action(DB(d, b))
def sq(m, b): return render_action(SQ(m, b))
def raw(h): return ('raw', h)

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

def diff_dots(d): return '●' * d + '○' * (3 - d)

# ---------------------------------------------------------------- combo cards
def combo_card(c, ca, compact=False):
    badge = ' <span class="corez">core</span>' if c.get('core') else ''
    hits = f' <span class="hits">{c["hits"]}</span>' if c.get('hits') else ''
    head = (f'<div class="cmb-h"><span class="cid">{c["id"]}</span><b>{c["name"]}</b>'
            f'<span class="diff" title="difficulty {c["diff"]}/3">{diff_dots(c["diff"])}</span>{hits}{badge}</div>')
    body = parse_combo(c['s'], c['_sp'])
    if compact:
        return f'<div class="cmb">{head}{body}</div>'
    note = f'<div class="cmb-note">{c["note"]}</div>' if c.get('note') else ''
    return f'<div class="cmb">{head}{body}{note}</div>'

COMBO_GROUPS = [
    ('bnb', 'Bread &amp; butter — meterless'),
    ('chain', 'Chains &amp; poke strings'),
    ('super', 'Into a Super (DM)'),
    ('dc', 'Super / Dream Cancels (advanced)'),
    ('counter', 'Counter-hit &amp; anti-air'),
    ('corner', 'Corner &amp; juggles'),
    ('team', 'Quick-Shift / team combos'),
]

def n_actions(c):
    return len([p for p in c['s'].split('>') if not p.strip().startswith('(')])

def detailed_combos(ch):
    out = [f'<section class="block" id="combos"><h2>Combos — every route'
           f'<a href="#toc" class="bt">contents ↑</a></h2>'
           f'<p class="note2">Every combo from the source FAQ, grouped by use-case and given a reference '
           f'ID. Specials are shown by <b>name</b> (hover for the input). '
           f'<span class="ann">(C)</span>=corner, <span class="ann">SC</span>=super-cancel, '
           f'<span class="ann">DC</span>=dream-cancel, <span class="ann">QS</span>=quick-shift.</p>'
           f'<div class="ccombo" style="--ca:{ch["ca"]}">']
    for gk, gl in COMBO_GROUPS:
        grp = [c for c in ch['combos'] if c['grp'] == gk]
        if not grp:
            continue
        out.append(f'<div class="ucg">{gl}</div>')
        for c in grp:
            out.append(combo_card(c, ch['ca']))
    out.append('</div></section>')
    return ''.join(out)

def chunk(combos, budget=6):
    pages, cur, w = [], [], 0
    for c in combos:
        na = n_actions(c)
        wt = 1 if na <= 4 else (2 if na <= 7 else 3)
        if cur and w + wt > budget:
            pages.append(cur); cur, w = [], 0
        cur.append(c); w += wt
    if cur:
        pages.append(cur)
    return pages

def combo_screens(ch):  # budget 5
    pages = chunk(ch["combos"], budget=5)
    n = len(pages); secs = []
    for i, page in enumerate(pages, 1):
        first = ' id="screens-combos"' if i == 1 else ''
        cards = ''.join(combo_card(c, ch['ca'], compact=True) for c in page)
        secs.append(
            f'<section class="block screenfit"{first}><h2>{ch["name"]} — combo screen {i}/{n}'
            f'<a href="#toc" class="bt">contents ↑</a></h2>'
            f'<div class="card combo-screen" style="--ca:{ch["ca"]}">'
            f'<div class="card-h"><b>{ch["short"]}</b><span>combos {page[0]["id"]}–{page[-1]["id"]}</span></div>'
            f'<div class="cscreen">{cards}</div></div></section>')
    return ''.join(secs), n

# ---------------------------------------------------------------- movelist
def movelist_section(ch):
    blocks = []
    for label, rows in ch['movelist']:
        rws = ''.join(
            f'<div class="mv"><span class="nm">{nm}{(" <span class=\"note\">"+note+"</span>") if note else ""}</span>'
            f'{render_moveinput(pieces)}</div>' for nm, note, pieces in rows)
        blocks.append(f'<div class="mlgrp"><h4>{label}</h4><div class="ms">{rws}</div></div>')
    return (f'<section class="block" id="moves"><h2>Movelist — full reference'
            f'<a href="#toc" class="bt">contents ↑</a></h2>'
            f'<div class="card" style="--ca:{ch["ca"]}">'
            f'<div class="card-h"><b>{ch["short"]}</b><span>{ch["role"]}</span></div>'
            f'{"".join(blocks)}</div></section>')

def moves_onescreen(ch):
    # the "special moves" one-screen card: command moves, specials, DMs, LDM, throws
    rows = ''.join(
        f'<div class="mv"><span class="nm">{nm}{(" <span class=\"note\">"+note+"</span>") if note else ""}</span>'
        f'{render_moveinput(pieces)}</div>' for nm, note, pieces in ch['onescreen'])
    return (f'<section class="block screenfit" id="moves-1"><h2>{ch["name"]} — special moves (one screen)'
            f'<a href="#toc" class="bt">contents ↑</a></h2>'
            f'<div class="card onescreen" style="--ca:{ch["ca"]}">'
            f'<div class="card-h"><b>{ch["short"]}</b><span>{ch["role"]}</span></div>'
            f'<div class="ms">{"".join(rows)}</div></div></section>')

# ---------------------------------------------------------------- strategy / matchups
def strategy_section(ch):
    if not ch.get('strategy'):
        return ''
    blocks = []
    for heading, rows in ch['strategy']:
        rws = ''.join(sysrow(nm, dsc, inn) for nm, dsc, inn in rows)
        blocks.append(f'<h3>{heading}</h3><div class="sys">{rws}</div>')
    return (f'<section class="block" id="strategy"><h2>Strategy, neutral &amp; mix-ups'
            f'<a href="#toc" class="bt">contents ↑</a></h2>'
            f'<div class="ccombo" style="--ca:{ch["ca"]}">{"".join(blocks)}</div></section>')

def sw_section(ch):
    pl = ''.join(f'<li>{x}</li>' for x in ch['pros'])
    cl = ''.join(f'<li>{x}</li>' for x in ch['cons'])
    return (f'<section class="block" id="sw"><h2>Strengths &amp; weaknesses'
            f'<a href="#toc" class="bt">contents ↑</a></h2>'
            f'<div class="ccombo" style="--ca:{ch["ca"]}"><h3>{ch["short"]} '
            f'<span class="role">· {ch["role"]}</span></h3>'
            f'<div class="sw"><div><h4 class="pro">Strengths</h4><ul>{pl}</ul></div>'
            f'<div><h4 class="con">Weaknesses</h4><ul>{cl}</ul></div></div></div></section>')

def matchups_section(ch):
    if not ch.get('matchups'):
        return ''
    rows = ''.join(
        f'<div class="mu"><div class="mu-h"><b>{n}</b><span class="mtier">{score}</span></div>'
        f'<div class="dsc">{txt}</div></div>' for n, score, txt in ch['matchups'])
    return (f'<section class="block" id="matchups"><h2>Matchups<a href="#toc" class="bt">contents ↑</a></h2>'
            f'<p class="note2">How {ch["short"]} fares against the cast — the source author’s read, with a '
            f'rough win chance.</p>{rows}</section>')

# ---------------------------------------------------------------- shared legends + system
def button_legend():
    items = [('A', 'Light Punch — green (Y)'), ('C', 'Hard Punch — blue (X)'),
             ('B', 'Light Kick — yellow (B)'), ('D', 'Hard Kick — red (A)'),
             ('E', 'Blowback / CD — grey'), ('P', 'any Punch (A or C)'), ('K', 'any Kick (B or D)')]
    lg = ''.join(f'<div class="lg"><span>{keycap(t)}</span><span>{d}</span></div>' for t, d in items)
    return (f'<div class="legendwrap"><div class="leg-grid">{lg}</div>'
            f'<p class="note2">KOF uses four attack buttons — two punches (A/C) and two kicks (B/D) — '
            f'plus <b>E</b>, the blowback (old CD) attack. Buttons are coloured to match your AYN Thor '
            f'face buttons; E sits on a grey shoulder.</p></div>')

def notation_ledger():
    mots = [('QCF', 'quarter-circle fwd'), ('QCB', 'quarter-circle back'), ('HCF', 'half-circle fwd'),
            ('HCB', 'half-circle back'), ('DP', 'dragon punch (F,D,DF)'), ('QCFx2', 'double QCF (super)')]
    dirs = [('F', 'forward (to foe)'), ('B', 'back'), ('D', 'down'), ('U', 'up'),
            ('DF', 'down-fwd'), ('UF', 'up-fwd')]
    rows = ''.join(f'<div class="lg"><span>{mot(t)}</span><span>{d}</span></div>' for t, d in mots)
    rows += ''.join(f'<div class="lg"><span>{dirp(t)}</span><span>{d}</span></div>' for t, d in dirs)
    return (f'<div class="legendwrap" id="notation"><div class="motlegend" style="margin-top:0;line-height:1.5">'
            f'Motions are <b>facing-relative</b> — <b>F</b> = toward the opponent, <b>B</b> = away. '
            f'A named pill (e.g. {spn("Power Geyser","QCB-DB-F","P")}) is a move — hover for the input.</div>'
            f'<div class="leg-grid">{rows}</div></div>')

def system_section():
    movement = ''.join([
        sysrow('Walk / dash / backstep', 'Tap <b>f,f</b> (hold) to run; <b>b,b</b> to hop back (brief '
               'invincibility).', f'{dirp("F")}{dirp("F")} <span class="osep">·</span> {dirp("B")}{dirp("B")}'),
        sysrow('Jumps', 'Tap up = a <b>short hop</b>; press up = a full jump. There are also fast-hops and '
               'high jumps. Hops are the heart of KOF offence.', f'{dirp("U")} <span class="ann">tap = hop</span>'),
        sysrow('Block', 'Hold <b>back</b> to block high, <b>down-back</b> to block low. You cannot block in '
               'the air in KOF.', f'{dirp("B")} <span class="osep">/</span> {dirp("DB")}'),
    ])
    defense = ''.join([
        sysrow('Roll (Emergency Evade)', 'Roll forward through an attack (invincible on start-up, then '
               'vulnerable). Back-roll with b+AB.', f'{kb("A")}{kb("B")}'),
        sysrow('Guard Cancel roll / blowback', 'While blocking, spend <b>1 stock</b> to roll out (AB) or to '
               'shove them off with the blowback (E).', f'{kb("A")}{kb("B")} <span class="osep">/</span> {kb("E")}'),
        sysrow('Fallbreaker (recovery roll)', 'Tap AB just before you hit the ground to recover and avoid an '
               'OTG (not vs. hard-knockdown moves).', f'{kb("A")}{kb("B")} <span class="ann">landing</span>'),
        sysrow('Guard Crush', 'Every block chips your guard gauge; let it empty and you’re <b>Crushed</b> — '
               'stunned and wide open. Stop blocking forever.'),
    ])
    offense = ''.join([
        sysrow('Throw / throw escape', 'Close <b>f/b + C or D</b> throws (unblockable); the same input the '
               'instant you’re grabbed escapes a ground throw.', f'{dirp("F")}{kb("C")}'),
        sysrow('Blowback (CD)', 'The <b>E</b> button — a knockdown blow that’s cancellable on many '
               'characters and great as a poke / anti-air.', f'{kb("E")}'),
        sysrow('Stun gauge', 'The red bar above your life; fill it and the opponent is <b>STUNNED</b> for a '
               'free combo.'),
    ])
    team = ''.join([
        sysrow('Tag out (Multi-Shift)', 'Swap to a teammate any time on the ground — but you can be hit out '
               'of it, so do it safe.', f'{kb("A")}{kb("C")} <span class="osep">/</span> {kb("B")}{kb("D")}'),
        sysrow('Quick Shift', 'Cancel your own attack to tag a partner in <b>airborne</b> for a follow-up — '
               'costs <b>1 skill point</b>. The basis of team combos.', f'{kb("A")}{kb("C")} <span class="ann">attacking</span>'),
        sysrow('Saving Shift', 'When you’re <i>being</i> hit, tag a partner in to break the opponent’s '
               'pursuit — costs <b>both skill points</b>.', f'{kb("A")}{kb("C")} <span class="ann">when hit</span>'),
        sysrow('Skill gauge', 'The bar above the power stocks; auto-charges to <b>2 points</b>. Pays for '
               'Super/Dream Cancels and Quick/Saving Shifts.'),
    ])
    meter = ''.join([
        sysrow('Power stocks &amp; Desperation Moves', 'Attacking fills the power gauge into <b>stocks</b> '
               '(up to 5). A <b>DM</b> (super) costs 1 stock.'),
        sysrow('Leader &amp; LDM', 'You pick one <b>Leader</b> (green gauge). Only the Leader can do the '
               '<b>Leader DM</b> (2 stocks) and Dream Cancels.'),
        sysrow('Super Cancel', 'Cancel a special into a DM — needs <b>1 skill point + 1 stock</b>.'),
        sysrow('Dream Cancel', 'Cancel a DM into the Leader’s LDM — Leader only, <b>1 skill point + 3 '
               'stocks</b>. The big-damage finisher.'),
        sysrow('Judgement (time-over)', 'If time runs out, the player who dealt more / landed an LDM wins '
               '(the timer colour shows who’s ahead).'),
    ])
    return (f'<section class="block" id="system"><h2>How KOF XI works — controls &amp; systems'
            f'<a href="#toc" class="bt">contents ↑</a></h2>'
            f'<p class="note2">Everything you need to play, beyond this character’s own moves. KOF XI is a '
            f'<b>3-on-1 tag</b> fighter (you pick a team of three + a Leader, but only one fights at a time).</p>'
            f'<div class="sysgrp">Movement</div><div class="sys">{movement}</div>'
            f'<div class="sysgrp">Defence</div><div class="sys">{defense}</div>'
            f'<div class="sysgrp">Offence</div><div class="sys">{offense}</div>'
            f'<div class="sysgrp">Team — tags &amp; shifts</div><div class="sys">{team}</div>'
            f'<div class="sysgrp">Meter, cancels &amp; the Leader</div><div class="sys">{meter}</div></section>')

# ---------------------------------------------------------------- page assembly
def build_one(ch):
    # assign combo IDs in display (group) order; attach the specials registry for the parser
    gorder = {k: i for i, (k, _) in enumerate(COMBO_GROUPS)}
    ch['combos'].sort(key=lambda c: gorder[c['grp']])
    for i, c in enumerate(ch['combos'], 1):
        c['id'] = f"{ch['pfx']}-{i:02d}"
        c['_sp'] = ch['specials']
    css = open(_os.path.join(_HERE,'style.css')).read()
    js = open(_os.path.join(_HERE,'app.js')).read()
    defs = ('<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>'
            '<linearGradient id="gp" x1="0" x2="1" y1="0" y2="0"><stop offset="50%" stop-color="#2fb84a"/>'
            '<stop offset="50%" stop-color="#2f86f0"/></linearGradient>'
            '<linearGradient id="gk" x1="0" x2="1" y1="0" y2="0"><stop offset="50%" stop-color="#f2c531"/>'
            '<stop offset="50%" stop-color="#ec3b3b"/></linearGradient></defs></svg>')
    screens, nscreens = combo_screens(ch)
    toc = ('<nav id="toc"><div class="toc-head"><h2>Contents</h2></div><ul class="toc-top">'
           '<li><a href="#how">How to read this guide</a></li>'
           '<li><a href="#system">KOF XI — controls &amp; systems</a></li>'
           '<li><a href="#sw">Strengths &amp; weaknesses</a></li>'
           '<li><a href="#moves">Movelist — full reference</a></li>'
           '<li><a href="#combos">Combos — every route</a></li>'
           '<li><a href="#strategy">Strategy &amp; mix-ups</a></li>'
           + ('<li><a href="#matchups">Matchups</a></li>' if ch.get('matchups') else '')
           + f'<li><a href="#screens-combos">Combo screens (×{nscreens})</a></li>'
           '<li><a href="#moves-1">Special moves (one screen)</a></li>'
           '<li><a href="#refs">References &amp; sources</a></li>'
           '</ul></nav>')
    how = (f'<section class="block" id="how"><h2>How to read this guide'
           f'<a href="#toc" class="bt">contents ↑</a></h2>'
           f'<p>Inputs use coloured buttons matching your AYN&nbsp;Thor and short, facing-relative motion '
           f'tokens. Combos read left→right with a faint <span class="cs">›</span> between steps; '
           f'<span class="ann">italics</span> are notes. Difficulty is '
           f'<span class="diff">●○○</span>–<span class="diff">●●●</span>.</p>'
           f'{button_legend()}{notation_ledger()}</section>')
    intro = (f'<p class="intro">{ch["intro"]}</p>')
    body = (f'<header class="bar"><span class="title">KOF XI — {ch["short"]}</span>'
            f'<a class="jump" href="#toc">Contents</a></header>'
            f'<div class="wrap"><h1>{ch["name"]} — King of Fighters XI guide</h1>'
            f'{intro}{toc}{how}{system_section()}{sw_section(ch)}{movelist_section(ch)}'
            f'{detailed_combos(ch)}{strategy_section(ch)}{matchups_section(ch)}'
            f'{screens}{moves_onescreen(ch)}{references_section(ch["key"])}'
            f'</div><a href="#top" id="totop" aria-label="Back to top">↑</a><script>{js}</script>')
    doc = ('<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
           '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
           '<meta name="color-scheme" content="dark">\n'
           f'<title>KOF XI — {ch["name"]} guide</title>\n'
           f'<style>{css}</style>\n</head>\n<body id="top">\n{defs}\n{body}\n</body>\n</html>\n')
    out = _os.path.join(_REPO,'guides','kofxi', f'kofxi-{ch["key"]}.html')
    import os
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, 'w').write(doc)
    print(f'wrote {out} ({len(doc)} bytes, {len(ch["combos"])} combos, {nscreens} combo screens)')

if __name__ == '__main__':
    from chardata import CHARS
    for key in ('terry', 'athena', 'bjenet'):
        if key in CHARS:
            build_one(CHARS[key])