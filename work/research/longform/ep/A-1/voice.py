# A-1 목소리 — script.md 말하는 문장을 한 줄씩 제미나이 TTS로 읽혀 video/public/audio/a1/에 두고, 장별 문장·길이를 voice.json에 남긴다.
#   py -3.12 work/research/longform/ep/A-1/voice.py [--budget 초] [--by-section]   (이미 만든 문장은 건너뛴다 — 429로 끊겨도 다음 회차가 이어서 돈다)
# 방식은 research/sonpum2/tour_voice.py와 같다(gemini-3.8-flash-tts, 목소리 Charon — 9-1 결정). 화면 자막은 대본 글자 그대로, 읽는 문장만 영문 약어를 한국 유튜버들이 읽는 소리로 바꾼다.
import glob, json, os, re, sys, time, base64, wave, array, hashlib, urllib.request, urllib.error
sys.stdout.reconfigure(encoding='utf-8')
EP = os.path.dirname(os.path.abspath(__file__))
VID = os.path.normpath(os.path.join(EP, '..', '..', '..', '..', 'video'))
AUD = os.path.join(VID, 'public', 'audio', 'a1'); os.makedirs(AUD, exist_ok=True)
KEY = [l.split('=', 1)[-1].strip() for l in open(r'C:\Users\강영준\Documents\gemini_key.txt', encoding='utf-8-sig') if l.strip()][0]
MODELS = ['gemini-3.8-flash-tts', 'gemini-3.1-flash-tts-preview', 'gemini-2.5-flash-preview-tts', 'gemini-3.8-flash-lite-tts']; VOICE = 'Charon'; FPS = 30   # lite: 14:20 PD 추가(목록에 있고 할당량 따로)
BUDGET = int(sys.argv[sys.argv.index('--budget') + 1]) if '--budget' in sys.argv else 1500
T0 = time.time()
SAY = [('S&P500', '에스앤피 500'), ('JEPQ', '제피큐'), ('JEPI', '제피'), ('SCHD', '슈드'), ('QQQI', '큐큐큐아이'), ('QQQ', '큐큐큐'),
       ('SPYI', '에스피와이아이'), ('SPY', '에스피와이'), ('KODEX', '코덱스'), ('ELN', '이엘엔'), ('ETF', '이티에프'), ('ISA', '아이에스에이'),
       ('JP모건', '제이피모건'), ('3M', '쓰리엠'), ('%포인트', '퍼센트포인트')]

def speak(t):
    for a, b in SAY: t = t.replace(a, b)
    return t

def sections():
    body = open(os.path.join(EP, 'script.md'), encoding='utf-8').read().split('\n---', 1)[0]
    out, cur = [], None
    for line in body.splitlines():
        if line.startswith('## '):
            cur = {'title': line[3:].strip(), 'lines': []}; out.append(cur)
        elif line.lstrip().startswith('- ') and cur is not None:
            t = re.sub(r'\s*\(화면.*$', '', line.strip()[2:]).strip()   # 화면 메모는 줄 끝에 온다(안에 괄호가 있어도 통째로 뺀다)
            if t: cur['lines'].append(t)
    return out

class Stop(Exception): pass

# 2026-09-30 루프 2회차: 첫 16문장 중 5개가 목소리 구간 기준 초당 2.1~4.4음절(나머지 5.4~6.9) — 한국어로 길게 쓴 말투 지시문까지
# 소리 내 읽은 것으로 보인다(짧은 문장 18음절이 12.3초). 그래서 ① 지시문을 짧은 영어로 바꾸고 ② 목소리 구간 기준 초당 4.8음절 밑이면
# 버리고 다시 만든다(두 번 다 느리면 남기고 voice.json에 slow로 표시 — 사람이 들어 볼 목록).
def voiced_rate(fn, text):
    with wave.open(fn) as w:
        a = array.array('h', w.readframes(w.getnframes())); sr = w.getframerate()
    win = sr // 50
    v = sum(1 for i in range(0, len(a), win) if max((abs(x) for x in a[i:i + win]), default=0) > 600) / 50
    return len(re.findall('[가-힣0-9]', text)) / max(v, 0.1)
MIN_RATE = 4.8

