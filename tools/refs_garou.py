# -*- coding: utf-8 -*-
"""Shared References section for the Garou: Mark of the Wolves combo guides."""
BASE = 'https://gamefaqs.gamespot.com/arcade/562919-garou-mark-of-the-wolves/faqs/'
COMMON = [
    ('FAQ / Move List', 'JKuroki (James Kuroki)', '6097'),
    ('Combo FAQ', 'MGA', '7828'),
    ('Move List &amp; Guide', 'Goh_Billy', '46834'),
]
PER = {
    'terry':  [('Terry Guide', 'Shirow', '14695'), ('Terry Guide', 'ghoward11', '8673')],
    'bjenet': [('B. Jenet Guide', 'TalbainEric', '14967')],
}

def references_section(char):
    rows = PER.get(char, []) + COMMON
    items = ''.join(
        f'<li><a href="{BASE}{fid}" rel="noopener noreferrer">{title}</a> — {author}</li>'
        for title, author, fid in rows)
    return (
        '<section class="block" id="refs"><h2>References &amp; sources'
        '<a href="#toc" class="bt">contents ↑</a></h2>'
        '<p class="note2">Combos are drawn from the GameFAQs FAQs below (read via the Wayback Machine) — '
        'MGA’s Combo FAQ plus the movelists — and extended with Garou’s Brake/Break and super-cancel '
        'rules. Full credit to their authors. Buttons are Garou’s A/B/C/D (= LP/LK/HP/HK). Links open '
        'the live GameFAQs pages.</p>'
        f'<ul>{items}</ul></section>')
