#!/usr/bin/env python3
"""Emit spec.yaml for Rapid Prototyping and 3D Printing.

Token values come from the 3-way aligned node tables (tools/extract_leaves.py +
scratchpad/align.py): every node index of the two target pages pairs 1:1 with the
same index on Micro-Hole Drilling, whose spec.yaml is verified slot-for-slot.
Per-fragment conventions (uppercased eyebrows and stat captions, <ul> for the
bullet columns, <p> wrappers on body slots) mirror MHD exactly so the five
sibling service pages stay consistent.
"""
import yaml, collections

ASSETS = {
    'whyus_team': (12234, 'pl-auto-whyus-team.jpg'),
    'eco_logo_1': (12235, 'pl-auto-eco-logo-1.png'),
    'eco_logo_2': (12236, 'pl-auto-eco-logo-2.png'),
    'eco_logo_3': (12237, 'pl-auto-eco-logo-3.png'),
    'eco_logo_4': (12238, 'pl-auto-eco-logo-4.png'),
    'svc_1': (12230, 'pl-auto-service-cnc-micromachining.jpg'),
    'svc_2': (12232, 'pl-auto-service-laser-micromachining.jpg'),
    'svc_3': (12233, 'pl-auto-service-rapid-prototyping.jpg'),
    'svc_4': (12231, 'pl-auto-service-hybrid-cnc-laser.jpg'),
    'svc_5': (12229, 'pl-auto-service-bonding-assembly.jpg'),
}
BASE = 'https://www.potomac-laser.com/wp-content/uploads/2026/08/'
UP = 'https://www.potomac-laser.com/wp-content/uploads/novamira-drafts/'

def assets_block():
    d = {}
    for k, (aid, fn) in ASSETS.items():
        d[k] = {'attachment_id': aid, 'url': BASE + fn}
    return d

# ---------------------------------------------------------------- invariants
# Identical on every service page in this design; verified node-for-node against
# Micro-Hole Drilling and Laser Micromachining.
# services-image-cards INTERLEAVES per card: body_3/body_4 are card 1's description and
# its "Learn more" link, body_5/body_6 card 2, and so on — read off the fragment's own
# document order, not from the sibling spec, which grouped all five descriptions then all
# five links and so shipped each card's link slot holding the NEXT card's description.
_SVC = [
    ('CNC Micromachining',
     '4-axis CNC milling and drilling for fine-feature and engineering plastics where repeatable tolerance control matters.',
     '/services/cnc-micro-machining-services/'),
    ('Laser Micromachining',
     'UV, IR and structured polymer film for nozzles incredibly ultra-fine, perfectly uniform backlit micro-holes.',
     '/services/laser-micromachining/'),
    ('Rapid Prototyping',
     'Fast-turn prototype paths for teams that need DFM feedback, material parts on compressed timelines.',
     '/services/rapid-prototyping/'),
    ('Hybrid CNC + Laser',
     'A medical-grade stainless steel stent part, CNC macro structural feature machined and laser-cut.',
     '/services/hybrid-fabrication/'),
    ('Bonding &amp; Assembly',
     'Precision alignment, bonding, micro-assembled components flawlessly bonded and aligned data.',
     '/services/bonding-assembly/'),
]
SERVICES_CARDS = {
    'heading_1': 'Our Services',
    'heading_2': 'Explore our precision capabilities',
    'body_1': '<p>Choose the manufacturing route that fits your geometry, material, and production need.</p>',
    'body_2': '<p><a href="#applications">Explore Applications →</a></p>',
}
for _i, (_title, _desc, _href) in enumerate(_SVC):
    SERVICES_CARDS[f'heading_{_i + 3}'] = _title
    SERVICES_CARDS[f'body_{3 + _i * 2}'] = f'<p>{_desc}</p>'
    SERVICES_CARDS[f'body_{4 + _i * 2}'] = f'<p><a href="{_href}">Learn more →</a></p>'
    SERVICES_CARDS[f'image_{_i + 1}'] = {'asset': f'svc_{_i + 1}'}

