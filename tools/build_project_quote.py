#!/usr/bin/env python3
"""Build the 2026-11-18 "guided quote" widgets from the Potomac Laser - 2027 design.

Design source (claude.ai/design project c2a2fa49-6c18-41c3-a39b-ae9ec2acf6dd):
  - `Contact - Project Quote.html`  -> /project-quote/ (hero + guided form)
  - `Services - *.html` #quote      -> the quote section on the five service pages

Outputs (built/project-quote-20261118/):
  quote.<key>.widget.html   one Elementor `html` widget per page (CSS + markup + JS)
  hero.project-quote.widget.html
  project-quote.elementor.json   _elementor_data for the new /project-quote/ page

The form posts straight to HubSpot `[Potomac] Start a Project`
(9dba7d36-e36b-4a10-9411-9dc073dab7a0, portal 143181153), the form GF #2 feeds on the
old /project-quote/ page. Contract: reference/HUBSPOT-FORMS.md.

The file upload is REQUIRED, as the design's form marks it (user decision 2026-11-18),
even though the design's step-3 guide text says "Optional" - reported upstream.
"""
import json
import pathlib
import re
import secrets
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "reference" / "design-20261118"
OUT = ROOT / "built" / "project-quote-20261118"

SCOPE = ".pl-svc-quote"
HERO_SCOPE = ".pl-pq-hero"

# Per-page values, verbatim from each design file's #quote section.
SERVICES = {
    "cnc": dict(post=12239, service="CNC micromachining",
                placeholder="e.g. Titanium implant, 4 machined faces, ±20 µm on mating surfaces, 50 parts, first-article report required"),
    "laser": dict(post=12240, service="Laser micromachining",
                  placeholder="e.g. Laser-cut Kapton® part, fine slots and through-holes, 100 parts"),
    "mhd": dict(post=12241, service="Micro-hole drilling",
                placeholder="e.g. 30 µm holes in 0.5 mm stainless sheet, 2,000 holes, ±5 µm position, first-article report"),
    "rp": dict(post=12242, service="Rapid prototyping",
               placeholder="e.g. Functional prototype, ±10 µm features, 5 parts, fastest possible turnaround"),
    "3dp": dict(post=12243, service="3D printing",
                placeholder="e.g. Micro 3D-printed housing, complex internal channels, biocompatible material, 10 parts"),
}
CONTACT_PLACEHOLDER = "e.g. Process, material and thickness, feature sizes, critical tolerances, quantity and timeline"
SERVICE_OPTIONS = ["Laser micromachining", "Micro-hole drilling", "CNC micromachining",
                   "3D printing", "Rapid prototyping", "Other", "Not sure, please recommend"]


# ---------------------------------------------------------------- CSS scoping
def _scope_selector(sel, scope, root_class):
    sel = sel.strip()
    if not sel:
        return sel
    if root_class and sel.startswith(root_class):
        # the section root itself carries both classes
        return scope + sel
    return scope + " " + sel


def _split_selectors(s):
    out, depth, cur = [], 0, ""
    for ch in s:
        if ch in "([":
            depth += 1
        elif ch in ")]":
            depth -= 1
        if ch == "," and depth == 0:
            out.append(cur)
            cur = ""
        else:
            cur += ch
    out.append(cur)
    return out


def scope_css(css, scope, root_class=None):
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    out, i = [], 0
    while i < len(css):
        j = css.find("{", i)
        if j < 0:
            break
        head = css[i:j].strip()
        if head.startswith("@keyframes"):
            depth, k = 0, j
            while True:
                if css[k] == "{":
                    depth += 1
                elif css[k] == "}":
                    depth -= 1
                    if depth == 0:
                        break
                k += 1
            out.append(css[i:k + 1].strip())
            i = k + 1
            continue
        if head.startswith("@media"):
            depth, k = 0, j
            while True:
                if css[k] == "{":
                    depth += 1
                elif css[k] == "}":
                    depth -= 1
                    if depth == 0:
                        break
                k += 1
            out.append(head + "{" + scope_css(css[j + 1:k], scope, root_class) + "}")
            i = k + 1
            continue
        k = css.find("}", j)
        body = re.sub(r"\s*\n\s*", "", css[j + 1:k]).strip()
        sels = ",".join(_scope_selector(s, scope, root_class) for s in _split_selectors(head))
        out.append(sels + "{" + body + "}")
        i = k + 1
    return "\n".join(out)


