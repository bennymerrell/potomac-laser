"""§7.2 AUTHOR — the five UNMATCHED sections of `About - About Potomac.html`.

Same contract as gen_group.py: every style value was read off the design mock at 1440px
with getComputedStyle (run 20260924-100754). Writes candidates/<id>.json + .values.json.

Brand normalisation (TRANSLATE.md §6) is applied to PRESENT-TENSE brand references only.
Past-tense history that names the old company is kept verbatim and listed in the report:
Mike Davis's bio ("joined Potomac…", "led Potomac to ISO 9001:2000…", "Potomac's laser
technologies"). Rewriting those would change what the sentences claim happened.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from elb import *  # noqa
from gen_group import save, INK, MUTED, LINE, SUBTLE, GRID_BG  # noqa  (re-running gen_group is harmless)

NAVY = '#15253D'      # gfnavy — card titles, stat values, card links
BODY = '#6B7280'      # gfbody — card text
CARD_SHADOW = '0 2px 8px rgba(0,0,0,.07)'


def eyebrow(t, value, align=None, ls=1.68, margin=None):
    kw = {'_margin': margin} if margin else {}
    return heading(t('heading', value), 12, '600', color='#F5821F', align=align, lh=18, ls=ls, upper=True, **kw)


def section_head(t, eb, h2):
    """Centred eyebrow + H2, no lede — the About pages' `.section__head`."""
    return container([
        eyebrow(t, eb, align='center'),
        heading(t('heading', h2), 40, '600', tag='h2', color=INK, align='center', lh=44.8, ls=-0.8,
                _margin=box(18, 0, 0, 0)),  # design: 12px margin + the eyebrow's 24px line box
    ], flex_direction='column', flex_align_items='center', flex_gap=gap(0), width=px(760),
       width_mobile={'unit': '%', 'size': 100}, _margin=box(0, 0, 48, 0))


def band(children, bg='#FFFFFF', align='stretch'):
    return container([
        container(children, content_width='boxed', flex_direction='column', flex_align_items=align, flex_gap=gap(0)),
    ], flex_direction='column', flex_align_items='center', padding=box(80, 24),
       background_background='classic', background_color_hex=bg)


def grid(cards, n, g=20, mobile_n=1):
    per = f'calc((100% - {(n - 1) * g}px) / {n})'
    css = (f'selector > .e-con{{flex:0 0 {per} !important;max-width:{per} !important}}'
           f'@media(max-width:979px){{selector > .e-con{{flex:0 0 100% !important;max-width:100% !important}}}}')
    return container(cards, flex_direction='row', flex_wrap='wrap', flex_align_items='stretch',
                     flex_gap=gap(g, g), width={'unit': '%', 'size': 100}, custom_css=css)


def card(children, pad, g, extra_css=''):
    return container(children, flex_direction='column', flex_align_items='stretch', flex_gap=gap(g),
                     padding=pad, background_background='classic', background_color_hex='#FFFFFF',
                     border_border='solid', border_width=box(1), border_color=LINE, border_radius=box(8),
                     custom_css=f'selector{{box-shadow:{CARD_SHADOW};overflow:hidden}}' + extra_css)


# ------------------------------------------------------------ hero-dark-centered-meta
t = Tok()
META = [('1982', 'Founded'), ('5K+', 'Projects'), ('100M+', 'Holes drilled')]
hero = container([
    container([
        eyebrow(t, 'About us', align='center', ls=2.16),
        heading(t('heading', 'The story of Goodfellow Microfabrication'), 54.4, '600', tag='h1', color='#FFFFFF',
                align='center', lh=57.66, ls=-1.088, _margin=box(38, 0, 18, 0),
                css='selector .elementor-heading-title{max-width:22ch;margin:0 auto;text-wrap:balance}'),
        text(t('body', '<p>Since 1982, Goodfellow Microfabrication has been recognised by commercial and government '
                       'agencies for contributions to <strong>medical device manufacturing, biotech and electronics '
                       'fabrication</strong>. Now part of <a href="https://www.goodfellow.com/usa/" target="_blank" '
                       'rel="noopener">Goodfellow, a leading supplier of advanced materials</a>, we are expanding our '
                       'capabilities from our facility at the bwtech@UMBC Research and Technology Park in Baltimore, MD.</p>'),
             18, color='rgba(255,255,255,0.74)', lh=29.7, align='center',
             extra_css='selector p{max-width:727px;margin:0 auto}selector strong{color:#fff;font-weight:600}'
                       'selector a{color:#fff;text-decoration:underline;text-underline-offset:3px}'),
        container([container([
            heading(t('heading', num), 28, '600', color='#FFFFFF', align='center', lh=42, ls=-0.28),
            heading(t('heading', lab), 12, '600', color='rgba(255,255,255,0.55)', align='center', lh=18, ls=1.2, upper=True),
        ], flex_direction='column', flex_align_items='center', flex_gap=gap(4),
           custom_css='selector{width:auto;flex:0 0 auto}') for num, lab in META],
            flex_direction='row', flex_wrap='wrap', flex_justify_content='center', flex_align_items='flex-start',
            flex_gap=gap(28, 40), _margin=box(32, 0, 0, 0)),
    ], content_width='boxed', flex_direction='column', flex_align_items='center', flex_gap=gap(0), boxed_width=px(1200)),
], flex_direction='column', flex_align_items='center', padding=box(72, 24, 64, 24),
   background_background='classic', background_color_hex='#0D1B2A',
   custom_css='selector{overflow:hidden;' + GRID_BG + '}')
