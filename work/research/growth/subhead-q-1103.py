import sys, json, re, time, html, urllib.request
sys.stdout.reconfigure(encoding='utf-8')
RAW = sys.argv[1]
H = {'User-Agent': 'Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 Chrome/126 Mobile Safari/537.36', 'Referer': 'https://m.cafe.naver.com/'}
def get(u):
    try: return json.loads(urllib.request.urlopen(urllib.request.Request(u, headers=H), timeout=20).read().decode('utf-8','ignore'))
    except Exception as e: return {'err': str(e)}
INFO = {31050378,23676262,22290117,14028420,30786704,31097286,30852806,28497937,20898041}
d = json.load(open(RAW, encoding='utf-8'))
cands = []
for c in d:
    cid = int(c.get('cafeId') or 0)
    if cid not in INFO: continue
    for a in sorted((c.get('popular') or []), key=lambda x: -(x.get('read') or 0))[:25]:
        cands.append((cid, c.get('name'), a))
print('후보', len(cands))
def txt(s): return html.unescape(re.sub(r'<[^>]+>', '', s)).replace('\u200b','').strip()
rows = []
for cid, name, a in cands:
    aid = a.get('aid')
    r = get(f'https://apis.naver.com/cafe-web/cafe-articleapi/v2.1/cafes/{cid}/articles/{aid}?useCafeId=true')
    art = (r.get('result') or {}).get('article') or {}
    h = art.get('contentHtml') or ''
    if not h: continue
    body = txt(h)
    if len(body) < 800: continue
    subs = []
    for m in re.finditer(r'<div class="se-component se-(sectionTitle|quotation)[^"]*".*?</div>\s*</div>\s*</div>', h, re.S):
        t = txt(m.group(0));
        if 2 <= len(t) <= 60: subs.append(('blk', t))
    for m in re.finditer(r'<p[^>]*>(.*?)</p>', h, re.S):
        inner = m.group(1); t = txt(inner)
        if 2 <= len(t) <= 40 and re.fullmatch(r'\s*(<span[^>]*>\s*)*<b>.*</b>(\s*</span>)*\s*', inner, re.S):
            subs.append(('bold', t))
    rows.append({'cafe': name, 'aid': aid, 'title': art.get('subject') or a.get('subject'), 'read': a.get('read'), 'chars': len(body),
                 'subs': [t for _, t in subs], 'q': sum(1 for _, t in subs if t.rstrip().endswith('?'))})
    time.sleep(0.4)
json.dump(rows, open('subq_rows.json','w',encoding='utf-8'), ensure_ascii=False, indent=1)
withs = [r for r in rows if r['subs']]
ns = sum(len(r['subs']) for r in withs); nq = sum(r['q'] for r in rows)
print('본문 800자+', len(rows), '소제목 있는 글', len(withs), '소제목 합', ns, '물음 소제목', nq, '물음 소제목 있는 글', sum(1 for r in rows if r['q']), '전부 물음', sum(1 for r in withs if r['q']==len(r['subs'])))
for r in withs[:40]: print(r['cafe'][:8], r['aid'], r['read'], len(r['subs']), r['q'], '|', ' / '.join(r['subs'][:4])[:150])
