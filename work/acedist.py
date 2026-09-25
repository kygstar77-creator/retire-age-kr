# ACE(한국투자신탁운용) ETF의 분배금 지급 이력을 운용사 공식 API에서 그대로 읽어온다.
# 왜 필요한가: etfdist.py는 KODEX(삼성자산운용)만 읽는다. 2026-09-25 23시 회차에서
#   ACE 미국배당다우존스 분배금 장부를 쓰려다 읽을 도구가 없어 상품 페이지를 Playwright로
#   직접 열어야 했다. 그 과정에서 상품 페이지가 실제로 부르는 공식 API를 찾았고,
#   그 API는 HTTP만으로 읽힌다(브라우저가 필요 없다).
#   Nasdaq 배당 API가 종목에 따라 N/A만 돌려주는 것과 달리 이쪽은 값이 그대로 온다.
# 쓰는 법: py -3.12 work/acedist.py                      (등록된 ETF 목록과 펀드코드)
#          py -3.12 work/acedist.py 미국배당다우존스      (이름으로 찾아 분배금 이력)
#          py -3.12 work/acedist.py K55101DN4471          (펀드코드를 직접 줘도 된다)
# 결과: 기준일 · 지급일 · 주당분배금 · 분배율, 그리고 상품 기본정보(현재가·NAV·순자산·총보수).
#       research/etfdist/ace_<펀드코드>.json 에도 같이 남긴다.
import sys, json, pathlib, urllib.request, urllib.parse

PAPI = 'https://papi.aceetf.co.kr/api'
SITE = 'https://www.aceetf.co.kr'
OUT = pathlib.Path(__file__).resolve().parent / 'research' / 'etfdist'
H = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
     'Accept': 'application/json', 'Referer': SITE + '/'}


def get(url):
    return json.load(urllib.request.urlopen(urllib.request.Request(url, headers=H), timeout=30))


def find_fund(want):
    """이름 조각으로 펀드코드를 찾는다. 펀드코드를 그대로 줬으면 그대로 쓴다."""
    if want.startswith('K55') and len(want) >= 10:
        return want, want
    q = urllib.parse.quote(want)
    for path in (f'/funds?searchValue={q}&page=1&size=50', f'/funds/search?searchValue={q}'):
        try:
            d = get(PAPI + path)
        except Exception:
            continue
        for k in ('fundList', 'list', 'content', 'data'):
            for row in (d.get(k) or []) if isinstance(d, dict) else []:
                nm = row.get('fund_NM') or row.get('fundNm') or row.get('name') or ''
                cd = row.get('fund_CD') or row.get('fundCd') or ''
                if want in nm and cd:
                    return cd, nm
    return None, None


def dividends(fund_cd):
    rows = []
    for page in range(1, 8):
        d = get(f'{PAPI}/funds/{fund_cd}/dividend?page={page}')
        L = d.get('dividendList') or []
        if not L:
            break
        rows += L
    def fmt(s):
        return f'{s[:4]}.{s[4:6]}.{s[6:]}' if s and len(s) == 8 else (s or '')
    return [{'base': fmt(r.get('std_DT')), 'paid': fmt(r.get('dividend_DT')),
             'amount': r.get('dividend_PRI'), 'rate': r.get('dividend_RATE')} for r in rows]


def product(fund_cd):
    """상품 기본정보. 키 이름이 바뀔 수 있어 찾은 것만 담는다."""
    try:
        d = get(f'{PAPI}/funds/{fund_cd}/product')
    except Exception as e:
        return {'error': str(e)}
    flat = {}
    def walk(o, pre=''):
        if isinstance(o, dict):
            for k, v in o.items():
                walk(v, pre + k + '.')
        elif not isinstance(o, list):
            flat[pre.rstrip('.')] = o
    walk(d)
    return flat


def main():
    want = sys.argv[1] if len(sys.argv) > 1 else ''
    OUT.mkdir(parents=True, exist_ok=True)
    if not want:
        print('펀드 이름 조각이나 펀드코드를 준다. 예: py -3.12 work/acedist.py 미국배당다우존스')
        print('알려진 것: ACE 미국배당다우존스 = K55101DN4471 (종목코드 402970)')
        return 1
    cd, nm = find_fund(want)
    if not cd:
        print(f'"{want}"로 펀드를 못 찾았다. 펀드코드를 직접 주거나 상품 페이지에서 확인한다: {SITE}')
        return 2
    rows = dividends(cd)
    if not rows:
        print(f'분배금 기록이 비어 있다. 펀드코드 {cd}')
        return 3
    url = f'{PAPI}/funds/{cd}/dividend?page=1'
    print(f'출처: {url} · 펀드 {nm or cd} · {len(rows)}건 (최신순)')
    for r in rows:
        rate = f"{r['rate']:.4f}%" if isinstance(r['rate'], (int, float)) else str(r['rate'])
        print(f"  기준일 {r['base']}  지급 {r['paid']}  {str(r['amount'])+'원':>7}  분배율 {rate}")
    amts = [r['amount'] for r in rows[:12] if isinstance(r['amount'], (int, float))]
    if len(amts) == 12:
        print(f'  최근 12건 합계 {sum(amts)}원 · 최저 {min(amts)}원 · 최고 {max(amts)}원'
              f' · 최고÷최저 {max(amts)/min(amts):.2f}배')
    p = product(cd)
    (OUT / f'ace_{cd}.json').write_text(json.dumps(
        {'url': url, 'fund_cd': cd, 'name': nm, 'dividends': rows, 'product': p},
        ensure_ascii=False, indent=1), encoding='utf-8')
    print(f'  → {OUT / ("ace_" + cd + ".json")}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