def tts(text):
    h = hashlib.md5((VOICE + '|' + text).encode()).hexdigest()[:16]; fn = os.path.join(AUD, h + '.wav')
    if os.path.exists(fn):
        if voiced_rate(fn, text) >= MIN_RATE or os.path.exists(fn + '.slow'):
            with wave.open(fn) as w: return h, w.getnframes() / w.getframerate()
        os.remove(fn); print('  느린 파일 다시 만듦', text[:20])
    if time.time() - T0 > BUDGET: raise Stop()
    body = {'contents': [{'parts': [{'text': 'Say in Korean, calm and clear, at a natural YouTube narration pace: ' + text}]}],
            'generationConfig': {'responseModalities': ['AUDIO'], 'speechConfig': {'voiceConfig': {'prebuiltVoiceConfig': {'voiceName': VOICE}}}}}
    for attempt in range(6):
        m = MODELS[attempt % len(MODELS)]
        try:
            r = json.load(urllib.request.urlopen(urllib.request.Request(f'https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={KEY}',
                data=json.dumps(body).encode(), headers={'Content-Type': 'application/json'}), timeout=180))
            pcm = base64.b64decode(r['candidates'][0]['content']['parts'][0]['inlineData']['data'])
            with wave.open(fn, 'wb') as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(24000); w.writeframes(pcm)
            if voiced_rate(fn, text) < MIN_RATE:
                if attempt == 0: print('  느림 — 한 번 더', text[:20]); continue
                open(fn + '.slow', 'w').close()
            return h, len(pcm) / 48000
        except urllib.error.HTTPError as e:
            print('  재시도', m, e.code); time.sleep(8 + attempt * 6)
        except Exception as e:
            print('  재시도', m, str(e)[:80]); time.sleep(8)
    raise Stop()

