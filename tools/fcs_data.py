# -*- coding: utf-8 -*-
"""Data for the Felicia / Cyclops / Storm MvC2 guide set (build_fcs.py).
Sourced from GameFAQs FAQs (Felicia: SBAllen 7414, EZero 8530; Cyclops: Z-Force
7893, PhatDan81 7945, TBui 9838; Storm: The_fireboy 23122, RSmith 8320,
Gotenks2000 8321, Shinkuu_r 8330). Old 6-button notation normalised to MvC2's
LP/HP/LK/HK; specials shown by name (input in tooltip)."""
from gen import G, GC, JG, M, MA, DB, SQ, SP, PRE, TAG

def raw(h): return ('raw', h)
def C(grp, name, seq, note='', hits='', diff=1, core=False):
    return dict(grp=grp, name=name, seq=seq, note=note, hits=hits, diff=diff, core=core)

ORDER = ['felicia', 'cyclops', 'storm']
META = {
 'felicia': {'name': 'Felicia',  'role': 'Rushdown point', 'ca': '#ff9ad5', 'pfx': 'FE'},
 'cyclops': {'name': 'Cyclops',  'role': 'Assist anchor',  'ca': '#7cc0ff', 'pfx': 'CY'},
 'storm':   {'name': 'Storm',    'role': 'Anchor / runaway','ca': '#c9b6ff','pfx': 'ST'},
}

COMBO_GROUPS = [
 ('bnb',    'Bread &amp; butter — meterless'),
 ('air',    'Launcher → Aerial Rave'),
 ('super',  'Hit-confirm into a Hyper (1 bar)'),
 ('otg',    'OTG &amp; relaunch'),
 ('cancel', 'Special-cancel &amp; beam links'),
 ('corner', 'Corner, loops &amp; big damage'),
 ('team',   'Team — DHC &amp; assists'),
]

