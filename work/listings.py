# 해외 매물 읽기(대기열 1번) — 파이어맵 해외 도시 글에 쓸 "지금 나와 있는 월세" 실측.
#   py -3.12 work/listings.py 치앙마이 [건수=8]   → 매물 JSON + 생활비(Numbeo, 원화) + 화면에 요약
#   py -3.12 work/listings.py --cities            → 지원 도시와 출처
# 출처: FazWaz(태국·발리, div.result-search__item) · Idealista(포르투갈·스페인, article.item) · Numbeo(생활비·평균 월세, KRW 직접)
# 규칙: 프로필 없는 Playwright chromium(사장님 브라우저 안 씀), 도시당 요청 2회, 숫자는 화면에 있는 것만 적는다.
# 결과: work/research/listings/<도시>_<날짜>.json — facts.txt에 그대로 옮겨 쓸 수 있게 확인일·URL 포함.
import sys, os, re, json, time
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'research', 'listings'); os.makedirs(OUT, exist_ok=True)
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'

# 도시 → (매물 출처, 매물 URL, Numbeo 도시 슬러그)
CITIES = {
    '치앙마이':     ('fazwaz', 'https://www.fazwaz.com/property-for-rent/thailand/chiang-mai', 'Chiang-Mai'),
    '방콕':         ('fazwaz', 'https://www.fazwaz.com/property-for-rent/thailand/bangkok', 'Bangkok'),
    '푸켓':         ('fazwaz', 'https://www.fazwaz.com/property-for-rent/thailand/phuket', 'Phuket'),
    '파타야':       ('fazwaz', 'https://www.fazwaz.com/property-for-rent/thailand/chon-buri/pattaya', 'Pattaya'),
    '리스본':       ('idealista', 'https://www.idealista.pt/en/arrendar-casas/lisboa/', 'Lisbon'),
    '포르투':       ('idealista', 'https://www.idealista.pt/en/arrendar-casas/porto/', 'Porto'),
    # 매물 사이트가 막혔거나 아직 확인 안 된 도시 — 생활비(Numbeo)만 받는다
    # 2026-09-23 실측: fazwaz.com/…/indonesia/bali 404, fazwaz.id Cloudflare 403,
    #                 idealista.com(스페인) 403 — 같은 스크립트로 idealista.pt는 200
    '발리':         (None, None, 'Denpasar'),
    '바르셀로나':   (None, None, 'Barcelona'),
    '발렌시아':     (None, None, 'Valencia'),
    '마드리드':     (None, None, 'Madrid'),
    '다낭':         (None, None, 'Da-Nang'),
    '하노이':       (None, None, 'Hanoi'),
    '호치민':       (None, None, 'Ho-Chi-Minh-City'),
    '쿠알라룸푸르': (None, None, 'Kuala-Lumpur'),
    '페낭':         (None, None, 'George-Town'),
    '세부':         (None, None, 'Cebu'),
    '타이페이':     (None, None, 'Taipei'),
    '부다페스트':   (None, None, 'Budapest'),
    '트빌리시':     (None, None, 'Tbilisi'),
    '메데진':       (None, None, 'Medellin'),
    '후쿠오카':     (None, None, 'Fukuoka'),
    '오사카':       (None, None, 'Osaka'),
}

def page_ctx(pw, locale='en-US'):
    b = pw.chromium.launch(headless=True)          # 사장님 프로필 안 씀
    ctx = b.new_context(user_agent=UA, locale=locale, viewport={'width': 1400, 'height': 1200})
    return b, ctx.new_page()

# ── FazWaz ────────────────────────────────────────────────────────────────
FAZWAZ_JS = r"""(n) => [...document.querySelectorAll('div.result-search__item')].slice(0, n).map(e => {
  const a = [...e.querySelectorAll('a[href]')].map(x => x.href).find(h => /\/property-rent\//.test(h)) || '';
  return { text: e.innerText || '', url: a };
})"""

