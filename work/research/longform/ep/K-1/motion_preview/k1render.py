# K-1 움직이는 판 셋(DaysOver·CrossOver·SameDirDots, 11/3) 미리보기 렌더 + 줄마다 스틸 + 보드 + motioncheck + U5 (2026-11-03 motion)
# 11/3: 디스크 C: 18GB — Remotion은 렌더마다 public(5.9GB)을 통째로 복사한다. 이 부품들은 글꼴·종이 결만 쓰므로 6MB짜리 작은 public을 따로 만들어 --public-dir로 넘긴다.
import subprocess, imageio_ffmpeg, json, os, sys, glob, shutil, tempfile
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__)); V = os.path.abspath(os.path.join(H, '..', '..', '..', '..', '..', 'video'))
ff = imageio_ffmpeg.get_ffmpeg_exe(); os.chdir(V)
MP4 = os.path.join(H, 'k1_motion.mp4')
if '--stills' not in sys.argv:
    pub = os.path.join(tempfile.gettempdir(), 'k1_motion_pub')
    for rel in ('fonts/pd500.ttf', 'fonts/pd700.ttf', 'human/paper_crumple.jpg'):
        os.makedirs(os.path.dirname(os.path.join(pub, rel)), exist_ok=True); shutil.copy(os.path.join(V, 'public', rel), os.path.join(pub, rel))
    before = set(glob.glob(os.path.join(tempfile.gettempdir(), 'remotion-webpack-bundle-*')))   # 남(PD 본편)의 살아 있는 번들은 지우지 않는다
    subprocess.run('npx remotion render src/motion/preview/entry.ts K1Motion "%s" --props="%s" --public-dir="%s" --pixel-format=yuv420p --log=error --concurrency=2' % (MP4, os.path.join(H, 'k1_motion.json'), pub), shell=True, check=True)
    for b in set(glob.glob(os.path.join(tempfile.gettempdir(), 'remotion-webpack-bundle-*'))) - before: shutil.rmtree(b, ignore_errors=True)
os.chdir(H)
d = json.load(open('k1_motion.json', encoding='utf-8')); o = 0; os.makedirs('k1_st', exist_ok=True)
for k in ('over', 'cross', 'dots'):
    s = d[k]; a = o
    for i, l in enumerate(s['lines']):
        t = (a + l['frames'] * 0.85) / 30
        subprocess.run([ff, '-loglevel', 'error', '-y', '-ss', f'{t:.2f}', '-i', 'k1_motion.mp4', '-frames:v', '1', '-vf', 'scale=960:-1', f'k1_st/{k}_{i:02d}.png'], check=True); a += l['frames']
    subprocess.run([ff, '-loglevel', 'error', '-y', '-framerate', '1', '-i', f'k1_st/{k}_%02d.png', '-filter_complex', 'tile=3x2:padding=6', '-frames:v', '1', f'board_{k}.png'], check=True)
    o += s['frames']
r = subprocess.run([sys.executable, '-X', 'utf8', os.path.join(V, 'motioncheck.py'), 'k1_motion.mp4'], capture_output=True, text=True, encoding='utf-8', errors='replace')
open('k1_mc.txt', 'w', encoding='utf-8').write(r.stdout); print(r.stdout[-600:])
sys.path.insert(0, os.path.abspath(os.path.join(V, '..'))); import lfrender as LF
runs, _ = LF.still_runs(MP4); print('U5 최장', runs[0][0], '초 · 8초 넘는 곳', sum(r[0] > LF.STILL_MAX for r in runs))