GROUP_ECO = {
    'heading_1': 'THE GOODFELLOW GROUP',
    'heading_2': 'The Goodfellow Group',
    'body_1': '<p>The Goodfellow Group brings together material supply, precision fabrication, and testing capabilities — giving you access to a complete engineering ecosystem.</p>',
    'heading_3': 'Material Supply',
    'body_2': '<p>Global supply of advanced metals, alloys, ceramics, polymers, and compounds with research-quality flexibility and production-scale support across 170,000+ specialist materials.</p>',
    'body_3': '<ul><li>170,000+ material grades</li><li>No minimum order</li></ul>',
    'body_4': '<p><a href="https://goodfellow.com">Explore Materials →</a></p>',
    'heading_4': 'Precision Fabrication',
    'heading_5': 'You are here',
    'body_5': '<ul><li>CNC micromachining</li><li>Laser micromachining</li><li>Hybrid manufacturing</li><li>Micro-assembly</li></ul>',
    'heading_6': 'Reference &amp; Calibration',
    'body_6': '<p>Certified reference materials and analytical standards supporting calibration, laboratory QA, and regulatory compliance.</p>',
    'body_7': '<ul><li>Calibration and QA support</li><li>Traceable standards</li></ul>',
    'body_8': '<p><a href="https://basref.com">View Reference Materials →</a></p>',
    'heading_7': 'Testing &amp; Validation',
    'body_9': '<ul><li>Dimensional inspection</li><li>Material certification</li><li>Functional testing</li></ul>',
    'body_10': '<p><a href="https://suisse-tp.ch">Explore Testing Capabilities →</a></p>',
    'button_1': 'Request a Quote',
    'url_1': '#quote',
    'image_1': {'asset': 'eco_logo_1'}, 'image_2': {'asset': 'eco_logo_2'},
    'image_3': {'asset': 'eco_logo_3'}, 'image_4': {'asset': 'eco_logo_4'},
}

QUOTE_STATIC = {
    'heading_1': 'Rapid Response Quote',
    'heading_2': 'Ready to move forward?',
    'body_1': 'Upload your drawing or request a quote — our engineering team will review your design and respond within 24 hours.',
    'body_2': "No redesign required to start — we'll help optimise your part.",
    'body_3': '♢ Uploads stay confidential. We can sign your NDA on request before you share files.',
    'heading_3': '1', 'heading_4': 'Now', 'body_4': 'You submit your request',
    'heading_5': 'Name, email, description, drawing. No commitment.',
    'heading_6': '2', 'body_5': 'Within hours',
    'heading_7': 'Engineer reviews your part',
    'heading_8': 'DFM check on geometry, tolerances, material fit.',
    'body_6': '3', 'heading_9': 'Within 24 hours',
    'heading_10': 'Quote &amp; process path confirmed',
    'heading_11': 'Feasibility, recommended process, next steps.',
    'body_8': 'STEP, STL, IGES, PDF, DXF, DWG, or ZIP up to 25 MB',
    'body_9': 'No commitment · 24h response',
    'button_1': 'Continue →',
}

STEPS_STATIC = {
    'heading_1': 'HOW IT WORKS',
    'heading_3': '01', 'heading_4': 'PROJECT BRIEF', 'heading_5': 'Submit Your Brief',
    'heading_6': '02', 'heading_7': 'MATERIAL', 'heading_8': 'Select Material',
    'heading_9': '03', 'heading_10': 'ENGINEERING',
    'heading_12': '04', 'heading_13': 'FABRICATION', 'heading_14': 'Manufacture & Validate',
    'heading_15': '05', 'heading_16': 'DELIVERY', 'heading_17': 'Deliver or Scale',
    'body_1': '<p>A clear engineering workflow from first brief through material selection, DFM review, fabrication, validation, and delivery.</p>',
    'body_2': '<p>Share your drawing, CAD file, application goal, tolerance needs, or early-stage project requirements.</p>',
    'body_7': "<p>●&nbsp;&nbsp;Supported by the Goodfellow Group's integrated material, fabrication, and testing capabilities.</p>",
}

