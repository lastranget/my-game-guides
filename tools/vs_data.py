# -*- coding: utf-8 -*-
"""Data for the Vampire Savior (Darkstalkers 3) character guides (build_vs.py).
6-button game (LP/MP/HP/LK/MK/HK). Sourced from GameFAQs FAQs: Kao_Megura 5283
(movelists/system), KTanaka 1237, DJellybean 7976; character guides afroshouji
1243 (B.B. Hood), MKim 1248 (Morrigan), MKim 1247 (Lilith). Combos for Bulleta
are from afroshouji; Felicia/Morrigan/Lilith combos are built from the verified
movelists + VS's chain system (their sources explain the system rather than
listing combos). Specials shown by name (input in tooltip)."""
from gen import G, GC, JG, M, MA, DB, SQ, SP, PRE, TAG

def raw(h): return ('raw', h)
def C(grp, name, seq, note='', hits='', diff=1, core=False):
    return dict(grp=grp, name=name, seq=seq, note=note, hits=hits, diff=diff, core=core)

ORDER = ['bbhood', 'morrigan', 'lilith', 'felicia']
META = {
 'bbhood':  {'name': 'B.B. Hood', 'long': 'Bulleta', 'role': 'Trap zoner', 'ca': '#ff8fa3', 'pfx': 'BB'},
 'morrigan': {'name': 'Morrigan', 'long': 'Morrigan Aensland', 'role': 'All-round rushdown', 'ca': '#b388ff', 'pfx': 'MO'},
 'lilith':  {'name': 'Lilith', 'long': 'Lilith', 'role': 'Fast pressure', 'ca': '#ff9ad5', 'pfx': 'LI'},
 'felicia': {'name': 'Felicia', 'long': 'Felicia', 'role': 'Combo rushdown', 'ca': '#7ee0b0', 'pfx': 'FE'},
}

COMBO_GROUPS = [
 ('bnb',    'Bread &amp; butter — chains'),
 ('jumpin', 'Jump-in confirms'),
 ('special','Chain into a special'),
 ('super',  'Into an EX super'),
 ('otg',    'Pursuit / OTG &amp; corner'),
 ('df',     'Dark Force &amp; resets'),
]

# ============================================================ B.B. HOOD (Bulleta) — explicit (afroshouji)
COMBOS = {}
COMBOS['bbhood'] = [
 C('bnb', 'Stand chain', [G('LP','LK','MP','MK','HP')],
   'Her basic zig-zag chain (skip MP on small characters — it whiffs).', '7h', 1, True),
 C('jumpin', 'Jump-in chain', [JG('MP','MK'), PRE('land'), G('LP','LK','MP','MK','HP')],
   'Hop MP→MK, land into the full ground chain.', '7h', 1, True),
 C('special', 'Chain → Smile &amp; Missile', [JG('LP','LK','MP','HP'), PRE('land'), G('LP'), TAG('XX'),
   SP('Smile &amp; Missile','[B]F','HP')],
   'On large opponents — jump chain, land, jab, cancel into the HP missile.', '6h', 2),
 C('special', 'Tricky Basket → Typhoon', [PRE('corner'), JG('MP'), PRE('land'), G('LP','LK'),
   DB('F','MP'), TAG('XX'), SP('Sentimental Typhoon','HCB','MK'), TAG('ES'), SP('Pursuit','U','P')],
   'Corner: chain into the Tricky Basket, ES Sentimental Typhoon, then an ES Pursuit.', '', 3, core=True),
 C('otg', 'Low chain → Pursuit', [JG('MP','MK'), PRE('land'), GC('LP','LK','MK'), GC('HK'),
   TAG('sweep · XX'), SP('Pursuit','U','K'), TAG('ES')],
   'All-low confirm into the sweep, ES Pursuit for the OTG hits.', '18h', 2),
 C('otg', 'Corner max (large opp)', [JG('LP','LK','MP','HP'), PRE('land'), G('LP','LK'), DB('F','MP'),
   G('MK'), GC('HK'), TAG('sweep · XX'), SP('Pursuit','U','K'), TAG('ES')],
   'The 21-hit corner punish on big characters — tight links after the Basket hop.', '21h', 3),
 C('super', 'Chain → Cool Hunting', [G('LP','LK','MP','HP'), TAG('XX'), SP('Cool Hunting','HCF','PP')],
   'Cancel a chain into the gun super for big damage / chip.', '', 2, core=True),
 C('special', 'Cheer &amp; Fire confirm', [G('LP','LK'), TAG('XX'), SP('Cheer &amp; Fire','DP','P')],
   'Quick chain into the flame — her anti-air-ish poke ender.', '', 1),
]

