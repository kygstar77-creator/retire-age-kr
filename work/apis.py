# 사장님이 발급해 준 키를 실제로 쓰는 자리 — 2026-09-23.
# 사장님: "내가 api 연동도 다 해줬잖아!" 맞는 말이었다. 키 11개 중 4개만 쓰이고 7개가 놀고 있었다.
# 원인은 키 파일이 `KEY=값` 형식인데 내가 파일 전체를 키로 읽어 전부 인증 실패로 보였던 것.
#
#   py -3.12 work/apis.py            → 키마다 실제로 한 번씩 불러 되는지 보여 준다
#   py -3.12 work/apis.py fred DGS10 → 개별 확인
#
# 다른 스크립트에서는 `import apis` 후 아래 함수를 쓴다. 숫자는 전부 출처가 있는 1차 자료다.
import sys, os, re, json, time, urllib.request, urllib.parse
sys.stdout.reconfigure(encoding='utf-8')
D = os.path.expanduser('~/Documents')
UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126 Safari/537.36'}

def key(name):
    """키 파일은 `KEY=값` 또는 `PEXELS_API_KEY=값` 형식이다. 값만 꺼낸다."""
    p = os.path.join(D, name + '_key.txt')
    if not os.path.exists(p): return None
    s = open(p, encoding='utf-8-sig', errors='ignore').read()
    m = re.search(r'^[A-Z_]*KEY\s*=\s*(\S+)', s, re.M)
    if m: return m.group(1)
    line = s.strip().splitlines()
    return line[0].strip() if line else None

def _j(u, t=25):
    r = urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=t)
    return json.loads(r.read().decode('utf-8', 'ignore'))

# ── 미국 ───────────────────────────────────────────────────────────────────
FRED_SERIES = {'기준금리': 'FEDFUNDS', '10년국채': 'DGS10', '2년국채': 'DGS2', '소비자물가': 'CPIAUCSL',
               '실업률': 'UNRATE', '근원물가': 'CPILFESL', '원달러': 'DEXKOUS', '30년주담대': 'MORTGAGE30US'}

def fred(series='FEDFUNDS', n=1):
    """미국 경제지표 — 세인트루이스 연준(FRED). 반환: [(날짜, 값)] 최신순."""
    k = key('fred')
    if not k: return []
    u = f'https://api.stlouisfed.org/fred/series/observations?series_id={series}&api_key={k}&file_type=json&limit={n}&sort_order=desc'
    return [(o['date'], o['value']) for o in _j(u).get('observations', []) if o.get('value') not in (None, '.')]