# ============================================================ FELICIA combos
COMBOS = {}
COMBOS['felicia'] = [
 C('bnb', 'Bread &amp; butter', [G('LP','LK'), SP('Sand Splash','QCF','K')],
   'Quick chain into her full-screen Sand Splash — safe, easy, your everyday poke-confirm.', '', 1, True),
 C('bnb', 'Delta Kick ender', [G('LP','LK'), SP('Delta Kick','DP','K')],
   'Ends in a knockdown you can OTG off of.', '', 1),
 C('bnb', 'Low confirm', [GC('LK','LK'), GC('HK'), SP('Sand Splash','QCF','K')],
   'All lows into the sweep + Sand Splash — opens crouchers, leaves them OTG-able.', '', 1),
 C('air', 'Aerial Rave → HP', [GC('LK'), G('HK'), TAG('launch'), PRE('sj'), G('LP','LK','LP','LK','HP')],
   'Her core air string (tap-climb the magic series).', '', 1, True),
 C('air', 'Aerial Rave → Delta Kick', [GC('LK'), G('HK'), TAG('launch'), PRE('sj'),
   G('LP','LK','LP','LK'), SP('Delta Kick','DP','K',air=True)],
   'Delta Kick is her best air-combo finisher and sets up an OTG.', '', 2, True),
 C('air', 'Jump-in → Aerial Rave', [JG('LP','LP'), PRE('land'), PRE('dash'), GC('LK'), G('HK'),
   TAG('launch'), PRE('sj'), G('LP','LK','LP','LK'), SP('Delta Kick','DP','K',air=True)],
   'Dash after landing the jump-in to stay close enough for the full chain.', '', 2),
 C('super', 'Into Dancing Flash', [G('LP','LK','LP','LK','HP'), DB('B','HK'), TAG('B+HK'),
   SP('Dancing Flash','QCF','PP')],
   'B+HK is a 2-hit handstand kick that links into any super. ~50% with a jump-in.', '', 2, True),
 C('super', 'Into Hyper Sand Splash', [G('LP','LK','LP','LK','HP'), DB('B','HK'),
   SP('Hyper Sand Splash','QCF','KK')],
   'Full-screen sand super — also her best long-range mistake punisher.', '', 1),
 C('super', 'Sand Splash super-cancel', [G('LP','LK'), GC('HK'), SP('Sand Splash','QCF','K'),
   TAG('XX'), SP('Hyper Sand Splash','QCF','KK')],
   'Cancel the Sand Splash special straight into its super.', '', 2),
 C('cancel', 'Rolling Buckler → Rising Slash', [G('LP','LK','HP'), SP('Rolling Buckler','QCF','P'),
   TAG('let it hit once'), SP('Rising Slash','QCF+P →','HP')],
   'Let the buckler hit once, then HP for the 3-hit rising slash. Corner ender = OTG.', '', 2),
 C('otg', 'Buckler → Sliding Kick → relaunch', [G('LP','LK','HP'), SP('Rolling Buckler','QCF','P'),
   SP('Sliding Kick','QCF+P →','K'), PRE('OTG'), GC('LK'), G('HK'), TAG('launch'), PRE('sj'),
   G('LP','LK','LP','LK'), SP('Delta Kick','DP','K',air=True)],
   'Sliding Kick leaves you point-blank for the OTG relaunch — the heart of her damage.', '', 3),
 C('otg', 'cr.HK OTG → super', [GC('LK'), GC('HK'), TAG('OTG'), GC('HK'), SP('Dancing Flash','QCF','PP')],
   'cr.HK knocks down; OTG a second cr.HK (cancellable) into the super. Less roll time than Sliding Kick.', '', 2),
 C('corner', 'Buckler → Sliding Kick → Help Me!', [JG('HP'), PRE('land'), G('LP','HP'),
   SP('Rolling Buckler','QCF','P'), SP('Sliding Kick','QCF+P →','K'), TAG('XX'),
   SP('Please Help Me!','QCB','KK'), TAG('mash')],
   'The "holy-crap-that-hurts" route — ~50%+. Mash the super for extra cats/hits.', '', 3, True),
 C('corner', 'Buckler → Sliding Kick → Dancing Flash', [G('LP','LK','HP'), SP('Rolling Buckler','QCF','P'),
   SP('Sliding Kick','QCF+P →','K'), GC('HK'), TAG('OTG'), SP('Dancing Flash','QCF','PP')],
   'OTG the cr.HK after the slide, then super. Reliable big-damage corner combo.', '', 3),
 C('corner', 'Help Me! loop', [PRE('corner'), G('LP','LK','HP'), SP('Rolling Buckler','QCF','P'),
   SP('Sliding Kick','QCF+P →','K'), SP('Please Help Me!','QCB','KK'), GC('HK'), TAG('OTG'),
   SP('Please Help Me!','QCB','KK'), TAG('repeat — needs 3+ bars')],
   'In the very corner you can OTG-loop Help Me! with cr.HK for absurd damage (drains the bar fast).', '', 3),
 C('team', 'DHC kill', [G('LP','LK','LP','LK','HP'), DB('B','HK'), SP('Dancing Flash','QCF','PP'),
   PRE('DHC'), SP('Mega Optic Blast','QCF','PP'), TAG('Cyclops'), PRE('DHC'),
   SP('Lightning Storm','HCF','PP'), TAG('Storm')],
   'Felicia builds the meter, the team cashes it — a 3-bar DHC kill.', '', 2, True),
]

