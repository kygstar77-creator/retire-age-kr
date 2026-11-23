# KOSPI-1 11/24 PD: 인사 3.83초를 자른 뒤 7분 58초 → 8분 바닥(ytlong) 아래. 끝 '숨 쉴 실사'(사진 8495394_last, 말 없는 줄)를
# 마지막 프레임으로 3초 더 멈추고, 깔린 음(-40dB)은 끝 4초에 걸쳐 0으로 줄인다. 말·글자 변경 0.
import subprocess, imageio_ffmpeg
FF = imageio_ffmpeg.get_ffmpeg_exe()
V = r'C:/Users/강영준/Documents/GitHub/retire-age-kr/work/video/out/'
SRC, OUT = V + 'kospi1_cut1124.mp4', V + 'kospi1_cut1124p.mp4'
d = float(subprocess.run([V + '../node_modules/@remotion/compositor-win32-x64-msvc/ffprobe.exe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', SRC], capture_output=True, text=True).stdout)
PAD = 3.0
fc = f'[0:v]tpad=stop_mode=clone:stop_duration={PAD}[v];[0:a]apad=pad_dur={PAD},afade=t=out:st={d + PAD - 4:.3f}:d=4[a]'
subprocess.run([FF, '-y', '-v', 'warning', '-i', SRC, '-filter_complex', fc, '-map', '[v]', '-map', '[a]', '-c:v', 'libx264', '-crf', '17', '-preset', 'medium',
                '-pix_fmt', 'yuv420p', '-r', '30', '-c:a', 'aac', '-b:a', '320k', '-movflags', '+faststart', OUT], check=True)
print('원래', round(d, 2), '초 → 새', OUT)
