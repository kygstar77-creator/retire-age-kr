"""렌더용 Remotion bundle 사본 자동 정리(11/22 사장님 "자동으로 알아서 좀 비우라" — 총무방 실측: cardshorts bundle 사본 88GB).

py -3.12 work/bundleclean.py            # 지운다
py -3.12 work/bundleclean.py --dry      # 무엇을 지울지만 보여 준다

- 대상: work/research 아래 이름이 bundle·bundle2·bundle_v2·bundle_* 인 폴더 중 index.html이 있는 것
  (`npx remotion bundle ... --out-dir=<폴더>`가 만든 사본 — 원본은 work/video/src·public, 렌더 스크립트가
  `[ -f $B/index.html ] || npx remotion bundle`로 다시 만든다).
- 안 지움: ① remotion 렌더(node 프로세스 명령줄에 'remotion')가 하나라도 돌고 있으면 전부 건너뜀
  ② 폴더 안이나 그 편 폴더(부모)에서 2시간 안에 바뀐 파일이 있으면 그 폴더 건너뜀(렌더 직전·직후)
  ③ bundle/public 안에 work/video/public에 없는 파일이 있으면 건너뜀(원본이 따로 없는 것).
- 11/23 사장님 A안: Temp 바로 아래 remotion-webpack-bundle-* 폴더도 기본 대상(같은 조건: 렌더 중이면 전부 건너뜀·2시간 안 바뀐 것 건너뜀). 다른 Temp 파일은 안 건드림.
- 완성본 mp4(work/video/out)·대본·스크립트·compete 자료는 대상이 아니다.
- 기록: work/research/_pc_health.log에 한 줄(git에 안 넣음).
"""
import datetime, os, shutil, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, 'research')
PUBLIC = os.path.join(HERE, 'video', 'public')
RECENT_S = 2 * 3600


def remotion_running():
    try:
        out = subprocess.run(['powershell', '-NoProfile', '-Command',
                              "Get-CimInstance Win32_Process -Filter \"name='node.exe'\" | ForEach-Object { $_.CommandLine }"],
                             capture_output=True, text=True, timeout=60).stdout
    except Exception:
        return True  # 못 재면 지우지 않는다
    return 'remotion' in out.lower()


def newest_mtime(path, depth_limit=None):
    m = os.path.getmtime(path)
    for dp, dn, fn in os.walk(path):
        for f in fn:
            try: m = max(m, os.path.getmtime(os.path.join(dp, f)))
            except OSError: pass
        if depth_limit == 0: break
    return m


def size_mb(path):
    s = 0
    for dp, dn, fn in os.walk(path):
        for f in fn:
            try: s += os.path.getsize(os.path.join(dp, f))
            except OSError: pass
    return s / 1e6


def has_orphan(bdir):
    pub = os.path.join(bdir, 'public')
    if not os.path.isdir(pub): return False
    for dp, dn, fn in os.walk(pub):
        for f in fn:
            rel = os.path.relpath(os.path.join(dp, f), pub)
            if not os.path.exists(os.path.join(PUBLIC, rel)):
                return rel
    return False


def candidates():
    for dp, dn, fn in os.walk(ROOT):
        for d in list(dn):
            if d == 'bundle' or d.startswith('bundle2') or d.startswith('bundle_'):
                p = os.path.join(dp, d)
                if os.path.isfile(os.path.join(p, 'index.html')):
                    yield p
                dn.remove(d)  # 안으로 내려가지 않음


TEMP = os.environ.get('TEMP') or os.path.join(os.path.expanduser('~'), 'AppData', 'Local', 'Temp')


def temp_bundles():
    """11/23 사장님 A안: Temp 바로 아래 remotion-webpack-bundle-* 폴더만(다른 Temp 파일은 안 건드림)."""
    try: names = os.listdir(TEMP)
    except OSError: return
    for n in names:
        p = os.path.join(TEMP, n)
        if n.startswith('remotion-webpack-bundle-') and os.path.isdir(p) and not os.path.islink(p):
            yield p


def main():
    dry = '--dry' in sys.argv
    now = time.time(); free0 = shutil.disk_usage('C:/').free / 1e9
    if remotion_running():
        msg = 'remotion 렌더 중 — 건너뜀'
        print(msg); log(free0, free0, msg); return 0
    done, skip = [], []
    for p in temp_bundles():
        rel = 'Temp/' + os.path.basename(p)
        if now - newest_mtime(p) < RECENT_S:
            skip.append(f'{rel}(2시간 안 바뀜)'); continue
        mb = size_mb(p)
        if not dry: shutil.rmtree(p, ignore_errors=True)
        done.append((rel, mb))
    for p in candidates():
        rel = os.path.relpath(p, HERE)
        parent = os.path.dirname(p)
        if now - newest_mtime(p) < RECENT_S or now - newest_mtime(parent, depth_limit=0) < RECENT_S:
            skip.append(f'{rel}(2시간 안 바뀜)'); continue
        o = has_orphan(p)
        if o:
            skip.append(f'{rel}(원본 없는 파일 {o})'); continue
        mb = size_mb(p)
        if not dry: shutil.rmtree(p, ignore_errors=True)
        done.append((rel, mb))
    free1 = shutil.disk_usage('C:/').free / 1e9
    tot = sum(m for _, m in done) / 1e3
    head = '지울 것' if dry else '지움'
    print(f'{head} {len(done)}개 {tot:.1f}GB · 건너뜀 {len(skip)}개 · C 남음 {free0:.1f}→{free1:.1f}GB')
    for r, m in done: print(f'  - {r} {m/1e3:.1f}GB')
    for s in skip: print(f'  · {s}')
    if not dry:
        log(free0, free1, f'bundleclean {len(done)}개 {tot:.1f}GB 지움, 건너뜀 {len(skip)}')
    return 0


def log(f0, f1, msg):
    try:
        with open(os.path.join(ROOT, '_pc_health.log'), 'a', encoding='utf-8') as f:
            f.write(f'{datetime.datetime.now():%Y-%m-%d %H:%M} | C 남음 {f0:.1f}→{f1:.1f} GB | {msg}\n')
    except OSError:
        pass


if __name__ == '__main__':
    sys.exit(main())
