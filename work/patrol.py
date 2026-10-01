# 순돌이 순찰 점검표(2026-10-02) — 사장님: "30분마다 순찰 돌면서 왜 우리가 이야기한 대로 감시하고 지시하지 못했지?"
# 순찰 때 git log만 보던 것을 '규칙을 실제로 지켰나'를 파일로 재는 점검으로 바꾼다. 결과는 표준 출력.
#   py -3.12 work/patrol.py
import os, re, glob, json, datetime, subprocess, sys
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(HERE, 'research')
now = datetime.datetime.now()
bad = []

# 1. 카페 대기 묶음(naverpost pending = 아직 안 나간 것만): 보류 안 걸린 것은 경쟁 조사·편집 통과가 있어야 한다
try:
    out = subprocess.run([sys.executable, os.path.join(HERE, 'naverpost.py'), 'pending', '--raw'], capture_output=True, text=True, encoding='utf-8', timeout=120).stdout
    pend = [json.loads(l) for l in out.splitlines() if l.strip().startswith('{')]
except Exception as e:
    pend = []; bad.append(f'카페 대기 목록을 못 읽음: {e}')
for x in pend:
    pkg = x.get('pkg', ''); d = os.path.dirname(pkg); name = os.path.basename(d)
    if x.get('kind') not in (None, 'cafe') and 'cafe' not in str(x.get('kind')): continue
    if os.path.exists(os.path.join(pkg, 'hold.txt')): continue
    miss = [f for f, ok in [('compare.md', os.path.exists(os.path.join(d, 'compare.md')) or os.path.exists(os.path.join(d, 'compete.md'))),
                            ('편집 통과', os.path.exists(pkg + '.edit.json'))] if not ok]
    if miss: bad.append(f'카페 대기 {name}({x.get("kind")}): {"·".join(miss)} 없음 (보류 안 걸림)')

# 2. 롱폼: 예약 대기 편은 경쟁 비교·심사 기록이 있어야 한다
for meta in glob.glob(os.path.join(R, 'longform', 'ep', '*', 'meta.json')):
    ep = os.path.dirname(meta); n = os.path.basename(ep)
    try: m = json.load(open(meta, encoding='utf-8'))
    except Exception: continue
    pa = m.get('publishAt')
    if not pa: continue
    try:
        if datetime.datetime.fromisoformat(pa).replace(tzinfo=None) < now: continue
    except Exception: pass
    for f in ['compare.md', 'review.md']:
        if not os.path.exists(os.path.join(ep, f)): bad.append(f'롱폼 {n}({pa[:16]}): {f} 없음')

# 3. 쇼츠 대기: compete.md
for d in glob.glob(os.path.join(R, 'cardshorts', '*')):
    if os.path.isdir(d) and not os.path.exists(os.path.join(d, 'compete.md')) and os.path.getmtime(d) > (now - datetime.timedelta(days=2)).timestamp():
        bad.append(f'쇼츠 {os.path.basename(d)}: compete.md 없음')

# 4. 영상 속 카페 약속
for s in glob.glob(os.path.join(R, 'longform', 'ep', '*', 'script.md')):
    t = open(s, encoding='utf-8').read()
    if re.search(r'카페에\s*올려', t):
        n = os.path.basename(os.path.dirname(s))
        pr = os.path.join(R, 'longform', 'loop', 'promises.md')
        if not (os.path.exists(pr) and re.search(rf'\b{re.escape(n)}\b.*(cafe\.naver\.com|firemap/\d+)', open(pr, encoding='utf-8').read())):
            bad.append(f'약속: {n} 대본 "카페에 올려" → promises.md에 글 주소 없음')

# 5. today.md 크기(토큰)
td = os.path.join(R, 'meeting', 'today.md')
if os.path.exists(td):
    lines = open(td, encoding='utf-8').read().count('\n')
    if lines > 200: bad.append(f'today.md {lines}줄 — 150줄 넘음(스프린트가 archive로 옮겨야)')

# 6. 최근 2시간 커밋 수(회사가 도는가)
try:
    c = subprocess.run(['git', '-C', os.path.dirname(HERE), 'log', '--since=2 hours ago', '--oneline'], capture_output=True, text=True, encoding='utf-8').stdout.count('\n')
except Exception: c = -1
print(f'순찰 {now:%m/%d %H:%M} · 최근 2시간 커밋 {c} · 규칙 위반 {len(bad)}')
for b in bad: print(' -', b)