# ============================================================ CYCLOPS combos (reused/curated)
COMBOS['cyclops'] = [
 C('bnb', 'Bread &amp; butter', [G('LP','LK','HK'), TAG('XX'), SP('Cyclone Kick','QCB','K')],
   'Magic series into Cyclone Kick — easy, safe, knocks down.', '', 1, True),
 C('bnb', 'Sweep knockdown', [G('LP','LK','HK'), TAG('XX'), SP('Optic Sweep','F-DF-D','P')],
   'Sweep ender lays them flat and keeps them OTG-able for a beam super.', '', 1),
 C('bnb', 'Low BnB', [GC('LK','HK'), TAG('XX'), SP('Cyclone Kick','QCB','K')],
   'Two lows into the kick — opens crouch-blockers.', '', 1),
 C('bnb', 'Jab anti-air', [G('LP'), TAG('XX'), SP('Gene Splice','DP','P')],
   'Tag a jumper, mash Gene Splice for extra hits.', '', 1),
 C('super', 'Chain into super', [G('LP','LK','HK'), TAG('XX'), SP('Mega Optic Blast','QCF','PP')],
   'The BnB into his screen-filling beam super.', '', 1, True),
 C('super', 'Low OTG super', [GC('LK','HK'), TAG('XX'), SP('Mega Optic Blast','QCF','PP'), TAG('OTG')],
   'cr.HK knocks down and the beam OTGs them on the floor.', '', 2),
 C('cancel', 'Cyclone → super', [G('LP','LK','HK'), TAG('XX'), SP('Cyclone Kick','QCB','K'),
   TAG('XX'), SP('Mega Optic Blast','QCF','PP')],
   'Cancel the Cyclone Kick into the beam — time it as the kick connects.', '', 2, True),
 C('cancel', 'Sweep OTG → super', [G('LP','LK','HK'), PRE('OTG'), SP('Optic Sweep','F-DF-D','P'),
   PRE('XX'), SP('Mega Optic Blast','QCF','PP')],
   'Sweep low, OTG the beam super.', '', 2),
 C('cancel', 'Beam → uppercut link', [GC('LK'), G('HK'), TAG('2-hit · XX'), SP('Optic Blast','QCF','HP'),
   TAG('XX'), SP('Gene Splice','DP','P')],
   'His coolest link — the HP beam recovers fast enough to dragon-punch after it.', '', 3),
 C('air', 'Aerial Rave', [G('LP','LP'), DB('DF','HP'), TAG('launch'), PRE('sj'),
   G('LP','LK','LP','LK','HK','HK')],
   'His long air string; the double-HK ender uses his double-kick.', '', 2, True),
 C('corner', 'Running Tackle → beam → DP', [SP('Running Tackle','[B]F','K'), GC('LK'), TAG('OTG'),
   G('HK'), TAG('2-hit · XX'), SP('Optic Blast','QCF','HP'), TAG('XX'), SP('Gene Splice','DP','P')],
   'Unblockable tackle into the beam→uppercut link.', '', 3),
 C('team', 'The DHC ender', [PRE('any super'), PRE('DHC'), SP('Mega Optic Blast','QCF','PP')],
   'Mega Optic Blast is the team’s mid-anchor closer; it also DHCs forward into Storm.', '', 1, True),
]

