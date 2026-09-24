"""§7.2 AUTHOR — Project Gallery (run 20260924-125928). Rendered with the design's tweak defaults
(layout Uniform, cols 3, gap 18, radius 7, aspect 4:3, caption On hover, modalCta Two, crop 20,
filterStyle Wrap).

  hero-dark-centered-meta-4      `.gal-hero`: centred eyebrow + H1 (18ch) + lede + 4 meta stats
  gallery-grid-filter-lightbox   sticky chip filter bar + "Showing N projects" + 54 native image
                                 cards (hover caption) + a lightbox with 2 CTAs

The zip's CLAUDE.md rule holds: every card is static markup (native widgets, editable); JS only
shows/hides, updates the runtime count, and copies the clicked card's own image/category/title into
the lightbox — it never carries copy. The lightbox, chip styles and script live in one html widget.
"""
import json, os, sys, html as H
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from about_shared import *  # noqa

CARDS = json.load(open(os.path.join(OUT, 'gallery.cards.json')))


def w(wtype, settings):
    return {'id': 'bbbbbbb', 'elType': 'widget', 'widgetType': wtype, 'settings': settings, 'elements': []}


# ------------------------------------------------------------------ hero-dark-centered-meta-4
t = Tok()
META = [('54', 'Projects shown'), ('14', 'Capabilities'), ('±10 µm', 'Typical tolerance'), ('40+ yrs', 'Microfabrication')]
kids = [
    eyebrow(t, 'Project Gallery', align='center', ls=2.16, color='#FFFFFF'),
    heading(t('heading', 'Selected work from the microfabrication floor'), 54.4, '600', tag='h1', color='#FFFFFF',
            align='center', lh=56.576, ls=-1.088, _margin=box(43, 0, 18, 0),
            css='selector .elementor-heading-title{max-width:18ch;margin:0 auto}'),
    text(t('body', '<p>A cross-section of parts we have machined, drilled, cut, marked and assembled, across '
                   '<strong>metals, polymers, glass, silicon and ceramics</strong>. Filter by capability or material to '
                   'find work close to your own project, then send us your drawing.</p>'),
         18, color='rgba(255,255,255,0.74)', lh=29.7, align='center',
         extra_css='selector p{max-width:704px;margin:0 auto}selector strong{color:#fff;font-weight:600}'),
    container([container([
        heading(t('heading', num), 28, '600', color='#FFFFFF', align='center', lh=42, ls=-0.28),
        heading(t('heading', lab), 12, '600', color='rgba(255,255,255,0.55)', align='center', lh=18, ls=1.2, upper=True),
    ], flex_direction='column', flex_align_items='center', flex_gap=gap(4), custom_css='selector{width:auto;flex:0 0 auto}')
        for num, lab in META],
        flex_direction='row', flex_wrap='wrap', flex_justify_content='center', flex_align_items='flex-start',
        flex_gap=gap(28, 28), _margin=box(32, 0, 0, 0)),
]
hero = container([
    container(kids, content_width='boxed', flex_direction='column', flex_align_items='center', flex_gap=gap(0),
              boxed_width=px(1200)),
], flex_direction='column', flex_align_items='center', padding=box(72, 24, 64, 24),
   background_background='classic', background_color_hex='#0D1B2A', custom_css='selector{overflow:hidden;' + GRID_BG + '}')
save('hero-dark-centered-meta-4', hero, t)

# ------------------------------------------------------------------ gallery-grid-filter-lightbox
t = Tok()
from collections import Counter
cnt = Counter(c['cat'] for c in CARDS)
order = ['All'] + sorted(cnt)
chip_markup = ''.join(
    f'<button type="button" class="pl-gc{" on" if c == "All" else ""}" data-filter="{"all" if c == "All" else H.escape(c.lower())}" '
    f'aria-pressed="{"true" if c == "All" else "false"}">{H.escape(c)}<span>{54 if c == "All" else cnt[c]}</span></button>'
    for c in order)
