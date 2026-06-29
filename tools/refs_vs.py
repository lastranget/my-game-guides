# -*- coding: utf-8 -*-
"""Shared References section for the Vampire Savior character guides."""
BASE = 'https://gamefaqs.gamespot.com/arcade/583724-vampire-savior-the-lord-of-vampire/faqs/'
COMMON = [
    ('Move List &amp; Guide', 'Kao_Megura', '5283'),
    ('Move List &amp; Guide', 'DJellybean', '7976'),
    ('Move List &amp; Guide', 'KTanaka', '1237'),
]
PER = {
    'bbhood':  [('B.B. Hood Guide', 'afroshouji', '1243'), ('B.B. Hood Guide', '_Neil_', '1242')],
    'morrigan': [('Morrigan Guide', 'MKim', '1248')],
    'lilith':  [('Lilith Guide', 'MKim', '1247')],
    'felicia': [],
}

def references_section(char):
    rows = PER.get(char, []) + COMMON
    items = ''.join(
        f'<li><a href="{BASE}{fid}" rel="noopener noreferrer">{title}</a> — {author}</li>'
        for title, author, fid in rows)
    extra = ('' if PER.get(char) else
             ' Felicia has no dedicated character FAQ, so her section is built from the full-game '
             'guides + Vampire Savior’s chain system.')
    return (
        '<section class="block" id="refs"><h2>References &amp; sources'
        '<a href="#toc" class="bt">contents ↑</a></h2>'
        '<p class="note2">Aggregated and re-notated from the community FAQs below, hosted on '
        '<b>GameFAQs</b> (read via the Internet Archive’s Wayback Machine). Full credit to their authors. '
        'Moves use Vampire Savior’s six buttons (LP/MP/HP, LK/MK/HK).' + extra + ' Links open the live '
        'GameFAQs pages.</p>'
        f'<ul>{items}</ul></section>')