# ============================================================ MORRIGAN — authored from chains + movelist
COMBOS['morrigan'] = [
 C('bnb', 'Stand chain → Shadow Blade', [G('LP','LK','MP','MK','HP'), TAG('XX'), SP('Shadow Blade','DP','P')],
   'Her bread-and-butter zig-zag chain into the dragon-punch.', '', 1, core=True),
 C('bnb', 'Crouch chain → Soul Fist', [GC('LP','LK','MP'), TAG('XX'), SP('Soul Fist','QCF','P')],
   'Low confirm into the fireball — safe and easy.', '', 1),
 C('jumpin', 'Jump-in BnB', [JG('HP'), PRE('land'), G('LP','LK','MP','MK','HP'), TAG('XX'),
   SP('Shadow Blade','DP','P')],
   'Deep jumping HP into the full chain + Shadow Blade.', '', 1, core=True),
 C('special', 'Chain → Vector Drain', [G('LP','LK'), PRE('then'), SP('Vector Drain','HCB','HP'), TAG('command throw')],
   'Tick a light, then the command grab — a frame trap into a throw.', '', 2),
 C('super', 'Chain → Finishing Shower', [G('LP','LK','MP','HP'), TAG('XX'), SP('Finishing Shower','MP-LP-B-LK-MK','')],
   'Cancel a chain into the missile super (aim the shots with d / u).', '', 2, core=True),
 C('super', 'Chain → Darkness Illusion', [G('LP','LK'), TAG('XX'), SP('Darkness Illusion','LP-LP-F-LK-HP','',air=True)],
   'Her signature hyper — easiest after a short confirm; air-OK.', '', 3),
 C('otg', 'Air chain → air Soul Fist', [PRE('air'), G('LP','LK','MP','HP'), TAG('XX'),
   SP('Soul Fist','QCF','P',air=True)],
   'Off a launch / air-to-air, chain in the air and fire on the way down.', '', 2),
 C('df', 'Astral Vision pressure', [SP('Astral Vision','P+K',''), TAG('Dark Force'), PRE('then'),
   G('LP','LK','MP','MK','HP'), TAG('mirror hits')],
   'Activate the mirror, then chain — the clone doubles every hit for huge damage.', '', 3),
]

# ============================================================ LILITH — authored from chains + movelist
COMBOS['lilith'] = [
 C('bnb', 'Stand chain → Shining Blade', [G('LP','LK','MP','MK','HP'), TAG('XX'), SP('Shining Blade','DP','P')],
   'Her zig-zag chain into the rising blade.', '', 1, core=True),
 C('bnb', 'Crouch chain → Soul Flash', [GC('LP','LK','MP'), TAG('XX'), SP('Soul Flash','QCF','P')],
   'Low confirm into the projectile.', '', 1),
 C('jumpin', 'Jump-in BnB', [JG('HP'), PRE('land'), G('LP','LK','MP','MK','HP'), TAG('XX'),
   SP('Shining Blade','DP','P')],
   'Deep jump HP, full chain, blade.', '', 1, core=True),
 C('special', 'Chain → Merry Turn', [G('LP','LK','MP'), TAG('XX'), SP('Merry Turn','QCB','K')],
   'Chain into the rolling kick for a knockdown.', '', 1),
 C('super', 'Chain → Splendor Love', [G('LP','LK','MP','MK','HP'), TAG('XX'), SP('Splendor Love','DP','KK')],
   'Cancel the chain into her rushing kick super.', '', 2, core=True),
 C('super', 'Chain → Luminous Illusion', [G('LP','LK'), TAG('XX'), SP('Luminous Illusion','LP-LP-F-LK-HP','',air=True)],
   'Her big air super — confirm off a short chain; air-OK.', '', 3),
 C('otg', 'Mystic Arrow okizeme', [G('LP','LK','MP'), TAG('XX'), SP('Mystic Arrow','HCB','P'),
   PRE('then'), SP('Pursuit','U','P')],
   'Arrow knocks down; follow with a Pursuit / safe-jump set-up.', '', 2),
 C('df', 'Mirror Doll pressure', [SP('Mirror Doll','HP+HK',''), TAG('Dark Force'), PRE('then'),
   G('LP','LK','MP','MK','HP'), TAG('mirror hits')],
   'Like Morrigan’s Astral Vision — the doll doubles your chain.', '', 3),
]

