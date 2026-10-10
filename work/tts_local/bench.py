# 무료 로컬 TTS 비교(10/11 PD) — 같은 12줄(C-1 0장 예고)로 후보마다 줄 파일을 만들고, lfvoice.py의 f0·speech_sec로 잰다.
#   py -3.12 work/tts_local/bench.py lines            # lines.json(원문·숫자 한글 읽기) + 참고음성 ref_e1.wav(E-1 우리 녹음 2줄)
#   py -3.12 work/tts_local/bench.py gemini           # 기존 C-1 제미나이 줄 파일 → out/gemini/run1 (TTS 호출 없음)
#   py -3.12 work/tts_local/bench.py measure <후보>    # out/<후보>/run1·run2 → 표 한 줄 + samples/<후보>.wav
#   py -3.12 work/tts_local/bench.py hear <후보>       # 제미나이 받아쓰기(TTS 아님)로 발음 오류 세기, 429면 '확인 안 함'
import sys, os, re, json, glob, wave, time, base64, io, difflib, urllib.request, urllib.error
import numpy as np
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); WORK = os.path.dirname(HERE)
sys.path.insert(0, WORK)
import lfvoice
EP = os.path.join(WORK, 'research', 'longform', 'ep')
OUT = os.path.join(HERE, 'out'); SAMP = os.path.join(HERE, 'samples')
GAP = 8 / 30   # lfvoice 문장 사이 8프레임

