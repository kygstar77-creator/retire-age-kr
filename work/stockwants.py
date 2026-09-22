# 종목·ETF별로 "사람들이 뭘 찾는지" — 네이버 자동완성 + 검색광고 연관검색어(월 검색수). 글에 꼭 담을 항목을 정하는 근거.
#   python work/stockwants.py SCHD JEPQ 엔비디아 ...   → 종목별 상위 연관어 출력, work/research/wants/<종목>.json 저장
import sys, os, json, time, urllib.request, urllib.parse
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, 'research', 'wants'); os.makedirs(OUT, exist_ok=True)
import importlib.util
spec = importlib.util.spec_from_file_location('kwscan_mod', os.path.join(HERE, 'kwscan.py'))
src = open(os.path.join(HERE, 'kwscan.py'), encoding='utf-8').read().split('num = lambda')[0]   # call() 정의까지만 실행
ns = {}; exec(src, ns); call = ns['call']
def ac(q):
    u = 'https://ac.search.naver.com/nx/ac?' + urllib.parse.urlencode({'q': q, 'con': '1', 'frm': 'nv', 'ans': '2', 'r_format': 'json', 'r_enc': 'UTF-8', 'r_unicode': '0', 't_koreng': '1', 'run': '2', 'rev': '4', 'q_enc': 'UTF-8', 'st': '100'})
    try:
        d = json.load(urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0', 'Referer': 'https://www.naver.com/'}), timeout=15))
        return [x[0] for g in d.get('items', []) for x in g]
    except Exception: return []
num = lambda v: int(v) if str(v).isdigit() else 5
for seed in sys.argv[1:]:
    auto = []
    for q in (seed, seed + ' ', seed + ' 배', seed + ' 세', seed + ' 주', seed + ' 환'):
        for a in ac(q):
            if a not in auto: auto.append(a)
    rel = {}
    for r in call([seed.replace(' ', '')]):
        k = r['relKeyword']
        if seed.replace(' ', '').lower() in k.lower():
            rel[k] = num(r['monthlyPcQcCnt']) + num(r['monthlyMobileQcCnt'])
    time.sleep(0.4)
    top = sorted(rel.items(), key=lambda x: -x[1])[:25]
    json.dump({'seed': seed, 'autocomplete': auto, 'related': dict(top), 'at': time.strftime('%Y-%m-%d')}, open(os.path.join(OUT, seed.replace(' ', '_') + '.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f'\n== {seed} | 자동완성 {len(auto)}개 | 연관어(종목명 포함) {len(rel)}개')
    print('  자동완성:', ' · '.join(auto[:18]))
    print('  검색수:', ' · '.join(f'{k} {v:,}' for k, v in top[:18]))
