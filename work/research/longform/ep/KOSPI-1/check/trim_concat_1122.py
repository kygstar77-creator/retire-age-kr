# KOSPI-1 11/22 PD(H-6 trim_concat_1122.py 그대로, 이름만 kospi1): 토막 mp4마다 소리가 화면보다 약 53ms 길다(AAC 끝 채움, 끝이 빈 소리).
# concat -c copy로 붙이면 경계마다 50ms 끊김 + 소리가 경계마다 밀려 끝에서 약 0.8초 늦음(패치 토막 대조: 2000 +54ms · 9000 +426ms · 10000 +480ms).
# 실측(h5p_9000 자막 바뀜 프레임 8991 ↔ 57e3 wav 시작): 렌더마다 소리 앞에 빈 2,048샘플(43ms)이 붙어 소리가 늦다.
# 고침: 토막마다 앞 2,048샘플을 떼고 화면 길이(프레임/30초)만큼만 잘라 wav로 이어 붙이고, 화면은 그대로 이어 붙인 것에 얹는다.
import subprocess, numpy as np, wave, re, sys
V = r'C:/Users/강영준/Documents/GitHub/retire-age-kr/work/video'
FF = V + '/node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe'
FP = V + '/node_modules/@remotion/compositor-win32-x64-msvc/ffprobe.exe'
SR = 48000
LEAD = 2048
parts = re.findall(r"file '([^']+)'", open(V + '/out/kospi1_parts.txt', encoding='utf-8').read())
chunks = []
for p in parts:
    f = V + '/out/' + p
    nf = int(subprocess.run([FP, '-v', 'error', '-count_packets', '-select_streams', 'v:0', '-show_entries', 'stream=nb_read_packets', '-of', 'csv=p=0', f], capture_output=True, text=True).stdout.strip())
    t = 'C:/fm_render_tmp/_p.wav'
    subprocess.run([FF, '-y', '-v', 'error', '-i', f, '-vn', '-f', 'wav', '-acodec', 'pcm_s16le', t], check=True)
    with wave.open(t) as w: assert w.getframerate() == SR; a = np.frombuffer(w.readframes(w.getnframes()), np.int16).reshape(-1, 2)
    n = round(nf / 30 * SR)
    a = np.vstack([a, np.zeros((max(0, LEAD + n - len(a)), 2), np.int16)]); tail = a[LEAD + n:]
    print(p, '프레임', nf, '소리', len(a), '자를 샘플', n, '버리는 끝 rms', int(np.sqrt((tail.astype(float) ** 2).mean())) if len(tail) else 0)
    chunks.append(a[LEAD:LEAD + n])
full = np.vstack(chunks)
out = V + '/out/kospi1_trimaudio.wav'
with wave.open(out, 'wb') as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(full.tobytes())
print('소리 길이', len(full) / SR)
subprocess.run([FF, '-y', '-v', 'error', '-i', V + '/out/kospi1_vonly.mp4', '-i', out, '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '320k', '-shortest', V + '/out/kospi1.mp4'], check=True)
print('OK out/kospi1.mp4')
