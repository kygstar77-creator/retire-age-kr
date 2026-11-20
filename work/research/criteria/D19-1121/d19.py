import sys, json, re, html, time, urllib.request
sys.stdout.reconfigure(encoding='utf-8')
H = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 Mobile/15E148', 'Referer': 'https://m.cafe.naver.com/'}
OUT = sys.argv[1]
M = json.load(open('slugmap.json'))
def get(u):
    try: return json.loads(urllib.request.urlopen(urllib.request.Request(u, headers=H), timeout=20).read().decode('utf-8','ignore'))
    except Exception as e: return {'err': str(e)}
def txt(s): return html.unescape(re.sub(r'<[^>]+>', '', s)).replace('\u200b','').strip()
rows = []
for x in sys.argv[2:]:
    slug, aid = x.split('/')
    r = get(f'https://apis.naver.com/cafe-web/cafe-articleapi/v2.1/cafes/{M.get(slug,slug)}/articles/{aid}?useCafeId=true')
    art = (r.get('result') or {}).get('article') or {}
    h = art.get('contentHtml') or ''
    if not h: print(x, 'NO', str(r)[:120]); continue
    subs = []
    for m in re.finditer(r'<div class="se-component se-(sectionTitle|quotation)[^"]*".*?</div>\s*</div>\s*</div>', h, re.S):
        t = txt(m.group(0))
        if 2 <= len(t) <= 60: subs.append((m.start(), 'blk', t))
    for m in re.finditer(r'<p[^>]*>(.*?)</p>', h, re.S):
        inner = m.group(1); t = txt(inner)
        if 2 <= len(t) <= 40 and re.fullmatch(r'\s*(<span[^>]*>\s*)*<b>.*</b>(\s*</span>)*\s*', inner, re.S): subs.append((m.start(), 'bold', t))
        elif 2 <= len(t) <= 40 and re.match(r'^\s*(\d+[.)]|[■▶●◆★✔️✅#]+|\[)', t): subs.append((m.start(), 'mark', t))
    subs.sort()
    body = txt(h)
    open(f'{OUT}/{slug}_{aid}.txt','w',encoding='utf-8').write((art.get('subject') or '')+'\n'+'\n'.join(l for l in html.unescape(re.sub(r'<[^>]+>','\n',h)).splitlines() if l.strip()))
    row = {'id': x, 'title': art.get('subject'), 'read': art.get('readCount'), 'cmt': art.get('commentCount'), 'chars': len(body), 'subs': [t for _,_,t in subs]}
    rows.append(row)
    print(x, row['read'], row['chars'], len(row['subs']), '|', row['title'][:40], '| 끝3:', ' / '.join(row['subs'][-3:])[:120])
    time.sleep(0.5)
json.dump(rows, open(f'{OUT}/rows.json','w',encoding='utf-8'), ensure_ascii=False, indent=1)
