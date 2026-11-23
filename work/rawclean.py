# 분석 끝난 원본 자동 정리 (사장님 11/24 "다운받은거 분석 다 하고 다 잘 지우고 있지?")
# - 경쟁 채널 원본(자막 원문 UC*.txt·스토리보드 sb_*.jpg·yt/full·yt/design/<채널>/)은 3일 지나면 지운다.
#   분석 결과는 보고서(.md)·spec.json에 숫자로 남긴다. 원본은 저작물이라 공개 저장소에 넣지 않는다.
# - 우리 렌더 옛판 work/video/out/old_* 폴더는 2일 지나면 지운다(이름이 old_ = 버린 판).
# - git이 추적하는 파일은 건드리지 않는다. 결과는 한 줄로 출력한다.
import os, sys, time, shutil, subprocess, glob
sys.stdout.reconfigure(encoding='utf-8')
W = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(W)
now = time.time()
tracked = set(subprocess.run(['git', '-C', ROOT, 'ls-files', '-z', 'work/research/yt', 'work/video/out'],
                             capture_output=True).stdout.decode('utf-8', 'replace').split('\0'))

def newest(p):
    if os.path.isfile(p): return os.path.getmtime(p)
    m = os.path.getmtime(p)
    for dp, dn, fn in os.walk(p):
        for f in fn:
            try: m = max(m, os.path.getmtime(os.path.join(dp, f)))
            except OSError: pass
    return m

def rel(p): return os.path.relpath(p, ROOT).replace(os.sep, '/')

def has_tracked(p):
    r = rel(p)
    return r in tracked or any(t.startswith(r + '/') for t in tracked)

gone, size, kept = 0, 0, 0
targets = []
yt = os.path.join(W, 'research', 'yt')
targets += [(p, 3) for p in glob.glob(os.path.join(yt, 'UC*.txt')) + glob.glob(os.path.join(yt, 'sb_*.jpg'))]
targets += [(p, 3) for p in [os.path.join(yt, 'full')] if os.path.isdir(p)]
targets += [(p, 3) for p in glob.glob(os.path.join(yt, 'design', '*')) if os.path.isdir(p)]
targets += [(p, 2) for p in glob.glob(os.path.join(W, 'video', 'out', 'old_*')) if os.path.isdir(p)]
for p, days in targets:
    try:
        if now - newest(p) < days * 86400 or has_tracked(p): kept += 1; continue
        if os.path.isdir(p):
            s = sum(os.path.getsize(os.path.join(dp, f)) for dp, dn, fn in os.walk(p) for f in fn)
            shutil.rmtree(p)
        else:
            s = os.path.getsize(p); os.remove(p)
        gone += 1; size += s
    except OSError:
        kept += 1
print(f'rawclean: 지움 {gone}개 {size/1e9:.2f}GB · 남김 {kept}개(기한 안 지남·git 추적)')