# ============================================================ FELICIA — authored from chains + movelist
COMBOS['felicia'] = [
 C('bnb', 'Stand chain', [G('LP','LK','MP','MK','HP','HK')],
   'Felicia’s full six-hit zig-zag chain — she’s one of the best chain characters.', '6h', 1, core=True),
 C('bnb', 'Chain → Rolling Buckler', [G('LP','LK','MP','MK'), TAG('XX'), SP('Rolling Buckler','QCF','P'),
   TAG('→ Uppercut (P)')],
   'Chain into the roll, then tap P for the rising-claw finish.', '', 2, core=True),
 C('jumpin', 'Jump-in BnB', [JG('MK'), JG('HK'), PRE('land'), G('LP','LK','MP','MK','HP'), TAG('XX'),
   SP('Delta Kick','DP','K')],
   'Hop kicks, land, chain, Delta Kick ender (knocks down for OTG).', '', 1, core=True),
 C('special', 'Chain → Cat Spike', [G('LP','LK','MP'), TAG('XX'), SP('Cat Spike','DP','P')],
   'Quick chain into her anti-air dragon-punch.', '', 1),
 C('super', 'Chain → Dancing Flash', [G('LP','LK','MP','MK','HP'), TAG('XX'), SP('Dancing Flash','HCF','PP')],
   'Cancel the chain into the rolling super.', '', 2, core=True),
 C('super', 'Chain → Please Help Me', [G('LP','LK','MP','HP'), TAG('XX'), SP('Please Help Me','HCF','KK')],
   'The cat-swarm super — LK+MK straight, MK+HK jumping, LK+HK diving.', '', 2),
 C('otg', 'Knockdown → Toy Touch', [SP('Delta Kick','DP','K'), TAG('knockdown'), PRE('then'),
   SP('Toy Touch','D,D','P'), TAG('OTG')],
   'After a Delta Kick knockdown, Toy Touch (d,d+P) keeps the OTG pressure going.', '', 2),
 C('df', 'Cat Helper loop', [SP('Cat Helper','P+K',''), TAG('Dark Force'), PRE('then'),
   G('LP','LK','MP','MK'), TAG('Kitty follows up')],
   'Kitty attacks after each of your hits — set up big extended combos.', '', 3),
 C('otg', 'Corner Rolling loop', [PRE('corner'), G('LP','LK','MP'), TAG('XX'), SP('Rolling Buckler','QCF','P'),
   TAG('Sliding Kick (K)'), PRE('OTG'), GC('LP'), G('LP','LK'), TAG('repeat')],
   'In the corner the Sliding-Kick ending of the Buckler lets you relink and loop.', '', 3),
]

