# -*- coding: utf-8 -*-
"""KOF XI character data for build_kof.py. Combos use the build_kof mini-DSL
(parsed at build time). B. Jenet's combo list + Athena's matchups are imported
from auto-generated files."""
from gen import M, MA, DB, SQ, G
from bjenet_combos import _load as _bj_load
from athena_matchups import ATHENA_MATCHUPS

def raw(h): return ('raw', h)
def C(grp, name, s, hits='', diff=1, core=False):
    return dict(grp=grp, name=name, s=s, hits=hits, diff=diff, core=core)

CHARS = {}

# ============================================================ TERRY
CHARS['terry'] = {
 'key': 'terry', 'name': 'Terry Bogard', 'short': 'Terry', 'role': 'All-round rushdown',
 'ca': '#ff8a4c', 'pfx': 'T',
 'intro': 'Terry Bogard — the Hungry Wolf and KOF’s definitive all-rounder. Strong pokes, a genuine '
          'anti-air in Power Dunk, and the iconic Buster Wolf / Power Geyser supers. This guide covers his '
          'KOF XI moves, every combo from the source FAQ, and how to use them.',
 'pros': ['Textbook all-rounder — strong at every range.',
          'A real anti-air / reversal in <b>Power Dunk</b> (the buffed NGBC version, like a shoto DP).',
          'Excellent zoning normals — cr.HP, cr.HK and st.HP.',
          '<b>Buster Wolf</b> is a top hop/jump-stopping super (mostly invincible).',
          'Flexible: pokes, pressure and keep-away all work.'],
 'cons': ['Buster Wolf does <b>pathetic damage</b> when comboed — use Power Geyser for damage.',
          'HK versions of Crack Shoot / Burning Knuckle are risky or useless.',
          'Power Stream (LDM) has a small hitbox + heavy scaling — not his best super.',
          'Power Dunk is unsafe on block.'],
 'specials': {
   'burning': ('Burning Knuckle', 'QCB', 'A', False),
   'powercharge': ('Power Charge', 'HCF', 'B', False),
   'crack': ('Crack Shoot', 'QCB', 'B', False),
   'dunk': ('Power Dunk', 'F-D-DF', 'B', False),
   'rising': ('Rising Upper', 'DF', 'C', False),
   'powerwave': ('Power Wave', 'QCF', 'A', False),
   'combo': ('Combination Blow', '(close C)', 'E', False),
   'buster': ('Buster Wolf', 'QCFx2', 'D', False),
   'geyser': ('Power Geyser', 'QCB-DB-F', 'A', False),
   'stream': ('Power Stream', 'QCB-HCF', 'E', False),
 },
 'combos': [
   C('bnb', 'Burning Knuckle', 'cB > cA > @rising > @burning.A', '4h', 1, True),
   C('bnb', 'Burning Knuckle (punish)', 'jD > sD > @burning.A', '4h', 1),
   C('bnb', 'Power Charge levels', 'jD > cB > cA > @powercharge.B > (Lv2) > (Lv3)', '', 2),
   C('bnb', 'Power Charge (punish)', 'jD > sD > @powercharge.B > (Lv2) > (Lv3)', '', 2),
   C('corner', 'Power Dunk juggle', 'jD > sC > @dunk.B > (Break) > @powercharge.B > @dunk.B', '', 3),
   C('super', 'Buster Wolf', 'cB > cA > @rising > @buster', '', 1, True),
   C('super', 'Power Geyser', 'cB > cA > @rising > @geyser', '', 1),
   C('super', 'Buster Wolf (punish)', 'jD > sD > @buster', '', 1),
   C('super', 'Power Geyser (punish)', 'jD > sD > @geyser.A', '', 1),
   C('super', 'Combination → Buster', 'jD > sC > @combo > @buster', '', 2),
   C('chain', 'Light chain → Buster', 'jD > cB > cB > sB > @buster', '', 2),
   C('dc', 'Power Charge SC → Buster', 'jD > sD > @powercharge.B > (Lv2 SC) > @buster', '', 3),
   C('dc', 'Power Charge SC → Buster (cr.)', 'jD > cB > cA > @powercharge.B > (Lv2 SC) > @buster', '', 3),
 ],
 'movelist': [
   ('Command moves', [
     ('Rising Upper', 'combos from lights; combo verifier', [DB('DF', 'C')]),
     ('Combination Blow', 'close C → E; link Buster Wolf', [G('C'), raw('<span class="ann">→</span>'), G('E')]),
   ]),
   ('Special moves', [
     ('Power Wave', 'poke / fireball — LP version is best', [M('QCF', 'P')]),
     ('Burning Knuckle', 'combo ender; LP version combos', [M('QCB', 'P')]),
     ('Power Charge', 'combo-only; Lv2/3 = f,f+K', [M('HCF', 'K')]),
     ('Crack Shoot', 'overhead; mix-up off cr. lights', [M('QCB', 'K')]),
     ('Power Dunk', 'anti-air / DP; Break = A+B', [SQ('F-D-DF', 'P')]),
   ]),
   ('Supers (DM)', [
     ('Buster Wolf', 'Dream-Cancellable; hop-stopper', [M('QCFx2', 'K')]),
     ('Power Geyser', 'anti-air; scales in combos', [SQ('QCB-DB-F', 'P')]),
   ]),
   ('Leader DM', [
     ('Power Stream', 'corner combos; small hitbox', [SQ('QCB-HCF', 'E')]),
   ]),
 ],
 'onescreen': [
   ('Rising Upper', '', [DB('DF', 'C')]),
   ('Combination Blow', 'close', [G('C'), raw('<span class="ann">→</span>'), G('E')]),
   ('Power Wave', '', [M('QCF', 'P')]),
   ('Burning Knuckle', '', [M('QCB', 'P')]),
   ('Power Charge', 'Lv2/3 f,f+K', [M('HCF', 'K')]),
   ('Crack Shoot', 'overhead', [M('QCB', 'K')]),
   ('Power Dunk', 'Break A+B', [SQ('F-D-DF', 'P')]),
   ('SUPER · Buster Wolf', 'DC', [M('QCFx2', 'K')]),
   ('SUPER · Power Geyser', '', [SQ('QCB-DB-F', 'P')]),
   ('LEADER · Power Stream', '', [SQ('QCB-HCF', 'E')]),
   ('Throw', 'close', [DB('F', 'C'), raw('<span class="ann">/</span>'), DB('B', 'D')]),
 ],
 'strategy': [
   ('Neutral & zoning', [
     ('Power Wave', 'Throw the <b>LP</b> version from max range as a poke and a wall to advance behind.', ''),
     ('Zoning normals', 'cr.HP, cr.HK and st.HP all hit far and cancel — your spacing tools.', ''),
     ('No-meter anti-air', '<b>Power Dunk</b> (LK) is your DP without bar; with bar, <b>Power Geyser</b>.', ''),
     ('Stop the hop', 'With a stock, <b>Buster Wolf</b> answers hops and jump-ins (mostly invincible).', ''),
   ]),
   ('Combos & cancels', [
     ('Verify with Rising Upper', 'cr.LK, cr.LP, <b>Rising Upper</b> hit-confirms into Burning Knuckle or a super.', ''),
     ('Power Charge = the light-confirm', 'His only special that combos from lights — and Lv2 super-cancels into Buster.', ''),
     ('Damage route', 'End with <b>Power Geyser</b> (not Buster Wolf) for damage; or Power Dunk → Break → juggle.', ''),
   ]),
   ('Mix-ups', [
     ('Overhead', '<b>Crack Shoot</b> (LK) off a blocked cr.LP/LK is a fast overhead.', ''),
     ('After a blocked low', 'Mix dash-throw, Crack Shoot, or a delayed <b>Buster Wolf</b> counter.', ''),
   ]),
 ],
 'matchups': None,
}

