"""Service-page refresh from the current designs (Potomac Laser.zip fab7225c, `Services - *.html`).

Supervised refresh of drafts 12239-12243 (user request 2026-09-25, build style "Mixed"):
native Elementor widgets for hero / why-us / services / workflow / group / testimonials / FAQ /
closing band; HTML widgets carrying the design's own markup + scoped CSS for the application
explorer, the specifications block, the process-selection panel and the quote form.

Inputs (scratchpad):  svc/Services - <name>.html    the designs (tweak defaults: explorer "Example",
                                                    quote "Compact", progress + upload shown)
                      meas/<key>-<sec>.html|.css    markup + CSS extracted from the rendered design
                                                    and scoped under .pl-svc-<sec> (css-extract.js)
Decisions carried in:  explorer pills are informational (no drawer / basket); "Browse materials"
dropped; "Upload CAD" / "Request Material + Machining Quote" jump to #quote; the design's
normalizeStandaloneLinks() (rewrites every root-relative link through a Mimecast redirect) is NOT
carried; present-tense "Potomac" -> "Goodfellow Microfabrication"; copy otherwise verbatim.

    <scratchpad>/venv/bin/python built/authored/run-a/gen_services.py
"""
import html as H, json, os, re, sys
from bs4 import BeautifulSoup, Tag, NavigableString

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from elb import container, heading, text, button, image, box, gap, px, Tok, colour, KIT  # noqa: E402

SCR = '/private/tmp/claude-501/-Users-admin-orca-potomac-laser/d79e1efa-e1f9-4dfb-b04f-d08b0ac7ba4e/scratchpad/'
OUT = os.path.join(HERE, 'candidates')
PAGES = [('cnc', 'CNC Micromachining', 12239), ('lm', 'Laser Micromachining', 12240),
         ('mhd', 'Micro-Hole Drilling', 12241), ('rp', 'Rapid Prototyping', 12242), ('3dp', '3D Printing', 12243)]
B = 'https://www.potomac-laser.com'
# design hrefs -> live URLs (header Services dropdown, run 20260925-service-urls)
HREF = {'Services - CNC Micromachining.html': B + '/services/cnc-micro-machining-services/',
        'Services - Laser Micromachining.html': B + '/services/laser-micromachining/',
        'Services - Micro-Hole Drilling.html': B + '/services/micro-hole-drilling/',
        'Services - Rapid Prototyping.html': B + '/services/rapid-prototyping-services/',
        'Services - 3D Printing.html': B + '/services/3d-printing-contract-services/',
        'Services - Services & Applications.html': B + '/services-applications/',
        'Services - Services &amp; Applications.html': B + '/services-applications/',
        'Contact - Contact.html': B + '/contact/', 'Gallery - Project Gallery.html': B + '/project-gallery/',
        'Materials - Materials.html': B + '/materials/'}

ORANGE, NAVYMID, NAVY, NAVYDP = '#F5821F', '#1D3557', '#15253D', '#0D1B2A'
GRAY500, GRAY400, GRAY200, GRAY100 = '#6B7280', '#9CA3AF', '#E5E7EB', '#F3F4F6'
FONT = 'Inter'
BRAND_LOG = []


def brand(s):
    n = s.count('Potomac')
    if n:
        BRAND_LOG.append(n)
    return s.replace('Potomac Photonics', 'Goodfellow Microfabrication').replace('Potomac', 'Goodfellow Microfabrication')


def clean(s):
    return brand(H.unescape(re.sub(r'\s+', ' ', s)).strip())


def inner(el):
    """inner HTML, whitespace collapsed, svg dropped, brand-normalised."""
    for x in el.find_all('svg'):
        x.decompose()
    return brand(re.sub(r'\s+', ' ', ''.join(str(c) for c in el.contents)).strip())


def link(href):
    if not href:
        return '#quote'
    href = H.unescape(href)
    # the design's normalizeStandaloneLinks() rewrote root-relative links in the rendered DOM through a Mimecast redirect
    mm = re.match(r'https?://url\.[a-z.]*mimecastprotect\.com/s/[^?]*\?domain=([a-z0-9.-]+)(/.*)?$', href)
    if mm:
        dom, path = mm.group(1), mm.group(2) or '/'
        if dom.endswith('goodfellow.com') and mm.group(2):
            href = path          # rendered DOM: a root-relative site link rewritten by normalizeStandaloneLinks()
        else:                    # wrapped in the design source itself: an external site
            known = {'goodfellow.com': 'https://www.goodfellow.com', 'basref.com': 'https://www.basrid.co.uk',  # basref.com does not resolve
                     'basrid.co.uk': 'https://www.basrid.co.uk', 'suisse-tp.ch': 'https://suisse-tp.ch'}
            return known.get(dom.replace('www.', ''), 'https://' + dom) + path
    base = href.split('#')[0]
    frag = ('#' + href.split('#', 1)[1]) if '#' in href else ''
    if base in HREF:
        return HREF[base] + frag
    if href.startswith('#') or href.startswith('http') or href.startswith('mailto:') or href.startswith('tel:'):
        return href
    if href.startswith('/'):
        # dead paths in the designs -> the live dropdown targets (run 20260925-service-urls)
        dead = {'/services/rapid-prototyping/': '/services/rapid-prototyping-services/', '/services/hybrid-fabrication/': '/services-applications/'}
        return B + dead.get(href.split('#')[0], href.split('#')[0]) + (('#' + href.split('#', 1)[1]) if '#' in href else '')
    return href


def secs_of(key, name):
    s = BeautifulSoup(open(SCR + f'svc/Services - {name}.html', encoding='utf-8').read(), 'html.parser')
    for x in s.find_all(['script', 'style']):
        x.decompose()
    return s.body.find_all('section', recursive=False)


def save(pid, section, tok):
    json.dump([section], open(os.path.join(OUT, pid + '.json'), 'w'), indent=1, ensure_ascii=False)
    json.dump(tok.values, open(os.path.join(OUT, pid + '.values.json'), 'w'), indent=1, ensure_ascii=False)


def html_widget(t, markup, css='', eid=None):
    s = {'html': t('embed', markup)}
    if css:
        s['custom_css'] = css
    if eid:
        s['_element_id'] = eid
    return {'id': '0000000', 'elType': 'widget', 'widgetType': 'html', 'settings': s, 'elements': []}


def outer(children, bg=None, pad=(64, 24, 64, 24), css='', eid=None, **kw):
    s = dict(content_width='full', flex_direction='column', flex_gap=gap(0), padding=box(*pad), **kw)
    if bg:
        s['background_background'] = 'classic'
        s['background_color_hex'] = bg
    c = 'selector{position:relative;overflow:hidden}' + css
    s['custom_css'] = c
    if eid:
        s['_element_id'] = eid
    return container(children, **s)


def boxed(children, width=1260, **kw):
    kw.setdefault('flex_direction', 'column')
    kw.setdefault('flex_gap', gap(0))
    # Snippet #10 caps .e-con-inner at 1224px on services posts; the refreshed designs are 1260 wide
    kw['custom_css'] = f'selector.e-con > .e-con-inner{{max-width:{width}px!important}}' + kw.get('custom_css', '')
    return container(children, content_width='boxed', boxed_width=px(width), **kw)


def label(t, value, color=ORANGE, ls=1.98, size=11, weight='700', align=None, **kw):
    return heading(t('heading', value), size, weight, color=color, lh=16.5, ls=ls, upper=True, align=align, **kw)


