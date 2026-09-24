"""§7.2 AUTHOR — Employment (run 20260924-125928).

  hero-dark-centered-cta     `.ab-hero` + one CTA button, no meta row
  split-prose-list-media     prose (eyebrow, H2, paragraph, check-list) left | framed photo right
  text-link-cards-6-filter   centred head + category chips + 6 whole-card links (no image)

The chip filter follows the zip's own CLAUDE.md rule: every card is static markup and JS only
shows/hides. The script reads each card's visible category label (its first heading), so the
fragment carries no page-specific classes; chips are one {embed_1} slot of <button> markup.

Fix log (verify iteration 1 on 12298): cards are queried at click time — the script runs before
the grid below it is in the DOM, so a load-time query found none and the filter was inert.
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from about_shared import *  # noqa

Z = '/private/tmp/claude-501/-Users-admin-orca-potomac-laser/d79e1efa-e1f9-4dfb-b04f-d08b0ac7ba4e/scratchpad/zip/'
sx = sections(Z + 'About - Employment.html')

# check-list: one text-editor <ul>, each <li> a bordered card with an orange check (design .ab-list)
CHECK = ("url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' "
         "stroke='%23F5821F' stroke-width='2.5' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline "
         "points='20 6 9 17 4 12'/%3E%3C/svg%3E\")")
LIST_CSS = ('selector ul{list-style:none;margin:0;padding:0;display:grid;gap:12px}'
            'selector li{position:relative;margin:0;font-size:15.5px;line-height:25.575px;color:#3C4858;'
            'padding:16px 18px 16px 48px;background:#fff;border:1px solid #DCE1EA;border-radius:12px}'
            f'selector li::before{{content:"";position:absolute;left:18px;top:20px;width:18px;height:18px;background:{CHECK} no-repeat center/18px}}')


def check_list(t, items_html):
    return text(t('body', items_html), 15.5, color='#3C4858', lh=25.575, extra_css=LIST_CSS)


def media(t, asset):
    return container([image(t('image', {'asset': asset}), css='selector img{display:block;width:100%;height:auto}')],
                     background_background='classic', background_color_hex='#0D1B2A',
                     border_border='solid', border_width=box(1), border_color=LINE, border_radius=box(18),
                     custom_css='selector{overflow:hidden;box-shadow:0 22px 58px rgba(15,42,68,.12)}' + COLS2.format(g=72))


CHIPS_HTML = ('<div class="pl-chips" data-pl-chips role="group" aria-label="Filter">{embed_1}</div>'
              '<style>.pl-chips{display:flex;flex-wrap:wrap;gap:8px;justify-content:center}'
              '.pl-chips button{border:1.5px solid #DCE1EA;background:#fff;border-radius:9999px;padding:9px 18px;'
              'font:700 12px/15px Inter,system-ui,sans-serif;letter-spacing:.72px;text-transform:uppercase;color:#6B7280;'
              'cursor:pointer;transition:all .25s cubic-bezier(.25,.46,.45,.94)}'
              '.pl-chips button:hover{border-color:#F5821F;color:#15253D}'
              '.pl-chips button[aria-pressed="true"]{background:#F5821F;border-color:#F5821F;color:#fff}</style>'
              '<script>(function(){var g=document.currentScript.previousElementSibling.previousElementSibling;'
              'var scope=g.closest(".e-parent")||document;'
                            'g.querySelectorAll("button[data-filter]").forEach(function(b){b.addEventListener("click",function(){'
              'var v=b.getAttribute("data-filter");'
              'g.querySelectorAll("button[data-filter]").forEach(function(x){x.setAttribute("aria-pressed",x===b?"true":"false");});'
              'scope.querySelectorAll(".pl-filter-card").forEach(function(c){var h=c.querySelector(".elementor-heading-title");'
              'var cat=h?h.textContent.trim().toLowerCase():"";'
              'c.style.display=(v==="all"||cat===v)?"":"none";});});});})();</script>')


# ---------------------------------------------------------------- hero-dark-centered-cta
t = Tok()
cta = container([button(t('button', 'View openings'), t('url', '#openings'), size=15, pad=(15, 28),
                        shadow='0 8px 24px rgba(245,130,31,.3)', css='selector .elementor-button{border:1px solid transparent}')],
                flex_direction='row', flex_wrap='wrap', flex_justify_content='center', flex_gap=gap(12, 12),
                _margin=box(30, 0, 0, 0))
sec = hero_centered(t, 'Careers', 'Careers at Goodfellow Microfabrication',
                    '<p>Ready to advance your career with a high-tech manufacturer? Goodfellow Microfabrication is '
                    'always looking for <strong>detail-oriented, multitasking professionals</strong> to join the team in '
                    'Maryland, whether your experience is in shipping and receiving, operations or another area.</p>',
                    extra=cta)
save('hero-dark-centered-cta', sec, t)

# ---------------------------------------------------------------- split-prose-list-media
t = Tok()
items = re.findall(r'<li><svg.*?</svg><span>(.*?)</span></li>', sx[1], re.S)
assert len(items) == 5
prose = container([
    eyebrow(t, 'Working at Goodfellow Microfabrication', margin=box(0, 0, 20, 0)),  # 14 + the 24px line box
    heading(t('heading', 'Benefits'), 36, '600', tag='h2', color=INK, lh=41.4, ls=-0.72, _margin=box(0, 0, 18, 0)),
    text(t('body', '<p>We offer competitive pay and a comprehensive benefits package. If there is no role listed that '
                   'matches your experience, we still welcome your résumé for future opportunities.</p>'),
         16, color='#3C4858', lh=28, _margin=box(0, 0, 16, 0)),
    check_list(t, '<ul>' + ''.join(f'<li>{i}</li>' for i in items) + '</ul>'),
], flex_direction='column', flex_align_items='stretch', flex_gap=gap(0), custom_css=COLS2.format(g=72))
sec = band([container([prose, media(t, 'emp_benefits')], flex_direction='row', flex_wrap='wrap',
                      flex_align_items='center', flex_gap=gap(48, 72))])
save('split-prose-list-media', sec, t)

# ---------------------------------------------------------------- text-link-cards-6-filter
t = Tok()
head = section_head(t, 'Openings', 'Current roles', mb=48)
chips = re.findall(r'<button type="button" class="ab-chip" data-filter="([^"]+)"[^>]*>(.*?)</button>', sx[2])
chip_markup = ''.join(f'<button type="button" data-filter="{"all" if k == "all" else txt(v).lower()}" '
                      f'aria-pressed="{"true" if k == "all" else "false"}">{v}</button>' for k, v in chips)
chips_w = {'id': 'c0ffee1', 'elType': 'widget', 'widgetType': 'html', 'settings': {
    'html': CHIPS_HTML.replace('{embed_1}', t('embed', chip_markup)), '_margin': box(0, 0, 28, 0)}, 'elements': []}
jobs = ab_cards(sx[2]); assert len(jobs) == 6
cards = [card([
    heading(t('heading', j['meta']), 11, '700', color='#F5821F', lh=16.5, ls=1.54, upper=True),
    heading(t('heading', j['title']), 17.6, '700', tag='h3', color=NAVY, lh=22.88, ls=-0.176),
    text(t('body', f'<p>{j["text"]}</p>'), 14, color=BODY, lh=23.1),
    text(t('body', f'<p>{j["label"]}</p>'), 11.5, color=NAVY, weight='800', lh=17.25, extra_css=LINK_LABEL + 'selector{margin-top:auto}'),
], box(24, 24, 26, 24), 10, html_tag='a', link={'url': t('url', j['href']), 'is_external': 'on', 'nofollow': ''},
   css_classes='pl-filter-card',
   extra_css='selector{text-decoration:none;color:inherit;transition:transform .3s cubic-bezier(.25,.46,.45,.94),box-shadow .3s cubic-bezier(.25,.46,.45,.94)}'
             'selector:hover{transform:translateY(-2px);box-shadow:0 10px 24px rgba(15,42,68,.08)}') for j in jobs]
sec = band([head, chips_w, grid(cards, 3)], bg=SUBTLE, align='center')
sec['settings']['_element_id'] = 'openings'
save('text-link-cards-6-filter', sec, t)

assert re.search(r'<img src="https://www.potomac-laser.com/wp-content/uploads/2024/05/TS_KAP-1024x683.webp"', sx[1])
print('ok', len(chips), 'chips')
