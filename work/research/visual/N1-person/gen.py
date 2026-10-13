# N1 시범 가상 인물 시트·장면 — gemini 이미지 모델. py -3.12 gen.py <출력이름> <프롬프트키> [참조이미지.png ...]
# 인물은 지어낸 사람(실존 인물·사진 금지), 그림 안 글자 0 — 글자·'가상 인물' 고지는 렌더 때 따로 얹는다.
import json, base64, urllib.request, sys, os
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__))
KEY = [l.split('=', 1)[-1].strip() for l in open(r'C:\Users\강영준\Documents\gemini_key.txt', encoding='utf-8-sig') if l.strip()][0]
STYLE = (" Style: warm flat editorial illustration, clean vector-like shapes, soft grain, muted palette (cream, navy, warm grey, one coral accent),"
         " clearly a drawing not a photo, fictional person who does not resemble any real or famous person."
         " Absolutely no text, no letters, no numbers, no logos, no brand marks anywhere in the image.")
WHO = ("The same fictional Korean man throughout: round face, short side-parted black hair with grey at the temples, thin black-rimmed rectangular glasses,"
       " small mole under the left eye, navy cardigan over a light-blue collared shirt, carries a small dark-blue bank passbook.")
P = {
 'sheet': "Character model sheet on a plain cream background, wide 16:9. " + WHO +
          " Top row, age 55 (year 1998): front view, three-quarter view, side profile, full body standing — identical face, hair, glasses, mole and clothes in every view."
          " Bottom row, same man age 66 (year 2009, hair mostly grey, slightly thinner face, same glasses, mole and cardigan): front view, and four expression heads — calm, worried looking at passbook, surprised, relieved small smile."
          " Even spacing, no panels borders needed." + STYLE,
}
SCENE = {
 's1998': "Wide 16:9 scene. Year 1998, a small Korean apartment living room, morning light. The man (age 55) sits at a low table opening his dark-blue passbook for the first time after retiring, calm hopeful face. Leave the left 40% of the frame quiet (plain wall) for on-screen text.",
 's2001': "Wide 16:9 scene. Year 2001, evening, the man (age 58) at a kitchen table under a single lamp, holding the dark-blue passbook, worried face, a TV in the background showing only an abstract falling red line (no text). Leave the right 40% quiet for text.",
 's2009': "Wide 16:9 scene. Year 2009, the man (age 66, hair mostly grey) at a bank counter-like table seen from the side, looking at the dark-blue passbook with a surprised face. Leave the left 40% quiet for text.",
}
name, k = sys.argv[1], sys.argv[2]
refs = sys.argv[3:]
text = P.get(k) or ("Use the attached character sheet as the exact reference: same face, hair, glasses, mole under left eye, navy cardigan, dark-blue passbook. " + WHO + " " + SCENE[k] + STYLE)
parts = [{'text': text}] + [{'inline_data': {'mime_type': 'image/png', 'data': base64.b64encode(open(r, 'rb').read()).decode()}} for r in refs]
for m in ['gemini-3-pro-image-preview', 'gemini-3.1-flash-image-preview', 'gemini-2.5-flash-image']:
    try:
        r = json.load(urllib.request.urlopen(urllib.request.Request(f'https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={KEY}',
            data=json.dumps({'contents': [{'parts': parts}], 'generationConfig': {'responseModalities': ['IMAGE'], 'imageConfig': {'aspectRatio': '16:9'}}}).encode(),
            headers={'Content-Type': 'application/json'}), timeout=300))
        for p in r['candidates'][0]['content']['parts']:
            d = p.get('inlineData') or p.get('inline_data')
            if d:
                open(os.path.join(H, name + '.png'), 'wb').write(base64.b64decode(d['data'])); print('ok', m, name); sys.exit()
        print('no image', m, str(r)[:300])
    except SystemExit: raise
    except Exception as e: print('fail', m, str(e)[:200])
