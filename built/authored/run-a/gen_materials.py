"""§7.2 AUTHOR — RUN B, the nine Materials pages (run 20260924-135039). Run with a Python that has bs4.

The Materials pages reuse the About skeleton but vary item counts constantly (pills, check-lists, card
grids of 5/6/9, "Related:" lines). Rather than a fixed-arity fragment per count, list-like content lives
in ONE text-editor slot per section — a "rich body" — whose HTML uses a small class vocabulary the
fragment styles (count free, copy editable, no JS):

  <p class="pills"><span class="pill">…</span> | <a class="pill" href>…</a></p>     pill cloud
  <ul class="check"><li>…</li></ul>                                                 check-list cards
  <ul class="cards"><li>[<a href>]<span class="meta">…</span><h3>…</h3><p>…</p><span class="more">…</span></li></ul>
  <p class="eb">…</p>  sub-eyebrow · <p class="related">…</p> · <p class="note">…</p> · <p>…</p> prose

Patterns: split-media-rich · split-rich-media · head-rich-subtle · head-rich-white · split-rich-rich-related
· media-grid-6-note · media-grid-4-note · tabs-panels-6-note · figure-cards-2-note · rich-band-white.
Hero = library hero-dark-centered; close = cta-band-dark. Copy converted from the design DOM, never retyped.
"""
import html as H, json, os, re, sys
from bs4 import BeautifulSoup, NavigableString, Tag
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from about_shared import *  # noqa

Z = '/private/tmp/claude-501/-Users-admin-orca-potomac-laser/d79e1efa-e1f9-4dfb-b04f-d08b0ac7ba4e/scratchpad/zip/'
CHECK = ("url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' "
         "stroke='%23F5821F' stroke-width='2.5' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline "
         "points='20 6 9 17 4 12'/%3E%3C/svg%3E\")")
RICH_CSS = (
    'selector p{margin:0 0 16px}selector p:last-child{margin-bottom:0}'
    'selector a{color:#15253D;text-decoration:none}selector a:hover{color:#F5821F}'
    'selector p.pills{display:flex;flex-wrap:wrap;gap:10px;margin:0}'
    'selector .pill{display:inline-flex;align-items:center;padding:9px 16px;border:1.5px solid #DCE1EA;border-radius:9999px;background:#fff;'
    'font:700 13.5px/20.25px Inter,system-ui,sans-serif;color:#15253D;text-decoration:none;transition:all .3s cubic-bezier(.25,.46,.45,.94)}'
    'selector a.pill:hover{border-color:#F5821F;color:#15253D;transform:translateY(-1px);box-shadow:0 8px 20px rgba(245,130,31,.12)}'
    'selector p.pills + p.eb{margin-top:28px}'
    'selector p.eb{margin:0 0 14px;font:600 12px/18px Inter,system-ui,sans-serif;letter-spacing:1.68px;text-transform:uppercase;color:#F5821F}'
    'selector ul.check{list-style:none;margin:0;padding:0;display:grid;gap:12px}'
    'selector ul.check li{position:relative;margin:0;font-size:15.5px;line-height:25.575px;color:#3C4858;padding:16px 18px 16px 48px;'
    'background:#fff;border:1px solid #DCE1EA;border-radius:12px}'
    f'selector ul.check li::before{{content:"";position:absolute;left:18px;top:20px;width:18px;height:18px;background:{CHECK} no-repeat center/18px}}'
    'selector ul.cards{list-style:none;margin:0;padding:0;display:grid;gap:20px;grid-template-columns:repeat(3,minmax(0,1fr))}'
    '@media(max-width:979px){selector ul.cards{grid-template-columns:repeat(2,minmax(0,1fr))}}'
    '@media(max-width:620px){selector ul.cards{grid-template-columns:1fr}}'
    'selector ul.cards li{margin:0;display:flex;flex-direction:column;gap:10px;background:#fff;border:1px solid #DCE1EA;border-radius:8px;'
    'box-shadow:0 2px 8px rgba(0,0,0,.07);padding:24px 24px 26px;transition:transform .3s cubic-bezier(.25,.46,.45,.94),box-shadow .3s cubic-bezier(.25,.46,.45,.94)}'
    'selector ul.cards.p26 li{padding:26px 24px}'
    'selector ul.cards li > a{display:flex;flex-direction:column;gap:10px;flex:1;color:inherit;text-decoration:none}'
    'selector ul.cards li:has(> a):hover{transform:translateY(-2px);box-shadow:0 10px 24px rgba(15,42,68,.08)}'
    'selector ul.cards .meta{display:block;font:700 11px/16.5px Inter,system-ui,sans-serif;letter-spacing:1.54px;text-transform:uppercase;color:#F5821F}'
    'selector ul.cards h3{margin:0;font:700 17.6px/22.88px Inter,system-ui,sans-serif;letter-spacing:-.176px;color:#15253D}'
    'selector ul.cards p{margin:0;font-size:14px;line-height:23.1px;color:#6B7280}'
    'selector ul.cards .more{display:block;margin-top:auto;font:800 11.5px/17.25px Inter,system-ui,sans-serif;letter-spacing:1.15px;text-transform:uppercase;color:#15253D}'
    'selector p.related{margin:24px 0 0;font-size:15px;line-height:24px;text-align:center}'
    'selector ul + p.related{margin-top:28px}'
    'selector p.note{margin:28px auto 0;max-width:760px;font-size:15.5px;line-height:27.125px;text-align:center}'
    'selector ul.check.narrow{max-width:760px;margin:0 auto}'
    'selector p.aside{margin:28px 0 0;font-size:15px;line-height:26.25px;text-align:center}'
    'selector p.related a,selector p.note a,selector p.aside a{font-weight:700}')