# ---------------------------------------------------------------- markup
CHECK = ('<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
         'stroke-width="3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
         '<path d="M20 6 9 17l-5-5"/></svg>')
LOCK = ('<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        'stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" '
        'style="display:inline-block;vertical-align:-2px" aria-hidden="true">'
        '<rect x="3" y="11" width="18" height="11" rx="2"></rect><path d="M7 11V7a5 5 0 0 1 10 0v4"></path></svg>')
STATE_LABEL = ('<div class="gf-rapid-label"><span class="qs-when-active">Now</span>'
               '<span class="qs-when-locked">Next</span><span class="qs-when-done">Complete</span></div>')
CHIP = '<span class="qs-chip"><span class="qs-when-locked">Locked</span><span class="qs-when-done">Complete</span></span>'

SERVICE_LEFT_INTRO = f"""<div class="gf-rapid-kicker">Rapid Response Quote</div>
<h2>Ready to move forward?</h2>
<div class="gf-rapid-copy">
<p>Upload your drawing or request a quote, our engineering team will review your design and respond within 24 hours.</p>
<p>No redesign required to start, we'll help optimise your part.</p>
<p class="gf-rapid-secure"><strong>{LOCK}</strong> Uploads stay confidential. We can sign your NDA on request before you share files.</p>
</div>
"""


def guide(n, state, title, text):
    return (f'<div class="gf-rapid-step qs-guide" data-guide="{n}" data-state="{state}">\n'
            f'<div class="gf-rapid-num"><span class="qs-n">{n}</span><span class="qs-ok">{CHECK}</span></div>\n'
            f'<div>{STATE_LABEL}<h3>{title}</h3><p>{text}</p></div>\n</div>\n')


def head(n, title):
    return (f'<div class="qs-head"><span class="qs-badge"><span class="qs-n">{n}</span><span class="qs-ok">{CHECK}</span></span>'
            f'<div><strong>{title}</strong><small>Step {n} of 3</small></div>{CHIP}</div>\n')


