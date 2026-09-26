# 회차 맥박 — 어느 회차가 언제 시작했고 끝났는지 남긴다.
#   py -3.12 work/beat.py start write        # 회차 맨 처음에
#   py -3.12 work/beat.py mark  write 3단계  # 회차 도중, 단계가 바뀔 때마다
#   py -3.12 work/beat.py end   write        # 회차 맨 끝에
#   py -3.12 work/beat.py list               # 지금 상태
#
# 사장님 2026-09-24: "에이전트들 각각 이름 붙여서 역할 정의 잘하고,
#                    니가 일 제대로 하는지 알아서 자가발전되고 있는지 감시해"
#
# 왜 필요한가: 감시기 회차 하나가 새벽 3시 52분에 시작해 16시간 23분 동안 안 끝났다.
# 예약은 앞 회차가 끝나야 다음을 돌리므로 그동안 감시기가 한 번도 안 돌았고,
# 원고 재고를 채우는 유일한 장치가 멈춰 있었다. 로그인이 만료된 것도, 발행이 두 시간 빵꾸 난 것도
# 아무도 못 알렸다. 사장님이 "재고가 왜 0이냐"고 물어서야 찾았다.
#
# 회차 자신은 자기가 멈춘 걸 알릴 수 없다. 그래서 밖에서 맥박을 본다.
import sys, os, json, time
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
BEAT = os.path.join(HERE, 'heartbeat.json')
NL = chr(10)

# 회차별 정상 소요 시간(분). 이걸 넘으면 멈춘 것으로 본다.
BUDGET = {'write': 45, 'watchdog': 20, 'improve': 40, 'loop': 40, 'report': 50}

# 회차별 "여기까지는 안 돌아도 정상"인 간격(시간). 예약(cron)에서 그대로 뽑았다.
# 2026-09-25: 전에는 모든 회차를 6시간 하나로 쟀다. 그래서 하루 한 번 도는 report는
# 무슨 짓을 해도 늘 '맥박 없음'으로 잡혔고, improve도 밤(23:30~13:30)이면 늘 잡혔다.
# 계기판 맨 위 점수 6.0이 회차를 거듭해도 안 내려간 게 이것 때문이다 — 고칠 수 없는 걸 세고 있었다.
#   write    0 0,1,8-23 * * *  → 새벽 2~7시를 쉬니 01시→08시 7시간이 최대
#   watchdog 45 * * * *        → 매시
#   improve  30 13-23/2 * * *  → 23:30 다음이 13:30, 14시간
#   loop     45 1-23/2 * * *   → 두 시간
#   report   30 12 * * *       → 하루 한 번
GAP_OK = {'write': 7, 'watchdog': 1, 'improve': 14, 'loop': 2, 'report': 24}
SLACK = 1.5   # 예약이 늦게 떠도 되도록 얹는 시간

def load():
    try: return json.load(open(BEAT, encoding='utf-8'))
    except Exception: return {}

