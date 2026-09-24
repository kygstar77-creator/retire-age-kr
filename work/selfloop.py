# 마스터 루프 — 사장님 2026-09-23 "전부 내가 손 안 대고 자동으로 돌아가고 발전하도록".
#   py -3.12 work/selfloop.py            → 계기판 → 일감 정하기 → 기계로 되는 건 즉시 실행 → 일감표 갱신 → 지난 일감 판정
# 사람이 "무엇을 하라"고 정하지 않는다. 계기판(health.py)의 점수가 정한다.
# 회차 루틴(firemap-write/improve/report/loop)은 시작할 때 work/worklist.md 맨 위 항목을 읽고 그것부터 닫는다.
import sys, os, re, json, time, subprocess
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(HERE, 'research')
WORK = os.path.join(HERE, 'worklist.md'); LOG = os.path.join(HERE, 'selfloop_log.json')
HEALTH = os.path.join(HERE, 'health.json')

def sh(*a, timeout=1800):
    try:
        r = subprocess.run([sys.executable] + list(a), capture_output=True, text=True, encoding='utf-8', errors='ignore', timeout=timeout, cwd=os.path.dirname(HERE))
        return (r.stdout or '') + (r.stderr or '')
    except Exception as e: return 'ERR ' + str(e)[:100]

def load(p, d=None):
    try: return json.load(open(p, encoding='utf-8'))
    except Exception: return d

# 기계로 바로 돌릴 수 있는 것은 루프가 직접 한다(사람·모델 판단이 필요 없는 것만)
AUTO = {
    '경쟁 대비 미해결 차이 수': lambda: sh(os.path.join(HERE, 'loop.py')),
    '올린 숏폼 수': None,          # 대본을 Gemini가 써야 해서 회차 루틴이 한다
    '블로그 오늘 방문': None,
}

def _profile_locked_by_live():
    """브라우저 프로필 잠금을 살아 있는 프로세스가 쥐고 있으면 그 PID, 아니면 None.
    판단 기준은 naverpost 가 쓰는 것과 같은 것을 그대로 빌려 쓴다(두 군데서 다르게 세지 않게)."""
    try:
        sys.path.insert(0, HERE)
        import naverpost
        owner = open(naverpost.LOCK, encoding='utf-8').read().strip()
        return owner if owner and naverpost._alive(owner) else None
    except Exception:
        return None   # 잠금 파일이 없거나 못 읽으면 막을 이유가 없다


def always():
    """점수와 상관없이 매 회차 돌리는 것 — 글 루프는 항상 최신이어야 회차가 규칙을 읽을 수 있다.
    사장님 2026-09-23 '숏폼뿐만이 아니라 블로그랑 카페도 자가발전 하라고'."""
    out = []
    for name, script in (('글 규칙(카페·블로그 성과 → 규칙)', 'textloop.py'),
                         ('제목 분석(네이버 상위 노출 제목 → 규칙)', 'titlestudy.py'),
                         ('발행 감시', 'watchdog.py')):
        # 발행 감시는 브라우저 프로필을 쓴다. 그 프로필은 한 번에 한 회차만 열 수 있어서
        # naverpost.acquire_lock 이 최대 900초를 기다리는데, 여기 timeout 도 900초다.
        # 그래서 발행 회차(firemap-write)가 잠금을 쥐고 있으면 이 줄은 반드시 900초를 버리고
        # ERR(TimeoutExpired)로 끝난다 — 2026-09-25 01:19 실제로 그랬다(PID 802948 이 쥐고 있었다).
        # 기다릴 이유도 없다: 감시는 매시 예약(firemap-watchdog)으로 따로 돌기 때문이다.
        # 주인이 살아 있으면 건너뛴다. 죽은 잠금이면 watchdog 이 스스로 치우므로 그대로 돌린다.
        if script == 'watchdog.py':
            held = _profile_locked_by_live()
            if held:
                out.append(f'{name}: 건너뜀 — 발행 회차가 브라우저를 쓰는 중(PID {held}) · 매시 예약이 따로 돈다')
                continue
        r = sh(os.path.join(HERE, script), timeout=900).strip()
        out.append(f"{name}: " + (r.splitlines()[0][:100] if r else '(출력 없음)'))
    return out

