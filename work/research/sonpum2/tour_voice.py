# "대신 둘러봐 드립니다" 해설 문장 + 목소리 — tour.json을 읽어 장면별 해설을 만들고 제미나이 TTS로 읽혀 video/public/audio/tour/에 둔다.
#   py -3.12 work/research/sonpum2/tour_voice.py   (tour.py 다음에 돌린다) → tour.json에 'scenes'(장면별 문장·음성·길이)를 붙인다
# 해설 문장은 전부 그 동네 숫자에서 나온다(스팸정책 "템플릿 반복" 대응 — 동네마다 가장 높은·낮은 단지, 차이가 문장에 들어간다).
# 목소리: gemini-3.8-flash-tts(약관: 생성물 소유권을 구글이 주장하지 않음, 2026-09-30 확인). 화면 자막은 글자 그대로, 읽는 문장은 단위를 말로 바꾼다.
import json, os, re, sys, time, base64, wave, hashlib, math, urllib.request, urllib.error
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); VID = os.path.join(HERE, '..', '..', 'video')
TJ = os.path.join(VID, 'tour.json'); AUD = os.path.join(VID, 'public', 'audio', 'tour'); os.makedirs(AUD, exist_ok=True)
KEY = [l.split('=', 1)[-1].strip() for l in open(r'C:\Users\강영준\Documents\gemini_key.txt', encoding='utf-8-sig') if l.strip()][0]
MODELS = ['gemini-3.8-flash-tts', 'gemini-3.1-flash-tts-preview']; VOICE = 'Charon'; FPS = 30
p = json.load(open(TJ, encoding='utf-8'))

def eok(man):
    e, r = divmod(int(round(man)), 10000)
    return (f'{e}억 {r:,}만원' if r else f'{e}억') if e else f'{r:,}만원'
def ym(s): y, m = s.split('.'); return f'{y}년 {int(m)}월'
def speak(t):
    t = re.sub(r'(\d{4})\.(\d{2})', lambda m: f'{m[1]}년 {int(m[2])}월', t)
    t = t.replace('㎡', '제곱미터').replace('1·2단지', '1, 2단지').replace('~', '에서 ')
    t = re.sub(r'(\d[\d,]*)m\b', r'\1미터', t)
    return t

C = {c['name']: c for c in p['complexes']}
tour = [C[n] for n in p['tour']]
ranked = sorted([c for c in p['complexes'] if c.get('ppyTop')], key=lambda c: -c['ppyTop'])
rent = sorted([c for c in p['complexes'] if c['rent'].get('j')], key=lambda c: c['rent']['j'])
scenes = []
scenes.append({'kind': 'title', 'lines': [f"대신 둘러봐 드립니다. 오늘은 {p['gu']} {p['umd']}이에요."]})
over = [f"{p['umd']} 아파트 {len(p['complexes'])}곳을 최근 1년 실거래로 대신 둘러볼게요.",
        f"평수가 다르면 평당가도 달라서, 가장 많이 거래된 전용 {p['topLabel']}끼리만 견줬어요."]
if len(ranked) >= 2:
    over.append(f"이 면적 평당가는 {ranked[0]['name']}이 {ranked[0]['ppyTop']:,}만원으로 가장 높고, {ranked[-1]['name']}이 {ranked[-1]['ppyTop']:,}만원으로 가장 낮아요.")