# ============================================================ STORM combos
COMBOS['storm'] = [
 C('bnb', 'Ground confirm', [GC('LP','LK'), GC('HP'), TAG('XX'),
   SP('Lightning Attack','HP+LK · hold dir',''), TAG('fwd · XX'), SP('Lightning Storm','HCF','PP')],
   'Crouch chain, cancel into a forward Lightning Attack, then the super.', '', 2, True),
 C('bnb', '(corner) ground confirm', [GC('LK'), G('HP'), G('HK'), TAG('XX'),
   SP('Lightning Attack','HP+LK · hold dir',''), TAG('fwd · XX'), SP('Lightning Storm','HCF','PP')],
   '~18 hits and they can’t roll once you’re in. Corner only.', '', 2),
 C('air', 'Aerial Rave (basic)', [GC('LK'), G('HK'), TAG('launch'), PRE('sj'),
   G('LP','LK','HP','HK'), G('HP')],
   'The 7-hit rave most of the cast shares — but Storm does much better (see below).', '', 1),
 C('air', '★ Air rave → Lightning Storm', [GC('LK'), G('HK'), TAG('launch'), PRE('sj'),
   G('LP','LK','HP','HK'), TAG('XX'), SP('Lightning Attack','HP+LK · hold dir',''),
   TAG('up-fwd · XX'), SP('Lightning Storm','HCF','PP')],
   'The essence of Storm — 40–70%. Learn this and the many ways to confirm into it.', '', 2, True),
 C('air', 'Meter-build rave', [GC('LK'), G('HK'), TAG('launch'), PRE('sj'), G('LP','LK','HP','HK'),
   PRE('air-dash df'), DB('F','HP'), TAG('air throw')],
   'No meter spent — the air throw banks ~3/4 of a bar. She’s the team’s battery.', '', 2),
 C('super', 'Typhoon → Hail Storm', [SP('Vertical Typhoon','HCB','K'), TAG('pause'),
   SP('Hail Storm','QCB','PP')],
   'About the only way to combo into Hail Storm on point — mostly a turtle-buster.', '', 2),
 C('corner', 'Tri-jump infinite (advanced)', [PRE('tri-jump df'), G('LK'), G('HK'), PRE('land'),
   PRE('repeat…')],
   'Her real payoff once you can tri-jump: df tri-jump, LK, HK, land, repeat. Hard but defining.', '', 3),
 C('team', '★ Hail Storm DHC anchor', [PRE('partner super'), PRE('DHC'), SP('Hail Storm','QCB','PP')],
   'Hail Storm has NO recovery — the safest DHC in the game. This is why Storm anchors the team.', '', 1, True),
 C('team', 'Lightning Storm DHC', [G('LP','LK','HP','HK'), TAG('XX'), SP('Lightning Attack','HP+LK · hold dir',''),
   TAG('XX'), SP('Lightning Storm','HCF','PP'), PRE('DHC'), TAG('partner super')],
   'Lightning Storm also DHCs cleanly (it stays in hyper-space through the spin).', '', 2),
]

# ============================================================ movelists
MOVES = {
 'felicia': [
   ('Special moves', [
     ('Rolling Buckler', 'QCF+P; → Neko Punch (P) / Rising Slash (HP) / Sliding Kick (K)', [M('QCF','P')]),
     ('Sand Splash', 'QCF+K; ~¾-screen ground projectile, OTGs', [M('QCF','K')]),
     ('Delta Kick', 'F,D,DF+K; air OK; best AC finisher + OTG setup', [SQ('F-D-DF','K')]),
     ('Neko Spike', 'F,D,DF+P; short range, jab version cancels', [SQ('F-D-DF','P')]),
     ('Hell Cat', 'close HCB+K; command throw', [M('HCB','K')]),
   ]),
   ('Hypers', [
     ('Dancing Flash', 'QCF+PP; 11-hit auto-combo, easy to land', [M('QCF','PP')]),
     ('Hyper Sand Splash', 'QCF+KK; full-screen, mistake punisher', [M('QCF','KK')]),
     ('Please Help Me!', 'QCB+KK; mash for hits; corner OTG monster', [M('QCB','KK')]),
   ]),
   ('Normals & throws', [
     ('Launcher', 'HK or DF+HK', [G('HK'), TAG('or'), DB('DF','HK')]),
     ('B+HK', '2-hit handstand kick; links to supers', [DB('B','HK')]),
     ('Throws', 'close f/b + HP (mash) or HK', [DB('F','HP'), TAG('/'), DB('F','HK')]),
     ('Assist (α) Delta Kick', 'crossup / knockdown — her best', [G('A1')]),
   ]),
 ],
 'cyclops': [
   ('Special moves', [
     ('Optic Blast', 'QCF+P; air OK; HP angles up', [M('QCF','P')]),
     ('Gene Splice', 'DP+P; anti-air; mash', [M('DP','P')]),
     ('Cyclone Kick', 'QCB+K; combo ender', [M('QCB','K')]),
     ('Optic Sweep', 'F-DF-D+P; OTG', [SQ('F-DF-D','P')]),
     ('Running Tackle', '[B]F+K; unblockable', [DB('[B]F','K')]),
   ]),
   ('Hypers', [
     ('Mega Optic Blast', 'QCF+PP; the DHC ender', [M('QCF','PP')]),
     ('Super Optic Blast', 'QCF+KK; aimable', [M('QCF','KK')]),
   ]),
   ('Normals & throws', [
     ('Launcher', 'DF+HP or DF+HK', [DB('DF','HP'), TAG('or'), DB('DF','HK')]),
     ('Assist (β) Gene Splice', 'elite anti-air — the team glue', [G('A1')]),
   ]),
 ],
 'storm': [
   ('Special moves', [
     ('Horizontal Typhoon', 'QCF+K; air OK; uncancellable projectile', [M('QCF','K')]),
     ('Vertical Typhoon', 'HCB+K; runaway / Hail Storm setup', [M('HCB','K')]),
     ('Lightning Attack', 'HP+LK (hold dir); air-dash attack, ×3', [raw('<span class="sp" title="HP+LK, hold a direction">Lightning Attack</span>')]),
     ('Flight', 'QCB+KK; ground or air', [M('QCB','KK')]),
   ]),
   ('Hypers', [
     ('Lightning Storm', 'HCF+PP; air OK; the combo super', [M('HCF','PP')]),
     ('Hail Storm', 'QCB+PP; the safest DHC in the game', [M('QCB','PP')]),
   ]),
   ('Normals & throws', [
     ('Launcher', 'HK', [G('HK')]),
     ('Movement', '8-way air-dash · tri-jump · float (hold up)', [raw('<span class="ann">air-dash / tri-jump</span>')]),
     ('Assist (α) Whirlwind', 'horizontal Typhoon projectile', [G('A1')]),
   ]),
 ],
}

