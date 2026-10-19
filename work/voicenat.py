# 말 자연스러움 — 어절 사이 틈·쉼을 사람 진행자 기준과 맞대 '붙음/끊김'을 찾는다(2026-10-19 사장님 "두 단어를 빠르게 붙여 말하거나 떼서 말하거나").
#   py -3.12 work/voicenat.py words <wav...>              # 어절 시각(faster-whisper word_timestamps) 뽑아 캐시에 둔다
#   py -3.12 work/voicenat.py line "<say>" <wav>           # 한 줄 판정(붙음·끊김·빠르기) — 관문은 lfvoice check(nat_gate 편)
# 사람 기준(research/longform/voice-naturalness-1019.md, 사람 진행자 12편 각 3분 실측)은 아래 HUMAN에 숫자로 둔다. 기준을 바꾸면 그 문서도 같이 고친다.
# 틈 = 소리 크기가 바닥(줄 최고 −25dB 아래, 50ms 중앙값)인 0.05초+ 구간을 Whisper 단어 시각으로 가장 가까운 어절 경계에 붙인 길이.
#   Whisper 시각만 쓰면 쉼이 다음 어절 머리에 들어가 틈이 0으로 나온다(사람 소리 첫 판 틈 중앙 0초) — 그래서 무음 구간을 따로 찾는다.
import os, re, sys, json, hashlib, wave
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.environ.get('VOICENAT_CACHE') or os.path.join(HERE, 'research', 'longform', 'voice-naturalness-1019', 'words_cache')
WSIZE = os.environ.get('VOICENAT_WHISPER', 'small')
_WM = []

def _model():
    # 10/19: 다른 작업이 CPU를 다 쓰는 때 OpenMP 스레드가 헛돌아(spin) 5초 줄 하나에 4분 넘게 걸렸다 → 기다림 PASSIVE·스레드 3·허브 확인 끔으로 17초.
    for k, val in (('OMP_WAIT_POLICY', 'PASSIVE'), ('KMP_BLOCKTIME', '0'), ('OMP_NUM_THREADS', '3'), ('HF_HUB_OFFLINE', '1')): os.environ.setdefault(k, val)
    if not _WM:
        from faster_whisper import WhisperModel
        _WM.append(WhisperModel(WSIZE, device='cpu', compute_type='int8', cpu_threads=int(os.environ['OMP_NUM_THREADS'])))
    return _WM[0]

def load(fn, sr=16000):
    # wav(어떤 표본율이든) → 16kHz float32. 다른 형식은 ffmpeg로.
    try:
        with wave.open(fn) as w:
            a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768; r = w.getframerate()
            if w.getnchannels() > 1: a = a.reshape(-1, w.getnchannels()).mean(1)
    except Exception:
        import subprocess, imageio_ffmpeg
        p = subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), '-loglevel', 'error', '-i', fn, '-ac', '1', '-ar', str(sr), '-f', 's16le', '-'], capture_output=True, check=True)
        return np.frombuffer(p.stdout, dtype=np.int16).astype(np.float32) / 32768
    if r != sr:
        n = int(len(a) * sr / r); a = np.interp(np.linspace(0, len(a) - 1, n), np.arange(len(a)), a).astype(np.float32)
    return a

def words(fn, initial=None):
    """[(글, 시작, 끝), ...] — 같은 소리면 캐시(파일 내용 md5)."""
    os.makedirs(CACHE, exist_ok=True)
    h = hashlib.md5(open(fn, 'rb').read()).hexdigest()[:16]; c = os.path.join(CACHE, f'{h}_{WSIZE}.json')
    if os.path.exists(c): return json.load(open(c, encoding='utf-8'))
    a = load(fn)
    segs, _ = _model().transcribe(a, language='ko', beam_size=int(os.environ.get('VOICENAT_BEAM', '1')), word_timestamps=True, initial_prompt=initial, condition_on_previous_text=False)
    out = [(w.word.strip(), round(w.start, 3), round(w.end, 3)) for s in segs for w in (s.words or []) if w.word.strip()]
    json.dump(out, open(c, 'w', encoding='utf-8'), ensure_ascii=False)
    return out

