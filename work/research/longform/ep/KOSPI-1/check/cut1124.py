# KOSPI-1 11/24 PD: 공개본(kospi1_dsl1123.mp4)에서 ① 달러 지폐 실사 3곳이 든 토막 10000~11999를 새 렌더 토막으로 갈고
# ② C-37 첫 인사 장면(scenes.0, 115프레임=3.83초)을 앞에서 잘라 낸다. 소리는 dsl1123 그대로(쉿소리·음량 맞춘 판), 앞만 같이 자름.
#   새 토막: lfrender render <ep> --frames=10000-10999 / 11000-11999 → out/kospi1_p1124_10000.mp4 · _11000.mp4 (화면만 씀)
#   py -3.12 work/research/longform/ep/KOSPI-1/check/cut1124.py
import subprocess, json, sys
V = r'C:/Users/강영준/Documents/GitHub/retire-age-kr/work/video'
FF = V + '/node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe'
FP = V + '/node_modules/@remotion/compositor-win32-x64-msvc/ffprobe.exe'
SRC = V + '/out/kospi1_dsl1123.mp4'
P1, P2 = V + '/out/kospi1_p1124_10000.mp4', V + '/out/kospi1_p1124_11000.mp4'
OUT = V + '/out/kospi1_cut1124.mp4'
props = json.load(open(V + '/kospi1.json', encoding='utf-8'))
TRIM = props['scenes'][0]['frames']
assert TRIM == 115, TRIM
nf = lambda f: int(subprocess.run([FP, '-v', 'error', '-count_packets', '-select_streams', 'v:0', '-show_entries', 'stream=nb_read_packets', '-of', 'csv=p=0', f], capture_output=True, text=True).stdout.strip())
n0, n1, n2 = nf(SRC), nf(P1), nf(P2)
print('프레임', n0, n1, n2)
assert n1 == 1000 and n2 == 1000, '토막 길이가 1000이 아님'
fc = (f'[0:v]trim=start_frame={TRIM}:end_frame=10000,setpts=PTS-STARTPTS[a];'
      f'[1:v]setpts=PTS-STARTPTS[b];[2:v]setpts=PTS-STARTPTS[c];'
      f'[3:v]trim=start_frame=12000,setpts=PTS-STARTPTS[d];'
      f'[a][b][c][d]concat=n=4:v=1:a=0[v];'
      f'[0:a]atrim=start={TRIM / 30:.6f},asetpts=PTS-STARTPTS,afade=t=in:d=0.25[au]')
import imageio_ffmpeg  # Remotion ffmpeg는 축소판이라 trim·setpts·concat 필터가 없음 → 전체판
cmd = [imageio_ffmpeg.get_ffmpeg_exe(), '-y', '-v', 'warning', '-i', SRC, '-i', P1, '-i', P2, '-i', SRC, '-filter_complex', fc, '-map', '[v]', '-map', '[au]',
       '-c:v', 'libx264', '-crf', '17', '-preset', 'medium', '-pix_fmt', 'yuv420p', '-r', '30', '-c:a', 'aac', '-b:a', '320k', '-movflags', '+faststart', OUT]
subprocess.run(cmd, check=True)
print('OK', OUT, '프레임', nf(OUT), '(기대', n0 - TRIM, ')')