# one-screen "special moves" card per character (specials + hypers + launcher + assist)
ONESCREEN = {
 'felicia': [
   ('Rolling Buckler', '→ Slash/Slide', [M('QCF','P')]),
   ('Sand Splash', 'OTG projectile', [M('QCF','K')]),
   ('Delta Kick', 'air OK', [SQ('F-D-DF','K')]),
   ('Neko Spike', '', [SQ('F-D-DF','P')]),
   ('Hell Cat', 'cmd throw', [M('HCB','K')]),
   ('Launcher', '', [G('HK'), TAG('/'), DB('DF','HK')]),
   ('B+HK', '→ super', [DB('B','HK')]),
   ('SUPER · Dancing Flash', '', [M('QCF','PP')]),
   ('SUPER · Hyper Sand Splash', '', [M('QCF','KK')]),
   ('SUPER · Please Help Me!', 'mash', [M('QCB','KK')]),
   ('Assist (α) Delta Kick', '', [G('A1')]),
 ],
 'cyclops': [
   ('Optic Blast', 'air OK', [M('QCF','P')]),
   ('Gene Splice', 'anti-air', [M('DP','P')]),
   ('Cyclone Kick', '', [M('QCB','K')]),
   ('Optic Sweep', 'OTG', [SQ('F-DF-D','P')]),
   ('Running Tackle', 'unblockable', [SQ('[B]F','K')]),
   ('Launcher', '', [DB('DF','HP'), TAG('/'), DB('DF','HK')]),
   ('SUPER · Mega Optic Blast', 'DHC ender', [M('QCF','PP')]),
   ('SUPER · Super Optic Blast', 'aimable', [M('QCF','KK')]),
   ('Assist (β) Gene Splice', 'elite AAA', [G('A1')]),
 ],
 'storm': [
   ('Horizontal Typhoon', 'projectile', [M('QCF','K')]),
   ('Vertical Typhoon', 'runaway', [M('HCB','K')]),
   ('Lightning Attack', '×3, hold dir', [raw('<span class="sp" title="HP+LK, hold a direction">HP+LK</span>')]),
   ('Flight', '', [M('QCB','KK')]),
   ('Launcher', '', [G('HK')]),
   ('SUPER · Lightning Storm', 'combo super', [M('HCF','PP')]),
   ('SUPER · Hail Storm', 'safest DHC', [M('QCB','PP')]),
   ('Assist (α) Whirlwind', 'projectile', [G('A1')]),
 ],
}
