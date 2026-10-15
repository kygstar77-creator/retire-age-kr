# BuybackDays 미리보기 렌더(원래 크기) + 줄마다 스틸 2장 묶음(board_buy.png) + motioncheck (2026-10-15 motion)
import subprocess, imageio_ffmpeg, json, os, sys
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__)); V = os.path.abspath(os.path.join(H, '..', '..', '..', '..', '..', '..', 'video'))
ff = imageio_ffmpeg.get_ffmpeg_exe(); os.chdir(V)
subprocess.run('npx remotion render src/motion/preview/entry.ts W2Buy "%s" --props="%s" --pixel-format=yuv420p --log=error' % (os.path.join(H, 'w2_buy.mp4'), os.path.join(H, 'w2_buy.json')), shell=True, check=True)
os.chdir(H)
d = json.load(open('w2_buy.json', encoding='utf-8')); B = d['buy']['beats'] + [d['scene']['frames']]
k = 0
for i in range(len(B) - 1):
    for q in (0.4, 0.9):
        subprocess.run([ff, '-loglevel', 'error', '-y', '-ss', str(round((B[i] + (B[i + 1] - B[i]) * q) / 30, 2)), '-i', 'w2_buy.mp4', '-frames:v', '1', f'st_{k:02d}.png'], check=True); k += 1
subprocess.run([ff, '-loglevel', 'error', '-y', '-framerate', '1', '-i', 'st_%02d.png', '-filter_complex', 'tile=2x3', '-frames:v', '1', 'board_buy.png'], check=True)
r = subprocess.run([sys.executable, os.path.join(V, 'motioncheck.py'), 'w2_buy.mp4'], capture_output=True, text=True, encoding='utf-8', errors='replace')
open('buy_mc.txt', 'w', encoding='utf-8').write(r.stdout); print(r.stdout[-400:])
