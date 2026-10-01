# 렌더 뒤 목소리 '치익'(ㅅ·ㅊ 쉿소리) 줄이기 — 화면은 그대로 복사, 소리만 디에서 통과.
#   py -3.12 work/video/deess.py <입력.mp4> [출력.mp4]      # 출력 생략 시 <입력>_ds.mp4
#   py -3.12 work/video/deess.py --measure <파일>          # 쉿소리/모음 비(dB)·대역만 잰다
# 2026-10-01 사장님 "두 번째 유튜브 영상에서 치익~ 하는 소리 너무 거슬린다".
# 실측(E-1 앞 120초): 우리 렌더에는 효과음 트랙이 없다(Remotion은 문장 wav만, 쇼츠는 합성 패드뿐) →
#   '치익'은 TTS 목소리의 ㅅ·ㅊ 쉿소리. 쉿소리 구간 중앙 세기가 모음보다 7.6dB 낮을 뿐(A-1도 -8.5dB).
#   시험 6종 중 deesser i=0.6:m=0.5:f=0.6 → 앞 120초 쉿소리 -14.6dB(7dB 줄임), 2~4kHz(또렷함)는 -2.3dB만. (i=0.5:f=0.5는 편 전체 -11.5dB로 기준 못 넘음)
#   더 센 설정(i=0.8)은 2~4kHz가 -5dB라 혀 짧은 소리 위험 → 안 씀. 기준: 쉿소리/모음 -12dB 이하.
import sys, subprocess, os
import numpy as np, imageio_ffmpeg
sys.stdout.reconfigure(encoding='utf-8')
FF = imageio_ffmpeg.get_ffmpeg_exe()
FILTER = 'deesser=i=0.6:m=0.5:f=0.6:s=o'
LIMIT_DB = -12.0

def measure(path, sec=None):
    sr = 44100
    cmd = [FF, '-v', 'error', '-i', path] + (['-t', str(sec)] if sec else []) + ['-vn', '-ac', '1', '-ar', str(sr), '-f', 's16le', '-']
    x = np.frombuffer(subprocess.run(cmd, capture_output=True, check=True).stdout, np.int16).astype(np.float32) / 32768
    N = 1024; fr = np.lib.stride_tricks.sliding_window_view(x, N)[::N] * np.hanning(N)
    S = np.abs(np.fft.rfft(fr, axis=1)) ** 2 + 1e-12; fq = np.fft.rfftfreq(N, 1 / sr)
    rms = np.sqrt((fr ** 2).mean(1)); hf = S[:, fq > 4000].sum(1) / S.sum(1)
    voiced = (rms > 0.01) & (hf < 0.2); sib = (rms > 0.01) & (hf > 0.6)
    if voiced.sum() < 10 or sib.sum() < 10: return None
    act = rms > 0.01; tot = S[act].sum()
    band = lambda a, b: round(float(10 * np.log10(S[act][:, (fq >= a) & (fq < b)].sum() / tot)), 1)
    return {'sib_vs_voiced_db': round(float(20 * np.log10(np.median(rms[sib]) / np.median(rms[voiced]))), 1),
            'band_2_4k': band(2000, 4000), 'band_4_8k': band(4000, 8000), 'band_8_12k': band(8000, 12000)}

def run(src, dst):
    subprocess.run([FF, '-v', 'error', '-y', '-i', src, '-map', '0:v', '-map', '0:a', '-c:v', 'copy',
                    '-af', FILTER, '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', dst], check=True)
    a, b = measure(src), measure(dst)
    print('전', a); print('후', b)
    if b and b['sib_vs_voiced_db'] > LIMIT_DB: print(f'경고: 쉿소리가 아직 {b["sib_vs_voiced_db"]}dB (기준 {LIMIT_DB}dB 이하)'); sys.exit(1)
    print(dst)

if __name__ == '__main__':
    if sys.argv[1] == '--measure': print(measure(sys.argv[2])); sys.exit(0)
    src = sys.argv[1]; dst = sys.argv[2] if len(sys.argv) > 2 else os.path.splitext(src)[0] + '_ds.mp4'
    run(src, dst)