def words_many(fns, gap=1.2, chunk=24.0):
    """여러 줄 소리를 1.2초 무음으로 이어 붙여 한 번에 받아쓴다(짧은 줄 하나도 30초 창 하나를 쓰므로 줄마다 부르면 5배 느리다).
    어절은 시각으로 줄에 돌려준다. 결과·캐시는 words()와 같다."""
    os.makedirs(CACHE, exist_ok=True)
    res, todo = {}, []
    for fn in fns:
        h = hashlib.md5(open(fn, 'rb').read()).hexdigest()[:16]; c = os.path.join(CACHE, f'{h}_{WSIZE}.json')
        if os.path.exists(c): res[fn] = json.load(open(c, encoding='utf-8'))
        else: todo.append((fn, c))
    i = 0
    while i < len(todo):
        parts, spans, t = [], [], 0.0
        while i < len(todo) and (not parts or t < chunk):
            a = load(todo[i][0]); parts += [a, np.zeros(int(16000 * gap), np.float32)]
            spans.append((todo[i], t, t + len(a) / 16000)); t += len(a) / 16000 + gap; i += 1
        segs, _ = _model().transcribe(np.concatenate(parts), language='ko', beam_size=int(os.environ.get('VOICENAT_BEAM', '1')), word_timestamps=True, condition_on_previous_text=False)
        ws = [(w.word.strip(), w.start, w.end) for s in segs for w in (s.words or []) if w.word.strip()]
        for (fn, c), t0, t1 in spans:
            mine = [(w, round(max(0, s - t0), 3), round(min(t1, e) - t0, 3)) for w, s, e in ws if t0 - 0.3 <= (s + e) / 2 <= t1 + 0.3]
            json.dump(mine, open(c, 'w', encoding='utf-8'), ensure_ascii=False); res[fn] = mine
    return [res[fn] for fn in fns]

def env_db(a, sr=16000, hop=0.01):
    k = int(sr * hop); n = len(a) // k
    if n == 0: return np.zeros(0)
    d = 20 * np.log10(np.sqrt((a[:n * k].reshape(n, k) ** 2).mean(1)) + 1e-6)
    if len(d) >= 5: d = np.median(np.lib.stride_tricks.sliding_window_view(np.pad(d, 2, mode='edge'), 5), axis=1)
    return d

def quiet_runs(db, th, hop=0.01, minrun=0.05):
    # th 아래로 minrun초 넘게 이어진 구간들 [(시작, 끝)] — 파일 앞뒤 무음은 뺀다
    out, i, n = [], 0, len(db)
    while i < n:
        if db[i] < th:
            j = i
            while j < n and db[j] < th: j += 1
            if i > 0 and j < n and (j - i) * hop >= minrun: out.append((i * hop, j * hop))
            i = j
        else: i += 1
    return out

def assign(runs, pts, maxd=0.25, pen=None):
    # 무음 구간마다 가장 가까운 어절 경계(pts 초) 하나에 붙인다 — Whisper 단어 시각은 0.1~0.2초 틀려 창으로 찾으면 쉼을 놓친다(사람 소리 첫 판 틈 중앙 0초).
    #   단어 안 무음(파열음 막힘 0.05~0.1초)도 가까운 경계에 붙는다 — 사람·우리 같은 잣대라 비교는 공정하다.
    g = [0.0] * len(pts)
    for r0, r1 in runs:
        c = (r0 + r1) / 2; best = min(range(len(pts)), key=lambda k: abs(pts[k] - c) + (pen[k] if pen else 0) if pts[k] is not None else 9e9, default=None)
        if best is not None and pts[best] is not None and abs(pts[best] - c) <= maxd + (r1 - r0) / 2: g[best] = max(g[best], r1 - r0)
    return g

def thresh(db):
    # 10/19: Chirp 쉼 바닥은 디지털 무음이 아니라 −40~−56dB 숨소리라 '최고 −30dB'로는 쉼이 토막 났다 → −25dB + 50ms 중앙값 거르기(env_db)
    return (np.percentile(db, 95) if len(db) else 0) - 25

def gaps(ws, a, sr=16000):
    """어절 경계마다 틈(초). ws = words() 결과."""
    db = env_db(a, sr); pts = [(e1 + s2) / 2 for (_, _, e1), (_, s2, _) in zip(ws, ws[1:])]
    g = assign(quiet_runs(db, thresh(db)), pts)
    return [round(max(x, s2 - e1), 3) for x, ((_, _, e1), (_, s2, _)) in zip(g, zip(ws, ws[1:]))]

