# 롱폼 목소리 — RULES.md '목소리 고정·말 속도' 규칙 1~3을 코드로 지킨다(ep/A-1/voice.py의 후속, A-1에서 난 사고 세 가지를 막는다).
#   py -3.12 work/lfvoice.py plan  <ep폴더> [--maxreq 9]   # 요청 묶음만 보여 준다(API 안 부름)
#   py -3.12 work/lfvoice.py make  <ep폴더> [--maxreq 9]   # 없는 문장만 만든다 → 자르기 → 느린 문장 atempo → voice.json
#   py -3.12 work/lfvoice.py check <ep폴더>                 # 편 전체 말 속도·음높이 일관성 검사(공개 전 필수, 규칙 3)
#   py -3.12 work/lfvoice.py cutat <ep폴더> <묶음번호> 6.7,19.0,...  # 자르기 실패 묶음을 받아쓰기로 확인한 문장 시작 시각으로 자른다(API 안 부름)
#   py -3.12 work/lfvoice.py fixcut <ep폴더> <묶음번호> [--dry]  # 조각마다 받아써서 대본 문장에 맞춰 자른다(지시문 읽은 앞머리 버림) — 공개 전 받아쓰기 대조에서 어긋나면
#   py -3.12 work/lfvoice.py readback <ep폴더> [3:6,12:0]  # 공개 전 필수: 문장마다 받아써 숫자 대조·지시문 앞머리 의심 찾기(lessons 9)
# 규칙 1: 모델·목소리는 ep/tts.json에 처음 한 번 적고 잠근다. 429여도 다른 모델로 넘어가지 않고 멈춘다(다음 날 같은 모델로 이어서).
# 규칙 2(10/3 22시 사장님 "목소리 속도는 일정하게"로 바뀜): 빠르기는 늘 1.0 — atempo로 늘이거나 줄이지 않는다. 장면 길이가 목소리 길이를 따라간다.
# 규칙 4(10/3 22시 '목소리 한결같음'): 문장 f0가 편 중앙값 ±12% 밖이면 다시 녹음 · 한 편은 한 날에 녹음(문장마다 rec 날짜, 날짜 둘 이상이면 check 막힘 — 이어 붙이기 금지).
#         편 전체(대본 음절 ÷ 내레이션 길이) 5.5 이상이어야 check 통과. .slow 통과 없음.
# 무료 등급은 모델당 하루 10회라 장 여러 개를 한 요청에 묶는다(기본 9회 이하). 받은 소리는 _raw/에 먼저 저장해 다시 요청하지 않는다.
import sys, os, re, json, glob, time, base64, wave, hashlib, subprocess, urllib.request, urllib.error
import numpy as np
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
PUB = os.path.join(HERE, 'video', 'public')
SR, FPS, GAP_F, SEC_F = 24000, 30, 8, 18      # 문장 사이 8프레임(0.27초), 장 끝 18프레임 — A-1(12·24)보다 짧게
DEFAULT = {'model': 'gemini-3.8-flash-tts', 'voice': 'Charon'}
PROMPT = 'Read these Korean lines in order as an energetic, brisk YouTube finance narration. Keep a quick pace. Pause briefly between lines:\n'
SAY = [('S&P500', '에스앤피 500'), ('JEPQ', '제피큐'), ('JEPI', '제피'), ('SCHD', '슈드'), ('QQQ', '큐큐큐'), ('SPY', '에스피와이'),
       ('KODEX', '코덱스'), ('ETF', '이티에프'), ('ISA', '아이에스에이'), ('HBM', '에이치비엠'), ('DRAM', '디램'), ('NAND', '낸드'),
       ('SEC', '에스이씨'), ('8-K', '에잇케이'), ('10-K', '텐케이'), ('Form 4', '폼 포'), ('DART', '다트'), ('AI', '에이아이'),
       ('%포인트', '퍼센트포인트'), ('%p', '퍼센트포인트')]
syl = lambda t: len(re.findall('[가-힣0-9]', t))

