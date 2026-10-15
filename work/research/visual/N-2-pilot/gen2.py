# N-2 시범작 v7 장면 그림 — 이름 붙은 인물 없이 '보통 직장인' 장면(뒷모습·손·장소). 제미나이 이미지 모델(무료 키).
#   py -3.12 gen2.py <장면키> [출력이름]   → visual/N-2-pilot/<출력이름>.png
# 그림 안 글자 0 — 숫자·자막은 pilot/compose7.py가 얹는다. 429면 다음 모델로(프로젝트 바꿔 우회 금지). 키는 출력하지 않는다.
import json, base64, urllib.request, urllib.error, sys, os
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(H, '..', '..', '..')))
from crosscheck import load_key
KEY = load_key('gemini_key.txt')['KEY']
MODELS = [m for m in os.environ.get('GEN_MODELS', 'gemini-3-pro-image,gemini-3.1-flash-image,gemini-nano-banana-2.1').split(',')]

STYLE = (" Style: high-quality documentary photograph look, natural light, realistic but slightly soft focus, muted everyday colors,"
         " 35mm lens, shallow depth of field. Ordinary fictional people who do not resemble any real or famous person.")
NOTEXT = (" Absolutely no readable text, no letters, no Korean characters, no numbers, no logos, no brand marks, no signage anywhere:"
          " papers, screens and signs are blank or blurred.")
SCENE = {
 'crowd': ("Wide 16:9. Morning rush hour on a wide pedestrian crosswalk in a Korean city (Seoul-like office district, generic glass buildings, no signs)."
           " Many office and factory workers of mixed ages (20s to 60s) walking away from the camera, seen from behind and from the side, faces not visible or blurred by motion."
           " Camera at chest height. Keep the left 45% of the frame calmer (out-of-focus street and sky) for big on-screen text."),
 'line': ("Wide 16:9. A very long single-file line of ordinary Korean working adults of mixed ages and jobs (office shirt, factory work jacket, apron, delivery jacket, cardigan)"
          " standing one behind another on a wide plain light-grey concrete plaza, seen from the side at a low three-quarter angle, the line receding far into the distance."
          " Most faces turned away or tiny in the distance. In the exact middle of the frame one middle-aged worker in a plain navy jacket stands slightly lit by a soft spotlight."
          " Calm overcast light. Leave the top 35% of the frame as plain sky / plain wall for on-screen text."),
 'payslip': ("Wide 16:9 close-up. A middle-aged Korean worker's hands (realistic, exactly five fingers each, simple wedding ring) holding a single printed pay slip"
             " over a worn wooden desk in a small factory office; the paper shows only grey blurred lines and blank boxes, nothing readable."
             " A ceramic cup of barley tea and reading glasses on the desk. Warm window light from the right. Only hands and forearms in white shirt sleeves visible, no face."
             " The hands and paper sit in the right half; the left 45% is a calm blurred desk and wall for on-screen text."),
 'towers': ("Wide 16:9. Dusk view of a Korean business district: a few tall glass office towers with some lit windows, seen from street level looking up,"
            " a single office worker in a suit seen from behind, small, walking toward the towers. No signs, no logos, no readable text."
            " Deep blue evening sky. Keep the left 45% calm (sky) for on-screen text."),
}

def run(key, name=None):
    name = name or key
    parts = [{'text': SCENE[key] + STYLE + NOTEXT}]
    for m in MODELS:
        try:
            r = json.load(urllib.request.urlopen(urllib.request.Request(f'https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={KEY}',
                data=json.dumps({'contents': [{'parts': parts}], 'generationConfig': {'responseModalities': ['IMAGE'], 'imageConfig': {'aspectRatio': '16:9'}}}).encode(),
                headers={'Content-Type': 'application/json'}), timeout=300))
            for p in r['candidates'][0]['content']['parts']:
                d = p.get('inlineData') or p.get('inline_data')
                if d:
                    open(os.path.join(H, name + '.png'), 'wb').write(base64.b64decode(d['data'])); print('ok', m, name); return m
            print('no image', m, str(r)[:200])
        except urllib.error.HTTPError as e:
            print('fail', m, e.code, e.read().decode('utf-8', 'replace')[:160].replace(KEY, '***'))
        except Exception as e:
            print('fail', m, str(e)[:160].replace(KEY, '***'))
    return None

if __name__ == '__main__':
    run(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
