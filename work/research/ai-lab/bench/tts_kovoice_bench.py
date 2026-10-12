# 롱폼 목소리 비교 — 지금 Chirp 3 HD Charon(이미 받은 R-1 줄 파일) vs gemini-3.8-flash-tts 한국어 전용 목소리(9/22 Extended Voice Library, ko-KR 117개)
#   py -3.12 work/research/ai-lab/bench/tts_kovoice_bench.py <ep폴더> <첫줄> <줄수> <목소리id,...>
# 같은 대본 줄. Chirp은 korsay 숫자 읽기 변환을 거친 녹음, 제미나이는 원문 그대로(숫자 변환 없이 읽는지 보려고).
# 잣대: 받아쓰기 글자 오류율(gemini-3.5-transcribe, 대본 원문 대비), 숫자 놓침, 말 속도(음절/말한 초), 음높이 중앙값.
import sys, os, json, re, io, wave, base64, difflib, time, urllib.request
import numpy as np
sys.stdout.reconfigure(encoding='utf-8')
W = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..')
sys.path.insert(0, W)
import lfvoice as L
ep, a0, n, voices = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4].split(',')
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '2026-10-12-tts-kovoice'); os.makedirs(OUT, exist_ok=True)
cfg = L.lock(ep)
texts = [t for s in L.sections(ep) for t in s['lines']][a0:a0 + n]
nsyl = sum(L.syl(t) for t in texts)
norm = lambda t: re.sub(r'[\s\.,!?%·~\-\'"“”‘’()\[\]:]', '', t)
num = lambda t: re.findall(r'\d+(?:\.\d+)?', t.replace(',', ''))
def lev(a, b):
    p = list(range(len(b) + 1))
    for i, x in enumerate(a, 1):
        c = [i]
        for j, y in enumerate(b, 1): c.append(min(p[j] + 1, c[j - 1] + 1, p[j - 1] + (x != y)))
        p = c
    return p[-1]
gap = np.zeros(int(L.SR * 0.3), np.float32)
def chirp():
    parts = []
    for t in texts:
        fn = L.wav_of(ep, cfg, L.speak(ep, t))[1]
        if not os.path.exists(fn): sys.exit(f'Chirp 줄 파일 없음: {t[:20]}')
        a, sr = L.read(fn); parts += [a, gap]
    return np.concatenate(parts)
def tx(a):
    buf = io.BytesIO()
    with wave.open(buf, 'wb') as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(L.SR); w.writeframes(np.clip(a, -32768, 32767).astype(np.int16).tobytes())
    body = {'contents': [{'parts': [{'inlineData': {'mimeType': 'audio/wav', 'data': base64.b64encode(buf.getvalue()).decode()}}]}], 'generationConfig': {'temperature': 0}}
    r = json.load(urllib.request.urlopen(urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-transcribe:generateContent?key={L.key()}",
        data=json.dumps(body).encode(), headers={'Content-Type': 'application/json'}), timeout=300))
    p = r['candidates'][0]['content']['parts'][0]
    return (p.get('text') or p.get('audioTranscription', {}).get('text', '')).strip()
ref = ' '.join(texts); res = {}
for name in ['chirp'] + voices:
    pfn = os.path.join(OUT, name + '.pcm')
    if os.path.exists(pfn): a = np.fromfile(pfn, dtype=np.int16).astype(np.float32)
    else:
        try: a = chirp() if name == 'chirp' else L.request({'model': 'gemini-3.8-flash-tts', 'voice': name, 'prompt': L.PROMPT}, texts)
        except Exception as e: res[name] = {'error': str(e)[:200]}; print(name, 'ERR', str(e)[:200]); continue
        np.clip(a, -32768, 32767).astype(np.int16).tofile(pfn)
    tfn = os.path.join(OUT, name + '.txt')
    if not os.path.exists(tfn):
        open(tfn, 'w', encoding='utf-8').write(tx(a)); time.sleep(21)
    heard = open(tfn, encoding='utf-8').read()
    cer = lev(norm(ref), norm(heard)) / max(1, len(norm(ref)))   # 편집 거리(끼어든 글자도 센다 — 10/5 lite 비교의 matching-blocks 방식은 끼어든 글자를 못 셌다)
    sp = L.speech_sec(a, L.SR); f0 = L.f0(a, L.SR)
    res[name] = {'total_sec': round(len(a) / L.SR, 2), 'rate': round(nsyl / sp, 2), 'f0_med': round(f0 or 0, 1), 'cer_pct': round(cer * 100, 2),
                 'num_miss': [x for x in num(ref) if x not in num(heard)]}
    L.write(os.path.join(OUT, name + '.wav'), a)
print(json.dumps({'ep': ep, 'lines': len(texts), 'syllables': nsyl, 'results': res}, ensure_ascii=False, indent=1))
json.dump({'ref': texts, 'results': res}, open(os.path.join(OUT, 'result.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
