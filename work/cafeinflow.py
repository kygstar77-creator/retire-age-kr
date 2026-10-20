"""카페 하루 유입 경로 줄 (firemap-report, 2026-10-20 회의 O3).
어제까지 8일치 '유입 경로'를 카페 관리 통계에서 읽어 하루 한 줄로 찍는다:
총 유입 · 홈판 · 카페검색 · 통합검색 비중. 어제 홈판이 앞 7일 평균보다 50% 넘게 줄면 '경보' 줄.
읽기만 한다(growthfunnel.py cafe와 같은 길: 매니저 프로필 launch → cafe.stat API).
발행 회차가 브라우저를 쓰는 중이면 같은 프로필을 못 열므로 '확인 안 함'으로 끝낸다.
  py -3.12 work/cafeinflow.py            # 찍기
  py -3.12 work/cafeinflow.py --append   # growth/revenue.md 맨 아래에 어제 줄 더하기
"""
import datetime, sys, time

B = 'https://cafe.stat.naver.com/api/cafe/31789001/'
HOME = '네이버 메인_모바일_홈판'
UNI = ('네이버 통합검색_모바일', '네이버 통합검색_PC')


def fetch(days=8):
    from playwright.sync_api import sync_playwright
    from naverpost import launch
    res = {}
    with sync_playwright() as p:
        ctx = launch(p, True)
        pg = ctx.new_page(); pg.goto('https://cafe.naver.com/ManageNaverStat.nhn?type=user&cafeId=31789001', timeout=40000); time.sleep(4)
        d = datetime.date.today() - datetime.timedelta(days=days)
        while d < datetime.date.today():
            s = d.isoformat()
            r = ctx.request.get(B + f'user/referer/total?service=CAFE&timeDimension=DATE&startDate={s}',
                                headers={'Referer': 'https://cafe.naver.com/'}, timeout=30000)
            try:
                rows = {x['dataId']: x['data'] for x in r.json()['result']['statData']}['referer']['rows']
                res[s] = dict(zip(rows.get('referrerDomain', []), rows.get('cv', [])))
            except Exception:
                res[s] = None
            d += datetime.timedelta(days=1); time.sleep(0.4)
        ctx.close()
    return res


def line(day, ref):
    tot = sum(ref.values()) or 1
    home = ref.get(HOME, 0)
    cafes = sum(c for a, c in ref.items() if '카페검색' in a or '카페 검색' in a)
    uni = sum(ref.get(a, 0) for a in UNI)
    return home, f'{day} 카페 유입 {sum(ref.values())}회 · 홈판 {home}({home / tot * 100:.0f}%) · 카페검색 {cafes}({cafes / tot * 100:.0f}%) · 통합검색 {uni}({uni / tot * 100:.1f}%)'


def main():
    try:
        res = fetch()
    except Exception as e:
        print(f'확인 안 함 — 카페 통계를 못 엶({type(e).__name__}: {str(e)[:120]}). 발행 회차가 브라우저를 쓰는 중이면 다음 회차에 다시.')
        return 1
    out, homes = [], []
    for day in sorted(res):
        if res[day] is None:
            out.append(f'{day} 확인 안 함(통계 응답 없음)'); continue
        h, s = line(day, res[day]); homes.append((day, h)); out.append(s)
    for s in out: print(s)
    if len(homes) >= 2:
        (yd, yh), prev = homes[-1], [h for _, h in homes[:-1]][-7:]
        avg = sum(prev) / len(prev)
        msg = (f'경보: {yd} 홈판 {yh}회 = 앞 {len(prev)}일 평균 {avg:.0f}회보다 {(1 - yh / avg) * 100:.0f}% 적음(기준 50%)'
               if avg and yh < avg * 0.5 else f'{yd} 홈판 {yh}회 · 앞 {len(prev)}일 평균 {avg:.0f}회 (경보 아님)')
        print(msg); out.append(msg)
    if '--append' in sys.argv and homes:
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        with open('work/research/growth/revenue.md', 'a', encoding='utf-8') as f:
            f.write(f'{now} · {[s for s in out if s.startswith(homes[-1][0])][0]} · {out[-1]} (cafeinflow.py)\n')
    return 0


if __name__ == '__main__':
    sys.exit(main())
