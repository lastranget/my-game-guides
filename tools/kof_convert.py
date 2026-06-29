# -*- coding: utf-8 -*-
"""Helpers used to turn raw GameFAQs FAQ pages into guide data.

Pipeline (see tools/README.md):
  1. tools/kof_fetch.sh <slug> <faq-id> raw.html        # download via Wayback
  2. python3 tools/kof_convert.py extract raw.html > faq.txt
  3. python3 tools/kof_convert.py bjenet  faq.txt > bjenet_combos.py   # B. Jenet combo list
     python3 tools/kof_convert.py athena  faq.txt > athena_matchups.py # Athena matchup chart

The `bjenet`/`athena` extractors are tuned to those specific FAQs' formats
(RTorrez 44220 / dante_croft 51436). They document how the committed
`bjenet_combos.py` / `athena_matchups.py` were produced; re-running needs the
matching source FAQ text. Other characters' combos were hand-transcribed in
`chardata.py` (small lists / prose-described sources).
"""
import sys, re, html as _html


def extract(htmltext):
    """Pull readable FAQ prose out of a GameFAQs page (faqtext div / <pre>)."""
    m = (re.search(r'<div[^>]*class="[^"]*faqtext[^"]*"[^>]*>(.*?)</div>\s*</div>', htmltext, re.S)
         or re.search(r'<pre[^>]*>(.*?)</pre>', htmltext, re.S))
    body = m.group(1) if m else htmltext
    body = re.sub(r'<br\s*/?>', '\n', body)
    body = re.sub(r'<[^>]+>', '', body)
    body = _html.unescape(body)
    return re.sub(r'\n{3,}', '\n\n', body)


# motion -> named-special token, for B. Jenet's combo notation (FAQ 44220)
_BJ_REPL = [
    (r'qcf,\s*qcf\s*\+\s*P', '@torpedo'), (r'qcf,\s*qcf\s*\+\s*K', '@aurora'),
    (r'qcb,\s*qcb\s*\+\s*E', '@anoi'),
    (r'd\s*\+\s*K(?:,\s*K){2,4}', '@harrier.B'), (r'd\s*\+\s*D(?:,\s*D){1,3}', '@harrier.D'),
    (r'qcf\s*\+\s*B', '@hind.B'), (r'qcf\s*\+\s*D', '@hind.D'),
    (r'qcf\s*\+\s*A', '@buffrass.A'), (r'qcf\s*\+\s*C', '@buffrass.C'),
    (r'qcb\s*\+\s*A', '@ivan.A'), (r'qcb\s*\+\s*C', '@ivan.C'),
    (r'qcb\s*\+\s*B', '@gulf.B'), (r'qcb\s*\+\s*D', '@gulf.D'),
    (r'df\s*\+\s*D', 'df+D'), (r'f\s*\+\s*B', 'f+B'),
    (r'\bfar sC\b', 'fC'), (r'\bshort jump C\b', 'shC'), (r'\bshort jump D\b', 'shD'),
    (r'\bcX D\b', 'cxD'), (r'\bin air,\s*', '@harrier.D, '), (r'sA~sC', 'sA, sC'), (r'\bland\b', '(land)'),
]
_END = {'@anoi': 'DC → An Oi', '@torpedo': 'Many Torpedo', '@aurora': 'Aurora', '@hind': 'The Hind',
        '@gulf': 'Gulf Tomahawk', '@ivan': 'Crazy Ivan', '@harrier': 'Harrier loop', '@buffrass': 'Buffrass'}


def _bj_conv(combo):
    s = combo
    for pat, rep in _BJ_REPL:
        s = re.sub(pat, rep, s)
    s = re.sub(r'd\s*\+\s*D', '@harrier.D', s)
    return ' > '.join(p.strip() for p in s.split(',') if p.strip())