def rich_text(t, html_, extra='', **kw):
    return text(t('body', html_), 16, color='#3C4858', lh=28, extra_css=RICH_CSS + extra, **kw)


# ------------------------------------------------------------------ brand normalisation
KEEP = ['Potomac Photonics has joined the', 'Potomac and Goodfellow', 'Potomac Photonics now combines',
        "Together, Potomac's microfabrication", 'Potomac Photonics, now part of', 'Potomac Photonics, <a']
BRAND_LOG = []


def brand(s):
    masks = {}
    for i, k in enumerate(KEEP):
        if k in s:
            m = f'@@K{i}@@'; masks[m] = k; s = s.replace(k, m)
    n = s.count('Potomac')
    s = s.replace('Potomac Photonics', 'Goodfellow Microfabrication').replace('Potomac', 'Goodfellow Microfabrication')
    for m, k in masks.items():
        s = s.replace(m, k)
    if n: BRAND_LOG.append(n)
    return s


# ------------------------------------------------------------------ design DOM -> rich body
def ihtml(el):
    """Inner HTML with whitespace collapsed; drops SVGs and design-only classes/attributes on links."""
    for s in el.find_all('svg'): s.decompose()
    x = ''.join(str(c) for c in el.contents)
    return re.sub(r'\s+', ' ', x).strip()


def cls(el): return el.get('class') or []


