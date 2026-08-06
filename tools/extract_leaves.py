"""Leaf text nodes of a design section, in document order, inline markup preserved.

TRANSLATE §6 needs design copy mapped onto fragment token slots. Regex cannot do it:
a non-greedy `<div ...>(.*?)</div>` stops at the FIRST closing tag, so on nested markup
it skips whole nodes. Measured on the Laser Micromachining page 2026-08-06 — regex found
15 of 24 nodes in the capabilities section and silently mapped a *description* onto
`heading_3`. A real parser found all 24 and aligned slot-for-slot with the fragment.

Use for sections with no prior build to read values from. Where a prior build exists in
the same fragment structure (a `draft-blocks` page), prefer its stored widget values —
they are already this page's copy, and B9 makes the legends unusable for that purpose.

    from tools.extract_leaves import leaves
    nodes = leaves(section_html)      # [(parent_tag, "text with <strong>inline</strong>"), ...]
"""
from html.parser import HTMLParser
import re
SKIP={'script','style','svg','path','circle','line','rect','g','defs','use','br','img','input','select','textarea','option','button'}
INLINE={'strong','em','b','i','span','a','sup','sub','code','small','br'}
class Leaves(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack=[]; self.out=[]; self.buf=[]; self.depth_skip=0
    def handle_starttag(self,tag,attrs):
        if tag in SKIP and tag not in ('br',): self.depth_skip+=1; return
        if self.depth_skip: return
        if tag in INLINE:
            self.buf.append(('open',tag,dict(attrs))); return
        self._flush()
        self.stack.append(tag)
    def handle_endtag(self,tag):
        if tag in SKIP and tag not in ('br',):
            if self.depth_skip: self.depth_skip-=1
            return
        if self.depth_skip: return
        if tag in INLINE:
            self.buf.append(('close',tag,None)); return
        self._flush()
        if self.stack and self.stack[-1]==tag: self.stack.pop()
    def handle_data(self,data):
        if self.depth_skip: return
        if data.strip(): self.buf.append(('text',data,None))
    def _flush(self):
        if not self.buf: return
        parts=[]
        for kind,a,b in self.buf:
            if kind=='text': parts.append(a)
            elif kind=='open':
                attr=''
                if a=='a' and b and b.get('href'): attr=f' href="{b["href"]}"'
                parts.append(f'<{a}{attr}>')
            else: parts.append(f'</{a}>')
        txt=re.sub(r'\s+',' ',''.join(parts)).strip()
        if txt and re.sub(r'<[^>]+>','',txt).strip():
            self.out.append((self.stack[-1] if self.stack else '?', txt))
        self.buf=[]
def leaves(html):
    p=Leaves(); p.feed(html); p._flush(); return p.out
