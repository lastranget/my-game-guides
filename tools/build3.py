# -*- coding: utf-8 -*-
"""Assemble mvc2-cammy-bbhood-cyclops-advanced.html — strategy/matchup companion."""
import os as _os
_HERE=_os.path.dirname(_os.path.abspath(__file__))
_REPO=_os.path.dirname(_HERE)
from gen import (keycap, mot, dirp, render_action, render_combo,
                 G, M, MA, DB, CH, SQ, DIR, SP, PRE, TAG)
from refs import references_section

OUT = _os.path.join(_REPO,'guides','mvc2','mvc2-cammy-bbhood-cyclops-advanced.html')
CA = {'cammy': '#5fd36b', 'bbhood': '#ff8fa3', 'cyclops': '#7cc0ff'}

# inline glyph helpers (return HTML for use in prose)
def kb(t):              return keycap(t)
def mv(m, b, air=False): return render_action(MA(m, b) if air else M(m, b))
def spn(n, m, b, air=False): return render_action(SP(n, m, b, air))
def dbtn(d, b):         return render_action(DB(d, b))
def chg(d, b):          return render_action(CH(d, b))
def sq(m, b):           return render_action(SQ(m, b))
def grp(*b):            return render_action(G(*b))

def sysrow(nm, dsc, inn=''):
    intop = f'<span class="in">{inn}</span>' if inn else ''
    return (f'<div class="sysrow"><div class="top"><span class="nm">{nm}</span>{intop}</div>'
            f'<div class="dsc">{dsc}</div></div>')

def charblock(char, title_role, inner):
    return (f'<div class="ccombo" style="--ca:{CA[char]}"><h3>{title_role}</h3>{inner}</div>')

# ============================================================ §1 strengths/weaknesses
SW = {
 'cammy': ('Cammy <span class="role">· Rushdown point</span>',
   ['<b>Fastest in the game</b> — top movement <i>and</i> attack speed.',
    'A <b>full-screen ground dash</b> — the best way to get in.',
    '<b>Tiny hitbox</b> (smaller than Jill) — many attacks whiff over her.',
    'Owns the air: elite priority, anti-airs, Aerial Raves and OTG loops.',
    'Vicious mix-ups, cross-ups and tick-throws.'],
   ['<b>Bad start-up / recovery</b> on every special and super.',
    'Almost <b>no chip damage</b>.',
    'Takes above-average damage, deals below-average — poor lasting power.',
    '<b>No projectile</b> — she loses a pure keep-away war.',
    'Mediocre assists &amp; a poor Variable Combination (BB Hood fixes it).']),
 'bbhood': ('BB Hood <span class="role">· Zoner / battery</span>',
   ['Elite keep-away: high / low / air missiles at many angles with <b>Guile-fast recovery</b>.',
    '<b>Cool Hunting</b> does huge damage <i>and</i> huge chip — and it combos.',
    'Builds meter fast — the team’s <b>battery</b>.',
    'Tiny and slippery; has a <b>double jump</b> and a crawl for movement tricks.'],
   ['<b>Almost no anti-air</b> of her own.',
    'One of the <b>worst launchers</b> in the game — air combos are minor.',
    'Stubby normals (very short range).',
    'Cool Hunting has long recovery — punishable if it whiffs.',
    'Leans hard on assists — weak when cornered with no meter.']),
 'cyclops': ('Cyclops <span class="role">· Assist anchor</span>',
   ['<b>Two of the best beam supers</b> in the game (Mega / Super Optic Blast) — great priority, '
    'huge block damage, usable in the air.',
    'High-priority ground chains and a strong beam keep-away.',
    'Great mid-air priority (rivals Spider-Man); a <b>double jump</b> for long air combos.',
    '<b>Gene Splice assist</b> = one of the best anti-airs in the game — the team’s glue.',
    'Balanced and durable — a great anchor.'],
   ['<b>No reliable on-point anti-air</b> (Gene Splice is punished on block; fierce beam unreliable; '
    's.HK has short vertical range).',
    'No truly safe reversal.',
    'Middling speed — wins neutral on reads, not raw rushdown.']),
}
def sec_sw():
    blocks = []
    for ch in ('cammy', 'bbhood', 'cyclops'):
        title, pros, cons = SW[ch]
        pl = ''.join(f'<li>{x}</li>' for x in pros)
        cl = ''.join(f'<li>{x}</li>' for x in cons)
        inner = (f'<div class="sw"><div><h4 class="pro">Strengths</h4><ul>{pl}</ul></div>'
                 f'<div><h4 class="con">Weaknesses</h4><ul>{cl}</ul></div></div>')
        blocks.append(charblock(ch, title, inner))
    return ('<section class="block" id="sw"><h2>Strengths &amp; weaknesses'
            '<a href="#toc" class="bt">contents ↑</a></h2>'
            '<p class="note2">Know what each character is <i>for</i> — it explains why the team is built '
            'point → battery → anchor, and which jobs to lean on.</p>' + ''.join(blocks) + '</section>')

