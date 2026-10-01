# 받아쓰기 모델 비교 — lfvoice.py readback의 1차 모델(gemini-3.5-flash-lite) vs 받아쓰기 전용 gemini-3.5-transcribe
#   py -3.12 work/research/ai-lab/bench/transcribe_bench.py <ep폴더> [최대줄수] [모델,모델]
# 같은 문장 음성을 두 모델에 넣고: 숫자 놓침(=readback 거짓 경보), 글자 오류율(CER, 공백·문장부호 무시), 실패(429 등), 걸린 시간.
import sys, os, json, re, time, io, wave, base64, difflib, urllib.request
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
from lfvoice import read, key, PUB  # 같은 파일 읽기·키를 그대로 쓴다

ep = sys.argv[1]; N = int(sys.argv[2]) if len(sys.argv) > 2 else 30
MODELS = (sys.argv[3] if len(sys.argv) > 3 else 'gemini-3.5-flash-lite,gemini-3.5-transcribe').split(',')
PROMPT = 'Transcribe this Korean audio verbatim. Write numbers exactly as spoken using digits.'   # readback과 같은 지시
num = lambda t: sorted(re.findall(r'\d+(?:\.\d+)?', re.sub(r'(\d+)천', lambda m: str(int(m.group(1)) * 1000), t.replace(',', ''))))
PACE = 21
norm = lambda t: re.sub(r'[\s\.,!?%·~\-\'"“”‘’()]', '', t)

def tx(fn, mdl):
    a, sr = read(fn); buf = io.BytesIO()
    import numpy as np
    with wave.open(buf, 'wb') as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes(a.astype(np.int16).tobytes())
    parts = [{'inlineData': {'mimeType': 'audio/wav', 'data': base64.b64encode(buf.getvalue()).decode()}}]
    if 'transcribe' in mdl: time.sleep(PACE)   # 전용 모델: 지시문 없이 오디오만, 무료 한도 분당 3회(10-01 실측 429)
    else: parts.append({'text': PROMPT})
    body = {'contents': [{'parts': parts}], 'generationConfig': {'temperature': 0}}
    t0 = time.time()
    try:
        r = json.load(urllib.request.urlopen(urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/{mdl}:generateContent?key={key()}",
            data=json.dumps(body).encode(), headers={'Content-Type': 'application/json'}), timeout=120))
        p0 = r['candidates'][0]['content']['parts'][0]   # 전용 모델은 text가 아니라 audioTranscription.text로 준다
        return (p0.get('text') or p0.get('audioTranscription', {}).get('text', '')).strip(), time.time() - t0, None
    except urllib.error.HTTPError as e: return None, time.time() - t0, f'HTTP {e.code}'
    except Exception as e: return None, time.time() - t0, type(e).__name__

v = json.load(open(os.path.join(ep, 'voice.json'), encoding='utf-8'))
lines = [l for s in v['sections'] for l in s['lines'] if l.get('audio') and re.search(r'\d', l['text'])][:N]
st = {m: {'ok': 0, 'fail': 0, 'nummiss': 0, 'cer': 0.0, 'sec': 0.0, 'errs': []} for m in MODELS}; rows = []
for l in lines:
    fn = os.path.join(PUB, l['audio'].replace('/', os.sep)); want = num(l['text']); row = {'text': l['text']}
    for m in MODELS:
        h, dt, err = tx(fn, m); s = st[m]; s['sec'] += dt
        if h is None: s['fail'] += 1; s['errs'].append(err); row[m] = err; continue
        s['ok'] += 1
        miss = [x for x in want if x not in num(h)]; s['nummiss'] += bool(miss)
        a, b = norm(l['text']), norm(h); cer = 1 - difflib.SequenceMatcher(None, a, b, autojunk=False).ratio(); s['cer'] += cer
        row[m] = {'heard': h, 'miss': miss, 'cer': round(cer, 3)}
    rows.append(row)
out = {'ep': ep, 'lines': len(lines), 'prompt': PROMPT, 'summary': {m: {'ok': s['ok'], 'fail': s['fail'], 'num_miss_lines': s['nummiss'],
       'cer_avg': round(s['cer'] / max(s['ok'], 1), 4), 'sec_avg': round(s['sec'] / max(len(lines), 1), 2), 'errs': sorted(set(s['errs']))} for m, s in st.items()}, 'rows': rows}
fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"transcribe_{os.path.basename(os.path.normpath(ep))}_{'+'.join(m.split('-')[-1] for m in MODELS)}.json")
json.dump(out, open(fn, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(json.dumps(out['summary'], ensure_ascii=False, indent=1)); print('→', fn)
