"""렌더 중 디스크 감시(회의 11/2 21:43 — 10/18 디스크 7MB 사고 재발 방지).

py -3.12 work/renderguard.py <ep폴더> [--min-gb 3] [lfrender render 뒤 인자...]
- lfrender.py render <ep>를 띄우고 20초마다 C: 남은 양을 잰다.
- 남은 양이 --min-gb(기본 3GB, 회의가 정한 임시 안전선) 아래로 내려가면 렌더 프로세스 트리를 멈춘다.
- 끝나면 시작 남은 양·최저 남은 양·최대 사용량(GB)을 <ep>/renderguard.log에 한 줄 남긴다(registry에 적을 값).
"""
import datetime, os, shutil, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))


def free_gb(path='C:/'):
    return shutil.disk_usage(path).free / 1e9


def main():
    a = sys.argv[1:]
    if not a: print(__doc__); return 2
    ep = os.path.abspath(a[0]); rest = a[1:]
    min_gb = 3.0
    if '--min-gb' in rest:
        i = rest.index('--min-gb'); min_gb = float(rest[i + 1]); rest = rest[:i] + rest[i + 2:]
    start = free_gb(); low = start
    t0 = datetime.datetime.now()
    print(f'시작 남은 양 {start:.1f}GB · 멈춤선 {min_gb:g}GB', flush=True)
    if start < min_gb:
        print('시작부터 멈춤선 아래 — 렌더하지 않는다'); return 3
    p = subprocess.Popen([sys.executable, os.path.join(HERE, 'lfrender.py'), 'render', ep, *rest])
    stopped = False
    while p.poll() is None:
        time.sleep(20)
        f = free_gb(); low = min(low, f)
        if f < min_gb:
            print(f'남은 양 {f:.2f}GB < {min_gb:g}GB — 렌더 멈춤', flush=True)
            subprocess.call(['taskkill', '/T', '/F', '/PID', str(p.pid)])
            stopped = True; break
    rc = p.wait()
    line = (f"{t0:%Y-%m-%d %H:%M}~{datetime.datetime.now():%H:%M} rc={rc} 멈춤={'예' if stopped else '아니오'} "
            f"시작 {start:.1f}GB 최저 {low:.1f}GB 최대 사용 {start - low:.1f}GB 멈춤선 {min_gb:g}GB")
    print(line)
    with open(os.path.join(ep, 'renderguard.log'), 'a', encoding='utf-8') as fh: fh.write(line + '\n')
    return 4 if stopped else rc


if __name__ == '__main__':
    sys.exit(main())
