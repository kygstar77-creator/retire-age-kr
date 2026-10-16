# FxDates 미리보기 렌더(원래 크기) + 줄마다 스틸 + 보드 + motioncheck (2026-10-16 motion)
import subprocess, imageio_ffmpeg, json, os, sys
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__)); V = os.path.abspath(os.path.join(H, '..', '..', '..', '..', '..', 'video'))
ff = imageio_ffmpeg.get_ffmpeg_exe(); os.chdir(V)
subprocess.run('npx remotion render src/motion/preview/entry.ts X1Fx "%s" --props="%s" --pixel-format=yuv420p --log=error' % (os.path.join(H, 'x1_fx.mp4'), os.path.join(H, 'x1_fx.json')), shell=True, check=True)
os.chdir(H)
d = json.load(open('x1_fx.json', encoding='utf-8')); o = d['s1']['frames']
B = d['fx']['b1'] + [o + b for b in d['fx']['b2']] + [o + d['s2']['frames']]
k = 0
for i in range(len(B) - 1):
    subprocess.run([ff, '-loglevel', 'error', '-y', '-ss', str(round((B[i] + (B[i + 1] - B[i]) * 0.85) / 30, 2)), '-i', 'x1_fx.mp4', '-frames:v', '1', f'st_{k:02d}.png'], check=True); k += 1
subprocess.run([ff, '-loglevel', 'error', '-y', '-framerate', '1', '-i', 'st_%02d.png', '-filter_complex', 'scale=960:-1,tile=2x5', '-frames:v', '1', 'board_fx.png'], check=True)
r = subprocess.run([sys.executable, os.path.join(V, 'motioncheck.py'), 'x1_fx.mp4'], capture_output=True, text=True, encoding='utf-8', errors='replace')
open('fx_mc.txt', 'w', encoding='utf-8').write(r.stdout); print(r.stdout[-500:])