def quote_markup(placeholder, selected, with_intro, anchor_project_form):
    opts = "\n".join(
        f"<option{' selected' if o == selected else ''}>{o}</option>" for o in SERVICE_OPTIONS)
    left = (SERVICE_LEFT_INTRO if with_intro else "")
    anchor = '<div id="projectForm" aria-hidden="true"></div>\n' if anchor_project_form else ""
    return f"""<section id="quote" class="pl-svc-quote gf-rapid-quote" data-screen-label="Quote form">
{anchor}<div class="gf-rapid-wrap">
<div class="gf-rapid-left">
{left}<div class="gf-rapid-steps" aria-label="Form progress">
{guide(1, "active", "Your details", "Our team of engineers may have follow up questions to fully understand your requirements.")}{guide(2, "locked", "Describe your project", "Please provide as much information as possible to help us respond accurately. This may include material details and dimensions, quantities and timing, regulatory requirements and application.")}{guide(3, "locked", "Upload your file", "STEP, STL, IGES, PDF, DXF, DWG or ZIP. Optional, but it speeds up the quote.")}<div class="gf-rapid-step qs-done" id="pl-qs-done" hidden>
<div class="gf-rapid-num qs-done__num">{CHECK}</div>
<div><div class="gf-rapid-label qs-done__label">Submission received</div><h3>We will respond within 24 hours</h3><p><strong>Quote &amp; process path confirmed.</strong> Feasibility, recommended process, next steps.</p></div>
</div>
</div>
</div>
<div class="qs-col">
<div class="gf-rapid-card">
<form id="pl-qs-form" novalidate onsubmit="return false">
<fieldset class="qs-block" data-block="1" data-state="active">
{head(1, "Your details")}<div class="qs-body">
<div class="gf-rapid-grid">
<label><span>First name <em>*</em></span><input type="text" name="first_name" autocomplete="given-name" placeholder="Jane" required></label>
<label><span>Last name <em>*</em></span><input type="text" name="last_name" autocomplete="family-name" placeholder="Smith" required></label>
</div>
<label><span>Company <em>*</em></span><input type="text" name="company" autocomplete="organization" placeholder="Company or university" required></label>
<label><span>Email <em>*</em></span><input type="email" name="email" autocomplete="email" placeholder="j.smith@example.com" required></label>
</div>
</fieldset>
<fieldset class="qs-block" data-block="2" data-state="locked" inert>
{head(2, "Describe your project")}<div class="qs-body">
<label><span>Part description and requirements <em>*</em></span><textarea name="description" placeholder="{placeholder}" required></textarea></label>
<label><span>Service <em>*</em></span>
<select name="service" required>
<option value="">Select…</option>
{opts}
</select>
</label>
</div>
</fieldset>
<fieldset class="qs-block" data-block="3" data-state="locked" inert>
{head(3, "Upload your file")}<div class="qs-body">
<label>
<span>Upload drawing / CAD <em>*</em></span>
<div class="gf-rapid-upload"><input type="file" name="files" required accept=".step,.stp,.stl,.iges,.igs,.pdf,.dxf,.dwg,.zip"></div>
<small>STEP, STL, IGES, PDF, DXF, DWG or ZIP, up to 25 MB</small>
</label>
<div class="gf-rapid-actions"><p>No commitment · 24h response</p><button type="submit"><span data-btn-state="idle">Send request →</span><span data-btn-state="sent" hidden>Sent ✓</span></button></div>
</div>
</fieldset>
</form>
<div class="qs-thanks" id="pl-qs-thanks" hidden>
<span class="qs-thanks__ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 6 9 17l-5-5"/></svg></span>
<h2>Thank you for your submission</h2>
<p>Your request is with our engineering team. We will review your part and respond within 24 hours with feasibility, a recommended process and next steps.</p>
</div>
</div>
</div>
</div>
</section>"""


