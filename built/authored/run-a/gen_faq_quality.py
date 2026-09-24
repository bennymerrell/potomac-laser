"""§7.2 AUTHOR — FAQs + Quality Policy (run 20260924-125928).

  faq-accordion-filter-10   category chips + 10 one-question toggles in an 880px column (FAQs)
  split-list-figure         prose (eyebrow, H2, check-list) | framed certificate figure + caption (Quality)
  check-list-centered       light section, centred head + one check-list in a 900px column (Quality)

The FAQ filter reuses text-link-cards-6-filter's chip widget and click-time script unchanged:
each question is a `.pl-filter-card` container whose first heading is its category label, hidden
(display:none) because the design shows no category on the item. Hero sections reuse
hero-dark-centered (library, minted this run) — values only.
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from about_shared import *  # noqa
from gen_employment import CHIPS_HTML, check_list, LIST_CSS  # noqa  (re-runs gen_employment: harmless, same output)

Z = '/private/tmp/claude-501/-Users-admin-orca-potomac-laser/d79e1efa-e1f9-4dfb-b04f-d08b0ac7ba4e/scratchpad/zip/'


def save_values(page, pid, tok):
    json.dump(tok.values, open(os.path.join(OUT, f'{page}.{pid}.values.json'), 'w'), indent=1, ensure_ascii=False)


def hero_vals(page, eb, h1, lede):
    t = Tok(); hero_centered(t, eb, h1, lede); save_values(page, 'hero-dark-centered', t)


TOGGLE_CSS = (
    'selector .elementor-toggle-item{border:0;background:transparent;margin:0}'
    'selector .elementor-tab-title{display:flex!important;align-items:center;justify-content:space-between;gap:20px;'
    'padding:22px 0;border:0;background:transparent;font:700 16px/20px Inter,system-ui,sans-serif;color:var(--e-global-color-gfnavy);cursor:pointer}'
    'selector .elementor-tab-title.elementor-active{color:var(--e-global-color-gforange)}'
    'selector .elementor-toggle-title{order:1;flex:1 1 auto;color:inherit}'
    'selector .elementor-toggle-icon{order:2;margin:0;width:28px;height:28px;min-width:28px;border:1.5px solid #DCE1EA;border-radius:50%;'
    'display:flex;align-items:center;justify-content:center;flex-shrink:0;float:none;transition:transform .3s cubic-bezier(.25,.46,.45,.94)}'
    'selector .elementor-toggle-icon *{display:none!important}'
    "selector .elementor-toggle-icon::before{content:'+';display:block;font-size:18px;line-height:1;color:var(--e-global-color-gforange)}"
    'selector .elementor-tab-title.elementor-active .elementor-toggle-icon{transform:rotate(45deg)}'
    'selector .elementor-tab-content{border:0;padding:0 0 22px;font-size:15px;line-height:26.25px;color:var(--e-global-color-gfink)}'
    'selector .elementor-tab-content p{margin:0;font-size:15px;line-height:26.25px}')


def faq_item(t, cat_label, q, a):
    return container([
        heading(t('heading', cat_label), 11, '700', css='selector{display:none}'),
        {'id': 'f0f0f01', 'elType': 'widget', 'widgetType': 'toggle', 'settings': {
            'tabs': [{'tab_title': t('faq_q', q), 'tab_content': t('faq_a', a), '_id': 'a1b2c3d'}],
            'selected_icon': {'value': 'fas fa-plus', 'library': 'fa-solid'},
            'selected_active_icon': {'value': 'fas fa-minus', 'library': 'fa-solid'},
            # an empty icon makes Elementor omit .elementor-toggle-icon entirely (12300 iter 1: no circle,
            # rows 65px not 73); the glyphs are hidden by TOGGLE_CSS and the design's '+' circle drawn instead
            'custom_css': TOGGLE_CSS}, 'elements': []},
    ], css_classes='pl-filter-card', border_border='solid', border_width=box(0, 0, 1, 0), border_color=LINE,
       flex_direction='column', flex_gap=gap(0))


# ---------------------------------------------------------------- FAQs
fq = sections(Z + 'About - FAQs.html')
hero_vals('faqs', 'Help', 'Frequently asked questions',
          '<p>Answers on <strong>ordering, drawings, lead times, materials and capability</strong>. If your question '
          'is not here, our engineers will answer it directly.</p>')
chips = re.findall(r'<button type="button" class="ab-chip" data-filter="([^"]+)"[^>]*>(.*?)</button>', fq[1])
label = {k: txt(v) for k, v in chips}
items = []
for blk in inner(fq[1]).split('<div class="faq-item"')[1:]:
    cat = re.search(r'data-filter-item="([^"]+)"', blk).group(1)
    q = re.search(r'<span>(.*?)</span>', blk).group(1)
    a = re.search(r'<div class="ab-faq-a"[^>]*>(.*?)</div>', blk).group(1)
    q = q.replace('does Potomac offer', 'does Goodfellow Microfabrication offer')  # brand normalisation (TRANSLATE §6)
    items.append((cat, q, a))
assert len(items) == 10, len(items)
t = Tok()
chip_markup = ''.join(f'<button type="button" data-filter="{"all" if k == "all" else label[k].lower()}" '
                      f'aria-pressed="{"true" if k == "all" else "false"}">{v}</button>' for k, v in chips)
chips_w = {'id': 'c0ffee2', 'elType': 'widget', 'widgetType': 'html', 'settings': {
    'html': CHIPS_HTML.replace('{embed_1}', t('embed', chip_markup)), '_margin': box(0, 0, 28, 0)}, 'elements': []}
qa = [faq_item(t, label[c], txt(q), re.sub(r'<p style="[^"]*">', '<p>', a.strip())) for c, q, a in items]
col = container([chips_w, container(qa, flex_direction='column', flex_gap=gap(0), border_border='solid',
                                    border_width=box(1, 0, 0, 0), border_color=LINE, width={'unit': '%', 'size': 100})],
                flex_direction='column', flex_align_items='stretch', flex_gap=gap(0), width=px(832),
                width_mobile={'unit': '%', 'size': 100})
save('faq-accordion-filter-10', band([col], align='center'), t)
save_values('faqs', 'faq-accordion-filter-10', t)

# ---------------------------------------------------------------- Quality Policy
qp = sections(Z + 'About - Quality Policy.html')
hero_vals('quality-policy', 'Quality policy', 'Committed to being a world leader in micro-manufacturing',
          '<p>Our quality management system is certified to <strong>ISO 13485:2016</strong>. These commitments and '
          'objectives guide how we work with every customer and supplier.</p>')
li = lambda sec: '<ul>' + ''.join(f'<li>{x}</li>' for x in re.findall(r'<li><svg.*?</svg><span>(.*?)</span></li>', sec, re.S)) + '</ul>'
t = Tok()
prose = container([
    eyebrow(t, 'Our commitments', margin=box(0, 0, 20, 0)),
    heading(t('heading', 'To achieve these goals, we will'), 36, '600', tag='h2', color=INK, lh=41.4, ls=-0.72,
            _margin=box(0, 0, 18, 0)),
    check_list(t, li(qp[1])),
], flex_direction='column', flex_align_items='stretch', flex_gap=gap(0), custom_css=COLS2.format(g=72))
fig = container([
    container([image(t('image', {'asset': 'qp_certificate'}), css='selector img{display:block;width:100%;height:auto}')],
              padding=box(18), background_background='classic', background_color_hex='#FFFFFF',
              border_border='solid', border_width=box(1), border_color=LINE, border_radius=box(18),
              custom_css='selector{overflow:hidden;box-shadow:0 22px 58px rgba(15,42,68,.12)}'),
    heading(t('heading', 'ISO 13485:2016 certificate'), 13, '400', tag='div', color=MUTED, align='center', lh=19.5,
            _margin=box(12, 0, 0, 0)),
], flex_direction='column', flex_align_items='stretch', flex_gap=gap(0), custom_css=COLS2.format(g=72))
save('split-list-figure', band([container([prose, fig], flex_direction='row', flex_wrap='wrap', flex_align_items='flex-start',
                                          flex_gap=gap(48, 72))]), t)
save_values('quality-policy', 'split-list-figure', t)

t = Tok()
head = section_head(t, 'Objectives', 'Our objectives', mb=48)
body = container([check_list(t, li(qp[2]))], width=px(852), width_mobile={'unit': '%', 'size': 100})
save('check-list-centered', band([head, body], bg=SUBTLE, align='center'), t)
save_values('quality-policy', 'check-list-centered', t)
print('ok faq', len(items), 'chips', [label[k] for k, _ in chips])
