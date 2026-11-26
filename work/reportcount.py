# 보고 세기 — firemap-report 회차가 손으로 세던 판단 재료를 코드가 센다.
#   사장님 2026-11-26 "품질 그대로, 읽는 양만 줄이기".
#   py -3.12 work/reportcount.py      (perf.py 12 · visitors.py 뒤에 돌린다 — 그 두 기록을 읽는다)
#
# 세는 것(기준은 SKILL·기존 코드 그대로):
#   1b 부족분: runs_today.json 서로 다른 주소 수(report.py와 같은 셈) · 하루 상한 naverpost.DAY_CAP · 정지 스위치 STOP_<종류> ·
#      오늘 지난 카페 칸(slots.json, 칸+50분 = watchdog.SLOT_LATE_MIN E-21) 중 장부에 발행 없는 칸 · 지금 올릴 수 있는(막힘 없는) 대기 묶음.
#   2 브레이크: perf_log 최신 mature 색인율 < 50% · visitors_log 3일 연속 감소 · 잰 시각(at)이 어제와 다른지.
#   2-원래 카페 멤버공개: 카페 API openArticle False 글 번호(최근 50편).
#   결재함: approvals.md '결재 대기' 줄 수.   8(d): 최근 7일 발행 묶음의 form.txt·axis.txt 분포.
# rules.json 근거 없음·미확인은 audit.py(6단계)가 이미 센다 — 여기서 다시 세지 않는다.
# 읽기·세기만 한다: 발행·공개 전환·메시지 보내기 없음. 로그인(naverpost.py check)·실물 검증(verify today)은 브라우저라 회차가 돌린다.
# 마지막 줄: 'STATUS: OK' 또는 'STATUS: 이상 — <무엇>'.
import sys, os, re, json, time, glob, subprocess, collections, datetime as dt, urllib.request
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(HERE, 'research')
sys.path.insert(0, HERE)
import naverpost as N, watchdog as W

BRAKE_RATE = 0.5    # SKILL 2: mature 색인율 50% 아래
BRAKE_DAYS = 3      # SKILL 2: 방문 3일 연속 감소


def load(p, d=None):
    try: return json.load(open(p, encoding='utf-8'))
    except Exception: return d


def falling(xs, n=BRAKE_DAYS):
    """끝 n번이 잇달아 줄었나(n+1개 값)."""
    xs = [x for x in xs if x is not None]
    return len(xs) > n and all(xs[-i] < xs[-i - 1] for i in range(1, n + 1))