# ============================================================ ATHENA
CHARS['athena'] = {
 'key': 'athena', 'name': 'Athena Asamiya', 'short': 'Athena', 'role': 'Zoner / mix-up',
 'ca': '#c98bff', 'pfx': 'AT',
 'intro': 'Athena Asamiya — psychic idol and one of KOF’s premier zoners. A fast Psycho Ball, an '
          'invincible anti-air DM, crossups, a command throw, and a Leader super that does ~60%. This guide '
          'covers her KOF XI moves, every combo from the source FAQ, her game plan, and her full matchup chart.',
 'pros': ['Elite zoning — <b>Psycho Ball</b> is fast with quick recovery.',
          'A near-guaranteed anti-air DM in <b>Shining Crystal Bit</b> (invincible start-up).',
          'A ~60% <b>Leader super</b> — Super Phoenix Infinity.',
          'Fast and agile, with strong air mobility and crossups (Phoenix Bomb / Arrow).',
          'Has a command throw <i>and</i> an air throw, and can <b>reflect</b> projectiles.'],
 'cons': ['<b>Psycho Sword</b> (her DP) is slow / low-priority — a poor ground anti-air or wake-up.',
          'Many of her combos are <b>corner-only</b>.',
          'Lost cancellability on some normals vs older KOF (e.g. cr.D).',
          'Struggles against strong ground-priority rushdown (Kim especially).'],
 'specials': {
   'ball': ('Psycho Ball', 'QCB', 'A', False),
   'teleport': ('Psychic Teleport', 'QCF', 'B', False),
   'psword': ('Psycho Sword', 'DP', 'A', False),
   'reflector': ('Psycho Reflector', 'QCB', 'B', False),
   'phoenixarrow': ('Phoenix Arrow', 'QCB', 'B', True),
   'phoenixbomb': ('Phoenix Bomb', 'D', 'B', True),
   'linkkick': ('Link Kick', 'F', 'B', False),
   'superthrow': ('Super Psychic Throw', 'HCF', 'A', False),
   'scb': ('Shining Crystal Bit', 'HCBx2', 'A', False),
   'crystalshoot': ('Crystal Shoot', 'QCB', 'A', False),
   'fang': ('Phoenix Fang Arrow', 'QCBx2', 'B', True),
   'infinity': ('Super Phoenix Infinity', 'QCFx2', 'E', True),
 },
 'combos': [
   C('bnb', 'Air pop-up', '@linkkick > jC', '', 1),
   C('bnb', 'Psycho Sword', 'jD > sC > @psword', '', 1, True),
   C('bnb', 'Psycho Ball ender', 'jD > sC > @ball.C', '', 1, True),
   C('bnb', 'Bomb reset', '@phoenixbomb > sA > @psword', '', 2),
   C('corner', 'Sword (corner)', 'sC > @linkkick > @psword.C > (C)', '', 2),
   C('corner', 'Crystal Bit', 'jD > sC > @linkkick > @scb > (C)', '', 2),
   C('corner', 'Fang Arrow', 'jD > sC > @linkkick > @phoenixarrow > @fang > (C)', '', 3),
   C('corner', 'Sword → Crystal Bit', 'jD > sC > @linkkick > @psword > @scb > (C)', '', 3),
   C('super', 'Air → LDM', 'jA > @phoenixarrow > @fang > @infinity', '', 3, True),
   C('team', 'All-girls (· Mai)', 'jC > sA > sA > sA > (▶ Many Many Torpedo) > (QS Mai) > '
     '(Mai: jD, sC, f+B, qcb+C) > (QS Athena) > jD > sC > @linkkick > @psword > @infinity', '', 3),
   C('team', 'with Benimaru', '(Malin: jD, sC, f+B, hcf+B) > (QS Benimaru) > '
     '(Benimaru: jD, sC, df+B, qcb+D) > (QS Athena) > jD > sC > @infinity', '', 3),
   C('team', 'with Kensou', '(Kula: jD, sC, f+A) > (QS Kensou) > (Kensou: cC, qcf~hcb+B) > '
     '(QS Athena) > @scb > @infinity > (C)', '', 3),
 ],
 'movelist': [
   ('Command moves', [
     ('Link Kick', 'FD+B; pops up, cancellable', [DB('F', 'B')]),
     ('Phoenix Bomb', 'air down+B; overhead / crossup', [raw('<span class="air">air</span>'), DB('D', 'B')]),
     ('Triangular Jump', 'corner: jump off the wall', [raw('<span class="ann">corner wall-jump</span>')]),
   ]),
   ('Special moves', [
     ('Psycho Ball', 'QCB+A/C; fast projectile', [M('QCB', 'P')]),
     ('Psychic Teleport', 'QCF+B/D; air OK, SC in air', [M('QCF', 'K')]),
     ('Psycho Sword', 'DP+A/C; air OK', [M('DP', 'P')]),
     ('Psycho Reflector', 'QCB+B; reflects projectiles', [M('QCB', 'B')]),
     ('Phoenix Arrow', 'air QCB+B/D; crossup', [MA('QCB', 'K')]),
     ('Super Psychic Throw', 'close HCF+A/C', [M('HCF', 'P')]),
   ]),
   ('Supers (DM)', [
     ('Shining Crystal Bit', 'HCB,HCB+A/C; air OK; invincible', [M('HCBx2', 'P')]),
     ('Crystal Shoot', 'during Crystal Bit: QCB+A/C', [M('QCB', 'P')]),
     ('Phoenix Fang Arrow', 'air QCB,QCB+B/D', [MA('QCBx2', 'K')]),
   ]),
   ('Leader DM', [
     ('Super Phoenix Infinity', 'QCF,QCF+E; air OK; ~60%', [M('QCFx2', 'E')]),
   ]),
   ('Throws', [
     ('Psychic Throw', 'close f+C/D', [DB('F', 'C')]),
     ('Psychic Shoot', 'air, close', [raw('<span class="ann">air throw</span>')]),
   ]),
 ],
 'onescreen': [
   ('Link Kick', 'pops up', [DB('F', 'B')]),
   ('Phoenix Bomb', 'air overhead', [raw('<span class="air">air</span>'), DB('D', 'B')]),
   ('Psycho Ball', '', [M('QCB', 'P')]),
   ('Psychic Teleport', 'air OK', [M('QCF', 'K')]),
   ('Psycho Sword', 'air OK', [M('DP', 'P')]),
   ('Psycho Reflector', 'reflect', [M('QCB', 'B')]),
   ('Phoenix Arrow', 'air', [MA('QCB', 'K')]),
   ('Super Psychic Throw', 'close', [M('HCF', 'P')]),
   ('SUPER · Shining Crystal Bit', 'invincible', [M('HCBx2', 'P')]),
   ('SUPER · Phoenix Fang Arrow', 'air', [MA('QCBx2', 'K')]),
   ('LEADER · Super Phoenix Infinity', '~60%', [M('QCFx2', 'E')]),
   ('Throw', 'close', [DB('F', 'C')]),
 ],
 'strategy': [
   ('Neutral & zoning', [
     ('Keep moving + fireball', 'Great agility — never sit still; abuse <b>Psycho Ball</b> from range.', ''),
     ('Anti-air', 'When they jump, <b>Shining Crystal Bit</b> or the LDM — both work even as you rise.', ''),
     ('The fireball trap', 'Mid-screen Psycho Ball loop — if they <b>roll</b>: Link Kick / cr.C; if they '
      '<b>jump</b>: Crystal Bit / LDM; if <b>close</b>: st.C / cr.A.', ''),
   ]),
   ('Mix-ups & escapes', [
     ('Teleport feint', 'Cancel cr.C into <b>Psychic Teleport</b> to cross up / confuse.', ''),
     ('Retreat', '<b>back, back</b> then air <b>Phoenix Bomb</b> to regain ground fast.', ''),
     ('Corner escape', 'Use the <b>triangle jump</b> to leave the corner — don’t rely on Psycho Sword.', ''),
   ]),
 ],
 'matchups': ATHENA_MATCHUPS,
}