BAR_CSS = (
    '.pl-gbar{display:flex;align-items:center;gap:12px;max-width:1200px;margin:0 auto;padding:14px 24px;box-sizing:border-box}'
    '.pl-gbar .lbl{font:600 12px/18px Inter,system-ui,sans-serif;letter-spacing:1.2px;text-transform:uppercase;color:#65718A;white-space:nowrap;flex-shrink:0}'
    '.pl-gbar .chips{display:flex;flex-wrap:wrap;gap:8px}'
    '.pl-gc{display:inline-flex;align-items:center;gap:7px;padding:8px 14px;border-radius:999px;border:1px solid #DCE1EA;background:#fff;color:#3C4858;'
    'font:600 14px/17px Inter,system-ui,sans-serif;cursor:pointer;white-space:nowrap;transition:background .15s,border-color .15s,color .15s}'
    '.pl-gc:hover{background:#FFF7F0;border-color:#FFF2E8}.pl-gc span{font-size:12px;font-weight:600;color:#9AA4B5;background:#F6F8FB;border-radius:999px;padding:1px 8px}'
    '.pl-gc.on{background:#F5821F;border-color:#F5821F;color:#fff}.pl-gc.on span{background:rgba(255,255,255,.22);color:#fff}'
    '.pl-lb{position:fixed;inset:0;z-index:99999;display:none;background:rgba(11,26,44,.92);backdrop-filter:blur(4px);font-family:Inter,system-ui,sans-serif}'
    '.pl-lb.open{display:block}.pl-lb .stage{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;padding:64px 80px}'
    '.pl-lb figure{margin:0;max-width:100%;max-height:100%;display:flex;flex-direction:column;align-items:center}'
    '.pl-lb img{max-width:100%;max-height:78vh;border-radius:8px;box-shadow:0 24px 60px rgba(0,0,0,.5);background:#ECEFF4}'
    '.pl-lb figcaption{margin-top:18px;text-align:center;max-width:60ch}'
    '.pl-lb .cat{font-size:12px;font-weight:600;text-transform:uppercase;letter-spacing:1.2px;color:#F9B067;margin-bottom:6px}'
    '.pl-lb .ttl{font-size:20px;font-weight:600;color:#fff;margin:0}.pl-lb .cta{display:flex;gap:12px;justify-content:center;flex-wrap:wrap;margin-top:20px}'
    '.pl-lb .cta a{display:inline-flex;align-items:center;padding:12px 24px;border-radius:999px;font:600 15px/15px Inter,system-ui,sans-serif;text-decoration:none}'
    '.pl-lb .cta a.p{background:#F5821F;color:#fff;box-shadow:0 8px 24px rgba(245,130,31,.3)}.pl-lb .cta a.g{border:1px solid rgba(255,255,255,.32);color:#fff}'
    '.pl-lb .b{position:absolute;display:flex;align-items:center;justify-content:center;width:48px;height:48px;border-radius:999px;border:1px solid rgba(255,255,255,.22);'
    'background:rgba(255,255,255,.08);color:#fff;cursor:pointer}.pl-lb .b:hover{background:rgba(255,255,255,.18);border-color:rgba(255,255,255,.5)}'
    '.pl-lb .b svg{width:22px;height:22px;fill:none;stroke:currentColor;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}'
    '.pl-lb .x{top:20px;right:20px}.pl-lb .pv{left:20px;top:50%;transform:translateY(-50%)}.pl-lb .nx{right:20px;top:50%;transform:translateY(-50%)}'
    '.pl-lb .n{position:absolute;top:32px;left:50%;transform:translateX(-50%);color:rgba(255,255,255,.7);font-size:13px;font-weight:600;letter-spacing:.8px}'
    '@media(max-width:720px){.pl-lb .stage{padding:56px 12px 88px}}')