def kinds(texts):
    """어절 글 목록 → 경계마다 칸(korsay.kind, 형태소 품사). 사람 소리는 Whisper 어절·문장부호로, 우리 소리는 대본 say로."""
    sys.path.insert(0, HERE); import korsay
    toks = [re.sub(r'\s+', '', t) or '·' for t in texts]
    es = korsay.eojeols(' '.join(toks))
    if len(es) != len(toks): return ['other'] * (len(toks) - 1)
    return [korsay.kind(x, y) for x, y in zip(es, es[1:])]

SYLL = lambda t: len(re.findall('[가-힣]', t))

def _hangul_words(ws):
    # Whisper 어절(숫자는 korsay로 한글 읽기) → 글자마다 (글자, 시작, 끝, 어절 번호)
    sys.path.insert(0, HERE); import korsay
    out = []
    for k, (w, s, e) in enumerate(ws):
        h = re.sub('[^가-힣]', '', korsay.say(w))
        for i, c in enumerate(h): out.append((c, s + (e - s) * i / len(h), s + (e - s) * (i + 1) / len(h), k))
    return out

def boundaries(say, ws, a, sr=16000):
    """대본(say) 어절 경계마다 (앞 어절, 뒤 어절, 칸, 틈, 들린 글 일치율).
    대본 글자와 Whisper 글자를 맞춰(difflib) 경계 시각을 얻고, 무음 구간을 가장 가까운 경계 하나에 붙인다(assign).
    10/19 시험: 음절 수 비례로 자리를 잡는 방법은 Chirp이 쉼 앞 음절을 늘여 2~7음절씩 빗나갔다 — Whisper 쪽이 맞았다(쉼은 다음 어절 머리에 들어간다).
    들린 글 일치율 0.6 아래면 틈 None."""
    import difflib
    say = re.sub(r'\[pause[^\]]*\]', ' ', say)
    toks = [t for t in say.split() if re.search('[가-힣]', t)]
    kd = kinds(toks)
    sc, tok_of = [], []
    for j, t in enumerate(toks):
        for c in re.sub('[^가-힣]', '', t): sc.append(c); tok_of.append(j)
    hc = _hangul_words(ws)
    sm = difflib.SequenceMatcher(None, ''.join(sc), ''.join(c for c, *_ in hc), autojunk=False); ok = sm.ratio()
    m = {}
    for blk in sm.get_matching_blocks():
        for i in range(blk.size): m[blk.a + i] = blk.b + i
    db = env_db(a, sr)
    last = {j: max(i for i, x in enumerate(tok_of) if x == j) for j in set(tok_of)}
    pts = []; pen = [0.0] * max(0, len(toks) - 1)
    for j in range(len(toks) - 1):
        i1, i2 = last[j], last[j] + 1
        if i1 not in m or i2 not in m: pts.append(None); continue
        c1, c2 = hc[m[i1]], hc[m[i2]]
        pts.append((c1[2] + c2[1]) / 2); pen[j] = (0.2 if c1[3] == c2[3] else 0.0) - (0.1 if toks[j][-1] in ',.?!' else 0.0)
    # 한 Whisper 어절 안 경계('5년' 속 '오|년')는 0.2초 불리하게 — Whisper는 쉼을 다음 어절 머리에 넣어 그 안 글자 시각이 늦게 잡힌다(s1 '규칙으로' 뒤 쉼이 '오|년'으로 감)
    g = assign(quiet_runs(db, thresh(db)), pts, pen=pen)
    return [(toks[j], toks[j + 1], kd[j], (None if (pts[j] is None or ok < 0.6) else round(g[j], 3)), round(ok, 2)) for j in range(len(toks) - 1)]

def artic(say, a, sr=16000):
    # 우리 소리 말 빠르기: 대본 음절 ÷ (말 시간 − 0.25초 넘는 무음)
    say = re.sub(r'\[pause[^\]]*\]', ' ', say); db = env_db(a, sr); th = thresh(db); loud = np.where(db >= th)[0]
    if not len(loud): return 0.0
    t0, t1 = loud[0] * 0.01, (loud[-1] + 1) * 0.01
    sp = (t1 - t0) - sum(r1 - r0 for r0, r1 in quiet_runs(db, th, minrun=0.25) if t0 < r0 and r1 < t1)
    return SYLL(say) / max(sp, 0.1)

