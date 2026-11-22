"""카페 유입 경로 소급 + 통계 화면이 부르는 API 목록 (firemap-report 2026-11-22, 회의 11/21 21:46 지시 ②③).
읽기만 한다. cafeinflow.fetch와 같은 길(매니저 프로필 → cafe.stat API).
  py -3.12 work/cafeinflow_hist.py 2026-10-20 2026-11-21 out.json
통계 화면 몇 개를 열어 cafe.stat API 주소를 모아 둔다 — 글·게시판별 유입이나 검색어 API가 있는지 보려고.
"""
import datetime, json, sys, time
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright
from naverpost import launch

B = 'https://cafe.stat.naver.com/api/cafe/31789001/'
PAGES = ['type=user', 'type=article', 'type=visit', 'type=search']


def main(start, end, out):
    s0, e0 = datetime.date.fromisoformat(start), datetime.date.fromisoformat(end)
    apis, days = set(), {}
    with sync_playwright() as p:
        ctx = launch(p, True)
        pg = ctx.new_page()
        pg.on('request', lambda r: apis.add(r.url.split('?')[0] + ('?' + r.url.split('?')[1][:160] if '?' in r.url else ''))
              if 'cafe.stat.naver.com/api' in r.url else None)
        for t in PAGES:
            try:
                pg.goto(f'https://cafe.naver.com/ManageNaverStat.nhn?{t}&cafeId=31789001', timeout=40000); time.sleep(5)
                for fr in pg.frames:
                    for txt in ('검색어', '게시글', '유입', '인기'):
                        try:
                            loc = fr.get_by_text(txt, exact=False)
                            if loc.count():
                                loc.first.click(timeout=2000); time.sleep(2)
                        except Exception:
                            pass
            except Exception as e:
                print('화면 못 엶', t, type(e).__name__)
        d = s0
        while d <= e0:
            s = d.isoformat()
            r = ctx.request.get(B + f'user/referer/total?service=CAFE&timeDimension=DATE&startDate={s}',
                                headers={'Referer': 'https://cafe.naver.com/'}, timeout=30000)
            try:
                rows = {x['dataId']: x['data'] for x in r.json()['result']['statData']}['referer']['rows']
                days[s] = dict(zip(rows.get('referrerDomain', []), rows.get('cv', [])))
            except Exception:
                days[s] = None
            d += datetime.timedelta(days=1); time.sleep(0.4)
        ctx.close()
    json.dump({'days': days, 'apis': sorted(apis)}, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('일수', len(days), '· 못 받은 날', sum(v is None for v in days.values()), '· API', len(apis))
    for a in sorted(apis):
        print(' ', a[:220])


if __name__ == '__main__':
    main(*sys.argv[1:4])