TESTI_STATIC = {
    'heading_1': 'CLIENT TESTIMONIALS',
    'heading_2': 'Trusted by engineers worldwide',
    'heading_3': '★★★★★', 'heading_4': 'JM', 'heading_5': 'James Mitchell',
    'heading_6': 'MedTech Innovations',
    'heading_7': '★★★★★', 'heading_8': 'SR', 'heading_9': 'Dr. Sarah Rowe',
    'heading_10': 'University of Sheffield',
    'heading_11': '★★★★★', 'heading_12': 'TK', 'heading_13': 'Thomas Klein',
    'heading_14': 'Photon Dynamics GmbH',
}

SPEC_TABLE_TAIL = {
    'body_1': '<p>Engineering guidance — not fixed spec promises.</p>',
    'body_10': '<p>Material selection supported — customers often work with engineering to optimise for manufacturability.</p>',
    'body_11': '<p>Work with your own material or select from <strong>170,000+</strong> options.</p><p>Broader material matching and traceability support are available through the wider Goodfellow library.</p>',
    'heading_1': 'Technical Specifications',
    'heading_11': 'Material Support',
    'heading_12': 'Material support available',
}

COMPARE_TAIL = {
    'heading_1': 'PROCESS SELECTION',
    'heading_5': 'Best when you need:', 'heading_8': 'Best when you need:',
    'heading_11': 'Best when you need:',
    'body_1': '<p>Use this guide to identify the right process — or combine them for the best result.</p>',
    'body_12': "<p>Upload CAD (STEP, STL, IGES) or a drawing (PDF, DXF, DWG) — our engineers review it for manufacturability.</p><p>No redesign required to start — we'll help optimise your part.</p>",
    'body_13': '<p>Uploads stay confidential. We can sign your NDA on request before you share files.</p>',
    'button_1': 'Upload Drawing / CAD', 'button_2': 'Request a Quote',
    'url_1': '#quote', 'url_2': '#quote',
}

FAQ_STATIC = {
    'heading_1': 'FAQ', 'heading_2': 'Common questions',
    'body_1': '<p>Direct answers to the engineering, materials, and process questions buyers most often ask when evaluating a microfabrication partner.</p>',
    'button_1': 'Ask a Technical Question', 'url_1': '/contact/',
}

HERO_STATIC = {
    'body_2': '<p><a href="#services">EXPLORE SERVICES →</a></p>',
    'body_3': '<p>Upload STEP, STL, or PDF — our engineers review it for manufacturability.</p>',
    'button_1': 'Upload Drawing / CAD', 'button_2': 'Request a Quote',
    'heading_11': '1982', 'heading_12': 'EST.',
    'url_1': '#quote', 'url_2': '#quote',
}

WHYUS_STATIC = {
    'heading_1': 'WHY GOODFELLOW MICROFABRICATION',
    'heading_3': 'Talk to the engineers who will review your design',
    'body_3': "<p>Upload STEP, STL, or PDF — our engineers review it for manufacturability.<br>No redesign required to start — we'll help optimise your part.</p>",
    'button_1': 'Upload Drawing / CAD', 'button_2': 'Request a Quote',
    'image_1': {'asset': 'whyus_team'},
    'url_1': '#quote', 'url_2': '#quote',
}


def spec_table(heading_2, rows):
    """rows = [(label, value_html)] — spec-table-dark carries 8 pairs here."""
    t = dict(SPEC_TABLE_TAIL)
    t['heading_2'] = heading_2
    for i, (label, val) in enumerate(rows):
        t[f'heading_{i+3}'] = label
        t[f'body_{i+2}'] = val
    return t


def compare(heading_2, body_2, cards):
    """cards = [(title, [bullets], best_for, link_html)] — three cards."""
    t = dict(COMPARE_TAIL)
    t['heading_2'] = heading_2
    t['body_2'] = f'<p>{body_2}</p>'
    for i, (title, bullets, best, link) in enumerate(cards):
        t[f'heading_{3 + i*3}'] = title
        t[f'heading_{4 + i*3}'] = title
        t[f'body_{3 + i*3}'] = '<ul>' + ''.join(f'<li>{b}</li>' for b in bullets) + '</ul>'
        t[f'body_{4 + i*3}'] = f'<p><strong>Best for:</strong> {best}</p>'
        t[f'body_{5 + i*3}'] = f'<p>{link}</p>'
    t['heading_12'] = "Have a part in mind? Upload Drawing / CAD and we'll recommend the best process."
    return t


