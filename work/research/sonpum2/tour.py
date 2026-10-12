# "대신 둘러봐 드립니다" 재료 v3 — 동네 이름만 주면 한 동네를 통째로 만든다(사장님 2026-09-30 "전부 고치고").
#   py -3.12 work/research/sonpum2/tour.py 11440 1144010200 공덕동 마포구   → work/video/tour.json (+ 캐시 work/research/sonpum2/<법정동코드>/)
# 쓰는 재료(전부 무료·공개, 네이버 부동산 화면은 쓰지 않는다 — 저작권법 제93조 DB권·다윈중개 판결):
#   국토부 실거래(research/rt, rtmolit.py) · 국토부 공동주택 단지목록 AptListService4 + 기본·상세 AptBasisInfoServiceV5(이용허락 제한 없음)
#   오픈스트리트맵(ODbL, 화면에 출처) — Overpass(지도·보행로·역 출입구·학교·마트) · Nominatim(도로명 주소 → 좌표, 초당 1회 이하)
# v2에서 고친 것(사장님 "100% 완벽해?"에 내가 짚은 것):
#   ① 면적이 다른 단지끼리 평당가를 비교했다 → 동네에서 거래가 가장 많은 면적대 하나로만 비교한다
#   ② 층을 안 보고 최근·최고를 견줬다 → 층을 같이 싣는다
#   ③ 동떨어진 거래(같은 면적대 중앙값의 ±20% 밖)를 그대로 썼다 → 따로 표시하고 최근·최고 계산에서 뺀다
#   ④ 역까지 직선거리였다 → 보행로를 따라 걷는 거리(지하철 출입구까지)로 재고, 관리사무소 등록 정보(역·도보 시간)를 같이 싣는다
#   ⑤ 14단지 중 8곳만 다뤘다 → 공동주택 목록 전체에서 시작해 주소·좌표로 지도 단지를 찾는다
import json, glob, math, os, sys, re, time, heapq, statistics as st, collections, urllib.request, urllib.parse
sys.stdout.reconfigure(encoding='utf-8')
GU, BJD, UMD, GUNM = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
HERE = os.path.dirname(os.path.abspath(__file__)); WORK = os.path.join(HERE, '..', '..'); RT = os.path.join(WORK, 'research', 'rt')
C = os.path.join(HERE, BJD); os.makedirs(C, exist_ok=True)
OUT = os.path.join(WORK, 'video', 'tour.json')
UA = {'User-Agent': 'firemap-research/1.0 (kygstar77@gmail.com)'}
PY = 3.305785
def num(s): return float(str(s or '0').replace(',', '') or 0)
def cache(name, make):
    p = os.path.join(C, name)
    if not os.path.exists(p): json.dump(make(), open(p, 'w', encoding='utf-8'), ensure_ascii=False)
    return json.load(open(p, encoding='utf-8'))
