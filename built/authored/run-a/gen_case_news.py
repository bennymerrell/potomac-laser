"""§7.2 AUTHOR — Case Studies + News (run 20260924-125928).

  hero-dark-centered          `.ab-hero` with no meta row and no CTA (Case Studies; reused by News)
  image-link-cards-5          5 linked image cards, no section head (Case Studies)
  image-link-cards-12-button  12 linked image cards + one centred secondary button (News)

Copy is extracted from the design HTML (about_shared.ab_cards), not retyped. Brand normalisation
applies to the present-tense hero ledes/H1 only; case-study titles/text and dated news headlines
name the company as it was at the time and stay verbatim (listed in the report).
Values are written as <page>.<pattern>.values.json so both pages can use the same pattern.
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from about_shared import *  # noqa

Z = '/private/tmp/claude-501/-Users-admin-orca-potomac-laser/d79e1efa-e1f9-4dfb-b04f-d08b0ac7ba4e/scratchpad/zip/'


def save_values(page, pid, tok):
    with open(os.path.join(OUT, f'{page}.{pid}.values.json'), 'w') as f:
        json.dump(tok.values, f, indent=1, ensure_ascii=False)


def hero(page, eb, h1, lede):
    t = Tok()
    sec = hero_centered(t, eb, h1, lede)
    save_values(page, 'hero-dark-centered', t)
    return sec, t


def cards_section(page, pid, cards, prefix, button=None):
    t = Tok()
    kids = [grid([link_card(t, f'{prefix}_{i + 1}', c['meta'], c['title'], f'<p>{c["text"]}</p>', c['label'], c['href'])
                  for i, c in enumerate(cards)], 3)]
    if button:
        kids.append(container([button_secondary(t, *button)], flex_direction='row', flex_justify_content='center',
                              width={'unit': '%', 'size': 100}, _margin=box(40, 0, 0, 0)))
    sec = band(kids, bg=SUBTLE, align='stretch')
    save_values(page, pid, t)
    return sec, t


# ---------------------------------------------------------------- Case Studies
cs = sections(Z + 'About - Case Studies.html')
sec, t = hero('case-studies', 'Proof', 'Case studies',
              '<p>How Goodfellow Microfabrication has solved micro-manufacturing problems for '
              '<strong>semiconductor, aerospace, medical device and electronics</strong> customers.</p>')
save('hero-dark-centered', sec, t)
cards = ab_cards(cs[1]); assert len(cards) == 5
sec, t = cards_section('case-studies', 'image-link-cards-5', cards, 'cs_img')
save('image-link-cards-5', sec, t)

# ---------------------------------------------------------------- News
nw = sections(Z + 'About - News.html')
hero('news', 'Newsroom', 'News from Goodfellow Microfabrication',
     '<p>Awards, programmes, grants and features from over four decades of <strong>micro-manufacturing</strong> '
     'at Goodfellow Microfabrication.</p>')
cards = ab_cards(nw[1]); assert len(cards) == 12
btn = re.search(r'<a href="([^"]+)"[^>]*class="btn btn--secondary"[^>]*>(.*?)</a>', nw[1])
sec, t = cards_section('news', 'image-link-cards-12-button', cards, 'news_img', button=(txt(btn.group(2)), btn.group(1)))
save('image-link-cards-12-button', sec, t)

json.dump({'case-studies': [c['img'] for c in ab_cards(cs[1])], 'news': [c['img'] for c in ab_cards(nw[1])]},
          open(os.path.join(OUT, 'case-news.images.json'), 'w'), indent=1)
print('ok')
