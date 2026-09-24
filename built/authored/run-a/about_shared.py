"""Shared builders + design extractors for the About-family pages (run 20260924-125928).

The measurements are the ones already verified on posts 12268/12277 (see gen_about_potomac.py);
this module only re-expresses them as reusable functions so the re-entry run's candidates
are built from the same values. gen_group.py / gen_about_potomac.py are left untouched —
they are the provenance of already-minted fragments.
"""
import html as _html
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from elb import *  # noqa

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'candidates')
os.makedirs(OUT, exist_ok=True)

INK = '#0F1620'
MUTED = '#65718A'
LINE = '#DCE1EA'
SUBTLE = '#F6F8FB'
NAVY = '#15253D'
BODY = '#6B7280'
CARD_SHADOW = '0 2px 8px rgba(0,0,0,.07)'
GRID_BG = ('background-image:radial-gradient(ellipse at 30% 0%,rgba(14,99,168,0.28) 0%,transparent 60%),'
           'radial-gradient(ellipse at 90% 100%,rgba(148,18,82,0.16) 0%,transparent 55%),'
           'linear-gradient(rgba(255,255,255,0.04) 1px,transparent 1px),'
           'linear-gradient(90deg,rgba(255,255,255,0.04) 1px,transparent 1px);'
           'background-size:auto,auto,32px 32px,32px 32px;')
COLS2 = ('selector{{flex:0 0 calc((100% - {g}px) / 2) !important;max-width:calc((100% - {g}px) / 2) !important}}'
         '@media(max-width:979px){{selector{{flex:0 0 100% !important;max-width:100% !important}}}}')


def save(pid, section, tok):
    with open(os.path.join(OUT, pid + '.json'), 'w') as f:
        json.dump([section], f, indent=1, ensure_ascii=False)
    with open(os.path.join(OUT, pid + '.values.json'), 'w') as f:
        json.dump(tok.values, f, indent=1, ensure_ascii=False)


# ------------------------------------------------------------------ building blocks
def eyebrow(t, value, align=None, ls=1.68, margin=None, color='#F5821F'):
    kw = {'_margin': margin} if margin else {}
    return heading(t('heading', value), 12, '600', color=color, align=align, lh=18, ls=ls, upper=True, **kw)


def section_head(t, eb, h2, lede=None, align='center', width=760, mb=48):
    kids = [eyebrow(t, eb, align=align if align == 'center' else None),
            heading(t('heading', h2), 40, '600', tag='h2', color=INK, align=align if align == 'center' else None,
                    lh=44.8, ls=-0.8, _margin=box(18, 0, 0, 0))]
    if lede:
        kids.append(text(t('body', lede), 18, color='#3C4858', lh=29.7, align=align if align == 'center' else None,
                         _margin=box(16, 0, 0, 0)))
    return container(kids, flex_direction='column', flex_align_items='center' if align == 'center' else 'flex-start',
                     flex_gap=gap(0), width=px(width) if align == 'center' else {'unit': '%', 'size': 100},
                     width_mobile={'unit': '%', 'size': 100}, _margin=box(0, 0, mb, 0))


def band(children, bg='#FFFFFF', align='stretch', pad=(80, 24)):
    return container([
        container(children, content_width='boxed', flex_direction='column', flex_align_items=align, flex_gap=gap(0)),
    ], flex_direction='column', flex_align_items='center', padding=box(pad[0], pad[1]),
       background_background='classic', background_color_hex=bg)


def grid(cards, n, g=20, justify=None):
    per = f'calc((100% - {(n - 1) * g}px) / {n})'
    css = (f'selector > .e-con{{flex:0 0 {per} !important;max-width:{per} !important}}'
           f'@media(max-width:979px){{selector > .e-con{{flex:0 0 100% !important;max-width:100% !important}}}}')
    kw = {'flex_justify_content': justify} if justify else {}
    return container(cards, flex_direction='row', flex_wrap='wrap', flex_align_items='stretch',
                     flex_gap=gap(g, g), width={'unit': '%', 'size': 100}, custom_css=css, **kw)


def card(children, pad, g, extra_css='', **kw):
    return container(children, flex_direction='column', flex_align_items='stretch', flex_gap=gap(g),
                     padding=pad, background_background='classic', background_color_hex='#FFFFFF',
                     border_border='solid', border_width=box(1), border_color=LINE, border_radius=box(8),
                     custom_css=f'selector{{box-shadow:{CARD_SHADOW};overflow:hidden}}' + extra_css, **kw)