# ============================================================ §2 assist reference
def arow(typ, desc, pick=False):
    badge = '<span class="pick">team pick</span>' if pick else ''
    return f'<div class="arow"><span class="atype">{typ}</span><span class="adesc">{desc}{badge}</span></div>'
def sec_assists():
    cam = charblock('cammy', 'Cammy', ''.join([
        arow('α Alpha', f'<b>Cannon Spike</b> ({mv("DP","K")}) — invincible anti-air; the team’s second '
             'get-off-me AAA.', pick=True),
        arow('β Beta', f'<b>Cannon Drill</b> ({mv("QCF","K")}) — fast horizontal ground coverage; for lockdown.'),
        arow('γ Gamma', f'<b>Axel Spin Knuckle</b> ({mv("QCF","P")}) — spinning punch; rarely chosen.'),
        '<div class="dsc" style="margin-top:5px">Variable Combination is <b>Spin Drive Smasher</b> '
        '(α/β) — weak on its own, but BB Hood’s bullets pin the foe so it actually connects.</div>']))
    bb = charblock('bbhood', 'BB Hood', ''.join([
        arow('α Alpha', f'<b>Smile &amp; Missile</b> ({chg("[B]F","P")}) — knockdown projectile; her '
             '<b>only worthwhile assist</b> — pins and zones for the point.', pick=True),
        arow('β / γ', 'Anti-air flame &amp; basket types exist but are rarely used — α is the clear pick.'),
        '<div class="dsc" style="margin-top:5px">Variable Combination is <b>Cool Hunting</b> — huge '
        'chip even when blocked.</div>']))
    cyc = charblock('cyclops', 'Cyclops', ''.join([
        arow('α Alpha', f'<b>Optic Blast</b> ({mv("QCF","P")}) — fast beam; beats fireballs (not beams); '
             'covers a partner who is weak at range.'),
        arow('β Beta', f'<b>Gene Splice</b> ({mv("DP","P")}) — elite anti-air; defensive get-off-me; '
             'great for escaping corner pressure; doubles as a decoy.', pick=True),
        arow('γ Gamma', f'<b>Cyclone Kick</b> ({mv("QCB","K")}) — poke / combo assist; least useful.'),
        '<div class="dsc" style="margin-top:5px">All three Variable Combination into <b>Mega Optic '
        'Blast</b> — the team’s closer.</div>']))
    return ('<section class="block" id="assists"><h2>Assist reference (α / β / γ)'
            '<a href="#toc" class="bt">contents ↑</a></h2>'
            '<p class="note2">The general guide gives the picks; here is <i>why</i>. The team runs '
            '<b>Cammy α · BB Hood α · Cyclops β</b> — two anti-airs plus a knockdown projectile cover the '
            'ground and the sky from every angle.</p>' + cam + bb + cyc + '</section>')