def pill_btn(t, lbl, url, primary=True, size=14, pad=(14, 32), ls=0.7, border_hex='rgba(255,255,255,0.35)', fg='#FFFFFF', **kw):
    css = f'selector .elementor-button{{letter-spacing:{ls}px;text-transform:uppercase;line-height:20px}}'
    if primary:
        return button(t('button', lbl), t('url', url), size=size, weight='700', pad=pad, css=css, **kw)
    return button(t('button', lbl), t('url', url), bg='rgba(0,0,0,0)', fg=fg, size=size, weight='700', pad=(pad[0] - 1, pad[1]),
                  border=border_hex, css=css + 'selector .elementor-button{border-width:1.8px!important}', **kw)


# ============================================================ HTML-widget sections
def scoped(key, name):
    """design markup + scoped CSS for one section, as extracted from the rendered design."""
    # mhd's explorer and 3dp's quote were captured in their own tweak defaults (explorer Current / quote Detailed);
    # we build Example + Compact everywhere, so take those two sections' CSS from cnc's capture
    src = 'cnc' if (key, name) in (('mhd', 'appx'), ('3dp', 'quote')) else key
    css = open(SCR + f'meas/{src}-{name}.css', encoding='utf-8').read()
    css = re.sub(r'^/\* errs \d+ \*/\n', '', css)
    css = re.sub(r'@import[^;]+;', '', css)
    markup = open(SCR + f'meas/{key}-{name}.html', encoding='utf-8').read()
    return markup, css


def fix_markup(soup):
    for a in soup.find_all('a', href=True):
        a['href'] = link(a['href'])
    for el in soup.find_all(string=True):
        if 'Potomac' in el:
            el.replace_with(brand(str(el)))
    for el in soup.find_all(class_=re.compile(r'\breveal\b')):
        el['class'] = [c for c in el['class'] if c not in ('reveal', 'd1', 'd2', 'd3', 'd4', 'd5')]


def html_section(t, key, name, transform=None, script='', eid=None):
    markup, css = scoped(key, name)
    soup = BeautifulSoup(markup, 'html.parser')
    sec = soup.find('section')
    sec['class'] = ['pl-svc-' + name] + [c for c in sec.get('class', []) if not c.startswith('pl-svc-')]
    fix_markup(soup)
    if transform:
        transform(soup, sec)
    # keep the design's own section id: its CSS targets it (e.g. #applications.appx-on); the anchor lives there too
    if sec.get('id'):
        eid = None
    body = str(sec)
    body = re.sub(r'\n\s*\n+', '\n', body)
    # the theme sets `ul li{padding:5px 20px 5px 0}`; reset it under the scope, before the design rules so they win ties
    reset = f'.pl-svc-{name} li{{padding:0}}'
    out = f'<style>{reset}{css}</style>{body}{script}'
    w = html_widget(t, out)
    return outer([w], pad=(0, 0, 0, 0), eid=eid, css='selector > .e-con-inner, selector{max-width:none}')


def t_appx(soup, sec):
    if 'appx-on' not in sec['class']:
        sec['class'].append('appx-on')
    for el in sec.select('.appx-orig'):
        el.decompose()
    tabs = {b.get('data-app-id') for b in sec.select('.app-tab')}
    for p in sec.select('[data-app-panel]'):
        if p.get('data-app-layout') != 'example' or p.get('data-app-panel') not in tabs:
            p.decompose()
    first = sec.select_one('.app-tab')
    for b in sec.select('.app-tab'):
        b.attrs.pop('onclick', None)
        on = b is first
        b['class'] = [c for c in b.get('class', []) if c != 'active'] + (['active'] if on else [])
        b['aria-selected'] = 'true' if on else 'false'
    for p in sec.select('[data-app-panel]'):
        if p.get('data-app-panel') == first.get('data-app-id'):
            p.attrs.pop('hidden', None)
        else:
            p['hidden'] = ''
    for c in sec.select('.appx-chip'):          # informational pills (decision 2026-09-25)
        c.name = 'span'
        c.attrs = {'class': c.get('class', [])}
    for b in sec.select('[onclick]'):
        oc = b['onclick']
        if 'goToQuoteUpload' in oc or 'openBasket' in oc:
            a = soup.new_tag('a', href='#quote', **{'class': ' '.join(b.get('class', []))})
            a.string = b.get_text(strip=True)
            b.replace_with(a)
        elif 'openMatDetail' in oc or 'addToBasket' in oc:
            b.decompose()
        else:
            del b['onclick']


APPX_JS = ('<script>(function(){var s=document.currentScript.previousElementSibling;if(!s||s.dataset.plWired)return;'
           's.dataset.plWired="1";function go(id){s.querySelectorAll(".app-tab").forEach(function(t){var on=t.dataset.appId===id;'
           't.classList.toggle("active",on);t.setAttribute("aria-selected",on?"true":"false")});'
           's.querySelectorAll("[data-app-panel]").forEach(function(p){p.hidden=p.dataset.appPanel!==id})}'
           's.querySelectorAll(".app-tab").forEach(function(t){t.addEventListener("click",function(){go(t.dataset.appId)})});})();</script>')


def t_quote(soup, sec):
    for f in sec.select('form[data-quote-variant="detailed"]'):
        f.decompose()
    forms = sec.select('form[data-quote-variant="compact"]')
    for extra in forms[1:]:
        extra.decompose()
    f = forms[0]
    if f.has_attr('hidden'):   # 3dp was captured with the Detailed form showing
        del f['hidden']
    f['id'] = 'pl-rq-form'
    f['novalidate'] = ''
    del f['data-quote-variant']
    names = ['first_name', 'last_name', 'company', 'email']
    for inp, n in zip(f.select('input[type=text], input[type=email]'), names):
        inp['name'] = n
        inp['id'] = 'pl-rq-' + n
        inp['required'] = ''
    ta = f.select_one('textarea')
    ta['name'] = 'description'; ta['id'] = 'pl-rq-desc'; ta['required'] = ''
    fi = f.select_one('input[type=file]')
    fi['name'] = 'file'; fi['id'] = 'pl-rq-file'
    btn = f.select_one('.gf-rapid-actions button')
    btn['type'] = 'submit'; btn['id'] = 'pl-rq-submit'
    card = sec.select_one('.gf-rapid-card')
    card['id'] = 'pl-rq-card'