save('hero-dark-centered-meta', hero, t)


# ------------------------------------------------------------------ split-media-prose
t = Tok()
split = band([container([
    container([image(t('image', {'asset': 'about_team_facility'}),
                      css='selector img{display:block;width:100%;height:auto}')],
              width={'unit': '%', 'size': 47}, width_mobile={'unit': '%', 'size': 100},
              background_background='classic', background_color_hex='#0D1B2A',
              border_border='solid', border_width=box(1), border_color=LINE, border_radius=box(18),
              custom_css='selector{overflow:hidden;box-shadow:0 22px 58px rgba(15,42,68,.12);'
                         'flex:0 0 calc((100% - 72px) / 2) !important;max-width:calc((100% - 72px) / 2) !important}'
                         '@media(max-width:979px){selector{flex:0 0 100% !important;max-width:100% !important}}'),
    container([
        eyebrow(t, 'Know the feature', margin=box(0, 0, 14, 0)),
        heading(t('heading', 'Rapid fabrication of precision devices, from prototyping to full-scale production'),
                36, '600', tag='h2', color=INK, lh=41.4, ls=-0.72, _margin=box(0, 0, 18, 0)),
        text(t('body', '<p>From a single prototype to production volumes, Goodfellow Microfabrication combines laser '
                       'micromachining, micro-CNC and 3D printing to help teams move miniature products to market '
                       'quickly and cost-effectively.</p>'), 16, color='#3C4858', lh=28, _margin=box(0, 0, 16, 0)),
        container([
            button(t('button', 'Our services'), t('url', 'Services - Services &amp; Applications.html'),
                   shadow='0 8px 24px rgba(245,130,31,.3)'),
            button(t('button', 'Project gallery'), t('url', 'Gallery - Project Gallery.html'),
                   bg='#FFFFFF', fg='#F5821F', border='#F5821F'),
        ], flex_direction='row', flex_wrap='wrap', flex_gap=gap(12, 12), _margin=box(8, 0, 0, 0)),
    ], flex_direction='column', flex_align_items='flex-start', flex_gap=gap(0),
       width={'unit': '%', 'size': 47}, width_mobile={'unit': '%', 'size': 100},
       custom_css='selector{flex:0 0 calc((100% - 72px) / 2) !important;max-width:calc((100% - 72px) / 2) !important}'
                  '@media(max-width:979px){selector{flex:0 0 100% !important;max-width:100% !important}}'),
], flex_direction='row', flex_wrap='wrap', flex_align_items='center', flex_gap=gap(48, 72))])
save('split-media-prose', split, t)


# ---------------------------------------------------------------------- icon-cards-3
t = Tok()
ICON = [('about_icon_history', 'Proud history',
         '<p>For over 40 years Goodfellow Microfabrication has helped clients develop miniature products and bring them '
         'to market quickly and cost-effectively. Since our founding in 1982 we have used a broad range of advanced '
         'technologies, from single prototypes to millions of parts, with a focus on precision and quality.</p>'),
        ('about_icon_partnership', 'Long-term partnership',
         '<p>We prefer to partner on projects from the first prototypes through to product realisation, not just '
         'fabricate parts. That has meant taking on novel materials and production methods, as well as assembly and '
         'supply chain management for our partners.</p>'),
        ('about_icon_group', 'Backed by Goodfellow',
         '<p>Our integration with <a href="https://www.goodfellow.com/usa" target="_blank" rel="noopener">Goodfellow</a> '
         'combines the resources and expertise of both companies. From engineers to support staff, the team works to '
         'your project objectives, with micro-manufacturing capability now supported by a global materials supplier.</p>')]
head = section_head(t, 'How we work', 'History, partnership and group strength')
cards = [card([
    image(t('image', {'asset': a}), css='selector{text-align:left}selector img{width:48px;height:48px;display:block}'),
    heading(t('heading', title), 17.6, '700', tag='h3', color=NAVY, lh=22.88, ls=-0.176),
    text(t('body', body), 14, color=BODY, lh=23.1, extra_css='selector a{color:#15253D}selector a:hover{color:#F5821F}'),
], box(28, 26), 14) for a, title, body in ICON]
save('icon-cards-3', band([head, grid(cards, 3)], bg=SUBTLE, align='center'), t)


# -------------------------------------------------------------------- profile-cards-4
t = Tok()
LINK = ('selector a{font-size:11.5px;font-weight:800;letter-spacing:1.15px;text-transform:uppercase;'
        'color:#15253D;text-decoration:none;line-height:17.25px}selector a:hover{color:#F5821F}')
