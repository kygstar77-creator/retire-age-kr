# 검색어 순위 추적 — 사람들이 실제로 치는 말로 우리가 몇 위인지 날마다 잰다.
#   py -3.12 work/rankwatch.py              → 추적 목록 전부
#   py -3.12 work/rankwatch.py "국채금리"    → 한 건만
#
# 사장님 2026-09-24: "니가 사람들이 클릭하고 싶고 조회할 만한 글을 못 쓰니까
#                    오늘 조회수가 낮은 거 아니야? 노출이 안 돼서 그런가?"
#
# 재 보니 팩트였다. 제목을 통째로 검색하면 1위인데(그 문장을 치는 사람은 없다),
# 사람이 실제로 치는 말로는 전부 30위 밖이었다 —
#   국채금리 13만 회 검색 / 30위 밖 · 재산세 계산기 30위 밖 · DSR 계산기 30위 밖 · 전세가율 30위 밖.
# 색인은 80% 되고 있으니 '안 걸리는' 게 아니라 '걸려도 뒤에 있는' 것이다.
#
# 왜 뒤에 있는지는 두 갈래다 — 제목에 검색어가 없어서인지, 블로그 지수가 낮아서인지.
# 한 번 재서는 못 가른다. **날마다 재서 추세를 봐야** 갈린다. 그래서 이 도구를 만든다.
# 제목에 검색어를 앞세운 글을 낸 뒤 그 키워드 순위가 오르면 제목 탓, 안 오르면 지수 탓이다.
import sys, os, re, json, time
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(HERE, 'research')
sys.path.insert(0, HERE)
import perf
LOG = os.path.join(HERE, 'rank_log.json')
OUT = os.path.join(R, 'rankwatch.md')
BLOG = 'kygstar7777'

# 우리가 실제로 글을 쓰는 주제 중, 사람이 치는 말. demand.py로 검색량을 확인한 것만 넣는다.
WATCH = ['국채금리', '실거래가', '재산세 계산기', 'DSR 계산기', '전세가율', '배당락',
         '오피스텔 수익률', '아파트 실거래가', '근로장려금', '건강보험료율', '코픽스',
         '연금소득세', '퇴직연금', '배당주 추천', '월배당 ETF', '순자산 상위']

def load(p, d):
    try: return json.load(open(p, encoding='utf-8'))
    except Exception: return d

def main():
    kws = sys.argv[1:] or WATCH
    log = load(LOG, {})
    day = time.strftime('%Y-%m-%d')
    today = log.setdefault(day, {})
    for k in kws:
        if k in today: continue
        r = perf.search_rank(k, BLOG, 'blog')
        today[k] = r                      # None이면 30위 밖
        print(f'  {(str(r) + "위") if r else "30위 밖":>8}  {k}')
        time.sleep(0.8)
    json.dump(log, open(LOG, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)

    days = sorted(log)
    lines = ['# 검색어 순위 (rankwatch — 날마다 잰다)', '',
             f'측정 {time.strftime("%Y-%m-%d %H:%M")} · 추적 {len(kws)}개 · 기록 {len(days)}일치', '',
             '**제목을 통째로 검색하면 1위여도 뜻이 없다.** 그 문장을 치는 사람은 없다.',
             '사람이 실제로 치는 말로 몇 위인지가 유입을 정한다.', '',
             '| 검색어 | ' + ' | '.join(days[-5:]) + ' |',
             '|---' * (len(days[-5:]) + 1) + '|']
    inside = 0
    for k in kws:
        cells = []
        for d in days[-5:]:
            v = log.get(d, {}).get(k, '—')
            cells.append('—' if v == '—' else (f'{v}위' if v else '30위 밖'))
        if log.get(days[-1], {}).get(k): inside += 1
        lines.append(f'| {k} | ' + ' | '.join(cells) + ' |')
    lines += ['', f'30위 안에 든 검색어: {inside}/{len(kws)}개', '',
              '## 이 표를 어떻게 읽나', '',
              '- 30위 안이 늘면 제목·본문 고친 것이 먹힌 것이다.',
              '- 아무리 고쳐도 안 늘면 제목이 아니라 블로그 지수 문제다 — 그때는 발행량이 아니라',
              '  체류시간·유입 경로(카페·이웃)를 손봐야 한다.',
              '- 한 번 잰 값으로 단정하지 않는다. 최소 사흘은 봐야 한다.']
    os.makedirs(R, exist_ok=True); open(OUT, 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
    print(f'\n30위 안 {inside}/{len(kws)}개 · 저장 {OUT}')

if __name__ == '__main__': main()
