# -*- coding: utf-8 -*-
"""Data for the Garou: Mark of the Wolves combo guides (B. Jenet, Terry).
4-button game: A=LP, B=LK, C=HP, D=HK. Sources (GameFAQs, via Wayback):
JKuroki 6097 (movelists/system), MGA 7828 (Combo FAQ), Shirow 14695 (Terry),
ghoward11 8673 (Terry), TalbainEric 14967 (B. Jenet). Combos are from MGA's
combo FAQ + the verified movelists + Garou's Brake/Break and super-cancel rules;
specials shown by name (input in tooltip)."""
from gen import G, GC, JG, M, MA, DB, SQ, SP, PRE, TAG

def raw(h): return ('raw', h)
def C(grp, name, seq, note='', hits='', diff=1, core=False):
    return dict(grp=grp, name=name, seq=seq, note=note, hits=hits, diff=diff, core=core)

ORDER = ['terry', 'bjenet']
META = {
 'terry':  {'name': 'Terry Bogard', 'short': 'Terry', 'role': 'All-round', 'ca': '#ff8a4c', 'pfx': 'T'},
 'bjenet': {'name': 'B. Jenet', 'short': 'B. Jenet', 'role': 'Speed rushdown', 'ca': '#ffcf5a', 'pfx': 'BJ'},
}

COMBO_GROUPS = [
 ('bnb',    'Bread &amp; butter'),
 ('chain',  'Pokes &amp; low confirms'),
 ('special','Brake / Break cancels'),
 ('super',  'Into a Super (S.Power)'),
 ('top',    'Potential, T.O.P. &amp; corner'),
]

COMBOS = {}
COMBOS['terry'] = [
 C('bnb', 'BnB → Power Wave', [JG('C'), G('C'), DB('F','C'), TAG('XX'), SP('Power Wave','QCF','C')],
   'Jump-in, close C, the f+C command hit, cancel into Power Wave. Terry’s staple.', '', 1, core=True),
 C('bnb', 'BnB → Power Dunk', [JG('C'), G('D'), TAG('XX'), SP('Power Dunk','DP','D')],
   'Jump-in, close D, into the Power Dunk (knockdown anti-air ender).', '', 1, core=True),
 C('bnb', 'BnB → Crack Shoot', [JG('C'), G('C'), TAG('XX'), SP('Crack Shoot','QCB','B')],
   'Crack Shoot ender — an overhead-ish flip kick, knocks down.', '', 1),
 C('chain', 'Low confirm', [GC('B'), GC('B'), TAG('XX'), SP('Power Wave','QCF','A')],
   'Two crouch B into the LP Power Wave — opens crouchers, safe poke string.', '', 1),
 C('special', 'Power Charge string', [JG('C'), G('C'), DB('F','C'), TAG('XX'), SP('Power Charge','F,F','C'),
   TAG('×3')],
   'End in Power Charge and mash it up to three hits. Drop the f+C on tougher links.', '', 2),
 C('special', 'Power Dunk → Break → juggle', [JG('C'), G('C'), SP('Power Dunk','DP','D'),
   TAG('Break (A+B)'), PRE('juggle'), SP('Power Charge','F,F','C')],
   'Brake the Power Dunk’s first hit with A+B, then juggle — Terry’s signature damage.', '', 3, core=True),
 C('super', 'BnB → Power Geyser', [JG('C'), G('C'), DB('F','C'), TAG('XX'), SP('Power Geyser','QCFx2','A')],
   'Hit-confirm the chain into the Power Geyser super (S.Power).', '', 2, core=True),
 C('super', 'BnB → Buster Wolf', [JG('C'), G('C'), DB('F','C'), TAG('XX'), SP('Buster Wolf','QCFx2','B')],
   'Same confirm into Buster Wolf — the famous rushing super.', '', 2),
 C('top', 'Confirm → Potential Buster Wolf', [GC('B'), GC('B'), G('C'), TAG('XX'),
   SP('Buster Wolf (Potential)','QCFx2','D')],
   'With two power stocks, end in the Potential (P.Power) Buster Wolf for big damage.', '', 2),
 C('top', 'Break → Power Geyser', [JG('C'), G('C'), SP('Power Dunk','DP','D'), TAG('Break'),
   PRE('then'), SP('Power Geyser','QCFx2','A')],
   'Brake the Dunk and super-cancel into Power Geyser.', '', 3),
 C('top', 'T.O.P. attack combo', [PRE('in T.O.P.'), JG('C'), G('C'), TAG('XX'), SP('Max Dunk','CD',''),
   TAG('T.O.P. attack')],
   'Inside your T.O.P. zone, CD is a powered T.O.P. attack you can cancel a chain into.', '', 2),
 C('special', 'Feint pressure', [G('C'), TAG('close'), SP('Burn Knuckle feint','f+AC',''), PRE('then'),
   G('A'), TAG('XX'), SP('Burn Knuckle','QCB','A')],
   'Close C, feint the Burn Knuckle (f+AC), then a jab links — a frame-trap into the real Knuckle.', '', 3),
]