D = '영일이삼사오육칠팔구'
def sino(n):
    if n == 0: return '영'
    s, u = '', 0
    while n:
        g = n % 10000; part = ''
        for d, k in ((g // 1000, '천'), (g // 100 % 10, '백'), (g // 10 % 10, '십'), (g % 10, '')):
            if d: part += ('' if (d == 1 and k) else D[d]) + k
        if g: s = (('' if (g == 1 and u == 1) else part) + ['', '만', '억', '조'][u]) + s
        n //= 10000; u += 1
    return s
def kor(t):   # 이 12줄의 숫자는 모두 한자어 읽기(년·원·만원·억·년째)
    return re.sub(r'\d[\d,]*', lambda m: sino(int(m.group(0).replace(',', ''))), t)

def lines():
    v = json.load(open(os.path.join(EP, 'C-1', 'voice.json'), encoding='utf-8'))['sections'][0]['lines']
    L = [{'say': l['say'], 'kor': kor(l['say']), 'gemini': l['audio']} for l in v]
    json.dump(L, open(os.path.join(HERE, 'lines.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    for l in L: print(l['kor'])
    # 참고 음성: 사장님이 좋다고 한 E-1의 우리 제미나이(Charon) 녹음 2줄, 숫자 없는 줄
    e = json.load(open(os.path.join(EP, 'E-1', 'voice.json'), encoding='utf-8'))
    pick = [l for s in e['sections'] for l in s['lines'] if l.get('audio') and os.path.basename(l['audio']).split('.')[0] in ('c55eb53936ad18b7', '975b0847c10f73d3')]
    a = [lfvoice.read(os.path.join(lfvoice.PUB, l['audio']))[0] for l in pick]
    ref = np.concatenate([a[0], np.zeros(int(24000 * 0.3), np.float32), a[1]])
    wr(os.path.join(HERE, 'ref_e1.wav'), ref, 24000)
    json.dump({'text': ' '.join(l['say'] for l in pick), 'files': [l['audio'] for l in pick]}, open(os.path.join(HERE, 'ref_e1.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    print('ref', len(ref) / 24000, 's |', ' '.join(l['say'] for l in pick))

def load(fn):
    with wave.open(fn) as w:
        sr, ch, sw = w.getframerate(), w.getnchannels(), w.getsampwidth(); b = w.readframes(w.getnframes())
    if sw == 2: a = np.frombuffer(b, np.int16).astype(np.float32)
    elif sw == 4: a = np.frombuffer(b, np.int32).astype(np.float32) / 65536
    else: raise ValueError(sw)
    if ch > 1: a = a.reshape(-1, ch).mean(1)
    return a, sr
def wr(fn, a, sr):
    with wave.open(fn, 'wb') as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes(np.clip(a, -32768, 32767).astype(np.int16).tobytes())
def trim(a, sr):   # 앞뒤 무음만 자른다(줄 사이 간격을 후보마다 같게)
    m, win = lfvoice.loud_mask(a, sr, th=300)
    if not m.any(): return a
    i = np.where(m)[0]; return a[max(0, i[0] * win - int(sr * 0.03)): min(len(a), (i[-1] + 1) * win + int(sr * 0.05))]
def norm(a):   # f0의 1500 문턱이 후보 음량에 좌우되지 않게 줄마다 RMS −20dBFS로 맞춘다(제미나이도 같은 처리)
    r = np.sqrt(np.mean(a ** 2)) + 1e-6; return np.clip(a * (3277 / r), -32767, 32767)

def gemini():
    L = json.load(open(os.path.join(HERE, 'lines.json'), encoding='utf-8')); d = os.path.join(OUT, 'gemini', 'run1'); os.makedirs(d, exist_ok=True)
    for i, l in enumerate(L):
        a, sr = load(os.path.join(lfvoice.PUB, l['gemini'])); wr(os.path.join(d, f'{i:02d}.wav'), a, sr)
    print('gemini', len(L), '줄')

def run_stats(d, L):
    f, rate, dur, segs, sr0 = [], [], 0.0, [], None
    for i, l in enumerate(L):
        a, sr = load(os.path.join(d, f'{i:02d}.wav')); a = trim(a, sr); sr0 = sr
        f.append(lfvoice.f0(norm(a), sr)); sp = lfvoice.speech_sec(norm(a), sr)
        rate.append(lfvoice.syl(l['say']) / max(sp, 0.1)); dur += len(a) / sr + GAP; segs.append(a)
    f = np.array(f); fm = float(np.median(f)); h = len(f) // 2
    return {'f0': [round(float(x), 1) for x in f], 'fm': round(fm, 1), 'iqr': round(float((np.percentile(f, 75) - np.percentile(f, 25)) / fm), 3),
            'drift': round(float(np.mean(f[h:]) / np.mean(f[:h]) - 1), 3), 'line_rate_med': round(float(np.median(rate)), 2),
            'whole_rate': round(sum(lfvoice.syl(l['say']) for l in L) / dur, 2), 'sec': round(dur, 1)}, segs, sr0

def measure(c):
    L = json.load(open(os.path.join(HERE, 'lines.json'), encoding='utf-8')); res = {}
    for run in sorted(glob.glob(os.path.join(OUT, c, 'run*'))):
        st, segs, sr = run_stats(run, L); res[os.path.basename(run)] = st
        if os.path.basename(run) == 'run1':
            gap = np.zeros(int(sr * GAP), np.float32); wav = np.concatenate([x for s in segs for x in (s, gap)])
            wav = wav * (0.89 * 32767 / max(1, np.abs(wav).max()))   # 들어 보기 편하게 피크만 맞춤
            wr(os.path.join(SAMP, f'{c}.wav'), wav, sr)
    if 'run2' in res:
        a, b = np.array(res['run1']['f0']), np.array(res['run2']['f0'])
        res['repro'] = {'line_abs_med': round(float(np.median(np.abs(b / a - 1))), 3), 'line_abs_max': round(float(np.max(np.abs(b / a - 1))), 3),
                        'median_diff': round(res['run2']['fm'] / res['run1']['fm'] - 1, 3)}
    meta = os.path.join(OUT, c, 'meta.json')
    if os.path.exists(meta): res['meta'] = json.load(open(meta, encoding='utf-8'))
    json.dump(res, open(os.path.join(OUT, c, 'stats.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    r = res['run1']; print(f"{c}: 중앙 {r['fm']}Hz · IQR/중앙 {r['iqr']} · 앞뒤 {r['drift']:+.1%} · 편 {r['whole_rate']}음절/초 · 줄 중앙 {r['line_rate_med']} · {r['sec']}초")
    print('  줄 f0', r['f0'])
    if 'repro' in res: print('  재현성', res['repro'], '| run2 IQR', res['run2']['iqr'], '앞뒤', res['run2']['drift'])

def hear(c):
    L = json.load(open(os.path.join(HERE, 'lines.json'), encoding='utf-8')); d = os.path.join(OUT, c, 'run1'); out = []; errs = 0; tot = 0
    hg = lambda x: re.sub(r'[^가-힣]', '', kor(x or ''))
    for i, l in enumerate(L):
        a, sr = load(os.path.join(d, f'{i:02d}.wav')); buf = io.BytesIO(); wr_buf = wave.open(buf, 'wb')
        wr_buf.setnchannels(1); wr_buf.setsampwidth(2); wr_buf.setframerate(sr); wr_buf.writeframes(np.clip(a, -32768, 32767).astype(np.int16).tobytes()); wr_buf.close()
        body = {'contents': [{'parts': [{'inlineData': {'mimeType': 'audio/wav', 'data': base64.b64encode(buf.getvalue()).decode()}},
                 {'text': 'Transcribe this Korean audio verbatim, exactly as pronounced (do not correct mistakes). Write numbers as Korean words. Output only the transcript.'}]}], 'generationConfig': {'temperature': 0}}
        got = None
        for mdl in ['gemini-3.5-flash-lite', 'gemini-flash-lite-latest']:   # 모든 후보 같은 받아쓰기 모델(3.5-flash는 429)
            try:
                r = json.load(urllib.request.urlopen(urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/{mdl}:generateContent?key={lfvoice.key()}",
                    data=json.dumps(body).encode(), headers={'Content-Type': 'application/json'}), timeout=120))
                got = r['candidates'][0]['content']['parts'][0].get('text', '').strip(); break
            except urllib.error.HTTPError as e: print('  ', mdl, e.code)
            except Exception as e: print('  ', mdl, str(e)[:60])
        if got is None: print('받아쓰기 실패 — 확인 안 함'); return
        want, heard = hg(l['say']), hg(got)
        ops = [op for op in difflib.SequenceMatcher(None, want, heard, autojunk=False).get_opcodes() if op[0] != 'equal']
        e = sum(max(i2 - i1, j2 - j1) for _, i1, i2, j1, j2 in ops); errs += e; tot += len(want)
        out.append({'i': i, 'want': l['say'], 'heard': got, 'err_chars': e, 'diff': [(want[i1:i2], heard[j1:j2]) for _, i1, i2, j1, j2 in ops]})
        print(f'  {i:02d} 틀린 글자 {e} | {got[:50]}', [(want[i1:i2], heard[j1:j2]) for _, i1, i2, j1, j2 in ops][:5]); time.sleep(1)
    lines_bad = sum(1 for o in out if o['err_chars'])
    json.dump({'err_chars': errs, 'chars': tot, 'cer': round(errs / tot, 3), 'lines_bad': lines_bad, 'lines': out}, open(os.path.join(OUT, c, 'hear.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f'{c}: 틀린 글자 {errs}/{tot} (CER {errs / tot:.1%}) · 틀린 줄 {lines_bad}/12')

if __name__ == '__main__':
    cmd = sys.argv[1]
    {'lines': lines, 'gemini': gemini}.get(cmd, lambda: None)() if cmd in ('lines', 'gemini') else {'measure': measure, 'hear': hear}[cmd](sys.argv[2])