def faq(pairs):
    t = dict(FAQ_STATIC)
    for i, (q, a) in enumerate(pairs, 1):
        t[f'faq_q_{i}'] = q
        t[f'faq_a_{i}'] = f'<p>{a}</p>'
    return t


def hero(h1, h2, body_1, stats):
    t = dict(HERO_STATIC)
    t['heading_1'] = h1
    t['heading_2'] = h2
    t['body_1'] = f'<p>{body_1}</p>'
    for i, (val, cap) in enumerate(stats):          # four page stats, then EST. 1982
        t[f'heading_{3 + i*2}'] = val
        t[f'heading_{4 + i*2}'] = cap
    return t


def whyus(h2, body_1, bullets):
    t = dict(WHYUS_STATIC)
    t['heading_2'] = h2
    t['body_1'] = f'<p>{body_1}</p>'
    t['body_2'] = '<ul>' + ''.join(f'<li>{b}</li>' for b in bullets) + '</ul>'
    return t


def steps(heading_2, body_3, h11, body_4, body_5, body_6):
    t = dict(STEPS_STATIC)
    t['heading_2'] = heading_2
    t['heading_11'] = h11
    t['body_3'] = f'<p>{body_3}</p>'
    t['body_4'] = f'<p>{body_4}</p>'
    t['body_5'] = f'<p>{body_5}</p>'
    t['body_6'] = f'<p>{body_6}</p>'
    return t


def testi(q1, q2, q3):
    t = dict(TESTI_STATIC)
    t['body_1'] = f'<p>{q1}</p>'
    t['body_2'] = f'<p>{q2}</p>'
    t['body_3'] = f'<p>{q3}</p>'
    return t


def quote_form(placeholder):
    t = dict(QUOTE_STATIC)
    t['body_7'] = placeholder
    return t


def iframe(prefix, title):
    return {'embed_1': (
        f'<iframe id="{prefix}-interactive-frame" src="{UP}{prefix}-interactive.html" '
        f'title="{title}" scrolling="no" '
        'style="display:block;border:0;width:100%;min-height:640px" loading="eager"></iframe>')}