def rate(ws, a=None, pause=0.25):
    # 말 빠르기(음절/초) — 0.25초 넘는 무음은 뺀 '말하는 동안' 빠르기(사람·우리 같은 잣대). a(소리)가 없으면 Whisper 틈으로만.
    sys.path.insert(0, HERE); import korsay
    if not ws: return 0.0
    syl = sum(SYLL(korsay.say(w)) for w, _, _ in ws); t0, t1 = ws[0][1], ws[-1][2]; dur = t1 - t0
    if a is not None:
        db = env_db(a); dur -= sum(min(r1, t1) - max(r0, t0) for r0, r1 in quiet_runs(db, thresh(db), minrun=pause) if r1 > t0 and r0 < t1)
    else:
        for (_, _, e1), (_, s2, _) in zip(ws, ws[1:]):
            if s2 - e1 > pause: dur -= s2 - e1
    return syl / max(dur, 0.1)

# 사람 진행자 기준(research/longform/voice-naturalness-1019.md 표 1) — 사람 진행자 12편 각 3분, 같은 잣대(어절 경계에 붙인 무음 길이)
#   쉼표 뒤: 사람 0.12초 넘게 쉰 비율 70%(중앙 0.19초) → 0.06초도 안 쉬면 '붙음'
#   한 덩어리 안: 숫자+단위·'하는 것'(dep) 사람 0.2초 넘게 쉰 비율 5%·1% → 0.2초 넘으면 '끊김', 꾸밈말+명사(adnom) 9% → 0.3초, 그 밖 문장부호 없는 경계 → 0.4초
#   말 빠르기(0.25초 넘는 쉼 뺀 음절/초): 사람 편별 5.7~7.6 → 줄이 4.8 아래·8.8 위면 표시(줄은 짧아 흔들림이 커서 ±15% 둠)
HUMAN = {'comma_min': 0.06, 'split': {'numunit': 0.2, 'dep': 0.2, 'adnom': 0.3, 'obj': 0.4, 'other': 0.4, 'topic': 0.4, 'conn': 9}, 'rate_lo': 4.8, 'rate_hi': 8.8}

def judge(say, wav, ws=None):
    """한 줄 → {'flags': [(칸, 자리, 값)], 'b': boundaries, 'rate': 음절/초}. 칸: 붙음(쉼표인데 안 쉼)·끊김(한 덩어리 안 긴 쉼)·빠르기."""
    ws = ws if ws is not None else words(wav)
    a = load(wav); b = boundaries(say, ws, a); r = artic(say, a); H = HUMAN; flags = []
    for w1, w2, kd, g, ok in b:
        if g is None: continue
        if kd == 'comma' and g < H['comma_min']: flags.append(('붙음', f'{w1} {w2}', g))
        elif kd in H['split'] and g > H['split'][kd]: flags.append(('끊김', f'{w1} / {w2}', g))
    if r and SYLL(re.sub(r'\[pause[^\]]*\]', '', say)) >= 12 and not H['rate_lo'] <= r <= H['rate_hi']: flags.append(('빠르기', f'{r:.1f}음절/초', round(r, 2)))   # 12음절 아래 짧은 줄은 빠르기 잣대가 흔들려 안 본다
    return {'flags': flags, 'b': b, 'rate': round(r, 2), 'ok': b[0][4] if b else None}

def check_lines(items, cache=None):
    """items = [(이름, say, wav)] → (걸린 줄 [(이름, say, flags)], 전체 줄 수). Whisper는 줄을 묶어 한 번에(words_many)."""
    global CACHE
    if cache: CACHE = cache
    W = words_many([w for _, _, w in items]); bad = []
    for (nm, say, wav), ws in zip(items, W):
        j = judge(say, wav, ws)
        if j['flags']: bad.append((nm, say, j['flags']))
    return bad, len(items)

if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    if sys.argv[1] == 'words':
        for fn in sys.argv[2:]:
            ws = words(fn); print(fn, len(ws), ' '.join(w for w, _, _ in ws[:20]))
    elif sys.argv[1] == 'line':
        j = judge(sys.argv[2], sys.argv[3])
        print('빠르기', j['rate'], '| 걸림', j['flags'] or '없음')
        print(' '.join(f'{w1}|{g}' for w1, w2, kd, g, ok in j['b']))