def save(d):
    try: json.dump(d, open(BEAT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    except Exception as e: print('맥박 저장 실패:', str(e)[:60])

SINCE = '_watch_since'   # 언제부터 맥박을 보고 있었나. 한 번도 안 찍은 회차를 언제부터 셀지 정한다.


def tasks(d=None):
    """회차 기록만. 밑줄로 시작하는 키(메타)는 회차가 아니다."""
    d = d if d is not None else load()
    return {k: v for k, v in (d or {}).items() if not k.startswith('_')}


def watch_since(d=None, save_if_new=True):
    """이 파일이 언제부터 맥박을 보고 있었나(유닉스 시각).

    2026-09-25: 전에는 기록이 없는 회차를 무조건 '예약 간격을 넘겼다'고 셌다.
    그래서 report(하루 한 번)에 맥박 지시가 붙은 뒤 아직 첫 회차가 안 온 동안,
    멀쩡한 회차가 계기판 1순위를 차지했다. 고칠 수 없는 걸 세고 있었던 셈이다.
    이제는 '보기 시작한 뒤로 제 간격이 지났는데도 한 번도 안 왔을 때'만 센다."""
    d = d if d is not None else load()
    t = (d or {}).get(SINCE)
    if t: return t
    t = min([v for r in tasks(d).values()
             for v in (r.get('start'), r.get('end')) if v] or [time.time()])
    if save_if_new:
        d = d or {}; d[SINCE] = t; save(d)
    return t


GONE = '_abandoned'   # 끝을 못 찍고 죽은 회차들. start가 기록을 덮어쓰기 전에 여기로 옮긴다.


def mark(task, label=''):
    """회차가 도중에 "나 아직 살아 있고 지금 이 단계다"를 찍는다.

    2026-09-26: 죽은 회차의 걸린 시간을 '시작~발견'으로 셌다. loop가 11:52에 시작해
    12:05에 죽어도, 13:55에 다음 회차가 발견하면 123분으로 적혔다. 예산이 40분이니
    기록만 보면 늘 '예산을 넘겨 끊겼다'로 보였고, 계기판도 일감표도 그 원인을 가리켰다.
    실제로는 13분짜리 죽음이었다 — 예산과 아무 상관이 없었다. 원인을 못 찾은 이유가 이것이다.
    단계를 찍어 두면 마지막 맥박이 곧 죽은 시각이 되고, 어느 단계에서 죽었는지도 남는다."""
    d = load()
    r = d.get(task) or {}
    if not r.get('start'):
        print(f'{task}: 시작 기록이 없다 — mark 를 건너뛴다'); return
    r['alive'] = time.time(); r['alive_at'] = time.strftime('%Y-%m-%d %H:%M')
    if label: r['stage'] = label[:80]
    d[task] = r; save(d)
    print(f'{task} 단계 {r.get("stage", "-")} ({r["alive_at"]})')


def start(task):
    d = load()
    # 2026-09-26: loop 회차가 11:52에 시작해 12:05에 세션이 죽었다(end 없음).
    # 다음 loop가 start를 부르면 d[task]를 통째로 덮어써서 '안 끝나고 죽었다'는 사실이 사라졌다.
    # 그래서 계기판의 '멈춘 회차'는 늘 1이었다가 다음 회차가 뜨면 0으로 돌아갔고,
    # "loop 회차가 얼마나 자주 죽나"는 아무도 답할 수 없었다. 덮어쓰기 전에 옮겨 적는다.
    prev = (d.get(task) or {})
    if prev.get('start') and not prev.get('end'):
        # 마지막 단계 맥박(mark)이 있으면 그게 죽은 시각이다. 없으면 발견 시각까지가 상한일 뿐이다.
        # 상한을 소요 시간이라고 적으면 전부 '예산 초과'로 보여 원인을 엉뚱한 데서 찾게 된다.
        alive = prev.get('alive')
        gone = d.get(GONE) or []
        gone.append({'task': task, 'at': prev.get('at'),
                     'min': round(((alive or time.time()) - prev['start']) / 60),
                     'how': 'mark' if alive else 'upper',
                     'stage': prev.get('stage') or '',
                     'budget': BUDGET.get(task, 60), 'found': time.strftime('%Y-%m-%d %H:%M')})
        d[GONE] = gone[-60:]
        g = gone[-1]
        print(f'! {task} 지난 회차가 끝을 못 찍고 죽었다 — {prev.get("at")} 시작, '
              + (f'{g["min"]}분' if alive else f'{g["min"]}분 이내(단계 맥박 없음 — 상한)')
              + f' (예산 {g["budget"]}분)'
              + (f' · 마지막 단계: {g["stage"]}' if g['stage'] else ' · 단계 기록 없음'))
    d[task] = {'start': time.time(), 'end': None, 'at': time.strftime('%Y-%m-%d %H:%M')}
    save(d); print(f'{task} 시작 {d[task]["at"]}')


def abandoned(hours=24, now=None):
    """최근 <hours>시간 안에 '끝을 못 찍고 죽은' 것으로 확인된 회차 목록.

    stuck()은 지금 열려 있는 회차만 본다 — 다음 회차가 뜨면 그 기록이 덮어써져 0으로 돌아간다.
    이건 덮어쓰기 전에 옮겨 둔 기록을 읽으므로, 죽었다는 사실이 남는다."""
    now = now or time.time()
    out = []
    for g in (load() or {}).get(GONE) or []:
        try: t = time.mktime(time.strptime(g.get('found', ''), '%Y-%m-%d %H:%M'))
        except Exception: continue
        if (now - t) / 3600 <= hours: out.append(g)
    return out

def end(task):
    d = load()
    r = d.get(task) or {}
    r['end'] = time.time(); r['end_at'] = time.strftime('%Y-%m-%d %H:%M')
    if r.get('start'): r['min'] = round((r['end'] - r['start']) / 60, 1)
    d[task] = r; save(d)
    print(f'{task} 끝 {r.get("end_at")} ({r.get("min", "?")}분)')

def last_any(d=None):
    """어느 회차든 마지막으로 맥박을 찍은 시각. 기계가 켜져 있었는지 보는 데 쓴다."""
    d = d if d is not None else load()
    ts = [v for r in tasks(d).values() for v in (r.get('start'), r.get('end')) if v]
    return max(ts) if ts else None


def beats(d=None):
    """맥박 시각 전부(시작·끝 가리지 않고) 오름차순."""
    d = d if d is not None else load()
    return sorted(v for r in tasks(d).values()
                  for v in (r.get('start'), r.get('end')) if v)


def cut_off(task, now=None, d=None):
    """열린 회차가 '멈춘' 게 아니라 기계가 꺼져/잠자서 끊긴 것인가.

    2026-09-25 01:16 회차에서 처음 걸렸다. write가 21:02에 시작해 260분째 안 끝난 것으로
    보였지만 도는 중이 아니었다 — 21:13 뒤로 네 시간 동안 어떤 회차도 맥박을 못 찍었고
    (기계가 잠들었다), 밀린 예약 넷이 01:16에 한꺼번에 떴다.
    세션을 끊으러 갈 일이 아니라 "그 시간에 발행이 통째로 빠졌다"고 적어 둘 일이다.

    도는 중이어야 할 구간(시작~예산) 바로 뒤에 아무 회차도 안 뛴 구멍이 있으면 끊긴 것으로 본다.
    구멍 길이(시간)를 돌려준다. 끊긴 게 아니면 0.
    """
    now = now or time.time()
    d = d if d is not None else load()
    r = tasks(d).get(task) or {}
    st = r.get('start')
    if not st or r.get('end'): return 0.0
    ts = beats(d)
    win = st + BUDGET.get(task, 60) * 60          # 여기까지는 돌고 있는 게 정상
    alive = max([t for t in ts if t <= win] or [st])   # 그 안에 마지막으로 뛴 맥박
    nxt = min([t for t in ts if t > alive] or [now])   # 그다음 맥박
    hole = (nxt - alive) / 3600
    return round(hole, 1) if hole > min(GAP_OK.values()) + SLACK else 0.0


def stuck(now=None):
    """시작하고 예산 시간을 넘겨도 안 끝난 회차. (이름, 지난 분, 예산) 목록.

    기계가 자고 있던 구간은 뺀다. 그때는 그 회차가 문 게 아니라 아무도 안 돈 것이다."""
    now = now or time.time()
    d = load() or {}
    out = []
    for task, r in tasks(d).items():
        if not r.get('start') or r.get('end'): continue
        m = (now - r['start']) / 60
        b = BUDGET.get(task, 60)
        if m <= b: continue
        # 돌아야 할 구간 뒤에 맥박 구멍이 있으면 기계가 꺼진 것이지 이 회차가 문 게 아니다.
        if cut_off(task, now, d): continue
        out.append((task, round(m), b))
    return sorted(out, key=lambda x: -x[1])


def stale(now=None):
    """자기 예약 간격(GAP_OK)을 넘도록 한 번도 안 시작한 회차. (이름, 지난 시간, 정상간격)."""
    now = now or time.time()
    d = load() or {}
    out = []
    for task, gap in GAP_OK.items():
        st = (tasks(d).get(task) or {}).get('start')
        if not st:
            # 아직 한 번도 안 찍은 회차. 보기 시작한 지 제 간격도 안 지났으면 멀쩡한 것이다.
            if (now - watch_since(d)) / 3600 > gap + SLACK:
                out.append((task, None, gap))
            continue
        h = (now - st) / 3600
        if h > gap + SLACK: out.append((task, round(h, 1), gap))
    return sorted(out, key=lambda x: -(x[1] if x[1] is not None else 9e9))

def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'list'
    if cmd in ('start', 'end') and len(sys.argv) > 2:
        (start if cmd == 'start' else end)(sys.argv[2]); return
    if cmd == 'mark' and len(sys.argv) > 2:
        mark(sys.argv[2], ' '.join(sys.argv[3:])); return
    d = load(); now = time.time()
    print('회차     시작            끝              걸린시간   상태')
    for task in sorted(set(list(tasks(d)) + list(BUDGET))):
        r = d.get(task) or {}
        if not r.get('start'):
            print(f'{task:9s} (기록 없음)'); continue
        m = (now - r['start']) / 60
        if r.get('end'): st = '끝남'
        elif m <= BUDGET.get(task, 60): st = f'도는 중 {round(m)}분'
        elif cut_off(task, now, d): st = f'끊김 ({round(m)}분 전 시작, 기계 꺼짐)'
        else: st = f'멈춤? {round(m)}분째 (예산 {BUDGET.get(task, 60)}분)'
        if not r.get('end') and r.get('stage'): st += f' · 단계 {r["stage"]}'
        print(f'{task:9s} {r.get("at", ""):15s} {r.get("end_at", "-"):15s} {str(r.get("min", "-")):8s} {st}')
    s = stuck(now)
    if s: print('\n멈춘 것으로 보이는 회차:', ', '.join(f'{t}({m}분)' for t, m, _ in s))

    for task in sorted(tasks(d)):
        h = cut_off(task, now, d)
        if h:
            print(NL + f'{task}: 멈춘 게 아니라 끊겼다 — {d[task].get("at")} 시작 뒤 '
                       f'{h}시간 동안 어떤 회차도 맥박이 없다(기계가 꺼져 있었다). '
                       f'그 사이 예약은 통째로 빠졌다.')
    ab = abandoned(24, now)
    if ab:
        print(NL + f'끝을 못 찍고 죽은 회차(최근 24시간) {len(ab)}건: ' + ', '.join(
            f'{g["task"]} {g["at"]}('
            + (f'{g["min"]}분' if g.get('how') == 'mark' else f'{g["min"]}분 이내')
            + f'/예산 {g["budget"]}분'
            + (f', {g["stage"]}에서' if g.get('stage') else '') + ')' for g in ab[-5:]))
    sl = stale(now)
    if sl:
        print(NL + '예약 간격을 넘긴 회차: ' + ', '.join(
            f'{t}(' + ('기록 없음' if h is None else f'{h}시간째') + f', 정상 {g}시간)'
            for t, h, g in sl))

if __name__ == '__main__': main()
