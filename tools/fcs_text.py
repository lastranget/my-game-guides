# -*- coding: utf-8 -*-
"""Prose sections (team plan, learning path, advanced) for the Felicia/Cyclops/Storm set."""
from gen import keycap, dirp, render_action, render_combo, M, MA, DB, SP, G, PRE, TAG
from fcs_data import META

def kb(t): return keycap(t)
def mv(m, b, air=False): return render_action(MA(m, b) if air else M(m, b))
def spn(n, m, b, air=False): return render_action(SP(n, m, b, air))
def dbtn(d, b): return render_action(DB(d, b))

def sysrow(nm, dsc, inn=''):
    intop = f'<span class="in">{inn}</span>' if inn else ''
    return (f'<div class="sysrow"><div class="top"><span class="nm">{nm}</span>{intop}</div>'
            f'<div class="dsc">{dsc}</div></div>')

def ccwrap(ch, title, inner):
    return f'<div class="ccombo" style="--ca:{META[ch]["ca"]}"><h3>{title}</h3>{inner}</div>'

# ============================================================ team plan (beginner)
def team_section():
    return ('<section class="block" id="team"><h2>How to play this team'
            '<a href="#toc" class="bt">contents ↑</a></h2>'
            '<h3>Why this team (in plain terms)</h3>'
            '<p>A fast rushdown point, an anchor whose assist makes that rushdown safe, and a top-tier '
            'closer who can also run away and win on her own:</p><ul>'
            '<li><b>Felicia</b> is your <b>point</b> — small, fast, and built to get in, open people up and '
            'cash out with her insane OTG combos. Her catch: she’s frail and has no real zoning, so she '
            'needs help getting in.</li>'
            '<li><b>Cyclops</b> is your <b>glue</b> — his <b>β Gene&nbsp;Splice</b> is one of the best '
            'anti-air assists in the game, so it covers Felicia’s approach; his <b>Mega Optic Blast</b> is '
            'a perfect DHC relay into Storm.</li>'
            '<li><b>Storm</b> is your <b>anchor</b> — the game’s best battery target, a huge '
            '<b>Lightning Storm</b> for damage, and <b>Hail Storm</b>, the safest DHC in the game. Even '
            'down to her alone she can <i>runaway</i> and steal games.</li></ul>'
            '<p>The glue is <b>anti-air</b>: Gene Splice makes Felicia’s jump-ins and dash-ins safe, '
            'Felicia and Cyclops feed meter to Storm, and Storm’s safe DHC + runaway mean a dropped '
            'character isn’t the end.</p>'
            '<p><b>Team order:</b> Felicia → Cyclops → Storm. <b>Assists:</b> Felicia <b>α</b> '
            '(Delta&nbsp;Kick), Cyclops <b>β</b> (Gene&nbsp;Splice), Storm <b>α</b> (Whirlwind).</p>'
            '<h3>Your first-day game plan</h3><ul>'
            f'<li>Play Felicia and get in — dash, super-jump, or roll forward with Rolling Buckler. Touch '
            f'them and do {kb("LP")}{kb("LK")} › {spn("Sand Splash","QCF","K")}.</li>'
            f'<li><b>Call Cyclops ({kb("A2")})</b> before you approach — Gene Splice covers you if they jump '
            f'or mash.</li>'
            '<li>Block when it isn’t your turn (hold back / down-back).</li>'
            f'<li>With a bar, end a chain in {spn("Dancing Flash","QCF","PP")} — or DHC it forward for the kill.</li>'
            '</ul></section>')

def path_section():
    steps = [
        ('Felicia’s touch', 'Land cr.LK/LP chains into Sand Splash, and always call the Gene Splice assist '
         'before you commit to getting in.'),
        ('Launch → air → OTG', 'Launch (HK), air-rave into Delta Kick, then OTG-relaunch with cr.HK or the '
         'Rolling Buckler → Sliding Kick. This is most of Felicia’s damage.'),
        ('Cyclops basics', 'cr.LK/LP, st.HK XX Cyclone Kick / Mega Optic Blast — and use Gene Splice as your '
         'on-point anti-air when Felicia is hurt.'),
        ('Storm in the air', 'Launch → air-rave XX Lightning Attack XX Lightning Storm. Learn to confirm into '
         'it from anywhere.'),
        ('The DHC kill', 'Felicia super → Cyclops Mega Optic Blast → Storm Lightning/Hail Storm. Bank meter '
         'with Felicia/Cyclops, cash it on Storm.'),
        ('Storm as anchor', 'Runaway (super-jump, air-dash, typhoons) to close games; tri-jump cross-ups when '
         'you want to rush. Advanced but match-winning.'),
    ]
    rows = ''.join(f'<li><b>{i}.</b> <b>{n}</b> — {t}</li>' for i, (n, t) in enumerate(steps, 1))
    return ('<section class="block" id="path"><h2>Learning path — what to practice'
            f'<a href="#toc" class="bt">contents ↑</a></h2><ul>{rows}</ul></section>')

