# n1s_rank 렌더(10/17 PD) — v3redo.py의 화면 규칙(fmt_eok 억 소수 금지·번들·편마다 임시 폴더)대로, 소리 포함 렌더 → 디에서 → 관문(안전 영역·디자인·0초 빈 곳)·sheet
# 번들(C:/Users/Public/rtmp/bundles/c1s)은 public을 따로 들고 있어 새 wav(n1r_*.wav)를 번들 public/audio/n-1에도 복사해야 렌더된다(10/17 404).
import os, sys, json, subprocess
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); CS = os.path.dirname(HERE)
sys.path.insert(0, CS); import v3redo
VID = v3redo.VID; WORK = v3redo.WORK; REPO = v3redo.REPO
name = 'n1s_rank'
props = v3redo.fmt_eok(json.load(open(os.path.join(VID, name + '.json'), encoding='utf-8')))
assert props.get('bg')
tmp = f'_v3tmp_{name}.json'; json.dump(props, open(os.path.join(VID, tmp), 'w', encoding='utf-8'), ensure_ascii=False)
v = os.path.join(VID, 'out', f'{name}.mp4'); vd = os.path.join(VID, 'out', f'{name}_ds.mp4')
tdir = 'C:/Users/Public/rtmp/' + name; os.makedirs(tdir, exist_ok=True)
if '--skip-render' not in sys.argv:
    rc = subprocess.call(['npx', 'remotion', 'render', 'C:/Users/Public/rtmp/bundles/c1s', 'C1S', v, f'--props={tmp}', '--pixel-format=yuv420p', '--concurrency=3', '--bundle-cache=false', '--timeout=180000'], cwd=VID, shell=True, env=dict(os.environ, TEMP=tdir, TMP=tdir))
    if rc: sys.exit(rc)
sys.path.insert(0, VID); import deess
if '--skip-render' not in sys.argv: deess.run(v, vd, 'deesser=i=0.65:m=0.5:f=0.6:s=o')   # 기본 i=0.6은 -11.7dB(기준 -12 못 넘음) → 0.65 -12.5dB, 2~4kHz -19.8→-20.1dB(0.3dB만)
sys.path.insert(0, WORK); sys.path.insert(0, CS)
import safezone, bgcheck, emptyscan
ok1, m1 = safezone.gate(vd, quiet=True); ok2, m2 = bgcheck.gate(vd); e0 = emptyscan.frame0(vd)[0]
print(m1); print(m2); print(f'0초 빈 곳 {e0:.0%} (기준 {emptyscan.LIMIT0:.0%} 이하)')
v3redo.sheet(vd, os.path.join(HERE, 'sheet.png'))
json.dump({'mp4': os.path.relpath(vd, REPO).replace(chr(92), '/'), 'frames': v3redo.nframes(vd), 'safezone': ok1, 'design': ok2, 'empty0': round(e0, 3), 'msg': [m1, m2]}, open(os.path.join(HERE, 'render.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
