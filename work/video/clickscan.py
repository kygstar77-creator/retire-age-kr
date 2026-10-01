# 말 끝난 직후 '치직' 찾기·고치기 (2026-10-02 사장님 "유튜브 말 끝나고 치직 했는데").
#   py -3.12 work/video/clickscan.py scan <파일.wav|.mp4|.pcm|폴더> [...]   # 치직 목록(시각·세기). 하나라도 있으면 종료코드 1
#   py -3.12 work/video/clickscan.py fix  <문장wav 폴더>                    # 문장 wav의 치직을 지우고 페이드·DC 제거(원본은 _preclick/에)
# 실측(10/02 01:4x): 제미나이 TTS(gemini-3.8-flash-tts) 응답 끝에 0.12~0.15초 광대역 잡음(rms 13,000~24,000, 4kHz 위 에너지 38%)이
#   붙어 온다. E-1 원본 응답 17개 중 13개, A-1·D-1도 같음. 응답마다 마지막 문장 = 장 끝 문장 바로 뒤에서 난다.
#   어제 진단(ㅅ·ㅊ 쉿소리, deess.py)은 다른 소리였다 — 디에서는 이 잡음을 못 지운다.
# 판정: 10ms 틀 rms > 8,000 이고 4kHz 위 비율 > 0.25 인 틀이 4개 이상 이어지고(목소리는 이렇게 크고 고르게 '쉬'하지 않는다),
#   그 앞 100ms 안에 조용한 틀(rms < 400)이 있으면 '말 끝난 뒤 잡음'. 경계 클릭: 이웃 샘플 차이 > 12,000.
import sys, os, glob, wave, subprocess, shutil, json
import numpy as np
sys.stdout.reconfigure(encoding='utf-8')
SR = 24000

def load(fn):
    if fn.endswith('.pcm'): return np.fromfile(fn, np.int16).astype(np.float32), SR
    if fn.endswith('.wav'):
        with wave.open(fn) as w: return np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32), w.getframerate()
    import imageio_ffmpeg
    raw = subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), '-v', 'error', '-i', fn, '-vn', '-ac', '1', '-ar', str(SR), '-f', 's16le', '-'],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32), SR

def frames(a, sr):
    k = sr // 100; n = len(a) // k
    if n == 0: return np.zeros(0), np.zeros(0), k
    x = a[:n * k].reshape(n, k)
    rms = np.sqrt((x ** 2).mean(1))
    S = np.abs(np.fft.rfft(x * np.hanning(k), axis=1)) ** 2 + 1e-9; fq = np.fft.rfftfreq(k, 1 / sr)
    return rms, S[:, fq > 4000].sum(1) / S.sum(1), k

def bursts(a, sr):
    # 규칙 A(문장 wav·원본): 크고(rms>8,000) 쉬-하는(4kHz 위 >0.25) 틀 4개 이상, 앞 100ms 안에 조용한 틀.
    # 규칙 B(렌더·디에서 뒤 — 고음이 깎여 A로 안 잡힘): 무음(<200) 사이에 갑자기 낀 큰 섬(말 중앙값 1.8배·5,000 넘음) 0.04~0.25초.
    #   실측 e1_ds.mp4 55.97초: 무음 → rms 6,400~11,700 0.12초 → 무음. 진짜 말은 섬이 이보다 길고 중앙값 근처다.
    rms, hf, k = frames(a, sr); out = []
    if len(rms) == 0: return out
    i = 0
    while i < len(rms):
        if rms[i] > 8000 and hf[i] > 0.25:
            j = i
            while j < len(rms) and rms[j] > 8000 and hf[j] > 0.2: j += 1
            if j - i >= 4 and (i < 10 or rms[max(0, i - 10):i].min() < 400):
                out.append((i * k, j * k, int(rms[i:j].max())))
            i = j
        else: i += 1
    speech = rms[rms > 300]
    big = max(5000.0, 1.8 * float(np.median(speech))) if len(speech) else 5000.0
    quiet = rms < 200; i = 0
    while i < len(rms):
        if quiet[i]: i += 1; continue
        j = i
        while j < len(rms) and not quiet[j]: j += 1
        isl = rms[i:j]
        # 말은 소리가 서서히 커지고 출렁인다(3,300→7,500→9,600). 치직은 첫 10ms부터 다 크고 판판하다(11,500·11,200·12,300·11,600·12,000).
        #   첫 틀은 반만 걸칠 수 있어 둘째 틀부터 5개를 본다.
        h5 = isl[1:6]; flat = len(h5) == 5 and h5[0] > 0.8 * h5.max() and h5.std() / h5.mean() < 0.12
        if 4 <= j - i <= 25 and (i == 0 or quiet[i - 1]) and flat and np.median(h5) > big and not any(s <= i * k < e for s, e, _ in out):
            out.append((i * k, j * k, int(isl.max())))
        i = j
    return sorted(out)