def hav(a, b, c, d):
    p1, p2 = math.radians(a), math.radians(c)
    return 2 * 6371000 * math.asin(math.sqrt(math.sin((p2 - p1) / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(math.radians(d - b) / 2) ** 2))

# ── 실거래(최근 12개월 파일) ──
def load(kind):
    ms = sorted({os.path.basename(f).split('_')[1] for f in glob.glob(os.path.join(RT, f'{GU}_2*_trade.json'))})[-12:]
    rows = []
    for m in ms:
        f = os.path.join(RT, f'{GU}_{m}_{kind}.json')
        if os.path.exists(f):
            d = json.load(open(f, encoding='utf-8')); rows += d if isinstance(d, list) else d.get('rows', [])
    return rows
TALL = load('trade'); RALL = load('rent')
T = [r for r in TALL if r.get('umdNm') == UMD and not r.get('cdealType') and r.get('buyerGbn') != '공공기관']
RA = [r for r in RALL if r.get('umdNm') == UMD]
months = sorted({r['dealYear'] + r['dealMonth'].zfill(2) for r in T})
def band(r): return int(num(r['excluUseAr']) // 5 * 5)
def ppy(r): return num(r['dealAmount']) / (num(r['excluUseAr']) / PY)
def road(r):
    if not r.get('roadNm') and not r.get('roadnm'): return None
    if r.get('roadNm'):
        b, s = int(r.get('roadNmBonbun') or 0), int(r.get('roadNmBubun') or 0); return f"{r['roadNm']} {b}" + (f'-{s}' if s else '')
    return r['roadnm'].strip()   # 전월세는 '창전로2길 42' 꼴로 온다

# ── 공동주택 단지 정보 ──
KEY = [l.split('=', 1)[1].strip() for l in open(r'C:\Users\강영준\Documents\datago_key.txt', encoding='utf-8-sig') if l.startswith('KEY=')][0]
def api(path, q): return json.loads(urllib.request.urlopen(f'https://apis.data.go.kr/1613000/{path}?serviceKey={KEY}&{q}', timeout=30).read().decode('utf-8', 'ignore'))
def make_kapt():
    lst = api('AptListService4/getLegaldongAptList4', f'bjdCode={BJD}&numOfRows=200&pageNo=1')['response']['body']['items']
    return {x['kaptCode']: {'b': api('AptBasisInfoServiceV5/getAphusBassInfoV5', 'kaptCode=' + x['kaptCode'])['response']['body']['item'],
                            'd': api('AptBasisInfoServiceV5/getAphusDtlInfoV5', 'kaptCode=' + x['kaptCode'])['response']['body']['item']} for x in lst}
KAPT = cache('kapt.json', make_kapt)
RENTAL = ('임대', '행복주택')
def make_geo():
    out = {}
    for code, v in KAPT.items():
        q = (v['b'].get('doroJuso') or '').strip()
        r = json.load(urllib.request.urlopen(urllib.request.Request('https://nominatim.openstreetmap.org/search?' + urllib.parse.urlencode(
            {'q': q, 'format': 'json', 'limit': 1, 'countrycodes': 'kr', 'addressdetails': 1}), headers=UA), timeout=30))
        out[code] = r[0] if r else None; time.sleep(1.2)
    return out
GEO = cache('geo.json', make_geo)
pts = [(float(g['lat']), float(g['lon'])) for g in GEO.values() if g]
la0, la1 = min(p[0] for p in pts) - 0.007, max(p[0] for p in pts) + 0.007
lo0, lo1 = min(p[1] for p in pts) - 0.009, max(p[1] for p in pts) + 0.009
BB = f'{la0:.4f},{lo0:.4f},{la1:.4f},{lo1:.4f}'

def overpass(q):
    req = urllib.request.Request(os.environ.get('OVERPASS_URL', 'https://overpass-api.de/api/interpreter'), data=urllib.parse.urlencode({'data': q}).encode(), headers=UA)
    return json.load(urllib.request.urlopen(req, timeout=180))
OSM = cache('osm.json', lambda: overpass(f"""[out:json][timeout:150];
( way["landuse"="residential"]({BB}); relation["landuse"="residential"]({BB}); way["building"="apartments"]["name"]({BB});
  node["railway"="station"]({BB}); node["station"="subway"]({BB}); node["railway"="subway_entrance"]({BB});
  way["highway"]({BB}); way["leisure"="park"]({BB}); relation["boundary"="administrative"]["admin_level"="8"]({BB}); ); out geom;"""))['elements']
POI = cache('poi.json', lambda: overpass(f"""[out:json][timeout:90];
( nwr["amenity"="school"]({BB}); nwr["shop"="supermarket"]({BB}); nwr["shop"="department_store"]({BB}); ); out center tags;"""))['elements']

def rings(e):
    if e['type'] == 'way' and e.get('geometry'): return [[[p['lon'], p['lat']] for p in e['geometry']]]
    return [[[p['lon'], p['lat']] for p in m['geometry']] for m in e.get('members', []) if m.get('geometry') and m.get('role') == 'outer']
def inside(lon, lat, ring):
    c = False
    for i in range(len(ring)):
        (x1, y1), (x2, y2) = ring[i], ring[i - 1]
        if (y1 > lat) != (y2 > lat) and lon < (x2 - x1) * (lat - y1) / (y2 - y1) + x1: c = not c
    return c
def nname(s): return re.sub(r'아파트|단지|\s|\(.*?\)|삼성|[0-9]+동$', '', s or '')
POLY = [e for e in OSM if e['type'] in ('way', 'relation') and (e.get('tags', {}).get('landuse') == 'residential' or e.get('tags', {}).get('building') == 'apartments') and rings(e)]

# ── 공동주택 → 지도 단지(규칙과 이유를 남긴다) ──
def match_poly(code):
    b = KAPT[code]['b']; addr = (b.get('doroJuso') or '').strip(); g = GEO.get(code)
    tail = ' '.join(addr.split()[-2:])                                        # '마포대로11길 84'
    for e in POLY:                                                            # (가) OSM 주소가 도로명 주소와 같다
        t = e.get('tags', {})
        hn_ = t.get('addr:housenumber') or t.get('addr:housename') or ''
        if t.get('addr:street') and f"{t['addr:street']} {hn_}".strip() == tail: return e, f'OSM 주소 {tail} 일치'
    hn = g and (g.get('address') or {}).get('house_number')
    if hn:                                                                    # (나) 번지까지 잡힌 주소 좌표가 이름 있는 단지 안에 있다
        lat, lon = float(g['lat']), float(g['lon'])
        hit = [e for e in POLY if e.get('tags', {}).get('name') and any(inside(lon, lat, r) for r in rings(e))]
        if len(hit) > 1: hit = [e for e in hit if e.get('tags', {}).get('landuse') == 'residential'] or hit   # 동 건물보다 단지 경계
        if len(hit) == 1: return hit[0], f'주소 좌표({tail})가 단지 안'
    kn = nname(b['kaptName'])                                                 # (다) 이름이 같다(아파트·단지·삼성·띄어쓰기 빼고)
    same = [e for e in POLY if nname(e.get('tags', {}).get('name')) == kn]
    if len(same) == 1: return same[0], '이름 일치'
    same = [e for e in POLY if nname(e.get('tags', {}).get('name')) and sorted(nname(e['tags']['name'])) == sorted(kn)]
    if len(same) == 1: return same[0], '이름 일치(글자 순서만 다름)'
    return None, '못 찾음'

# ── 실거래 → 공동주택(도로명 주소) ──
def kapt_by_road(rd, jibun=None):
    hit = [c for c, v in KAPT.items() if rd and (v['b'].get('doroJuso') or '').strip().endswith(' ' + rd)]
    if not hit and jibun: hit = [c for c, v in KAPT.items() if f' {UMD} {jibun} ' in ' ' + (v['b'].get('kaptAddr') or '') + ' ']   # 한 단지에 도로명이 둘인 곳(래미안공덕5차: 마포대로 167 / 173-15)
    if len(hit) > 1: hit = [c for c in hit if not any(w in KAPT[c]['b']['kaptName'] for w in RENTAL)]
    return hit[0] if len(hit) == 1 else None
trade_k = collections.defaultdict(list); unk = collections.Counter()
for r in T:
    k = kapt_by_road(road(r) or '', r.get('jibun'))
    (trade_k[k].append(r) if k else unk.update([r['aptNm']]))
rent_k = collections.defaultdict(list)
for r in RA:
    k = kapt_by_road(road(r) or '', r.get('jibun'))
    if k: rent_k[k].append(r)

# ── 보행 그래프(OSM 길 전부, 자동차 전용 제외) ──
NODE = {}; ADJ = collections.defaultdict(list)
for e in OSM:
    t = e.get('tags', {})
    if e['type'] != 'way' or 'highway' not in t or t['highway'] in ('motorway', 'motorway_link') or t.get('foot') == 'no' or not e.get('geometry'): continue
    ids = e.get('nodes') or []; g = e['geometry']
    for i, p in enumerate(g):
        nid = ids[i] if i < len(ids) else f"{e['id']}_{i}"; NODE[nid] = (p['lat'], p['lon'])
        if i:
            pid = ids[i - 1] if i - 1 < len(ids) else f"{e['id']}_{i-1}"; w = hav(*NODE[pid], p['lat'], p['lon'])
            ADJ[pid].append((nid, w)); ADJ[nid].append((pid, w))
GRID = collections.defaultdict(list)
for nid, (a, b) in NODE.items(): GRID[(round(a, 3), round(b, 3))].append(nid)
def snap(lat, lon):
    best = None
    for da in (-0.001, 0, 0.001):
        for db in (-0.001, 0, 0.001):
            for nid in GRID.get((round(lat + da, 3), round(lon + db, 3)), []):
                d = hav(lat, lon, *NODE[nid])
                if best is None or d < best[1]: best = (nid, d)
    return best
def dijkstra(src):
    D = {src: 0}; P = {}; q = [(0, src)]
    while q:
        d, u = heapq.heappop(q)
        if d > D[u] or d > 2500: continue
        for v, w in ADJ[u]:
            if d + w < D.get(v, 1e18): D[v] = d + w; P[v] = u; heapq.heappush(q, (d + w, v))
    return D, P
def path(P, v):
    out = [v]
    while out[-1] in P: out.append(P[out[-1]])
    return [[NODE[n][1], NODE[n][0]] for n in reversed(out)]

stations = []; seen = set()
for e in OSM:
    t = e.get('tags', {})
    if e['type'] == 'node' and (t.get('railway') == 'station' or t.get('station') == 'subway') and t.get('name') and t['name'] not in seen:
        seen.add(t['name']); stations.append({'name': t['name'], 'lat': e['lat'], 'lon': e['lon']})
entr = [{'lat': e['lat'], 'lon': e['lon'], 'st': min(stations, key=lambda s: hav(e['lat'], e['lon'], s['lat'], s['lon']))['name']}
        for e in OSM if e['type'] == 'node' and e.get('tags', {}).get('railway') == 'subway_entrance'] if stations else []
def pt(e): return (e['lat'], e['lon']) if 'lat' in e else (e['center']['lat'], e['center']['lon'])
schools = [dict(name=e['tags']['name'], lat=pt(e)[0], lon=pt(e)[1]) for e in POI if e.get('tags', {}).get('amenity') == 'school'
           and re.search(r'초등학교$', e['tags'].get('name', ''))]
marts = [dict(name={'E-Mart': '이마트'}.get(e['tags']['name'], e['tags']['name']), lat=pt(e)[0], lon=pt(e)[1]) for e in POI
         if e.get('tags', {}).get('name') in ('E-Mart', '이마트', '롯데마트', '홈플러스', '홈플러스 익스프레스', '이마트 에브리데이', '롯데슈퍼', 'GS더프레시')]
parks = [dict(name=e['tags']['name'], lat=st.mean(p['lat'] for p in e['geometry']), lon=st.mean(p['lon'] for p in e['geometry']))
         for e in OSM if e['type'] == 'way' and e.get('tags', {}).get('leisure') == 'park' and '공원' in e['tags'].get('name', '') and e.get('geometry')]
def walk_to(D, P, lst, label=lambda x: x['name']):
    best = None
    for x in lst:
        sn = snap(x['lat'], x['lon'])
        if not sn or sn[0] not in D: continue
        d = D[sn[0]] + sn[1]
        if best is None or d < best['m']: best = {'name': label(x), 'm': d, 'lat': x['lat'], 'lon': x['lon'], 'route': path(P, sn[0])}
    if best: best['m'] = int(round(best['m'], -1)); best['route'] = best['route'][::max(1, len(best['route']) // 60)] + [best['route'][-1]]
    return best

# ── 전월세 환산(히트맵과 같은 식, 신규 계약만) ──
sys.path.insert(0, WORK); import heatmap_re as HR
rates, rbase, rn = HR.conv_rate(RALL); CR = rates.get(GUNM, rbase) / 100
NEW = [r for r in RA if r.get('contractType') == '신규' and num(r.get('excluUseAr')) > 0]
def pj(r): return (num(r['deposit']) + num(r['monthlyRent']) * 12 / CR) / (num(r['excluUseAr']) / PY)
def pw(r): return (num(r['monthlyRent']) + num(r['deposit']) * CR / 12) / (num(r['excluUseAr']) / PY)
umd_j = st.median(num(r['deposit']) / (num(r['excluUseAr']) / PY) for r in NEW if num(r['monthlyRent']) == 0); umd_w = st.median(pw(r) for r in NEW if num(r['monthlyRent']) > 0)

# 동네 비교 면적대 — 이 동네 매매가 가장 많은 5㎡ 면적대 하나(①)
TOPB = collections.Counter(band(r) for r in T).most_common(1)[0][0]
def blabel(b): return {55: '59㎡대', 80: '84㎡대', 45: '49㎡대', 70: '74㎡대', 75: '76㎡대'}.get(b, f'{b}~{b+5}㎡')

complexes, skipped = [], []
groups = collections.defaultdict(list)
for code, v in KAPT.items():
    if any(w in v['b']['kaptName'] for w in RENTAL): continue
    e, how = match_poly(code)
    if not e: skipped.append((v['b']['kaptName'], how)); continue
    groups[f"{e['type']}/{e['id']}"].append((code, how, e))
for oid, items in groups.items():
    e = items[0][2]; codes = [c for c, _, _ in items]; how = ' / '.join(sorted({h for _, h, _ in items}))
    rows = [r for c in codes for r in trade_k.get(c, [])]
    if not rows: skipped.append((KAPT[codes[0]]['b']['kaptName'], '1년 매매 없음')); continue
    poly = rings(e); allp = [p for rg in poly for p in rg]; clat = st.mean(p[1] for p in allp); clon = st.mean(p[0] for p in allp)
    bs = [KAPT[c]['b'] for c in codes]; ds = [KAPT[c]['d'] for c in codes]
    hh = sum(int(b.get('kaptdaCnt') or 0) for b in bs); pk = sum(int(d.get('kaptdPcnt') or 0) + int(d.get('kaptdPcntu') or 0) for d in ds)
    name = re.sub(r'\s*\d단지$', '', bs[0]['kaptName']).replace(' 아파트', '').replace('아파트', '') + (f"({'·'.join(re.findall(r'(\d)단지', ' '.join(b['kaptName'] for b in bs)))}단지)" if len(bs) > 1 else '')
    # 면적대별
    mb = collections.Counter(band(r) for r in rows).most_common(1)[0][0]
    rb = sorted([r for r in rows if band(r) == mb], key=lambda r: (r['dealYear'], r['dealMonth'].zfill(2), r['dealDay'].zfill(2)))
    med = st.median(num(r['dealAmount']) for r in rb)
    odd = lambda r: abs(num(r['dealAmount']) / med - 1) > 0.2 if len(rb) >= 4 else False   # ③
    ok = [r for r in rb if not odd(r)] or rb
    last = ok[-1]; mx = max(ok, key=lambda r: num(r['dealAmount']))
    topr = [r for r in rows if band(r) == TOPB and not (band(r) == mb and odd(r))]
    js = [num(r['deposit']) for r in rent_k.get(codes[0], []) + [x for c in codes[1:] for x in rent_k.get(c, [])] if num(r.get('monthlyRent')) == 0 and r.get('contractType') == '신규' and band(r) == mb]
    new = [r for c in codes for r in rent_k.get(c, []) if r.get('contractType') == '신규' and num(r.get('excluUseAr')) > 0]
    pjs = [num(r['deposit']) / (num(r['excluUseAr']) / PY) for r in new if num(r['monthlyRent']) == 0]   # 평당 전세는 순수 전세만 — 월세를 전환율로 전세에 섞으면 월세 많은 단지가 과하게 낮게 나온다(공덕현대 -58%, 2026-09-30)
    pws = [pw(r) for r in new if num(r['monthlyRent']) > 0]
    sn = snap(clat, clon); D, P = dijkstra(sn[0]) if sn else ({}, {})
    stw = walk_to(D, P, entr, lambda x: x['st'] + '역 출입구') if entr else None
    if stw: stw['station'] = stw['name'].replace(' 출입구', '').replace('역', '')
    use = bs[0].get('kaptUsedate') or ''
    complexes.append({
        'name': name, 'codes': codes, 'how': how, 'poly': poly, 'lat': clat, 'lon': clon,
        'built': use[:4] or rows[0]['buildYear'], 'n': len(rows), 'band': mb, 'bandLabel': blabel(mb), 'area': round(st.median(num(r['excluUseAr']) for r in rb), 2), 'nb': len(rb),
        'ppyTop': round(st.median(ppy(r) for r in topr)) if len(topr) >= 2 else None, 'nTop': len(topr),
        'deals': [{'ym': r['dealYear'] + '.' + r['dealMonth'].zfill(2), 'd': int(r['dealDay']), 'amt': int(num(r['dealAmount'])), 'floor': r['floor'], 'odd': odd(r)} for r in rb],
        'nOdd': sum(odd(r) for r in rb),
        'last': {'ym': last['dealYear'] + '.' + last['dealMonth'].zfill(2), 'amt': int(num(last['dealAmount'])), 'floor': last['floor']},
        'max': {'ym': mx['dealYear'] + '.' + mx['dealMonth'].zfill(2), 'amt': int(num(mx['dealAmount'])), 'floor': mx['floor']},
        'fromMax': round((num(last['dealAmount']) / num(mx['dealAmount']) - 1) * 100, 1),
        'jeonse': int(st.median(js)) if len(js) >= 3 else None, 'nj': len(js), 'saleMed': int(med),
        'jratio': round(st.median(js) / med * 100, 1) if len(js) >= 3 else None,
        'rent': {'j': round(st.median(pjs)) if len(pjs) >= 3 else None, 'nj': len(pjs), 'w': round(st.median(pws), 1) if len(pws) >= 3 else None, 'nw': len(pws),
                 'jd': round((st.median(pjs) / umd_j - 1) * 100, 1) if len(pjs) >= 3 else None, 'wd': round((st.median(pws) / umd_w - 1) * 100, 1) if len(pws) >= 3 else None},
        'kapt': {'hh': hh, 'dong': sum(int(b.get('kaptDongCnt') or 0) for b in bs), 'top': max(int(b.get('kaptTopFloor') or 0) for b in bs),
                 'use': f'{use[:4]}.{use[4:6]}' if len(use) >= 6 else None, 'heat': bs[0].get('codeHeatNm'), 'builder': bs[0].get('kaptBcompany'),
                 'park': pk, 'parkPer': round(pk / hh, 2) if hh else None, 'subway': ds[0].get('subwayStation'), 'subwayWalk': ds[0].get('kaptdWtimesub')},
        'walk': {'station': stw, 'school': walk_to(D, P, schools), 'park': walk_to(D, P, parks), 'mart': walk_to(D, P, marts)},
    })
complexes.sort(key=lambda c: -c['n'])
TOUR = [c['name'] for c in complexes][:4]

bg = {'roads': [], 'parks': [], 'others': []}; used = set(groups)
for e in OSM:
    t = e.get('tags', {})
    if e['type'] == 'way' and t.get('highway') in ('motorway', 'trunk', 'primary', 'secondary', 'tertiary', 'residential', 'unclassified', 'living_street') and e.get('geometry'):
        bg['roads'].append({'k': t['highway'], 'pts': [[p['lon'], p['lat']] for p in e['geometry']]})
    elif e['type'] == 'way' and t.get('leisure') == 'park' and e.get('geometry'): bg['parks'].append([[p['lon'], p['lat']] for p in e['geometry']])
    elif e['type'] == 'way' and (t.get('landuse') == 'residential' or t.get('building') == 'apartments') and e.get('geometry') and f"way/{e['id']}" not in used:
        bg['others'].append([[p['lon'], p['lat']] for p in e['geometry']])
adm = next((e for e in OSM if e['type'] == 'relation' and e.get('tags', {}).get('name') == UMD), None)
out = {'umd': UMD, 'gu': GUNM, 'period': f'{months[0][:4]}.{months[0][4:]} ~ {months[-1][:4]}.{months[-1][4:]}', 'nTrade': len(T), 'checked': time.strftime('%Y-%m-%d'),
       'conv': round(CR * 100, 2), 'umdJ': round(umd_j), 'umdW': round(umd_w, 1), 'nNew': len(NEW), 'topBand': TOPB, 'topLabel': blabel(TOPB),
       'nKapt': len(KAPT), 'skipped': skipped, 'unmatchedTrades': dict(unk), 'complexes': complexes, 'tour': TOUR,
       'stations': stations, 'bg': bg, 'boundary': rings(adm) if adm else []}
json.dump(out, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False)
print(f"{GUNM} {UMD} · {out['period']} 매매 {len(T)}건 · 신규 전월세 {len(NEW)}건 · 전환율 {CR*100:.2f}% · 비교 면적대 {blabel(TOPB)}")
print('공동주택', len(KAPT), '곳 · 지도에 올린 단지', len(complexes), '· 빠진 곳', skipped, '· 공동주택과 못 맞춘 실거래', dict(unk))
for c in complexes:
    w = c['walk']; s = w['station']
    print(f"{c['name']:14} {c['built']} {c['kapt']['hh']}세대 주차 {c['kapt']['parkPer']} | {c['bandLabel']} {c['nb']}건(동떨어진 {c['nOdd']}) 최근 {c['last']['ym']} {c['last']['amt']:,}({c['last']['floor']}층) 최고 {c['max']['ym']} {c['max']['amt']:,}({c['max']['floor']}층) {c['fromMax']:+}% | {out['topLabel']} 평당 {c['ppyTop']} ({c['nTop']}건) | 전세가율 {c['jratio']} | 평당전세 {c['rent']['j']}({c['rent']['jd']}%) | 걸어서 {s['name'] if s else '-'} {s['m'] if s else ''}m · 관리사무소 {c['kapt']['subway']} {c['kapt']['subwayWalk']} | 학교 {w['school']['name'] if w['school'] else '-'} {w['school']['m'] if w['school'] else ''}m | {c['how']}")
