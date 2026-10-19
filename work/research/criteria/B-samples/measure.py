# B-screen 표본 재기(10/19) — 경쟁·우리 영상을 같은 잣대로.
#   py -3.12 measure.py <short|long> <영상.mp4> [소리.m4a] <id> <결과폴더>
# 재는 것
#   ① 글자 상자: 1초마다 한 장, RapidOCR 글자 찾기(읽기 안 함). 상자를 1080×1920(쇼츠)·1920×1080(롱폼) 좌표로 저장.
#      롱폼은 bgcheck.text_lines와 같은 법(426×240 → 852×480)도 함께: 가장 큰 글자 줄 높이 %, 줄 수(아래 20% 자막 띠 뺌).
#   ② 컷: ffmpeg scene > 0.3, 320px(bgcheck.cuts와 같은 법) → 분당 컷, 장면 길이.
#   ③ 소리: 통합 음량(LUFS, ffmpeg ebur128), 말·쉼 구간 음량(Whisper 어절 시각으로 말/쉼 나눔, 400ms RMS 중앙값),
#      말 빠르기(voicenat.rate — 0.25초 넘는 무음 뺀 음절/초, 사람 12편과 같은 잣대).
#   ④ 눈으로 볼 판: 쇼츠 2초·롱폼 10초마다 한 장 → sheets/<id>.jpg (남의 화면이라 커밋 안 함)
import sys, os, re, json, subprocess
import numpy as np, cv2
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); WORK = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, WORK)
import imageio_ffmpeg; FF = imageio_ffmpeg.get_ffmpeg_exe()   # remotion ffmpeg에는 ebur128이 없다
kind, mp4 = sys.argv[1], sys.argv[2]
rest = sys.argv[3:]
aud = rest[0] if len(rest) == 3 else mp4
vid, out = rest[-2], rest[-1]
os.makedirs(out, exist_ok=True); os.makedirs(os.path.join(HERE, 'sheets'), exist_ok=True)
LIMIT = 600 if kind == 'long' else 10 ** 6
res = {'id': vid, 'kind': kind}
from rapidocr_onnxruntime import RapidOCR
eng = RapidOCR(intra_op_num_threads=3, inter_op_num_threads=1)   # 작업 셋이 같이 돌 때 스레드 다툼을 줄인다(잰 값은 같음)

def ocr(img):
    r, _ = eng(img, use_det=True, use_cls=False, use_rec=False)
    return [np.array(b, dtype=float) for b in (r or [])]

cap = cv2.VideoCapture(mp4); fps = cap.get(cv2.CAP_PROP_FPS) or 30; n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
W, H = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
dur = min(n / fps, LIMIT); res.update(w=W, h=H, dur=round(n / fps, 1), measured=round(dur, 1))
RW, RH = (1080, 1920) if H > W else (1920, 1080)
frames, sheet = [], []
step_sheet = 2 if kind == 'short' else 10
i, t_next = 0, 0.0
while True:
    ok = cap.grab()
    if not ok: break
    t = i / fps
    if t > LIMIT: break
    if t + 1e-6 >= t_next:
        ok, bgr = cap.retrieve(); t_next += (1.0 if kind == 'short' else 3.0)   # 롱폼은 3초마다(10분 = 200장)
        if ok:
            fr = {'t': round(t, 1)}
            if H > W:
                s = cv2.resize(bgr, (540, 960), interpolation=cv2.INTER_AREA); sx, sy = RW / 540, RH / 960
                fr['boxes'] = [[round(b[:, 0].min() * sx), round(b[:, 1].min() * sy), round(b[:, 0].max() * sx), round(b[:, 1].max() * sy)] for b in ocr(s)]
            else:   # 롱폼: bgcheck.text_lines와 같은 법 한 번만(426×240 → 852×480), 상자는 1920×1080 좌표로
                s2 = cv2.resize(cv2.resize(bgr, (426, 240), interpolation=cv2.INTER_AREA), (852, 480), interpolation=cv2.INTER_CUBIC)
                bs = ocr(s2); hs = []
                fr['boxes'] = [[round(b[:, 0].min() * RW / 852), round(b[:, 1].min() * RH / 480), round(b[:, 0].max() * RW / 852), round(b[:, 1].max() * RH / 480)] for b in bs]
                for b in bs:
                    y0, y1 = b[:, 1].min() / 480, b[:, 1].max() / 480
                    if (y0 + y1) / 2 < 0.80: hs.append(y1 - y0)
                fr['maxh'] = round(max(hs, default=0) * 100, 2); fr['nlines'] = len(hs)
            frames.append(fr)
            if int(round(t)) % step_sheet == 0 and len(sheet) < 60:
                th = cv2.resize(bgr, (160, 284) if H > W else (256, 144), interpolation=cv2.INTER_AREA)
                cv2.putText(th, f'{int(t)//60}:{int(t)%60:02d}', (4, 14), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 255), 1)
                sheet.append(th)
    i += 1
cap.release()
res['frames'] = frames
if sheet:
    cols = 10 if kind == 'short' else 6
    while len(sheet) % cols: sheet.append(np.zeros_like(sheet[0]))
    rows = [np.hstack(sheet[k:k + cols]) for k in range(0, len(sheet), cols)]
    cv2.imencode('.jpg', np.vstack(rows), [cv2.IMWRITE_JPEG_QUALITY, 82])[1].tofile(os.path.join(HERE, 'sheets', f'{kind}_{vid}.jpg'))

