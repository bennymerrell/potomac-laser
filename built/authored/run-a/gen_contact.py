"""§7.2 AUTHOR — Contact (run 20260924-125928). Rendered with the design's tweak defaults
(heroLayout "Contact form", showHeroCard false, showMap true, officeCols 2, showNewsletter false).

  hero-split-contact-form  dark hero: copy + 2 CTAs left | contact form card right (wired to HubSpot)
  hq-panel-map             HQ panel (flag, city, 3 contact lines) | map embed, side by side
  offices-grid-6-social    left-aligned head + 2-column grid of 5 offices + 1 "can't find" card + social row

The form is one html widget (quote-form-hubspot's pattern): markup + scoped CSS + a submit script
that posts to the HubSpot Forms API v3, portal 143181153, form `[Potomac] Contact Form`
54d0ec75-106d-43eb-a420-0ff22e448e6d, whose fields (reference/HUBSPOT-FORMS.md, feed #18) are
exactly the design's: email, firstname, lastname, phone, company, website, potomac_message.
The design's own handler was front-end only (preventDefault + reset); this one really submits.
Copy inside the widget is tokenised as plain text (like quote-form-hubspot).
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from about_shared import *  # noqa

PORTAL, FORM = '143181153', '54d0ec75-106d-43eb-a420-0ff22e448e6d'


def w(wtype, settings):
    return {'id': 'aaaaaaa', 'elType': 'widget', 'widgetType': wtype, 'settings': settings, 'elements': []}


def icon_list(t, items, color, icon_color, size=15, lh=23.25, icon=18, gap_css='', font=''):
    """items: [(fa-icon, text, url-or-None)]"""
    lst = []
    for i, (ic, label, url) in enumerate(items):
        it = {'text': t('heading', label), 'selected_icon': {'value': ic, 'library': 'fa-solid'}, '_id': f'i{i}ab12c'}
        if url:
            it['link'] = {'url': t('url', url), 'is_external': '', 'nofollow': ''}
        lst.append(it)
    return w('icon-list', {'icon_list': lst, 'space_between': px(0), 'icon_size': px(icon),
                           'custom_css': (f'selector .elementor-icon-list-item{{align-items:flex-start!important}}'
                                          f'selector .elementor-icon-list-icon{{margin-top:3px}}'
                                          f'selector .elementor-icon-list-icon i{{color:{icon_color};font-size:{icon}px}}'
                                          f'selector .elementor-icon-list-icon svg{{fill:{icon_color};width:{icon}px;height:{icon}px}}'
                                          f'selector .elementor-icon-list-text,selector a .elementor-icon-list-text{{color:{color};'
                                          f'font:400 {size}px/{lh}px Inter,system-ui,sans-serif;padding-left:13px}}' + gap_css + font)})


# ------------------------------------------------------------------ hero-split-contact-form
t = Tok()
FORM_CSS = (
    '.pl-cf{background:#fff;border:1px solid #DCE1EA;border-radius:16px;box-shadow:0 30px 70px rgba(0,0,0,.4);padding:36px;color:#0F1620;font-family:Inter,system-ui,sans-serif}'
    '.pl-cf *{box-sizing:border-box}'
    '.pl-cf .k{margin:0 0 10px;font:700 12px/19.2px Inter,system-ui,sans-serif;letter-spacing:1.68px;text-transform:uppercase;color:#F5821F}'
    '.pl-cf h2{margin:0 0 8px;font:600 28px/33.6px Inter,system-ui,sans-serif;letter-spacing:-.28px;color:#0F1620}'
    '.pl-cf .sub{margin:0 0 28px;font-size:15px;line-height:24px;color:#65718A}.pl-cf .sub em{color:#F5821F;font-style:normal}'
    '.pl-cf .st{display:none;align-items:center;gap:10px;background:#EFFAF3;border:1px solid rgba(34,197,94,.25);color:#15803D;border-radius:8px;padding:14px 16px;font-size:15px;font-weight:600;margin-bottom:22px}'
    '.pl-cf .st.show{display:flex}.pl-cf .st svg{width:20px;height:20px;flex-shrink:0}'
    '.pl-cf .err{background:#FEF2F2;border:1px solid rgba(220,38,38,.25);color:#B91C1C;border-radius:8px;padding:12px 14px;font-size:14px;margin-bottom:18px}'
    '.pl-cf form{display:flex;flex-direction:column;gap:18px}.pl-cf .g{display:grid;grid-template-columns:1fr 1fr;gap:16px}'
    '.pl-cf .f{display:flex;flex-direction:column;gap:8px}'
    '.pl-cf label{font:600 12px/18px Inter,system-ui,sans-serif;letter-spacing:1.44px;text-transform:uppercase;color:#65718A}.pl-cf label em{color:#F5821F;font-style:normal}'
    '.pl-cf input,.pl-cf textarea{width:100%;padding:12px 14px;border:1px solid #DCE1EA;border-radius:4px;background:#fff;font:400 15px/18px Inter,system-ui,sans-serif;color:#0F1620;margin:0}'
    '.pl-cf textarea{min-height:96px;line-height:22.5px;resize:vertical}'
    '.pl-cf input:focus,.pl-cf textarea:focus{outline:none;border-color:#F5821F;box-shadow:0 0 0 3px rgba(245,130,31,.2)}'
    '.pl-cf ::placeholder{color:#9AA4B5}'
    '.pl-cf .a{display:flex;justify-content:space-between;align-items:center;gap:16px;margin-top:8px}'
    '.pl-cf button{display:inline-flex;align-items:center;justify-content:center;gap:8px;padding:15px 28px;border:1px solid transparent;border-radius:999px;'
    'background:#F5821F;color:#fff;font:600 15px/15px Inter,system-ui,sans-serif;box-shadow:0 8px 24px rgba(245,130,31,.3);cursor:pointer;transition:transform .15s,background .15s}'
    '.pl-cf button:hover{background:#D96E10;transform:translateY(-1px)}.pl-cf.busy button{opacity:.6;pointer-events:none}'
    '.pl-cf .m{font-size:13px;line-height:19.5px;color:#65718A}'
    '@media(max-width:560px){.pl-cf{padding:24px}.pl-cf .g{grid-template-columns:1fr}}')
FIELDS = [('fname', 'First name', 'Jane', 'text', True), ('lname', 'Last name', 'Doe', 'text', True),
          ('email', 'Email', 'jane@company.com', 'email', True), ('phone', 'Phone', '+1 555 000 0000', 'text', True),
          ('company', 'Company', 'Acme Devices', 'text', True), ('website', 'Website', 'acme.com', 'text', False)]


def field(fid, label, ph, typ, req):
    star = ' <em>*</em>' if req else ''
    return (f'<div class="f"><label for="pl-cf-{fid}">{t("heading", label)}{star}</label>'
            f'<input type="{typ}" id="pl-cf-{fid}" name="{fid}" placeholder="{t("heading", ph)}"{" required" if req else ""}></div>')


kicker, title = t('heading', 'Send a message'), t('heading', 'Tell us about your project')
sub = t('body', 'Fields marked <em>*</em> are required. Our engineers review every enquiry for manufacturability, '
                'no redesign required to start.')
status = t('heading', 'Thanks, your message is on its way. Our team will respond within one business day.')
rows = ''.join(f'<div class="g">{field(*FIELDS[i])}{field(*FIELDS[i + 1])}</div>' for i in (0, 2, 4))
msg_label, msg_ph = t('heading', 'Message'), t('heading', 'Tell us about your part, material, tolerances, feature sizes, quantities, and timeline.')
btn, micro = t('button', 'Send message →'), t('heading', 'No commitment · 24-hour response')
SCRIPT = ('<script>(function(){var PORTAL="' + PORTAL + '",FORM="' + FORM + '",FORM_ID="contact_form";'
    'var card=document.currentScript.parentElement.querySelector(".pl-cf");if(!card||card.dataset.plWired)return;card.dataset.plWired="1";'
    'var f=card.querySelector("form"),st=card.querySelector(".st");'
    'function utm(){var o={},q=new URLSearchParams(location.search);["utm_source","utm_medium","utm_campaign","utm_term","utm_content","gclid"].forEach(function(k){var v=q.get(k);if(v)o[k]=v;});'
    'try{if(Object.keys(o).length){localStorage.setItem("pl_utm_last",JSON.stringify(o));if(!localStorage.getItem("pl_utm_first"))localStorage.setItem("pl_utm_first",JSON.stringify(o));}'
    'else{o=JSON.parse(localStorage.getItem("pl_utm_last")||"null")||JSON.parse(localStorage.getItem("pl_utm_first")||"null")||{};}}catch(e){}return o;}'
    'function hutk(){var m=document.cookie.match(/hubspotutk=([^;]+)/);return m?m[1]:"";}'
    'function track(ev,d){var p={event:ev,form_id:FORM_ID,page_path:location.pathname},u=utm(),k;for(k in u)p[k]=u[k];if(d)for(k in d)p[k]=d[k];'
    'try{(window.dataLayer=window.dataLayer||[]).push(p);}catch(e){}try{if(window.gtag)window.gtag("event",ev,p);}catch(e){}}'
    'function err(m){var o=card.querySelector(".err");if(o)o.remove();var d=document.createElement("div");d.className="err";d.setAttribute("role","alert");d.textContent=m;f.parentNode.insertBefore(d,f);}'
    'var started=false;f.addEventListener("input",function(){if(!started){started=true;track("lead_form_start");}});'
    'function v(n){var e=f.elements[n];return e?(e.value||"").trim():"";}'
    'f.addEventListener("submit",async function(ev){ev.preventDefault();var o=card.querySelector(".err");if(o)o.remove();'
    'var d={email:v("email"),firstname:v("fname"),lastname:v("lname"),phone:v("phone"),company:v("company"),website:v("website"),potomac_message:v("message")};'
    'if(!d.firstname||!d.lastname||!d.email||!d.phone||!d.company||!d.potomac_message){err("Please fill in every field marked *.");track("lead_form_submit_error",{error:"validation"});return;}'
    'if(!/^[^\\s@]+@[^\\s@]+\\.[^\\s@]{2,}$/.test(d.email)){err("That email address does not look right. Please check it.");track("lead_form_submit_error",{error:"email"});return;}'
    'd.hs_lead_status="NEW";var u=utm(),k;for(k in u)d[k]=u[k];'
    'var props=Object.keys(d).filter(function(k){return d[k]!=null&&d[k]!=="";}).map(function(k){return{objectTypeId:"0-1",name:k,value:String(d[k])};});'
    'card.classList.add("busy");track("lead_form_submit",{fields_completed:props.length});'
    'try{var r=await fetch("https://api.hsforms.com/submissions/v3/integration/submit/"+PORTAL+"/"+FORM,{method:"POST",headers:{"Content-Type":"application/json"},'
    'body:JSON.stringify({fields:props,context:{pageName:document.title,pageUri:location.href,hutk:hutk()||undefined}})});'
    'if(r.ok){track("lead_form_submit_success");st.classList.add("show");f.reset();card.classList.remove("busy");try{st.scrollIntoView({behavior:"smooth",block:"center"});}catch(e){}return;}'
    'var j=await r.json().catch(function(){return null;});console.error("HubSpot submit failed",r.status,j);track("lead_form_submit_error",{error:"http_"+r.status});'
    'err("We could not send that just now. Please try again, or email info@potomac-laser.com.");}'
    'catch(e){console.error(e);track("lead_form_submit_error",{error:"network"});err("We could not send that just now. Please check your connection, or email info@potomac-laser.com.");}'
    'card.classList.remove("busy");});})();</script>')
FORM_HTML = ('<style>' + FORM_CSS + '</style><div class="pl-cf"><p class="k">' + kicker + '</p><h2>' + title + '</h2>'
             '<p class="sub">' + sub + '</p><div class="st" role="status"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
             'stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>' + status + '</div>'
             '<form novalidate>' + rows + '<div class="f"><label for="pl-cf-message">' + msg_label + ' <em>*</em></label>'
             '<textarea id="pl-cf-message" name="message" placeholder="' + msg_ph + '" required></textarea></div>'
             '<div class="a"><button type="submit">' + btn + '</button><span class="m">' + micro + '</span></div></form></div>' + SCRIPT)

left = container([
    heading(t('heading', 'Contact Us'), 12, '600', color='#FFFFFF', lh=18, ls=2.16, upper=True, _margin=box(0, 0, 26, 0)),
    heading(t('heading', 'What can we<br>help with <span class="pl-accent">today?</span>'), 64, '600', tag='h1', color='#FFFFFF',
            lh=67.2, ls=-1.6, _margin=box(0, 0, 24, 0), css='selector .pl-accent{color:var(--e-global-color-gforange)}'),
    text(t('body', '<p>Ask our engineers about your project or request a rapid quotation. Share your requirements and '
                   '<strong>we respond within one business day</strong>, with answers, feasibility, and a recommended '
                   "process path. We've been doing this for over 40 years. Try us out.</p>"),
         18, color='rgba(255,255,255,0.78)', lh=29.7, _margin=box(0, 0, 32, 0),
         extra_css='selector p{max-width:580px}selector strong{color:#fff;font-weight:600}'),
    container([
        button(t('button', 'Request a quote →'), t('url', 'Services - CNC Micromachining.html#quote'), size=15, pad=(15, 28),
               shadow='0 8px 24px rgba(245,130,31,.3)', css='selector .elementor-button{border:1px solid transparent}'),
        button(t('button', 'Call 443-543-5737'), t('url', 'tel:+14435435737'), bg=None, fg='#FFFFFF', size=15, pad=(15, 28),
               border='rgba(255,255,255,0.32)', css='selector .elementor-button{background:transparent}'),
    ], flex_direction='row', flex_wrap='wrap', flex_gap=gap(12, 12), _margin=box(0, 0, 24, 0)),
], flex_direction='column', flex_align_items='flex-start', flex_gap=gap(0),
   custom_css='selector{flex:0 0 calc((100% - 64px) * .55) !important;max-width:calc((100% - 64px) * .55) !important}'
              '@media(max-width:1023px){selector{flex:0 0 100% !important;max-width:100% !important}}')
right = container([w('html', {'html': FORM_HTML})], flex_direction='column', flex_gap=gap(0),
                  custom_css='selector{flex:0 0 calc((100% - 64px) * .45) !important;max-width:calc((100% - 64px) * .45) !important}'
                             '@media(max-width:1023px){selector{flex:0 0 100% !important;max-width:100% !important}}')
hero = container([
    container([left, right], content_width='boxed', boxed_width=px(1392), flex_direction='row', flex_wrap='wrap',
              flex_align_items='center', flex_gap=gap(40, 64)),
], flex_direction='column', flex_align_items='center', padding=box(72, 24, 56, 24),
   background_background='classic', background_color_hex='#0D1B2A',
   custom_css=('selector{background-image:linear-gradient(rgba(255,255,255,0.04) 1px,transparent 1px),'
               'linear-gradient(90deg,rgba(255,255,255,0.04) 1px,transparent 1px);background-size:32px 32px}'))
save('hero-split-contact-form', hero, t)

# ------------------------------------------------------------------ hq-panel-map
t = Tok()
panel = container([
    container([dot('#F5821F', 7), heading(t('heading', 'Headquarters'), 12, '700', color='#F5821F', lh=19.2, ls=1.68, upper=True)],
              flex_direction='row', flex_align_items='center', flex_gap=gap(8, 8), _margin=box(0, 0, 11, 0)),  # 6 + the 24px line box (12302 iter 1: 5px short)
    heading(t('heading', 'Baltimore, MD'), 24, '600', tag='h3', color='#FFFFFF', lh=31.2, _margin=box(0, 0, 20, 0)),
    icon_list(t, [('fas fa-map-marker-alt', '1450 South Rolling Road<br>Baltimore, MD 21227, USA', None),
                  ('fas fa-phone', '443-543-5737', 'tel:+14435435737'),
                  ('fas fa-envelope', 'info@potomac-laser.com', 'mailto:info@potomac-laser.com')],
              'rgba(255,255,255,0.86)', '#F5821F',
              gap_css='selector .elementor-icon-list-item{padding:11px 0!important;margin:0!important}'
                      'selector .elementor-icon-list-item + .elementor-icon-list-item{border-top:1px solid rgba(255,255,255,.1)}'),
], flex_direction='column', flex_align_items='stretch', flex_gap=gap(0), padding=box(30),
   background_background='classic', background_color_hex='#0D1B2A', border_radius=box(16),
   custom_css=('selector{position:relative;overflow:hidden;flex:1 1 0 !important}'
               'selector::before{content:"";position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,0.05) 1px,transparent 1px),'
               'linear-gradient(90deg,rgba(255,255,255,0.05) 1px,transparent 1px);background-size:26px 26px;opacity:.5;pointer-events:none}'
               'selector > *{position:relative;z-index:1}'
               '@media(max-width:759px){selector{flex:0 0 100% !important}}'))
MAP = ('<iframe title="Goodfellow Microfabrication, Baltimore, MD" src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2897.9445719291243!2d-76.71027930415296!3d39.23382146518388!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x89b7c1d6f04a78df%3A0xd81fb800436acb43!2sPotomac%20Photonics%20Inc.!5e0!3m2!1sen!2sid!4v1689661906881!5m2!1sen!2sid" '
       'loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>')
mapc = container([w('html', {'html': t('embed', MAP)})], border_border='solid', border_width=box(1), border_color=LINE,
                 border_radius=box(16),
                 custom_css=('selector{overflow:hidden;line-height:0;flex:1.3 1 0 !important;box-shadow:0 1px 2px rgba(15,22,32,.06),0 1px 1px rgba(15,22,32,.04)}'
                             'selector .elementor-widget-html,selector .elementor-widget-container{height:100%}'
                             'selector iframe{width:100%;height:100%;min-height:260px;border:0;display:block;filter:grayscale(.15)}'
                             '@media(max-width:759px){selector{flex:0 0 100% !important}}'))
save('hq-panel-map', band([container([panel, mapc], flex_direction='row', flex_wrap='wrap', flex_align_items='stretch',
                                     flex_gap=gap(24, 24))]), t)

# ------------------------------------------------------------------ offices-grid-6-social
t = Tok()
OFF = [('Cambridge', 'Ermine Business Park, Huntingdon, Cambs, PE29 6WR, England', '+44 (0) 1480 424800', 'tel:+441480424800'),
       ('Pittsburgh', '301 Grant Street, Suite 270, Pittsburgh, PA 15219, USA', '+1-800-821-2870', 'tel:+18008212870'),
       ('Hamburg', 'Alstertwiete 3, D-20099, Hamburg, Germany', '+49 (0) 800 1000 579', 'tel:+498001000579'),
       ('Lille', '229 rue Solférino, 59000, Lille, France', '+33 (0) 800 91 72 41', 'tel:+33800917241'),
       ('Shanghai', "Room 803, No. 568 Hengfeng Road, Jing'an District, Shanghai, 200070, China", '+86 (0) 21-5299 7072', 'tel:+862152997072')]
head = container([
    eyebrow(t, 'Worldwide'),
    heading(t('heading', 'Our global offices'), 40, '600', tag='h2', color=INK, lh=44.8, ls=-0.8, _margin=box(18, 0, 16, 0)),
    text(t('body', '<p>Part of the Goodfellow Group, with materials, microfabrication and analytics support across the US, '
                   'Europe and Asia.</p>'), 18, color=MUTED, lh=29.7),
], flex_direction='column', flex_align_items='flex-start', flex_gap=gap(0), width=px(760),
   width_mobile={'unit': '%', 'size': 100}, _margin=box(0, 0, 40, 0))
OFFICE_CSS = ('selector{position:relative;transition:transform .25s cubic-bezier(.25,.46,.45,.94),box-shadow .25s cubic-bezier(.25,.46,.45,.94),border-color .25s}'
              'selector:hover{transform:translateY(-3px);box-shadow:0 4px 12px rgba(15,22,32,.08);border-color:#C3CBD8}'
              'selector::after{content:"";position:absolute;left:0;top:24px;bottom:24px;width:3px;border-radius:0 3px 3px 0;'
              'background:var(--e-global-color-gforange);transform:scaleY(0);transform-origin:top;transition:transform .25s}'
              'selector:hover::after{transform:scaleY(1)}')
cards = []
for city, addr, tel, telu in OFF:
    cards.append(container([
        heading(t('heading', city), 20, '600', tag='h3', color=INK, lh=26, ls=-0.2, _margin=box(0, 0, 4, 0)),
        icon_list(t, [('fas fa-map-marker-alt', addr, None), ('fas fa-phone', tel, telu)], '#3C4858', '#F5821F',
                  size=14, lh=21.7, icon=16,
                  gap_css='selector .elementor-icon-list-item{padding:10px 0 0!important;margin:0!important}'
                          'selector .elementor-icon-list-text{padding-left:11px!important}'),
    ], flex_direction='column', flex_gap=gap(0), padding=box(26, 24), background_background='classic',
       background_color_hex='#FFFFFF', border_border='solid', border_width=box(1), border_color=LINE, border_radius=box(8),
       custom_css=OFFICE_CSS))
cards.append(container([
    heading(t('heading', "Can't find your region?"), 20, '600', tag='h3', color=INK, lh=26, ls=-0.2, _margin=box(0, 0, 8, 0)),
    text(t('body', "<p>The Goodfellow Group serves 111+ countries. Reach the Baltimore team and we'll route you.</p>"), 14,
         color='#3C4858', lh=22.4, _margin=box(0, 0, 16, 0)),
    button_secondary(t, 'Email the team →', 'mailto:info@potomac-laser.com'),
], flex_direction='column', flex_justify_content='center', flex_align_items='flex-start', flex_gap=gap(0), padding=box(26, 24),
   background_background='classic', background_color_hex='#FEF9F5', border_border='solid', border_width=box(1),
   border_color='#F9B067', border_radius=box(8), custom_css=OFFICE_CSS))
SOC = [('fab fa-instagram', 'https://www.instagram.com/potomacphotonic/'), ('fab fa-facebook-f', 'https://www.facebook.com/potomacphotonics'),
       ('fab fa-linkedin-in', 'https://www.linkedin.com/company/potomac-photonics/'), ('fab fa-x-twitter', 'https://twitter.com/PotomacPhotonic')]
social = container([
    heading(t('heading', 'Follow us'), 13, '600', color=MUTED, lh=19.5),
    w('social-icons', {'social_icon_list': [{'social_icon': {'value': ic, 'library': 'fa-brands'},
                                             'link': {'url': t('url', u), 'is_external': 'on', 'nofollow': ''}, '_id': f's{i}cd34e'}
                                            for i, (ic, u) in enumerate(SOC)],
                       'shape': 'circle', 'icon_color': 'custom', 'icon_size': px(18), 'icon_padding': {'unit': 'em', 'size': 0},
                       'icon_spacing': px(12),
                       'custom_css': ('selector .elementor-social-icon{width:40px;height:40px;display:inline-grid;place-items:center;'
                                      'background:transparent;border:1px solid #DCE1EA;border-radius:50%;color:#3C4858;transition:all .15s}'
                                      'selector .elementor-social-icon i{color:#3C4858;font-size:18px}'
                                      'selector .elementor-social-icon svg{fill:#3C4858;width:18px;height:18px}'
                                      'selector .elementor-social-icon:hover{background:var(--e-global-color-gforange);border-color:var(--e-global-color-gforange);transform:translateY(-2px)}'
                                      'selector .elementor-social-icon:hover i{color:#fff}selector .elementor-social-icon:hover svg{fill:#fff}')}),
], flex_direction='row', flex_wrap='wrap', flex_align_items='center', flex_gap=gap(12, 12), _margin=box(30, 0, 0, 0))
save('offices-grid-6-social', band([head, grid(cards, 2, g=18), social], bg=SUBTLE, align='stretch'), t)
print('ok')
