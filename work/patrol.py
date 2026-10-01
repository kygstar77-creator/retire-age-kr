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


# 7. 약속 점검표(research/commitments.json — 사장님과 정한 것마다 증거 파일·기한). 기한 지났는데 증거 없으면 위반.
try:
    C = json.load(open(os.path.join(R, 'commitments.json'), encoding='utf-8'))
except Exception as e:
    C = []; bad.append(f'commitments.json 못 읽음: {e}')
done = 0
for c in C:
    due = datetime.datetime.strptime(c['due'], '%Y-%m-%d %H:%M')
    ok = False
    if c.get('evidence'):
        f = os.path.join(R, c['evidence']); ok = os.path.exists(f)
        if ok and c.get('fresh_hours'): ok = (now.timestamp() - os.path.getmtime(f)) < c['fresh_hours'] * 3600
    elif c.get('evidence_glob'):
        ok = bool(glob.glob(os.path.join(R, c['evidence_glob'])))
    elif c.get('evidence_grep'):
        f, pat = c['evidence_grep']; f = os.path.join(R, f)
        ok = os.path.exists(f) and re.search(pat, open(f, encoding='utf-8', errors='ignore').read()) is not None
    if ok: done += 1
    elif now > due: bad.append(f'약속 기한 넘김: {c["what"]} (기한 {c["due"]}, 담당 {c["owner"]})')
print(f'약속 점검표 {done}/{len(C)} 끝남')


# 8. 발전하고 있나 — 증명 기준 4개(10/15 목표) 지금 값
def last_line(f, pat):
    f = os.path.join(R, f)
    if not os.path.exists(f): return '파일 없음'
    L = [l for l in open(f, encoding='utf-8', errors='ignore').read().splitlines() if re.search(pat, l)]
    return L[-1][:140] if L else '줄 없음'
print('지표 · 방문:', last_line('growth/daily.md', r'^20\d\d-\d\d-\d\d'))
print('지표 · 수익·쿠팡:', last_line('growth/revenue.md', r'^20\d\d-\d\d-\d\d'))
try:
    sys.path.insert(0, HERE); import ytupload
    y = ytupload.service()
    up = y.channels().list(part='contentDetails,statistics', mine=True).execute()['items'][0]
    ids = [i['contentDetails']['videoId'] for i in y.playlistItems().list(part='contentDetails', playlistId=up['contentDetails']['relatedPlaylists']['uploads'], maxResults=15).execute()['items']]
    vs = y.videos().list(part='snippet,statistics,status,contentDetails', id=','.join(ids)).execute()['items']
    pub = [v for v in vs if v['status']['privacyStatus'] == 'public']
    sh = [int(v['statistics'].get('viewCount', 0)) for v in pub if 'PT1M' not in v['contentDetails']['duration'] and re.match(r'PT\d+S$', v['contentDetails']['duration'])]
    print(f"지표 · 유튜브 구독 {up['statistics']['subscriberCount']} · 공개 쇼츠 {len(sh)}편 평균 조회 {sum(sh)//max(1,len(sh))}(목표 460)")
except Exception as e:
    print('지표 · 유튜브 확인 안 됨:', str(e)[:80])

# 6. 최근 2시간 커밋 수(회사가 도는가)
try:
    c = subprocess.run(['git', '-C', os.path.dirname(HERE), 'log', '--since=2 hours ago', '--oneline'], capture_output=True, text=True, encoding='utf-8').stdout.count('\n')
except Exception: c = -1
print(f'순찰 {now:%m/%d %H:%M} · 최근 2시간 커밋 {c} · 규칙 위반 {len(bad)}')
for b in bad: print(' -', b)
