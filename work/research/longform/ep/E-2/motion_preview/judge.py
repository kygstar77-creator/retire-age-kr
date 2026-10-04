# e2_interest 움직이는 첫 화면 1초 시험·제미나이 심사(2026-10-04 motion). onesec_short.py 방식: 168px 목록 칸 크기.
import sys, os, json, base64, urllib.request, subprocess, imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__)); FF = imageio_ffmpeg.get_ffmpeg_exe()
KEY = [l.split('=', 1)[-1].strip() for l in open(r'C:\Users\강영준\Documents\gemini_key.txt', encoding='utf-8-sig') if l.strip()][0]
MODELS = ['gemini-3-flash-preview', 'gemini-3.8-flash', 'gemini-3.7-flash', 'gemini-3.5-flash-lite']
COMPD = os.path.join(H, '..', '..', '..', '..', 'cardshorts', 'e1_hynix_dd', 'onesec')
W, HH = 168, 299
def grab(mp4, n, out):
    subprocess.run([FF, '-v', 'error', '-y', '-i', mp4, '-vf', rf"select='eq(n\,{n})'", '-frames:v', '1', out], check=True); return Image.open(out)
def small(im):
    im = im.convert('RGB'); w, h = im.size; t = round(h * 9 / 16)
    if t < w: im = im.crop(((w - t) // 2, 0, (w - t) // 2 + t, h))
    return im.resize((W, HH), Image.LANCZOS)
tiles = [('새 0.0초', grab(os.path.join(H, 'e2_interest_with_intro.mp4'), 0, os.path.join(H, 'g0.png'))),
         ('새 0.5초', grab(os.path.join(H, 'e2_interest_with_intro.mp4'), 15, os.path.join(H, 'g15.png'))),
         ('새 1.0초', grab(os.path.join(H, 'e2_interest_with_intro.mp4'), 30, os.path.join(H, 'g30.png'))),
         ('새 2.0초', grab(os.path.join(H, 'e2_interest_with_intro.mp4'), 59, os.path.join(H, 'g59.png'))),
         ('옛 0.0초', grab(os.path.join(H, 'e2_interest_nointro.mp4'), 0, os.path.join(H, 'o0.png')))]
comp = sorted(x for x in os.listdir(COMPD) if x.endswith('.jpg'))[:5]
tiles += [('경쟁' + str(i + 1), Image.open(os.path.join(COMPD, c))) for i, c in enumerate(comp)]
F = ImageFont.truetype(r'C:\Windows\Fonts\malgunbd.ttf', 13)
b = Image.new('RGB', (len(tiles) * (W + 8) + 8, HH + 30), 'white'); d = ImageDraw.Draw(b)
for n, (lab, im) in enumerate(tiles): b.paste(small(im), (8 + n * (W + 8), 26)); d.text((8 + n * (W + 8), 5), lab, fill='black', font=F)
b.save(os.path.join(H, 'board168.png')); small(tiles[0][1]).save(os.path.join(H, 'first168.png'))
def ask(text, paths):
    parts = [{'text': text}] + [{'inline_data': {'mime_type': 'image/png', 'data': base64.b64encode(open(p, 'rb').read()).decode()}} for p in paths]
    for m in MODELS:
        try:
            r = urllib.request.Request(f'https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={KEY}', json.dumps({'contents': [{'parts': parts}]}).encode(), {'Content-Type': 'application/json'})
            return m, json.load(urllib.request.urlopen(r, timeout=120))['candidates'][0]['content']['parts'][0]['text']
        except Exception as e: print(m, str(e)[:80])
    return None, ''
m1, blind = ask('유튜브 쇼츠 목록에서 이 첫 화면(168px)을 1초 봤다. 무슨 내용의 영상인지 한 줄로 맞혀라.', [os.path.join(H, 'first168.png')])
m2, score = ask('한국 경제 쇼츠의 첫 1~2초 화면 비교판이다. "새"는 우리 새 첫 화면(0초·0.5초·1초·2초: 숫자 422가 굴러 서고 카드가 막대 비교로 바뀐다), "옛"은 지금 첫 화면(정지), 경쟁1~5는 경쟁 쇼츠 표지. '
                '쇼츠 피드에서 엄지를 멈추게 하는 힘·한눈에 읽힘·숫자 강조를 기준으로 "새"에 1~10점을 주고(7=공개 통과선), 옛보다 나은 점 1개·경쟁 1등보다 못한 점 1개·고칠 점 1개를 한 줄씩. 첫 줄은 "점수: N".', [os.path.join(H, 'board168.png')])
open(os.path.join(H, 'gemini.md'), 'w', encoding='utf-8').write(f'## 블라인드({m1})\n{blind}\n\n## 점수({m2})\n{score}\n')
print(blind); print(score)
