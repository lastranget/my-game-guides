# -*- coding: utf-8 -*-
"""Shared References section for the Felicia / Cyclops / Storm guide set."""
BASE = 'https://gamefaqs.gamespot.com/dreamcast/914427-marvel-vs-capcom-2/faqs/'
FAQS = [
    ('Felicia', [
        ('Felicia FAQ', 'SBAllen (Allen “Sailor Bacon” Tyner)', '7414'),
        ('Felicia FAQ', 'Elff Zero (Robert Blumel)', '8530'),
    ]),
    ('Cyclops', [
        ('Cyclops FAQ (v1.0)', 'Z-Force', '7893'),
        ('Cyclops Guide (v1.5)', 'PhatDan81', '7945'),
        ('Cyclops Character Guide (v1.1)', 'TBui (Trung Bui)', '9838'),
    ]),
    ('Storm', [
        ('Storm FAQ', 'The_fireboy', '23122'),
        ('Storm FAQ', 'RSmith', '8320'),
        ('Storm FAQ', 'Gotenks2000', '8321'),
        ('Storm FAQ', 'Shinkuu_r', '8330'),
    ]),
]

def references_section():
    groups = []
    for char, lst in FAQS:
        items = ''.join(
            f'<li><a href="{BASE}{fid}" rel="noopener noreferrer">{title}</a> — {author}</li>'
            for title, author, fid in lst)
        groups.append(f'<h3>{char}</h3><ul>{items}</ul>')
    return (
        '<section class="block" id="refs"><h2>References &amp; sources'
        '<a href="#toc" class="bt">contents ↑</a></h2>'
        '<p class="note2">This guide and its companions for this team aggregate and re-notate the '
        'community FAQs below, hosted on <b>GameFAQs</b> (read via the Internet Archive’s Wayback '
        'Machine). Full credit to their authors. Move inputs were cross-checked and normalised to '
        'MvC2’s four-button scheme (no medium button); Storm’s matchup notes are condensed from the '
        'source. Links open the live GameFAQs pages.</p>'
        + ''.join(groups) + '</section>')