# ============================================================ §3 neutral & spacing
def sec_neutral():
    cam = charblock('cammy', 'Cammy <span class="role">· get in</span>', ''.join([
        sysrow('No projectile — you must approach',
               f'Use the full-screen <b>ground dash</b> and <b>dash-jump</b> to close, especially onto a '
               f'beamer recovering from a shot (Cable). There is no sitting back with Cammy.'),
        sysrow('Best pokes',
               f'Fast {kb("LP")}/{kb("LK")}; <b>standing {kb("HK")}</b> is a long, high-priority anti-air '
               f'that grants a <b>free Aerial Rave</b> on hit.'),
        sysrow('Anti-air menu',
               f'{spn("Cannon Spike","DP","K")} (invincible), standing {kb("HK")}, '
               f'{spn("Cannon Revenge","HCB","P")}, or just launch.'),
        sysrow('Slip under beams',
               f'{spn("Cannon Drill","QCF","K")} and {spn("Spin Drive Smasher","QCF","KK")} travel fast and '
               f'pass <b>under</b> many beams (Magneto’s EM Disruptor, Cable’s gunfire) and <b>over</b> '
               f'BB Hood’s low missile — great long-range punishes.'),
    ]))
    cyc = charblock('cyclops', 'Cyclops <span class="role">· beam control</span>', ''.join([
        sysrow('Beam game (with discipline)',
               f'Mix {spn("Optic Blast","QCF","LP")} (low/quick) and the angled {mv("QCF","HP")} version — '
               f'but <b>do not</b> throw them mindlessly; the recovery is punishable.'),
        sysrow('His anti-air problem',
               f'Standing {kb("HK")} is his safest AA but its range is short. He has <b>no great anti-air</b> '
               f'on point — this is why he sits in back behind the Gene Splice assist.'),
        sysrow('Punish from afar',
               f'Jump back and {spn("Super Optic Blast","QCF","KK")} to punish a called assist, a beam, or a '
               f'projectile. Cancel a <i>blocked</i> {spn("Gene Splice","DP","P")} into it to stay safe.'),
        sysrow('Up close',
               f'Mix high/low kicks, {spn("Cyclone Kick","QCB","K")}, the launcher, his double jump, and the '
               f'odd surprise {spn("Running Tackle","[B]F","K")}. {kb("HK")} dominates the air.'),
    ]))
    bb = charblock('bbhood', 'BB Hood <span class="role">· build the wall</span>', ''.join([
        sysrow('Two-height missile wall',
               f'Alternate {chg("[B]F","P")} (high missile) and {chg("[B]F","K")} (low missile), plus '
               f'{chg("[D]U","P")} (air) — they can’t crouch under <i>and</i> jump over. Walk in behind it.'),
        sysrow('Stay safe on fierce',
               f'Cancel any blocked or whiffed {kb("HP")} into a missile — its recovery is tiny, so you’re '
               f'never left open.'),
        sysrow('Her only anti-air',
               f'{spn("Cheer &amp; Fire","DP","P")} (flame, angles up). In the air, throw {mv("DP","K",air=True)} '
               f'flames to wall out approaches — but watch for counters.'),
        sysrow('Chip with the guns',
               f'After a called anti-air assist connects, {spn("Cool Hunting","QCF","PP")} for big chip even '
               f'if it doesn’t fully combo.'),
    ]))
    return ('<section class="block" id="neutral"><h2>Neutral game &amp; spacing'
            '<a href="#toc" class="bt">contents ↑</a></h2>'
            '<p class="note2">How to actually win the ground before any combo starts — the bridge between '
            'the movelist and a game plan.</p>' + cam + cyc + bb + '</section>')

# ============================================================ §4 defense
def sec_defense():
    rows = ''.join([
        sysrow('Advancing Guard (push-block)',
               'Shove the attacker away and cut block-stun — your #1 escape from pressure. Don’t spam it; '
               'sometimes it just resets them at a worse range for you.', f'{kb("PP")} <span class="ann">while blocking</span>'),
        sysrow('Variable Counter',
               'Tag a partner in with a counter-attack mid-blockstring to escape — costs one bar. Great for '
               'bailing Cyclops out of corner pressure.', f'{sq("B-DB-D","A1")} <span class="ann">blocking</span>'),
        sysrow('Reversals (wake-up)',
               f'Cammy’s {spn("Cannon Spike","DP","K")} is <b>invincible</b> — her best wake-up. Cyclops’ '
               f'{spn("Gene Splice","DP","P")} is fast but <b>punished on block</b> (cancel into '
               f'{spn("Super Optic Blast","QCF","KK")} to be safe). BB Hood has none — block and push out.'),
        sysrow('Air-guard — and its limit',
               'Hold <b>back in the air</b> to block air attacks, projectiles and supers. But you '
               '<b>cannot</b> air-block a grounded normal — so jumping is <i>not</i> a free escape; you’ll '
               'get launched.', f'{dirp("B")}<span class="ann">in air</span>'),
        sysrow('Tech roll',
               'Tap toward or away as you hit the ground from a knockdown to roll out and dodge an OTG.',
               f'{dirp("F")}<span class="ann">on landing</span>'),
        sysrow('KBA as a panic button',
               f'Cammy’s {spn("Killer Bee Assault","QCB","PP",air=True)} has invincible start-up — '
               f'<b>DHC into it</b> to save a partner from an incoming super (it has beaten Sentinel’s '
               f'rockets and even countered a Cool Hunting).'),
        sysrow('Counter the counter',
               f'End a <i>blocked</i> chain with {spn("Cannon Revenge","HCB","P")} now and then — it snuffs '
               f'their mashed poke. Against combo-sprites (Strider, Spider-Man, Wolverine), push-block their '
               f'string, then Cannon Revenge as they dash back in. Don’t repeat it — it’s readable.'),
    ])
    return ('<section class="block" id="defense"><h2>Defense &amp; escaping pressure'
            '<a href="#toc" class="bt">contents ↑</a></h2>'
            '<p class="note2">The moves are in the movelist; this is <i>when</i> to use them — how not to '
            'die.</p><div class="sys">' + rows + '</div></section>')

