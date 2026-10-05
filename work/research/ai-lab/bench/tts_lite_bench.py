# TTS 모델 비교 — 롱폼 기본 gemini-3.8-flash-tts vs gemini-3.8-flash-lite-tts(9/23 GA, 무료 할당량 따로)
#   py -3.12 work/research/ai-lab/bench/tts_lite_bench.py <ep폴더> [묶음번호=0]
# 이미 받은 flash 원본(_raw/*.pcm)을 그대로 쓰고, 같은 문장·같은 지시문·같은 목소리로 lite만 1회 새로 부른다.
# 잣대: 말 속도(음절 ÷ 말한 시간, lfvoice.speech_sec), 음높이 중앙값과 5초 조각 간 흔들림(lfvoice.f0 — 규칙 4 ±12%),
#        받아쓰기 글자 오류율(gemini-3.5-transcribe, 공백·문장부호 무시), 숫자 놓침.
import sys, os, json, re, io, wave, base64, hashlib, difflib, time, urllib.request
import numpy as np
sys.stdout.reconfigure(encoding='utf-8')
W = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..')
sys.path.insert(0, W)
import lfvoice as L

ep = sys.argv[1]; gi = int(sys.argv[2]) if len(sys.argv) > 2 else 0
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '2026-10-05-tts-lite')
os.makedirs(OUT, exist_ok=True)
cfg = L.lock(ep); g = L.pack(L.sections(ep), 9)[gi]
texts = [L.speak(ep, t) for s in g for t in s['lines']]
rk = hashlib.md5(('|'.join([cfg['model'], cfg['voice']] + texts)).encode()).hexdigest()[:16]
raw = os.path.join(L.aud_dir(ep), '_raw', rk + '.pcm')
if not os.path.exists(raw): sys.exit(f'flash 원본 없음 {raw} — 일부 문장만 다시 녹음된 묶음이면 다른 묶음 번호로')
flash = np.fromfile(raw, dtype=np.int16).astype(np.float32)
lfn = os.path.join(OUT, 'lite.pcm')
if os.path.exists(lfn): lite = np.fromfile(lfn, dtype=np.int16).astype(np.float32)
else:
    lite = L.request(dict(cfg, model='gemini-3.8-flash-lite-tts'), texts)
    np.clip(lite, -32768, 32767).astype(np.int16).tofile(lfn)
nsyl = sum(L.syl(t) for t in texts)
norm = lambda t: re.sub(r'[\s\.,!?%·~\-\'"“”‘’()\[\]:]', '', t)
num = lambda t: re.findall(r'\d+(?:\.\d+)?', t.replace(',', ''))

def tx(a):
    buf = io.BytesIO()
    with wave.open(buf, 'wb') as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(L.SR); w.writeframes(np.clip(a, -32768, 32767).astype(np.int16).tobytes())
    body = {'contents': [{'parts': [{'inlineData': {'mimeType': 'audio/wav', 'data': base64.b64encode(buf.getvalue()).decode()}}]}], 'generationConfig': {'temperature': 0}}
    r = json.load(urllib.request.urlopen(urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-transcribe:generateContent?key={L.key()}",
        data=json.dumps(body).encode(), headers={'Content-Type': 'application/json'}), timeout=300))
    p = r['candidates'][0]['content']['parts'][0]
    return (p.get('text') or p.get('audioTranscription', {}).get('text', '')).strip()

ref = ' '.join(texts); res = {}
for name, a in (('flash', flash), ('lite', lite)):
    tfn = os.path.join(OUT, name + '.txt')
    if not os.path.exists(tfn):
        open(tfn, 'w', encoding='utf-8').write(tx(a)); time.sleep(21)   # 받아쓰기 무료 분당 3회
    heard = open(tfn, encoding='utf-8').read()
    sm = difflib.SequenceMatcher(None, norm(ref), norm(heard))
    cer = 1 - sum(b.size for b in sm.get_matching_blocks()) / max(1, len(norm(ref)))
    seg = int(L.SR * 5); f0s = [L.f0(a[i:i + seg], L.SR) for i in range(0, len(a) - seg, seg)]; f0s = [x for x in f0s if x]
    med = float(np.median(f0s)); spread = max(abs(x / med - 1) for x in f0s)
    miss = [n for n in num(ref) if n not in num(heard)]
    sp = L.speech_sec(a, L.SR)
    res[name] = {'total_sec': round(len(a) / L.SR, 2), 'speech_sec': round(sp, 2), 'rate': round(nsyl / sp, 2), 'f0_med': round(med, 1),
                 'f0_max_dev_pct': round(spread * 100, 1), 'cer_pct': round(cer * 100, 2), 'num_miss': miss}
    L.write(os.path.join(OUT, name + '.wav'), a)
print(json.dumps({'ep': ep, 'group': gi, 'lines': len(texts), 'syllables': nsyl, 'voice': cfg['voice'], 'results': res}, ensure_ascii=False, indent=1))
json.dump(res, open(os.path.join(OUT, 'result.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
