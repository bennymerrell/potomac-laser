"""Tiny builders for authoring §7 candidate sections as Elementor v3 legacy JSON.

Conventions copied from the existing fragments (reference/snippets/*.json), not invented:
outer container content_width:full + background -> inner container content_width:boxed;
card rows flex_align_items:stretch; widths via width/boxed_width, never
_element_custom_width; typography per widget (the Kit has no typography globals);
colours through Kit 11259 `__globals__` where a token exists, literal otherwise.
Ids are placeholders — tools/assemble.py re-ids every element on assembly.
"""
import itertools

_ids = itertools.count(1)

# Kit 11259 custom colours (PATTERNS.md §Kit global tokens). Anything else stays literal.
KIT = {'#F5821F': 'gforange', '#D96E10': 'gforangedk', '#15253D': 'gfnavy', '#1D3557': 'gfnavymid',
       '#0D1B2A': 'gfnavydp', '#6B7280': 'gfbody', '#3C4858': 'gfink', '#FFFFFF': 'gfwhite',
       '#1A71AB': 'gfblue'}


def _id():
    return f'{next(_ids):07x}'


def px(v):
    return {'unit': 'px', 'size': v}


def box(t, r=None, b=None, l=None):
    r = t if r is None else r
    b = t if b is None else b
    l = r if l is None else l
    return {'unit': 'px', 'top': str(t), 'right': str(r), 'bottom': str(b), 'left': str(l),
            'isLinked': len({t, r, b, l}) == 1}


def gap(row, col=None):
    col = row if col is None else col
    return {'unit': 'px', 'column': str(col), 'row': str(row), 'isLinked': row == col}


def colour(settings, key, hexv):
    """Set a colour control, via a Kit global when one exists."""
    if hexv is None:
        return
    tok = KIT.get(hexv.upper())
    if tok:
        settings[key] = ''
        settings.setdefault('__globals__', {})[key] = f'globals/colors?id={tok}'
    else:
        settings[key] = hexv


FONT = 'Inter'  # the design's face; the Kit has no typography globals, and Elementor's
                # fallback is Roboto, so every text widget names it explicitly.


def container(children, **s):
    s.setdefault('content_width', 'full')
    # Elementor's container default padding is 10px; the design's nested boxes have none
    # unless stated, and an unpadded 11px dot otherwise renders 20x20.
    s.setdefault('padding', box(0))
    # Containers take `margin`; `_margin` is the WIDGET key and is silently ignored here
    # (verify iteration 2 on post 12268: every container margin was dropped).
    if '_margin' in s:
        s['margin'] = s.pop('_margin')
    if s.get('content_width') == 'boxed':
        s.setdefault('boxed_width', px(1152))  # design .container 1200 - 2x24 gutter
    for k in [k for k in list(s) if k.endswith('_hex')]:
        colour(s, k[:-4], s.pop(k))
    return {'id': _id(), 'elType': 'container', 'isInner': False, 'settings': s, 'elements': children}


def heading(title, size, weight='600', tag='div', color=None, align=None, lh=None, ls=None,
            upper=False, css=None, **extra):
    s = {'title': title, 'header_size': tag, 'typography_typography': 'custom', 'typography_font_family': FONT,
         'typography_font_size': px(size), 'typography_font_weight': str(weight)}
    colour(s, 'title_color', color)
    if align:
        s['align'] = align
    if lh:
        s['typography_line_height'] = px(lh)
    if ls is not None:
        s['typography_letter_spacing'] = px(ls)
    if upper:
        s['typography_text_transform'] = 'uppercase'
    if css:
        s['custom_css'] = css
    s.update(extra)
    return {'id': _id(), 'elType': 'widget', 'widgetType': 'heading', 'settings': s, 'elements': []}


def text(html, size, color=None, weight='400', lh=None, align=None, extra_css='', **extra):
    """text-editor. The theme styles `p` at 16px with a bottom margin and beats the widget's
    inherited typography (PATTERNS.md services-image-cards Notes), so size/leading/margin are
    pinned on `selector p` as well."""
    s = {'editor': html, 'typography_typography': 'custom', 'typography_font_family': FONT, 'typography_font_size': px(size),
         'typography_font_weight': str(weight)}
    colour(s, 'text_color', color)
    if lh:
        s['typography_line_height'] = px(lh)
    if align:
        s['align'] = align
    col = f'color:{color};' if color and not KIT.get(color.upper()) else ''
    s['custom_css'] = (f'selector p{{font-size:{size}px;{f"line-height:{lh}px;" if lh else ""}'
                       f'font-weight:{weight};{col}margin:0}}'
                       # the theme sizes bare `a` at 16px, which beats inheritance (12277 iter 2)
                       'selector a{font-size:inherit;line-height:inherit}' + extra_css)
    s.update(extra)
    return {'id': _id(), 'elType': 'widget', 'widgetType': 'text-editor', 'settings': s, 'elements': []}


def button(label, url, bg='#F5821F', fg='#FFFFFF', size=15, weight='600', pad=(12, 24),
           border=None, shadow=None, css='', **extra):
    s = {'text': label, 'link': {'url': url, 'is_external': '', 'nofollow': ''},
         'typography_typography': 'custom', 'typography_font_family': FONT, 'typography_font_size': px(size),
         'typography_font_weight': str(weight),
         'border_radius': box(999), 'text_padding': box(pad[0], pad[1])}
    colour(s, 'background_color', bg)
    colour(s, 'button_text_color', fg)
    if border:
        s['border_border'] = 'solid'
        s['border_width'] = box(1)
        s['border_color'] = border
    if shadow or css:
        s['custom_css'] = (f'selector .elementor-button{{box-shadow:{shadow}}}' if shadow else '') + css
    s.update(extra)
    return {'id': _id(), 'elType': 'widget', 'widgetType': 'button', 'settings': s, 'elements': []}


def image(token, css='', **extra):
    s = {'image': {'url': token, 'id': ''}, 'image_size': 'full'}
    if css:
        s['custom_css'] = css
    s.update(extra)
    return {'id': _id(), 'elType': 'widget', 'widgetType': 'image', 'settings': s, 'elements': []}


def dot(hexv, size):
    return container([], width=px(size), min_height=px(size), custom_css='selector{flex-shrink:0}',
                     background_background='classic', background_color_hex=hexv,
                     border_radius={'unit': '%', 'top': '50', 'right': '50', 'bottom': '50',
                                    'left': '50', 'isLinked': True})


class Tok:
    """Per-fragment token numbering in document order (PATTERNS.md §Placeholder vocabulary)."""
    def __init__(self):
        self.n = {}
        self.values = {}

    def __call__(self, kind, value):
        self.n[kind] = self.n.get(kind, 0) + 1
        name = f'{kind}_{self.n[kind]}'
        self.values[name] = value
        return '{' + name + '}'