# ============================================================ §5 meter & DHC
def sec_meter():
    routes = ''.join([
        '<div class="cmb"><div class="cmb-h"><b>Team kill</b></div>' + render_combo(
            [SP('Cool Hunting', 'QCF', 'PP'), TAG('BB Hood'), PRE('DHC'),
             SP('Mega Optic Blast', 'QCF', 'PP'), TAG('Cyclops')]) + '</div>',
        '<div class="cmb"><div class="cmb-h"><b>Point cash-out</b></div>' + render_combo(
            [SP('Spin Drive Smasher', 'QCF', 'KK'), TAG('Cammy'), PRE('DHC'),
             SP('Cool Hunting', 'QCF', 'PP'), TAG('BB Hood'), PRE('DHC'),
             SP('Mega Optic Blast', 'QCF', 'PP'), TAG('Cyclops')]) + '</div>',
        '<div class="cmb"><div class="cmb-h"><b>Rescue (beat an incoming super)</b></div>' + render_combo(
            [PRE('partner blocked'), PRE('DHC'),
             SP('Killer Bee Assault', 'QCB', 'PP', air=True), TAG('Cammy · invincible start-up')]) + '</div>',
    ])
    rows = ''.join([
        sysrow('BB Hood is the battery',
               'Her missiles and Cool Hunting build bars fast. Bank them — for Cyclops’ kill, or to spend '
               'on her own monstrous chip.'),
        sysrow('When to spend',
               '<b>Solo super</b> to confirm a stray hit. <b>DHC</b> to kill, or to bring a fresh character '
               'in safely. <b>Snapback</b> (' + render_action(SP('Snapback', 'QCF', 'A1')) +
               ', 1 bar) to force out a scary point character or delete a low assist. <b>Save 2+</b> for a '
               'guaranteed DHC kill.'),
        sysrow('Fix Cammy’s bad Variable Combination',
               'On its own her VC whiffs. With BB Hood behind her, the bullets pin the foe in the corner so '
               'every hit of Spin Drive Smasher connects — a win-win even on block (Cool Hunting chip).'),
    ])
    return ('<section class="block" id="meter"><h2>Meter game &amp; DHC routes'
            '<a href="#toc" class="bt">contents ↑</a></h2>'
            '<p class="note2">This team banks meter on BB Hood and cashes it on Cyclops. Decide '
            '<i>when</i> to spend here; full combo routes live in the combo guide.</p>'
            '<div class="sys">' + rows + '</div>'
            '<h3>DHC routes</h3>' + routes + '</section>')