QUOTE_JS = r'''<script>(function(){
var f=document.getElementById('pl-rq-form');if(!f||f.dataset.plWired)return;f.dataset.plWired='1';
var PORTAL='143181153',FORM='9dba7d36-e36b-4a10-9411-9dc073dab7a0',UPLOAD='/wp-json/cnc-quote/v1/upload';
var card=document.getElementById('pl-rq-card');
function utm(){var o={},q=new URLSearchParams(location.search);['utm_source','utm_medium','utm_campaign','utm_term','utm_content'].forEach(function(k){var v=q.get(k);if(v)o[k]=v});return o}
function hutk(){var m=document.cookie.match(/(?:^|;\s*)hubspotutk=([^;]+)/);return m?m[1]:''}
function track(ev,p){try{(window.dataLayer=window.dataLayer||[]).push(Object.assign({event:ev,form_id:'rapid_response_quote'},p||{}))}catch(e){}}
function err(msg){var o=card.querySelector('.pl-rq-err');if(!o){o=document.createElement('p');o.className='pl-rq-err';o.setAttribute('role','alert');o.style.cssText='margin:0 0 14px;padding:10px 14px;border-radius:8px;background:#FEF2F2;border:1px solid #FECACA;color:#B91C1C;font-size:13px;line-height:1.5';f.parentNode.insertBefore(o,f)}o.textContent=msg}
function v(id){var e=document.getElementById(id);return e?(e.value||'').trim():''}
async function upload(){var i=document.getElementById('pl-rq-file');if(!i||!i.files||!i.files[0])return '';var fd=new FormData();fd.append('file',i.files[0]);
 try{var r=await fetch(UPLOAD,{method:'POST',body:fd});var j=await r.json();if(r.ok&&j&&j.url)return j.url;err('That file could not be uploaded ('+((j&&j.error)||'unknown')+'). Send the request without it, or try a smaller file.');return null}
 catch(e){err('That file could not be uploaded. Send the request without it, or try again.');return null}}
f.addEventListener('submit',async function(ev){ev.preventDefault();var o=card.querySelector('.pl-rq-err');if(o)o.remove();
 var d={firstname:v('pl-rq-first_name'),lastname:v('pl-rq-last_name'),company:v('pl-rq-company'),email:v('pl-rq-email'),potomac_project_description:v('pl-rq-desc')};
 if(!d.firstname||!d.lastname||!d.company||!d.email||!d.potomac_project_description){err('Please fill in every field marked *.');track('lead_form_submit_error',{error:'validation'});return}
 if(!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(d.email)){err('That email address does not look right. Please check it.');track('lead_form_submit_error',{error:'email'});return}
 var btn=document.getElementById('pl-rq-submit');btn.disabled=true;var url=await upload();if(url===null){btn.disabled=false;return}
 d.potomac_project_name='Rapid Response Quote — '+document.title;if(url)d.potomac_file_submission=url;d.hs_lead_status='NEW';d.lifecyclestage='lead';var u=utm(),k;for(k in u)d[k]=u[k];
 var props=Object.keys(d).filter(function(k){return d[k]!=null&&d[k]!==''}).map(function(k){return{objectTypeId:'0-1',name:k,value:String(d[k])}});
 track('lead_form_submit',{fields_completed:props.length});
 try{var r=await fetch('https://api.hsforms.com/submissions/v3/integration/submit/'+PORTAL+'/'+FORM,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({fields:props,context:{pageName:document.title,pageUri:location.href,hutk:hutk()||undefined}})});
  var j=await r.json().catch(function(){return{}});
  if(r.ok){track('lead_form_submit_success');var items=card.querySelectorAll('.gf-rapid-progress-item');if(items[1])items[1].classList.add('active');var t=card.querySelector('.gf-rapid-form-title');if(t)t.textContent='Request received';
   var p=document.createElement('p');p.className='gf-rapid-note';p.innerHTML='<strong>Received.</strong> An engineer will review your part and reply within 24 hours.';f.replaceWith(p);return}
  console.error('HubSpot submit failed',r.status,j);err('We could not send that just now. Please check your connection, or email inq@goodfellow.com.');track('lead_form_submit_error',{error:'http_'+r.status})}
 catch(e){console.error(e);err('We could not send that just now. Please check your connection, or email inq@goodfellow.com.');track('lead_form_submit_error',{error:'network'})}
 btn.disabled=false});
})();</script>'''


def t_static(soup, sec):
    for b in sec.select('[onclick]'):
        oc = b['onclick']
        if 'goToQuoteUpload' in oc or 'openBasket' in oc:
            a = soup.new_tag('a', href='#quote', **{'class': ' '.join(b.get('class', []))})
            a.string = b.get_text(strip=True)
            b.replace_with(a)
        else:
            del b['onclick']


# ============================================================ native sections
def txt_(el):
    return clean(el.get_text(' ', strip=True)).replace(' ,', ',').replace(' .', '.')


HERO_DECOR = ('<div class="pl-hero-decor" aria-hidden="true">'
              '<div style="position:absolute;inset:0;background-image:linear-gradient(rgba(245,130,31,.05) 1px,transparent 1px),linear-gradient(90deg,rgba(245,130,31,.05) 1px,transparent 1px),linear-gradient(rgba(255,255,255,.02) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.02) 1px,transparent 1px);background-size:80px 80px,80px 80px,16px 16px,16px 16px"></div>'
              '<div style="position:absolute;left:0;right:0;top:50%;height:1px;background:rgba(255,255,255,.04)"></div>'
              '<div style="position:absolute;left:-5%;top:18%;width:42%;height:68%;background:radial-gradient(rgba(245,130,31,.08) 0%,transparent 65%)"></div>'
              '<div style="position:absolute;right:8%;top:-8%;width:48%;height:118%;background:radial-gradient(at 55% 35%,rgba(29,53,87,.45) 0%,transparent 62%)"></div>'
              '<div class="pl-hero-art" style="position:absolute;right:0;top:0;bottom:0;width:56%;opacity:.14">{svg}</div></div>')
HERO_DECOR_CSS = ('selector{position:absolute!important;inset:0;z-index:0;pointer-events:none;margin:0!important}'
                  'selector .pl-hero-decor{position:absolute;inset:0}'
                  'selector .pl-hero-art svg{width:100%;height:100%}'
                  '@media(max-width:1023px){selector .pl-hero-art{display:none}}')


