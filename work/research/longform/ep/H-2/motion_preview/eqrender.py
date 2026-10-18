# H-2 5장 견본 방식 장면 셋(LoanSteps·EqStack·LoanSteps) 미리보기 렌더(원래 크기) + 줄마다 스틸 + 보드 + motioncheck (2026-10-18 motion)
import subprocess, imageio_ffmpeg, json, os, sys, glob, shutil, tempfile
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__)); V = os.path.abspath(os.path.join(H, '..', '..', '..', '..', '..', 'video'))
ff = imageio_ffmpeg.get_ffmpeg_exe(); os.chdir(V)
if '--stills' not in sys.argv:
    subprocess.run('npx remotion render src/motion/preview/entry.ts H2Eq "%s" --props="%s" --pixel-format=yuv420p --log=error' % (os.path.join(H, 'h2_eq.mp4'), os.path.join(H, 'h2_eq.json')), shell=True, check=True)
    for b in glob.glob(os.path.join(tempfile.gettempdir(), 'remotion-webpack-bundle-*')): shutil.rmtree(b, ignore_errors=True)   # 10/15 디스크 꽉 참 교훈
os.chdir(H)
d = json.load(open('h2_eq.json', encoding='utf-8')); o = 0; os.makedirs('eq_st', exist_ok=True)
for k in ('rule', 'cash', 'edge'):
    s = d[k]; a = o
    for i, l in enumerate(s['lines']):
        t = (a + l['frames'] * 0.8) / 30
        subprocess.run([ff, '-loglevel', 'error', '-y', '-ss', f'{t:.2f}', '-i', 'h2_eq.mp4', '-frames:v', '1', '-vf', 'scale=960:-1', f'eq_st/{k}_{i:02d}.png'], check=True); a += l['frames']
    subprocess.run([ff, '-loglevel', 'error', '-y', '-framerate', '1', '-i', f'eq_st/{k}_%02d.png', '-filter_complex', 'tile=3x4:padding=6', '-frames:v', '1', f'board_{k}.png'], check=True)
    o += s['frames']
r = subprocess.run([sys.executable, '-X', 'utf8', os.path.join(V, 'motioncheck.py'), 'h2_eq.mp4'], capture_output=True, text=True, encoding='utf-8', errors='replace')
open('eq_mc.txt', 'w', encoding='utf-8').write(r.stdout); print(r.stdout[-600:])
# U5(같은 화면 8초) — motioncheck 통과 ≠ U5 통과(10/17 교훈), lfrender.still_runs로 바로 잰다
sys.path.insert(0, os.path.abspath(os.path.join(V, '..'))); import lfrender as LF
runs, _ = LF.still_runs(os.path.join(H, 'h2_eq.mp4')); print('U5 최장', runs[0][0], '초 · 8초 넘는 곳', sum(r[0] > LF.STILL_MAX for r in runs))
