"""Ordered content nodes per section (leaves + button/anchor labels + img/iframe refs),
then a 3-way side-by-side alignment MHD | RP | 3DP. Structure is identical per the
signature diff, so the lists pair 1:1 and give the exact substitution table."""
import re,sys
from html.parser import HTMLParser
SKIP={'script','style','svg','path','circle','line','rect','g','defs','use','input','select','textarea','option'}
INLINE={'strong','em','b','i','span','a','sup','sub','code','small','br'}
class N(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack=[]; self.out=[]; self.buf=[]; self.skip=0
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag in SKIP: self.skip+=1; return
        if self.skip: return
        if tag=='img': self._flush(); self.out.append(('IMG',a.get('src','')[:70],a.get('alt',''))); return
        if tag=='iframe': self._flush(); self.out.append(('IFRAME',a.get('src','')[:70],'')); return
        if tag in INLINE: self.buf.append(('open',tag,a)); return
        self._flush(); self.stack.append(tag)
    def handle_startendtag(self,tag,attrs):
        self.handle_starttag(tag,attrs)
        if tag not in ('img','iframe'): self.handle_endtag(tag)
    def handle_endtag(self,tag):
        if tag in SKIP:
            if self.skip: self.skip-=1
            return
        if self.skip: return
        if tag in INLINE: self.buf.append(('close',tag,None)); return
        self._flush()
        if self.stack and self.stack[-1]==tag: self.stack.pop()
    def handle_data(self,d):
        if self.skip: return
        if d.strip(): self.buf.append(('text',d,None))
    def _flush(self):
        if not self.buf: return
        parts=[]
        for k,a,b in self.buf:
            if k=='text': parts.append(a)
            elif k=='open':
                at=''
                if a=='a' and b and b.get('href'): at=f' href="{b["href"]}"'
                if a=='span' and b and 'text-orange' in (b.get('class') or ''): at=' class="text-orange"'
                parts.append(f'<{a}{at}>')
            else: parts.append(f'</{a}>')
        t=re.sub(r'\s+',' ',''.join(parts)).strip()
        if t and re.sub(r'<[^>]+>','',t).strip():
            self.out.append((self.stack[-1] if self.stack else '?', t, ''))
        self.buf=[]
def sections(path):
    h=open(path,encoding='utf-8').read(); out=[]
    for m in re.finditer(r'<section\b',h):
        i=m.start(); depth=0; j=i
        for t in re.finditer(r'</?section\b',h[i:]):
            depth += -1 if t.group().startswith('</') else 1
            if depth==0: j=i+t.end()+1; break
        out.append(h[i:j])
    return out
def nodes(s):
    p=N(); p.feed(s); p._flush(); return p.out