# ============================================================ strengths/weaknesses
SW = {
 'felicia': (['<b>Very fast</b> with huge combo potential.',
              '<b>Insane OTG game</b> — Sliding Kick &amp; cr.HK relaunch into more.',
              'All three Hypers combo easily; great mobility (run, super-jump, Delta-Kick air control).'],
             ['<b>Physically weak</b> — low damage output.',
              '<b>Frail</b> — takes damage poorly.',
              'Short-range normals (a point-blank character); no real zoning; good rollers beat her OTGs.']),
 'cyclops': (['<b>Two of the best beam supers</b> in the game; high-priority ground chains.',
              'Great air priority + a double jump; the <b>Gene Splice</b> assist is elite — the team’s glue.',
              'Balanced and durable.'],
             ['<b>No reliable on-point anti-air</b> (Gene Splice is punished on block).',
              'No truly safe reversal; middling speed — wins on reads.']),
 'storm':   (['<b>2nd-fastest</b>; top-tier rushdown <i>and</i> runaway.',
              '<b>8-way air-dash, flight, tri-jump</b> cross-ups; tons of range.',
              '<b>Hail Storm</b> = the safest DHC in the game; <b>Lightning Storm</b> can take 40–70%.',
              'The best <b>battery</b> in the game.'],
             ['<b>Hard to learn</b> and frail; weak chip.',
              'Only <i>runaway</i>, not true keep-away; her specials are slow to start/recover.',
              'Hail Storm is telegraphed on its own; she’d like better anti-airs.']),
}
def sw_section():
    blocks = []
    for ch in META:
        pros, cons = SW[ch]
        pl = ''.join(f'<li>{x}</li>' for x in pros)
        cl = ''.join(f'<li>{x}</li>' for x in cons)
        blocks.append(ccwrap(ch, f'{META[ch]["name"]} <span class="role">· {META[ch]["role"]}</span>',
            f'<div class="sw"><div><h4 class="pro">Strengths</h4><ul>{pl}</ul></div>'
            f'<div><h4 class="con">Weaknesses</h4><ul>{cl}</ul></div></div>'))
    return ('<section class="block" id="sw"><h2>Strengths &amp; weaknesses'
            '<a href="#toc" class="bt">contents ↑</a></h2>'
            '<p class="note2">Know each character’s job — it explains the point → glue → anchor structure.</p>'
            + ''.join(ccwrap_order(blocks)) + '</section>')

def ccwrap_order(blocks):  # keep META order
    return blocks

# ============================================================ assists
def arow(typ, desc, pick=False):
    badge = '<span class="pick">team pick</span>' if pick else ''
    return f'<div class="arow"><span class="atype">{typ}</span><span class="adesc">{desc}{badge}</span></div>'
def assists_section():
    fe = ccwrap('felicia', 'Felicia', ''.join([
        arow('α Alpha', f'<b>Delta Kick</b> ({mv("DP","K")}) — full-screen, crosses up, knocks down for an '
             'OTG. Her best assist.', pick=True),
        arow('β Beta', f'<b>Sand Splash</b> ({mv("QCF","K")}) — fast, safe, low projectile.'),
        arow('γ Gamma', f'<b>Neko Spike</b> ({mv("DP","P")}) — little reason to pick it.'),
    ]))
    cy = ccwrap('cyclops', 'Cyclops', ''.join([
        arow('α Alpha', f'<b>Optic Blast</b> ({mv("QCF","P")}) — fast beam; beats fireballs.'),
        arow('β Beta', f'<b>Gene Splice</b> ({mv("DP","P")}) — elite anti-air; makes Felicia’s rushdown '
             'safe. The whole reason he’s here.', pick=True),
        arow('γ Gamma', f'<b>Cyclone Kick</b> ({mv("QCB","K")}) — least useful.'),
    ]))
    st = ccwrap('storm', 'Storm', ''.join([
        arow('α Alpha', f'<b>Whirlwind</b> ({mv("QCF","K")}, Horizontal Typhoon) — a solid projectile assist.', pick=True),
        arow('β Beta', '<b>Lightning Attack</b> — an air-dash assist.'),
        arow('γ Gamma', '<b>Double Typhoon</b> — situational.'),
        '<div class="dsc" style="margin-top:5px">Storm’s real value is as the <b>anchor</b>: '
        f'{spn("Hail Storm","QCB","PP")} is the safest DHC in the game and she can runaway to close.</div>',
    ]))
    return ('<section class="block" id="assists"><h2>Assist reference (α / β / γ)'
            '<a href="#toc" class="bt">contents ↑</a></h2>'
            '<p class="note2">The team runs <b>Felicia α · Cyclops β · Storm α</b> — Gene Splice is the key '
            'pick that covers the point.</p>' + fe + cy + st + '</section>')

