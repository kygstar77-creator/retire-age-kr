"""공개 끝난 롱폼의 렌더 재료·중간 렌더 정리 (11/26 사장님 "확인 끝나거나 필요 없어진 건 지워야 하지 않아? 컴퓨터 용량도 생각해야지").

  py -3.12 work/vidclean.py            # 목록만(기본) — 지울 것·남길 것·GB
  py -3.12 work/vidclean.py --apply    # 실제로 지움 (사장님 확인 뒤에만 pc_health.ps1에 --apply로 넣는다)

지우는 것: 공개(meta.json publishAt) 뒤 DAYS일 지난 롱폼의
  - video/public/bg/<편>/      (판 그림·클립 — 렌더 재료)
  - video/public/audio/<편>*/  (녹음 — 렌더 재료)
  - video/out/<편>_*·old_<편>* (중간 렌더·소리만·토막·옛판)
  + 공개 끝난 쇼츠 재료 video/public/bg/<x>s_<이름>/ (DAYS일 지남, 앞으로 칸·비축에 없음)
남기는 것:
  - video/out/<편>.mp4 최종본(유튜브 원본과 같은 것 — 보관용)
  - 앞으로 칸(slots.json 오늘 이후)·남은 비축에 편 이름이 나오는 편 — 쇼츠는 롱폼 재료로 다시 렌더한다(c1clip)
  - 공개 전 편, git 추적 파일, 렌더 중인 편(.render_lock 라벨), bg/_sample·fonts 등 편이 아닌 폴더
공개 영상은 교체하지 않는 규칙(PD)이라 공개 뒤 롱폼 재렌더는 없다 — 남은 쓰임은 쇼츠 자르기뿐이고 그건 보호 목록이 막는다.
"""
import datetime, glob, json, os, re, shutil, subprocess, sys

W = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(W)
V = os.path.join(W, 'video')
R = os.path.join(W, 'research')
DAYS = 3
now = datetime.datetime.now().astimezone()
norm = lambda s: re.sub(r'[^0-9a-z]', '', s.lower())


def size(p):
    if os.path.isfile(p): return os.path.getsize(p)
    return sum(os.path.getsize(os.path.join(d, f)) for d, _, fs in os.walk(p) for f in fs)


def protected_words():
    """앞으로 칸·남은 비축 글에서 편 코드(H-5·KOSPI-1)와 쇼츠 이름(k1s_split → 편 k1)을 뽑는다."""
    d = json.load(open(os.path.join(R, 'slots.json'), encoding='utf-8'))
    texts = [str(s.get('item', '')) + ' ' + str(s.get('note', ''))[:300]
             for s in d.get('slots', []) if str(s.get('at', '')) >= now.strftime('%Y-%m-%d')]
    for lst in (d.get('reserve') or {}).values():
        for r in lst if isinstance(lst, list) else []:
            if isinstance(r, dict):
                st = str(r.get('status', ''))[:40]
                if '소진' not in st and '쓰지 않음' not in st: texts.append(str(r.get('item', '')))
    eps, shorts = set(), set()
    for t in texts:
        for m in re.findall(r'\b([A-Z]{1,6}(?:-[A-Z]{1,4})?-\d{1,2})\b', t): eps.add(norm(m))
        for m in re.findall(r'\b([a-z]{1,6}\d{0,2})s_([a-z0-9]+)', t): eps.add(m[0]); shorts.add(norm(m[0] + 's' + m[1]))
    try:
        lab = json.load(open(os.path.join(W, '.render_lock'), encoding='utf-8')).get('label', '')
        eps.add(norm(lab.split()[0]))
    except Exception: pass
    return eps, shorts


