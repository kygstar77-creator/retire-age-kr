"""K-1 11/8 PD 실사 9컷(1차 심사 못함 4컷은 같은 이름·길이로 클립 교체 — 교체 내역 README) 비교 그림 shotcmp/r38~r46.jpg — visual-designer 2026-11-08.
왼쪽 = 따라 한 경쟁 장면(이미 만든 shotcmp/rNN.jpg 왼쪽 반, 같은 경쟁 번호), 오른쪽 = 우리 클립의 실제 쓰는 구간(0~3초) 1.5초 프레임.
경쟁 캡처가 들어 있어 shotcmp/는 커밋하지 않는다(mkcmp.py와 같음). 사용: py -3.12 mk1108b.py
"""
import os, subprocess, imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); WORK = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
EP = os.path.join(WORK, 'research', 'longform', 'ep', 'K-1'); ST = os.path.join(WORK, 'video', 'public', 'bg', 'k1', 'stock')
FF = imageio_ffmpeg.get_ffmpeg_exe(); F = ImageFont.truetype(os.path.join(WORK, 'fonts', 'pd700.ttf'), 26)
# (비교 그림, 클립, 경쟁 #, 경쟁 캡처를 가져올 shotcmp, 왼쪽 판에서 자를 칸 — r01은 #3·#10 두 장이 나란히라 #10만)
FULL = (10, 56, 950, 586); R01_10 = (484, 56, 950, 586)
ROWS = [('r38', 'news_cup', '19', 'r07', FULL), ('r39', 'rain_drops', '6', 'r23', FULL), ('r40', 'money_count', '19', 'r07', FULL),
        ('r41', 'money_pen', '9', 'r15', FULL), ('r42', 'cup_stir', '6', 'r26', FULL), ('r43', 'notepad_calc', '10', 'r01', R01_10),
        ('r44', 'water_drops', '6', 'r23', FULL), ('r45', 'empty_office', '5', 'r19', FULL), ('r46', 'dining_room', '9', 'r15', FULL)]
def fit(im, w, h):
    im = im.copy(); im.thumbnail((w, h)); bg = Image.new('RGB', (w, h), (20, 20, 22)); bg.paste(im, ((w - im.width) // 2, (h - im.height) // 2)); return bg
for r, name, ref, src, box in ROWS:
    left = Image.open(os.path.join(EP, 'shotcmp', src + '.jpg')).convert('RGB').crop(box)
    tmp = os.path.join(os.environ.get('TEMP', '.'), f'k1b_{name}.png')
    subprocess.run([FF, '-y', '-loglevel', 'error', '-ss', '1.5', '-i', os.path.join(ST, name + '.mp4'), '-frames:v', '1', tmp], check=True)
    im = Image.new('RGB', (1920, 600), (250, 250, 248)); d = ImageDraw.Draw(im)
    d.text((20, 14), f'경쟁 #{ref}', font=F, fill=(40, 40, 40)); d.text((980, 14), f'우리 · bg/k1/stock/{name}.mp4 (쓰는 구간 0~3초)', font=F, fill=(40, 40, 40))
    im.paste(fit(left, 940, 530), (10, 56)); im.paste(fit(Image.open(tmp).convert('RGB'), 940, 530), (970, 56))
    im.save(os.path.join(EP, 'shotcmp', r + '.jpg'), quality=88); print(r, name)
