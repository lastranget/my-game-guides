# -*- coding: utf-8 -*-
"""Shared References/credits section for the KOF XI character guides."""

BASE = 'https://gamefaqs.gamespot.com/arcade/928580-the-king-of-fighters-xi/faqs/'

# (title, author, faq-id) — which sources fed each guide
COMMON = ('The King of Fighters XI — FAQ / Move List &amp; Game System', 'Tel', '44141')
PER = {
    'athena': ('Athena Asamiya FAQ', 'dante_croft (Durval Oliveira)', '51436'),
    'terry':  ('Terry Bogard FAQ', 'Psychochronic (Brett Navarro)', '45250'),
    'bjenet': ('Bonne Jenet Character FAQ', 'Raul Torrez', '44220'),
}

def references_section(char):
    main = PER[char]
    items = ''.join(
        f'<li><a href="{BASE}{fid}" rel="noopener noreferrer">{title}</a> — {author}</li>'
        for title, author, fid in (main, COMMON))
    return (
        '<section class="block" id="refs"><h2>References &amp; sources'
        '<a href="#toc" class="bt">contents ↑</a></h2>'
        '<p class="note2">This guide aggregates and re-notates the community FAQs below, hosted on '
        '<b>GameFAQs</b> (read via the Internet Archive’s Wayback Machine). Full credit to their authors. '
        'Moves use KOF’s native <b>A / B / C / D / E</b> buttons; the system notes are drawn from both '
        'sources. Links open the live GameFAQs pages.</p>'
        f'<ul>{items}</ul></section>')