def av_quote(symbol):
    """미국 종목·ETF 현재가 — Alpha Vantage. 무료는 분당 5회·하루 25회 제한이 있다."""
    k = key('alphavantage')
    if not k: return None
    d = _j(f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={urllib.parse.quote(symbol)}&apikey={k}').get('Global Quote', {})
    if not d: return None
    return {'종목': d.get('01. symbol'), '종가': d.get('05. price'), '전일대비': d.get('09. change'),
            '등락률': d.get('10. change percent'), '기준일': d.get('07. latest trading day')}

# ── 국내 ───────────────────────────────────────────────────────────────────
def dart_list(bgn=None, end=None, count=20, corp_code=None):
    """국내 공시 목록 — 금융감독원 DART. bgn/end는 YYYYMMDD."""
    k = key('dart')
    if not k: return []
    bgn = bgn or time.strftime('%Y%m%d'); end = end or bgn
    u = f'https://opendart.fss.or.kr/api/list.json?crtfc_key={k}&bgn_de={bgn}&end_de={end}&page_count={count}'
    if corp_code: u += f'&corp_code={corp_code}'
    d = _j(u)
    if d.get('status') != '000': return []
    return [{'회사': x.get('corp_name'), '보고서': x.get('report_nm'), '접수일': x.get('rcept_dt'),
             '링크': 'https://dart.fss.or.kr/dsaf001/main.do?rcpNo=' + x.get('rcept_no', '')} for x in d.get('list', [])]

ECOS_STATS = {'기준금리·여수신금리': ('722Y001', 'M'), '예금은행 수신금리': ('721Y001', 'M'), '소비자물가지수': ('901Y009', 'M')}

def ecos(stat='722Y001', cycle='M', start=None, end=None, item='0101000', n=12):
    """한국은행 경제통계(ECOS). 반환: [(시점, 값, 항목명)] """
    k = key('ecos')
    if not k: return []
    end = end or time.strftime('%Y%m'); start = start or time.strftime('%Y%m', time.localtime(time.time() - n * 31 * 86400))
    u = f'https://ecos.bok.or.kr/api/StatisticSearch/{k}/json/kr/1/{n}/{stat}/{cycle}/{start}/{end}/{item}'
    d = _j(u).get('StatisticSearch', {})
    return [(r.get('TIME'), r.get('DATA_VALUE'), r.get('ITEM_NAME1')) for r in d.get('row', [])]

FIN_GROUP = {'은행': '020000', '저축은행': '030300', '신협': '050000', '보험': '050000'}

def finlife(kind='deposit', group='020000', page=1):
    """예금·적금·주담대·전세대출 금리 — 금융감독원 금융상품통합비교공시.
    kind: deposit(정기예금) / saving(적금) / mortgage(주택담보대출) / rent(전세자금대출) / credit(신용대출)"""
    k = key('finlife')
    if not k: return []
    ep = {'deposit': 'depositProductsSearch', 'saving': 'savingProductsSearch', 'mortgage': 'mortgageLoanProductsSearch',
          'rent': 'rentHouseLoanProductsSearch', 'credit': 'creditLoanProductsSearch'}[kind]
    d = _j(f'http://finlife.fss.or.kr/finlifeapi/{ep}.json?auth={k}&topFinGrpNo={group}&pageNo={page}').get('result', {})
    if d.get('err_cd') != '000': return []
    base = {b['fin_prdt_cd']: b for b in d.get('baseList', [])}
    out = []
    for o in d.get('optionList', []):
        b = base.get(o['fin_prdt_cd'], {})
        out.append({'은행': b.get('kor_co_nm'), '상품': b.get('fin_prdt_nm'),
                    '기간': o.get('save_trm'), '금리': o.get('intr_rate'), '최고금리': o.get('intr_rate2'),
                    '대출최저': o.get('lend_rate_min'), '대출최고': o.get('lend_rate_max'), '공시월': b.get('dcls_month')})
    return out

def vworld_coord(address, road=None):
    """주소 → 좌표. 국토교통부 브이월드. 손품 영상(sonpum.py)이 동네를 찾을 때 쓴다.
    '목동 917' 같은 지번 주소는 road로는 안 잡힌다(2026-09-23 확인) → 도로명·지번을 차례로 시도한다."""
    k = key('vworld')
    if not k: return None
    kinds = ['road', 'parcel'] if road is None else (['road'] if road else ['parcel'])
    for t in kinds:
        u = ('https://api.vworld.kr/req/address?service=address&request=getcoord&format=json'
             f'&key={k}&type={t}&address=' + urllib.parse.quote(address))
        try: d = _j(u).get('response', {})
        except Exception: continue
        if d.get('status') != 'OK': continue
        p = d['result']['point']
        return {'주소': (d.get('refined') or {}).get('text', address), '경도': float(p['x']), '위도': float(p['y']), '방식': t}
    return None

def building(sigungu_cd, bjdong_cd, bun, ji='0'):
    """단지의 세대수·주차대수·준공일·동수. 국토교통부 건축HUB 건축물대장(2026-09-24 승인).
    사장님 2026-09-23 "평수나 내부구조 세대수 주차장 연식 등도 봐야지".

    **총괄표제부(getBrRecapTitleInfo)를 쓴다.** 표제부(getBrTitleInfo)는 동마다 한 줄이라
    24개 동을 다 받아도 세대수·주차가 0으로 나온다(경로당 같은 부속건축물이 섞인다).
    총괄표제부는 단지 전체를 한 줄로 준다 — 래미안신당하이베르 세대 784·주차 968·16개 동으로 확인.

    인자는 실거래 자료에 그대로 있다: sggCd, umdCd, bonbun, bubun."""
    k = key('datago')
    if not k: return None
    u = ('https://apis.data.go.kr/1613000/BldRgstHubService/getBrRecapTitleInfo'
         f'?serviceKey={urllib.parse.quote(k, safe="")}&sigunguCd={sigungu_cd}&bjdongCd={bjdong_cd}'
         f'&bun={str(bun).zfill(4)}&ji={str(ji or "0").zfill(4)}&_type=json&numOfRows=5')
    PARK = ('indrAutoUtcnt', 'oudrAutoUtcnt', 'indrMechUtcnt', 'oudrMechUtcnt')

    def rows(url):
        try: b = _j(url, 30)['response']['body']
        except Exception: return []
        it = b.get('items'); it = (it.get('item') if isinstance(it, dict) else it) or []
        return it if isinstance(it, list) else [it]

    def pack(x, dong):
        park = sum(_i(x.get(f)) for f in PARK)
        d = str(x.get('useAprDay') or '')
        hh = _i(x.get('hhldCnt'))
        return {'단지': x.get('bldNm') or x.get('dongNm'), '주소': x.get('platPlc'), '세대수': hh,
                '주차대수': park, '동수': dong,
                '준공': f'{d[:4]}년 {int(d[4:6])}월' if len(d) >= 6 else '',
                '세대당주차': round(park / hh, 2) if hh else None}

    it = rows(u)
    if it:
        x = max(it, key=lambda z: _i(z.get('hhldCnt')))
        if _i(x.get('hhldCnt')): return pack(x, _i(x.get('mainBldCnt')))

    # 총괄표제부는 단지형에만 있다. 오피스텔·연립처럼 한 동짜리는 표제부에서 주건축물만 합친다
    # (부속건축물인 경로당·관리동이 섞이면 세대수가 0으로 나온다 — 2026-09-24 확인).
    u2 = u.replace('getBrRecapTitleInfo', 'getBrTitleInfo').replace('numOfRows=5', 'numOfRows=100')
    main = [x for x in rows(u2) if _i(x.get('hhldCnt'))]
    if not main: return None
    hh = sum(_i(x.get('hhldCnt')) for x in main)
    park = sum(sum(_i(x.get(f)) for f in PARK) for x in main)
    big = max(main, key=lambda z: _i(z.get('hhldCnt')))
    d = str(big.get('useAprDay') or '')
    return {'단지': big.get('bldNm') or big.get('dongNm'), '주소': big.get('platPlc'), '세대수': hh,
            '주차대수': park, '동수': len(main),
            '준공': f'{d[:4]}년 {int(d[4:6])}월' if len(d) >= 6 else '',
            '세대당주차': round(park / hh, 2) if hh else None}

def _i(x):
    try: return int(float(x or 0))
    except Exception: return 0

def _dist_m(lat1, lng1, lat2, lng2):
    import math
    R = 6371000.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp, dl = math.radians(lat2 - lat1), math.radians(lng2 - lng1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return int(2 * R * math.asin(math.sqrt(a)))

def vworld_nearby(lat, lng, query, n=3, box=0.012):
    """그 좌표 둘레에서 '지하철역'·'초등학교' 같은 것을 찾아 직선거리(m)와 함께 돌려준다.
    사장님 2026-09-23 손품 아이디어: "집집마다 가격 구조 역과의 거리 주변에 뭐 있는지, 경사 접근성 학교".
    2026-09-23 공덕동에서 확인: 공덕역·서울공덕초등학교가 좌표까지 나온다."""
    k = key('vworld')
    if not k: return []
    bbox = f'{lng-box},{lat-box},{lng+box},{lat+box}'
    u = ('https://api.vworld.kr/req/search?service=search&request=search&version=2.0&format=json'
         f'&size=20&page=1&query={urllib.parse.quote(query)}&type=place&key={k}&crs=EPSG:4326&bbox={bbox}')
    try: r = _j(u).get('response', {})
    except Exception: return []
    if r.get('status') != 'OK': return []
    out = []
    for it in (r.get('result', {}) or {}).get('items', []) or []:
        p = it.get('point') or {}
        try: x, y = float(p['x']), float(p['y'])
        except Exception: continue
        out.append({'이름': it.get('title'), '분류': (it.get('category') or '').strip(),
                    '거리m': _dist_m(lat, lng, y, x), '위도': y, '경도': x})
    seen, uniq = set(), []
    for o in sorted(out, key=lambda z: z['거리m']):
        if o['이름'] in seen: continue
        seen.add(o['이름']); uniq.append(o)
    return uniq[:n]

def around(lat, lng):
    """손품 영상·부동산 글에 넣을 '주변' 한 줄 — 역·초등학교·중학교.
    '마트'로 찾으면 '○○마트부동산공인중개사사무소'가 섞여 나온다(2026-09-23 확인) → 분류로 거른다."""
    out = {}
    for label, q, must in (('지하철역', '역', '철도'), ('초등학교', '초등학교', '초등학교'),
                           ('중학교', '중학교', '중학교'), ('고등학교', '고등학교', '고등학교')):
        r = [x for x in vworld_nearby(lat, lng, q, n=8) if must in x['분류'] or must in x['이름']]
        if r: out[label] = [f"{x['이름']} {x['거리m']}m" for x in r[:2]]
        time.sleep(0.4)
    return out

CHECKS = [
    ('fred  미국 기준금리', lambda: fred('FEDFUNDS', 1)),
    ('fred  미국 10년 국채', lambda: fred('DGS10', 1)),
    ('alphavantage  SCHD 시세', lambda: av_quote('SCHD')),
    ('dart  오늘 공시', lambda: dart_list(count=3)),
    ('ecos  한국은행 기준금리', lambda: ecos(n=3)),
    ('finlife  정기예금 금리', lambda: finlife('deposit')[:3]),
    ('finlife  주택담보대출 금리', lambda: finlife('mortgage')[:3]),
    ('vworld  주소→좌표', lambda: vworld_coord('서울특별시 마포구 공덕동 256')),
]

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'fred':
        print(fred(sys.argv[2] if len(sys.argv) > 2 else 'FEDFUNDS', 5)); sys.exit()
    ok = 0
    for name, f in CHECKS:
        try:
            r = f()
            good = bool(r)
            ok += good
            print(('  O ' if good else '  X ') + name + ' : ' + json.dumps(r, ensure_ascii=False)[:150])
        except Exception as e:
            print('  X ' + name + ' : ' + str(e)[:110])
        time.sleep(1)
    print(f'\n{ok}/{len(CHECKS)} 동작')