# ============================================================ B. JENET
CHARS['bjenet'] = {
 'key': 'bjenet', 'name': 'Bonne Jenet', 'short': 'B. Jenet', 'role': 'Speed rushdown',
 'ca': '#ffcf5a', 'pfx': 'BJ',
 'intro': 'Bonne Jenet — captain of the Lilien Knights and one of the fastest rushdown characters in KOF '
          'XI. Relentless pressure with <b>The Hind</b> → Harrier Bee, a deep combo tree, and a counter '
          'Leader super. This guide covers her moves, <b>every</b> combo from the source FAQ, and her game.',
 'pros': ['One of the <b>fastest</b> characters — pure rushdown.',
          '<b>The Hind → Harrier Bee</b> gives safe, frame-positive pressure that also builds meter fast.',
          'A huge, flexible combo tree from almost any normal.',
          'Strong pokes (far st.A / st.E) and a fast, spammable blowback (E).',
          'A reversal/counter <b>LDM</b> (An Oi Mademoiselle) and an air throw.'],
 'cons': ['Defence is on the weaker side — she wants to be the aggressor.',
          'Combo damage leans on meter (Dream-Cancel routes) to really hurt.',
          'Stubby on some normals; needs to get in to do work.',
          'Many of her biggest combos are corner-only.'],
 'specials': {
   'buffrass': ('Buffrass', 'QCF', 'A', False),
   'ivan': ('Crazy Ivan', 'QCB', 'A', False),
   'gulf': ('Gulf Tomahawk', 'QCB', 'B', False),
   'hind': ('The Hind', 'QCF', 'D', False),
   'harrier': ('Harrier Bee', 'D', 'D', True),
   'rolling': ('Rolling Thunder', 'DF', 'D', False),
   'torpedo': ('Many Many Torpedo', 'QCFx2', 'A', False),
   'aurora': ('Aurora', 'QCFx2', 'B', False),
   'anoi': ('An Oi Mademoiselle', 'QCBx2', 'E', False),
 },
 'combos': _bj_load(C) + [
   C('team', 'Jenet → Oswald (68!)', 'shC > sA > sC > @hind.D (2) > @harrier.D > @torpedo > (QS Oswald) > '
     '(Oswald: df+A, qcb+B, sA/D, charge b,f,b,f+E)', '68h (C)', 3),
   C('team', 'Jenet → Kula', 'shC > sA > sC > @hind.D (2) > @harrier.D > @torpedo > (QS Kula) > '
     '(Kula: qcb+B, f+B, sA, qcb,qcb+E)', '32h (C)', 3),
   C('team', 'Jenet → K’', 'shC > sA > sC > @hind.D (2) > @harrier.D > @torpedo > (QS K’) > '
     '(K’: air qcb+B, u, qcb+B ×3)', '17h (C)', 3),
 ],
 'movelist': [
   ('Command moves', [
     ('Combination A', 'close A×3 or A,C — cancel into specials', [G('A'), G('A'), G('A')]),
     ('Combination C', 'far C, C', [raw('<span class="ann">far</span>'), G('C'), G('C')]),
     ('Rolling Thunder', 'df+D; clean-hit dive (T.O.P. attack)', [DB('DF', 'D')]),
   ]),
   ('Special moves', [
     ('Buffrass', 'QCF+A/C; tornado projectile, chip', [M('QCF', 'P')]),
     ('Crazy Ivan', 'QCB+A/C; knockdown, safe on block', [M('QCB', 'P')]),
     ('Gulf Tomahawk', 'QCB+B/D; overhead crescent', [M('QCB', 'K')]),
     ('The Hind', 'QCF+B/D; pressure into Harrier Bee', [M('QCF', 'K')]),
     ('Harrier Bee', 'air d+K (×3–5); dive after The Hind', [MA('D', 'K')]),
   ]),
   ('Supers (DM)', [
     ('Many Many Torpedo', 'QCF,QCF+A/C; Dream-Cancellable', [M('QCFx2', 'P')]),
     ('Aurora', 'QCF,QCF+B/D; anti-air / corner ender', [M('QCFx2', 'K')]),
   ]),
   ('Leader DM', [
     ('An Oi Mademoiselle', 'QCB,QCB+E; counter / reversal, ~60%', [M('QCBx2', 'E')]),
   ]),
   ('Throws', [
     ('Bye-Bye Boo', 'close f/b+C/D', [DB('F', 'C')]),
     ('Falling Crush', 'air uf/ub+C', [raw('<span class="air">air</span>'), DB('UF', 'C')]),
   ]),
 ],
 'onescreen': [
   ('Rolling Thunder', 'df+D', [DB('DF', 'D')]),
   ('Buffrass', 'projectile', [M('QCF', 'P')]),
   ('Crazy Ivan', 'safe', [M('QCB', 'P')]),
   ('Gulf Tomahawk', 'overhead', [M('QCB', 'K')]),
   ('The Hind', '→ Harrier', [M('QCF', 'K')]),
   ('Harrier Bee', 'air dive', [MA('D', 'K')]),
   ('SUPER · Many Many Torpedo', 'DC', [M('QCFx2', 'P')]),
   ('SUPER · Aurora', 'anti-air', [M('QCFx2', 'K')]),
   ('LEADER · An Oi Mademoiselle', 'counter', [M('QCBx2', 'E')]),
   ('Throw', 'close', [DB('F', 'C')]),
 ],
 'strategy': [
   ('Offence — rushdown', [
     ('The Hind → Harrier', 'Your core pressure: <b>The Hind (D)</b> into <b>Harrier Bee (d+D)</b> is '
      'safe, frame-positive on landing, and builds meter. Branch into anything after.', ''),
     ('Combination A', '<b>st.A, st.C</b> is your bread-and-butter chain — link it into The Hind and keep going.', ''),
     ('Short jumps', 'sh.C is her main jump attack; sh.D up close / in the corner stresses huge pressure.', ''),
   ]),
   ('Defence & anti-air', [
     ('Spam the blowback', 'Far <b>st.E</b> is so good you can poke with it all day; cancel it into Gulf '
      'Tomahawk if they jump.', ''),
     ('Anti-air', '<b>Gulf Tomahawk</b> and <b>Aurora</b> both swat jump-ins; st.D / st.E stuff hops.', ''),
     ('Get out', 'qcf+D(2), d+D escapes a lot; Guard-Cancel blowback (E while blocking) resets space; '
      'Saving Shift if you’re really stuck.', ''),
   ]),
   ('Meter & mix-ups', [
     ('Build stocks', 'The Hind → Harrier and back-dash Harrier (b,b, d+D) build power fast.', ''),
     ('Tick throws', 'cr.A/B, walk up, <b>Bye-Bye Boo</b> — or whiff a jump A next to them for a free throw.', ''),
     ('Corner mix after Hind', 'After qcf+D(2), d+D in the corner, st.A/C juggle then cancel into anything — '
      'or Quick-Shift for an unblockable set-up.', ''),
   ]),
 ],
 'matchups': None,
}
