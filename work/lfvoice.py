# 롱폼 목소리 — RULES.md '목소리 고정·말 속도' 규칙 1~3을 코드로 지킨다(ep/A-1/voice.py의 후속, A-1에서 난 사고 세 가지를 막는다).
#   py -3.12 work/lfvoice.py plan  <ep폴더> [--maxreq 9]   # 요청 묶음만 보여 준다(API 안 부름)
#   py -3.12 work/lfvoice.py make  <ep폴더> [--maxreq 9]   # 없는 문장만 만든다 → 자르기 → 느린 문장 atempo → voice.json
#   py -3.12 work/lfvoice.py check <ep폴더>                 # 편 전체 말 속도·음높이 일관성 검사(공개 전 필수, 규칙 3)
# 규칙 1: 모델·목소리는 ep/tts.json에 처음 한 번 적고 잠근다. 429여도 다른 모델로 넘어가지 않고 멈춘다(다음 날 같은 모델로 이어서).
# 규칙 2: 문장별 말 속도(0.6초 넘는 쉼 뺀 초당 음절) 5.6 밑이면 atempo(음높이 유지, 최대 1.25배)로 6.8에 맞춘다. 8.2 넘으면 표시.
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
        s = [syl(t) for t in texts]; ts = sum(s); tgt = [sum(s[:k + 1]) / ts * tl for k in range(need)]
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

def tempo(fn, rate):
    # 규칙 2: 5.6 밑이면 6.8에 맞춘다(최대 1.25배). 결과 파일로 바꿔 넣고 배수를 돌려준다.
    if rate >= 5.6: return 1.0
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
        segs = cut(pcm, todo)
        if segs is None: print('  자르기 실패(저장본 있음, 다시 요청 안 함):', todo[0][:20]); continue
        for t, sg in zip(todo, segs): write(wav_of(ep, cfg, t)[1], np.concatenate([pad, sg, pad]))
        print('  묶음 완료', len(todo), '문장')
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
                if 'tempo' not in info: info = {'tempo': tempo(fn, r), 'rate_raw': round(r, 2)}; json.dump(info, open(meta, 'w'))
                a, sr = read(fn); sec = len(a) / sr; sp = speech_sec(a, sr)
                rec.update({'audio': f"audio/{os.path.basename(aud_dir(ep))}/{h}.wav", 'sec': round(sec, 2), 'frames': int(sec * FPS + 0.999) + GAP_F,
                            'rate': round(syl(say) / max(sp, 0.1), 2), 'tempo': info['tempo'], 'f0': round(f0(a, sr), 1)}); done += 1
            else: miss += 1
            out.append(rec)
        s['lines'] = out; s['frames'] = sum(l.get('frames', 0) for l in out) + (SEC_F if out else 0)
    tot = sum(s['frames'] for s in secs) / FPS; tsyl = sum(syl(l['say']) for s in secs for l in s['lines'])
    res = {'model': cfg['model'], 'voice': cfg['voice'], 'fps': FPS, 'sections': secs, 'done': done, 'missing': miss,
           'seconds': round(tot, 1), 'rate_total': round(tsyl / max(tot, 0.1), 2) if not miss else None}
    json.dump(res, open(os.path.join(ep, 'voice.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f"문장 {done} 완료 · 남음 {miss} · 길이 {tot/60:.1f}분 · 편 전체 {res['rate_total']} 음절/초")

def check(ep, vj=None):
    # 규칙 3: 문장별 음높이·속도가 편 중앙값에서 튀는지. 음높이 ±20%(E-1 첫 한 모델 편으로 다시 맞출 값) 또는 속도 5.6 미만·8.2 초과면 다시 만들 목록.
    d = json.load(open(vj or os.path.join(ep, 'voice.json'), encoding='utf-8')); rows = []
    for s in d['sections']:
        for l in s['lines']:
            if not l.get('audio'): continue
            a, sr = read(os.path.join(PUB, l['audio'])); sp = speech_sec(a, sr)
            rows.append((s['title'][:12], l['text'][:24], syl(l.get('say', l['text'])) / max(sp, 0.1), f0(a, sr), len(a) / sr))
    if not rows: sys.exit('소리 없음')
    fm = float(np.median([r[3] for r in rows if r[3]])); bad = []
    for t, x, r, p, _ in rows:
        why = [w for w, c in (('음높이', p and abs(p / fm - 1) > 0.2), ('느림', r < 5.6), ('빠름', r > 8.2)) if c]
        if why: bad.append(f'{t} | {x} | {r:.2f}음절/초 · {p:.0f}Hz | ' + '·'.join(why))
    tot = sum(s.get('frames', 0) for s in d['sections']) / d.get('fps', FPS); tsyl = sum(syl(l.get('say', l['text'])) for s in d['sections'] for l in s['lines'])
    whole = tsyl / max(tot, 0.1); rates = [r[2] for r in rows]
    print(f'문장 {len(rows)} · 음높이 중앙 {fm:.0f}Hz · 문장 속도 중앙 {np.median(rates):.2f}(최저 {min(rates):.2f}) · 편 전체 {whole:.2f}음절/초(목표 5.5 이상)')
    print('튀는 문장', len(bad), *bad[:40], sep='\n  ')
    ok = whole >= 5.5 and not bad and not d.get('missing')
    print('통과' if ok else '막힘'); return ok

if __name__ == '__main__':
    cmd, ep = sys.argv[1], os.path.abspath(sys.argv[2]); mr = int(sys.argv[sys.argv.index('--maxreq') + 1]) if '--maxreq' in sys.argv else 9
    if cmd == 'plan': make(ep, mr, dry=True)
    elif cmd == 'make': make(ep, mr)
    elif cmd == 'check': sys.exit(0 if check(ep, sys.argv[3] if len(sys.argv) > 3 else None) else 1)