# ============================================================ §6 mind games & resets
def sec_mixups():
    rows = ''.join([
        sysrow('Tick-throw (Cammy)',
               f'A {kb("LP")} has great range/speed — tick with it, then Suplex ({dbtn("F","HP")}), then OTG '
               f'{dbtn("D","LK")}, {dbtn("D","HP")} into an Aerial Rave.'),
        sysrow('Cross-up + assist',
               'Dash-jump to the <b>far</b> side and call a close-range / dasher assist <i>before</i> you '
               'leave the ground. As you land behind them the assist hits — they can’t tell which way to '
               'block. Launch the opened guard.'),
        sysrow('Air Suplex side-switch (Cammy)',
               'Her air throw switches sides (so the wrong tech-roll direction whiffs) and lets you OTG '
               'afterward.'),
        sysrow('Instant super-jump escape (Cammy)',
               'If a launcher is <b>blocked</b>, tap up to instantly super-jump out of the punish — '
               'up-forward to cross to the other side (deadly if you also called an assist).'),
        sysrow('DHC confuser',
               f'Whiff or get {spn("Spin Drive Smasher","QCF","KK")} blocked on purpose, then DHC — the '
               f'follow-up super catches them repositioning to punish.'),
        sysrow('Crawl mix-up (BB Hood)',
               f'{spn("Stalking","D,D","KK")} crawls <b>under</b> a fireball or super and comes out the other '
               f'side — bait, then punish.'),
        sysrow('Pattern-breakers (Cyclops)',
               f'A random {spn("Running Tackle","[B]F","K")} (unblockable) or surprise {spn("Gene Splice","DP","P")} '
               f'cracks a turtle’s rhythm. Vs heavy blockers, BB Hood’s {spn("Hyper Apple For You","HCB","KK")} '
               f'grab super beats guarding outright.'),
    ])
    return ('<section class="block" id="mixups"><h2>Mind games &amp; resets'
            '<a href="#toc" class="bt">contents ↑</a></h2>'
            '<p class="note2">Opening up a defender once you’ve cornered them.</p>'
            '<div class="sys">' + rows + '</div></section>')

# ============================================================ §7 matchups
def mu(name, tier, dsc):
    return (f'<div class="mu"><div class="mu-h"><b>{name}</b><span class="mtier">{tier}</span></div>'
            f'<div class="dsc">{dsc}</div></div>')
def sec_matchups():
    cards = ''.join([
        mu('Magneto', 'top tier — very hard',
           f'The fastest, strongest rushdown in the game — one opening can kill. Lead with the '
           f'<b>Gene Splice / Cannon Spike assists</b> for cross-up protection, contest his approach with '
           f'Cammy’s <b>invincible</b> {spn("Cannon Spike","DP","K")}, and time '
           f'{spn("Killer Bee Assault","QCB","PP",air=True)} to phase through EM Disruptor and punish. '
           f'Do not get opened.'),
        mu('Storm', 'top tier — hard',
           f'Everyone struggles, but she takes <i>more</i> damage than Cammy. One '
           f'{spn("Killer Bee Assault","QCB","PP",air=True)} punishes a Whirlwind/Typhoon or her runaway '
           f'fly game (she can’t block while flying). {spn("Cannon Revenge","HCB","P")} her dive-ins; match '
           f'her air mobility with {spn("Cannon Drill","QCF","K")}/{spn("Cannon Strike","QCB","K",air=True)}. '
           f'Strip her typhoon &amp; fly and her options collapse.'),
        mu('Sentinel', 'top tier — winnable',
           f'His stomp-rushdown chips on block. <b>Push-block</b> the stomp or stuff it with '
           f'{spn("Cannon Spike","DP","K")} / the Gene Splice assist. He’s huge — he eats ~4 KBA combos, so '
           f'stay patient and play act/react. Cyclops’ beams contest his drones.'),
        mu('Cable', 'top tier — patience',
           f'He wins a pure keep-away war (Cammy has no projectile). Anticipate the Viper Beam → '
           f'{spn("Killer Bee Assault","QCB","PP",air=True)} (invincible) to dodge <i>and</i> punish; or '
           f'dash-jump + air {spn("Cannon Drill","QCF","K")} to get behind his weak air-defence. Cammy is '
           f'short enough to <b>duck his gunfire</b>. Let BB Hood / Cyclops contest the projectile war.'),
        mu('Spiral', 'top tier — toughest',
           f'Considered the hardest character to face. Don’t throw out laggy specials except in combos. '
           f'{spn("Killer Bee Assault","QCB","PP",air=True)} her when she rises to replenish swords; block '
           f'the sword wall and punish the gaps. Pure reflexes and patience; lean on Cyclops’ beams + assists '
           f'to contest space.'),
    ])
    arche = ''.join([
        sysrow('vs Rushdown',
               'The Gene Splice + Cannon Spike assists are your wall. Push-block to reset space, then '
               'KBA / super the gap. Don’t mash into their pressure.'),
        sysrow('vs Keep-away / runaway',
               f'Close with Cammy’s dash; slip {spn("Cannon Drill","QCF","K")}/{spn("Spin Drive Smasher","QCF","KK")} '
               f'under beams; BB Hood can out-zone some keepaway outright.'),
        sysrow('vs Turtle',
               f'{spn("Cool Hunting","QCF","PP")} chip + {spn("Hyper Apple For You","HCB","KK")} (unblockable '
               f'grab) + Cyclops beam chip pry them open. Snapback their anchor to force a fight.'),
    ])
    return ('<section class="block" id="matchups"><h2>Matchups vs the top tiers'
            '<a href="#toc" class="bt">contents ↑</a></h2>'
            '<p class="note2">MvC2 is defined by a handful of characters. Here is how this team handles '
            'them, then a quick primer by play-style.</p>' + cards +
            '<h3>By archetype</h3><div class="sys">' + arche + '</div></section>')

