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

# 회차별 정상 소요 시간(분). 이걸 넘으면 멈춘 것으로 본다.
BUDGET = {'write': 45, 'watchdog': 20, 'improve': 40, 'loop': 40, 'report': 50}

def load():
    try: return json.load(open(BEAT, encoding='utf-8'))
    except Exception: return {}

def save(d):
    try: json.dump(d, open(BEAT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    except Exception as e: print('맥박 저장 실패:', str(e)[:60])

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

def stuck(now=None):
    """시작하고 예산 시간을 넘겨도 안 끝난 회차. (이름, 지난 분, 예산) 목록."""
    now = now or time.time()
    out = []
    for task, r in (load() or {}).items():
        if not r.get('start') or r.get('end'): continue
        m = (now - r['start']) / 60
        b = BUDGET.get(task, 60)
        if m > b: out.append((task, round(m), b))
    return sorted(out, key=lambda x: -x[1])

def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'list'
    if cmd in ('start', 'end') and len(sys.argv) > 2:
        (start if cmd == 'start' else end)(sys.argv[2]); return
    d = load(); now = time.time()
    print('회차     시작            끝              걸린시간   상태')
    for task in sorted(set(list(d) + list(BUDGET))):
        r = d.get(task) or {}
        if not r.get('start'):
            print(f'{task:9s} (기록 없음)'); continue
        m = (now - r['start']) / 60
        st = ('끝남' if r.get('end') else
              (f'멈춤? {round(m)}분째 (예산 {BUDGET.get(task, 60)}분)' if m > BUDGET.get(task, 60) else f'도는 중 {round(m)}분'))
        print(f'{task:9s} {r.get("at", ""):15s} {r.get("end_at", "-"):15s} {str(r.get("min", "-")):8s} {st}')
    s = stuck(now)
    if s: print('\n멈춘 것으로 보이는 회차:', ', '.join(f'{t}({m}분)' for t, m, _ in s))

if __name__ == '__main__': main()