def fazwaz(page, url, n):
    page.goto(url, wait_until='domcontentloaded', timeout=60000); page.wait_for_timeout(6000)
    rows, seen = [], set()
    for c in page.evaluate(FAZWAZ_JS, n * 3):
        t, u = c['text'], c['url']
        if not u or u in seen: continue
        L = [x.strip() for x in t.splitlines() if x.strip()]
        price = next((x for x in L if '/mo' in x), '')
        persqm = next((x for x in L if '/SqM' in x), '')
        area = next((x for x in L if re.fullmatch(r'[\d,.]+ SqM', x)), '')
        beds = next((L[i - 1] for i, x in enumerate(L) if x.startswith('Bedroom(s)') and i), '')
        baths = next((L[i - 1] for i, x in enumerate(L) if x.startswith('Bathroom(s)') and i), '')
        ptype = next((L[i + 1] for i, x in enumerate(L) if x == 'Property Type:' and i + 1 < len(L)), '')
        built = next((x.replace('Year Built', '').strip() for x in L if x.startswith('Year Built')), '')
        listed = next((x for x in L if x.startswith('LISTED')), '')
        hi = next((i for i, x in enumerate(L) if x.count(',') >= 1 and not re.search(r'SqM|Bedroom|/mo', x)), -1)
        hood = L[hi] if hi >= 0 else ''
        # 단지명은 동네 줄 바로 위 — LISTED/UPDATED 배지와 목록 잔줄(See All 등)은 건너뛴다
        name = next((L[j] for j in range(hi - 1, -1, -1)
                     if not re.match(r'LISTED|UPDATED|NEW|See All|\d+ Propert', L[j])), '') if hi > 0 else ''
        headline = next((x for x in L if ' for rent' in x), '')
        feats = [x for x in L if x in ('High Rise', 'Low Rise', 'Pool', 'Fully Furnished', 'Partly Furnished', 'Unfurnished', 'Pet Friendly')]
        desc = max(L, key=len) if L else ''
        rows.append({'단지': name, '제목': headline, '동네': hood, '월세': price, '㎡당': persqm,
                     '면적': area, '방': beds, '욕실': baths, '유형': ptype, '준공': built,
                     '시설': ', '.join(feats), '게시': listed, '설명': desc[:260], 'URL': u})
        seen.add(u)
        if len(rows) >= n: break
    return rows

# ── Idealista ─────────────────────────────────────────────────────────────
IDEALISTA_JS = r"""(n) => [...document.querySelectorAll('article.item')].slice(0, n).map(e => {
  const a = e.querySelector('a.item-link');
  return { text: e.innerText || '', url: a ? a.href : '' };
})"""

def idealista(page, url, n):
    page.goto(url, wait_until='domcontentloaded', timeout=60000); page.wait_for_timeout(6000)
    rows, seen = [], set()
    for c in page.evaluate(IDEALISTA_JS, n * 2):
        t, u = c['text'], c['url']
        if not u or u in seen: continue
        L = [x.strip() for x in t.splitlines() if x.strip()]
        price = next((x for x in L if '€' in x), '')
        spec = next((x for x in L if re.search(r'\d+\s*m²', x)), '')
        title = next((x for x in L if ',' in x and '€' not in x and 'm²' not in x), '')
        m = re.search(r'([\d.,]+)\s*m²', spec); area = (m.group(1) + ' m²') if m else ''
        m = re.search(r'\bT(\d+)\b|(\d+)\s*(?:bed|hab)', spec, re.I); rooms = m.group(0) if m else ''
        m = re.search(r'(\d+\w{0,2} floor|ground floor|bajo|interior|exterior)', spec, re.I); floor = m.group(1) if m else ''
        feats = ', '.join(x for x in ('with lift', 'without lift') if x in spec)
        hood = title.split(',')[-1].strip() if ',' in title else ''
        desc = max(L, key=len) if L else ''
        rows.append({'단지': title, '제목': title, '동네': hood, '월세': price, '㎡당': '', '면적': area, '방': rooms,
                     '욕실': '', '유형': spec, '준공': '', '시설': (floor + ' ' + feats).strip(),
                     '게시': '', '설명': desc[:260], 'URL': u})
        seen.add(u)
        if len(rows) >= n: break
    return rows

# ── Numbeo(생활비·평균 월세, 원화) ────────────────────────────────────────
NUMBEO_JS = """() => { const t = document.querySelector('table.data_wide_table'); if (!t) return [];
  return [...t.querySelectorAll('tr')].map(r => [...r.querySelectorAll('td,th')].map(c => c.innerText.trim())).filter(r => r.length >= 2); }"""