PEOPLE = [
    ('about_leader_simon', 'Chief Executive Officer', 'Simon Kenney',
     '<p>Before joining Goodfellow, Simon spent 24 years at RS Components in sales, purchasing and product management. '
     'In 2010 he moved to Noida, India, on a one-year secondment to an RS joint venture, then led the Emerging Markets '
     'and Export team covering countries including Russia, Kazakhstan, Saudi Arabia and Israel.</p>'
     '<p>Simon joined Goodfellow in 2016 with responsibility for strategic sales growth, sales planning, business '
     'development and the sales teams. Following the acquisition of the business by Battery Ventures in September '
     '2021, he moved into the CEO role. He lives in Northamptonshire with his family and supports the Northampton '
     'Saints rugby team.</p>',
     '<p><a href="https://uk.linkedin.com/in/simon-kenney-6012371/" target="_blank" rel="noopener">LinkedIn profile</a></p>'),
    ('about_leader_andrew', 'Chief Financial Officer', 'Andrew Watson',
     '<p>Andrew has held senior finance positions for 15 years, qualifying through industry while studying in the '
     'evenings and at weekends. Before joining Goodfellow in 2016 he specialised in turnarounds, as Finance Director '
     'for a regional law firm and previously Group Financial Controller for a large motor retail group.</p>'
     '<p>He is responsible for all financial aspects of the business and, alongside Simon, the creation and delivery '
     'of the growth strategy, and line manages the Finance and HR functions. Andrew is a Chartered Management '
     'Accountant and lives in Nottinghamshire with his family.</p>',
     '<p><a href="https://www.linkedin.com/in/andrew-watson-83a18a15/" target="_blank" rel="noopener">LinkedIn profile</a></p>'),
    ('about_leader_mike', 'Vice President, Manufacturing', 'Mike Davis',
     '<p>Mike joined Potomac as a Sales and Marketing Administrator for what was then a fledgling contract '
     'manufacturing group. As that business grew, he built the Quality System, became a certified Lead Assessor '
     'through the Maryland ISO Consortium, and led Potomac to ISO 9001:2000 certification in January 2004 and '
     'ISO 13485:2003 certification a few years later.</p>'
     '<p>To understand every part of quality, Mike became proficient with Potomac\'s laser technologies: assembling '
     'production laser systems, creating programs, developing customer applications in R&amp;D and production, and '
     'training technicians. He moved into the role of Director of Operations and now leads the upgrade of the '
     'facility. Outside work he spends time with his family, plays sport and enjoys the occasional trip to Canada.</p>',
     None),
    ('about_leader_saniya', 'R&amp;D Engineer', 'Saniya Shetty', None, None),
]
head = section_head(t, 'Our team', 'Leadership')
cards = []
for asset, role, name, bio, link in PEOPLE:
    body = [heading(t('heading', role), 11, '700', color='#F5821F', lh=16.5, ls=1.54, upper=True),
            heading(t('heading', name), 17.6, '700', tag='h3', color=NAVY, lh=22.88, ls=-0.176)]
    if bio:
        body.append(text(t('body', bio), 14, color=BODY, lh=23.1, extra_css='selector p + p{margin-top:10px}'))
    if link:
        body.append(text(t('body', link), 11.5, color=NAVY, weight='800', lh=17.25,
                         extra_css=LINK + 'selector{margin-top:auto}'))
    cards.append(card([
        image(t('image', {'asset': asset}),
              css='selector{margin:0}selector img{display:block;width:100%;aspect-ratio:1/1;height:auto;object-fit:cover}'),
        container(body, flex_direction='column', flex_align_items='stretch', flex_gap=gap(10),
                  padding=box(20, 22, 24, 22), custom_css='selector{flex:1 1 auto}'),
    ], box(0), 0, extra_css='selector .elementor-widget-image{background:#0D1B2A}'))
save('profile-cards-4', band([head, grid(cards, 4)], align='center'), t)


# ---------------------------------------------------------------------- stat-cards-6
t = Tok()
STATS = [('Founded', '1982', 'Over 40 years in micro-manufacturing technologies.'),
         ('Projects', '5K+', 'Thousands of projects across medical, biotech, automotive, semiconductor and aerospace.'),
         ('Holes', '100M+', 'Hundreds of millions of holes drilled, with diameters as small as 1 micron.'),
         ('Lead time', 'Rapid', 'Parts turned around in as fast as 24 hours, depending on the application.'),
         ('Technologies', 'Expanding', 'Market-driven micro-manufacturing technologies, continually advanced.'),
         ('Materials', 'Flexible', 'Processes continually updated to machine new and emerging materials.')]
head = section_head(t, 'By the numbers', 'Four decades of micro-manufacturing')
cards = [card([
    heading(t('heading', m), 11, '700', color='#F5821F', lh=16.5, ls=1.54, upper=True),
    heading(t('heading', v), 35.2, '700', color=NAVY, lh=36.96, ls=-1.056),
    text(t('body', f'<p>{d}</p>'), 14, color=BODY, lh=23.1),
], box(26, 24), 8) for m, v, d in STATS]
save('stat-cards-6', band([head, grid(cards, 3)], bg=SUBTLE, align='center'), t)
print('ok')
