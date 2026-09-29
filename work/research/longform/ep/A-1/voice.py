# A-1 목소리 — script.md 말하는 문장을 한 줄씩 제미나이 TTS로 읽혀 video/public/audio/a1/에 두고, 장별 문장·길이를 voice.json에 남긴다.
#   py -3.12 work/research/longform/ep/A-1/voice.py [--budget 초]   (이미 만든 문장은 건너뛴다 — 429로 끊겨도 다음 회차가 이어서 돈다)
# 방식은 research/sonpum2/tour_voice.py와 같다(gemini-3.8-flash-tts, 목소리 Charon — 9-1 결정). 화면 자막은 대본 글자 그대로, 읽는 문장만 영문 약어를 한국 유튜버들이 읽는 소리로 바꾼다.
import json, os, re, sys, time, base64, wave, array, hashlib, urllib.request, urllib.error
sys.stdout.reconfigure(encoding='utf-8')
EP = os.path.dirname(os.path.abspath(__file__))
VID = os.path.normpath(os.path.join(EP, '..', '..', '..', '..', 'video'))
AUD = os.path.join(VID, 'public', 'audio', 'a1'); os.makedirs(AUD, exist_ok=True)
KEY = [l.split('=', 1)[-1].strip() for l in open(r'C:\Users\강영준\Documents\gemini_key.txt', encoding='utf-8-sig') if l.strip()][0]
MODELS = ['gemini-3.8-flash-tts', 'gemini-3.1-flash-tts-preview', 'gemini-2.5-flash-preview-tts']; VOICE = 'Charon'; FPS = 30
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
            t = re.sub(r'\s*\(화면[^)]*\)', '', line.strip()[2:]).strip()
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

secs = sections(); done = missing = 0
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
