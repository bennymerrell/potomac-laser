"""§7.2 AUTHOR — Services & Applications (run 20260924-125928).

  hero-dark-centered-meta-4-bold  `.sa-hero`: 900px column, bold 56px H1, orange eyebrow, 4 meta stats
  service-cards-5-caps            head + 5 whole-card links (4:3 image) + capability pills + 1 button
  service-cards-6-button          head + 6 whole-card links (16:10 image) in 3 columns + 1 button
  estimate-band-split             mid-page dark gradient band: copy left | 2 buttons right
  feature-cards-2-image           two feature cards (light | dark) with faded background photos

Measured off the design mock at 1440px; copy extracted from the design HTML.
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from about_shared import *  # noqa

C = json.load(open(os.path.join(OUT, 'sa.cards.json')))
SA_GLOW = ('background-image:radial-gradient(ellipse at 28% 0%,rgba(245,130,31,0.16) 0%,transparent 58%),'
           'radial-gradient(ellipse at 92% 100%,rgba(14,99,168,0.22) 0%,transparent 55%),'
           'linear-gradient(rgba(255,255,255,0.04) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,0.04) 1px,transparent 1px);'
           'background-size:auto,auto,32px 32px,32px 32px;')

# ------------------------------------------------------------------ hero-dark-centered-meta-4-bold
t = Tok()
META = [('12', 'Capabilities'), ('1 µm', 'Smallest feature'), ('±10 µm', 'Typical tolerance'), ('Est. 1982', 'Micromanufacturing')]
kids = [
    eyebrow(t, 'Services &amp; Applications', align='center'),
    heading(t('heading', 'Precision micromanufacturing for demanding applications'), 56, '700', tag='h1', color='#FFFFFF',
            align='center', lh=58.8, ls=-1.12, _margin=box(24, 0, 18, 0),  # 24px eyebrow line box + 18 − 18 (12371 iter 1: +18)
            css='selector .elementor-heading-title{max-width:20ch;margin:0 auto}'),
    text(t('body', '<p>A comprehensive range of micromanufacturing services tailored to your exact needs, from precision '
                   'small-hole drilling to features as small as <strong>1 micron</strong>. Our technologies support '
                   'everything from <strong>aerospace components</strong> to fully fabricated <strong>microfluidic '
                   'devices</strong> advancing biotech and medical diagnostics.</p>'),
         18, color='rgba(255,255,255,0.76)', lh=30.6, align='center',
         extra_css='selector p{max-width:772px;margin:0 auto}selector strong{color:#fff;font-weight:600}'),
    container([container([
        heading(t('heading', num), 28, '700', color='#FFFFFF', align='center', lh=42, ls=-0.28),
        heading(t('heading', lab), 12, '600', color='rgba(255,255,255,0.55)', align='center', lh=18, ls=1.2, upper=True),
    ], flex_direction='column', flex_align_items='center', flex_gap=gap(4), custom_css='selector{width:auto;flex:0 0 auto}')
        for num, lab in META],
        flex_direction='row', flex_wrap='wrap', flex_justify_content='center', flex_align_items='flex-start',
        flex_gap=gap(32, 32), _margin=box(34, 0, 0, 0)),
]
save('hero-dark-centered-meta-4-bold', container([
    container(kids, content_width='boxed', flex_direction='column', flex_align_items='center', flex_gap=gap(0), boxed_width=px(900)),
], flex_direction='column', flex_align_items='center', padding=box(76, 24, 64, 24), background_background='classic',
   background_color_hex='#0D1B2A', custom_css='selector{overflow:hidden;' + SA_GLOW + '}'), t)


# ------------------------------------------------------------------ shared service card
def svc_card(t, asset, c, ratio):
    return card([
        container([image(t('image', {'asset': asset}),
                         css='selector{margin:0;position:absolute!important;inset:0;width:100%}selector img{width:100%;height:100%;object-fit:cover;'
                             'transition:transform .45s cubic-bezier(.25,.46,.45,.94)}')],
                  custom_css=f'selector{{position:relative;aspect-ratio:{ratio};overflow:hidden;background:#FEF9F5;border-bottom:1px solid #DCE1EA}}'),
        container([
            heading(t('heading', c['title']), 18, '600', tag='h3', color=INK, lh=23.4, ls=-0.18),
            text(t('body', f'<p>{c["text"]}</p>'), 14, color=MUTED, lh=21.7, extra_css='selector{flex:1 1 auto}'),
            heading(t('heading', c['label']), 13, '600', color='#F5821F', lh=19.5, _margin=box(4, 0, 0, 0)),
        ], flex_direction='column', flex_gap=gap(12), padding=box(24), custom_css='selector{flex:1 1 auto}'),
    ], box(0), 0, html_tag='a', link={'url': t('url', c['href']), 'is_external': '', 'nofollow': ''},
       extra_css=('selector{text-decoration:none;color:inherit;box-shadow:none;transition:border-color .25s,box-shadow .25s,transform .15s}'
                  'selector:hover{border-color:#F5821F;box-shadow:0 4px 12px rgba(15,22,32,.08);transform:translateY(-2px)}'
                  'selector:hover .elementor-widget-image img{transform:scale(1.04)}'))


def head(t, eb, h2, lede):
    kids = [eyebrow(t, eb, align='center'),
            heading(t('heading', h2), 40, '600', tag='h2', color=INK, align='center', lh=44.8, ls=-0.8, _margin=box(18, 0, 16, 0)),
            text(t('body', f'<p>{lede}</p>'), 18, color=MUTED, lh=29.7, align='center')]
    return container(kids, flex_direction='column', flex_align_items='center', flex_gap=gap(0), width=px(760),
                     width_mobile={'unit': '%', 'size': 100}, _margin=box(0, 0, 48, 0))


def center_button(t, label, href, top):
    return container([button(t('button', label), t('url', href), bg='#FFFFFF', fg='#F5821F', border='#F5821F', size=15, pad=(15, 28))],  # btn--lg
                     flex_direction='row', flex_justify_content='center',
                     width={'unit': '%', 'size': 100}, _margin=box(top, 0, 0, 0))


# ------------------------------------------------------------------ service-cards-5-caps
t = Tok()
CAPS = ('<p><a href="/services/laser-cutting/">Laser Cutting</a><a href="/services/laser-micromachining-welding/">Laser Micro Welding</a>'
        '<a href="/services/laser-marking-applications/">Laser Marking</a><a href="/services/laser-patterning/">Laser Patterning</a>'
        '<a href="/services/3d-printing/">Micro 3D Printing</a><a href="/services/hot-embossing/">Hot Embossing</a>'
        '<a href="/services/bonding-assembly/">Bonding &amp; Assembly</a></p>')
CAPS_CSS = ('selector p{display:flex;flex-wrap:wrap;gap:10px;justify-content:center;margin:0}'
            'selector a{display:inline-flex;align-items:center;gap:8px;padding:10px 18px;border-radius:999px;border:1px solid #DCE1EA;'
            'background:#fff;color:#0F1620;font:600 14px/21px Inter,system-ui,sans-serif;text-decoration:none;transition:border-color .15s,color .15s,background .15s,transform .15s}'
            "selector a::after{content:'→';color:#F5821F;font-weight:700;transform:translateX(-2px);opacity:0;transition:opacity .15s,transform .15s}"
            'selector a:hover{border-color:#F5821F;color:#F5821F;background:#FFF7F0;transform:translateY(-1px)}selector a:hover::after{opacity:1;transform:translateX(0)}')
kids = [head(t, 'Our Services', 'Check out our growing list of capabilities',
             'We are innovators at our core, constantly evolving to meet market demands and pioneering new micro-manufacturing technologies.'),
        grid([svc_card(t, f'sa_svc_{i + 1}', c, '4/3') for i, c in enumerate(C['svc'])], 5),
        text(t('body', CAPS), 14, color=INK, lh=21, extra_css=CAPS_CSS, _margin=box(32, 0, 0, 0)),
        center_button(t, 'View all services', '/services/', 36)]
sec = band(kids, align='center')
sec['elements'][0]['elements'][1]['settings']['custom_css'] = sec['elements'][0]['elements'][1]['settings']['custom_css'].replace(
    '@media(max-width:979px){selector > .e-con{flex:0 0 100% !important;max-width:100% !important}}',
    '@media(max-width:1179px){selector > .e-con{flex:0 0 calc((100% - 40px) / 3) !important;max-width:calc((100% - 40px) / 3) !important}}'
    '@media(max-width:859px){selector > .e-con{flex:0 0 calc((100% - 20px) / 2) !important;max-width:calc((100% - 20px) / 2) !important}}'
    '@media(max-width:559px){selector > .e-con{flex:0 0 100% !important;max-width:100% !important}}')
save('service-cards-5-caps', sec, t)

# ------------------------------------------------------------------ service-cards-6-button
t = Tok()
kids = [head(t, 'Our Applications', 'Changing the world one micron at a time',
             'Our customers span many industries: medical device, biotech, semiconductor, automotive, aerospace and more.'),
        grid([svc_card(t, f'sa_app_{i + 1}', c, '16/10') for i, c in enumerate(C['app'])], 3),
        center_button(t, 'View all applications', '/applications/', 40)]
save('service-cards-6-button', band(kids, bg=SUBTLE, align='center'), t)

# ------------------------------------------------------------------ estimate-band-split
t = Tok()
left = container([
    heading(t('heading', 'Get an estimate'), 12, '600', color='#FFFFFF', lh=18, ls=1.68, upper=True),
    heading(t('heading', 'Submit your drawing, get a quick estimate'), 38.4, '700', tag='h2', color='#FFFFFF', lh=46.08, ls=-0.576,
            _margin=box(14, 0, 10, 0)),  # 8 + the eyebrow's 24px line box
    text(t('body', "<p>Send us your CAD or drawing and see if we're the right fit. Our engineers review every design for "
                   'manufacturability and respond within one business day.</p>'), 16, color='rgba(255,255,255,0.78)', lh=26.4,
         extra_css='selector p{max-width:525px}'),
], flex_direction='column', flex_align_items='flex-start', flex_gap=gap(0), custom_css='selector{flex:1 1 520px;width:auto}')
right = container([
    button(t('button', 'Request a quote'), t('url', 'Services - CNC Micromachining.html#quote'), size=15, pad=(15, 28),
           shadow='0 8px 24px rgba(245,130,31,.3)', css='selector .elementor-button{border:1px solid transparent}'),
    button(t('button', 'Contact us'), t('url', '/contact/'), bg=None, fg='#FFFFFF', size=15, pad=(15, 28),
           border='rgba(255,255,255,0.32)', css='selector .elementor-button{background:transparent}'),
], flex_direction='row', flex_wrap='wrap', flex_gap=gap(12, 12), custom_css='selector{width:auto;flex:0 0 auto}')
save('estimate-band-split', container([
    container([left, right], content_width='boxed', boxed_width=px(1152), flex_direction='row', flex_wrap='wrap',
              flex_justify_content='space-between', flex_align_items='center', flex_gap=gap(28, 28)),
], flex_direction='column', flex_align_items='center', padding=box(56, 24),
   custom_css=('selector{background-image:linear-gradient(rgba(255,255,255,0.04) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,0.04) 1px,transparent 1px),'
               'linear-gradient(135deg,#16253D 0%,#1B2E4A 55%,#213754 100%);background-size:40px 40px,40px 40px,auto}')), t)

# ------------------------------------------------------------------ feature-cards-2-image
t = Tok()


def feat(asset, eb, title, body, label, href, dark):
    tc, bc = ('#FFFFFF', 'rgba(255,255,255,0.78)') if dark else (INK, '#3C4858')
    btn = (button(t('button', label), t('url', href), bg=None, fg='#FFFFFF', border='rgba(255,255,255,0.32)',
                  css='selector .elementor-button{background:transparent}')
           if dark else button_secondary(t, label, href))
    return container([
        image(t('image', {'asset': asset}),
              css=('selector{position:absolute!important;inset:0;margin:0;width:100%;height:100%;z-index:0}'
                   f'selector img{{width:100%;height:100%;object-fit:cover;opacity:{".28;mix-blend-mode:screen" if dark else ".16"}}}')),
        container([
            eyebrow(t, eb, color='#FFFFFF' if dark else '#F5821F'),
            heading(t('heading', title), 28, '700', tag='h3', color=tc, lh=36.4, ls=-0.42, _margin=box(10, 0, 12, 0)),
            text(t('body', f'<p>{body}</p>'), 16, color=bc, lh=27.2, _margin=box(0, 0, 24, 0), extra_css='selector p{max-width:464px}'),
            container([btn], custom_css='selector{margin-top:auto;width:auto}'),
        ], flex_direction='column', flex_align_items='flex-start', flex_gap=gap(0), custom_css='selector{position:relative;z-index:1;flex:1 1 auto}'),
    ], flex_direction='column', flex_gap=gap(0), padding=box(40), background_background='classic',
       background_color_hex='#0D1B2A' if dark else SUBTLE, border_border='solid', border_width=box(1),
       border_color='rgba(0,0,0,0)' if dark else LINE, border_radius=box(16),
       custom_css='selector{position:relative;overflow:hidden;min-height:320px}')


cards = [feat('sa_feat_1', 'Materials', 'Everything you need for your business',
              'The best parts start with the best materials. As part of the Goodfellow family, a global leader in high-quality '
              'material supply, we draw on an extensive range of superior materials, enhancing our precision microfabrication '
              'with 170,000+ grades.', 'Learn more', '/materials/', False),
         feat('sa_feat_2', 'Industries', 'Trusted since 1982',
              'Recognised by commercial and government agencies alike for innovative contributions to medical device '
              'manufacturing, biotech and electronics fabrication, from our high-tech facility at bwtech@UMBC Research and '
              'Technology Park in Baltimore, MD.', 'Learn more', 'About - About Our Group.html', True)]
sec = band([grid(cards, 2, g=24)])
sec['elements'][0]['elements'][0]['settings']['custom_css'] = sec['elements'][0]['elements'][0]['settings']['custom_css'].replace('979px', '899px')
save('feature-cards-2-image', sec, t)
print('ok')
