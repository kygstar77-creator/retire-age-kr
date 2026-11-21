# H-5 11/21 PD: 토막 렌더 경계 뒤 0.1~0.6초 소리 끊김(50ms 0) 고치기
# out/h5_full_raw.mp4 소리에서 경계 b의 [b/30-1.5, b/30+1.5]초를 h5p_<b>.mp4(경계 3초 전부터 렌더, 끊김 자리가 토막 한가운데)의 같은 구간으로 바꿔 끼운다.
# 맞춤은 상호상관으로 샘플 단위 확인(±50ms), 이음매는 10ms 교차. 화면은 그대로 복사.
import subprocess, numpy as np, os, sys
V = r'C:/Users/강영준/Documents/GitHub/retire-age-kr/work/video'
FF = V + '/node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe'
SR = 48000
def dec(p):
    import wave; t = 'C:/fm_render_tmp/_dec.wav'
    subprocess.run([FF, '-y', '-v', 'error', '-i', p, '-vn', '-f', 'wav', '-acodec', 'pcm_s16le', t], check=True)
    with wave.open(t) as w: assert w.getframerate() == SR and w.getnchannels() == 2; raw = w.readframes(w.getnframes())
    return np.frombuffer(raw, np.int16).reshape(-1, 2).astype(np.float32)
main = dec(V + '/out/h5_full_raw.mp4')
fixed = main.copy()
for b in [2000, 4000, 5000, 6000, 7000, 9000, 10000]:
    p = dec(V + f'/out/h5p_{b}.mp4'); t0 = (b - 90) / 30
    s0 = int(round(t0 * SR))
    # 맞춤: 토막 1.0~2.0초(경계 2초 전, 양쪽 다 멀쩡한 곳)
    ref = p[int(1.0*SR):int(2.0*SR), 0]; best = (None, -2)
    for d in range(-2400, 2401, 4):
        m = main[s0 + int(1.0*SR) + d: s0 + int(2.0*SR) + d, 0]
        c = float(np.dot(ref, m) / (np.linalg.norm(ref) * np.linalg.norm(m) + 1e-9))
        if c > best[1]: best = (d, c)
    d = best[0]
    for dd in range(d - 4, d + 5):
        m = main[s0 + int(1.0*SR) + dd: s0 + int(2.0*SR) + dd, 0]
        c = float(np.dot(ref, m) / (np.linalg.norm(ref) * np.linalg.norm(m) + 1e-9))
        if c > best[1]: best = (dd, c)
    d = best[0]
    a, z = int(1.5*SR), int(4.5*SR)          # 토막 안 구간 = 경계 -1.5 ~ +1.5초
    seg = p[a:z].copy(); n = int(0.01*SR); w = np.linspace(0, 1, n)[:, None]
    tgt = slice(s0 + d + a, s0 + d + z)
    old = fixed[tgt]
    seg[:n] = old[:n] * (1 - w) + seg[:n] * w; seg[-n:] = seg[-n:] * (1 - w) + old[-n:] * w
    fixed[tgt] = seg
    diff = np.abs(old - seg).mean()
    print(f'{b}: 어긋남 {d} 샘플({d/SR*1000:.1f}ms) 상관 {best[1]:.4f} · 바꾼 구간 평균 차 {diff:.0f}')
out = V + '/out/h5_fixaudio.wav'
fixed = np.clip(fixed, -32768, 32767).astype(np.int16)
import wave
with wave.open(out, 'wb') as w_:
    w_.setnchannels(2); w_.setsampwidth(2); w_.setframerate(SR); w_.writeframes(fixed.tobytes())
subprocess.run([FF, '-y', '-v', 'error', '-i', V + '/out/h5_full_raw.mp4', '-i', out, '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '320k', V + '/out/h5.mp4'], check=True)
print('OK out/h5.mp4')
