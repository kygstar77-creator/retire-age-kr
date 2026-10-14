# N-2 시범작 인물·장면 그림 — 제미나이 이미지 모델(무료 키). py -3.12 gen.py <출력이름> <키> [참조.png ...]
# 인물은 지어낸 사람(실존 인물 닮음 금지), 그림 안 글자 0 — 글자·숫자·'가상 인물' 표시는 compose.py가 얹는다.
# 키는 work/crosscheck.load_key('gemini_key.txt') — 출력하지 않는다.
import json, base64, urllib.request, urllib.error, sys, os
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(H, '..', '..', '..')))
from crosscheck import load_key
KEY = load_key('gemini_key.txt')['KEY']
MODELS = ['gemini-3-pro-image', 'gemini-3.1-flash-image', 'gemini-nano-banana-2.1']

STYLE = {
 'w': (" Style: Korean webtoon-style digital illustration, clean confident line art, soft cel shading, natural muted everyday colors,"
       " matte finish (no glossy plastic skin, no shiny highlights), realistic adult proportions, hands drawn simply and correctly with five fingers,"
       " calm documentary mood like a slice-of-life webtoon."),
 'p': (" Style: hand-painted semi-realistic editorial illustration (gouache texture), warm natural light, muted earthy palette,"
       " matte, realistic adult proportions, hands simple and anatomically correct, calm documentary mood."),
}
NOTEXT = (" Fictional ordinary person who does not resemble any real or famous person."
          " Absolutely no text, no letters, no Korean characters, no numbers, no logos, no brand marks anywhere: papers, screens and signs are blank or show only grey lines.")
WHO = ("The same fictional Korean man throughout: age 57, office manager at a small parts-manufacturing company. Oval face with gentle laugh lines,"
       " short neatly combed black hair with grey streaks and a slightly receding hairline, thin gold-rimmed rectangular glasses,"
       " navy zip-up company work jacket with a thin orange stripe across the chest (no logo), white collared shirt underneath, silver wristwatch on the left wrist.")
SHEET = ("Character model sheet on a plain light-grey background, wide 16:9. " + WHO +
         " Top row: front view, three-quarter view, side profile, full body standing - identical face, hair, glasses and clothes in every view."
         " Bottom row: four head close-ups with expressions - calm, puzzled looking down at a phone, surprised, relieved small smile. Even spacing, no panel borders.")
SCENE = {
 's1': ("Wide 16:9 scene. Lunch break in a small Korean factory's staff cafeteria (simple metal trays, long tables, a window to a factory yard)."
        " The man sits alone at the end of a table with a half-finished lunch tray, holding his smartphone and frowning slightly at it, puzzled."
        " Medium shot from slightly to his side, he is on the right third of the frame. Keep the left 40% of the frame calm and uncluttered (cafeteria wall, soft light) for on-screen text."),
 's2': ("Wide 16:9 scene. His desk in a modest factory office (grey steel desk, binders, a desk calendar with blank squares, a window to the shop floor)."
        " He holds a single blank paper pay slip (only grey lines, no writing) in both hands, looking at it thoughtfully. Medium close shot,"
        " he is on the right half. Keep the left 40% calm (plain wall) for on-screen text."),
 's3': ("Wide 16:9 scene. A long single-file line of about twenty ordinary Korean office and factory workers in their late 50s standing on a wide plain light floor,"
        " seen from the side and slightly above, receding into the distance - like a line for a group photo. Everyone wears different everyday work clothes."
        " The man (navy work jacket with orange stripe, gold glasses) stands roughly in the middle of the line, slightly toward the front half, looking a bit surprised."
        " Near the very front of the line, two or three people stand on tall stacked platforms, much higher than everyone else."
        " Clean simple background. Leave the top 30% of the frame calm for on-screen text."),
 's4': ("Wide 16:9 scene. Evening at home in a modest Korean apartment kitchen table, warm lamp light. The man has taken off his work jacket and wears the white shirt,"
        " sitting relaxed with a cup of barley tea, a folded blank pay slip on the table, smiling slightly with relief while talking to his wife who is seen only from behind"
        " (shoulder-length hair, cardigan, face not visible). He is on the right half. Keep the left 35% calm for on-screen text."),
 'th': ("Wide 16:9 thumbnail-style image, close medium shot of the man from chest up, against a plain soft background, holding a blank pay slip (grey lines only) beside his face,"
        " eyebrows raised, curious and slightly surprised expression looking at the viewer. He fills the right 45% of the frame. Left 55% is plain flat background for big text."),
}

def run(name, key, refs):
    st = key[0]; k = key[1:]
    if k == 'sheet': text = SHEET + STYLE[st] + NOTEXT
    else: text = ("Use the attached character sheet as the exact reference for the man: same face, hair, gold glasses, navy jacket with orange stripe, watch. "
                  + WHO + " " + SCENE[k] + STYLE[st] + NOTEXT)
    parts = [{'text': text}] + [{'inline_data': {'mime_type': 'image/png', 'data': base64.b64encode(open(r, 'rb').read()).decode()}} for r in refs]
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
            print('fail', m, e.code, e.read().decode('utf-8', 'replace')[:200].replace(KEY, '***'))
        except Exception as e:
            print('fail', m, str(e)[:200].replace(KEY, '***'))
    return None

if __name__ == '__main__':
    run(sys.argv[1], sys.argv[2], sys.argv[3:])