# ============================================================ neutral
def neutral_section():
    fe = ccwrap('felicia', 'Felicia <span class="role">· get in</span>', ''.join([
        sysrow('No zoning — you must approach', f'Get in with the super-jump, a dash, or '
               f'{spn("Rolling Buckler","QCF","P")} (faster than a dash). Always with the Gene Splice assist out.'),
        sysrow('Pokes', f'{spn("Sand Splash","QCF","K")} reaches ~¾ screen; cr.HK is a fast knockdown sweep '
               'that starts your OTG game.'),
        sysrow('Mistake punisher', f'{spn("Hyper Sand Splash","QCF","KK")} covers the whole screen — punish a '
               'whiff from afar.'),
    ]))
    cy = ccwrap('cyclops', 'Cyclops <span class="role">· beam control</span>', ''.join([
        sysrow('Beam game', f'Mix {spn("Optic Blast","QCF","LP")} (low/quick) and the HP angled version — '
               'don’t throw them mindlessly.'),
        sysrow('His anti-air problem', 'Standing HK is his only real AA and its range is short — that’s why '
               'he sits behind the Gene Splice assist.'),
        sysrow('Punish', f'Jump back and {spn("Super Optic Blast","QCF","KK")} a called assist or beam.'),
    ]))
    st = ccwrap('storm', 'Storm <span class="role">· runaway &amp; rush</span>', ''.join([
        sysrow('Runaway', f'Super-jump, air-dash and rain {spn("Horizontal Typhoon","QCF","K")} / air fierces; '
               f'{spn("Vertical Typhoon","HCB","K")} keeps them grounded. Her way to stall out a lead.'),
        sysrow('Rushdown', 'Tri-jump cross-ups and her fast dash open people up; convert into the air rave.'),
        sysrow('Battery', 'She builds meter faster than anyone — air fierces + the air-throw rave bank ~¾ a bar.'),
    ]))
    return ('<section class="block" id="neutral"><h2>Neutral game &amp; spacing'
            '<a href="#toc" class="bt">contents ↑</a></h2>'
            '<p class="note2">How each character wins the ground before a combo starts.</p>' + fe + cy + st + '</section>')

# ============================================================ defense
def defense_section():
    rows = ''.join([
        sysrow('Advancing Guard (push-block)', 'Both punches as you block to shove pressure off. Don’t spam '
               'it.', f'{kb("PP")} <span class="ann">blocking</span>'),
        sysrow('Variable Counter', 'Tag a partner in with a counter mid-blockstring — 1 bar. Good for bailing '
               'frail Felicia out.', f'{dirp("B")}{dirp("DB")}{dirp("D")}+{kb("A1")}'),
        sysrow('Reversals', f'Cyclops’ {spn("Gene Splice","DP","P")} is fast but punished on block. Felicia &amp; '
               'Storm lack a great reversal — block, push-block, and DHC out instead.'),
        sysrow('Air-guard — and its limit', 'Hold back in the air to block air attacks/projectiles/supers — '
               'but you can’t air-block a grounded normal.', f'{dirp("B")} <span class="ann">in air</span>'),
        sysrow('Hail Storm bail', f'DHC into Storm’s {spn("Hail Storm","QCB","PP")} (no recovery) to escape a '
               'bad spot and bring her in safely.'),
        sysrow('Snapback', 'QCF+assist (1 bar) forces out a dangerous point character or deletes a low '
               'assist.', f'{spn("Snapback","QCF","A1")}'),
    ])
    return ('<section class="block" id="defense"><h2>Defense &amp; escaping pressure'
            f'<a href="#toc" class="bt">contents ↑</a></h2><div class="sys">{rows}</div></section>')

