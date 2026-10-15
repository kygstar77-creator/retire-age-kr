import imageio_ffmpeg, subprocess, sys, os
FF = imageio_ffmpeg.get_ffmpeg_exe(); mp4 = sys.argv[1]; out = sys.argv[2]
os.makedirs(out, exist_ok=True)
for t in sys.argv[3:]:
    subprocess.run([FF, '-loglevel', 'error', '-y', '-ss', t, '-i', mp4, '-frames:v', '1', '-vf', 'scale=540:-1', os.path.join(out, f't{t}.png')], check=True)
subprocess.run([FF, '-loglevel', 'error', '-y', '-i', mp4, '-vf', 'fps=1/3,scale=270:-1,tile=6x3', '-frames:v', '1', os.path.join(out, '..', 'sheet.png')], check=True)
subprocess.run([FF, '-loglevel', 'error', '-y', '-i', mp4, '-frames:v', '1', os.path.join(out, '..', 'frame0.png')], check=True)
