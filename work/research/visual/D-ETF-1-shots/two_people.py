"""D-ETF-1 0장 '이 숫자를 두 사람에게 대 볼 거예요' 판 — 좌우 두 실사(얼굴 없음) + 대본 말 그대로 이름표. visual 10/27.
새 심사관 3·4·5차 '찻잔 둘·손 한 장으로는 두 사람(은퇴자·직장인)이 안 갈림 → 좌우 두 칸으로' 반영. 글자는 대본 '은퇴해서 지금 생활비가 필요한 분 / 앞으로 오래 모을 직장인'.
사진: Pexels 8164676 Kindel Media(나이 든 손) · 6964247 Mikhail Nilov(계산기 옆 노트에 적는 손). → ep/D-ETF-1/fig/two_people.png, public/bg/detf/fig/two_people.png"""
import os, subprocess, shutil
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
H = os.path.dirname(os.path.abspath(__file__)); WORK = os.path.abspath(os.path.join(H, '..', '..', '..'))
PUB = os.path.join(WORK, 'video', 'public'); FF = os.path.join(WORK, 'video', 'node_modules', '@remotion', 'compositor-win32-x64-msvc', 'ffmpeg.exe')
EP = os.path.join(WORK, 'research', 'longform', 'ep', 'D-ETF-1')
def grab(cid, sec):
    out = os.path.join(os.environ.get('TEMP', '.'), f'tp_{cid}.png')
    subprocess.run([FF, '-y', '-loglevel', 'error', '-ss', str(sec), '-i', os.path.join(PUB, 'bg', 'detf', 'stock', f'{cid}.mp4'), '-frames:v', '1', out], check=True)
    return Image.open(out).convert('RGB').resize((1920, 1080))
def font(sz):
    f = ImageFont.truetype(os.path.join(WORK, 'fonts', 'NotoSansKR-Black.ttf'), sz); f.set_variation_by_name('Black'); return f
a = grab(8164676, 4).crop((150, 0, 1106, 1080)); b = grab(6964247, 3).crop((520, 0, 1476, 1080))
im = Image.new('RGB', (1920, 1080), (16, 17, 20)); im.paste(ImageEnhance.Brightness(a).enhance(0.8), (0, 0)); im.paste(ImageEnhance.Brightness(b).enhance(0.8), (964, 0))
m = Image.new('L', im.size, 0); d = ImageDraw.Draw(m)
for y in range(560, 1080): d.line([(0, y), (1920, y)], fill=int(235 * min(1, (y - 560) / 300)))
im = Image.composite(Image.new('RGB', im.size, (12, 13, 16)), im, m); d = ImageDraw.Draw(im)
for x0, (t1, t2) in ((0, ('은퇴해서 지금', '생활비가 필요한 분')), (964, ('앞으로 오래 모을', '직장인'))):
    for k, t in enumerate((t1, t2)):
        f = font(80); w = d.textlength(t, font=f)
        d.text((x0 + (956 - w) / 2, 700 + k * 104), t, font=f, fill=(255, 255, 255), stroke_width=4, stroke_fill=(0, 0, 0))
for p in (os.path.join(EP, 'fig', 'two_people.png'), os.path.join(PUB, 'bg', 'detf', 'fig', 'two_people.png')): im.save(p)
print('ok')