# ============================================================ movelists (specials + supers + throws)
MOVES = {
 'bbhood': [
   ('Special moves', [
     ('Smile &amp; Missile', 'charge B,F + P/K; ground missiles', [DB('[B]F','P')]),
     ('Happy &amp; Missile', 'charge D,U + P/K; air missiles', [DB('[D]U','P')]),
     ('Cheer &amp; Fire', 'DP + P; flame', [M('DP','P')]),
     ('Shyness &amp; Strike', 'QCB + P (hold/release); basket', [M('QCB','P')]),
     ('Sentimental Typhoon', 'close HCB + MK/HK', [M('HCB','MK')]),
     ('Tricky Basket', 'b/f + MP', [DB('F','MP')]),
     ('Malice &amp; Mine', 'df + HK; low mine', [DB('DF','HK')]),
     ('Tell Me Why', 'd + KKK; crawl', [DB('D','K')]),
   ]),
   ('EX supers', [
     ('Cool Hunting', 'HCF + PP; guns', [M('HCF','PP')]),
     ('Beautiful Memory', 'HCF + KK', [M('HCF','KK')]),
     ('Apple For You', 'HCB + KK', [M('HCB','KK')]),
     ('Dark Force · Bazooka Ransha', 'same-strength P+K', [SP('Bazooka Ransha','P+K','')]),
   ]),
   ('Throws &amp; pursuit', [
     ('Hold &amp; Cut', 'close b/f + MP/HP', [DB('F','HP')]),
     ('Law of the Bullet', 'Pursuit: u + P/K when foe is down', [SP('Pursuit','U','P')]),
   ]),
 ],
 'morrigan': [
   ('Special moves', [
     ('Soul Fist', 'QCF + P (air); fireball', [M('QCF','P')]),
     ('Shadow Blade', 'DP + P; dragon-punch', [M('DP','P')]),
     ('Vector Drain', 'close HCB + MP/HP; command throw', [M('HCB','HP')]),
     ('Valkyrie Turn', 'HCB + K, then K; invincible re-entry', [M('HCB','K')]),
     ('Flying / Vertical Dash', 'hold b,b/f,f · tap d,u', [raw('<span class="dir">D</span><span class="dir">U</span>')]),
   ]),
   ('EX supers', [
     ('Darkness Illusion', 'LP,LP,f,LK,HP (air)', [SP('Darkness Illusion','LP-LP-F-LK-HP','',air=True)]),
     ('Finishing Shower', 'MP,LP,b,LK,MK; missiles', [SP('Finishing Shower','MP-LP-B-LK-MK','')]),
     ('Cryptic Needle', 'f,HP,MP,LP,f', [SP('Cryptic Needle','F-HP-MP-LP-F','')]),
     ('Dark Force · Astral Vision', 'same-strength P+K; mirror clone', [SP('Astral Vision','P+K','')]),
   ]),
   ('Throws &amp; pursuit', [
     ('Moon Tracer', 'close b/f + MP/HP', [DB('F','HP')]),
     ('Shell Pierce', 'Pursuit: u + P/K when foe is down', [SP('Pursuit','U','P')]),
   ]),
 ],
 'lilith': [
   ('Special moves', [
     ('Soul Flash', 'QCF + P (air); projectile', [M('QCF','P')]),
     ('Shining Blade', 'DP + P; rising blade', [M('DP','P')]),
     ('Merry Turn', 'QCB + K; rolling kick', [M('QCB','K')]),
     ('Mystic Arrow', 'HCB + P; homing arrow', [M('HCB','P')]),
     ('High Jump', 'tap d, ub~uf', [raw('<span class="dir">D</span><span class="dir">UF</span>')]),
   ]),
   ('EX supers', [
     ('Splendor Love', 'DP + KK; rushing kicks', [M('DP','KK')]),
     ('Luminous Illusion', 'LP,LP,f,LK,HP (air)', [SP('Luminous Illusion','LP-LP-F-LK-HP','',air=True)]),
     ('Gloomy Puppet Show', 'HCF + KK (2 stocks)', [M('HCF','KK')]),
     ('Dark Force · Mindless Doll', 'LP+LK / HP+HK; clone', [SP('Mindless Doll','P+K','')]),
   ]),
   ('Throws &amp; pursuit', [
     ('Innocent Hug', 'close b/f + MP/HP', [DB('F','HP')]),
     ('Toe Pierce', 'Pursuit: u + P/K when foe is down', [SP('Pursuit','U','P')]),
   ]),
 ],
 'felicia': [
   ('Special moves', [
     ('Rolling Buckler', 'QCF + P,P; → Uppercut/Slide', [M('QCF','P')]),
     ('Cat Spike', 'DP + P; anti-air', [M('DP','P')]),
     ('Delta Kick', 'DP + K; air OK; knockdown', [M('DP','K')]),
     ('Hell Cat', 'close HCB + MK/HK', [M('HCB','MK')]),
     ('Toy Touch', 'd,d + P when foe is down; OTG', [SP('Toy Touch','D,D','P')]),
     ('EX Charge', 'd,d + KK (hold); fills stock', [SP('EX Charge','D,D','KK')]),
   ]),
   ('EX supers', [
     ('Dancing Flash', 'HCF + PP; rolling super', [M('HCF','PP')]),
     ('Please Help Me', 'HCF + KK; cat swarm', [M('HCF','KK')]),
     ('Dark Force · Cat Helper', 'same-strength P+K; Kitty', [SP('Cat Helper','P+K','')]),
   ]),
   ('Throws &amp; pursuit', [
     ('Panic Nail', 'close b/f + MP/HP', [DB('F','HP')]),
     ('Sankaku Tobi', 'wall-jump (triangle jump)', [raw('<span class="ann">wall-jump</span>')]),
     ('Romper Cat', 'Pursuit: u + P/K when foe is down', [SP('Pursuit','U','P')]),
   ]),
 ],
}

