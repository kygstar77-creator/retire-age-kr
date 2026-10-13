# StepCliff 미리보기 렌더(원래 크기 — 0.5배 렌더는 카메라 확대 중 SVG 글자와 도형 배율이 어긋나 심사가 오독함, 10/13) + 줄마다 스틸 묶음(board_step.png) + motioncheck (2026-10-13 motion)
import subprocess, imageio_ffmpeg, json, os, sys, glob
H = os.path.dirname(os.path.abspath(__file__)); V = os.path.abspath(os.path.join(H, '..', '..', '..', '..', '..', 'video'))
ff = imageio_ffmpeg.get_ffmpeg_exe(); os.chdir(V)
subprocess.run('npx remotion render src/motion/preview/entry.ts P1Step "%s" --props="%s" --pixel-format=yuv420p --log=error' % (os.path.join(H, 'p1_step.mp4'), os.path.join(H, 'p1_step.json')), shell=True, check=True)
os.chdir(H)
d = json.load(open('p1_step.json', encoding='utf-8')); B = d['step']['beats'] + [d['scene']['frames']]
for i in range(len(B) - 1):
    subprocess.run([ff, '-loglevel', 'error', '-y', '-ss', str(round((B[i] + B[i + 1]) / 2 / 30 + 0.4, 2)), '-i', 'p1_step.mp4', '-frames:v', '1', f'st_{i:02d}.png'], check=True)
subprocess.run([ff, '-loglevel', 'error', '-y', '-framerate', '1', '-i', 'st_%02d.png', '-filter_complex', 'tile=4x4', '-frames:v', '1', 'board_step.png'], check=True)
r = subprocess.run([sys.executable, os.path.join(V, 'motioncheck.py'), 'p1_step.mp4'], capture_output=True, text=True, encoding='utf-8', errors='replace')
open('step_mc.txt', 'w', encoding='utf-8').write(r.stdout); print(r.stdout[-300:])