def main():
    now = dt.datetime.now(); today = now.strftime('%Y-%m-%d')
    bad, out = [], []
    stop = {k: N.stop_flag(k) for k in ('blog', 'cafe')}

    # 1b 발행 편수 · 지난 칸 · 올릴 수 있는 묶음
    rt = load(os.path.join(HERE, 'runs_today.json'), {}) or {}
    runs = rt.get('runs', []) if rt.get('date') == today else []
    n = {k: len({(r.get(k) or {}).get('url') for r in runs if (r.get(k) or {}).get('url')}) for k in ('blog', 'cafe')}
    past = [x for x in W._slots().get('slots', []) if x.get('kind') == 'cafe' and not x.get('skip') and x.get('at', '')[:10] == today
            and dt.datetime.strptime(x['at'], '%Y-%m-%d %H:%M') + dt.timedelta(minutes=W.SLOT_LATE_MIN) <= now]
    empty = [x for x in past if not x.get('published')]
    try:
        pend = [json.loads(l) for l in subprocess.run([sys.executable, os.path.join(HERE, 'naverpost.py'), 'pending'],
                capture_output=True, text=True, encoding='utf-8', errors='ignore', timeout=300,
                env={**os.environ, 'PYTHONIOENCODING': 'utf-8'}).stdout.splitlines() if l.startswith('{')]
    except Exception:
        pend = None; bad.append('naverpost.py pending 실패')
    cnt = collections.defaultdict(collections.Counter)
    ready = collections.defaultdict(list)
    for x in pend or []:
        b = str(x.get('block') or '')
        c = 'ok' if not b else 'wait' if N.is_stock_block(b) else 'held'
        cnt[x['kind']][c] += 1
        if c == 'ok': ready[x['kind']].append(os.path.basename(os.path.dirname(x['pkg'])))
    if rt.get('date') != today: out.append(f"! runs_today.json 날짜 {rt.get('date')} — 오늘 기록 아님(오늘 0편으로 셈)")
    for k, nm in (('cafe', '카페'), ('blog', '블로그')):
        c = cnt[k]
        line = f"{nm} 오늘 {n[k]}/{N.DAY_CAP.get(k, '?')}(하루 상한)"
        if stop[k]: line += f' · 정지 중(STOP_{k})'
        if k == 'cafe': line += f" · 지난 칸 {len(past)}개 중 장부 발행 없음 {len(empty)}" + (f" ({', '.join(x['at'][11:] + ' ' + str(x.get('item'))[:16] for x in empty)})" if empty else '')
        line += f" · 대기 지금 올릴 수 있음 {c['ok']}" + (f"({', '.join(ready[k])})" if ready[k] else '') + f" · 시각 대기 {c['wait']} · 보류 {c['held']}"
        out.append(line)
        short = (len(empty) if k == 'cafe' else max(0, N.DAY_CAP.get(k, 0) - n[k]))
        if not stop[k] and short and c['ok']:
            bad.append(f'1b 보충 후보 {nm} 부족 {short}·올릴 묶음 {c["ok"]}')

    # 2 브레이크
    perf = load(os.path.join(HERE, 'perf_log.json'), {}) or {}
    pd = sorted(perf)
    if not pd: out.append('! perf_log 비었음'); bad.append('perf_log 없음')
    else:
        last = perf[pd[-1]]; mt = last.get('mature') or {}
        prev_at = perf[pd[-2]].get('at') if len(pd) > 1 else None
        rate = mt.get('rate')
        hit = rate is not None and rate < BRAKE_RATE
        line = (f"색인 mature {mt.get('indexed')}/{mt.get('n')}({'—' if rate is None else str(round(rate * 100)) + '%'}) 기준 {int(BRAKE_RATE * 100)}%"
                + (' 아래' if hit else '') + f" · {mt.get('basis', '')[:24]} · 잰 시각 {last.get('at')} (전날 {prev_at})")
        if pd[-1] != today: line += ' · ! 오늘 perf.py 12 기록 아님'; bad.append('perf_log 오늘 기록 없음(perf.py 12 먼저)')
        out.append(line)
    vis = load(os.path.join(HERE, 'visitors_log.json'), {}) or {}
    vd = sorted(vis)[-(BRAKE_DAYS + 1):]
    vt = [vis[d].get('today') for d in vd]
    tot = [vis[d].get('total') for d in sorted(vis)[-(BRAKE_DAYS + 2):]]
    inc = [b - a for a, b in zip(tot, tot[1:]) if a is not None and b is not None]
    vfall = falling(vt) or falling(inc)
    out.append(f"방문 오늘값 {' → '.join(f'{d[5:]} {v}' for d, v in zip(vd, vt))} · 전체 하루 증가 {inc} · {BRAKE_DAYS}일 연속 감소 {'예' if vfall else '아님'}"
               + (f" · ! 오늘 visitors.py 기록 아님" if vd and vd[-1] != today else ''))
    if vd and vd[-1] != today: bad.append('visitors_log 오늘 기록 없음(visitors.py 먼저)')
    brake = (pd and hit) or vfall
    if brake and stop['blog']:
        out.append('브레이크 기준 해당 — 단 블로그 정지 중(STOP_blog)이라 줄일 블로그 발행이 없다(11/22·11/24 회차는 이 경우 안 걸었다)')
    elif brake:
        bad.append('브레이크 기준 해당')

    # 카페 멤버공개
    try:
        u = (f'https://apis.naver.com/cafe-web/cafe2/ArticleListV2dot1.json?search.clubid={N.CAFE_ID}'
             '&search.queryType=lastArticle&search.page=1&search.perPage=50')
        arts = json.load(urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0', 'Referer': 'https://cafe.naver.com/'}),
                         timeout=20))['message']['result']['articleList']
        closed = [(a['articleId'], a.get('writerNickname') == N.CAFE_NICK) for a in arts if not a.get('openArticle')]
        out.append(f'카페 멤버공개(최근 {len(arts)}편) {len(closed)}' + (': ' + ', '.join(f"#{i}{'' if ours else '(회원 글)'}" for i, ours in closed) if closed else ''))
        if closed: bad.append(f'멤버공개 {len(closed)}편(#315 같은 회원 자료는 일부러 멤버공개 — 확인 후 public)')
    except Exception as e:
        out.append(f'카페 멤버공개 확인 실패: {str(e)[:60]}'); bad.append('카페 API 실패')

    # 결재함
    try:
        ap = sum(1 for l in open(os.path.join(R, 'approvals.md'), encoding='utf-8') if '결재 대기' in l)
        out.append(f'결재 대기 줄 {ap}건(approvals.md)')
    except Exception: out.append('approvals.md 못 읽음')

    # 8(d) 최근 7일 형식·축
    cut = time.time() - 7 * 86400
    form, axis = collections.Counter(), collections.Counter()
    for p in glob.glob(os.path.join(R, '*', 'pkg', 'published.txt')):
        if os.path.getmtime(p) < cut: continue
        d = os.path.dirname(p)
        for f, c in (('form.txt', form), ('axis.txt', axis)):
            try: c[open(os.path.join(d, f), encoding='utf-8').readline().strip()[:10] or '(빈칸)'] += 1
            except Exception: c['(없음)'] += 1
    out.append(f"최근 7일 발행 묶음 {sum(form.values())} · 형식 {dict(form.most_common())} · 축 {dict(axis.most_common())}")

    print(f"[보고 세기 {now.strftime('%Y-%m-%d %H:%M')}]")
    for l in out: print('· ' + l)
    print('STATUS: OK' if not bad else 'STATUS: 이상 — ' + ' / '.join(dict.fromkeys(bad)))


if __name__ == '__main__': main()
