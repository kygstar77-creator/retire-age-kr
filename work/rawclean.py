# 분석·제작 끝난 파일 자동 정리 (사장님 11/18 "이미 올렸으면 파일 지워도 되는거 아니야?",
# 11/24 "다운받은거 분석 다 하고 다 잘 지우고 있지?" · "필요없는 파일, 이미지 등 정리하면서 하고 있지?")
# 지우는 것(모두 git이 추적하지 않는 파일만, 마지막으로 바뀐 뒤 기한이 지난 것만):
#   1) 경쟁 채널 원본 — yt/UC*.txt·sb_*.jpg·yt/full·yt/design/<채널>/ : 3일 (분석 결과는 보고서·spec.json에)
#   2) 우리 렌더 옛판 — video/out/old_* : 2일
#   3) 백업 사본 — *.pre*·*.orig*·*.bak*·*_old* : 7일
#   4) 렌더 완성본·조각 — video/out/*, research/**/*.mp4·*.wav·*.pcm : 10일
#   5) 녹음 폴더 — video/public/audio/<편>/ : 14일
# 지우지 않는 것: git 추적 파일, slots.json에서 앞으로 나갈 칸·남은 비축분 이름이 든 경로,
#   video/public/bg·fonts 같은 렌더 소재, criteria/(기준 근거), 글·코드·보고서.
import os, re, sys, time, json, shutil, subprocess, glob
sys.stdout.reconfigure(encoding='utf-8')
W = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(W)
R = os.path.join(W, 'research')
now = time.time()
DAY = 86400
tracked = set(subprocess.run(['git', '-C', ROOT, 'ls-files', '-z', 'work'],
                             capture_output=True).stdout.decode('utf-8', 'replace').split('\0'))
norm = lambda s: re.sub(r'[^0-9a-z가-힣]', '', s.lower())

# 앞으로 쓸 이름(보호): 오늘 이후 칸 item 첫 낱말 + 소진·철회 안 된 비축분
active = set()
try:
    d = json.load(open(os.path.join(R, 'slots.json'), encoding='utf-8'))
    today = time.strftime('%Y-%m-%d')
    for s in d.get('slots', []):
        if str(s.get('at', '')) >= today:
            w = re.split(r'[\s(（|—]', str(s.get('item', '')).strip())[0]
            if w and not w.startswith('TBD') and w != '빔': active.add(norm(w))
    for lst in (d.get('reserve') or {}).values():
        for r in lst if isinstance(lst, list) else []:
            if not isinstance(r, dict): continue
            st = str(r.get('status', ''))[:40]
            if '소진' not in st and '쓰지 않음' not in st: active.add(norm(str(r.get('item', ''))))
except Exception as e:
    print('rawclean: slots.json 못 읽음 — 아무것도 지우지 않음', e); sys.exit(0)
active = {a for a in active if len(a) >= 2}

def rel(p): return os.path.relpath(p, ROOT).replace(os.sep, '/')
def protected(p):
    n = norm(rel(p))
    return any(a in n for a in active)
def newest(p):
    if os.path.isfile(p): return os.path.getmtime(p)
    m = os.path.getmtime(p)
    for dp, dn, fn in os.walk(p):
        for f in fn:
            try: m = max(m, os.path.getmtime(os.path.join(dp, f)))
            except OSError: pass
    return m
def has_tracked(p):
    r = rel(p)
    return r in tracked or any(t.startswith(r + '/') for t in tracked)

targets = []
yt = os.path.join(R, 'yt')
targets += [(p, 3) for p in glob.glob(os.path.join(yt, 'UC*.txt')) + glob.glob(os.path.join(yt, 'sb_*.jpg'))]
targets += [(p, 3) for p in [os.path.join(yt, 'full')] if os.path.isdir(p)]
targets += [(p, 3) for p in glob.glob(os.path.join(yt, 'design', '*')) if os.path.isdir(p)]
targets += [(p, 2) for p in glob.glob(os.path.join(W, 'video', 'out', 'old_*')) if os.path.isdir(p)]
targets += [(p, 14) for p in glob.glob(os.path.join(W, 'video', 'public', 'audio', '*')) if os.path.isdir(p)]
BACKUP = re.compile(r'\.(pre|orig|bak)\w*$|\.(pre|orig|bak)\w*\.\w+$|_old\d*\.\w+$')
for base in (R, os.path.join(W, 'video', 'out')):
    for dp, dn, fn in os.walk(base):
        d = dp.replace(os.sep, '/')
        if 'node_modules' in d or '/bundle' in d or '/criteria/' in d + '/' or '/video/out/old_' in d: continue
        for f in fn:
            p = os.path.join(dp, f)
            if BACKUP.search(f): targets.append((p, 7))
            elif d.endswith('/video/out') or '/video/out/' in d or re.search(r'\.(mp4|wav|pcm)$', f, re.I):
                targets.append((p, 10))

DRY = '--dry' in sys.argv
if DRY: print('보호 이름:', sorted(active))
gone, size, kept = 0, 0, 0
seen = set()
for p, days in targets:
    if p in seen or not os.path.exists(p): continue
    seen.add(p)
    try:
        if now - newest(p) < days * DAY or has_tracked(p) or protected(p): kept += 1; continue
        if os.path.isdir(p):
            s = sum(os.path.getsize(os.path.join(dp, f)) for dp, dn, fn in os.walk(p) for f in fn)
            if DRY: print('DRY', round(s/1e6), 'MB', rel(p))
            else: shutil.rmtree(p)
        else:
            s = os.path.getsize(p)
            if DRY: print('DRY', round(s/1e6), 'MB', rel(p))
            else: os.remove(p)
        gone += 1; size += s
    except OSError:
        kept += 1
print(('(시험) ' if DRY else '') + f'rawclean: 지움 {gone}개 {size/1e9:.2f}GB · 남김 {kept}개(기한 안 지남·git 추적·앞으로 쓸 칸) · 보호 이름 {len(active)}개')
