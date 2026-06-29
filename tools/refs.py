# -*- coding: utf-8 -*-
"""Shared References/credits section — cites the individual GameFAQs FAQs this
character set's guides were aggregated from. CSS-light (h3/ul/li/a/.note2) so it
drops cleanly into all three guides, including the hand-styled general guide."""

BASE = 'https://gamefaqs.gamespot.com/dreamcast/914427-marvel-vs-capcom-2/faqs/'

FAQS = [
    ('Cammy', [
        ('Cammy FAQ (v0.1)',           'Johmeriquai (John Hodges)', '7669'),
        ('Cammy Guide',                'The_fireboy',               '22878'),
        ('Cammy FAQ',                  'ABrea',                     '8517'),
    ]),
    ('BB Hood', [
        ('B.B. Hood / Bulleta FAQ',    'G-Boy',                     '8318'),
    ]),
    ('Cyclops', [
        ('Cyclops FAQ (v1.0)',         'Z-Force',                   '7893'),
        ('Cyclops Guide (v1.5)',       'PhatDan81',                 '7945'),
        ('Cyclops Character Guide (v1.1)', 'TBui (Trung Bui)',      '9838'),
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
        'Machine). Full credit to their authors. Move inputs were cross-checked across sources and '
        'normalised to MvC2’s four-button scheme (no medium button) and the facing-relative notation '
        'used throughout. Links open the live GameFAQs pages.</p>'
        + ''.join(groups) +
        '</section>')

if __name__ == '__main__':
    # emit the raw section HTML (used to paste into the hand-styled general guide)
    print(references_section())
