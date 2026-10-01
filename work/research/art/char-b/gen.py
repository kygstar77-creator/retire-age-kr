# X-THUMB-1 B군 캐릭터 시안 생성(제미나이 이미지) — py -3.12 gen.py [a|b]
import sys, os, json, base64, urllib.request, time
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__))
KEY = [l.split('=', 1)[-1].strip() for l in open(r'C:\Users\강영준\Documents\gemini_key.txt', encoding='utf-8-sig') if l.strip()][0]
MODELS = ['gemini-3-pro-image', 'gemini-3-pro-image-preview', 'gemini-3.1-flash-image', 'gemini-3.1-flash-image-preview', 'gemini-3.1-flash-lite-image', 'gemini-2.5-flash-image']
BASE = ("One original cartoon character, full body, centered, on a perfectly plain flat pure white (#FFFFFF) background, no shadow on the ground, no scenery, "
        "no text, no letters, no numbers, no logos anywhere. Character: an ordinary Korean office worker in his early 40s who just quit his job, "
        "short black hair, round friendly face, simple dot eyes, wearing a plain navy cardigan over a white shirt, beige trousers. "
        "Not a real person, not a celebrity, not an expert or teacher, no glasses with brand, generic and original design, not resembling any existing mascot or webtoon character. "
        "Chunky 2.5-head-tall chibi proportions so the face reads clearly when the image is shrunk to 80 pixels tall. Strong clean silhouette, limited palette (navy, white, beige, skin tone, one small orange #FF5A00 accent only on the paper's corner stripe).")
P = {
 'a': BASE + " Pose: holding a single blank white bill letter (paper with only grey horizontal lines, no writing) in both hands, staring at it with a shocked face: wide eyes, open mouth, three small sweat drops. "
             "Style: flat 2D vector sticker illustration, bold even dark outlines (#18191d), flat colors, no gradients, plus a thick white sticker border around the whole figure.",
 'b': BASE + " Pose: one hand holding a single blank white bill letter (paper with only grey horizontal lines, no writing) at arm's length, other hand on his forehead, worried frowning face, mouth a small wavy line. "
             "Style: soft 3D clay-toy render, matte material, gentle studio lighting from the top left, smooth rounded shapes, no outlines.",
}
def gen(k):
    body = {'contents': [{'parts': [{'text': P[k]}]}], 'generationConfig': {'responseModalities': ['IMAGE'], 'imageConfig': {'aspectRatio': '1:1'}}}
    for m in MODELS:
        try:
            r = json.load(urllib.request.urlopen(urllib.request.Request(
                f'https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={KEY}',
                data=json.dumps(body).encode(), headers={'Content-Type': 'application/json'}), timeout=300))
            for p in r['candidates'][0]['content']['parts']:
                d = p.get('inlineData') or p.get('inline_data')
                if d:
                    out = os.path.join(H, f'raw_{k}.png'); open(out, 'wb').write(base64.b64decode(d['data']))
                    print(k, m, out); return m
            print(k, m, '이미지 없음', json.dumps(r)[:300])
        except Exception as e:
            msg = getattr(e, 'read', lambda: b'')()[:200]
            print(f'{k} {m} 실패 {e} {msg}', file=sys.stderr)
    return None
if __name__ == '__main__':
    used = {k: gen(k) for k in (sys.argv[1:] or ['a', 'b'])}
    json.dump({'models': used, 'prompts': P}, open(os.path.join(H, 'gen_log.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