# ---------------------------------------------------------------- JS
# Step logic is the design's; submission mirrors the live service-page widget
# (direct HubSpot v3 submit, upload via Code Snippet #12, UTM, hutk, dataLayer).
JS = r"""<script>
(function(){
var root=document.querySelector('.pl-svc-quote');if(!root||root.dataset.plWired)return;root.dataset.plWired='1';
var PORTAL='143181153',FORM='9dba7d36-e36b-4a10-9411-9dc073dab7a0',UPLOAD='/wp-json/cnc-quote/v1/upload',FORM_ID='__FORM_ID__';
var form=document.getElementById('pl-qs-form'),done=document.getElementById('pl-qs-done'),card=form.closest('.gf-rapid-card'),sent=false,busy=false,started=false;
function blk(n){return form.querySelector('[data-block="'+n+'"]')}
function valid(n){return Array.from(blk(n).querySelectorAll('[required]')).every(function(f){return f.value.trim()&&f.checkValidity()})}
function setState(n,s){
var b=blk(n);b.dataset.state=s;b.toggleAttribute('inert',s==='locked'||s==='sealed');
root.querySelector('[data-guide="'+n+'"]').dataset.state=s==='open'?'locked':(s==='sealed'?'done':s);
}
var current=1;
function sync(){
if(sent)return;
var v1=valid(1),v2=v1&&valid(2);
if(!v1)current=1;else if(!v2&&current>2)current=2;
[1,2,3].forEach(function(n){
var unlocked=n===1||(n===2&&v1)||(n===3&&v2);
if(!unlocked)setState(n,'locked');
else if(n<current)setState(n,'done');
else if(n===current)setState(n,'active');
else setState(n,'open');
});
}
function val(name){var e=form.querySelector('[name="'+name+'"]');return e?(e.value||'').trim():''}
function utm(){var o={},q=new URLSearchParams(location.search);['utm_source','utm_medium','utm_campaign','utm_term','utm_content'].forEach(function(k){var v=q.get(k);if(v)o[k]=v});return o}
function hutk(){var m=document.cookie.match(/(?:^|;\s*)hubspotutk=([^;]+)/);return m?m[1]:''}
function track(ev,p){try{(window.dataLayer=window.dataLayer||[]).push(Object.assign({event:ev,form_id:FORM_ID},p||{}))}catch(e){}}
function clearErr(){var o=card.querySelector('.pl-qs-err');if(o)o.remove()}
function err(msg){clearErr();var o=document.createElement('p');o.className='pl-qs-err';o.setAttribute('role','alert');
o.style.cssText='margin:0 0 14px;padding:10px 14px;border-radius:8px;background:#FEF2F2;border:1px solid #FECACA;color:#B91C1C;font-size:13px;line-height:1.5';
o.textContent=msg;form.parentNode.insertBefore(o,form)}
async function upload(){var i=form.querySelector('[name="files"]');if(!i||!i.files||!i.files[0])return '';
var fd=new FormData();fd.append('file',i.files[0]);
try{var r=await fetch(UPLOAD,{method:'POST',body:fd});var j=await r.json();if(r.ok&&j&&j.url)return j.url;
err('That file could not be uploaded ('+((j&&j.error)||'unknown error')+'). Please try a smaller file, or email it to inq@goodfellow.com.');return null}
catch(e){err('That file could not be uploaded. Please try again, or email it to inq@goodfellow.com.');return null}}
function thanks(){
sent=true;[1,2,3].forEach(function(n){setState(n,'sealed')});
form.querySelectorAll('[data-btn-state]').forEach(function(el){el.hidden=el.dataset.btnState!=='sent'});
card.style.minHeight=card.offsetHeight+'px';card.classList.add('is-thanks');form.hidden=true;document.getElementById('pl-qs-thanks').hidden=false;done.hidden=false;
if(window.gtag)gtag('event','generate_lead',__GTAG_PARAMS__);
var r=done.getBoundingClientRect();if(r.bottom>window.innerHeight||r.top<0)window.scrollTo({top:r.top+window.scrollY-160,behavior:'smooth'});
}
form.addEventListener('input',function(){if(!started){started=true;track('lead_form_start')}sync()});
form.addEventListener('change',sync);
form.addEventListener('focusin',function(e){
var b=e.target.closest('[data-block]');if(!b||sent)return;
var n=+b.dataset.block;if(n!==current){current=n;sync()}
});
form.addEventListener('submit',async function(e){
e.preventDefault();if(busy||sent)return;clearErr();
if(!valid(1)||!valid(2)||!valid(3)){form.reportValidity();track('lead_form_submit_error',{error:'validation'});return}
var d={firstname:val('first_name'),lastname:val('last_name'),company:val('company'),email:val('email')};
if(!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(d.email)){err('That email address does not look right. Please check it.');track('lead_form_submit_error',{error:'email'});return}
var btn=form.querySelector('button[type=submit]');busy=true;btn.disabled=true;
var url=await upload();if(url===null){busy=false;btn.disabled=false;track('lead_form_submit_error',{error:'upload'});return}
d.potomac_project_name='Rapid Response Quote \u2014 '+document.title;
d.potomac_project_description=val('description')+'\n\nService: '+val('service');
if(url)d.potomac_file_submission=url;d.hs_lead_status='NEW';d.lifecyclestage='lead';
var u=utm(),k;for(k in u)d[k]=u[k];
var props=Object.keys(d).filter(function(k){return d[k]!=null&&d[k]!==''}).map(function(k){return{objectTypeId:'0-1',name:k,value:String(d[k])}});
track('lead_form_submit',{fields_completed:props.length});
try{var r=await fetch('https://api.hsforms.com/submissions/v3/integration/submit/'+PORTAL+'/'+FORM,{method:'POST',headers:{'Content-Type':'application/json'},
body:JSON.stringify({fields:props,context:{pageName:document.title,pageUri:location.href,hutk:hutk()||undefined}})});
var j=await r.json().catch(function(){return{}});
if(r.ok){track('lead_form_submit_success');busy=false;thanks();return}
console.error('HubSpot submit failed',r.status,j);err('We could not send that just now. Please try again, or email inq@goodfellow.com.');track('lead_form_submit_error',{error:'http_'+r.status})}
catch(x){console.error(x);err('We could not send that just now. Please check your connection, or email inq@goodfellow.com.');track('lead_form_submit_error',{error:'network'})}
busy=false;btn.disabled=false;
});
sync();
})();
</script>"""