def jumps(a):
    d = np.abs(np.diff(a)); return np.where(d > 12000)[0]

def scan_one(fn):
    a, sr = load(fn); b = bursts(a, sr)
    # 경계 클릭: 파일 첫·끝 샘플이 0에서 멀면 붙일 때 '틱'
    edge = [int(abs(a[np.nonzero(a)[0][0]])), int(abs(a[np.nonzero(a)[0][-1]]))] if np.any(a) else [0, 0]
    return {'file': fn, 'sec': round(len(a) / sr, 1), 'bursts': [(round(s / sr, 2), round((e - s) / sr, 2), m) for s, e, m in b],
            'edge': edge}

def clean(a, sr):
    # 1) 치직 구간을 지운다(앞 10ms부터 끝까지 0, 뒤에 말이 이어지면 그 구간만) 2) DC 제거 3) 소리 앞뒤 페이드(인 8ms·아웃 25ms)
    a = a.copy()
    for s, e, _ in bursts(a, sr):
        s = max(0, s - sr // 100); a[s:min(len(a), e + sr // 50)] = 0
    nz = np.nonzero(np.abs(a) > 1)[0]
    if len(nz) == 0: return a
    s, e = nz[0], nz[-1] + 1
    body = a[s:e].copy(); body -= body.mean()   # copy 필수: 아래 a[:] = 0 이 보기(view)까지 지운다(10/02 01:5x 전 문장 무음 사고)
    fi, fo = min(len(body), int(sr * .008)), min(len(body), int(sr * .025))
    body[:fi] *= np.linspace(0, 1, fi); body[len(body) - fo:] *= np.linspace(1, 0, fo)
    a[:] = 0; a[s:e] = body
    return a

def fix_dir(d):
    bak = os.path.join(d, '_preclick'); os.makedirs(bak, exist_ok=True); n = 0
    for fn in sorted(glob.glob(os.path.join(d, '*.wav'))):
        with wave.open(fn) as w: sr = w.getframerate(); a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32)
        b = os.path.join(bak, os.path.basename(fn))
        if not os.path.exists(b): shutil.copy2(fn, b)
        had = len(bursts(a, sr)); c = clean(a, sr)
        # 안전장치: 치직 말고 목소리 에너지가 2% 넘게 줄면 쓰지 않는다
        keep = np.ones(len(a), bool)
        for s0, e0, _ in bursts(a, sr): keep[max(0, s0 - sr // 100):e0 + sr // 50] = False
        ea, ec = float((a[keep] ** 2).sum()), float((c[keep] ** 2).sum())
        if ea > 0 and ec < 0.98 * ea: print('중단: 목소리가 줄었다', os.path.basename(fn), round(ec / ea, 3)); sys.exit(2)
        with wave.open(fn, 'wb') as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes(np.clip(c, -32768, 32767).astype(np.int16).tobytes())
        left = len(bursts(c, sr))
        if had or left: print(os.path.basename(fn), '치직', had, '→', left)
        n += had
    print(d, '지운 치직', n)

if __name__ == '__main__':
    cmd, args = sys.argv[1], sys.argv[2:]
    if cmd == 'fix':
        for d in args: fix_dir(d)
        sys.exit(0)
    files = []
    for p in args:
        files += sorted(glob.glob(os.path.join(p, '*.wav')) + glob.glob(os.path.join(p, '*.pcm'))) if os.path.isdir(p) else [p]
    bad = 0
    for f in files:
        r = scan_one(f)
        if r['bursts']: bad += len(r['bursts']); print(os.path.basename(f), r['sec'], '초 · 치직(시각초, 길이초, 최대rms):', r['bursts'][:8])
        if r['edge'] == [0, 0] or max(np.abs(load(f)[0]).max(), 0) < 1000: bad += 1; print(os.path.basename(f), '무음 파일(목소리 없음)')
    print(f'파일 {len(files)}개 · 치직 {bad}개'); sys.exit(1 if bad else 0)
