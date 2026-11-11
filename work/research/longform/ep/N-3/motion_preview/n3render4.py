# N-3 MeanPull만 다시(11/11 motion · visual 09:10 요청: 1% 추→깃발 줄 빼기, '중간값'→'가운데쯤') — N3Motion의 mean 구간 프레임만 렌더 → 줄마다 스틸·보드 → U5·bgcheck
import subprocess, imageio_ffmpeg, json, os, sys, glob, shutil, tempfile
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__)); V = os.path.abspath(os.path.join(H, '..', '..', '..', '..', '..', 'video')); WK = os.path.abspath(os.path.join(V, '..'))
ff = imageio_ffmpeg.get_ffmpeg_exe(); MP4 = os.path.join(H, 'n3_mean4.mp4')
d = json.load(open(os.path.join(H, 'n3_motion.json'), encoding='utf-8')); c0 = d['cap']['frames']; c1 = c0 + d['mean']['frames'] - 1
if '--stills' not in sys.argv:
    os.chdir(V); pub = os.path.join(tempfile.gettempdir(), 'n3_motion_pub')
    for rel in ('fonts/pd500.ttf', 'fonts/pd700.ttf', 'human/paper_crumple.jpg'):
        os.makedirs(os.path.dirname(os.path.join(pub, rel)), exist_ok=True); shutil.copy(os.path.join(V, 'public', rel), os.path.join(pub, rel))
    before = set(glob.glob(os.path.join(tempfile.gettempdir(), 'remotion-webpack-bundle-*')))
    subprocess.run('npx remotion render src/motion/preview/entry.ts N3Motion "%s" --props="%s" --public-dir="%s" --frames=%d-%d --pixel-format=yuv420p --log=error --concurrency=2' % (MP4, os.path.join(H, 'n3_motion.json'), pub, c0, c1), shell=True, check=True)
    for b in set(glob.glob(os.path.join(tempfile.gettempdir(), 'remotion-webpack-bundle-*'))) - before: shutil.rmtree(b, ignore_errors=True)
os.chdir(H); os.makedirs('n3_st4', exist_ok=True); a = 0
for i, l in enumerate(d['mean']['lines']):
    t = (a + l['frames'] * 0.8) / 30
    subprocess.run([ff, '-loglevel', 'error', '-y', '-ss', f'{t:.2f}', '-i', MP4, '-frames:v', '1', '-vf', 'scale=960:-1', f'n3_st4/mean_{i:02d}.png'], check=True); a += l['frames']
subprocess.run([ff, '-loglevel', 'error', '-y', '-framerate', '1', '-i', 'n3_st4/mean_%02d.png', '-filter_complex', 'tile=3x3:padding=6', '-frames:v', '1', 'board_mean4.png'], check=True)
sys.path.insert(0, WK); import lfrender as LF
runs, _ = LF.still_runs(MP4); print('U5 최장', runs[0][0], '초 · 8초 넘는 곳', sum(r[0] > LF.STILL_MAX for r in runs))
r = subprocess.run([sys.executable, '-X', 'utf8', os.path.join(WK, 'bgcheck.py'), MP4], capture_output=True, text=True, encoding='utf-8', errors='replace'); print(r.stdout[-700:], r.stderr[-300:])
