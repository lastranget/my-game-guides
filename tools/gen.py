# -*- coding: utf-8 -*-
"""Generator for the MvC2 Cammy/BB Hood/Cyclops COMBO guide (AGGREGATE mode).
Reuses the exact glyph/combo markup + OLED-black Thor style of the existing guide.
Combos grouped by use-case; each has a unique ID (CA/BB/CY-##); single-screen
practice pages + a copy of the special-move one-screen movesets."""

import html as _html

# ---------------------------------------------------------------- glyphs
# solid 2-char keycaps (physical Thor buttons) + gradient P/K/PP/KK
BTN = {
    'LP': ('#2fb84a', '#ffffff', 14), 'HP': ('#2f86f0', '#ffffff', 14),
    'LK': ('#f2c531', '#1a1505', 14), 'HK': ('#ec3b3b', '#ffffff', 14),
    'A1': ('#6c7079', '#ffffff', 14), 'A2': ('#6c7079', '#ffffff', 14),
}
GRAD = {'P': 'gp', 'PP': 'gp', 'K': 'gk', 'KK': 'gk'}

def keycap(tok):
    if tok in BTN:
        fill, txt, fs = BTN[tok]
        return (f'<svg class="key" viewBox="0 0 38 27" role="img" aria-label="{tok}">'
                f'<rect x="1.5" y="1.5" width="35" height="24" rx="6" fill="{fill}" stroke="rgba(0,0,0,.4)"/>'
                f'<text x="19" y="19" text-anchor="middle" font-size="{fs}" font-weight="800" fill="{txt}" '
                f'font-family="Arial,Helvetica,sans-serif">{tok}</text></svg>')
    grad = GRAD[tok]
    return (f'<svg class="key" viewBox="0 0 38 27" role="img" aria-label="{tok}">'
            f'<rect x="1.5" y="1.5" width="35" height="24" rx="6" fill="url(#{grad})" stroke="rgba(0,0,0,.4)"/>'
            f'<text x="19" y="19" text-anchor="middle" font-size="13" font-weight="800" fill="#fff" '
            f'style="paint-order:stroke" stroke="rgba(0,0,0,.45)" stroke-width="0.7" stroke-linejoin="round" '
            f'font-family="Arial,Helvetica,sans-serif">{tok}</text></svg>')

MOT_TITLE = {
    'QCF': 'Quarter-circle forward (QCF)', 'QCB': 'Quarter-circle back (QCB)',
    'HCF': 'Half-circle forward (HCF)', 'HCB': 'Half-circle back (HCB)',
    'DP': 'Dragon punch (DP / Z-motion)', 'F-DF-D': 'Forward to down (F, DF, D)',
    'F-DF-D-DB-B': 'Half-circle-ish command grab',
}
DIR_TITLE = {
    '[B]F': 'charge back, then forward', '[D]U': 'charge down, then up',
    'F': 'forward (toward foe)', 'B': 'back (away)', 'U': 'up', 'D': 'down',
    'DF': 'down-forward', 'DB': 'down-back',
}

def mot(tok):
    return f'<span class="mot" title="{MOT_TITLE.get(tok, tok)}">{tok}</span>'
def dirp(tok):
    return f'<span class="dir" title="{DIR_TITLE.get(tok, tok)}">{tok}</span>'

PLUS = '<span class="plus">+</span>'
AIR = '<span class="air">air</span>'
def cs():  # the faint step separator
    return ' <span class="cs">›</span> '
def ann(t):
    return f'<span class="ann">{t}</span>'

# ---------------------------------------------------------------- combo DSL
# each seq item is a tuple; constructors keep the data compact + readable
def G(*btns):       return ('grp', list(btns), None)    # button group (chain)
def GP(pre, *btns): return ('grp', list(btns), pre)     # prefixed group
def GC(*btns):      return ('grp', list(btns), 'cr.')   # crouching group
def JG(*btns):      return ('grp', list(btns), 'j.')    # jump-in group
def M(m, b):        return ('mot', m, b, False)         # motion + button
def MA(m, b):       return ('mot', m, b, True)          # AIR motion + button
def DB(d, b):       return ('dir', d, b)                # direction + button (D+HP…)
def CH(d, b):       return ('chg', d, b)                # charge + button
def SQ(m, b):       return ('seq', m, b)                # spelled motion + button
def DIR(d):         return ('dir1', d)                  # lone direction (U air-jump…)
def SP(name, m, b, air=False):  return ('sp', name, m, b, air)  # NAMED special/super (input in tooltip)
def PRE(t):         return ('pre', t)                   # connector glued to NEXT
def TAG(t):         return ('tag', t)                   # descriptor glued to PREV

def _sp_input(m, b, air):
    pre = 'air ' if air else ''
    if m.startswith('['):          # charge motion
        return f'{pre}charge {m} + {b}'
    return f'{pre}{m} + {b}'

def _grp(inner):    return f'<span class="grp">{inner}</span>'

def render_action(pc):
    k = pc[0]
    if k == 'grp':
        pre = pc[2] if len(pc) > 2 else None
        inner = (f'<span class="pfx">{pre}</span>' if pre else '') + ''.join(keycap(b) for b in pc[1])
        return _grp(inner)
    if k == 'mot':
        _, m, b, air = pc
        a = AIR if air else ''
        return _grp(a + mot(m) + PLUS + keycap(b))
    if k == 'dir':
        _, d, b = pc
        return _grp(dirp(d) + PLUS + keycap(b))
    if k == 'chg':
        _, d, b = pc
        return _grp(dirp(d) + PLUS + keycap(b))
    if k == 'seq':
        _, m, b = pc
        return _grp(mot(m) + PLUS + keycap(b))
    if k == 'dir1':
        return _grp(dirp(pc[1]))
    if k == 'sp':
        _, name, m, b, air = pc
        title = _sp_input(m, b, air)
        a = AIR if air else ''
        return f'<span class="grp">{a}<span class="sp" title="{title}">{name}</span></span>'
    return ''

def render_combo(seq):
    out, first, glue = [], True, False
    for pc in seq:
        k = pc[0]
        if k == 'pre':
            if not first:
                out.append(cs())
            out.append(ann(pc[1]) + ' ')
            glue = True
            first = False
            continue
        if k == 'tag':
            out.append(' ' + ann(pc[1]))
            continue
        if not first and not glue:
            out.append(cs())
        out.append(render_action(pc))
        first = False
        glue = False
    return f'<div class="combo">{"".join(out)}</div>'
