# 쇼츠 쉿소리 비 — deess.measure()와 같은 식(쉿소리 틀 = rms>0.01·4kHz 위 60% 넘음, 모음 틀 = 20% 밑), 틀 수 10개 제한 없이 잰다(45~55초 클립은 디에서 뒤 틀이 10개 밑이라 measure가 None). 2026-10-11 PD
#   py -3.12 work/research/cardshorts/c1clips_sib.py <mp4 …>
import sys, subprocess, numpy as np, imageio_ffmpeg
FF = imageio_ffmpeg.get_ffmpeg_exe()
for path in sys.argv[1:]:
    sr = 44100
    x = np.frombuffer(subprocess.run([FF, '-v', 'error', '-i', path, '-vn', '-ac', '1', '-ar', str(sr), '-f', 's16le', '-'], capture_output=True, check=True).stdout, np.int16).astype(np.float32) / 32768
    N = 1024; fr = np.lib.stride_tricks.sliding_window_view(x, N)[::N] * np.hanning(N)
    S = np.abs(np.fft.rfft(fr, axis=1)) ** 2 + 1e-12; fq = np.fft.rfftfreq(N, 1 / sr)
    rms = np.sqrt((fr ** 2).mean(1)); hf = S[:, fq > 4000].sum(1) / S.sum(1)
    voiced = (rms > 0.01) & (hf < 0.2); sib = (rms > 0.01) & (hf > 0.6)
    db = 20 * np.log10(np.median(rms[sib]) / np.median(rms[voiced])) if sib.sum() else None
    print(path.split('/')[-1], 'voiced', int(voiced.sum()), 'sib', int(sib.sum()), 'sib_vs_voiced_db', None if db is None else round(float(db), 1))