# ============================================================ meter & DHC
def meter_section():
    routes = ''.join([
        '<div class="cmb"><div class="cmb-h"><b>DHC kill</b></div>' + render_combo(
            [SP('Dancing Flash', 'QCF', 'PP'), TAG('Felicia'), PRE('DHC'),
             SP('Mega Optic Blast', 'QCF', 'PP'), TAG('Cyclops'), PRE('DHC'),
             SP('Lightning Storm', 'HCF', 'PP'), TAG('Storm')]) + '</div>',
        '<div class="cmb"><div class="cmb-h"><b>Safe relay / rescue</b></div>' + render_combo(
            [SP('Mega Optic Blast', 'QCF', 'PP'), TAG('Cyclops'), PRE('DHC'),
             SP('Hail Storm', 'QCB', 'PP'), TAG('Storm · no recovery')]) + '</div>',
    ])
    rows = ''.join([
        sysrow('Felicia &amp; Cyclops are the battery', 'Their combos and chip build bars; bank them for '
               'Storm’s kill or a guaranteed DHC.'),
        sysrow('When to spend', '<b>Solo super</b> to confirm a stray hit; <b>DHC</b> to kill or to rescue a '
               'character safely (into Hail Storm); <b>save 2+</b> for a DHC kill.'),
    ])
    return ('<section class="block" id="meter"><h2>Meter game &amp; DHC routes'
            f'<a href="#toc" class="bt">contents ↑</a></h2><div class="sys">{rows}</div>'
            f'<h3>DHC routes</h3>{routes}</section>')

# ============================================================ mind games
def mixups_section():
    rows = ''.join([
        sysrow('OTG resets (Felicia)', f'After a knockdown, mix the Sliding-Kick / cr.HK relaunch with a '
               f'meaty {spn("Please Help Me!","QCB","KK")} — but bait good rollers, don’t auto-pilot it.'),
        sysrow('Get-in cross-up (Felicia)', 'Super-jump and angle a Delta&nbsp;Kick to come down on the far '
               'side; call Gene Splice first so they can’t challenge.'),
        sysrow('Tick throws (Felicia)', 'cr.LP, walk up, throw (mash for damage) — she’s fast enough to tick '
               'all day.'),
        sysrow('Tri-jump cross-up (Storm)', 'Storm’s tri-jump makes her jump-ins ambiguous; convert the open '
               'guard into the Lightning Storm air combo.'),
        sysrow('Pattern-breakers (Cyclops)', f'A surprise {spn("Running Tackle","[B]F","K")} (unblockable) or '
               f'{spn("Gene Splice","DP","P")} cracks a turtle.'),
    ])
    return ('<section class="block" id="mixups"><h2>Mind games &amp; resets'
            f'<a href="#toc" class="bt">contents ↑</a></h2><div class="sys">{rows}</div></section>')

# ============================================================ matchups (Storm)
def matchups_section(storm_list):
    cards = ''.join(
        f'<div class="mu"><div class="mu-h"><b>{n}</b></div><div class="dsc">{t}</div></div>'
        for n, t in storm_list)
    return ('<section class="block" id="matchups"><h2>Storm matchups'
            '<a href="#toc" class="bt">contents ↑</a></h2>'
            '<p class="note2">Storm is the anchor and the most matchup-defined of the three, so here’s the '
            'source author’s read on the whole cast (condensed). Felicia’s sources cover only the Abyss '
            'boss (zone form 1/3 with Hyper Sand Splash, super-jump the form-2 bubbles); Cyclops has no '
            'dedicated matchup data.</p>' + cards + '</section>')

# ============================================================ mistakes
def mistakes_section():
    rows = ''.join([
        sysrow('Sitting back with Felicia', 'She has no zoning — if you don’t approach, you lose. Use the '
               'super-jump / Rolling Buckler + the assist to get in.'),
        sysrow('Calling Felicia’s assist into danger', 'She’s frail — a badly-timed assist can lose her '
               'before she even fights.'),
        sysrow('Leaving Cyclops on point vs rushdown', 'He has no safe anti-air; he’s the glue, not the front '
               'line. Keep him in back behind Gene Splice.'),
        sysrow('Losing Storm early', 'She’s your comeback (runaway + Hail Storm). Protect the anchor.'),
        sysrow('Whiffing Help Me! / Hail Storm raw', 'Both are telegraphed on their own — use them in combos / '
               'as DHCs, not as random throws.'),
        sysrow('Over-OTGing vs good rollers', 'Mix in air combos and resets, or they’ll just roll out and '
               'punish.'),
        sysrow('Burning meter on solo supers', 'When a DHC kills or rescues, a single super is a waste.'),
        sysrow('Approaching without the assist', 'Calling Gene Splice before you dash in is the entire point '
               'of this team.'),
    ])
    return ('<section class="block donts" id="mistakes"><h2>Common mistakes to break'
            f'<a href="#toc" class="bt">contents ↑</a></h2><div class="sys">{rows}</div></section>')
