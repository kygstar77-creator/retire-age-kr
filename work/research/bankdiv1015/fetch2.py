# 네이버 증권 KRX 종가 확인 + 코스피 지수 + DART 배당에 관한 사항(2025 사업보고서) + 2026 분기배당 공시 목록
import json, sys, urllib.request, io, zipfile, re
sys.path.insert(0, '../../')
import apis
H = {'User-Agent': 'Mozilla/5.0'}
def get(u):
    return urllib.request.urlopen(urllib.request.Request(u, headers=H), timeout=25).read().decode('utf-8', 'replace')
T = {'KB금융': '105560', '신한지주': '055550', '하나금융지주': '086790', '우리금융지주': '316140', 'BNK금융지주': '138930'}
nv = {}
for n, c in T.items():
    j = json.loads(get(f'https://m.stock.naver.com/api/stock/{c}/basic'))
    nv[n] = {k: j.get(k) for k in ('closePrice', 'compareToPreviousClosePrice', 'fluctuationsRatio', 'localTradedAt', 'marketStatus')}
    print(n, nv[n])
k = json.loads(get('https://m.stock.naver.com/api/index/KOSPI/basic'))
print('KOSPI', {x: k.get(x) for x in ('closePrice', 'compareToPreviousClosePrice', 'fluctuationsRatio', 'localTradedAt')})
nv['KOSPI'] = k
json.dump(nv, open('src/naver_basic.json', 'w', encoding='utf-8'), ensure_ascii=False)
# DART corp_code
key = apis.key('DART')
z = zipfile.ZipFile(io.BytesIO(urllib.request.urlopen(f'https://opendart.fss.or.kr/api/corpCode.xml?crtfc_key={key}', timeout=60).read()))
x = z.read(z.namelist()[0]).decode('utf-8')
cc = {}
for n, c in T.items():
    m = re.search(r'<corp_code>(\d+)</corp_code>\s*<corp_name>[^<]*</corp_name>\s*(?:<corp_eng_name>[^<]*</corp_eng_name>\s*)?<stock_code>' + c, x)
    cc[n] = m.group(1)
print(cc)
dv = {}
for n, c in cc.items():
    j = json.loads(get(f'https://opendart.fss.or.kr/api/alotMatter.json?crtfc_key={key}&corp_code={c}&bsns_year=2025&reprt_code=11011'))
    dv[n] = j
    for r in j.get('list', []):
        if '주당' in r.get('se', '') and '현금' in r.get('se', '') or '배당성향' in r.get('se','') or '배당수익률' in r.get('se',''):
            print(n, r.get('se'), r.get('stock_knd'), r.get('thstrm'), r.get('frmtrm'))
json.dump({'corp': cc, 'alot': dv}, open('src/dart_alot2025.json', 'w', encoding='utf-8'), ensure_ascii=False)