lb_cta1, lb_cta2, lb_url = t('heading', 'Request a quote for this part'), t('heading', 'Upload CAD'), t('url', 'Services - CNC Micromachining.html#quote')
BAR_HTML = ('<style>' + BAR_CSS + '</style><div class="pl-gbar"><span class="lbl">' + t('heading', 'Filter') + '</span>'
            '<div class="chips" role="group" aria-label="Filter projects by category">' + t('embed', chip_markup) + '</div></div>'
            '<div class="pl-lb" role="dialog" aria-modal="true" aria-hidden="true" aria-label="Project image viewer"><div class="n"></div>'
            '<button type="button" class="b x" aria-label="Close viewer"><svg viewBox="0 0 24 24"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg></button>'
            '<button type="button" class="b pv" aria-label="Previous"><svg viewBox="0 0 24 24"><polyline points="15 18 9 12 15 6"/></svg></button>'
            '<button type="button" class="b nx" aria-label="Next"><svg viewBox="0 0 24 24"><polyline points="9 18 15 12 9 6"/></svg></button>'
            '<div class="stage"><figure><img alt=""><figcaption><div class="cat"></div><p class="ttl"></p>'
            '<div class="cta"><a class="p" href="' + lb_url + '">' + lb_cta1 + '</a><a class="g" href="' + lb_url + '">' + lb_cta2 + '</a></div>'
            '</figcaption></figure></div></div>'
            '<script>(function(){var bar=document.currentScript.previousElementSibling.previousElementSibling,lb=document.currentScript.previousElementSibling;'
            'var scope=bar;while(scope.parentElement&&!scope.parentElement.hasAttribute("data-elementor-id"))scope=scope.parentElement;'
            # the page section, not closest(".e-parent") — the bar's own container is e-parent too (12357 iter 1: filter + lightbox inert)
            'document.body.appendChild(lb);var vis=[],pos=0;'
            'function cards(){return [].slice.call(scope.querySelectorAll(".pl-gal-card"));}'
            'function cat(c){var h=c.querySelector(".elementor-heading-title");return h?h.textContent.trim():"";}'
            'function ttl(c){var h=c.querySelectorAll(".elementor-heading-title");return h[1]?h[1].textContent.trim():"";}'
            'function apply(v){vis=[];cards().forEach(function(c){var on=v==="all"||cat(c).toLowerCase()===v;c.style.display=on?"":"none";if(on)vis.push(c);});'
            'var n=scope.querySelector(".pl-gal-count strong");if(n)n.textContent=vis.length;}'
            'bar.querySelectorAll("button[data-filter]").forEach(function(b){b.addEventListener("click",function(){'
            'bar.querySelectorAll("button[data-filter]").forEach(function(x){var on=x===b;x.classList.toggle("on",on);x.setAttribute("aria-pressed",on?"true":"false");});'
            'apply(b.getAttribute("data-filter"));});});'
            'function paint(){var c=vis[pos];if(!c)return;var i=c.querySelector("img"),im=lb.querySelector("img");im.src=i.currentSrc||i.src;im.alt=i.alt;'
            'lb.querySelector(".cat").textContent=cat(c);lb.querySelector(".ttl").textContent=ttl(c);lb.querySelector(".n").textContent=(pos+1)+" / "+vis.length;}'
            'function open(c){if(!vis.length)apply("all");pos=Math.max(0,vis.indexOf(c));paint();lb.classList.add("open");lb.setAttribute("aria-hidden","false");document.body.style.overflow="hidden";}'
            'function close(){lb.classList.remove("open");lb.setAttribute("aria-hidden","true");document.body.style.overflow="";}'
            'function step(d){pos=(pos+d+vis.length)%vis.length;paint();}'
            'scope.addEventListener("click",function(e){var c=e.target.closest&&e.target.closest(".pl-gal-card");if(c){e.preventDefault();open(c);}});'
            'lb.querySelector(".x").addEventListener("click",close);lb.querySelector(".pv").addEventListener("click",function(){step(-1);});'
            'lb.querySelector(".nx").addEventListener("click",function(){step(1);});'
            'lb.querySelector(".stage").addEventListener("click",function(e){if(e.target===e.currentTarget)close();});'
            'document.addEventListener("keydown",function(e){if(!lb.classList.contains("open"))return;if(e.key==="Escape")close();else if(e.key==="ArrowLeft")step(-1);else if(e.key==="ArrowRight")step(1);});'
            '})();</script>')