COMBOS['bjenet'] = [
 C('bnb', 'BnB → Crazy Ivan', [JG('C'), G('D'), TAG('XX'), SP('Crazy Ivan','QCB','C')],
   'Jump-in, close D, into Crazy Ivan — her everyday knockdown.', '', 1, core=True),
 C('bnb', 'BnB → The Hind', [JG('C'), G('D'), TAG('XX'), SP('The Hind','QCF','D')],
   'Into The Hind (use the B version for an easier link).', '', 1, core=True),
 C('bnb', 'BnB → Buffrass', [JG('C'), G('D'), TAG('XX'), SP('Buffrass','QCF','A')],
   'Buffrass (tornado) ender for chip / space control.', '', 1),
 C('bnb', 'BnB → Gulf Tomahawk', [JG('C'), G('D'), TAG('XX'), SP('Gulf Tomahawk','QCB','B')],
   'Overhead crescent-kick ender.', '', 1),
 C('chain', 'Low confirm', [GC('B'), GC('B'), TAG('XX'), SP('The Hind','QCF','B')],
   'Crouch B × 2 into the B Hind — opens crouchers.', '', 1),
 C('special', 'The Hind → Harrier Bee', [JG('C'), G('C'), SP('The Hind','QCF','D'), TAG('Brake'),
   PRE('then'), SP('Harrier Bee','D','D',air=True)],
   'Her signature: Brake The Hind, then dive with Harrier Bee — safe, frame-positive pressure.', '', 2, core=True),
 C('special', 'Harrier loop', [PRE('air'), SP('Harrier Bee','D','D',air=True), PRE('land'), G('C'),
   SP('The Hind','QCF','D'), TAG('Brake'), PRE('then'), SP('Harrier Bee','D','D',air=True)],
   'Loop The Hind → Harrier to keep relentless pressure (and build meter).', '', 3),
 C('super', 'BnB → Many Many Torpedo', [JG('C'), G('C'), TAG('XX'), SP('Many Many Torpedo','QCFx2','A')],
   'Hit-confirm into the torpedo super (S.Power).', '', 2, core=True),
 C('super', 'BnB → Aurora', [JG('C'), G('C'), TAG('XX'), SP('Aurora','QCFx2','B')],
   'Aurora is a great anti-air / corner-ender super.', '', 2),
 C('top', 'Confirm → Potential Aurora', [GC('B'), GC('B'), G('C'), TAG('XX'),
   SP('Aurora (Potential)','QCFx2','D')],
   'With two stocks, the Potential Aurora for big damage.', '', 2),
 C('top', 'Hind → Harrier → Torpedo', [JG('C'), G('C'), SP('The Hind','QCF','D'), TAG('Brake'),
   SP('Harrier Bee','D','D',air=True), PRE('land'), SP('Many Many Torpedo','QCFx2','A')],
   'The pressure loop cashed into the super for the kill.', '', 3),
 C('top', 'T.O.P. Rolling Thunder', [PRE('in T.O.P.'), JG('C'), G('C'), TAG('XX'),
   SP('Rolling Thunder','CD',''), TAG('T.O.P. attack')],
   'Inside the T.O.P. zone, cancel a chain into her CD T.O.P. attack.', '', 2),
]

# one-screen "special moves" card per character (specials + supers + T.O.P.)
MOVES = {
 'terry': [
   ('Specials', [
     ('Power Wave', 'QCF + A/C; ground fireball', [M('QCF','A')]),
     ('Burn Knuckle', 'QCB + A/C; rush punch (feintable)', [M('QCB','A')]),
     ('Crack Shoot', 'QCB + B/D; flip kick', [M('QCB','B')]),
     ('Power Dunk', 'F,D,DF + B/D; Break-cancel with A+B', [M('DP','D')]),
     ('Power Charge', 'F,F + A/C (up to 3×)', [SQ('F,F','C')]),
     ('Buster Throw', 'close C', [DB('F','C')]),
   ]),
   ('Supers (S.Power) / Potentials (P.Power)', [
     ('Power Geyser', 'QCF,QCF + A (S) / + C (Potential)', [M('QCFx2','A')]),
     ('Buster Wolf', 'QCF,QCF + B (S) / + D (Potential)', [M('QCFx2','B')]),
     ('T.O.P. · Max Dunk', 'CD inside the T.O.P. zone', [raw('<span class="dir">CD</span>')]),
   ]),
 ],
 'bjenet': [
   ('Specials', [
     ('Buffrass', 'QCF + A/C; tornado projectile', [M('QCF','A')]),
     ('Crazy Ivan', 'QCB + A/C; knockdown swing', [M('QCB','A')]),
     ('Gulf Tomahawk', 'QCB + B/D; overhead crescent', [M('QCB','B')]),
     ('The Hind', 'QCF + B/D; Brake-cancellable', [M('QCF','D')]),
     ('Harrier Bee', 'air d + B/D (×4); dive after The Hind', [MA('D','D')]),
     ('Bye-Bye Boo', 'close C; throw', [DB('F','C')]),
   ]),
   ('Supers (S.Power) / Potentials (P.Power)', [
     ('Many Many Torpedo', 'QCF,QCF + A (S) / + C (Potential)', [M('QCFx2','A')]),
     ('Aurora', 'QCF,QCF + B (S) / + D (Potential)', [M('QCFx2','B')]),
     ('T.O.P. · Rolling Thunder', 'CD inside the T.O.P. zone', [raw('<span class="dir">CD</span>')]),
   ]),
 ],
}
ONESCREEN = {c: [(nm, note, p) for _, rows in MOVES[c] for nm, note, p in rows] for c in ORDER}