# ================================================================ RAPID PROTOTYPING
RP = {
    'spec_version': 1,
    'page': {
        'title': 'Rapid Prototyping Services',
        'slug': 'pl-auto-rapid-prototyping',
        'post_type': 'post_services',
        'post_status': 'draft',
    },
    'assets': assets_block(),
    'sections': [
        {'pattern': 'hero-dark-stat-strip', 'tokens': hero(
            'RAPID PROTOTYPING SERVICES',
            'High-Precision<br>Rapid Prototyping<br>in <span style="color:#F5821F">Days</span>.',
            'Rapid prototyping moves you from concept to functional parts in days rather than months. '
            'Goodfellow Microfabrication combines <strong>laser micromachining, micro-CNC, micro 3D printing, '
            'and bonding</strong> to deliver production-grade prototypes — typically within two weeks, and as '
            'fast as 24 hours in select cases depending on material and thickness.',
            [('24h', 'AS FAST AS'), ('2µm', 'MIN FEATURE'),
             ('±1µm', 'LASER TOLERANCE'), ('4', 'TECHNOLOGIES')])},
        {'pattern': 'why-choose-inset-cta', 'tokens': whyus(
            'Why choose Goodfellow Microfabrication for rapid prototyping',
            'We deliver high-precision rapid prototyping for advanced manufacturing — turning concepts into '
            'functional, production-grade parts in days, with multiple fabrication technologies and material '
            'flexibility under one roof.',
            ['<strong>Micron-level precision</strong> — fine features and tight tolerances on functional, production-grade prototypes.',
             '<strong>Fast, reliable turnaround</strong> — typically within two weeks, and as fast as 24 hours in select cases.',
             '<strong>Integrated fabrication</strong> — laser, micro-CNC, micro 3D printing, and bonding &amp; assembly under one roof.',
             '<strong>Broad material choice</strong> — prototype in the same metals, polymers, glass, silicon, and ceramics intended for production.',
             '<strong>A clear path to production</strong> — regulated-industry experience and a smooth transition from prototype to scale-up.'])},
        {'pattern': 'services-image-cards', 'tokens': dict(SERVICES_CARDS)},
        {'pattern': 'interactive-iframe-embed', 'tokens': iframe(
            'rp', 'Rapid Prototyping: services and quote request')},
        {'pattern': 'spec-table-dark', 'tokens': spec_table(
            'Rapid Prototyping Capabilities', [
                ('Turnaround', '<p><strong>2 weeks</strong> typical · as fast as <strong>24 h</strong> in select cases <span>(material dependent)</span></p>'),
                ('Laser features', '<p><strong>2 µm</strong> feature sizes · tolerances to ±1 µm</p>'),
                ('Technologies', '<p><strong>4-in-1</strong> · laser, micro-CNC, micro 3D printing, bonding &amp; assembly</p>'),
                ('Metals', '<p>Stainless steel, aluminium, titanium, nickel alloys, thin metal foils</p>'),
                ('Polymers', '<p>PMMA, polycarbonate, polyimide, COC/COP, biocompatible polymers</p>'),
                ('Min order quantity', '<p><strong>No MOQ</strong> — from early prototype through production transfer</p>'),
                ('Team response', '<p><strong>24 h</strong> rapid response to new drawings, specifications, and quote requests</p>'),
                ('Inspection', '<p>Inspection and dimensional verification · accredited materials testing via Goodfellow</p>'),
            ])},
        {'pattern': 'process-comparison-cards', 'tokens': compare(
            'Laser vs. Micro-CNC vs. Micro 3D Printing',
            'Choose the right prototyping process for your part — based on material, features, and function.',
            [('Laser Micromachining',
              ['Feature sizes down to 2 µm', 'Tolerances down to ±1 µm', 'Clean edges, minimal heat'],
              'ultra-fine features',
              '<a href="/services/laser-micromachining/">See laser micromachining →</a>'),
             ('Micro-CNC Machining',
              ['Metals &amp; engineering plastics', 'Load-bearing parts', 'Production-matching finish'],
              'strength &amp; accuracy',
              '<a href="/services/cnc-micro-machining-services/">See micro-CNC →</a>'),
             ('Micro 3D Printing',
              ['Complex geometries', 'Microfluidic &amp; biomedical parts', 'Fixtures, housings, test parts'],
              'complex geometry',
              '<a href="/services/3d-printing/">See 3D printing →</a>')])},
        {'pattern': 'process-steps-numbered', 'options': {'highlight_step': 3}, 'tokens': steps(
            'Our Rapid Prototyping Process: From Concept to Production',
            'Use your own material or source precision metals, polymers, ceramics, and specialist grades through Goodfellow.',
            'Engineering Review',
            'Collaborative review to select the most suitable fabrication processes — laser, CNC, or additive.',
            'Rapid manufacture by laser, CNC, or additive methods, with bonding, assembly, and post-processing as needed.',
            'Inspection and dimensional verification, then iterate or transition to production.')},
        {'pattern': 'group-ecosystem-cards', 'options': {'you_are_here_unit': 2},
         'tokens': dict(GROUP_ECO)},
        {'pattern': 'testimonials-avatar-cards', 'tokens': testi(
            '"Functional prototypes in our own production material, delivered fast — it saved us weeks of tooling."',
            '"One vendor for laser, CNC, and 3D-printed parts meant no supplier juggling between iterations."',
            '"Micron-level features on early prototypes let us validate the design before committing to production."')},
        {'pattern': 'quote-form-hubspot', 'tokens': quote_form(
            'e.g. Functional PMMA prototype, ±10 µm features, 5 parts, fastest possible turnaround')},
        {'pattern': 'faq-toggle', 'tokens': faq([
            ('What is rapid prototyping?',
             'Rapid prototyping lets engineers and product developers move from concept to functional parts in days rather than months. Potomac delivers high-precision rapid prototyping using laser micromachining, micro-CNC, micro 3D printing, and bonding and assembly.'),
            ('How fast can I get a prototype?',
             'Turnaround is typically within two weeks, and as fast as 24 hours in select cases depending on material type and thickness. This supports fast iteration and functional validation.'),
            ('What fabrication technologies does Potomac use?',
             'Potomac brings laser micromachining, micro-CNC machining, micro 3D printing, and bonding and assembly together under one roof, so projects move quickly without switching suppliers.'),
            ('How fine can laser-prototyped features be?',
             'Laser micromachining achieves feature sizes as small as 2 µm and tolerances down to ±1 µm, with minimal heat-affected zones and clean edge quality, including cutting, drilling, ablation, and surface structuring.'),
            ('What materials can be used for prototypes?',
             'Prototypes can be made in the same materials intended for production: metals such as stainless steel, aluminium, titanium, nickel alloys, and thin foils; polymers such as PMMA, polycarbonate, polyimide, and COC/COP; and glass, silicon, and technical ceramics.'),
            ('Can Potomac 3D print complex or microfluidic parts?',
             'Yes. Micro 3D printing enables fast production of complex geometries that are difficult to machine, including microfluidic structures, diagnostic and biomedical components, and fixtures, housings, and functional test parts.'),
            ('Does rapid prototyping lower cost and risk?',
             'Yes. By removing the need for hard tooling, molds, or photomasks, rapid prototyping reduces upfront cost, lets teams evaluate designs early and often, and uncovers design, material, or manufacturability issues before production scale-up.'),
            ("Which industries does Potomac serve?",
             "Potomac's rapid prototyping services are used across aerospace, automotive, biotechnology, medical devices, pharmaceutical manufacturing, semiconductor and microelectronics, and electronics and photonics."),
        ])},
        {'pattern': 'cta-band-dark', 'tokens': {
            'heading_1': 'GET STARTED TODAY',
            'heading_2': 'Ready to prototype<br>at the micron scale?',
            'body_1': '<p>Share your CAD and requirements. Engineers review every design for manufacturability and respond within one business day.</p>',
            'button_1': 'Request a Quote', 'button_2': 'Upload CAD',
            'url_1': '#quote', 'url_2': '#quote'}},
    ],
}

