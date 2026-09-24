# 회차 맥박 — 어느 회차가 언제 시작했고 끝났는지 남긴다.
#   py -3.12 work/beat.py start write        # 회차 맨 처음에
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


def start(task):
    d = load()
    d[task] = {'start': time.time(), 'end': None, 'at': time.strftime('%Y-%m-%d %H:%M')}
    save(d); print(f'{task} 시작 {d[task]["at"]}')

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
        print(f'{task:9s} {r.get("at", ""):15s} {r.get("end_at", "-"):15s} {str(r.get("min", "-")):8s} {st}')
    s = stuck(now)
    if s: print('\n멈춘 것으로 보이는 회차:', ', '.join(f'{t}({m}분)' for t, m, _ in s))

    for task in sorted(tasks(d)):
        h = cut_off(task, now, d)
        if h:
            print(NL + f'{task}: 멈춘 게 아니라 끊겼다 — {d[task].get("at")} 시작 뒤 '
                       f'{h}시간 동안 어떤 회차도 맥박이 없다(기계가 꺼져 있었다). '
                       f'그 사이 예약은 통째로 빠졌다.')
    sl = stale(now)
    if sl:
        print(NL + '예약 간격을 넘긴 회차: ' + ', '.join(
            f'{t}(' + ('기록 없음' if h is None else f'{h}시간째') + f', 정상 {g}시간)'
            for t, h, g in sl))

if __name__ == '__main__': main()