# ============================================================ §8 common mistakes
def sec_mistakes():
    rows = ''.join([
        sysrow('Throwing beams / missiles mindlessly',
               'Good players punish the recovery. Mix heights and cancel projectiles into specials.'),
        sysrow('Forgetting Cammy has no projectile',
               'You must approach — don’t sit back and lose the keep-away war you can’t win.'),
        sysrow('Jumping to escape pressure',
               'You can’t air-block a grounded normal — you’ll just get launched. Block or push-block instead.'),
        sysrow('Over-chaining lights',
               f'Damage scaling guts your finisher. Keep chains short — {grp("LP","LP","HP")} is plenty.'),
        sysrow('Repeating reversals / counters',
               'Cannon Spike, Gene Splice and Cannon Revenge are all readable. Bait one out, then punish.'),
        sysrow('Burning meter on solo supers',
               'When a DHC would kill or rescue, a single super is a waste. Plan the bars.'),
        sysrow('Leaving Cyclops on point vs rushdown',
               'He has no safe anti-air — he’s the <b>anchor</b> for a reason. Keep him in back behind Gene Splice.'),
        sysrow('Approaching without calling an assist',
               'Calling Gene Splice / Cannon Spike before you dash in is the entire point of this team.'),
        sysrow('Cornering yourself as BB Hood with no meter',
               'Her launcher and anti-air are weak — she needs space and bars to function.'),
    ])
    return ('<section class="block donts" id="mistakes"><h2>Common mistakes to break'
            '<a href="#toc" class="bt">contents ↑</a></h2>'
            '<p class="note2">Habits that quietly lose games — fix these first.</p>'
            '<div class="sys">' + rows + '</div></section>')

# ============================================================ §9 Abyss
def sec_abyss():
    rows = ''.join([
        sysrow('Form 1 — armoured humanoid',
               f'Just combo him to death — e.g. Cyclops {grp("LP","LK","HK")} <span class="ann">XX</span> '
               f'{spn("Cyclone Kick","QCB","K")}. When he fires the big cannon, make sure you’re already on '
               f'the safe side, then go back to beams/missiles.'),
        sysrow('Form 2 — orange blob',
               f'Zone it down with {spn("Optic Blast","QCF","P")} and missiles. When the bubble projectiles '
               f'come out, <b>super-jump then double-jump</b> over them and keep chipping.'),
        sysrow('Form 3 — small humanoid',
               f'Open with a jumping {spn("Mega Optic Blast","QCF","PP")}, or simply DHC / THC him down — '
               f'big beams melt this last form fast.'),
    ])
    return ('<section class="block" id="abyss"><h2>Beating Arcade mode — Abyss'
            '<a href="#toc" class="bt">contents ↑</a></h2>'
            '<p class="note2">The final boss has three forms. Zone the first, out-manoeuvre the second, '
            'nuke the third.</p><div class="sys">' + rows + '</div></section>')

# ============================================================ legends (compact)
def button_legend():
    items = [('LP','Light Punch — green (Y)'), ('HP','Hard Punch — blue (X)'),
             ('LK','Light Kick — yellow (B)'), ('HK','Hard Kick — red (A)'),
             ('A1','Assist 1 — grey trigger'), ('A2','Assist 2 — grey trigger'),
             ('P','any Punch'), ('K','any Kick'), ('PP','both Punches'), ('KK','both Kicks')]
    lg = ''.join(f'<div class="lg"><span>{keycap(t)}</span><span>{d}</span></div>' for t, d in items)
    mots = [('QCF','quarter-circle fwd'), ('QCB','quarter-circle back'), ('HCF','half-circle fwd'),
            ('HCB','half-circle back'), ('DP','dragon punch')]
    dirs = [('[B]F','charge back→fwd'), ('[D]U','charge down→up'),
            ('F','forward'), ('B','back'), ('U','up'), ('D','down')]
    nrows = ''.join(f'<div class="lg"><span>{mot(t)}</span><span>{d}</span></div>' for t, d in mots)
    nrows += ''.join(f'<div class="lg"><span>{dirp(t)}</span><span>{d}</span></div>' for t, d in dirs)
    return (f'<div class="legendwrap"><div class="leg-grid">{lg}</div></div>'
            f'<div class="legendwrap"><div class="motlegend" style="margin-top:0;line-height:1.5">Motions '
            f'are <b>facing-relative</b> — <b>F</b> = toward the opponent, <b>B</b> = away. A named pill '
            f'(e.g. {spn("Cyclone Kick","QCB","K")}) is a special move — hover it for the input.</div>'
            f'<div class="leg-grid">{nrows}</div></div>')