def conv(el, trailing_ok=True):
    """One design component -> rich-body HTML."""
    c = cls(el)
    if 'mat-pills' in c:
        out = []
        for p in el.find_all(class_='mat-pill'):
            out.append(f'<a class="pill" href="{p["href"]}">{ihtml(p)}</a>' if p.name == 'a' else f'<span class="pill">{ihtml(p)}</span>')
        return '<p class="pills">' + ''.join(out) + '</p>'
    if 'ab-grid' in c:
        out = []
        for card in el.find_all(class_='ab-card', recursive=False):
            parts = []
            for k, tag in [('ab-card__meta', 'meta'), ('ab-card__title', 'h3'), ('ab-card__text', 'p'), ('ab-card__link', 'more')]:
                e = card.find(class_=k)
                if e is None: continue
                parts.append(f'<{tag}>{ihtml(e)}</{tag}>' if tag in ('h3', 'p') else f'<span class="{tag}">{ihtml(e)}</span>')
            inner_ = ''.join(parts)
            out.append(f'<li><a href="{card["href"]}">{inner_}</a></li>' if card.name == 'a' else f'<li>{inner_}</li>')
        # two card paddings in the designs: 24/24/26 (default) and 26/24 (`p26`), set inline per card
        p26 = any('padding:26px 24px' in (cd.get('style') or '') for cd in el.find_all(class_='ab-card', recursive=False))
        return f'<ul class="cards{" p26" if p26 else ""}">' + ''.join(out) + '</ul>'
    if el.name == 'ul' and 'ab-list' in c:
        narrow = ' narrow' if 'max-width:760px' in (el.get('style') or '') else ''
        return f'<ul class="check{narrow}">' + ''.join(f'<li>{ihtml(li.find("span") or li)}</li>' for li in el.find_all('li')) + '</ul>'
    if 'eyebrow' in c:
        return f'<p class="eb">{ihtml(el)}</p>'
    if el.name == 'p':
        body = ihtml(el)
        if trailing_ok and 'reveal' in c:
            # class from the design's inline style: 760px column -> note; 15px at 1.75 -> aside; else related
            st = el.get('style') or ''
            k = ('note' if 'max-width:760px' in st else 'aside' if 'line-height:1.75' in st
                 else 'related' if re.match(r'(Related:|See more|More examples)', el.get_text(' ', strip=True)) else 'note')
            return f'<p class="{k}">{body}</p>'
        return f'<p>{body}</p>'
    if el.name == 'div' and el.find(class_='ab-list'):
        return conv(el.find(class_='ab-list'))
    raise ValueError(f'unhandled component {el.name}.{c}')


def rich_of(els):
    return brand(''.join(conv(e) for e in els))


def kids(el): return [c for c in el.children if isinstance(c, Tag)]


def txt_(el): return brand(H.unescape(re.sub(r'\s+', ' ', el.get_text(' ', strip=True))).replace(' ,', ',').replace(' .', '.'))


# ------------------------------------------------------------------ builders
def frame_media(t, asset):
    return container([image(t('image', {'asset': asset}), css='selector img{display:block;width:100%;height:auto}')],
                     background_background='classic', background_color_hex='#0D1B2A', border_border='solid', border_width=box(1),
                     border_color=LINE, border_radius=box(18),
                     custom_css='selector{overflow:hidden;box-shadow:0 22px 58px rgba(15,42,68,.12)}' + COLS2.format(g=72))


def prose(t, eb, h2, body):
    return container([
        eyebrow(t, eb, margin=box(0, 0, 20, 0)),
        heading(t('heading', h2), 36, '600', tag='h2', color=INK, lh=41.4, ls=-0.72, _margin=box(0, 0, 18, 0)),
        # .ab-prose p keeps its 16px bottom margin on the last paragraph too, and wraps pretty
        rich_text(t, body, extra='selector p{text-wrap:pretty}selector p:not([class]):last-child{margin-bottom:16px}'),
    ], flex_direction='column', flex_align_items='stretch', flex_gap=gap(0), custom_css=COLS2.format(g=72))


def split_band(left, right, align='center'):
    return band([container([left, right], flex_direction='row', flex_wrap='wrap', flex_align_items=align, flex_gap=gap(48, 72))])


def media_grid(t, assets, note, cols=4):
    per = f'calc((100% - {(cols - 1) * 14}px) / {cols})'
    figs = [container([image(t('image', {'asset': a}), css='selector{margin:0;line-height:0}selector img{display:block;width:100%;aspect-ratio:4/3;height:auto;object-fit:cover}')],
                      background_background='classic', background_color_hex='#0D1B2A', border_border='solid', border_width=box(1),
                      border_color=LINE, border_radius=box(12), custom_css='selector{overflow:hidden}') for a in assets]
    g = container(figs, flex_direction='row', flex_wrap='wrap', flex_gap=gap(14, 14), width={'unit': '%', 'size': 100},
                  custom_css=f'selector > .e-con{{flex:0 0 {per} !important;max-width:{per} !important}}'
                             '@media(max-width:979px){selector > .e-con{flex:0 0 calc((100% - 14px) / 2) !important;max-width:calc((100% - 14px) / 2) !important}}')
    return [g, rich_text(t, note, extra='selector p.related,selector p.note{margin-top:0}', _margin=box(28, 0, 0, 0))]