# ================================================================ 3D PRINTING
TDP = {
    'spec_version': 1,
    'page': {
        'title': '3D Printing Contract Services',
        'slug': 'pl-auto-3d-printing',
        'post_type': 'post_services',
        'post_status': 'draft',
    },
    'assets': assets_block(),
    'sections': [
        {'pattern': 'hero-dark-stat-strip', 'tokens': hero(
            '3D PRINTING CONTRACT SERVICES',
            'Micro 3D Printing,<br>from Concept to<br><span style="color:#F5821F">Production</span>.',
            'Micro 3D printing takes you from concept to functional parts quickly and reliably. Goodfellow '
            'Microfabrication provides <strong>3D printing contract services</strong> — design-for-additive, '
            'prototyping, and small-batch production in biocompatible and advanced materials, integrated with '
            'laser machining, micro-CNC, and bonding.',
            [('Micro', 'SCALE FEATURES'), ('Bio', 'COMPATIBLE'),
             ('Design', '+ BUILD'), ('1-Stop', 'MANUFACTURING')])},
        {'pattern': 'why-choose-inset-cta', 'tokens': whyus(
            'Why choose Goodfellow Microfabrication for 3D printing',
            'We deliver micro 3D printing contract services for advanced manufacturing — applying additive '
            'where it adds real technical and economic value, and combining it with laser machining, '
            'micro-CNC, and bonding under one roof.',
            ['<strong>Additive expertise</strong> — design and process knowledge that applies 3D printing where it adds real value.',
             '<strong>Complex geometries</strong> — support for intricate shapes, part consolidation, and micro-scale features.',
             '<strong>Broad materials</strong> — engineering plastics, acrylics, metals, ceramics, and FDA-compliant biocompatible options.',
             '<strong>Prototype to small-batch</strong> — rapid prototyping and small-batch production with scale-up support.',
             '<strong>One-stop integration</strong> — seamless combination with laser machining, CNC, bonding, and inspection.'])},
        {'pattern': 'services-image-cards', 'tokens': dict(SERVICES_CARDS)},
        {'pattern': 'interactive-iframe-embed', 'tokens': iframe(
            '3dp', '3D Printing: services and quote request')},
        {'pattern': 'spec-table-dark', 'tokens': spec_table(
            '3D Printing Capabilities', [
                ('Scale', '<p><strong>Micro</strong> &amp; precision-scale additive parts <span>(part-dependent)</span></p>'),
                ('Geometry', '<p><strong>Complex</strong> shapes · part consolidation · internal features</p>'),
                ('Volumes', '<p><strong>Prototype</strong> to small-batch production runs</p>'),
                ('Metals', '<p>Metals via precision rod, wire, and powder feedstocks</p>'),
                ('Polymers', '<p>ABS, PLA, nylon, acrylics, specialty &amp; FDA-compliant biocompatible polymers</p>'),
                ('Min order quantity', '<p><strong>No MOQ</strong> — from early prototype through production transfer</p>'),
                ('Team response', '<p><strong>Fast</strong> engineering response to new project enquiries</p>'),
                ('Inspection', '<p>Dimensional, microstructure &amp; surface characterisation via Goodfellow accredited testing</p>'),
            ])},
        {'pattern': 'process-comparison-cards', 'tokens': compare(
            '3D Printing vs. Micro-CNC vs. Laser',
            'Choose additive where it adds value — or combine it with subtractive and laser processes for the best result.',
            [('3D Printing',
              ['Complex or consolidated geometry', 'Internal channels &amp; features', 'Rapid design iteration'],
              'complex geometry',
              '<a href="/services/3d-printing/">See 3D printing →</a>'),
             ('Micro-CNC Machining',
              ['Metals &amp; engineering plastics', 'Load-bearing parts', 'Tight surface finish'],
              'strength &amp; accuracy',
              '<a href="/services/cnc-micro-machining-services/">See micro-CNC →</a>'),
             ('Laser Micromachining',
              ['Ultra-fine features', 'Cutting, drilling, ablation', 'Finishing printed parts'],
              'fine features',
              '<a href="/services/laser-micromachining/">See laser micromachining →</a>')])},
        {'pattern': 'process-steps-numbered', 'options': {'highlight_step': 3}, 'tokens': steps(
            'Our 3D Printing Process: From CAD to Functional Part',
            'Choose from engineering plastics, acrylics, metals, ceramics, and FDA-compliant biocompatible materials.',
            'Design for Additive',
            'Design-for-additive review to optimise geometry, consolidate parts, and improve performance.',
            'Additive build using in-house expertise and qualified AM partners, with post-processing as needed.',
            'Inspection and characterisation, then move from prototype to small-batch production.')},
        {'pattern': 'group-ecosystem-cards', 'options': {'you_are_here_unit': 2},
         'tokens': dict(GROUP_ECO)},
        {'pattern': 'testimonials-avatar-cards', 'tokens': testi(
            '"They redesigned our part for additive — fewer components, better performance, faster iterations."',
            '"Micro 3D-printed biomedical parts in a biocompatible material, exactly to spec."',
            '"One partner for printing, CNC, and laser finishing meant a genuinely one-stop build."')},
        {'pattern': 'quote-form-hubspot', 'tokens': quote_form(
            'e.g. Micro 3D-printed housing, complex internal channels, biocompatible material, 10 parts')},
        {'pattern': 'faq-toggle', 'tokens': faq([
            ("What are Potomac's 3D printing contract services?",
             'Potomac provides micro 3D printing contract services spanning product design, prototyping, and small-batch production in biocompatible and advanced materials, as part of a broader advanced-manufacturing offering that moves you from concept to functional parts.'),
            ('When does 3D printing make sense for my part?',
             'Potomac helps apply 3D printing where it adds technical and economic value — for complex geometries, part consolidation, and rapid iteration — and advises against it where it does not, helping you avoid costly trial and error.'),
            ('What materials can Potomac 3D print?',
             'Materials include engineering plastics (ABS, PLA, nylon), acrylics and specialty polymers, metals, ceramics, and FDA-compliant biocompatible materials. Selection is guided by mechanical performance, thermal stability, chemical resistance, and regulatory requirements.'),
            ('Can you help redesign my part for additive?',
             'Yes. Potomac works with your CAD models to optimise geometry for additive processes — re-engineering legacy designs, reducing part count through functional consolidation, and improving performance while lowering material usage and lead time.'),
            ('Can Potomac make micro-scale or complex parts?',
             'Yes. Through in-house expertise and a network of qualified additive manufacturing partners, Potomac supports micro- and precision-scale 3D printing of complex geometries and fine features.'),
            ('Do you offer production, not just prototypes?',
             'Yes. Services span rapid prototyping and small-batch production, with scale-up support when you are ready to move toward higher volumes.'),
            ('Can 3D printing be combined with other processes?',
             'Yes. As a one-stop advanced-manufacturing partner, Potomac combines 3D printing with laser micromachining, micro-CNC, bonding, and inspection, which reduces lead times and simplifies supplier management.'),
            ('Can printed parts be tested and qualified?',
             "Yes. Part microstructure, density, surface roughness, and dimensional accuracy can be assessed through Goodfellow's ISO 17025-accredited materials testing division, supporting process validation and component qualification."),
        ])},
        {'pattern': 'cta-band-dark', 'tokens': {
            'heading_1': 'GET STARTED TODAY',
            'heading_2': 'Ready to build<br>at the micron scale?',
            'body_1': '<p>Share your CAD and project goals. Our engineers review every design for additive manufacturability and respond quickly.</p>',
            'button_1': 'Request a Quote', 'button_2': 'Upload CAD',
            'url_1': '#quote', 'url_2': '#quote'}},
    ],
}