def main():
    t0 = time.time(); log = load(LOG, []) or []
    before = load(HEALTH, {'items': []})
    sh(os.path.join(HERE, 'health.py'), timeout=1200)          # 지금 상태 재측정
    h = load(HEALTH, {'items': []}); items = h.get('items', [])
    if not items: print('계기판을 못 읽음'); return

    # 지난 회차가 고르라고 한 항목이 실제로 좋아졌는지
    verdict = []
    if log:
        prevtop = {i['name']: i['score'] for i in log[-1].get('picked', [])}
        now = {i['name']: i['score'] for i in items}
        for name, ps in prevtop.items():
            ns = now.get(name)
            if ns is None: continue
            verdict.append(f"{name} {ps} → {ns} " + ('↓해결중' if ns < ps - 1e-9 else ('=변화없음' if abs(ns - ps) < 1e-9 else '↑나빠짐')))

    # 일감은 '루틴이 닫을 수 있는 것'만 고른다. 사장님만 움직일 수 있는 항목(owner='사람')은
    # 점수가 높아도 회차가 못 닫아 매번 1순위를 차지했다 — 아래 별도 칸으로 내리고 보고가 챙긴다.
    todo = [i for i in items if i['score'] > 0 and i.get('owner', '루틴') != '사람']
    waiting = [i for i in items if i['score'] > 0 and i.get('owner') == '사람']
    picked = todo[:5]

    # 기계로 되는 건 지금 돌린다
    ran = always()
    for p in picked:
        fn = AUTO.get(p['name'])
        if fn:
            out = fn(); ran.append(f"{p['name']}: {out.strip().splitlines()[-1][:90] if out.strip() else '(출력 없음)'}")
    if ran:
        sh(os.path.join(HERE, 'health.py'), timeout=1200); h = load(HEALTH, h); items = h.get('items', [])
        todo = [i for i in items if i['score'] > 0 and i.get('owner', '루틴') != '사람']
        waiting = [i for i in items if i['score'] > 0 and i.get('owner') == '사람']
        picked = todo[:5]

    # 일감표 — 다음 회차 루틴이 이걸 맨 먼저 읽는다
    lines = [f'# 일감표 (selfloop {time.strftime("%Y-%m-%d %H:%M")} 자동 생성 — 사람이 고치지 않는다)', '',
             '회차 루틴은 시작할 때 이 파일 맨 위 항목부터 닫는다. 닫았으면 그 줄에 `완료 <날짜시각> <무엇을 했는지>`를 붙인다.',
             '못 닫았으면 `막힘 <이유>`를 붙인다. 세 회차 연속 막히면 tools-wanted.md에 "사람이 봐야 함"으로 올린다.', '']
    for i, p in enumerate(picked, 1):
        lines.append(f"{i}. **[{p['area']}] {p['name']}** — 지금 {p['value']} / 목표 {p['target']} (점수 {p['score']})")
        lines.append(f"   - 어떻게: {p['how']}")
    if waiting:
        lines += ['', '## 사장님만 할 수 있는 것 (루틴은 못 닫는다 — 12:30 보고가 챙긴다)',
                  *[f"- [{w['area']}] {w['name']} — 지금 {w['value']} / 목표 {w['target']} · {w['how']}" for w in waiting]]
    lines += ['', '## 지난 회차 판정', *([f'- {v}' for v in verdict] or ['- (첫 회차)']),
              '', '## 기계로 이미 돌린 것', *([f'- {r}' for r in ran] or ['- 없음']),
              '', '## 전체 계기판', '| 점수 | 영역 | 항목 | 지금 | 목표 |', '|---|---|---|---|---|',
              *[f"| {i['score']} | {i['area']} | {i['name']} | {i['value']} | {i['target']} |" for i in items]]
    open(WORK, 'w', encoding='utf-8').write('\n'.join(lines))

    rec = {'at': time.strftime('%Y-%m-%d %H:%M'), 'sec': int(time.time() - t0), 'picked': picked, 'ran': ran, 'verdict': verdict,
           'total_score': round(sum(i['score'] for i in items), 2)}
    log.append(rec); json.dump(log[-300:], open(LOG, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f"[마스터 루프] {rec['sec']}초 · 전체 부족분 점수 {rec['total_score']}")
    for p in picked: print(f"  → [{p['area']}] {p['name']} {p['value']}/{p['target']} (점수 {p['score']})")
    for w in waiting: print(f"  (사장님) [{w['area']}] {w['name']} {w['value']}/{w['target']}")
    for v in verdict: print('  판정:', v)
    for r in ran: print('  실행:', r)
    print('  일감표:', WORK)

if __name__ == '__main__': main()
