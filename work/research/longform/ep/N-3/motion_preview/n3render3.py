# N-3 PayBlocks·RaiseStairs 마커 빗금판(11/9 motion) 미리보기 — 작은 public(글꼴·종이 결 6MB)으로 렌더 → 줄마다 스틸·보드 → bgcheck·UI 상자 수·U5
import subprocess, imageio_ffmpeg, json, os, sys, glob, shutil, tempfile
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__)); V = os.path.abspath(os.path.join(H, '..', '..', '..', '..', '..', 'video')); WK = os.path.abspath(os.path.join(V, '..'))
ff = imageio_ffmpeg.get_ffmpeg_exe(); MP4 = os.path.join(H, 'n3_motion3.mp4')
if '--stills' not in sys.argv:
    os.chdir(V); pub = os.path.join(tempfile.gettempdir(), 'n3_motion_pub')
    for rel in ('fonts/pd500.ttf', 'fonts/pd700.ttf', 'human/paper_crumple.jpg'):
        os.makedirs(os.path.dirname(os.path.join(pub, rel)), exist_ok=True); shutil.copy(os.path.join(V, 'public', rel), os.path.join(pub, rel))
    before = set(glob.glob(os.path.join(tempfile.gettempdir(), 'remotion-webpack-bundle-*')))
    subprocess.run('npx remotion render src/motion/preview/entry.ts N3Motion2 "%s" --props="%s" --public-dir="%s" --pixel-format=yuv420p --log=error --concurrency=2' % (MP4, os.path.join(H, 'n3_motion.json'), pub), shell=True, check=True)
    for b in set(glob.glob(os.path.join(tempfile.gettempdir(), 'remotion-webpack-bundle-*'))) - before: shutil.rmtree(b, ignore_errors=True)
os.chdir(H); d = json.load(open('n3_motion.json', encoding='utf-8')); o = 0; os.makedirs('n3_st3', exist_ok=True)
sys.path.insert(0, WK); import bgcheck as B, cv2
for k in ('blocks', 'stairs'):
    s = d[k]; a = o
    for i, l in enumerate(s['lines']):
        t = (a + l['frames'] * 0.8) / 30; png = f'n3_st3/{k}_{i:02d}.png'
        subprocess.run([ff, '-loglevel', 'error', '-y', '-ss', f'{t:.2f}', '-i', MP4, '-frames:v', '1', png], check=True); a += l['frames']
        print(png, 'UI 상자', B.ui_boxes(cv2.cvtColor(cv2.imread(png), cv2.COLOR_BGR2RGB)))
    subprocess.run([ff, '-loglevel', 'error', '-y', '-framerate', '1', '-i', f'n3_st3/{k}_%02d.png', '-filter_complex', 'scale=960:-1,tile=3x4:padding=6', '-frames:v', '1', f'board3_{k}.png'], check=True)
    o += s['frames']
r = subprocess.run([sys.executable, '-X', 'utf8', os.path.join(WK, 'bgcheck.py'), MP4], capture_output=True, text=True, encoding='utf-8', errors='replace'); print(r.stdout[-900:])
import lfrender as LF
runs, _ = LF.still_runs(MP4); print('U5 최장', runs[0][0], '초 · 8초 넘는 곳', sum(x[0] > LF.STILL_MAX for x in runs))
