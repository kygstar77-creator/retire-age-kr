# NDG-1 묶음 점 그림 미리보기 렌더(--scale=0.5, renderlock 줄 서기) + 줄마다 스틸 + 보드 + motioncheck + U5 (2026-11-27 motion, h6render.py 틀)
import subprocess, imageio_ffmpeg, json, os, sys, glob, shutil, tempfile
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__)); W = os.path.abspath(os.path.join(H, '..', '..', '..', '..', '..')); V = os.path.join(W, 'video')
sys.path.insert(0, W); from renderlock import render_lock
ff = imageio_ffmpeg.get_ffmpeg_exe(); os.chdir(V)
MP4 = os.path.join(H, 'ndg1_dots.mp4')
if '--stills' not in sys.argv:
    pub = os.path.join(tempfile.gettempdir(), 'ndg1_motion_pub')
    for rel in ('fonts/pd500.ttf', 'fonts/pd700.ttf', 'human/paper_crumple.jpg'):
        os.makedirs(os.path.dirname(os.path.join(pub, rel)), exist_ok=True); shutil.copy(os.path.join(V, 'public', rel), os.path.join(pub, rel))
    before = set(glob.glob(os.path.join(tempfile.gettempdir(), 'remotion-webpack-bundle-*')))
    with render_lock('NDG-1 motion 미리보기', 60, 2.5):
        subprocess.run('npx remotion render src/motion/preview/entry.ts NDG1Dots "%s" --props="%s" --public-dir="%s" --scale=0.5 --muted --pixel-format=yuv420p --log=error --concurrency=2' % (MP4, os.path.join(H, 'ndg1_dots.json'), pub), shell=True, check=True)
    for b in set(glob.glob(os.path.join(tempfile.gettempdir(), 'remotion-webpack-bundle-*'))) - before: shutil.rmtree(b, ignore_errors=True)
os.chdir(H)
s = json.load(open('ndg1_dots.json', encoding='utf-8'))['dots']; a = 0; os.makedirs('ndg1_st', exist_ok=True)
for i, l in enumerate(s['lines']):
    t = (a + l['frames'] * 0.85) / 30
    subprocess.run([ff, '-loglevel', 'error', '-y', '-ss', f'{t:.2f}', '-i', 'ndg1_dots.mp4', '-frames:v', '1', f'ndg1_st/dots_{i:02d}.png'], check=True); a += l['frames']
subprocess.run([ff, '-loglevel', 'error', '-y', '-framerate', '1', '-i', 'ndg1_st/dots_%02d.png', '-filter_complex', 'tile=3x2:padding=6', '-frames:v', '1', 'board_dots.png'], check=True)
r = subprocess.run([sys.executable, '-X', 'utf8', os.path.join(V, 'motioncheck.py'), 'ndg1_dots.mp4'], capture_output=True, text=True, encoding='utf-8', errors='replace')
open('ndg1_mc.txt', 'w', encoding='utf-8').write(r.stdout); print(r.stdout[-600:])
import lfrender as LF
runs, _ = LF.still_runs(MP4); print('U5 최장', runs[0][0], '초 · 8초 넘는 곳', sum(r[0] > LF.STILL_MAX for r in runs))