def cta_display(t, eb, h2, body, b1, b2):
    """`.final-cta` as the Materials designs render it (453px at 1440+): solid #0D1B2A, 28px grid
    overlay at .5, 720px column, 56/600 title, 18px copy at .8 white, 15px pill buttons. The library
    cta-band-dark has the same tree but a gradient, a dashed eyebrow and a 38/800 title (463px)."""
    return container([container([
        heading(t('heading', eb), 12, '600', color='#FFFFFF', align='center', lh=24, ls=1.68, upper=True),
        heading(t('heading', h2), 56, '600', tag='h2', color='#FFFFFF', align='center', lh=58.8, ls=-1.4, _margin=box(20, 0, 20, 0)),
        text(t('body', body), 18, color='rgba(255,255,255,.8)', lh=29.7, align='center',
             _element_width='initial', _element_custom_width=px(600), _margin=box(0, 0, 32, 0)),
        container([
            button(t('button', b1[0]), t('url', b1[1]), size=15, pad=(15, 28), border='rgba(0,0,0,0)', shadow='0 8px 24px rgba(245,130,31,.3)'),
            button(t('button', b2[0]), t('url', b2[1]), bg='rgba(0,0,0,0)', size=15, pad=(15, 28), border='rgba(255,255,255,.32)'),
        ], flex_direction='row', flex_wrap='wrap', flex_justify_content='center', flex_align_items='center', flex_gap=gap(12, 12)),
    ], content_width='boxed', boxed_width=px(720), flex_direction='column', flex_align_items='center', flex_gap=gap(0))],
        background_background='classic', background_color_hex='#0D1B2A', padding=box(96, 24),
        custom_css='selector{position:relative;overflow:hidden}selector::before{content:"";position:absolute;inset:0;'
                   'background-image:linear-gradient(rgba(255,255,255,.043) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.043) 1px,transparent 1px);'
                   'background-size:28px 28px;opacity:.5;pointer-events:none}selector > .e-con-inner{position:relative}')

# ------------------------------------------------------------------ page walker
PAGES, MEDIA, SAVED = {}, {}, set()


def media(page, img):
    k = f'mat_{re.sub("[^a-z0-9]", "", page.lower())[:12]}_{len(MEDIA.setdefault(page, [])) + 1}'
    MEDIA[page].append((k, img['src'], H.unescape(img.get('alt', ''))))
    return k


def emit(page, pid, section, t):
    if pid not in SAVED:
        save(pid, section, t); SAVED.add(pid)
    PAGES.setdefault(page, []).append({'pattern': pid, 'values': dict(t.values)})


def head_of(sec):
    h = sec.find(class_='section__head')
    return txt_(h.find(class_='eyebrow')), txt_(h.find('h2')), h