# ② 컷
def scene(vf):
    r = subprocess.run([FF, '-hide_banner', '-i', mp4, '-t', str(LIMIT), '-vf', vf + "select='gt(scene,0.3)',metadata=print", '-an', '-f', 'null', '-'],
                       capture_output=True, text=True, encoding='utf-8', errors='replace')
    return sorted({round(float(m.group(1)), 2) for m in re.finditer(r'pts_time:([\d.]+)', r.stderr)})
cuts = scene('scale=320:-2,')                       # bgcheck와 같은 법(화면 전체)
res['cuts'] = cuts
mid = scene('crop=iw:ih*0.6:0:ih*0.2,scale=320:-2,')   # 위·아래 고정 띠(제목·로고)를 뺀 가운데 60%만 — 쇼츠는 고정 띠가 점수를 묽힌다
res['cuts_mid'] = mid; res['cuts_mid_pm'] = round(len([c for c in mid if c < dur]) / (dur / 60), 2) if dur else 0
e2 = [0.0] + [c for c in mid if 0 < c < dur] + [dur]; s2 = [b - a for a, b in zip(e2, e2[1:]) if b > a]
res['scene_mid_med'] = round(float(np.median(s2)), 2) if s2 else None
edges = [0.0] + [c for c in cuts if 0 < c < dur] + [dur]; segs = [b - a for a, b in zip(edges, edges[1:]) if b > a]
res['cuts_pm'] = round(len([c for c in cuts if c < dur]) / (dur / 60), 2) if dur else 0
res['scene_med'] = round(float(np.median(segs)), 2) if segs else None
res['scene_max'] = round(max(segs), 1) if segs else None

# ③ 소리
wav = os.path.join(out, f'{vid}.wav')
subprocess.run([FF, '-y', '-loglevel', 'error', '-i', aud, '-t', str(LIMIT), '-ac', '1', '-ar', '16000', wav], check=True)
r = subprocess.run([FF, '-hide_banner', '-nostats', '-i', aud, '-t', str(LIMIT), '-vn', '-af', 'ebur128', '-f', 'null', '-'], capture_output=True, text=True, encoding='utf-8', errors='replace')
# 원래 채널 그대로 잰다(모노로 줄이면 약 3LU 낮게 나온다)
m = re.findall(r'I:\s+(-?[\d.]+) LUFS', r.stderr); res['lufs'] = float(m[-1]) if m else None
m = re.findall(r'LRA:\s+(-?[\d.]+) LU', r.stderr); res['lra'] = float(m[-1]) if m else None
import voicenat
a = voicenat.load(wav)
WIN = float(os.environ.get('B_ASR_SEC', '300' if kind == 'short' else '180'))   # 롱폼 말 빠르기는 앞 3분(사람 12편 실측도 3분)
a_asr = a[:int(16000 * WIN)]
tmpw = os.path.join(out, f'{vid}_asr.wav')
import wave
with wave.open(tmpw, 'wb') as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(16000); w.writeframes((np.clip(a_asr, -1, 1) * 32767).astype(np.int16).tobytes())
ws = voicenat.words(tmpw)
res['asr_sec'] = round(len(a_asr) / 16000, 1); res['n_words'] = len(ws)
# 받아쓴 글은 남의 말이라 저장하지 않는다(어절 수만)
if ws:
    res['rate'] = round(voicenat.rate(ws, a_asr), 2)
    span = ws[-1][2] - ws[0][1]
    import korsay
    syl = sum(voicenat.SYLL(korsay.say(w)) for w, _, _ in ws)
    res['rate_all'] = round(syl / max(span, 0.1), 2)   # 쉼 포함(첫 어절~끝 어절)
    # 말/쉼 음량: 400ms 창 RMS dBFS. 말 = 어절 안, 쉼 = 어절 사이 0.5초 넘는 틈의 가운데
    def db(x): return 20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-9)
    sp = [db(a_asr[int(s * 16000):int(e * 16000)]) for _, s, e in ws if e - s >= 0.2]
    gp = []
    for (_, _, e1), (_, s2, _) in zip(ws, ws[1:]):
        if s2 - e1 >= 0.5:
            c = (e1 + s2) / 2; gp.append(db(a_asr[int((c - 0.15) * 16000):int((c + 0.15) * 16000)]))
    res['speech_db'] = round(float(np.median(sp)), 1) if sp else None
    res['pause_db'] = round(float(np.median(gp)), 1) if gp else None
    res['n_pause'] = len(gp)
    res['bed_gap_db'] = round(res['speech_db'] - res['pause_db'], 1) if sp and gp else None
    # 바닥 음: 첫~끝 어절 사이 100ms 창 dB의 중앙값 − 5백분위. 음악·소음이 깔리면 작고(10~25dB), 말 사이가 무음이면 크다(40dB+)
    seg = a_asr[int(ws[0][1] * 16000):int(ws[-1][2] * 16000)]; k = 1600; nwin = len(seg) // k
    if nwin > 20:
        d = 20 * np.log10(np.sqrt((seg[:nwin * k].reshape(nwin, k) ** 2).mean(1)) + 1e-9)
        res['win_med_db'] = round(float(np.median(d)), 1); res['win_p05_db'] = round(float(np.percentile(d, 5)), 1)
        res['floor_gap_db'] = round(res['win_med_db'] - res['win_p05_db'], 1)
for f in (wav, tmpw):
    try: os.remove(f)
    except OSError: pass
json.dump(res, open(os.path.join(out, f'{kind}_{vid}.json'), 'w', encoding='utf-8'), ensure_ascii=False)
print(vid, kind, 'cuts_pm', res['cuts_pm'], 'scene_med', res['scene_med'], 'lufs', res['lufs'], 'rate', res.get('rate'), 'bed', res.get('bed_gap_db'))