def hero_centered(t, eb, h1, lede, extra=None, pad_bottom=64):
    """The About pages' `.ab-hero`: centred eyebrow + H1 + lede on dark navy grid.
    `extra` is appended below the lede (meta row / CTA row) — the caller owns it."""
    kids = [
        eyebrow(t, eb, align='center', ls=2.16),
        heading(t('heading', h1), 54.4, '600', tag='h1', color='#FFFFFF', align='center', lh=57.66, ls=-1.088,
                _margin=box(43, 0, 18, 0),  # 24px eyebrow line box + 20 + 18 − 18px widget line (12295 iter 1: 5px short at 38)
                css='selector .elementor-heading-title{max-width:22ch;margin:0 auto;text-wrap:balance}'),
        text(t('body', lede), 18, color='rgba(255,255,255,0.74)', lh=29.7, align='center',
             extra_css='selector p{max-width:727px;margin:0 auto}selector strong{color:#fff;font-weight:600}'
                       'selector a{color:#fff;text-decoration:underline;text-underline-offset:3px}'),
    ]
    if extra:
        kids.append(extra)
    return container([
        container(kids, content_width='boxed', flex_direction='column', flex_align_items='center', flex_gap=gap(0),
                  boxed_width=px(1200)),
    ], flex_direction='column', flex_align_items='center', padding=box(72, 24, pad_bottom, 24),
       background_background='classic', background_color_hex='#0D1B2A',
       custom_css='selector{overflow:hidden;' + GRID_BG + '}')


LINK_LABEL = ('selector a, selector p{font-size:11.5px;font-weight:800;letter-spacing:1.15px;'
              'text-transform:uppercase;color:#15253D;text-decoration:none;line-height:17.25px}')


def link_card(t, asset, meta, title, body_html, label, href, img_ratio='16/10'):
    """`a.ab-card`: whole card is the link; image flush top (16:10 cover), then tag/title/text,
    and an uppercase label pinned to the bottom. Hover lift + orange bottom bar as the design."""
    return card([
        image(t('image', {'asset': asset}),
              css=f'selector{{margin:0;background:#0D1B2A}}selector img{{display:block;width:100%;'
                  f'aspect-ratio:{img_ratio};height:auto;object-fit:cover}}'),
        container([
            heading(t('heading', meta), 11, '700', color='#F5821F', lh=16.5, ls=1.54, upper=True),
            heading(t('heading', title), 17.6, '700', tag='h3', color=NAVY, lh=22.88, ls=-0.176),
            text(t('body', body_html), 14, color=BODY, lh=23.1),
            text(t('body', f'<p>{label}</p>'), 11.5, color=NAVY, weight='800', lh=17.25,
                 extra_css=LINK_LABEL + 'selector{margin-top:auto}'),
        ], flex_direction='column', flex_align_items='stretch', flex_gap=gap(10), padding=box(20, 22, 24, 22),
           custom_css='selector{flex:1 1 auto}'),
    ], box(0), 0, html_tag='a', link={'url': t('url', href), 'is_external': 'on', 'nofollow': ''},
       extra_css=('selector{position:relative;text-decoration:none;color:inherit;transition:transform .3s cubic-bezier(.25,.46,.45,.94),'
                  'box-shadow .3s cubic-bezier(.25,.46,.45,.94)}selector:hover{transform:translateY(-2px);'
                  'box-shadow:0 10px 24px rgba(15,42,68,.08)}selector::after{content:"";position:absolute;left:0;right:0;'
                  'bottom:0;height:3px;background:var(--e-global-color-gforange);transform:scaleX(0);transform-origin:left;'
                  'transition:transform .3s cubic-bezier(.25,.46,.45,.94)}selector:hover::after{transform:scaleX(1)}'))


def button_secondary(t, label, href):
    return button(t('button', label), t('url', href), bg='#FFFFFF', fg='#F5821F', border='#F5821F')


# ------------------------------------------------------------------ design extraction
def inner(s):
    return re.sub(r'\s+', ' ', s).strip()


def sections(path):
    src = open(path, encoding='utf-8').read()
    body = src[src.find('<body'):]
    return re.findall(r'<section\b.*?</section>', body, re.S)


def txt(s):
    """Visible text of a fragment, entities decoded (for heading slots, which render literally)."""
    return _html.unescape(inner(re.sub(r'<[^>]+>', ' ', s))).replace(' ,', ',').replace(' .', '.')


def ab_cards(sec):
    out = []
    for m in re.finditer(r'<a class="ab-card[^"]*" href="([^"]+)"[^>]*>(.*?)</a>(?=\s*(?:<a class="ab-card|</div>))', sec, re.S):
        href, c = m.group(1), m.group(2)
        g = lambda p: (re.search(p, c, re.S) or [None, None])[1]
        out.append({'href': href, 'img': g(r'<img src="([^"]+)"'), 'alt': g(r'<img[^>]*alt="([^"]*)"'),
                    'meta': txt(g(r'ab-card__meta">(.*?)</div>') or ''), 'title': txt(g(r'ab-card__title">(.*?)</h3>') or ''),
                    'text': inner(g(r'ab-card__text">(.*?)</p>') or ''), 'label': txt(g(r'ab-card__link">(.*?)</span>') or ''),
                    'filter': (re.search(r'data-filter-item="([^"]+)"', m.group(0)) or [None, None])[1]})
    return out