def quote_widget(key, placeholder, selected, with_intro, anchor_project_form, form_id, gtag_params):
    design = (SRC / "quote.design.css").read_text()
    reset = (SRC / "live-reset.css").read_text()
    css = scope_css(design, SCOPE, root_class=".gf-rapid-quote") + "\n" + reset
    js = JS.replace("__FORM_ID__", form_id).replace("__GTAG_PARAMS__", gtag_params)
    return "<style>" + css + "</style>" + quote_markup(placeholder, selected, with_intro, anchor_project_form) + encode_js(js)


def encode_js(script_tag):
    """Ship the script base64-encoded.

    On this site the rendered page runs through content filters that rewrite `&&` to
    `&#038;&#038;` (and eat backslashes) inside an Elementor html widget's <script>, which
    leaves the script unparseable and the form unwired; a plain browser submit then GETs
    the homepage with the form values in the URL (seen 2026-11-18 on draft 12525).
    Base64 is [A-Za-z0-9+/=] only, so nothing in it can be rewritten.
    Source: tools/build_project_quote.py JS.
    """
    import base64
    body = script_tag.strip()[len("<script>"):-len("</script>")]
    if any(ord(c) > 127 for c in body):
        raise SystemExit("widget JS must be ASCII before base64 (atob yields Latin-1)")
    b64 = base64.b64encode(body.encode("ascii")).decode()
    return ("<script>/* pl guided quote: tools/build_project_quote.py */"
            "new Function(atob('" + b64 + "'))();</script>")


# ---------------------------------------------------------------- hero (Contact - Project Quote)
HERO_CSS = """
.pl-pq-hero.hero{position:relative;background:#0D1B2A;color:#fff;overflow:hidden;padding:44px 24px 36px;font-family:'Inter',system-ui,-apple-system,'Segoe UI',Roboto,sans-serif !important;-webkit-font-smoothing:antialiased;box-sizing:border-box}
.pl-pq-hero *,.pl-pq-hero *::before,.pl-pq-hero *::after{box-sizing:border-box}
.pl-pq-hero .hero__bg{position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,0.04) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,0.04) 1px,transparent 1px);background-size:80px 80px;pointer-events:none}
.pl-pq-hero .hero__bg::before{content:'';position:absolute;left:-10%;top:10%;width:60%;height:80%;background:radial-gradient(ellipse at center,rgba(20,48,73,0.7) 0%,transparent 65%)}
.pl-pq-hero .hero__bg::after{content:'';position:absolute;right:-5%;top:-10%;width:60%;height:80%;background:radial-gradient(ellipse at center,rgba(148,18,82,0.10) 0%,transparent 60%)}
.pl-pq-hero .hero__inner{position:relative;max-width:1440px;margin:0 auto;display:grid;grid-template-columns:1fr;gap:56px;align-items:center;padding-bottom:0}
.pl-pq-hero .hero__eyebrow{display:inline-flex;align-items:center;gap:12px;font-size:0.75rem;font-weight:600;letter-spacing:0.18em;text-transform:uppercase;color:#fff;margin:0 0 20px;white-space:nowrap;font-family:inherit !important}
.pl-pq-hero .hero__title{font-family:'Inter',system-ui,-apple-system,'Segoe UI',Roboto,sans-serif !important;font-size:clamp(2.5rem,5vw,4rem);line-height:1.05;letter-spacing:-0.025em;font-weight:600 !important;color:#fff;margin:0 0 24px;text-transform:none}
.pl-pq-hero .hero__title .accent{color:#F5821F}
.pl-pq-hero .hero__lede{font-size:1.125rem;line-height:1.65;color:rgba(255,255,255,0.78);max-width:640px;margin:0 0 32px;font-family:inherit !important}
.pl-pq-hero .pq-proof{display:flex;flex-wrap:wrap;gap:10px 24px;margin:26px 0 0;padding:0;list-style:none}
.pl-pq-hero .pq-proof li{display:flex;align-items:center;gap:8px;font-size:0.875rem;color:rgba(255,255,255,.86);margin:0;padding:0;list-style:none}
.pl-pq-hero .pq-proof li::before{content:none}
.pl-pq-hero .pq-proof svg{width:16px;height:16px;color:#F5821F;flex-shrink:0}
"""