scenes.append({'kind': 'over', 'lines': over})
for c in tour:
    k = c['kapt']; st = c['walk'].get('station')
    try: fd = c['fromMax'] < 0 and (abs(int(c['last']['floor']) - int(c['max']['floor'])) >= 5 or int(c['last']['floor']) <= 2)
    except ValueError: fd = False
    L = [f"{c['name']}, {c['built']}년에 지은 {k['hh']:,}세대 단지예요. 주차는 세대당 {k['parkPer']}대예요."]
    if c['fromMax'] == 0: L.append(f"전용 {c['area']}㎡ 최근 거래는 {c['last']['ym']} {c['last']['floor']}층 {eok(c['last']['amt'])}, 1년 중 가장 높은 값이었어요.")
    else: L.append(f"전용 {c['area']}㎡ 최근 거래는 {c['last']['ym']} {c['last']['floor']}층 {eok(c['last']['amt'])}, 1년 최고는 {c['max']['floor']}층 {eok(c['max']['amt'])}이에요." + (' 층이 달라 그대로 견주긴 어려워요.' if fd else ''))
    if c['nOdd']: L.append(f"빈 점 {c['nOdd']}개는 다른 거래와 20% 넘게 동떨어진 거래예요. 이유는 자료에 없어서 계산에서 뺐어요.")
    L.append(f"같은 면적 신규 전세는 중앙값 {eok(c['jeonse'])}, 매매 중앙값의 {c['jratio']}%예요." if c.get('jratio') else f"같은 면적 신규 전세는 1년에 {c['nj']}건뿐이라 전세가율은 내지 않았어요.")
    if st:
        s = f"{st['name']}까지 걸어서 {st['m']:,}m"
        if k.get('subwayWalk'): s += f", 관리사무소 등록 정보로는 {(k['subway'].rstrip('역') + '역 ') if k.get('subway') else '지하철역 '}도보 {k['subwayWalk'].replace('이내', ' 이내')}예요."
        else: s += '예요.'
        L.append(s)
    scenes.append({'kind': 'cx', 'name': c['name'], 'lines': L})
R = [f"이번엔 살 집으로 볼게요. 같은 {p['umd']} 안에서도 평당 전세가 이만큼 차이 나요."]
if len(rent) >= 2:
    R.append(f"순수 전세 신규 계약 기준으로 {rent[0]['name']}이 평당 {rent[0]['rent']['j']:,}만원으로 가장 낮고, {rent[-1]['name']}이 {rent[-1]['rent']['j']:,}만원으로 가장 높아요.")
R += ['낮은 곳엔 이유가 있을 수 있어요. 지은 해와 역까지 거리를 같이 보세요.', '평당 월세는 보증금을 0으로 바꿔 한 달에 평당 얼마인지 계산한 값이에요.']
scenes.append({'kind': 'rent', 'lines': R})
scenes.append({'kind': 'sum', 'lines': ['싸다 비싸다가 아니라, 실제로 거래된 숫자만 보여 드렸어요.', '지금 나와 있는 호가는 네이버 부동산에서 직접 확인해 보세요.']})

def tts(text):
    h = hashlib.md5((VOICE + '|' + text).encode()).hexdigest()[:16]; fn = os.path.join(AUD, h + '.wav')
    if os.path.exists(fn):
        with wave.open(fn) as w: return h, w.getnframes() / w.getframerate()
    body = {'contents': [{'parts': [{'text': '차분하고 또렷한 부동산 해설 유튜버 말투로, 숫자는 천천히 또박또박, 자연스럽게 읽어 주세요: ' + text}]}],
            'generationConfig': {'responseModalities': ['AUDIO'], 'speechConfig': {'voiceConfig': {'prebuiltVoiceConfig': {'voiceName': VOICE}}}}}
    for attempt in range(8):
        m = MODELS[attempt % len(MODELS)]
        try:
            r = json.load(urllib.request.urlopen(urllib.request.Request(f'https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={KEY}',
                data=json.dumps(body).encode(), headers={'Content-Type': 'application/json'}), timeout=180))
            pcm = base64.b64decode(r['candidates'][0]['content']['parts'][0]['inlineData']['data'])
            with wave.open(fn, 'wb') as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(24000); w.writeframes(pcm)
            return h, len(pcm) / 48000
        except urllib.error.HTTPError as e:
            print('  재시도', m, e.code); time.sleep(8 + attempt * 6)
        except Exception as e:
            print('  재시도', m, str(e)[:80]); time.sleep(8)
    raise RuntimeError('목소리 생성 실패: ' + text[:30])

total = 0
for sc in scenes:
    out = []
    for t in sc['lines']:
        h, sec = tts(speak(t))
        fr = math.ceil(sec * FPS) + 14; total += fr
        out.append({'text': t, 'audio': f'audio/tour/{h}.wav', 'frames': fr}); print(f'{sec:5.1f}초 {t}')
    sc['lines'] = out; sc['frames'] = sum(l['frames'] for l in out) + 24
p['scenes'] = scenes
json.dump(p, open(TJ, 'w', encoding='utf-8'), ensure_ascii=False)
print('장면', len(scenes), '· 문장', sum(len(s['lines']) for s in scenes), f'· 길이 약 {sum(s["frames"] for s in scenes)/FPS:.0f}초')