bar = container([w('html', {'html': BAR_HTML})], flex_direction='column', flex_gap=gap(0), width={'unit': '%', 'size': 100},
                background_background='classic', background_color='rgba(255,255,255,0.92)', border_border='solid',
                border_width=box(0, 0, 1, 0), border_color=LINE,
                custom_css='selector{position:sticky;top:0;z-index:40;backdrop-filter:blur(8px)}')
count = text(t('body', '<p class="pl-gal-count">Showing <strong>54</strong> projects</p>'), 14, color=MUTED, lh=22.4,
             _margin=box(0, 0, 20, 0), extra_css='selector strong{color:#0F1620;font-weight:600}')
CARD_CSS = ('selector{position:relative;overflow:hidden;cursor:pointer;transition:transform .25s cubic-bezier(.25,.46,.45,.94)}'
            'selector:hover{transform:translateY(-2px)}'
            'selector .elementor-widget-image img{display:block;width:100%;aspect-ratio:4/3;height:100%;object-fit:cover;transform:scale(1.2)}'
            'selector > .e-con:last-child{opacity:0;transition:opacity .25s cubic-bezier(.25,.46,.45,.94)}'
            'selector:hover > .e-con:last-child{opacity:1}@media(hover:none){selector > .e-con:last-child{opacity:1}}')
cards = []
for c in CARDS:
    cards.append(container([
        image(t('image', {'asset': c['asset']}), css='selector{margin:0;line-height:0}'),
        container([
            heading(t('heading', c['cat']), 12, '600', color='#FFFFFF', lh=15, ls=0.96, upper=True,
                    css='selector{width:auto;align-self:flex-start}selector .elementor-heading-title{background:rgba(14,99,168,.92);padding:3px 9px;border-radius:4px}',
                    _margin=box(0, 0, 8, 0)),
            heading(t('heading', c['title']), 16, '600', tag='h3', color='#FFFFFF', lh=20),
        ], flex_direction='column', flex_justify_content='flex-end', flex_align_items='flex-start', flex_gap=gap(0), padding=box(16),
           custom_css='selector{position:absolute!important;inset:0;background:linear-gradient(to top,rgba(11,26,44,.82) 0%,rgba(11,26,44,.3) 38%,transparent 64%)}'),
    ], css_classes='pl-gal-card', flex_direction='column', flex_gap=gap(0), background_background='classic',
       background_color='#ECEFF4', border_radius=box(7), custom_css=CARD_CSS))
grid_ = container(cards, flex_direction='row', flex_wrap='wrap', flex_align_items='stretch', flex_gap=gap(18, 18),
                  width={'unit': '%', 'size': 100},
                  custom_css=('selector > .e-con{flex:0 0 calc((100% - 36px) / 3) !important;max-width:calc((100% - 36px) / 3) !important}'
                              '@media(max-width:760px){selector > .e-con{flex:0 0 calc((100% - 18px) / 2) !important;max-width:calc((100% - 18px) / 2) !important}}'
                              '@media(max-width:460px){selector > .e-con{flex:0 0 100% !important;max-width:100% !important}}'))
section = container([
    bar,
    container([count, grid_], content_width='boxed', boxed_width=px(1200), flex_direction='column', flex_gap=gap(0),
              padding=box(40, 24, 80, 24)),
], flex_direction='column', flex_align_items='stretch', padding=box(0), background_background='classic',  # bar spans full width, as the design's
   background_color_hex='#FFFFFF', custom_css='selector{overflow:visible}')
save('gallery-grid-filter-lightbox', section, t)
print('ok', len(cards), 'cards', len(order), 'chips')