# ============================================================ page
def build():
    css = open(_os.path.join(_HERE,'style.css')).read()
    js = open(_os.path.join(_HERE,'app.js')).read()
    defs = ('<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>'
            '<linearGradient id="gp" x1="0" x2="1" y1="0" y2="0"><stop offset="50%" stop-color="#2fb84a"/>'
            '<stop offset="50%" stop-color="#2f86f0"/></linearGradient>'
            '<linearGradient id="gk" x1="0" x2="1" y1="0" y2="0"><stop offset="50%" stop-color="#f2c531"/>'
            '<stop offset="50%" stop-color="#ec3b3b"/></linearGradient></defs></svg>')
    toc = ('<nav id="toc"><div class="toc-head"><h2>Contents</h2></div><ul class="toc-top">'
           '<li><a href="#how">How to read this guide</a></li>'
           '<li><a href="#sw">Strengths &amp; weaknesses</a></li>'
           '<li><a href="#assists">Assist reference (α/β/γ)</a></li>'
           '<li><a href="#neutral">Neutral game &amp; spacing</a></li>'
           '<li><a href="#defense">Defense &amp; escaping pressure</a></li>'
           '<li><a href="#meter">Meter game &amp; DHC routes</a></li>'
           '<li><a href="#mixups">Mind games &amp; resets</a></li>'
           '<li><a href="#matchups">Matchups vs the top tiers</a></li>'
           '<li><a href="#mistakes">Common mistakes to break</a></li>'
           '<li><a href="#abyss">Beating Arcade — Abyss</a></li>'
           '<li><a href="#refs">References &amp; sources</a></li>'
           '</ul></nav>')
    intro = ('<p class="intro">The <b>advanced</b> companion for the <b>Cammy / BB Hood / Cyclops</b> team '
             'in <b>Marvel vs. Capcom 2</b> — strategy, team-building, matchups and habits, for when you '
             'already know the moves and combos. Pairs with the beginner guide (controls &amp; basics) and '
             'the combo dojo (73 combos to drill). Specials are shown by <b>name</b> — hover for the input.</p>')
    how = ('<section class="block" id="how"><h2>How to read this guide'
           '<a href="#toc" class="bt">contents ↑</a></h2>'
           '<p>Inputs use coloured buttons that match your AYN&nbsp;Thor face buttons and short, '
           'facing-relative motion tokens. This guide is mostly prose — the deep movelist is in the '
           'beginner guide, the combos in the combo dojo.</p>' + button_legend() + '</section>')
    body = (f'<header class="bar"><span class="title">MvC2 Advanced — Cammy · BB Hood · Cyclops</span>'
            f'<a class="jump" href="#toc">Contents</a></header>'
            f'<div class="wrap"><h1>Cammy / BB Hood / Cyclops — the advanced guide</h1>'
            f'{intro}{toc}{how}{sec_sw()}{sec_assists()}{sec_neutral()}{sec_defense()}{sec_meter()}'
            f'{sec_mixups()}{sec_matchups()}{sec_mistakes()}{sec_abyss()}{references_section()}'
            f'</div><a href="#top" id="totop" aria-label="Back to top">↑</a><script>{js}</script>')
    doc = ('<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
           '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
           '<meta name="color-scheme" content="dark">\n'
           '<title>MvC2 — Cammy / BB Hood / Cyclops (advanced guide)</title>\n'
           f'<style>{css}</style>\n</head>\n<body id="top">\n{defs}\n{body}\n</body>\n</html>\n')
    open(OUT, 'w').write(doc)
    print('wrote', OUT, len(doc), 'bytes')

if __name__ == '__main__':
    build()