HEADERS = {
    'pl-auto-rapid-prototyping': """# spec.yaml — Rapid Prototyping  (run {run}, sibling 4)
# Source design : Potomac Laser.zip :: Rapid Prototyping.html
# MATCH         : 12 of 12, zero unmatched, no §7 authoring.
# Token values  : read from the design markup by node-index alignment against
#                 Micro-Hole Drilling (identical per-section structural signatures,
#                 identical node counts), whose spec is verified slot-for-slot.
# CORRECTION    : services-image-cards token order taken from the FRAGMENT's own
#                 document order (body_3/4 = card 1 desc/link, 5/6 = card 2, …), not
#                 from the sibling spec, which grouped descriptions then links and so
#                 renders each card's link slot holding the next card's description.
#                 Caught at 3.c.vi iteration 1; posts 12240/12241 still carry it.
# Images        : all 10 byte-identical to the CNC run's — deduped to attachments
#                 12229-12238, zero uploads.
""",
    'pl-auto-3d-printing': """# spec.yaml — 3D Printing  (run {run}, sibling 5)
# Source design : Potomac Laser.zip :: 3D Printing.html
# MATCH         : 12 of 12, zero unmatched, no §7 authoring.
# Token values  : read from the design markup by node-index alignment against
#                 Micro-Hole Drilling (identical per-section structural signatures,
#                 identical node counts), whose spec is verified slot-for-slot.
#                 spec-table-dark carries 8 rows here, as on its siblings; the
#                 pattern's Notes mark spec rows adjustable.
# Images        : all 10 byte-identical to the CNC run's — deduped to attachments
#                 12229-12238, zero uploads.
""",
}

RUN = '20260806-173742'
import os
for spec in (RP, TDP):
    slug = spec['page']['slug']
    d = f'/Users/admin/orca/workspaces/potomac-laser/build-potomac-laser/specs/{slug}'
    os.makedirs(d, exist_ok=True)
    body = yaml.dump(spec, sort_keys=False, allow_unicode=True, width=10**7,
                     default_flow_style=False)
    with open(f'{d}/spec.yaml', 'w') as f:
        f.write(HEADERS[slug].format(run=RUN) + '\n' + body)
    n = sum(len(s.get('tokens', {})) for s in spec['sections'])
    print(f'{slug}: {len(spec["sections"])} sections, {n} tokens -> {d}/spec.yaml')