def build_page(page):
    soup = BeautifulSoup(open(Z + f'Materials - {page}.html', encoding='utf-8').read(), 'html.parser')
    secs = soup.find('body').find_all('section', recursive=False)
    for sec in secs:
        c = cls(sec)
        if 'ab-hero' in c:
            t = Tok()
            hero_centered(t, txt_(sec.find(class_='hero__eyebrow')), txt_(sec.find('h1')), '<p>' + brand(ihtml(sec.find(class_='ab-hero__lede'))) + '</p>')
            PAGES.setdefault(page, []).append({'pattern': 'hero-dark-centered', 'values': dict(t.values)}); continue
        if 'final-cta' in c:
            btns = sec.find_all('a', class_='btn')
            t = Tok()
            emit(page, 'cta-band-dark-display', cta_display(t, txt_(sec.find(class_='eyebrow')), brand(ihtml(sec.find('h2'))),
                 '<p>' + brand(ihtml(sec.find('p'))) + '</p>', (txt_(btns[0]), btns[0]['href']), (txt_(btns[1]), btns[1]['href'])), t)
            continue
        cont = sec.find(class_='container')
        subtle = 'section--subtle' in c
        split_ = cont.find(class_='ab-split', recursive=False)
        if split_ is not None:
            parts = kids(split_)
            pr = [p for p in parts if 'ab-prose' in cls(p)][0]
            other = [p for p in parts if p is not pr][0]
            pk = kids(pr)
            eb, h2 = txt_(pk[0]), txt_(pk[1])
            body = rich_of(pk[2:])
            t = Tok()
            if other.find('img') is not None and other.find(class_='ab-list') is None:
                asset = media(page, other.find('img'))
                if parts.index(other) == 0:
                    emit(page, 'split-media-rich', split_band(frame_media(t, asset), prose(t, eb, h2, body)), t)
                else:
                    emit(page, 'split-rich-media', split_band(prose(t, eb, h2, body), frame_media(t, asset)), t)
            else:  # prose | list, then the trailing related line below the split
                right = rich_of([other])
                after = [e for e in kids(cont) if e is not split_]
                rel = rich_of(after)
                left = prose(t, eb, h2, body)
                rc = container([rich_text(t, right)], flex_direction='column', custom_css=COLS2.format(g=72))
                row = container([left, rc], flex_direction='row', flex_wrap='wrap', flex_align_items='flex-start', flex_gap=gap(48, 72))
                emit(page, 'split-rich-rich-related', band([row, rich_text(t, rel, extra='selector p.related{margin-top:0}', _margin=box(36, 0, 0, 0))]), t)
            continue
        if cont.find(class_='mat-tabs') is not None:
            eb, h2, hd = head_of(sec)
            t = Tok()
            tabs = cont.find(class_='mat-tabs').find_all('button')
            markup = ''.join(f'<button type="button" role="tab" aria-selected="{"true" if i == 0 else "false"}">{ihtml(b)}</button>' for i, b in enumerate(tabs))
            panels = cont.find_all(class_='mat-panel')
            note = rich_of([p for p in kids(cont) if p.name == 'p'])
            head = section_head(t, eb, h2, mb=48)
            TABS = ('<div class="pl-tabs" role="tablist">{embed_1}</div><style>.pl-tabs{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;margin:0 0 24px}'
                    '.pl-tabs button{border:1.5px solid #DCE1EA;background:#fff;border-radius:9999px;padding:10px 18px;font:700 13px/19.5px Inter,system-ui,sans-serif;'
                    'color:#6B7280;cursor:pointer;transition:all .25s cubic-bezier(.25,.46,.45,.94)}.pl-tabs button:hover{border-color:#F5821F;color:#15253D}'
                    '.pl-tabs button[aria-selected="true"]{background:#F5821F;border-color:#F5821F;color:#fff}</style>'
                    '<script>(function(){var g=document.currentScript.previousElementSibling.previousElementSibling,s=g;'
                    'while(s.parentElement&&!s.parentElement.hasAttribute("data-elementor-id"))s=s.parentElement;'
                    'function show(i){var p=s.querySelectorAll(".pl-tab-panel");p.forEach(function(x,j){x.style.display=j===i?"flex":"none";});'
                    'g.querySelectorAll("button").forEach(function(b,j){b.setAttribute("aria-selected",j===i?"true":"false");});}'
                    'g.querySelectorAll("button").forEach(function(b,i){b.addEventListener("click",function(){show(i);});});'
                    'document.addEventListener("DOMContentLoaded",function(){show(0);});show(0);})();</script>')
            tw = {'id': 'ccccccc', 'elType': 'widget', 'widgetType': 'html', 'settings': {'html': TABS.replace('{embed_1}', t('embed', markup))}, 'elements': []}
            pans = [container([heading(t('heading', txt_(p.find('h3'))), 22.4, '700', tag='h3', color=NAVY, lh=29.12, ls=-0.448, _margin=box(0, 0, 12, 0)),
                               text(t('body', '<p>' + brand(ihtml(p.find('p'))) + '</p>'), 15.5, color='#3C4858', lh=27.125)],
                              css_classes='pl-tab-panel', flex_direction='column', flex_gap=gap(0), padding=box(28, 30),
                              background_background='classic', background_color_hex='#FFFFFF', border_border='solid', border_width=box(1),
                              border_color=LINE, border_radius=box(18),
                              custom_css=('selector{box-shadow:0 2px 8px rgba(0,0,0,.07)}' + ('' if i == 0 else 'selector{display:none}')))
                    for i, p in enumerate(panels)]
            col = container([tw] + pans + [rich_text(t, note, extra='selector p.related,selector p.note{margin-top:0}selector p{line-height:26.25px}', _margin=box(28, 0, 0, 0))],
                            flex_direction='column', flex_gap=gap(0), width=px(912), width_mobile={'unit': '%', 'size': 100})
            emit(page, 'tabs-panels-6-note', band([head, col], bg=SUBTLE, align='center'), t)
            continue
        if cont.find(class_='mat-media-grid') is not None:
            eb, h2, hd = head_of(sec)
            t = Tok()
            head = section_head(t, eb, h2, mb=48)
            assets = [media(page, i) for i in cont.find(class_='mat-media-grid').find_all('img')]
            note = rich_of([p for p in kids(cont) if p.name == 'p'])
            emit(page, f'media-grid-{len(assets)}-note', band([head] + media_grid(t, assets, note), bg=SUBTLE, align='center'), t)
            continue
        grid_ = cont.find(class_='ab-grid', recursive=False)
        if grid_ is not None and grid_.find('figure') is not None:
            t = Tok()
            cards = []
            for fg in grid_.find_all('figure'):
                a = media(page, fg.find('img'))
                cards.append(card([
                    image(t('image', {'asset': a}), css='selector{margin:0;background:#0D1B2A}selector img{display:block;width:100%;aspect-ratio:16/10;height:auto;object-fit:cover}'),
                    container([text(t('body', '<p>' + brand(ihtml(fg.find('figcaption'))) + '</p>'), 14, color=BODY, lh=23.1)],
                              flex_direction='column', padding=box(20, 22, 24, 22)),
                ], box(0), 0))
            note = rich_of([p for p in kids(cont) if p.name == 'p'])
            emit(page, 'figure-cards-2-note', band([grid(cards, 2), rich_text(t, note, extra='selector p.related,selector p.note{margin-top:0}', _margin=box(28, 0, 0, 0))], bg=SUBTLE), t)
            continue
        if cont.find(class_='section__head') is not None:
            eb, h2, hd = head_of(sec)
            t = Tok()
            head = section_head(t, eb, h2, mb=48)
            comps = [e for e in kids(cont) if e is not hd]
            body = rich_of(comps)
            extra = 'selector p.pills{justify-content:center}'
            emit(page, 'head-rich-subtle' if subtle else 'head-rich-white',
                 band([head, container([rich_text(t, body, extra=extra)], width={'unit': '%', 'size': 100})], bg=SUBTLE if subtle else '#FFFFFF', align='center'), t)
            continue
        # a lone trailing line (Foils): white band, no head, 0/24/80 padding
        t = Tok()
        body = rich_of(kids(cont))
        emit(page, 'rich-band-white', container([container([rich_text(t, body, extra='selector p.related{margin-top:0}')], content_width='boxed',
                                                            flex_direction='column', flex_gap=gap(0))],
                                                 flex_direction='column', flex_align_items='center', padding=box(0, 24, 80, 24),
                                                 background_background='classic', background_color_hex='#FFFFFF'), t)


ORDER = ['Materials', 'Adhesives', 'Glass', 'Kapton Polyimide', 'Metal Parts', 'Plastic Micromachining', 'Polymers', 'Stainless Steel', 'Thin Metal Foils']
for p in ORDER:
    build_page(p)
json.dump(PAGES, open(os.path.join(OUT, 'materials.pages.json'), 'w'), indent=1, ensure_ascii=False)
json.dump(MEDIA, open(os.path.join(OUT, 'materials.media.json'), 'w'), indent=1, ensure_ascii=False)
for p in ORDER:
    print(p.ljust(24), ' '.join(s['pattern'] for s in PAGES[p]))
print('patterns minted:', sorted(SAVED)); print('images:', sum(len(v) for v in MEDIA.values()), '| brand swaps in', len(BRAND_LOG), 'strings')