def main():
    apply = '--apply' in sys.argv
    tracked = set(subprocess.run(['git', '-C', ROOT, 'ls-files', '-z', 'work/video'], capture_output=True)
                  .stdout.decode('utf-8', 'replace').split('\0'))
    rel = lambda p: os.path.relpath(p, ROOT).replace(os.sep, '/')
    has_tracked = lambda p: rel(p) in tracked or any(t.startswith(rel(p) + '/') for t in tracked)
    try:
        peps, pshorts = protected_words()
    except Exception as e:
        print('vidclean: slots.json 못 읽음 — 아무것도 지우지 않음', e); return 0
    pub = {}
    for mp in glob.glob(os.path.join(R, 'longform', 'ep', '*', 'meta.json')):
        try: at = json.load(open(mp, encoding='utf-8')).get('publishAt')
        except Exception: continue
        if at: pub[os.path.basename(os.path.dirname(mp))] = datetime.datetime.fromisoformat(at)
    go, keep = [], []
    bgs = os.listdir(os.path.join(V, 'public', 'bg'))
    auds = os.listdir(os.path.join(V, 'public', 'audio'))
    outs = os.listdir(os.path.join(V, 'out'))
    for ep, at in sorted(pub.items()):
        e = norm(ep)
        names = {e} | ({e[:-1]} if e.endswith('1') and len(e) >= 4 else set())   # D-ETF-1 → detf
        paths = [os.path.join(V, 'public', 'bg', b) for b in bgs if b in names]
        paths += [os.path.join(V, 'public', 'audio', a) for a in auds if norm(a.split('_')[0]) == e]
        paths += [os.path.join(V, 'out', o) for o in outs
                  if (re.match(rf'^(old_?)?({"|".join(map(re.escape, names))})([_\-.].*)?$', o.lower())
                      and o.lower() not in {f'{n}.mp4' for n in names})]
        paths = [p for p in paths if os.path.exists(p)]
        if not paths: continue
        why = None
        if at > now: why = '공개 전'
        elif (now - at).days < DAYS: why = f'공개 {(now - at).days}일째(<{DAYS}일)'
        elif e in peps or any(n in peps for n in names): why = '앞으로 칸·비축이 이 편을 씀(쇼츠)'
        for p in paths:
            if has_tracked(p): keep.append((size(p), rel(p), 'git 추적'))
            elif why: keep.append((size(p), rel(p), why))
            else: go.append((size(p), rel(p), f'{ep} 공개 {at:%m-%d}'))
    for b in bgs:   # 쇼츠 재료
        m = re.match(r'^([a-z]+\d*)s_([a-z0-9_]+)$', b)
        if not m: continue
        p = os.path.join(V, 'public', 'bg', b)
        old = (now.timestamp() - max(os.path.getmtime(os.path.join(d, f)) for d, _, fs in os.walk(p) for f in fs or ['.'])) / 86400 if any(fs for _, _, fs in os.walk(p)) else 99
        if norm(b) in pshorts or m.group(1) in peps: keep.append((size(p), rel(p), '앞으로 칸·비축 쇼츠'))
        elif has_tracked(p): keep.append((size(p), rel(p), 'git 추적'))
        elif old < DAYS: keep.append((size(p), rel(p), f'{old:.0f}일 전 수정'))
        else: go.append((size(p), rel(p), '쇼츠 재료(칸·비축에 없음)'))
    G = lambda rows: sum(r[0] for r in rows) / 1e9
    print(f"vidclean{'' if apply else '(목록만)'}: 지울 것 {len(go)}개 {G(go):.2f}GB · 남김 {len(keep)}개 {G(keep):.2f}GB · 보호 편 {sorted(peps)}")
    for s, p, w in sorted(go, reverse=True): print(f'  지움 {s/1e9:6.2f}GB  {p}  ({w})')
    for s, p, w in sorted(keep, reverse=True)[:25]: print(f'  남김 {s/1e9:6.2f}GB  {p}  ({w})')
    if apply:
        for _, p, _ in go:
            a = os.path.join(ROOT, p)
            shutil.rmtree(a, ignore_errors=True) if os.path.isdir(a) else os.remove(a)
    return 0


if __name__ == '__main__':
    sys.exit(main())
