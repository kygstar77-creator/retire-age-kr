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

def always():
    """점수와 상관없이 매 회차 돌리는 것 — 글 루프는 항상 최신이어야 회차가 규칙을 읽을 수 있다.
    사장님 2026-09-23 '숏폼뿐만이 아니라 블로그랑 카페도 자가발전 하라고'."""
    out = []
    for name, script in (('글 규칙(카페·블로그 성과 → 규칙)', 'textloop.py'),
                         ('제목 분석(네이버 상위 노출 제목 → 규칙)', 'titlestudy.py'),
                         ('발행 감시', 'watchdog.py')):
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

    todo = [i for i in items if i['score'] > 0]
    picked = todo[:5]

    # 기계로 되는 건 지금 돌린다
    ran = always()
    for p in picked:
        fn = AUTO.get(p['name'])
        if fn:
            out = fn(); ran.append(f"{p['name']}: {out.strip().splitlines()[-1][:90] if out.strip() else '(출력 없음)'}")
    if ran: sh(os.path.join(HERE, 'health.py'), timeout=1200); h = load(HEALTH, h); items = h.get('items', []); todo = [i for i in items if i['score'] > 0]; picked = todo[:5]

    # 일감표 — 다음 회차 루틴이 이걸 맨 먼저 읽는다
    lines = [f'# 일감표 (selfloop {time.strftime("%Y-%m-%d %H:%M")} 자동 생성 — 사람이 고치지 않는다)', '',
             '회차 루틴은 시작할 때 이 파일 맨 위 항목부터 닫는다. 닫았으면 그 줄에 `완료 <날짜시각> <무엇을 했는지>`를 붙인다.',
             '못 닫았으면 `막힘 <이유>`를 붙인다. 세 회차 연속 막히면 tools-wanted.md에 "사람이 봐야 함"으로 올린다.', '']
    for i, p in enumerate(picked, 1):
        lines.append(f"{i}. **[{p['area']}] {p['name']}** — 지금 {p['value']} / 목표 {p['target']} (점수 {p['score']})")
        lines.append(f"   - 어떻게: {p['how']}")
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
    for v in verdict: print('  판정:', v)
    for r in ran: print('  실행:', r)
    print('  일감표:', WORK)

if __name__ == '__main__': main()
