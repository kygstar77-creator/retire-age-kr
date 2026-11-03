# RT-1 썸네일 배경 사진 — 제미나이 이미지 모델(무료 키, N-2-pilot/gen.py 꼴). py -3.12 gen.py <출력이름> <장면키>
# 실사 사진 느낌, 얼굴 없음(손·몸통만), 그림 안 글자 0 — 글자는 make_rt1n.py가 얹는다. AI 생성이라 유튜브 '합성 콘텐츠' 표시 켬(containsSyntheticMedia).
import json, base64, urllib.request, urllib.error, sys, os
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(H, '..', '..', '..')))
from crosscheck import load_key
KEY = load_key('gemini_key.txt')['KEY']
MODELS = ['gemini-3-pro-image', 'gemini-3.1-flash-image']
STYLE = (" Photorealistic documentary photo, shot on a 35mm lens, natural window light, slightly moody evening tone, shallow depth of field, realistic hands with five fingers,"
         " no people's faces visible anywhere (frame cuts above the shoulders or shows only hands and arms)."
         " Absolutely no text, no letters, no Korean characters, no numbers, no logos anywhere: papers are blank or show only grey lines.")
SCENE = {
 'box': ("Wide 16:9 photo. Last day at a Korean office: on a grey office desk, a cardboard box filled with personal belongings (a framed photo seen from the back, a mug,"
         " a small potted plant, folded documents). Two hands of a man in his late 50s (white shirt cuffs, silver wristwatch) place a desk name plate (blank) into the box."
         " The box and hands sit in the UPPER-CENTER of the frame (top 55%); the lower 40% is the dark plain desk surface in shadow, empty, for text."),
 'paper': ("Wide 16:9 photo. Close-up from above at a slight angle: on a dark wooden table, a man's hand (late 50s, white shirt cuff) holds a pen over a single blank paper form"
           " (grey lines only) next to a closed cardboard box of office belongings and a small calculator. The hand, form and box are in the UPPER half of the frame;"
           " the lower 40% is dark empty table in shadow, for text."),
}
def run(name, key):
    parts = [{'text': SCENE[key] + STYLE}]
    for m in MODELS:
        try:
            r = json.load(urllib.request.urlopen(urllib.request.Request(f'https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={KEY}',
                data=json.dumps({'contents': [{'parts': parts}], 'generationConfig': {'responseModalities': ['IMAGE'], 'imageConfig': {'aspectRatio': '16:9'}}}).encode(),
                headers={'Content-Type': 'application/json'}), timeout=300))
            for p in r['candidates'][0]['content']['parts']:
                d = p.get('inlineData') or p.get('inline_data')
                if d:
                    os.makedirs(os.path.join(H, 'photo'), exist_ok=True)
                    open(os.path.join(H, 'photo', name + '.png'), 'wb').write(base64.b64decode(d['data'])); print('ok', m, name); return m
            print('no image', m, str(r)[:200])
        except urllib.error.HTTPError as e:
            print('fail', m, e.code, e.read().decode('utf-8', 'replace')[:200].replace(KEY, '***'))
        except Exception as e:
            print('fail', m, str(e)[:200].replace(KEY, '***'))
if __name__ == '__main__':
    run(sys.argv[1], sys.argv[2])