def hero(t, sec, svg):
    col = sec.select_one('.max-w-\\[620px\\]')
    eb = txt_(col.select_one('.ha1'))
    h1 = col.find('h1')
    for sp in h1.find_all('span'):
        sp.attrs = {'style': 'color:#F5821F'}
    h1_html = brand(re.sub(r'\s+', ' ', ''.join(str(c) for c in h1.contents)).strip())
    lede = inner(col.find('p', class_='ha3'))
    lede = re.sub(r'<strong[^>]*>', '<strong>', lede)
    btns = col.select('.ha4 > *')
    notes = [txt_(p) for p in col.select('.space-y-1\\.5 p')]
    stats = [(txt_(d.select('div')[0]), txt_(d.select('div')[1])) for d in col.select('.ha5 > div')]
    b0, b1, b2 = btns[0], btns[1], btns[2]
    row = container([
        pill_btn(t, txt_(b0), '#quote', size=14, pad=(14, 32),
                 shadow='0 8px 24px rgba(245,130,31,.3)'),
        pill_btn(t, txt_(b1), link(b1.get('href')), primary=False, size=14, pad=(14, 32)),
        button(t('button', txt_(b2)), t('url', link(b2.get('href'))), bg='rgba(0,0,0,0)', fg='rgba(255,255,255,0.8)', size=12, weight='700',
               pad=(0, 0), css='selector .elementor-button{letter-spacing:1.92px;text-transform:uppercase;line-height:16px;padding:0!important}'),
    ], flex_direction='row', flex_wrap='wrap', flex_align_items='center', flex_gap=gap(12, 12), _margin=box(0, 0, 20, 0),
        custom_css='selector > .elementor-widget:nth-child(3){margin-left:12px}')
    notes_w = container([
        text(t('body', f'<p>{notes[0]}</p>'), 14, color='rgba(255,255,255,0.7)', lh=22.75),
        text(t('body', f'<p>{notes[1]}</p>'), 14, color='rgba(255,255,255,0.52)', lh=22.75, _margin=box(6, 0, 0, 0)),
    ], flex_direction='column', flex_gap=gap(0), _margin=box(0, 0, 40, 0))
    cells = []
    for i, (v, l) in enumerate(stats):
        cells.append(container([
            heading(t('heading', v), 24.8, '800', color=ORANGE, lh=24.8, ls=-0.62, _margin=box(0, 0, 2, 0)),
            heading(t('heading', l), 10, '600', color='rgba(255,255,255,0.4)', lh=15, ls=0.25, upper=True),
        ], flex_direction='column', flex_gap=gap(0), padding=box(0, 20, 8, 0 if i == 0 else 20),
            custom_css=('' if i == 0 else 'selector{border-left:1px solid rgba(255,255,255,.1)}')))
    stat_row = container(cells, flex_direction='row', flex_gap=gap(0), padding=box(24, 0, 0, 0),
                         custom_css='selector{border-top:1px solid rgba(255,255,255,.1);display:grid!important;grid-template-columns:repeat(5,124px)}'
                                    '@media(max-width:767px){selector{grid-template-columns:repeat(2,1fr)}}')
    content = container([
        label(t, eb, _margin=box(0, 0, 20, 0)),
        heading(t('heading', h1_html), 64, '800', tag='h1', color='#FFFFFF', lh=67.2, ls=-1.92, _margin=box(0, 0, 24, 0),
                css='@media(max-width:767px){selector .elementor-heading-title{font-size:40px;line-height:44px}}'),
        text(t('body', f'<p>{lede}</p>'), 15, color='rgba(255,255,255,0.6)', lh=25.8, _element_width='initial',
             _element_custom_width=px(560), _margin=box(0, 0, 40, 0),
             extra_css='selector strong{color:rgba(255,255,255,.9);font-weight:700}'),
        row, notes_w, stat_row,
    ], flex_direction='column', flex_gap=gap(0), width=px(620), width_mobile={'unit': '%', 'size': 100})
    decor = html_widget(t, HERO_DECOR.replace('{svg}', svg), HERO_DECOR_CSS)
    return container([decor, boxed([content], padding=box(56, 24, 56, 24), custom_css='selector{position:relative;z-index:1}')],
                     content_width='full', flex_direction='column', flex_justify_content='center', flex_gap=gap(0), padding=box(0),
                     min_height=px(440), background_background='gradient', background_color_hex=NAVYDP,
                     custom_css='selector{position:relative;overflow:hidden;background-image:linear-gradient(135deg,#0D1B2A 0%,#15253D 55%,#1A2F4A 100%)!important}')


def whyus(t, sec, asset):
    right = sec.select('.max-w-page > div')[1]
    badge = txt_(right.find('div'))
    h2 = txt_(right.find('h2'))
    lede = txt_(right.find('p'))
    items = []
    for it in right.select('.flex.flex-col > div'):
        p = it.find('p')
        items.append(inner(p).replace('<strong class="text-navy-mid font-bold">', '<strong>'))
    inset = right.select('.rounded-\\[18px\\]')[0]
    ititle = txt_(inset.find('p'))
    ib = inset.select('.flex.flex-wrap > *')
    inotes = [txt_(p) for p in inset.select('.space-y-1 p')]
    bullets = [container([
        container([], width=px(8), min_height=px(8), background_background='classic', background_color_hex=ORANGE,
                  border_radius={'unit': '%', 'top': '50', 'right': '50', 'bottom': '50', 'left': '50', 'isLinked': True},
                  _margin=box(9, 0, 0, 0), custom_css='selector{flex-shrink:0}'),
        text(t('body', f'<p>{h}</p>'), 14, color=GRAY500, lh=23.8, extra_css='selector strong{color:#1D3557;font-weight:700}'),
    ], flex_direction='row', flex_align_items='flex-start', flex_gap=gap(12, 12), flex_wrap='nowrap') for h in items]
    photo = container([image(t('image', {'asset': asset}), css='selector{position:absolute;inset:0;margin:0}selector img{width:100%;height:100%;object-fit:cover;display:block}')],
                      min_height=px(360), border_radius=box(8),
                      custom_css='selector{position:relative;overflow:hidden;flex:1.05 1 0}selector::after{content:"";position:absolute;inset:0;'
                                 'background:linear-gradient(to top,rgba(21,37,61,.18),transparent 55%,rgba(21,37,61,.08))}'
                                 '@media(max-width:1023px){selector{flex:1 1 100%}}')
    ins = container([
        heading(t('heading', ititle), 18, '800', color=NAVYMID, lh=22.5, _margin=box(0, 0, 12, 0)),
        container([
            button(t('button', txt_(ib[0])), t('url', '#quote'), size=12, weight='700', pad=(12, 24),
                   shadow='0 10px 24px rgba(245,130,31,.18)', css='selector .elementor-button{letter-spacing:.6px;text-transform:uppercase;line-height:16px}'),
            button(t('button', txt_(ib[1])), t('url', link(ib[1].get('href'))), bg='#FFFFFF', fg=NAVY, size=12, weight='700', pad=(11, 24),
                   border=GRAY200, css='selector .elementor-button{letter-spacing:.6px;text-transform:uppercase;line-height:16px}'),
        ], flex_direction='row', flex_wrap='wrap', flex_gap=gap(12, 12), _margin=box(0, 0, 12, 0)),
        text(t('body', f'<p>{inotes[0]}</p>'), 12, color=GRAY500, lh=19.5),
        text(t('body', f'<p>{inotes[1]}</p>'), 12, color=GRAY400, lh=19.5, _margin=box(4, 0, 0, 0)),
    ], flex_direction='column', flex_gap=gap(0), padding=box(20), background_background='classic', background_color_hex='#F9FAFB',
        border_border='solid', border_width=box(1), border_color=GRAY200, border_radius=box(18))
    copy = container([
        heading(t('heading', badge), 11, '700', color=NAVYMID, lh=16.5, ls=1.98, upper=True, _margin=box(0, 0, 16, 0),
                css='selector{align-self:flex-start}selector .elementor-heading-title{display:inline-flex;padding:6px 16px;border-radius:9999px;background:rgba(21,37,61,.06)}'),
        heading(t('heading', h2), 43.2, '800', tag='h2', color=NAVYMID, lh=54, ls=-1.08, _margin=box(0, 0, 16, 0)),
        text(t('body', f'<p>{lede}</p>'), 15, color=GRAY500, lh=26.25, _element_width='initial', _element_custom_width=px(540), _margin=box(0, 0, 28, 0)),
        container(bullets, flex_direction='column', flex_gap=gap(16, 16), _margin=box(0, 0, 32, 0)),
        ins,
    ], flex_direction='column', flex_gap=gap(0), custom_css='selector{flex:1 1 0}@media(max-width:1023px){selector{flex:1 1 100%}}')
    return outer([boxed([container([photo, copy], flex_direction='row', flex_wrap='wrap', flex_align_items='center', flex_gap=gap(32, 32))])],
                 bg='#FFFFFF', pad=(64, 24, 64, 24))