def nkr(n):   # 정수를 한국어로 읽을 때 음절 수(만 단위, '일십·일백·일천'의 '일'은 읽지 않음)
    if n == 0: return 1
    c, u = 0, 0
    while n:
        g = n % 10000
        if g:
            for d, k in ((g // 1000, 1), (g // 100 % 10, 1), (g // 10 % 10, 1), (g % 10, 0)):
                if d: c += (0 if (d == 1 and k) else 1) + k
            if u: c += 1
        n //= 10000; u += 1
    return c
def est(t):   # 자르기용 음절 어림: 숫자는 읽는 길이로, %는 '퍼센트'
    t = re.sub(r'(\d[\d,]*)(?:\.(\d+))?', lambda m: '가' * (nkr(int(m.group(1).replace(',', ''))) + (1 + len(m.group(2)) if m.group(2) else 0)), t)
    return len(re.findall('[가-힣A-Za-z]', t.replace('%', '가가가')))

def ffmpeg():
    import imageio_ffmpeg; return imageio_ffmpeg.get_ffmpeg_exe()

def key():
    return [l.split('=', 1)[-1].strip() for l in open(r'C:\Users\강영준\Documents\gemini_key.txt', encoding='utf-8-sig') if l.strip()][0]

def lock(ep):
    fn = os.path.join(ep, 'tts.json')
    if not os.path.exists(fn): json.dump(DEFAULT, open(fn, 'w', encoding='utf-8'), ensure_ascii=False)
    return json.load(open(fn, encoding='utf-8'))

def speak(ep, t):
    extra = os.path.join(ep, 'say.json')
    pairs = (json.load(open(extra, encoding='utf-8')) if os.path.exists(extra) else []) + SAY
    for a, b in sorted(pairs, key=lambda p: -len(p[0])): t = t.replace(a, b)
    return t

def sections(ep):
    body = open(os.path.join(ep, 'script.md'), encoding='utf-8').read().split('\n---', 1)[0]
    out, cur = [], None
    for line in body.splitlines():
        if line.startswith('## '): cur = {'title': line[3:].strip(), 'lines': []}; out.append(cur)
        elif line.lstrip().startswith('- ') and cur is not None:
            t = re.sub(r'\s*\(화면.*$', '', line.strip()[2:]).strip()
            if t: cur['lines'].append(t)
    return out

def aud_dir(ep):
    d = os.path.join(PUB, 'audio', os.path.basename(os.path.normpath(ep)).lower()); os.makedirs(os.path.join(d, '_raw'), exist_ok=True); return d
def wav_of(ep, cfg, say):
    h = hashlib.md5((cfg['model'] + '|' + cfg['voice'] + '|' + say).encode()).hexdigest()[:16]
    return h, os.path.join(aud_dir(ep), h + '.wav')

def read(fn):
    with wave.open(fn) as w: return np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32), w.getframerate()
def write(fn, a, sr=SR):
    # 10/02 사장님 "말 끝나고 치직": TTS 응답 끝에 붙는 0.12초 잡음을 지우고 DC 제거·앞뒤 페이드(work/video/clickscan.py)
    sys.path.insert(0, os.path.join(HERE, 'video')); import clickscan
    a = clickscan.clean(np.asarray(a, dtype=np.float32), sr)
    with wave.open(fn, 'wb') as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes(np.clip(a, -32768, 32767).astype(np.int16).tobytes())

def loud_mask(a, sr, win_s=0.02, th=600):
    win = int(sr * win_s); n = len(a) // win
    return np.abs(a[:n * win]).reshape(n, win).max(1) > th, win

def speech_sec(a, sr):
    # 0.6초 넘는 쉼과 앞뒤 무음을 뺀 길이(경쟁 실측 '말만' 속도와 같은 잣대)
    m, win = loud_mask(a, sr)
    if not m.any(): return 0.0
    idx = np.where(m)[0]; m = m[idx[0]:idx[-1] + 1]; t, run = 0, 0
    for v in m:
        if v: t += 1 + (run if run * 0.02 <= 0.6 else 0); run = 0
        else: run += 1
    return t * win / sr

def f0(a, sr):
    # 40ms 틀 자기상관으로 70~300Hz 중앙값(목소리 바뀜 감지용 — 절대값보다 편 안 비교가 목적)
    fr, hop, out = int(sr * 0.04), int(sr * 0.02), []
    lo, hi = sr // 300, sr // 70
    for i in range(0, len(a) - fr, hop):
        x = a[i:i + fr]
        if np.abs(x).max() < 1500: continue
        x = x - x.mean(); c = np.correlate(x, x, 'full')[fr - 1:]
        if c[0] <= 0: continue
        k = lo + int(np.argmax(c[lo:hi]));
        if c[k] / c[0] > 0.45: out.append(sr / k)
    return float(np.median(out)) if out else 0.0

def cut(pcm, texts):
    # 무음 후보 가운데 글자 수 누적 비율에 가장 가까운 자리를 순서대로 고른다(ep/A-1/voice.py split_dp와 같은 생각).
    for mingap in (8, 5, 3):
        m, win = loud_mask(pcm, SR)
        cand, i = [], 0
        while i < len(m):
            if not m[i]:
                j = i
                while j < len(m) and not m[j]: j += 1
                if i > 0 and j < len(m) and j - i >= mingap: cand.append(((i + j) // 2 * win, j - i))
                i = j
            else: i += 1
        need, tl = len(texts) - 1, len(pcm)
        if need == 0: return [pcm]
        if len(cand) < need: continue
        s = [est(t) for t in texts]; ts = sum(s); tgt = [sum(s[:k + 1]) / ts * tl for k in range(need)]
        n, INF = len(cand), float('inf')
        cost = lambda k, c: abs(cand[c][0] - tgt[k]) / tl - 0.002 * cand[c][1]
        best = [[INF] * n for _ in range(need)]; prev = [[-1] * n for _ in range(need)]
        for c in range(n): best[0][c] = cost(0, c)
        for k in range(1, need):
            run, arg = INF, -1
            for c in range(n):
                if c > 0 and best[k - 1][c - 1] < run: run, arg = best[k - 1][c - 1], c - 1
                if arg >= 0: best[k][c] = run + cost(k, c); prev[k][c] = arg
        c = min(range(n), key=lambda x: best[need - 1][x])
        if best[need - 1][c] == INF: continue
        cuts = []
        for k in range(need - 1, -1, -1): cuts.append(cand[c][0]); c = prev[k][c]
        cuts = sorted(cuts); segs = [pcm[a:b] for a, b in zip([0] + cuts, cuts + [tl])]
        if all(0.6 <= (len(g) / tl) / (x / ts) <= 1.6 for g, x in zip(segs, s)): return segs
    return None

ALIGN_MODELS = ['gemini-3.8-flash', 'gemini-3.7-flash', 'gemini-3.6-flash', 'gemini-3.5-flash', 'gemini-flash-latest']   # 받아쓰기·시각 맞추기용(목소리 모델 아님 — 규칙 1과 무관)
def align(pcm, texts):
    # cut()이 실패하면(숫자 많은 문장은 음절 비율이 어긋남) 받아쓰기(문장마다 [초] 표시)로 대본 문장 시작 시각을 찾고,
    # 0.4초 넘는 쉼 가운데 그 시각에 가장 가까운 것들을 순서대로(DP) 고른다. 모델 시각은 1~2초 틀릴 수 있어 '긴 쉼'만 후보로 둔다.
    # 10/1 E-1: 모델에게 시각만 받아 가장 가까운 무음에 붙였더니 한 문장씩 밀린 파일이 나왔다(받아쓰기 대조로 발견) → 이 방식으로 바꿈.
    import io, difflib
    buf = io.BytesIO()
    with wave.open(buf, 'wb') as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(np.clip(pcm, -32768, 32767).astype(np.int16).tobytes())
    body = {'contents': [{'parts': [{'inlineData': {'mimeType': 'audio/wav', 'data': base64.b64encode(buf.getvalue()).decode()}},
             {'text': 'Transcribe this Korean audio verbatim, one sentence per line, each line starting with its start time in seconds like [12.3].'}]}],
            'generationConfig': {'temperature': 0}}
    txt = None
    for tries in range(3):
        for m in ALIGN_MODELS:
            try:
                r = json.load(urllib.request.urlopen(urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={key()}",
                    data=json.dumps(body).encode(), headers={'Content-Type': 'application/json'}), timeout=300))
                txt = r['candidates'][0]['content']['parts'][0]['text']; break
            except Exception as e: print('  받아쓰기 실패', m, str(e)[:40])
        if txt: break
        time.sleep(20)
    if not txt: return None
    heard = []
    for ln in txt.splitlines():
        mm = re.match(r'\s*\[(?:(\d+):)?(\d+(?:\.\d+)?)\]\s*(.*)', ln)
        if mm: heard.append(((int(mm.group(1)) * 60 if mm.group(1) else 0) + float(mm.group(2)), re.sub('[^가-힣0-9]', '', mm.group(3))))
    key8 = lambda t: re.sub('[^가-힣0-9]', '', t)[:10]
    starts, j = [], 0
    for t in texts[1:]:                       # 대본 문장 첫머리와 가장 닮은 받아쓰기 줄(순서 유지)
        best = max(range(j, len(heard)), key=lambda k: difflib.SequenceMatcher(None, key8(t), heard[k][1][:10]).ratio(), default=None)
        if best is None or difflib.SequenceMatcher(None, key8(t), heard[best][1][:10]).ratio() < 0.5: print('  받아쓰기에서 못 찾음:', t[:20]); return None
        starts.append(heard[best][0] * SR); j = best + 1
    m, win = loud_mask(pcm, SR); gaps, i = [], 0
    while i < len(m):
        if not m[i]:
            k = i
            while k < len(m) and not m[k]: k += 1
            if i > 0 and k < len(m) and (k - i) * win / SR >= 0.4: gaps.append((i + k) // 2 * win)
            i = k
        else: i += 1
    n, need, INF = len(gaps), len(starts), float('inf')
    if n < need: return None
    best = [[INF] * n for _ in range(need)]; prev = [[-1] * n for _ in range(need)]
    for c in range(n): best[0][c] = abs(gaps[c] - starts[0])
    for k in range(1, need):
        run, arg = INF, -1
        for c in range(n):
            if c > 0 and best[k - 1][c - 1] < run: run, arg = best[k - 1][c - 1], c - 1
            if arg >= 0: best[k][c] = run + abs(gaps[c] - starts[k]); prev[k][c] = arg
    c = min(range(n), key=lambda x: best[need - 1][x])
    if best[need - 1][c] == INF: return None
    cuts = []
    for k in range(need - 1, -1, -1): cuts.append(gaps[c]); c = prev[k][c]
    cuts = sorted(cuts)
    if max(abs(a - b) for a, b in zip(cuts, starts)) > 2.0 * SR: print('  받아쓰기 시각과 쉼이 2초 넘게 어긋남'); return None
    segs = [pcm[a:b] for a, b in zip([0] + cuts, cuts + [len(pcm)])]
    rates = [est(t) / (len(g) / SR) for t, g in zip(texts, segs)]
    if not all(3.5 <= r <= 9.5 for r in rates): print('  자른 문장 속도 이상', [round(r, 1) for r in rates]); return None
    return segs

def tempo(fn, rate):
    # 규칙 2(10/3 22시부터): 빠르기 고정 — 늘 1.0. 아래 atempo는 옛 편 기록용으로만 남김.
    if True or rate >= 5.6: return 1.0
    f = min(1.25, 6.8 / max(rate, 0.1)); tmp = fn + '.tmp.wav'
    subprocess.run([ffmpeg(), '-y', '-loglevel', 'error', '-i', fn, '-filter:a', f'atempo={f:.3f}', '-ar', str(SR), '-ac', '1', tmp], check=True)
    os.replace(tmp, fn); return round(f, 3)

def pack(secs, maxreq):
    # 장 순서를 지키며 음절이 고르게 maxreq 묶음 이하로 나눈다
    tot = sum(syl(t) for s in secs for t in s['lines']); per = tot / maxreq; groups, cur, acc = [], [], 0
    for s in secs:
        if not s['lines']: continue
        n = sum(syl(t) for t in s['lines'])
        if cur and acc + n > per * 1.15 and len(groups) < maxreq - 1: groups.append(cur); cur, acc = [], 0
        cur.append(s); acc += n
    if cur: groups.append(cur)
    return groups

def request(cfg, texts):
    body = {'contents': [{'parts': [{'text': PROMPT + '\n'.join(texts)}]}],
            'generationConfig': {'responseModalities': ['AUDIO'], 'speechConfig': {'voiceConfig': {'prebuiltVoiceConfig': {'voiceName': cfg['voice']}}}}}
    r = json.load(urllib.request.urlopen(urllib.request.Request(
        f"https://generativelanguage.googleapis.com/v1beta/models/{cfg['model']}:generateContent?key={key()}",
        data=json.dumps(body).encode(), headers={'Content-Type': 'application/json'}), timeout=600))
    return np.frombuffer(base64.b64decode(r['candidates'][0]['content']['parts'][0]['inlineData']['data']), dtype=np.int16).astype(np.float32)

def make(ep, maxreq, dry=False):
    secs = sections(ep); holes = [t for s in secs for t in s['lines'] if '{{' in t or '○' in t]
    if holes: print(f'대본 빈자리 {len(holes)}곳(예: {holes[0][:30]})')
    if holes and not dry: sys.exit('빈자리를 채운 뒤 만든다')
    cfg = lock(ep); groups = pack(secs, maxreq)
    print(f"모델 {cfg['model']} · 목소리 {cfg['voice']} · 장 {sum(1 for s in secs if s['lines'])}개 → 요청 {len(groups)}회")
    for g in groups: print('  ', ' + '.join(s['title'][:14] for s in g), sum(syl(t) for s in g for t in s['lines']), '음절')
    if dry: return
    pad = np.zeros(int(SR * 0.08), dtype=np.float32); stopped = None
    for g in groups:
        texts = [speak(ep, t) for s in g for t in s['lines']]; todo = [t for t in texts if not os.path.exists(wav_of(ep, cfg, t)[1])]
        if not todo or stopped: continue
        rk = hashlib.md5(('|'.join([cfg['model'], cfg['voice']] + todo)).encode()).hexdigest()[:16]; raw = os.path.join(aud_dir(ep), '_raw', rk + '.pcm')
        if os.path.exists(raw): pcm = np.fromfile(raw, dtype=np.int16).astype(np.float32)
        else:
            try: pcm = request(cfg, todo); pcm.astype(np.int16).tofile(raw)
            except urllib.error.HTTPError as e:
                msg = e.read().decode(errors='ignore'); stopped = f"{e.code} {'하루 할당량' if 'PerDay' in msg else msg[:120]}"
                print('  멈춤 —', stopped, '(규칙 1: 다른 모델로 넘어가지 않음)'); continue
        segs = cut(pcm, todo) or align(pcm, todo)
        if segs is None: print('  자르기 실패(저장본 있음, 다시 요청 안 함):', todo[0][:20]); continue
        for t, sg in zip(todo, segs): write(wav_of(ep, cfg, t)[1], np.concatenate([pad, sg, pad]))
        print('  묶음 완료', len(todo), '문장')
        if est(todo[0]) / (len(segs[0]) / SR) < 3.6: print('  ⚠ 첫 문장이 대본보다 훨씬 김 — TTS가 지시문을 읽었을 수 있음 → readback 뒤 fixcut')
    build(ep)

def build(ep):
    cfg, secs = lock(ep), sections(ep); done = miss = 0
    for s in secs:
        out = []
        for t in s['lines']:
            say = speak(ep, t); h, fn = wav_of(ep, cfg, say); rec = {'text': t, 'say': say, 'audio': None}
            if os.path.exists(fn):
                a, sr = read(fn); sp = speech_sec(a, sr); r = syl(say) / max(sp, 0.1)
                meta = fn + '.json'; info = json.load(open(meta)) if os.path.exists(meta) else {}
                if 'tempo' not in info: info = {'tempo': tempo(fn, r), 'rate_raw': round(r, 2)}
                if 'rec' not in info: info['rec'] = time.strftime('%Y-%m-%d', time.localtime(os.path.getmtime(fn)))   # 녹음 날(규칙 4)
                json.dump(info, open(meta, 'w'))
                a, sr = read(fn); sec = len(a) / sr; sp = speech_sec(a, sr)
                rec.update({'audio': f"audio/{os.path.basename(aud_dir(ep))}/{h}.wav", 'sec': round(sec, 2), 'frames': int(sec * FPS + 0.999) + GAP_F,
                            'rate': round(syl(say) / max(sp, 0.1), 2), 'tempo': info['tempo'], 'rec': info['rec'], 'f0': round(f0(a, sr), 1)}); done += 1
            else: miss += 1
            out.append(rec)
        s['lines'] = out; s['frames'] = sum(l.get('frames', 0) for l in out) + (SEC_F if out else 0)
    tot = sum(s['frames'] for s in secs) / FPS; tsyl = sum(syl(l['say']) for s in secs for l in s['lines'])
    res = {'model': cfg['model'], 'voice': cfg['voice'], 'fps': FPS, 'sections': secs, 'done': done, 'missing': miss,
           'seconds': round(tot, 1), 'rate_total': round(tsyl / max(tot, 0.1), 2) if not miss else None}
    json.dump(res, open(os.path.join(ep, 'voice.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f"문장 {done} 완료 · 남음 {miss} · 길이 {tot/60:.1f}분 · 편 전체 {res['rate_total']} 음절/초")

def check(ep, vj=None):
    # 규칙 3·4: 문장별 음높이 ±12%(10/3 22시, 전엔 ±20%)·속도 4.8 미만·8.2 초과(빠르기 고정이라 하한을 낮춤, 편 전체 5.5는 그대로)·빠르기 1.0 아님·녹음 날 둘 이상이면 막힘.
    d = json.load(open(vj or os.path.join(ep, 'voice.json'), encoding='utf-8')); rows = []
    for s in d['sections']:
        for l in s['lines']:
            if not l.get('audio'): continue
            a, sr = read(os.path.join(PUB, l['audio'])); sp = speech_sec(a, sr)
            rows.append((s['title'][:12], l['text'][:24], syl(l.get('say', l['text'])) / max(sp, 0.1), f0(a, sr), len(a) / sr, l.get('tempo') or 1.0))
    if not rows: sys.exit('소리 없음')
    fm = float(np.median([r[3] for r in rows if r[3]])); bad = []
    for t, x, r, p, _, tp in rows:
        why = [w for w, c in (('음높이', p and abs(p / fm - 1) > 0.12), ('느림', r < 4.8), ('빠름', r > 8.2), (f'빠르기{tp}', tp != 1.0)) if c]
        if why: bad.append(f'{t} | {x} | {r:.2f}음절/초 · {p:.0f}Hz | ' + '·'.join(why))
    tot = sum(s.get('frames', 0) for s in d['sections']) / d.get('fps', FPS); tsyl = sum(syl(l.get('say', l['text'])) for s in d['sections'] for l in s['lines'])
    whole = tsyl / max(tot, 0.1); rates = [r[2] for r in rows]
    print(f'문장 {len(rows)} · 음높이 중앙 {fm:.0f}Hz · 문장 속도 중앙 {np.median(rates):.2f}(최저 {min(rates):.2f}) · 편 전체 {whole:.2f}음절/초(목표 5.5 이상)')
    print('튀는 문장', len(bad), *bad[:40], sep='\n  ')
    recs = sorted({l.get('rec') or '?' for s in d['sections'] for l in s['lines'] if l.get('audio')})
    print('녹음 날', recs, '(한 날이어야 통과 — 규칙 4)')
    ok = whole >= 5.5 and not bad and not d.get('missing') and len(recs) == 1 and '?' not in recs
    print('통과' if ok else '막힘'); return ok

def cutat(ep, gi, times, maxreq=9):
    # 받아쓰기로 확인한 문장 시작 시각으로 저장본을 자른다: 시각마다 0.3초 넘는 가장 가까운 쉼(0.8초 안)에 붙인다. API 안 부름.
    cfg = lock(ep); g = pack(sections(ep), maxreq)[gi]
    texts = [speak(ep, t) for s in g for t in s['lines']]; todo = [t for t in texts if not os.path.exists(wav_of(ep, cfg, t)[1])]
    rk = hashlib.md5(('|'.join([cfg['model'], cfg['voice']] + todo)).encode()).hexdigest()[:16]
    pcm = np.fromfile(os.path.join(aud_dir(ep), '_raw', rk + '.pcm'), dtype=np.int16).astype(np.float32)
    lead = None
    if len(times) == len(todo): lead, times = times[0], times[1:]      # 시각이 문장 수만큼이면 첫 값은 '여기부터 대본'(앞부분 버림 — TTS가 지시문을 읽은 경우)
    assert len(times) == len(todo) - 1, (len(times), len(todo))
    m, win = loud_mask(pcm, SR); gaps, i = [], 0
    while i < len(m):
        if not m[i]:
            k = i
            while k < len(m) and not m[k]: k += 1
            if i > 0 and k < len(m) and (k - i) * win / SR >= 0.3: gaps.append((i + k) // 2 * win)
            i = k
        else: i += 1
    cuts = []
    for t in times:
        c = min(gaps, key=lambda x: abs(x - t * SR)); assert abs(c - t * SR) <= 0.8 * SR, f'{t}초 근처에 쉼 없음'; cuts.append(c)
    assert cuts == sorted(set(cuts))
    pad = np.zeros(int(SR * 0.08), dtype=np.float32)
    st = min(gaps, key=lambda x: abs(x - lead * SR)) if lead else 0
    for t, sg in zip(todo, [pcm[a:b] for a, b in zip([st] + cuts, cuts + [len(pcm)])]): write(wav_of(ep, cfg, t)[1], np.concatenate([pad, sg, pad]))
    print('  시각으로 자름', len(todo), '문장'); build(ep)

def fixcut(ep, gi, maxreq=9, dry=False):
    # 받아쓰기 맞춤 자르기(10/1 E-1 사고 뒤 추가): 저장본을 모든 쉼(0.25초+)에서 조각내 조각마다 받아쓰고,
    # 조각을 대본 문장에 차례대로 붙여(DP, 글자 닮음 최대) 문장 파일을 만든다. 앞머리에 TTS가 읽어 버린 지시문(영어)은 버린다.
    import io, difflib
    cfg = lock(ep); g = pack(sections(ep), maxreq)[gi]
    texts = [speak(ep, t) for s in g for t in s['lines']]
    rk = hashlib.md5(('|'.join([cfg['model'], cfg['voice']] + texts)).encode()).hexdigest()[:16]
    pcm = np.fromfile(os.path.join(aud_dir(ep), '_raw', rk + '.pcm'), dtype=np.int16).astype(np.float32)
    m, win = loud_mask(pcm, SR); cuts, i = [], 0
    while i < len(m):
        if not m[i]:
            k = i
            while k < len(m) and not m[k]: k += 1
            if i > 0 and k < len(m) and (k - i) * win / SR >= 0.25: cuts.append((i + k) // 2 * win)
            i = k
        else: i += 1
    bounds = list(zip([0] + cuts, cuts + [len(pcm)]))
    cache = os.path.join(aud_dir(ep), '_raw', rk + '.chunks.json')
    heard = json.load(open(cache, encoding='utf-8')) if os.path.exists(cache) else {}
    for a, b in bounds:
        kk = f'{a}-{b}'
        if kk in heard: continue
        buf = io.BytesIO()
        with wave.open(buf, 'wb') as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm[a:b].astype(np.int16).tobytes())
        body = {'contents': [{'parts': [{'inlineData': {'mimeType': 'audio/wav', 'data': base64.b64encode(buf.getvalue()).decode()}},
                 {'text': 'Transcribe this short audio verbatim (Korean or English). Numbers as digits. Output only the transcript.'}]}], 'generationConfig': {'temperature': 0}}
        for tries in range(4):
            got = None
            for mdl in ['gemini-3.5-flash-lite', 'gemini-flash-lite-latest', 'gemini-3.1-flash-lite', 'gemini-3.5-flash']:
                try:
                    r = json.load(urllib.request.urlopen(urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/{mdl}:generateContent?key={key()}",
                        data=json.dumps(body).encode(), headers={'Content-Type': 'application/json'}), timeout=120))
                    got = r['candidates'][0]['content']['parts'][0].get('text', '').strip(); break
                except Exception: pass
            if got is not None: break
            time.sleep(15)
        if got is None: print('  조각 받아쓰기 실패 — 멈춤'); return None
        heard[kk] = got; json.dump(heard, open(cache, 'w', encoding='utf-8'), ensure_ascii=False); time.sleep(1)
    H = [heard[f'{a}-{b}'] for a, b in bounds]
    norm = lambda t: re.sub('[^가-힣0-9]', '', t)
    # 한국어 한 글자도 없는 앞머리 조각 = 지시문 → 버림(앞머리만)
    lead = 0
    PROMPTISH = re.compile(r'Read these|Keep a quick|Pause briefly|narration|brisk|in order', re.I)
    while lead < len(H) and (not re.search('[가-힣]', H[lead]) or PROMPTISH.search(H[lead])): lead += 1
    last_p = max([j for j in range(min(len(H), 6)) if PROMPTISH.search(H[j])], default=-1)
    lead = max(lead, last_p + 1)                 # 지시문이 보인 조각까지는 무조건 버린다
    C = [norm(h) for h in H]; n, L = len(C), len(texts); T = [norm(t) for t in texts]
    def sim(a, b):   # 맞은 글자 − 남는 글자 절반(쓰레기 조각을 붙이면 손해)
        M = sum(x.size for x in difflib.SequenceMatcher(None, a, b, autojunk=False).get_matching_blocks()); return M - 0.5 * (len(a) - M) - 0.5 * (len(b) - M)
    NEG = -1e9; best = [[NEG] * (n + 1) for _ in range(L + 1)]; prv = [[-1] * (n + 1) for _ in range(L + 1)]
    for s0 in range(lead, min(n, lead + 5)): best[0][s0] = -0.5 * (s0 - lead)   # 앞머리 조각 더 버리기 허용(지시문을 한국어로 잘못 받아쓴 경우)
    for li in range(1, L + 1):
        for e in range(lead + 1, n + 1):
            for s0 in range(max(lead, e - 12), e):
                if best[li - 1][s0] == NEG: continue
                v = best[li - 1][s0] + sim(''.join(C[s0:e]), T[li - 1])
                if v > best[li][e]: best[li][e], prv[li][e] = v, s0
    if best[L][n] == NEG: print('  맞춤 실패'); return None
    seg, e = [], n
    for li in range(L, 0, -1): s0 = prv[li][e]; seg.append((s0, e)); e = s0
    seg.reverse(); ok = True; lead = seg[0][0]
    for (s0, e), t, tt in zip(seg, texts, T):
        got = ''.join(C[s0:e]); r = difflib.SequenceMatcher(None, got, tt).ratio()
        flag = '' if r >= 0.75 else '  <<< 낮음'
        if r < 0.75: ok = False
        print(f'  {r:.2f} [{bounds[s0][0] / SR:.1f}-{bounds[e - 1][1] / SR:.1f}s] {t[:24]} | 들림 {"".join(H[s0:e])[:40]}{flag}')
    if lead: print(f'  앞머리 {bounds[lead - 1][1] / SR:.1f}초 버림(지시문): {" ".join(H[:lead])[:60]}')
    if dry or not ok: return ok
    pad = np.zeros(int(SR * 0.08), dtype=np.float32)
    for (s0, e), t in zip(seg, texts):
        write(wav_of(ep, cfg, t)[1], np.concatenate([pad, pcm[bounds[s0][0]:bounds[e - 1][1]], pad]))
    print('  받아쓰기 맞춤으로 자름', L, '문장'); build(ep); return True

_ONES = {'하나': 1, '한': 1, '둘': 2, '두': 2, '셋': 3, '세': 3, '넷': 4, '네': 4, '다섯': 5, '여섯': 6, '일곱': 7, '여덟': 8, '아홉': 9}
_TENS = {'열': 10, '스무': 20, '스물': 20, '서른': 30, '마흔': 40, '쉰': 50}
_SINO = {c: i for i, c in enumerate('영일이삼사오육칠팔구')}
def _sino(w):   # '사백구십' → 490 (만 아래만 — 만·억·조는 아래 단위 정규화가 맡는다)
    tot, cur = 0, 0
    for c in w:
        if c in _SINO: cur = _SINO[c]
        else: tot += (cur or 1) * {'십': 10, '백': 100, '천': 1000}[c]; cur = 0
    return tot + cur
def readback_num(t, words=False):
    # 대본·받아쓰기 숫자를 같은 꼴로: 쉼표 빼기, '5천7백'→5700, '8만 4,200'→84200·'27만 5천'→275000('만' 정규화, 2026-10-01 ai-lab 요청 — 거짓 경보였다).
    # words=True(받아쓰기 쪽만): 한글 숫자→아라비아. 받아쓰기 전용 모델은 '여덟 분기'처럼 들리는 대로 쓴다. 대본 쪽엔 쓰지 않는다
    # (대본 '세 회사'를 3으로 바꾸면 lite가 '새 회사'로 들은 걸 숫자 틀림으로 잡는다 — 대본에 아라비아로 쓴 숫자만 대조한다).
    t = t.replace(',', '')
    if words:
        t = re.sub(r'(?<![가-힣0-9])(?=[열스서마쉰한하두둘세셋네넷다여일아])(열|스무|스물|서른|마흔|쉰)?(하나|한|둘|두|셋|세|넷|네|다섯|여섯|일곱|여덟|아홉)?(?=\s?(?:분기|달|개|명|번|배|해|살|가지|곳|주|차례))',
                   lambda m: str(_TENS.get(m.group(1), 0) + _ONES.get(m.group(2), 0)) if (m.group(1) or m.group(2)) else m.group(0), t)
        t = re.sub(r'(?<![가-힣0-9])([일이삼사오육칠팔구]?[십백천](?:[일이삼사오육칠팔구]?[십백천])*[일이삼사오육칠팔구]?)(?=\s?(?:만|억|조|원|배|%|퍼센트|분기|달|년|월|일|주))',
                   lambda m: str(_sino(m.group(1))), t)
    t = re.sub(r'(\d+)\s?천\s?(\d+)\s?백', lambda m: str(int(m.group(1)) * 1000 + int(m.group(2)) * 100), t)
    t = re.sub(r'(\d+)\s?천', lambda m: str(int(m.group(1)) * 1000), t)          # '9천'='9000'
    t = re.sub(r'(\d+)\s?백', lambda m: str(int(m.group(1)) * 100), t)
    t = re.sub(r'(\d+)만\s?(\d{1,4})(?!\d|\.\d|\s?[만억조%배년월일])', lambda m: str(int(m.group(1)) * 10000 + int(m.group(2))), t)
    t = re.sub(r'(\d+)만(?!\s?\d)', lambda m: str(int(m.group(1)) * 10000), t)
    return sorted(re.findall(r'\d+(?:\.\d+)?', t))

def readback(ep, only=None):
    # 공개 전 필수(lessons 9): 문장마다 받아써서 대본 숫자와 대조하고, 길이가 대본보다 훨씬 긴 문장(지시문을 읽은 앞머리 의심)을 찾는다.
    # 숫자가 다르게 들리면 다른 받아쓰기 모델 2개로 더 듣고, 셋 중 둘 이상이 대본과 다를 때만 '다시 만들 문장'으로 적는다.
    import io
    v = json.load(open(os.path.join(ep, 'voice.json'), encoding='utf-8')); out, bad = [], []
    num = readback_num
    def tx(fn, mdl):
        a, sr = read(fn); buf = io.BytesIO()
        with wave.open(buf, 'wb') as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes(a.astype(np.int16).tobytes())
        parts = [{'inlineData': {'mimeType': 'audio/wav', 'data': base64.b64encode(buf.getvalue()).decode()}}]
        if 'transcribe' not in mdl: parts.append({'text': 'Transcribe this Korean audio verbatim. Write numbers exactly as spoken using digits.'})
        body = {'contents': [{'parts': parts}], 'generationConfig': {'temperature': 0}}     # 받아쓰기 전용 모델은 지시문 없이 오디오만
        for tries in range(2 if 'transcribe' in mdl else 3):
            if 'transcribe' in mdl: time.sleep(21)      # 전용 모델 무료 한도가 작다(ai-lab 10-01 실측 429)
            try:
                r = json.load(urllib.request.urlopen(urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/{mdl}:generateContent?key={key()}",
                    data=json.dumps(body).encode(), headers={'Content-Type': 'application/json'}), timeout=120))
                p0 = r['candidates'][0]['content']['parts'][0]          # 전용 모델은 text가 아니라 audioTranscription.text로 준다
                return (p0.get('text') or p0.get('audioTranscription', {}).get('text', '')).strip()
            except Exception: time.sleep(10)
        return None
    for si, sec in enumerate(v['sections']):
        for li, l in enumerate(sec['lines']):
            if only and f'{si}:{li}' not in only: continue
            if not l.get('audio'): continue
            fn = os.path.join(PUB, l['audio'].replace('/', os.sep)); want = num(l['text'])
            h1 = tx(fn, 'gemini-3.5-flash-lite'); votes = [h1]; models = ['gemini-3.5-flash-lite']
            miss = lambda h: [x for x in want if x not in num(h, words=True)]          # 대본 숫자가 다 들렸는가(대본의 '열두 달'이 '12달'로 들리는 건 괜찮다)
            if h1 is not None and miss(h1):
                # 추가 표 2개 중 하나는 받아쓰기 전용 모델(lite 계열은 같이 흔들린다 — ai-lab/bench/2026-10-01-transcribe.md). 429면 지금처럼 lite 표.
                h2, m2 = tx(fn, 'gemini-3.5-transcribe'), 'gemini-3.5-transcribe'
                if h2 is None: h2, m2 = tx(fn, 'gemini-flash-lite-latest'), 'gemini-flash-lite-latest'
                votes += [h2, tx(fn, 'gemini-3.1-flash-lite')]; models += [m2, 'gemini-3.1-flash-lite']
            wrong = sum(1 for h in votes if h is not None and miss(h))
            slow = est(l['say']) / max(l['sec'] / (l.get('tempo') or 1), 0.1) < 3.6      # 대본보다 훨씬 김 = 지시문 앞머리 의심
            # 글자 일치율(한글만, 숫자·띄어쓰기 뺌) — 숫자만 보면 앞뒤 문장이 한 칸 밀려도 못 잡는다(10/3 PD N-1 손자르기에서 발견)
            import difflib
            hg = lambda x: re.sub(r'[^가-힣]', '', x or '')
            sim = max((difflib.SequenceMatcher(None, hg(l['say']), hg(h)).ratio() for h in votes if h), default=0)
            shift = h1 is not None and sim < 0.75
            flag = ('숫자 ' if wrong >= 2 else '') + ('길이 ' if slow else '') + (f'밀림의심({sim:.2f}) ' if shift else '') + ('받아쓰기 실패' if h1 is None else '')
            out.append({'at': f'{si}:{li}', 'text': l['text'], 'heard': votes, 'models': models, 'sim': round(sim, 2), 'flag': flag.strip()})
            if flag.strip(): bad.append(f'{si}:{li} {flag.strip()} | {l["text"][:30]} | 들림 {votes[-1] and votes[-1][:40]}')
            time.sleep(1)
    json.dump(out, open(os.path.join(ep, 'check', 'voice_readback' + ('_part' if only else '') + '.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f'받아쓰기 대조 {len(out)}문장 · 걸린 문장 {len(bad)}'); [print('  ' + b) for b in bad]
    return not bad

if __name__ == '__main__':
    cmd, ep = sys.argv[1], os.path.abspath(sys.argv[2]); mr = int(sys.argv[sys.argv.index('--maxreq') + 1]) if '--maxreq' in sys.argv else 9
    if cmd == 'readback': sys.exit(0 if readback(ep, sys.argv[3].split(',') if len(sys.argv) > 3 and not sys.argv[3].startswith('--') else None) else 1)
    elif cmd == 'fixcut': fixcut(ep, int(sys.argv[3]), mr, dry='--dry' in sys.argv)
    elif cmd == 'cutat': cutat(ep, int(sys.argv[3]), [float(x) for x in sys.argv[4].split(',')], mr)
    elif cmd == 'plan': make(ep, mr, dry=True)
    elif cmd == 'make': make(ep, mr)
    elif cmd == 'check': sys.exit(0 if check(ep, sys.argv[3] if len(sys.argv) > 3 else None) else 1)