HERO_HTML = """<section class="pl-pq-hero hero pq-hero" id="hero" data-surface="dark" data-screen-label="Project quote hero">
<div class="hero__bg"></div>
<div class="hero__inner">
<div>
<div class="hero__eyebrow">Rapid Response Quote</div>
<h1 class="hero__title">Ready to move <span class="accent">forward?</span></h1>
<p class="hero__lede">We just need three things from you: your contact details, a description of your part, and your files.</p>
<ul class="pq-proof">
<li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>Uploads stay confidential. We can sign your NDA on request before you share files.</li>
</ul>
</div>
</div>
</section>"""


def hero_widget():
    return "<style>" + re.sub(r"\n+", "\n", HERO_CSS.strip()) + "</style>" + HERO_HTML


# ---------------------------------------------------------------- Elementor page
SECTION_SETTINGS = {
    "content_width": "full", "flex_direction": "column",
    "flex_gap": {"unit": "px", "column": "0", "row": "0", "isLinked": True},
    "padding": {"unit": "px", "top": "0", "right": "0", "bottom": "0", "left": "0", "isLinked": True},
    "custom_css": "selector{position:relative;overflow:hidden}selector > .e-con-inner, selector{max-width:none}",
}


def eid(used):
    while True:
        x = secrets.token_hex(4)[:7]
        if x not in used:
            used.add(x)
            return x


def html_section(html, used):
    return {"id": eid(used), "elType": "container", "isInner": False, "settings": dict(SECTION_SETTINGS),
            "elements": [{"id": eid(used), "elType": "widget", "widgetType": "html", "isInner": False,
                          "settings": {"html": html}, "elements": []}]}


SCAFFOLD = re.compile(r"cdn\.tailwindcss\.com|unpkg\.com|babel|tweaks-panel|tweaks-root|tweaks-ui|initTweaks|"
                      r"<script src=\"http|<link rel=\"stylesheet\" href=\"http|\$\{")
STYLE_BREACH = re.compile("[—–→←]")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    widgets = {}
    for key, s in SERVICES.items():
        widgets[f"quote.{key}"] = quote_widget(
            key, s["placeholder"], s["service"], with_intro=True, anchor_project_form=False,
            form_id="service_quote",
            gtag_params="{form_id:'service_quote',service:val('service')}")
    widgets["quote.project-quote"] = quote_widget(
        "project-quote", CONTACT_PLACEHOLDER, None, with_intro=False, anchor_project_form=True,
        form_id="project_quote", gtag_params="{form_id:'project_quote'}")
    widgets["hero.project-quote"] = hero_widget()

    problems = []
    for name, html in widgets.items():
        if SCAFFOLD.search(html):
            problems.append(f"{name}: design scaffolding / template literal: {SCAFFOLD.search(html).group(0)}")
        (OUT / f"{name}.widget.html").write_text(html)
        # rendered-text style breaches (design copy is reported, not fixed)
        text = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", html, flags=re.S)
        text = re.sub(r"<[^>]+>", " ", text)
        for m in set(STYLE_BREACH.findall(text)):
            print(f"style note {name}: rendered text contains {m!r} (design copy, report upstream)")

    used = set()
    page = [html_section(widgets["hero.project-quote"], used),
            html_section(widgets["quote.project-quote"], used)]
    (OUT / "project-quote.elementor.json").write_text(json.dumps(page, ensure_ascii=False))

    for name, html in widgets.items():
        print(f"{name}: {len(html):,} bytes")
    if problems:
        print("\n".join(problems))
        sys.exit(1)


if __name__ == "__main__":
    main()
