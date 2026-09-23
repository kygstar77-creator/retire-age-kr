# KODEX(삼성자산운용) ETF 분배금 현황을 운용사 공식 페이지에서 그대로 읽어온다.
# 왜 필요한가: 분배금·분배율은 블로그·유튜브마다 값이 다르고 재탕이 많다. 남이 말한 금액을 검증하려면
#   운용사가 스스로 올린 표를 봐야 하는데, 그 표가 자바스크립트로 그려져서 HTTP 요청으로는 안 읽힌다.
# 쓰는 법: py -3.12 work/etfdist.py            (분배율 높은 순 전부)
#          py -3.12 work/etfdist.py 커버드콜   (이름에 그 말이 든 것만)
# 결과: 종목명 · 종목코드 · 지급기준일 · 실지급일 · 주당분배금 · 분배율, 그리고 기준일과 출처 주소.
#       research/etfdist/kodex.json 에도 같이 남긴다.
import sys, re, json, pathlib
from playwright.sync_api import sync_playwright

URL = 'https://www.samsungfund.com/etf/product/distribution.do'
OUT = pathlib.Path(__file__).resolve().parent / 'research' / 'etfdist'

def parse(txt):
    lines = [l.strip() for l in txt.splitlines() if l.strip()]
    asof = ''
    m = re.search(r'기준일\s*:\s*([\d.\s]+)', txt)
    if m:
        asof = m.group(1).strip()
    rows, i = [], 0
    while i < len(lines):
        if lines[i] == '자세히보기' and i >= 1:
            name = lines[i - 1]
            code = ''
            for j in range(i + 1, min(i + 4, len(lines))):
                c = re.match(r'^([0-9A-Z]{6})\s*\|?$', lines[j].replace(' ', ''))
                if c:
                    code = c.group(1); break
            pay = ''
            d = None
            for j in range(i + 1, min(i + 8, len(lines))):
                d = re.search(r'지급기준일\s*([\d.]+)\s*실지급일\s*([\d.]+)', lines[j])
                if d: break
                if lines[j] in ('월말배당', '월중배당', '분기배당', '연배당'):
                    pay = lines[j]
            amt = rate = ''
            for j in range(i + 1, min(i + 12, len(lines))):
                if lines[j] == '분배금' and j + 1 < len(lines):
                    amt = lines[j + 1]
                if lines[j] == '분배율' and j + 1 < len(lines):
                    rate = lines[j + 1]
            if d and amt:
                rows.append({'name': name, 'code': code, 'pay': pay,
                             'base': d.group(1), 'paid': d.group(2),
                             'amount': amt, 'rate': rate})
        i += 1
    return asof, rows

def main():
    want = sys.argv[1] if len(sys.argv) > 1 else ''
    OUT.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch(headless=True)
        pg = b.new_page(locale='ko-KR', user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64)')
        pg.goto(URL, wait_until='domcontentloaded', timeout=60000)
        pg.wait_for_timeout(5000)
        for _ in range(12):
            pg.mouse.wheel(0, 4000); pg.wait_for_timeout(700)
        txt = pg.inner_text('body')
        b.close()
    asof, rows = parse(txt)
    if not rows:
        print('표를 못 읽었다. 출처:', URL); return 2
    if want:
        rows = [r for r in rows if want in r['name']]
    print(f'출처: {URL} · 운용사 기준일 {asof} · {len(rows)}종목')
    for r in rows:
        print(f"{r['rate']:>7} {r['amount']:>7}  {r['pay']:<5} 기준일 {r['base']} 지급 {r['paid']}  {r['name']} ({r['code']})")
    (OUT / 'kodex.json').write_text(json.dumps(
        {'url': URL, 'asof': asof, 'rows': rows}, ensure_ascii=False, indent=1), encoding='utf-8')
    return 0

if __name__ == '__main__':
    sys.exit(main())