NUMBEO_KO = {
    '1 Bedroom Apartment in City Centre': '원룸 월세(도심)',
    '1 Bedroom Apartment Outside of City Centre': '원룸 월세(도심 밖)',
    '3 Bedroom Apartment in City Centre': '방 3개 월세(도심)',
    '3 Bedroom Apartment Outside of City Centre': '방 3개 월세(도심 밖)',
    'Meal at an Inexpensive Restaurant': '저렴한 식당 한 끼',
    'Basic Utilities for 85 m2 Apartment': '공과금(85㎡, 월)',
    'Monthly Public Transport Pass (Regular Price)': '대중교통 정기권(월)',
    'Mobile Phone Plan (Monthly, with Calls and 10GB+ Data)': '휴대폰 요금제(월, 10GB+)',
    'Broadband Internet (Unlimited Data, 60 Mbps or Higher)': '인터넷(월, 60Mbps+)',
    'Monthly Fitness Club Membership': '헬스장(월)',
}

def numbeo(page, slug):
    url = f'https://www.numbeo.com/cost-of-living/in/{slug}?displayCurrency=KRW'
    page.goto(url, wait_until='domcontentloaded', timeout=60000); page.wait_for_timeout(2500)
    cost = {}
    for r in page.evaluate(NUMBEO_JS):
        for k, ko in NUMBEO_KO.items():
            if r[0].startswith(k[:38]):
                cost[ko] = {'중앙값': r[1], '범위': r[2] if len(r) > 2 else ''}
    body = page.evaluate('document.body.innerText')
    summary = [l.strip() for l in body.splitlines()
               if re.search(r'estimated monthly costs|less expensive than|more expensive than|^Rent in ', l.strip())]
    return {'URL': url, '항목': cost, '요약': summary[:4]}

# ── 실행 ──────────────────────────────────────────────────────────────────
if len(sys.argv) < 2 or sys.argv[1] == '--cities':
    print('매물+생활비:', ', '.join(c for c, v in CITIES.items() if v[0]))
    print('생활비만   :', ', '.join(c for c, v in CITIES.items() if not v[0]))
    sys.exit(0)

city = sys.argv[1]; want = int(sys.argv[2]) if len(sys.argv) > 2 else 8
if city not in CITIES:
    print(f'모르는 도시: {city}. --cities 로 목록을 본다.'); sys.exit(1)
src, url, slug = CITIES[city]
day = time.strftime('%Y-%m-%d')
res = {'도시': city, '확인일': day, '출처': src or 'numbeo', '매물URL': url, '매물': [], '생활비': {}, '막힘': ''}

with sync_playwright() as pw:
    br, pg = page_ctx(pw)
    try:
        if src:
            try:
                res['매물'] = (fazwaz if src == 'fazwaz' else idealista)(pg, url, want)
                if not res['매물']: res['막힘'] = f'{src} 카드 0건(선택자 또는 차단 확인 필요)'
            except Exception as e:
                res['막힘'] = f'{src} 실패: {type(e).__name__} {str(e)[:120]}'
        else:
            res['막힘'] = '매물 사이트 미확인 — 생활비만'
        try:
            res['생활비'] = numbeo(pg, slug)
        except Exception as e:
            res['막힘'] += f' / numbeo 실패: {type(e).__name__} {str(e)[:120]}'
    finally:
        br.close()

path = os.path.join(OUT, f'{city}_{day}.json')
json.dump(res, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(f'== {city} ({day}) 매물 {len(res["매물"])}건 · 생활비 {len(res["생활비"].get("항목", {}))}항목')
for r in res['매물']:
    print(f' - {r["월세"][:18]:>18} | {r["면적"]:>9} | {r["방"]:>2}방 | {r["단지"][:36]:36} | {r["동네"][:32]}')
for k, v in res['생활비'].get('항목', {}).items():
    print(f'   {k:<18} {v["중앙값"]:>16}   ({v["범위"]})')
for s in res['생활비'].get('요약', []): print('   ·', s[:150])
if res['막힘']: print('막힘:', res['막힘'])
print('저장:', path)
