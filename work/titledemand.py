# -*- coding: utf-8 -*-
"""묶음 제목의 검색어 수요를 재서 '아무도 안 치는 말'을 발행 전에 잡는다.

2026-09-25 22시 회차에서 확인한 것: 카페 최근 20편 조회 중앙값이 하루당 0.96 이었다.
색인은 정상이고 제목 검색 순위도 1위인데 조회가 1이었다. 원인은 노출이 아니라 수요였다.
최근 카페 글 8편의 핵심 검색어를 demand.py 로 재 보니 5편이 월 20 이하였다 —
SPYD 배당 15 · 미국 배당 인상 10 · HDV 배당 15 · 커버드콜 분배율 20.
반면 달러예금 4,100 · 미국 단기채 ETF 650 · JEPI JEPQ 350 은 같은 축인데 수요가 있었다.
블로그는 단지·종목을 고를 때 demand.py 로 재는데 카페 제목은 그 검사를 한 번도 안 받았다.

쓰는 법:  py -3.12 work/titledemand.py <pkg>          (묶음 제목에서 후보를 뽑아 잰다)
          py -3.12 work/titledemand.py --kw "검색어" ...  (검색어를 직접 준다)
결과는 pkg/check_demand.txt 에 쓴다. 최고 수요가 MIN_REAL 미만이면 마지막 줄이 '수요 없음'이다.
그 경우 제목의 말을 사람들이 실제로 치는 말로 바꾼다(글 내용을 바꾸라는 뜻이 아니다).
"""
import io, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import demand

MIN_REAL = getattr(demand, 'MIN_REAL', 20)

# 제목에서 검색어가 될 수 없는 말 — 숫자·단위·조사·글투
DROP = set('''그런데 하지만 이라는 라는 인데 있는 없는 하는 되는 받는 주는 드는 오는 가는 왜 뒤 앞 안 밖
때 것 곳 수 중 더 덜 만 원 년 월 일 개 편 곳 배 위 명 실제 이번 최근 지금 오늘 내일 어제
계산 정리 기록 확인 비교 차이 이유 방법 경우 기준 결과 상한 한도 공시 세후 세전'''.split())
HASNUM = re.compile(r'[0-9]')
TICKER = re.compile(r'^[A-Z]{2,5}$')


def cands(title, limit=6):
    """제목을 홀낱말과 이웃한 두 낱말 짝으로 쪼개 검색어 후보를 만든다.

    사람이 치는 말은 대개 낱말 한두 개다. 제목을 통째로 재면 늘 0이 나와 아무것도 못 잡는다.
    숫자가 섞인 낱말(221%·2,059만원·300원짜리가)은 버린다 — 그 글에만 있는 값이라 아무도 안 친다.
    홀낱말을 짝보다 먼저 놓는다. 2026-09-25 첫판은 짝이 자리를 다 차지해 '브로드컴'을 못 쟀다.
    """
    words = [w for w in re.split(r'[^0-9A-Za-z가-힣%]+', title) if w]
    keep = [w for w in words
            if w not in DROP and not HASNUM.search(w) and (len(w) > 1 or TICKER.match(w))]
    out = [w for w in keep if TICKER.match(w) or len(w) >= 3]
    for a, b in zip(keep, keep[1:]):
        out.append(f'{a} {b}')
    seen, uniq = set(), []
    for x in out:
        if x not in seen:
            seen.add(x)
            uniq.append(x)
    return uniq[:limit]


def report(keys):
    v = demand.vols(keys)
    rows = sorted(((v.get(k), k) for k in keys),
                  key=lambda r: (-1 if r[0] is None else r[0]), reverse=True)
    lines = ['# 제목 검색어 수요 (titledemand.py)',
             f'# 기준: 월 검색수 {MIN_REAL} 미만은 사람들이 치는 말이 아니다', '']
    for vol, k in rows:
        lines.append(f'{"못 잼" if vol is None else format(vol, ">9,")}  {k}')
    measured = [vol for vol, _ in rows if isinstance(vol, int)]
    top = max(measured) if measured else None
    lines.append('')
    if top is None:
        lines.append('판정: 못 잼 — 검색수를 재지 못했다. 이 결과로 제목을 바꾸지 않는다.')
    elif top >= MIN_REAL:
        best = next(k for vol, k in rows if vol == top)
        lines.append(f'판정: 수요 있음 — "{best}" 월 {top:,}. 이 말을 제목에 그대로 둔다.')
    else:
        lines.append(f'판정: 수요 없음 — 가장 높은 후보도 월 {top:,}이다. '
                     f'검색 1위를 해도 조회가 한 자리에 머문다. 같은 내용을 사람들이 치는 말로 다시 건다.')
    return '\n'.join(lines) + '\n', (top if top is not None else -1)


def main():
    args = sys.argv[1:]
    if not args:
        sys.exit('묶음 경로나 --kw 검색어를 주세요: py -3.12 work/titledemand.py <pkg>')
    if args[0] == '--kw':
        text, top = report(args[1:])
        sys.stdout.write(text)
        return 0 if top >= MIN_REAL or top < 0 else 1
    pkg = args[0]
    tp = os.path.join(pkg, 'title.txt')
    if not os.path.exists(tp):
        sys.exit(f'title.txt 가 없다: {tp}')
    title = io.open(tp, encoding='utf-8').read().strip()
    keys = cands(title)
    if not keys:
        sys.exit(f'제목에서 검색어 후보를 못 뽑았다: {title}')
    text, top = report(keys)
    text = f'# 묶음: {os.path.basename(os.path.dirname(pkg.rstrip(os.sep)))} · 제목: {title}\n' + text
    io.open(os.path.join(pkg, 'check_demand.txt'), 'w', encoding='utf-8').write(text)
    sys.stdout.write(text)
    return 0 if top >= MIN_REAL or top < 0 else 1


if __name__ == '__main__':
    sys.exit(main())
