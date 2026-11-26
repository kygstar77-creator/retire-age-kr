"""렌더는 한 번에 하나 (11/26 사장님 지시 — 총무 방 실측: 렌더 2~3개 동시에 빈 메모리 0.5~1GB, 다른 일 53분 멈춤).

품질 설정(해상도·concurrency·관문)은 건드리지 않고 순서만 줄 세운다.

  py -3.12 work/renderlock.py [--wait 분] [--label 이름] -- <렌더 명령 ...>
      예) py -3.12 work/renderlock.py --label cc1미리보기 -- npx remotion render src/motion/preview/entry.ts ...
  코드에서:  from renderlock import render_lock
            with render_lock('H-6 본편', wait_min=120): subprocess.call(...)

- 잠금 파일 work/.render_lock(git 무시). 잡은 프로세스가 죽었거나 4시간 넘은 잠금은 버린다.
- 다른 렌더가 돌면 30초마다 보며 기다린다. --wait(기본 60분) 넘으면 렌더하지 않고 종료코드 75 — 다음 회차에 다시.
- --min-free GB(미리보기에 2.5 권장): 잠금을 잡은 뒤 빈 메모리가 그 아래면 늘 때까지 같은 기한 안에서 기다린다.
  본편(lfrender)은 메모리로 기다리지 않는다 — 공개 기한이 먼저.
"""
import contextlib, ctypes, datetime, json, os, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
LOCK = os.path.join(HERE, '.render_lock')
STALE_H = 4
BUSY = 75


class Busy(RuntimeError):
    pass


def free_mem_gb():
    class M(ctypes.Structure):
        _fields_ = [('l', ctypes.c_ulong), ('load', ctypes.c_ulong)] + [(n, ctypes.c_ulonglong) for n in
                    ('tot', 'avail', 'tp', 'ap', 'tv', 'av', 'ext')]
    m = M(); m.l = ctypes.sizeof(M)
    ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m))
    return m.avail / 1e9


def alive(pid):
    h = ctypes.windll.kernel32.OpenProcess(0x1000, False, int(pid))  # QUERY_LIMITED_INFORMATION
    if not h: return False
    code = ctypes.c_ulong()
    ctypes.windll.kernel32.GetExitCodeProcess(h, ctypes.byref(code))
    ctypes.windll.kernel32.CloseHandle(h)
    return code.value == 259  # STILL_ACTIVE


def holder():
    try:
        d = json.load(open(LOCK, encoding='utf-8'))
    except FileNotFoundError:
        return None
    except (ValueError, OSError):
        d = {}
    old = time.time() - os.path.getmtime(LOCK) > STALE_H * 3600 if os.path.exists(LOCK) else True
    if old or not d.get('pid') or not alive(d['pid']):
        with contextlib.suppress(OSError): os.remove(LOCK)
        return None
    return d


@contextlib.contextmanager
def render_lock(label, wait_min=60, min_free_gb=0):
    end = time.time() + wait_min * 60
    said = False
    while True:
        h = holder()
        if h is None:
            try:
                fd = os.open(LOCK, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                with os.fdopen(fd, 'w', encoding='utf-8') as f:
                    json.dump({'pid': os.getpid(), 'label': label,
                               'at': datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}, f, ensure_ascii=False)
                break
            except FileExistsError:
                continue
        if not said:
            print(f"렌더 줄서기: '{h.get('label')}'({h.get('at')}) 끝나길 기다림 · 상한 {wait_min}분", flush=True); said = True
        if time.time() > end:
            raise Busy(f"{wait_min}분 기다려도 '{h.get('label')}' 렌더가 안 끝남 — 이번엔 렌더하지 않음")
        time.sleep(30)
    try:
        while min_free_gb and free_mem_gb() < min_free_gb:
            if time.time() > end:
                raise Busy(f'빈 메모리 {free_mem_gb():.1f}GB < {min_free_gb}GB가 {wait_min}분 안에 안 풀림 — 이번엔 렌더하지 않음')
            print(f'빈 메모리 {free_mem_gb():.1f}GB < {min_free_gb}GB — 기다림', flush=True)
            time.sleep(30)
        yield
    finally:
        with contextlib.suppress(OSError):
            if json.load(open(LOCK, encoding='utf-8')).get('pid') == os.getpid(): os.remove(LOCK)


def main(a):
    if '--' not in a: print(__doc__); return 2
    i = a.index('--'); opt, cmd = a[:i], a[i + 1:]
    wait = int(opt[opt.index('--wait') + 1]) if '--wait' in opt else 60
    label = opt[opt.index('--label') + 1] if '--label' in opt else ' '.join(cmd)[:60]
    mf = float(opt[opt.index('--min-free') + 1]) if '--min-free' in opt else 0
    try:
        with render_lock(label, wait, mf):
            return subprocess.call(cmd, shell=(os.name == 'nt'))
    except Busy as e:
        print(e); return BUSY


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
