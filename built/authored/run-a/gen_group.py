"""§7.2 AUTHOR — the two UNMATCHED sections of `About - About Our Group.html`.

Writes, for each candidate:
  built/authored/run-a/candidates/<id>.json          tokenised section (the would-be fragment)
  built/authored/run-a/candidates/<id>.values.json   this page's token values, in token order

Every style value below was read off the design mock at 1440px with getComputedStyle
(run 20260924-100754); none is guessed. Candidates are NOT library fragments until they
pass 3.c.vi and are re-tokenised server-side from the built post (§7.3–7.4).
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from elb import *  # noqa

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'candidates')
os.makedirs(OUT, exist_ok=True)

INK = '#0F1620'      # --fg-1, no Kit token
MUTED = '#65718A'    # --fg-3, no Kit token
LINE = '#DCE1EA'     # --border-1, no Kit token
SUBTLE = '#F6F8FB'   # --bg-subtle, no Kit token
GRID_BG = ('background-image:radial-gradient(ellipse at 30% 0%,rgba(14,99,168,0.28) 0%,transparent 60%),'
           'radial-gradient(ellipse at 90% 100%,rgba(148,18,82,0.16) 0%,transparent 55%),'
           'linear-gradient(rgba(255,255,255,0.04) 1px,transparent 1px),'
           'linear-gradient(90deg,rgba(255,255,255,0.04) 1px,transparent 1px);'
           'background-size:auto,auto,32px 32px,32px 32px;')


def save(pid, section, tok):
    with open(os.path.join(OUT, pid + '.json'), 'w') as f:
        json.dump([section], f, indent=1, ensure_ascii=False)
    with open(os.path.join(OUT, pid + '.values.json'), 'w') as f:
        json.dump(tok.values, f, indent=1, ensure_ascii=False)


# ---------------------------------------------------------------- legend-cards-dark
# Row anchors are fixed in the fragment (split-row-1..4): the placeholder vocabulary has no
# anchor token, so the legend links point at them via {url_n} rather than at #goodfellow etc.
LEGEND = [('#split-row-1', '#F5821F', 'Goodfellow', 'Advanced Materials'),
          ('#split-row-2', '#F5821F', 'Goodfellow Microfabrication', 'Microfabrication'),
          ('#split-row-3', '#1A71AB', 'Suisse TP', 'Analytics &amp; Materials'),
          ('#split-row-4', '#F08423', 'BAS', 'Reference Materials')]

t = Tok()
head = container([
    heading(t('heading', 'Why Us'), 12, '600', color='#F5821F', align='center', lh=18, ls=1.68, upper=True),
    heading(t('heading', 'Four specialist brands. One Goodfellow Group.'), 40, '600', tag='h2',
            color='#FFFFFF', align='center', lh=44.8, ls=-0.8, _margin=box(12, 0, 16, 0)),
    text(t('body', '<p>We deliver high-quality scientific materials and services across a wide range of '
                   'industries and applications. Together, Goodfellow, Goodfellow Microfabrication, Suisse '
                   'Technology Partners and the Bureau of Analysed Samples, we drive innovation from concept '
                   'to market, becoming your one-stop shop for scientific and industrial material needs.</p>'),
         18, color='rgba(255,255,255,0.74)', lh=29.7, align='center'),
], flex_direction='column', flex_align_items='center', flex_gap=gap(0),
   width=px(760), width_mobile={'unit': '%', 'size': 100})

cards = []
for href, dotc, name, role in LEGEND:
    cards.append(container([
        container([dot(dotc, 11),
                   heading(t('heading', name), 18, '600', color=INK, lh=27, ls=-0.18)],
                  flex_direction='row', flex_align_items='center', flex_gap=gap(9, 9)),
        heading(t('heading', role), 13, '600', color=MUTED, lh=19.5, ls=1.04, upper=True),
    ], html_tag='a', link={'url': t('url', href), 'is_external': '', 'nofollow': ''},
       flex_direction='column', flex_align_items='stretch', flex_gap=gap(6),
       padding=box(18, 20), background_background='classic', background_color_hex='#FFFFFF',
       border_border='solid', border_width=box(1), border_color=LINE, border_radius=box(8),
       width={'unit': '%', 'size': 23.9}, width_mobile={'unit': '%', 'size': 100},
       custom_css=('selector{flex:0 0 calc((100% - 42px) / 4) !important;max-width:calc((100% - 42px) / 4) !important;'
                   'text-decoration:none;transition:box-shadow .25s cubic-bezier(.25,.46,.45,.94),'
                   'transform .25s cubic-bezier(.25,.46,.45,.94),border-color .25s cubic-bezier(.25,.46,.45,.94)}'
                   'selector:hover{transform:translateY(-2px);box-shadow:0 4px 12px rgba(15,22,32,.08);border-color:#C3CBD8}'
                   '@media(max-width:879px){selector{flex:0 0 calc((100% - 14px) / 2) !important;max-width:calc((100% - 14px) / 2) !important}}')))

legend = container([
    container([head, container(cards, flex_direction='row', flex_align_items='stretch',
                               flex_gap=gap(14, 14), flex_wrap='wrap', width={'unit': '%', 'size': 100},
                               _margin=box(48, 0, 0, 0))],  # design: head margin-bottom 48; the legend's own 40 top margin does not apply
              content_width='boxed', flex_direction='column', flex_align_items='center', flex_gap=gap(0)),
], flex_direction='column', flex_align_items='center', padding=box(80, 24),
   background_background='classic', background_color_hex='#0D1B2A',
   custom_css='selector{' + GRID_BG + '}')
save('legend-cards-dark', legend, t)


# ---------------------------------------------------- split-rows-logo-alternating
ROWS = [
    dict(accent='#F5821F', logo='GF-Linear-logo', founded='Since 1946', eyebrow='Advanced Materials',
         title='Goodfellow',
         lead='A global leader in the supply of high-quality advanced materials, serving science and industry for over 75 years.',
         body='With a vast range of over 170,000 products, including metals, alloys, ceramics, polymers and compounds, '
              'Goodfellow is dedicated to driving innovation and solving technical challenges. Our commitment to '
              'excellence is reflected in extensive product offerings and a customer-focused approach, making us a '
              'trusted partner for researchers and engineers worldwide.',
         stats=['<strong>170,000+</strong> materials', '<strong>75+</strong> years', '<strong>ISO 9001</strong> quality assured'],
         btn='Visit Goodfellow →', url='https://www.goodfellow.com/', anchor='goodfellow'),
    dict(accent='#F5821F', logo='Potomac_Master_AGC', founded='Since 1982', eyebrow='Microfabrication',
         title='Goodfellow Microfabrication',
         lead='One of the US leaders in microfabrication and digital manufacturing, rapid prototyping through full-scale production of precision devices.',
         body='Since 1982, the Baltimore-based Goodfellow Microfabrication team (formerly Potomac Photonics) has been at '
              'the forefront of innovation in medical-device manufacturing, biotech and electronics fabrication. By '
              'leveraging advanced laser and CNC technologies, the team delivers high-quality, cost-effective solutions '
              'that carry your project from concept to market.',
         stats=['<strong>±10 µm</strong> tolerances', '<strong>40+</strong> years', '<strong>Prototype → production</strong>'],
         btn='Explore microfabrication →', url='Services - CNC Micromachining.html', anchor='potomac'),
    dict(accent='#1A71AB', logo='STP_Master_AGC', founded='Swiss labs', eyebrow='Analytics &amp; Materials',
         title='Suisse Technology Partners',
         lead='A Swiss competence centre for material-based solutions and analytics, ensuring safe and innovative products for industrial customers.',
         body='STP provides specialised services in materials and surface technology. Their expertise spans technical '
              'safety, chemical analytics and packaging development, supported by certified and accredited '
              'laboratories. An interdisciplinary approach drives progress and innovation across every engagement.',
         stats=['<strong>Accredited</strong> laboratories', '<strong>Surface</strong> technology', '<strong>Failure</strong> investigation'],
         btn='Visit Suisse TP →', url='https://suisse-tp.ch/', anchor='suisse'),
    dict(accent='#F08423', logo='BAS_AGC_Full', founded='Since 1935', eyebrow='Reference Materials',
         title='The Bureau of Analysed Samples',
         lead='A renowned provider of Certified Reference Materials (CRMs) for chemical and spectroscopic analysis.',
         body='Established in 1935, BAS continues the legacy of the British Chemical Standards movement, offering a wide '
              'range of materials for the iron and steel industry. Their CRMs are essential for ensuring accuracy and '
              'reliability in laboratory testing, making BAS a trusted partner for quality assurance across many industries.',
         stats=['<strong>Since 1935</strong>', '<strong>Certified</strong> reference materials', '<strong>Iron &amp; steel</strong> standards'],
         btn='Visit BAS →', url='https://www.basrid.co.uk/', anchor='bas'),
]
ASSET = {'GF-Linear-logo': 'group_logo_goodfellow', 'Potomac_Master_AGC': 'group_logo_microfab',
         'STP_Master_AGC': 'group_logo_stp', 'BAS_AGC_Full': 'group_logo_bas'}

t = Tok()
COL = {'unit': '%', 'size': 47}
COL_CSS = 'selector{flex:0 0 calc((100% - 72px) / 2) !important;max-width:calc((100% - 72px) / 2) !important}' \
          '@media(max-width:979px){selector{flex:0 0 100% !important;max-width:100% !important}}'
rows = []
for i, r in enumerate(ROWS):
    visual = container([
        image(t('image', {'asset': ASSET[r['logo']]}),
              css='selector{width:78%;text-align:center}selector img{max-width:100%;max-height:155px;'
                  'width:auto;height:auto;object-fit:contain;display:inline-block}'),
        heading(t('heading', r['founded']), 12, '400', color=MUTED, lh=18, ls=0.48,
                css=f'selector{{position:absolute;right:16px;bottom:14px;width:auto}}'
                    f'selector .elementor-heading-title{{font-family:"JetBrains Mono",ui-monospace,"SF Mono",Menlo,monospace;'
                    f'background:{SUBTLE};border:1px solid {LINE};border-radius:999px;padding:4px 11px}}'),
    ], flex_direction='column', flex_justify_content='center', flex_align_items='center',
       padding=box(48), background_background='classic', background_color_hex='#FFFFFF',
       border_border='solid', border_width=box(1), border_color=LINE, border_radius=box(16),
       width=COL, width_mobile={'unit': '%', 'size': 100},
       custom_css=COL_CSS + f'selector{{position:relative;aspect-ratio:16/10;overflow:hidden;'
                            f'box-shadow:0 1px 2px rgba(15,22,32,.06),0 1px 1px rgba(15,22,32,.04)}}'
                            f'selector::before{{content:"";position:absolute;top:0;left:0;right:0;height:4px;background:{r["accent"]}}}')
    copy = container([
        container([dot(r['accent'], 9),
                   heading(t('heading', r['eyebrow']), 12, '600', color=r['accent'], lh=18, ls=1.44, upper=True)],
                  flex_direction='row', flex_align_items='center', flex_gap=gap(10, 10), _margin=box(0, 0, 14, 0)),
        heading(t('heading', r['title']), 36, '600', tag='h2', color=INK, lh=39.6, ls=-0.72, _margin=box(0, 0, 8, 0)),
        text(t('body', f'<p>{r["lead"]}</p>'), 16, color=INK, weight='600', lh=24.8, _margin=box(0, 0, 12, 0)),
        text(t('body', f'<p>{r["body"]}</p>'), 16, color='#3C4858', lh=27.2, _margin=box(0, 0, 22, 0)),
        container([text(t('body', f'<p>{s}</p>'), 14, color='#3C4858', lh=21,
                        extra_css=f'selector{{width:auto;background:{SUBTLE};border:1px solid {LINE};border-radius:999px;padding:6px 13px}}'
                                  f'selector strong{{font-weight:600;color:{INK}}}')
                   for s in r['stats']],
                  flex_direction='row', flex_wrap='wrap', flex_align_items='center', flex_gap=gap(10, 10),
                  _margin=box(0, 0, 24, 0)),
        button(t('button', r['btn']), t('url', r['url']), shadow='0 8px 24px rgba(245,130,31,.3)'),
    ], flex_direction='column', flex_align_items='flex-start', flex_gap=gap(0),
       width=COL, width_mobile={'unit': '%', 'size': 100}, custom_css=COL_CSS)
    rows.append(container([visual, copy], _element_id=f'split-row-{i + 1}',
                          flex_direction='row-reverse' if i % 2 else 'row', flex_direction_mobile='column',
                          flex_align_items='center', flex_gap=gap(40, 72), flex_wrap='wrap'))

split = container([
    container(rows, content_width='boxed', flex_direction='column', flex_align_items='stretch', flex_gap=gap(96, 0)),
], flex_direction='column', flex_align_items='center', padding=box(80, 24),
   background_background='classic', background_color_hex='#FFFFFF')
save('split-rows-logo-alternating', split, t)
print('ok')
