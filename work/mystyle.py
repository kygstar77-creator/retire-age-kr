# 사장님 블로그의 옛 글(자동화 전, 2024년 이전)에서 말투를 잰다 — 루틴이 사장님 목소리로 쓰게 하기 위한 근거.
#   python work/mystyle.py  → work/research/mystyle.md (어미 분포·문장 길이·첫 문장·자주 쓰는 표현·표본 문장)
import sys, re, json, html, urllib.request, collections, os
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright
UA={'User-Agent':'Mozilla/5.0'}
rss=urllib.request.urlopen(urllib.request.Request('https://rss.blog.naver.com/kygstar7777.xml',headers=UA),timeout=20).read().decode('utf-8','ignore')
items=re.findall(r'<item>(.*?)</item>',rss,re.S)
old=[]
for it in items:
    t=html.unescape(re.sub(r'<!\[CDATA\[|\]\]>','',re.search(r'<title>(.*?)</title>',it,re.S).group(1)))
    d=re.search(r'<pubDate>(.*?)</pubDate>',it).group(1); log=re.search(r'/(\d{9,})',it).group(1)
    if '2026' not in d: old.append((t,d,log))
print('옛 글', len(old), '편')
texts=[]
with sync_playwright() as p:
    b=p.chromium.launch(headless=True); page=b.new_page(locale='ko-KR')
    for t,d,log in old:
        page.goto(f'https://m.blog.naver.com/PostView.naver?blogId=kygstar7777&logNo={log}',wait_until='domcontentloaded'); page.wait_for_timeout(4000)
        try: body=page.evaluate("() => { const c=document.querySelector('.se-main-container')||document.querySelector('#postViewArea')||document.querySelector('.post_ct')||document.querySelector('#viewTypeSelector'); return c? c.innerText : '' }")
        except Exception: body=''
        body=re.sub(r'[\u200b\xa0]+',' ',body).strip()
        if len(body)>200: texts.append((t,d,body))
    b.close()
print('본문 확보', len(texts), '편')
sents=[]
for t,d,body in texts:
    for s in re.split(r'(?<=[.!?])\s+|\n+', body):
        s=s.strip()
        if 6<=len(s)<=200: sents.append(s)
endings=collections.Counter()
for s in sents:
    m=re.search(r'(습니다|입니다|해요|예요|이에요|네요|죠|거든요|ㄴ다|는다|다|까요|요|자|니다)[.!?]?$', s)
    endings[m.group(1) if m else '기타']+=1
lens=sorted(len(s) for s in sents)
firsts=[body.split('\n')[0][:80] for _,_,body in texts]
words=collections.Counter(w for s in sents for w in re.findall(r'[가-힣]{2,}', s))
common=[w for w,_ in words.most_common(400) if w not in ('있습니다','합니다','것입니다','있는','하는','있다','한다')][:60]
out=['# 사장님 블로그 말투 실측 (자동화 이전 글, %d편·문장 %d개)'%(len(texts),len(sents)), '',
     '## 어미 분포', *[f'- {k}: {v} ({v*100//len(sents)}%)' for k,v in endings.most_common(12)], '',
     f'## 문장 길이(글자): 중앙값 {lens[len(lens)//2]}, 상위 25% {lens[int(len(lens)*0.75)]}, 최장 {lens[-1]}', '',
     '## 글 첫 문장(그대로)', *[f'- {f}' for f in firsts], '',
     '## 자주 쓰는 말', ' · '.join(common), '',
     '## 표본 문장(무작위 40)']
import random; random.seed(1)
out+= [f'- {s}' for s in random.sample(sents, min(40,len(sents)))]
os.makedirs('work/research',exist_ok=True); open('work/research/mystyle.md','w',encoding='utf-8').write('\n'.join(out))
json.dump([{'title':t,'date':d,'text':b} for t,d,b in texts], open('work/research/mystyle_posts.json','w',encoding='utf-8'), ensure_ascii=False)
print('\n'.join(out[:20]))