# one-screen "special moves" card per character (specials + EX supers; throws live in the system section)
ONESCREEN = {c: [(nm, note, p) for label, rows in MOVES[c] if 'Throw' not in label
                 for nm, note, p in rows] for c in ORDER}

# ============================================================ strengths/weaknesses
SW = {
 'bbhood': (['Premier <b>zoner</b> — high, low, and air missiles plus traps lock the screen down.',
             '<b>Cool Hunting</b> does huge damage and chip.',
             'Sneaky low/overhead mix-ups (Malice &amp; Mine, crawl) and a double jump.'],
            ['Weak up close once you’re past the missiles.',
             'Several specials are slow / punishable on block.',
             'Leans on spacing — gets opened up if cornered.']),
 'morrigan': (['Superb <b>all-rounder</b> — fireball, dragon-punch, command throw, air mobility.',
               'Flying dash + vertical dash + Astral Vision make her offense relentless.',
               '<b>Darkness Illusion</b> is a devastating, easy-to-confirm hyper.'],
              ['No single dominant tool — wins on fundamentals.',
               'Astral-Vision execution takes work to maximise.']),
 'lilith': (['Very <b>fast</b> pressure with great air movement.',
             'Soul Flash + Shining Blade cover ground and anti-air.',
             'The Mindless-Doll clone enables big doubled-up combos.'],
            ['Low damage per hit — needs combos and the doll to really hurt.',
             'Frail; lives in the opponent’s face, so a slip is costly.']),
 'felicia': (['One of the <b>best chain characters</b> in the game — long, easy combos.',
              'Great speed, OTG game (Toy Touch) and wall/triangle-jump mobility.',
              '<b>EX Charge</b> lets her bank meter for free.'],
             ['Low damage / frail — she has to combo to win.',
              'No real projectile zoning; must get in.']),
}

# ============================================================ strategy (per character)
STRATEGY = {
 'bbhood': [
   ('Build the wall', 'Alternate <b>Smile &amp; Missile</b> (ground, high/low) and <b>Happy &amp; Missile</b> '
    '(air) to fence the opponent out; walk behind them.'),
   ('Mix the openings', 'Once they respect the missiles, sneak <b>Malice &amp; Mine</b> (low) and the crawl, '
    'then convert into a chain.'),
   ('Cash it in', 'Confirm any chain into <b>Cool Hunting</b>, or end in <b>Sentimental Typhoon → ES Pursuit</b> '
    'in the corner for max damage.'),
 ],
 'morrigan': [
   ('Control the air', 'Flying dash + air <b>Soul Fist</b> let you approach safely; <b>Valkyrie Turn</b> '
    'is invincible to escape pressure.'),
   ('Open them up', 'Tick into <b>Vector Drain</b> (command throw) against blockers; chain into Shadow Blade '
    'on hit.'),
   ('Astral Vision', 'Pop the mirror when you’ve got Chi — every chain hits twice for huge damage.'),
 ],
 'lilith': [
   ('Stay in their face', 'Use her speed and air dashes to keep pressure; Soul Flash covers your approach.'),
   ('Anti-air', '<b>Shining Blade</b> swats jump-ins; <b>Merry Turn</b> for knockdowns.'),
   ('Doll combos', 'Mindless Doll doubles your chains — the key to her damage.'),
 ],
 'felicia': [
   ('Get in &amp; chain', 'No projectile, so close with dashes, the wall-jump and <b>Rolling Buckler</b>, then '
    'run her long chains.'),
   ('OTG game', 'End combos in <b>Delta Kick</b>, then <b>Toy Touch</b> / Pursuit for free OTG damage.'),
   ('Bank meter', 'Use <b>EX Charge</b> in down-time to stock up for Dancing Flash / Please Help Me.'),
 ],
}