# 2026-09-30 PD: 무료 등급 TTS는 모델마다 하루 10회(quotaId GenerateRequestsPerDayPerProjectPerModel-FreeTier, quotaValue 10)라
# 문장별 108회는 하루에 못 끝난다. --by-section: 한 장을 한 번에 읽히고, 문장 수-1개의 가장 긴 무음에서 잘라 문장별 파일로 둔다
# (파일 이름이 문장별 방식과 같아 아래 반복문이 그대로 가져다 쓴다). 자른 조각 길이 비율이 글자 비율과 2배 넘게 어긋나면 버린다.
# 이 모드에서는 문장별 요청을 하지 않는다(--line-fallback을 붙이면 한다).
BYSEC = '--by-section' in sys.argv
def split_section(pcm, texts, mingap=8):
    win = 480
    loud = [max((abs(x) for x in pcm[i:i + win]), default=0) > 600 for i in range(0, len(pcm), win)]
    gaps, i = [], 0
    while i < len(loud):
        if not loud[i]:
            j = i
            while j < len(loud) and not loud[j]: j += 1
            if i > 0 and j < len(loud) and (j - i) >= mingap: gaps.append((j - i, (i + j) // 2 * win))
            i = j
        else: i += 1
    need = len(texts) - 1
    if len(gaps) < need: return None
    cuts = sorted(c for _, c in sorted(gaps, reverse=True)[:need])
    segs = [pcm[a:b] for a, b in zip([0] + cuts, cuts + [len(pcm)])]
    syl = [len(re.findall('[가-힣0-9]', t)) for t in texts]; ts, tl = sum(syl), len(pcm)
    for s, n in zip(segs, syl):
        r = (len(s) / tl) / (n / ts)
        if r < 0.5 or r > 2.0: return None
    return segs

# 2026-09-30 14:30 PD: lite 모델은 문장 안 쉼표에서도 0.7~0.9초 쉬어서 '가장 긴 무음 N-1개'가 문장 경계가 아니었다(장 11·12).
# 그래서 마지막 방법으로, 무음 후보 중에서 글자 수 누적 비율에 가장 가까운 자리를 순서대로 고른다(DP, 무음이 길수록 조금 가산).
def split_dp(pcm, texts, mingap=8):
    win = 480
    loud = [max((abs(x) for x in pcm[i:i + win]), default=0) > 600 for i in range(0, len(pcm), win)]
    cand, i = [], 0
    while i < len(loud):
        if not loud[i]:
            j = i
            while j < len(loud) and not loud[j]: j += 1
            if i > 0 and j < len(loud) and (j - i) >= mingap: cand.append(((i + j) // 2 * win, j - i))
            i = j
        else: i += 1
    need = len(texts) - 1; tl = len(pcm)
    syl = [len(re.findall('[가-힣0-9]', t)) for t in texts]; ts = sum(syl)
    tgt = [sum(syl[:k + 1]) / ts * tl for k in range(need)]
    if len(cand) < need: return None
    INF = float('inf'); n = len(cand)
    cost = lambda k, c: abs(cand[c][0] - tgt[k]) / tl - 0.002 * cand[c][1]
    best = [[INF] * n for _ in range(need)]; prev = [[-1] * n for _ in range(need)]
    for c in range(n): best[0][c] = cost(0, c)
    for k in range(1, need):
        run, arg = INF, -1
        for c in range(n):
            if c > 0 and best[k - 1][c - 1] < run: run, arg = best[k - 1][c - 1], c - 1
            if arg >= 0: best[k][c] = run + cost(k, c); prev[k][c] = arg
    c = min(range(n), key=lambda x: best[need - 1][x]); cuts = []
    for k in range(need - 1, -1, -1): cuts.append(cand[c][0]); c = prev[k][c]
    cuts = sorted(cuts)
    segs = [pcm[a:b] for a, b in zip([0] + cuts, cuts + [tl])]
    for sg, n_ in zip(segs, syl):
        r = (len(sg) / tl) / (n_ / ts)
        if r < 0.6 or r > 1.6: return None
    return segs

def wav_of(t): return os.path.join(AUD, hashlib.md5((VOICE + '|' + t).encode()).hexdigest()[:16] + '.wav')

# 2026-09-30 10:30 PD: 자르기 실패 3번이 무료 할당량(하루 모델당 10회)을 그냥 버렸다 → ① 이미 있는 문장은 빼고 없는 문장만 보낸다
# ② 받은 소리는 _raw/에 먼저 저장해 두고(다시 요청하지 않는다) ③ 무음 기준을 0.16초→0.1초로 한 번 더 낮춰 자른다.
RAW = os.path.join(AUD, '_raw'); os.makedirs(RAW, exist_ok=True)
def cut_and_save(pcm, texts):
    segs = split_section(pcm, texts) or split_section(pcm, texts, 5) or split_section(pcm, texts, 3) or split_dp(pcm, texts)   # 14:20 PD: 0.06초까지, 그다음 글자 비율 DP
    if segs is None: return False
    pad = array.array('h', [0] * 2400)   # 앞뒤 0.1초
    for t, sg in zip(texts, segs):
        fn = wav_of(t)
        if os.path.exists(fn): continue
        with wave.open(fn, 'wb') as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(24000); w.writeframes((pad + sg + pad).tobytes())
        if voiced_rate(fn, t) < MIN_RATE: open(fn + '.slow', 'w').close()
    return True

def tts_section(texts):
    texts = [t for t in texts if not os.path.exists(wav_of(t))]
    if not texts: return True
    key = hashlib.md5((VOICE + '|' + '|'.join(texts)).encode()).hexdigest()[:16]
    for f in glob.glob(os.path.join(RAW, key + '_*.pcm')):   # 전에 받아 둔 소리부터
        pcm = array.array('h'); pcm.frombytes(open(f, 'rb').read())
        if cut_and_save(pcm, texts): print('  장 완료(저장본)', len(texts), '문장', texts[0][:20]); return True
    body = {'contents': [{'parts': [{'text': 'Read these Korean lines in order as a calm, clear YouTube narration at a natural pace. Pause about one second between lines:\n' + '\n'.join(texts)}]}],
            'generationConfig': {'responseModalities': ['AUDIO'], 'speechConfig': {'voiceConfig': {'prebuiltVoiceConfig': {'voiceName': VOICE}}}}}
    for m in MODELS:
        if time.time() - T0 > BUDGET: return False
        if m in DEAD: continue
        try:
            r = json.load(urllib.request.urlopen(urllib.request.Request(f'https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={KEY}',
                data=json.dumps(body).encode(), headers={'Content-Type': 'application/json'}), timeout=300))
            pcm = array.array('h'); pcm.frombytes(base64.b64decode(r['candidates'][0]['content']['parts'][0]['inlineData']['data']))
            open(os.path.join(RAW, f'{key}_{m}.pcm'), 'wb').write(pcm.tobytes())
            if not cut_and_save(pcm, texts): print('  장 자르기 실패', m, texts[0][:20]); continue
            print('  장 완료', m, len(texts), '문장', texts[0][:20]); return True
        except urllib.error.HTTPError as e:
            print('  장 실패', m, e.code)
            if e.code == 429 and 'PerDay' in e.read().decode(errors='ignore'): DEAD.add(m)   # 하루치 다 씀 — 오늘은 다시 부르지 않는다
        except Exception as e: print('  장 실패', m, str(e)[:80])
    return False
DEAD = set()

secs = sections(); done = missing = 0
if BYSEC:
    for sc in secs:
        if sc['lines']: tts_section([speak(t) for t in sc['lines']])
    if '--line-fallback' not in sys.argv: BUDGET = -1   # 없는 문장은 요청하지 않고 빈칸으로 남긴다
for sc in secs:
    out = []
    for t in sc['lines']:
        try:
            h, sec = tts(speak(t)); done += 1
            out.append({'text': t, 'say': speak(t), 'audio': f'audio/a1/{h}.wav', 'sec': round(sec, 2), 'frames': int(sec * FPS + 0.999) + 12})
        except Stop:
            missing += 1; out.append({'text': t, 'say': speak(t), 'audio': None})
    sc['lines'] = out
    sc['frames'] = sum(l.get('frames', 0) for l in out) + (24 if out else 0)
tot = sum(s['frames'] for s in secs) / FPS
json.dump({'voice': VOICE, 'fps': FPS, 'sections': secs, 'done': done, 'missing': missing, 'seconds': round(tot, 1)},
          open(os.path.join(EP, 'voice.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(f'문장 {done}개 완료 · 남음 {missing}개 · 지금까지 길이 {tot/60:.1f}분')
