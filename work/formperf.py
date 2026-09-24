# 형식(pkg/form.txt)·축(pkg/axis.txt)별로 실제 성과를 센다 — A(13시) 회차용.
# planner.our_perf()는 형식별 '제목검색 10위 안' 비율만 보고 축·색인·카페 조회를 안 본다.
# 사용: python work/formperf.py
# 재는 것: 블로그 색인율 / 제목검색 10위 안 비율 / 카페 조회 중앙값 (형식별·축별)
# 규칙 - 매칭 안 된 글은 비율에서 빼고 편수만 따로 적는다(측정 안 한 것을 측정한 척하지 않는다).
#        같은 글이 여러 날 기록돼 있으면 가장 최근 기록만 쓴다(한 글을 여러 번 세지 않는다).
import os, re, sys, json, glob, statistics, collections
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
R = os.path.join(HERE, 'research')
NAMES = {'1': '①원문정리', '2': '②계산사례', '3': '③일정', '4': '④통계기록'}

def norm(s):
    return re.sub(r'[^0-9A-Za-z가-힣]', '', str(s or ''))[:24]

def label_index():
    """제목 앞 24자(부호·공백 제거) -> (형식, 축). 잘린 제목도 잡으려고 앞자리로 맞춘다."""
    idx = {}
    for pkg in glob.glob(os.path.join(R, '*', 'pkg')):
        rd = lambda n: (open(os.path.join(pkg, n), encoding='utf-8').read().strip()
                        if os.path.exists(os.path.join(pkg, n)) else '')
        t = rd('title.txt')
        if not t: continue
        idx[norm(t)] = (rd('form.txt') or None, rd('axis.txt') or None)
    return idx

def latest_records(perf):
    """블로그는 가장 최근 기록(색인은 나중에 되므로 최신이 맞다).
    카페는 가장 큰 조회수 - 조회는 시간이 지나며 쌓이므로 '최근 기록'을 쓰면 갓 올린 0회가 잡혀
    전부 0으로 보인다(2026-09-24 첫 실행에서 실제로 그렇게 나왔다).
    올린 지 하루가 안 된 글은 비교가 안 되므로 조회 집계에서 뺀다."""
    blog, cafe = {}, {}
    days = sorted(perf)
    first = {}
    for day in days:
        # recheck = 지난 글을 며칠 뒤 다시 잰 기록(perf.py 2026-09-24 추가). 색인은 나중에 되므로
        # 이 기록이 그 글의 최신 상태다. blog 기록보다 나중에 넣어 덮어쓰게 한다.
        for x in perf[day].get('blog', []) + perf[day].get('recheck', []):
            k = norm(x.get('title'))
            first.setdefault(k, x.get('first_seen') or day)
            blog[k] = (bool(x.get('indexed')), (x.get('self_rank') or 99) <= 10, day, first[k])
        for x in perf[day].get('cafe', []):
            k = norm(x.get('title')); r = x.get('read') or 0
            seen = cafe.get(k)
            cafe[k] = (max(r, seen[0]) if seen else r, seen[1] if seen else day, day)
    # 처음 본 날과 마지막으로 본 날이 같으면 = 하루도 안 지난 글
    # 블로그도 같다 - 올린 날 바로 잰 글은 색인될 시간이 없어 전부 '색인 안 됨'으로 잡힌다
    # (2026-09-24 실측: 그날 발행 12편 색인 0%, 하루 지난 글은 67%).
    return ({k: (v[0], v[1], v[2]) for k, v in blog.items() if v[3] != v[2]},
            {k: (v[0], v[1]) for k, v in cafe.items() if v[1] != v[2]})

def match(key, idx):
    if key in idx: return idx[key]
    for k, v in idx.items():                       # 제목이 잘려 저장된 경우 앞자리로 맞춘다
        if k and (k.startswith(key) or key.startswith(k)) and min(len(k), len(key)) >= 12: return v
    return (None, None)

def table(rows, title, cols):
    if not rows: print('  %s: 측정 대상 0편' % title); return
    print('  ' + title)
    for name, vals in sorted(rows.items(), key=lambda kv: -len(kv[1][cols[0][0]])):
        n = len(vals[cols[0][0]])
        cells = []
        for k, lab, kind in cols:
            a = vals[k]
            if not a: cells.append('%s -' % lab); continue
            cells.append('%s %s' % (lab, ('%d%%' % round(sum(a) / len(a) * 100)) if kind == 'pct'
                                    else ('%.1f' % statistics.median(a))))
        print('    %-10s %2d편  %s' % (name, n, ' · '.join(cells)))

def main():
    perf = json.load(open(os.path.join(HERE, 'perf_log.json'), encoding='utf-8'))
    idx = label_index()
    blog, cafe = latest_records(perf)
    byform = collections.defaultdict(lambda: collections.defaultdict(list))
    byaxis = collections.defaultdict(lambda: collections.defaultdict(list))
    cform = collections.defaultdict(lambda: collections.defaultdict(list))
    caxis = collections.defaultdict(lambda: collections.defaultdict(list))
    miss_b = miss_c = 0
    for key, (indexed, top10, day) in blog.items():
        f, a = match(key, idx)
        if not f and not a: miss_b += 1; continue
        if f: byform[NAMES.get(f, '형식' + f)]['색인'].append(indexed); byform[NAMES.get(f, '형식' + f)]['10위'].append(top10)
        if a: byaxis[a]['색인'].append(indexed); byaxis[a]['10위'].append(top10)
    for key, (read, day) in cafe.items():
        f, a = match(key, idx)
        if not f and not a: miss_c += 1; continue
        if f: cform[NAMES.get(f, '형식' + f)]['조회'].append(read)
        if a: caxis[a]['조회'].append(read)
    print('=== 블로그 — 올린 지 하루 넘은 글만 (%d편 중 형식·축 표기된 %d편)' % (len(blog), len(blog) - miss_b))
    table(byform, '형식별', [('색인', '색인', 'pct'), ('10위', '10위안', 'pct')])
    table(byaxis, '축별', [('색인', '색인', 'pct'), ('10위', '10위안', 'pct')])
    print('=== 카페 — 올린 지 하루 넘은 글만 (%d편 중 형식·축 표기된 %d편)' % (len(cafe), len(cafe) - miss_c))
    table(cform, '형식별', [('조회', '조회중앙', 'med')])
    table(caxis, '축별', [('조회', '조회중앙', 'med')])
    print('표기 없어 뺀 글: 블로그 %d편 · 카페 %d편' % (miss_b, miss_c))
    print('주의: 기록은 %s~%s 며칠치뿐이라 한 형식이 좋다고 단정하지 않는다.' % (min(perf), max(perf)))

main()