def services(t, sec, assets):
    head = sec.select_one('.gf-services-head')
    kick, h2, copy = txt_(head.select_one('.gf-services-kicker')), txt_(head.find('h2')), txt_(head.select_one('.gf-services-copy'))
    cta = head.select_one('.gf-services-cta')
    cta_lbl = clean(cta.get_text(' ', strip=True))
    cards = []
    for a, asset in zip(sec.select('.gf-service-card'), assets):
        b = a.select_one('.gf-service-body')
        cards.append(container([
            image(t('image', {'asset': asset}), css='selector{margin:0;line-height:0}selector img{display:block;width:100%;height:198px;object-fit:cover}'),
            container([
                heading(t('heading', txt_(b.find('h3'))), 20, '800', tag='h3', color='#0F1F3A', lh=23.6, ls=-0.4, _margin=box(0, 0, 10, 0)),
                text(t('body', f'<p>{txt_(b.find("p"))}</p>'), 14, color='#111827', lh=21.28, _margin=box(0, 0, 22, 0)),
                heading(t('heading', clean(b.select_one('.gf-service-link').get_text(' ', strip=True))), 13, '800', color='#B9681F', lh=19.5,
                        css='selector{margin-top:auto;align-self:flex-start}selector .elementor-heading-title{display:inline-flex;align-items:center;gap:7px;padding:9px 13px;'
                            'background:#fff;border:1px solid #D5DCE7;border-radius:6px}'),
            ], flex_direction='column', flex_gap=gap(0), padding=box(22, 22, 20, 22), custom_css='selector{flex:1 1 auto}'),
        ], html_tag='a', link={'url': t('url', link(a.get('href'))), 'is_external': '', 'nofollow': ''},
            flex_direction='column', flex_gap=gap(0), background_background='classic', background_color_hex='#FFFFFF',
            border_border='solid', border_width=box(1), border_color='#E1E6EE', border_radius=box(8),
            custom_css='selector{overflow:hidden;box-shadow:0 12px 28px rgba(15,42,68,.08);transition:transform .3s,box-shadow .3s}'
                       'selector:hover{transform:translateY(-3px);box-shadow:0 18px 36px rgba(15,42,68,.12)}'))
    head_w = container([
        container([
            heading(t('heading', kick), 11, '800', color=ORANGE, lh=16.5, ls=1.98, upper=True, _margin=box(0, 0, 12, 0)),
            heading(t('heading', h2), 50.4, '800', tag='h2', color='#22395D', lh=53.424, ls=-1.512, _margin=box(0, 0, 14, 0),
                    css='@media(max-width:767px){selector .elementor-heading-title{font-size:34px;line-height:38px}}'),
            text(t('body', f'<p>{copy}</p>'), 17, color='#1F2937', lh=26.35, _element_width='initial', _element_custom_width=px(560)),
        ], flex_direction='column', flex_gap=gap(0), custom_css='selector{flex:1 1 0}'),
        button(t('button', cta_lbl), t('url', link(cta.get('href'))), size=13, weight='800', pad=(17, 28),
               css='selector{margin-top:18px}selector .elementor-button{letter-spacing:1.04px;text-transform:uppercase;line-height:19.5px}'),
    ], flex_direction='row', flex_wrap='wrap', flex_justify_content='space-between', flex_align_items='flex-start', flex_gap=gap(28, 28),
        _margin=box(0, 0, 34, 0))
    grid = container(cards, flex_direction='row', flex_gap=gap(22, 22), flex_align_items='stretch',
                     custom_css='selector{display:grid!important;grid-template-columns:repeat(5,minmax(0,1fr))}'
                                '@media(max-width:1179px){selector{grid-template-columns:repeat(3,minmax(0,1fr))}}'
                                '@media(max-width:767px){selector{grid-template-columns:1fr}}')
    return outer([boxed([head_w, grid])], bg='#F8FAFC', pad=(64, 24, 72, 24),
                 css='selector{border-top:1px solid #EEF2F7;border-bottom:1px solid #EEF2F7}', eid='services')


def centered_head(t, eb, h2, sub=None, h2_size=40, h2_lh=47.2, h2_ls=-1, h2_color=NAVYMID, sub_color=GRAY500, eb_weight='800',
                  mb=34, sub_lh=25.5, sub_w=720, h2_w=760, eb_mb=12, sub_mt=10):
    kids = [heading(t('heading', eb), 11, eb_weight, color=ORANGE, lh=16.5, ls=1.98, upper=True, align='center', _margin=box(0, 0, eb_mb, 0)),
            heading(t('heading', h2), h2_size, '800', tag='h2', color=h2_color, lh=h2_lh, ls=h2_ls, align='center',
                    _element_width='initial', _element_custom_width=px(h2_w))]
    if sub:
        kids.append(text(t('body', f'<p>{sub}</p>'), 15, color=sub_color, lh=sub_lh, align='center', _element_width='initial',
                         _element_custom_width=px(sub_w), _margin=box(sub_mt, 0, 0, 0)))
    return container(kids, flex_direction='column', flex_align_items='center', flex_gap=gap(0), _margin=box(0, 0, mb, 0))


def workflow(t, sec):
    head = sec.select_one('.gf-workflow-head')
    steps = []
    for st in sec.select('.gf-workflow-step'):
        active = 'active' in st.get('class', [])
        card = st.select_one('.gf-workflow-card')
        svg = card.select_one('.gf-workflow-icon svg')
        svg_html = re.sub(r'\s+', ' ', str(svg)) if svg else ''
        minis = [txt_(m) for m in card.select('.gf-workflow-mini')]
        kids = [
            heading(t('heading', txt_(card.select_one('.gf-workflow-label'))), 10, '800', color=ORANGE if active else GRAY400, lh=15, ls=2.2,
                    upper=True, align='center', _margin=box(0, 0, 14, 0)),
            html_widget(t, f'<div class="pl-wf-icon">{svg_html}</div>',
                        'selector{margin:0 0 14px!important}selector .pl-wf-icon{width:42px;height:42px;border-radius:12px;background:#F7F9FC;'
                        'border:1px solid #E7ECF3;display:flex;align-items:center;justify-content:center;margin:0 auto}'
                        'selector .pl-wf-icon svg{width:23px;height:23px}'),
            heading(t('heading', txt_(card.select_one('.gf-workflow-card-title'))), 15, '800', tag='h3', color=NAVY, lh=19.5, ls=-0.45,
                    align='center', _margin=box(0, 0, 12, 0)),
            text(t('body', f'<p>{txt_(card.select_one(".gf-workflow-card-copy"))}</p>'), 13, color=GRAY500, lh=20.8, align='center'),
        ]
        for m in minis:
            kids.append(text(t('body', f'<p class="pl-mini">{m}</p>'), 12, color=GRAY500, lh=18, align='center',
                             extra_css='selector p.pl-mini::before{content:"";display:inline-block;width:6px;height:6px;border-radius:50%;background:#F5821F;margin-right:9px;vertical-align:middle;opacity:.65}'))
        steps.append(container([
            heading(t('heading', txt_(st.select_one('.gf-workflow-num'))), 18, '800', color=NAVY, lh=27, align='center', _margin=box(0, 0, 12, 0),
                    css='selector{align-self:center;position:relative;z-index:1}selector .elementor-heading-title{width:50px;height:50px;border-radius:9999px;background:#fff;'
                        'border:2px solid rgba(245,130,31,.38);box-shadow:0 8px 24px rgba(245,130,31,.08);display:flex;align-items:center;justify-content:center}'),
            container(kids, flex_direction='column', flex_align_items='center', flex_gap=gap(0), padding=box(22, 18, 20, 18),
                      background_background='classic', background_color_hex='#FFFFFF', border_border='solid', border_width=box(1),
                      border_color='rgba(245,130,31,0.45)' if active else GRAY200, border_radius=box(8),
                      custom_css=('selector{box-shadow:0 8px 24px rgba(245,130,31,.08);flex:1 1 auto}' if active else
                                  'selector{box-shadow:0 2px 8px rgba(0,0,0,.07);flex:1 1 auto}')),
        ], flex_direction='column', flex_align_items='stretch', flex_gap=gap(0)))
    note = sec.select_one('.gf-workflow-note')
    tl = container(steps, flex_direction='row', flex_gap=gap(18, 18), flex_align_items='stretch', _margin=box(34, 0, 0, 0),
                   custom_css='selector{position:relative;display:grid!important;grid-template-columns:repeat(5,minmax(0,1fr))}'
                              "selector::before{content:'';position:absolute;top:28px;left:7%;right:7%;height:1px;background:linear-gradient(90deg,rgba(245,130,31,.15),rgba(245,130,31,.5),rgba(245,130,31,.15));z-index:0}"
                              '@media(max-width:1023px){selector{grid-template-columns:repeat(2,minmax(0,1fr))}selector::before{display:none}}'
                              '@media(max-width:639px){selector{grid-template-columns:1fr}}')
    kids = [centered_head(t, txt_(head.select_one('.gf-workflow-kicker')), txt_(head.find('h2')), txt_(head.select_one('.gf-workflow-sub')),
                          mb=0, h2_w=760, sub_w=720), tl]
    if note:
        kids.append(text(t('body', f'<p>{txt_(note)}</p>'), 14, color=GRAY500, lh=21, align='center', _margin=box(24, 0, 0, 0),
                         extra_css='selector p::before{content:"";display:inline-block;width:14px;height:14px;box-sizing:border-box;border-radius:50%;border:2px solid rgba(245,130,31,.45);margin-right:10px;vertical-align:-2px}'))
    return outer([boxed(kids)], bg='#FFFFFF', pad=(62, 24, 52, 24), eid='process')


