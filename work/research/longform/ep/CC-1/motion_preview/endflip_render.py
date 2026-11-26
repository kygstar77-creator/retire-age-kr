# CC-1 EndFlip 미리보기 렌더 + 줄마다 스틸 + 보드 + motioncheck + U5 (2026-11-20 motion, k1render.py 틀 — 작은 public)
import subprocess, imageio_ffmpeg, json, os, sys, glob, shutil, tempfile
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__)); V = os.path.abspath(os.path.join(H, '..', '..', '..', '..', '..', 'video'))
ff = imageio_ffmpeg.get_ffmpeg_exe(); os.chdir(V)
MP4 = os.path.join(H, 'cc1_ends.mp4')
if '--stills' not in sys.argv:
    pub = os.path.join(tempfile.gettempdir(), 'cc1_ends_pub')
    for rel in ('fonts/pd500.ttf', 'fonts/pd700.ttf', 'human/paper_crumple.jpg'):
        os.makedirs(os.path.dirname(os.path.join(pub, rel)), exist_ok=True); shutil.copy(os.path.join(V, 'public', rel), os.path.join(pub, rel))
    for l in json.load(open(os.path.join(H, 'cc1_ends.json'), encoding='utf-8'))['ends']['lines']:   # 말 소리 4줄도 작은 public에
        if l.get('audio'): os.makedirs(os.path.dirname(os.path.join(pub, l['audio'])), exist_ok=True); shutil.copy(os.path.join(V, 'public', l['audio']), os.path.join(pub, l['audio']))
    before = set(glob.glob(os.path.join(tempfile.gettempdir(), 'remotion-webpack-bundle-*')))
    subprocess.run('npx remotion render src/motion/preview/entry.ts CC1Ends "%s" --props="%s" --public-dir="%s" --pixel-format=yuv420p --log=error --concurrency=2' % (MP4, os.path.join(H, 'cc1_ends.json'), pub), shell=True, check=True)
    for b in set(glob.glob(os.path.join(tempfile.gettempdir(), 'remotion-webpack-bundle-*'))) - before: shutil.rmtree(b, ignore_errors=True)
os.chdir(H)
s = json.load(open('cc1_ends.json', encoding='utf-8'))["ends"]; a = 0; os.makedirs('st', exist_ok=True)
for i, l in enumerate(s['lines']):
    t = (a + l['frames'] * 0.85) / 30
    subprocess.run([ff, '-loglevel', 'error', '-y', '-ss', f'{t:.2f}', '-i', 'cc1_ends.mp4', '-frames:v', '1', '-vf', 'scale=960:-1', f'st/ends_{i:02d}.png'], check=True); a += l['frames']
subprocess.run([ff, '-loglevel', 'error', '-y', '-framerate', '1', '-i', 'st/ends_%02d.png', '-filter_complex', 'tile=3x2:padding=6', '-frames:v', '1', 'board_ends.png'], check=True)
r = subprocess.run([sys.executable, '-X', 'utf8', os.path.join(V, 'motioncheck.py'), 'cc1_ends.mp4'], capture_output=True, text=True, encoding='utf-8', errors='replace')
open('cc1_ends_mc.txt', 'w', encoding='utf-8').write(r.stdout); print(r.stdout[-600:])
sys.path.insert(0, os.path.abspath(os.path.join(V, '..'))); import lfrender as LF
runs, _ = LF.still_runs(MP4); print('U5 최장', runs[0][0], '초 · 8초 넘는 곳', sum(r[0] > LF.STILL_MAX for r in runs))
