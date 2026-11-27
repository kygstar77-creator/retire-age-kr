# CC-1 장 카드 8장 미리보기 렌더(줄 세움) + 장마다 스틸 + 보드 + U5 (2026-11-27 motion)
import subprocess, imageio_ffmpeg, json, os, sys, shutil, tempfile
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__)); V = os.path.abspath(os.path.join(H, '..', '..', '..', '..', '..', 'video'))
W = os.path.abspath(os.path.join(V, '..')); ff = imageio_ffmpeg.get_ffmpeg_exe()
MP4 = os.path.join(H, 'cc1_asks.mp4'); PR = os.path.join(H, '_asks_props.json')
json.dump(json.load(open(os.path.join(H, 'cc1_asks.json'), encoding='utf-8'))['preview'], open(PR, 'w', encoding='utf-8'), ensure_ascii=False)
if '--stills' not in sys.argv:
    pub = os.path.join(tempfile.gettempdir(), 'cc1_asks_pub')
    for rel in ('fonts/pd500.ttf', 'fonts/pd700.ttf', 'human/paper_crumple.jpg'):
        os.makedirs(os.path.dirname(os.path.join(pub, rel)), exist_ok=True); shutil.copy(os.path.join(V, 'public', rel), os.path.join(pub, rel))
    os.chdir(V)
    cmd = ['py', '-3.12', os.path.join(W, 'renderlock.py'), '--label', 'CC-1 장 카드 미리보기', '--wait', '60', '--min-free', '2.5', '--',
           'npx', 'remotion', 'render', 'src/motion/preview/entry.ts', 'CC1Asks', MP4, f'--props={PR}', f'--public-dir={pub}', '--pixel-format=yuv420p', '--muted', '--log=error', '--concurrency=2']
    rc = subprocess.run(cmd, shell=True).returncode
    if rc: sys.exit(rc)
os.chdir(H); os.makedirs('st', exist_ok=True)
cards = json.load(open(PR, encoding='utf-8'))['cards']; a = 0
for i, c in enumerate(cards):
    t = (a + c['frames'] * 0.8) / 30
    subprocess.run([ff, '-loglevel', 'error', '-y', '-ss', f'{t:.2f}', '-i', 'cc1_asks.mp4', '-frames:v', '1', f'st/ask_{i+1}.png'], check=True); a += c['frames']
subprocess.run([ff, '-loglevel', 'error', '-y', '-framerate', '1', '-i', 'st/ask_%d.png', '-filter_complex', 'scale=960:-1,tile=4x2:padding=6', '-frames:v', '1', 'board_asks.png'], check=True)
sys.path.insert(0, W); import lfrender as LF
runs, _ = LF.still_runs(MP4); print('U5 최장', runs[0][0], '초')