def group(t, sec, assets):
    hd = sec.select_one('.mb-8.text-center')
    cols = sec.select('.grid.gap-5 > div')
    cards = []
    for c, asset in zip(cols, assets):
        lab = txt_(c.find('div'))
        box_ = c.select('div')[1]
        here = box_.find(string=re.compile('You are here'))
        bullets = [txt_(s) for s in box_.select('.flex.flex-col span')]
        a = box_.find('a')
        primary = a is not None and 'bg-orange' in ' '.join(a.get('class', []))
        kids = []
        if here:
            kids.append(heading(t('heading', clean(str(here))), 10, '700', color=ORANGE, lh=15, ls=1, upper=True,
                                css='selector{position:absolute!important;top:20px;right:20px}selector .elementor-heading-title{padding:4px 12px;border-radius:9999px;background:rgba(245,130,31,.1)}'))
        kids.append(container([image(t('image', {'asset': asset}), css='selector{margin:0;line-height:0}selector img{height:48px;width:auto;display:block}')],
                              min_height=px(52), flex_direction='row', flex_align_items='center', padding=box(20 if here else 0, 0, 0, 0)))
        kids.append(container([container([
            container([], width=px(6), min_height=px(6), background_background='classic', background_color_hex=ORANGE, _margin=box(7, 0, 0, 0),
                      border_radius={'unit': '%', 'top': '50', 'right': '50', 'bottom': '50', 'left': '50', 'isLinked': True}, custom_css='selector{flex-shrink:0}'),
            text(t('body', f'<p>{b}</p>'), 14, color=GRAY500, lh=20),
        ], flex_direction='row', flex_align_items='flex-start', flex_gap=gap(8, 8), flex_wrap='nowrap') for b in bullets],
            flex_direction='column', flex_gap=gap(8, 8), custom_css='selector{flex:1 1 auto}'))
        if a is not None:
            css = 'selector{margin-top:4px;align-self:flex-start}selector .elementor-button{letter-spacing:.6px;text-transform:uppercase;line-height:16px}'
            if primary:
                kids.append(button(t('button', txt_(a)), t('url', link(a.get('href'))), size=12, weight='700', pad=(10, 20), css=css))
            else:
                kids.append(button(t('button', txt_(a)), t('url', link(a.get('href'))), bg='rgba(0,0,0,0)', fg=NAVYMID, size=12, weight='700', pad=(9, 20),
                                   border=NAVYMID, css=css + 'selector .elementor-button{border-width:1.8px!important}'))
        cards.append(container([
            heading(t('heading', lab), 12, '400', color=GRAY400, lh=16, ls=0.6, upper=True, _margin=box(0, 0, 8, 0),
                    # LM/MHD/RP/3DP designs bottom-align the labels in a 34px box (CNC's does not)
                    css=('selector{min-height:34px;display:flex;align-items:flex-end;margin-bottom:8px!important}' if 'min-h-[34px]' in c.find('div').get('class', []) else None)),
            container(kids, flex_direction='column', flex_gap=gap(16, 16), padding=box(24), background_background='classic', background_color_hex='#FFFFFF',
                      border_border='solid', border_width=box(2 if here else 1), border_color='rgba(245,130,31,0.4)' if here else GRAY200, border_radius=box(8),
                      custom_css='selector{position:relative;flex:1 1 auto}'),
        ], flex_direction='column', flex_gap=gap(0)))
    grid = container(cards, flex_direction='row', flex_gap=gap(20, 20), flex_align_items='stretch',
                     custom_css='selector{display:grid!important;grid-template-columns:repeat(4,minmax(0,1fr))}'
                                '@media(max-width:1279px){selector{grid-template-columns:repeat(2,minmax(0,1fr))}}@media(max-width:767px){selector{grid-template-columns:1fr}}')
    head = centered_head(t, txt_(hd.find('span')), txt_(hd.find('h2')), txt_(hd.find('p')), h2_lh=50, h2_color='#FFFFFF', sub_color='#FFFFFF',
                         eb_weight='700', mb=32, sub_lh=24.375, sub_w=760, h2_w=1260, eb_mb=16, sub_mt=12)
    return outer([boxed([head, grid])], bg='#152C4A', pad=(56, 24, 56, 24),
                 css='selector{background-image:linear-gradient(rgba(255,255,255,.035) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.035) 1px,transparent 1px),'
                     'linear-gradient(rgba(255,255,255,.01) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.01) 1px,transparent 1px);'
                     'background-size:160px 160px,160px 160px,20px 20px,20px 20px;border-top:1px solid #F3F4F6;border-bottom:1px solid #F3F4F6}')