def bjenet(text):
    def blk(a, b):
        i = text.index(a); j = text.index(b, i); return text[i + len(a):j]
    PAT = re.compile(r'(.+?)\s*-\s*([\d/]+)\s*-?\s*hits?\s*(\(C\))?', re.S)

    def parse(b):
        b = re.sub(r'\s+', ' ', b).strip()
        out = []
        for m in PAT.finditer(b):
            combo = m.group(1).strip().lstrip('- ').strip().replace('sCD.', 'sCD')
            if not combo:
                continue
            s = _bj_conv(combo)
            if m.group(3) and '(C)' not in s:
                s += ' > (C)'
            out.append((s, m.group(2)))
        return out

    def grp(s, counter=False):
        if counter: return 'counter'
        if '(DC)' in s: return 'dc'
        if '@torpedo' in s or '@aurora' in s: return 'super'
        if '@harrier' in s and '(C)' in s: return 'corner'
        if '@harrier' in s: return 'chain'
        return 'bnb'

    def name(s):
        toks = [t for t in s.split(' > ') if not t.startswith('(')]
        end = toks[-1] if toks else s
        for k, v in _END.items():
            if end.startswith(k): return v
        return 'Rolling Thunder' if end == 'df+D' else 'Normal chain'

    def diff(s):
        return 3 if '(DC)' in s else (2 if ('@harrier' in s or '(SC)' in s) else 1)
    print('# -*- coding: utf-8 -*-')
    print('# AUTO-GENERATED from GameFAQs FAQ 44220 (RTorrez) by tools/kof_convert.py — do not hand-edit.')
    print('def _load(C):\n    return [')
    main = blk('Beginner/Intermediate/Advance Combos', 'COUNTER HIT Combos')
    chit = blk('COUNTER HIT Combos', 'Quick-Shift Combos')
    for s, h in parse(main):
        print(f"        C({grp(s)!r}, {name(s)!r}, {s!r}, {h + 'h'!r}, {diff(s)}),")
    for s, h in parse(chit):
        print(f"        C('counter', {name(s)!r}, {s!r}, {h + 'h'!r}, {diff(s)}),")
    print('    ]')


def athena(text):
    lines = text.splitlines()
    i0 = next(i for i, l in enumerate(lines) if 'TIPS AGAINST ALL CHARACTERS' in l)
    i1 = next(i for i, l in enumerate(lines) if 'CURIOSITIES' in l)
    hdr = re.compile(r'^\s*\d+\s*[:.]?\s*AGAINST\s+(.+?)[:.]?\s*$', re.I)
    rows = []; cur = None; buf = []

    def clean(t):
        t = re.sub(r'\s+', ' ', t).strip().replace('´', '’').replace('`', '’')
        t = re.sub(r'([a-z])- ([a-z])', r'\1\2', t)              # de-hyphenate line wraps
        t = t.replace('&', '&amp;').replace('"', '&quot;')
        return (t + '.') if t and not t.endswith(('.', '!')) else t

    def flush():
        if cur is None: return
        txt = ' '.join(buf)
        ms = re.search(r'[Cc]han[cs]e\s+of\s+Vi\w*ory\s*:?\s*([\d.]+\s*/?\s*10|\?)', txt)
        score = re.sub(r'\s+', '', ms.group(1)) if ms else '?/10'
        if '/' not in score: score = '?/10'
        tip = clean(txt[:ms.start()] if ms else txt)
        if len(tip) > 5: rows.append((cur, score, tip))
    for l in lines[i0 + 1:i1]:
        m = hdr.match(l)
        if m:
            flush(); cur = m.group(1).strip().title().replace('Ex Kyo', 'EX Kyo'); buf = []
        elif cur is not None:
            buf.append(l)
    flush()
    print('# -*- coding: utf-8 -*-')
    print('# AUTO-GENERATED from GameFAQs FAQ 51436 (dante_croft) by tools/kof_convert.py')
    print('ATHENA_MATCHUPS = [')
    for n, s, t in rows:
        print(f"    ({n!r}, {s!r}, {t!r}),")
    print(']')


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else ''
    data = open(sys.argv[2], encoding='utf-8', errors='replace').read() if len(sys.argv) > 2 else ''
    if cmd == 'extract':
        print(extract(data))
    elif cmd == 'bjenet':
        bjenet(data)
    elif cmd == 'athena':
        athena(data)
    else:
        print(__doc__)
