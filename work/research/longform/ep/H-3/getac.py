# 네이버 자동완성(연관검색어) — 사람들이 실제로 치는 말. 무료·키 없음(ac.search.naver.com). 실행: py -3.12 getac.py <편> 검색어...
import sys, os, json, urllib.request, urllib.parse, datetime
sys.stdout.reconfigure(encoding='utf-8')
ep, qs = sys.argv[1], sys.argv[2:]
W = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
out = {'at': datetime.datetime.now().strftime('%Y-%m-%d %H:%M'), 'src': 'https://ac.search.naver.com/nx/ac', 'q': {}}
for q in qs:
    u = 'https://ac.search.naver.com/nx/ac?q=' + urllib.parse.quote(q) + '&con=1&frm=nv&ans=2&r_format=json&r_enc=UTF-8&r_unicode=0&t_koreng=1&run=2&rev=4&q_enc=UTF-8&st=100'
    d = json.loads(urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'}), timeout=15).read().decode('utf-8'))
    out['q'][q] = [x[0] for x in d['items'][0]]
    print(q, '→', ' | '.join(out['q'][q]))
json.dump(out, open(os.path.join(W, ep, 'raw', f'naver_ac_{datetime.date.today():%m%d}.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