def testimonials(t, sec):
    hd = sec.select_one('.text-center.mb-8')
    cards = []
    for c in sec.select('.grid.gap-4 > div'):
        stars = txt_(c.find('div'))
        q = txt_(c.find('p'))
        foot = c.select('div.flex.items-center')[0]
        ini = txt_(foot.select('div')[0])
        name = txt_(foot.select('div div')[0]); co = txt_(foot.select('div div')[1])
        cards.append(container([
            heading(t('heading', stars), 14, '400', color=ORANGE, lh=20, ls=1.4),
            text(t('body', f'<p>{q}</p>'), 15, color=NAVY, lh=24.75, extra_css='selector p{font-style:italic}selector{flex:1 1 auto}'),
            container([
                heading(t('heading', ini), 12, '700', color='#FFFFFF', lh=16, align='center',
                        css='selector .elementor-heading-title{width:36px;height:36px;border-radius:9999px;background:#15253D;display:flex;align-items:center;justify-content:center}'),
                container([heading(t('heading', name), 14, '700', color=NAVYMID, lh=20), heading(t('heading', co), 12, '400', color=GRAY400, lh=16)],
                          flex_direction='column', flex_gap=gap(0)),
            ], flex_direction='row', flex_align_items='center', flex_gap=gap(12, 12), padding=box(12, 0, 0, 0),
                custom_css='selector{border-top:1px solid #F3F4F6}'),
        ], flex_direction='column', flex_gap=gap(12, 12), padding=box(24), background_background='classic', background_color_hex='#FFFFFF',
            border_border='solid', border_width=box(1), border_color=GRAY200, border_radius=box(8)))
    grid = container(cards, flex_direction='row', flex_gap=gap(16, 16), flex_align_items='stretch',
                     custom_css='selector{display:grid!important;grid-template-columns:repeat(3,minmax(0,1fr))}'
                                '@media(max-width:1279px){selector{grid-template-columns:repeat(2,minmax(0,1fr))}}@media(max-width:767px){selector{grid-template-columns:1fr}}')
    head = container([
        heading(t('heading', txt_(hd.find('span'))), 11, '700', color=ORANGE, lh=16.5, ls=1.98, upper=True, align='center', _margin=box(0, 0, 8, 0)),
        heading(t('heading', txt_(hd.find('h2'))), 35.2, '800', tag='h2', color=NAVYMID, lh=44, ls=-0.88, align='center'),
    ], flex_direction='column', flex_align_items='center', flex_gap=gap(0), _margin=box(0, 0, 32, 0))
    return outer([boxed([head, grid])], bg='#F9FAFB', pad=(56, 24, 56, 24))


FAQ_CSS = (
    'selector .elementor-toggle-item{border:0;border-bottom:1px solid #F3F4F6;background:transparent;margin:0}'
    'selector .elementor-tab-title{display:flex!important;align-items:center;justify-content:space-between;gap:20px;'
    'padding:20px 0;border:0;background:transparent;font:700 15px/22.5px Inter,system-ui,sans-serif;color:#1D3557;cursor:pointer}'
    'selector .elementor-toggle-title{order:1;flex:1 1 auto;color:inherit}'
    'selector .elementor-toggle-icon{order:2;margin:0;width:28px;height:28px;min-width:28px;border:1.4px solid #D1D5DB;border-radius:50%;'
    'display:flex;align-items:center;justify-content:center;flex-shrink:0;float:none;transition:transform .3s cubic-bezier(.25,.46,.45,.94)}'
    'selector .elementor-toggle-icon *{display:none!important}'
    "selector .elementor-toggle-icon::before{content:'+';display:block;font-size:18px;font-weight:700;line-height:1;color:#6B7280}"
    'selector .elementor-tab-title.elementor-active .elementor-toggle-icon{transform:rotate(45deg)}'
    'selector .elementor-tab-content{border:0;padding:0 0 20px;font-size:14px;line-height:24.92px;color:#6B7280}'
    'selector .elementor-tab-content p{margin:0;font-size:14px;line-height:24.92px}')


def faq(t, sec):
    left = sec.find('div').find_all('div', recursive=False)[0]   # sticky on CNC only in the designs; built sticky on all five
    items = []
    for it in sec.select('.faq-item'):
        q = txt_(it.select_one('.faq-trigger')).rstrip('+').strip()
        body = it.select_one('.faq-body')
        a = inner(body.find('div') or body)
        items.append((q, a))
    tabs = [{'tab_title': t('faq_q', q), 'tab_content': t('faq_a', f'<p>{a}</p>' if not a.startswith('<p') else a), '_id': f'{i + 1:07x}'}
            for i, (q, a) in enumerate(items)]
    tog = {'id': '0000000', 'elType': 'widget', 'widgetType': 'toggle', 'settings': {
        'tabs': tabs, 'selected_icon': {'value': 'fas fa-plus', 'library': 'fa-solid'},
        'selected_active_icon': {'value': 'fas fa-minus', 'library': 'fa-solid'}, 'custom_css': FAQ_CSS}, 'elements': []}
    a = left.find('a')
    lcol = container([
        label(t, txt_(left.select_one('.eyebrow-text')), _margin=box(0, 0, 12, 0)),
        heading(t('heading', txt_(left.find('h2'))), 27.2, '800', tag='h2', color=NAVYMID, lh=34, ls=-0.68, _margin=box(0, 0, 12, 0)),
        text(t('body', f'<p>{txt_(left.find("p"))}</p>'), 14, color=GRAY500, lh=22.75, _margin=box(0, 0, 20, 0)),
        button(t('button', txt_(a)), t('url', link(a.get('href'))), bg='rgba(0,0,0,0)', fg=NAVY, size=12, weight='700', pad=(11, 20), border=NAVY,
               css='selector{align-self:flex-start}selector .elementor-button{letter-spacing:.6px;text-transform:uppercase;line-height:16px;border-width:1.8px!important}'),
    ], flex_direction='column', flex_gap=gap(0), width=px(340), width_mobile={'unit': '%', 'size': 100},
        custom_css='selector{position:sticky;top:130px;align-self:flex-start}@media(max-width:1023px){selector{position:static}}')
    rcol = container([tog], flex_direction='column', flex_gap=gap(0), custom_css='selector{flex:1 1 0;border-top:1px solid #F3F4F6}@media(max-width:1023px){selector{flex:1 1 100%}}')
    return outer([boxed([container([lcol, rcol], flex_direction='row', flex_wrap='wrap', flex_align_items='flex-start', flex_gap=gap(32, 32))])],
                 bg='#FFFFFF', pad=(64, 24, 64, 24), eid='faq')


def closing(t, sec):
    c = sec.select_one('.max-w-\\[720px\\]')
    eb = txt_(c.select_one('span'))
    h2 = c.find('h2')
    h2_html = brand(re.sub(r'\s+', ' ', ''.join(str(x) for x in h2.contents)).strip())
    p = txt_(c.find('p'))
    b = c.select('.flex > *')
    return outer([boxed([
        label(t, eb, ls=2.42, align='center', _margin=box(0, 0, 20, 0)),
        heading(t('heading', h2_html), 59.24, '800', tag='h2', color='#FFFFFF', lh=60.42, ls=-2.07, align='center', _margin=box(0, 0, 20, 0),
                css='@media(max-width:767px){selector .elementor-heading-title{font-size:38px;line-height:40px}}'),
        text(t('body', f'<p>{p}</p>'), 16, color='#FFFFFF', lh=27.2, align='center', _element_width='initial', _element_custom_width=px(640),
             _margin=box(0, 0, 32, 0)),
        container([
            button(t('button', txt_(b[0])), t('url', link(b[0].get('href')) if b[0].name == 'a' else '#quote'), size=12, weight='700', pad=(16, 28),
                   css='selector .elementor-button{letter-spacing:1.44px;text-transform:uppercase;line-height:16px;min-width:170px;justify-content:center}'),
            button(t('button', txt_(b[1])), t('url', link(b[1].get('href')) if b[1].name == 'a' else '#quote'), bg='rgba(0,0,0,0)', fg='#FFFFFF', size=12,
                   weight='700', pad=(16, 28), border='rgba(255,255,255,0.25)',
                   css='selector .elementor-button{letter-spacing:1.44px;text-transform:uppercase;line-height:16px;min-width:170px;justify-content:center}'),
        ], flex_direction='row', flex_wrap='wrap', flex_justify_content='center', flex_align_items='center', flex_gap=gap(12, 12)),
    ], width=720, flex_align_items='center')], pad=(101, 24, 96, 24),
        css='selector{background-image:linear-gradient(135deg,#16253D 0%,#1B2E4A 52%,#213754 100%);border-top:1px solid rgba(255,255,255,.1)}'
            "selector::before{content:'';position:absolute;inset:0;opacity:.9;pointer-events:none;background-image:linear-gradient(rgba(255,255,255,.043) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.043) 1px,transparent 1px);background-size:28px 28px}"
            "selector::after{content:'';position:absolute;inset:0;pointer-events:none;background-image:radial-gradient(circle at 50% 14%,rgba(245,130,31,.1) 0%,transparent 18%),radial-gradient(circle,rgba(255,255,255,.04) 0%,transparent 36%)}"
            'selector > .e-con-inner{position:relative;z-index:1}')


# ============================================================ assembly
IMG = {'img-p14k52.jpg': ('svc_whyus', 12234, 'pl-auto-whyus-team.jpg'),
       'img-1v67tvr.jpg': ('svc_cnc', 12230, 'pl-auto-service-cnc-micromachining.jpg'),
       'img-1pn4v5i.jpg': ('svc_lm', 12232, 'pl-auto-service-laser-micromachining.jpg'),
       'img-1n48553.jpg': ('svc_rp', 12233, 'pl-auto-service-rapid-prototyping.jpg'),
       'img-mi7p38.jpg': ('svc_hybrid', 12231, 'pl-auto-service-hybrid-cnc-laser.jpg'),
       'img-40hu7r.jpg': ('svc_bonding', 12229, 'pl-auto-service-bonding-assembly.jpg'),
       'img-1rqj09.png': ('svc_logo_1', 12235, 'pl-auto-eco-logo-1.png'),
       'img-1noxp18.png': ('svc_logo_2', 12236, 'pl-auto-eco-logo-2.png'),
       'img-xr81kv.png': ('svc_logo_3', 12237, 'pl-auto-eco-logo-3.png'),
       'img-xerlob.png': ('svc_logo_4', 12238, 'pl-auto-eco-logo-4.png')}
PAT = ['hero-dark-stats-5-art', 'split-photo-bullets-inset', 'service-cards-5-link', 'app-explorer-tabs-html',
       'spec-rows-dark-html', 'process-selection-html', 'workflow-steps-5-icons', 'group-cards-4-logos-dark',
       'testimonial-cards-3', 'quote-rapid-hubspot-html', 'faq-sticky-toggle', 'cta-band-dark-grid-2']
SLUG = {'cnc': 'pl-auto-cnc-micromachining', 'lm': 'pl-auto-laser-micromachining', 'mhd': 'pl-auto-micro-hole-drilling',
        'rp': 'pl-auto-rapid-prototyping', '3dp': 'pl-auto-3d-printing'}
TITLE = {'cnc': 'CNC Micromachining Services', 'lm': 'Laser Micromachining Services', 'mhd': 'Laser Micro-Hole Drilling Services',
         'rp': 'Rapid Prototyping Services', '3dp': '3D Printing Contract Services'}


def key_of(img):
    return IMG[os.path.basename(img.get('src', ''))][0]


TPL = {}


def main():
    amap = json.load(open(os.path.join(OUT, 'assets.json')))
    for fn, (k, i, name) in IMG.items():
        amap[k] = {'url': f'{B}/wp-content/uploads/2026/08/{name}', 'attachment_id': i, 'source': 'reused (hash-identical to the design asset ' + fn + ')'}
    json.dump(amap, open(os.path.join(OUT, 'assets.json'), 'w'), indent=1, ensure_ascii=False)
    svg_all = open(SCR + 'meas/cnc-hero-svg.html', encoding='utf-8').read()
    saved = set(); summary = {}
    for key, name, pid in PAGES:
        secs = secs_of(key, name)
        raw = BeautifulSoup(open(SCR + f'svc/Services - {name}.html', encoding='utf-8').read(), 'html.parser')
        hsvg = raw.select_one('#hero svg')
        svg = re.sub(r'\s+', ' ', str(hsvg)) if hsvg else svg_all
        builders = [
            lambda t: hero(t, secs[0], svg),
            lambda t: whyus(t, secs[1], key_of(secs[1].find('img'))),
            lambda t: services(t, secs[2], [key_of(im) for im in secs[2].find_all('img')]),
            lambda t: html_section(t, key, 'appx', t_appx, APPX_JS, eid='applications'),
            lambda t: html_section(t, key, 'caps', t_static, eid='capabilities'),
            lambda t: html_section(t, key, 'procsel', t_static),
            lambda t: workflow(t, secs[6]),
            lambda t: group(t, secs[7], [key_of(im) for im in secs[7].find_all('img')]),
            lambda t: testimonials(t, secs[8]),
            lambda t: html_section(t, key, 'quote', t_quote, QUOTE_JS, eid='quote'),
            lambda t: faq(t, secs[10]),
            lambda t: closing(t, secs[11]),
        ]
        sections, assets = [], []
        for pat, fn in zip(PAT, builders):
            t = Tok(); sec = fn(t)
            js = re.sub(r'"id": "[0-9a-f]{7}"', '"id": ""', json.dumps(sec, sort_keys=True))
            if pat == 'group-cards-4-logos-dark' and 'min-height:34px' in js:
                pat = 'group-cards-4-logos-dark-labels'
            if pat not in saved:
                save(pat, sec, t); saved.add(pat); TPL[pat] = js
            elif TPL[pat] != js:   # pages are rebuilt from the first page's template: structure must match
                raise SystemExit(f'{key}: {pat} differs structurally from the saved template')
            sections.append({'pattern': pat, 'values': dict(t.values)})
            for v in t.values.values():
                if isinstance(v, dict) and 'asset' in v and v['asset'] not in assets:
                    assets.append(v['asset'])
        hdr = (f"# spec.yaml — {TITLE[key]}  (supervised service refresh, 2026-09-25)\n"
               f"# Source design : Potomac Laser.zip (fab7225c…) :: Services - {name}.html  (tweak defaults: explorer Example, quote Compact)\n"
               "# Build style   : Mixed (user decision) — native widgets + HTML widgets for explorer / specs / process selection / quote\n"
               "# Decisions     : explorer pills informational (no drawer/basket); 'Browse materials' dropped; basket CTAs -> #quote;\n"
               "#                 design normalizeStandaloneLinks() (Mimecast redirect) not carried; present-tense Potomac normalised.\n")
        page = {'slug': SLUG[key], 'title': TITLE[key], 'post_type': 'post_services', 'design_page': f'Services - {name}.html',
                'header': hdr, 'assets': assets, 'sections': sections}
        json.dump(page, open(os.path.join(HERE, 'pages', f'svc-{key}.json'), 'w'), indent=1, ensure_ascii=False)
        summary[key] = len(sections)
    print('pages', summary, 'patterns', len(saved), 'brand swaps', len(BRAND_LOG))


if __name__ == '__main__':
    main()
