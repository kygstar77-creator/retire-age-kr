# 스토리보드 낱장으로 한 장 판 만들기(눈으로 보기용, 커밋 안 함): 앞 30초 촘촘히 + 나머지 고르게 24칸
#   py -3.12 work/research/strategy/format-1022/montage.py <id> ...  → frames/<id>/montage.jpg
import sys, os, json
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
F = ImageFont.truetype(r'C:\Windows\Fonts\malgunbd.ttf', 20)
def make(vid, n=24, cols=4):
    d = os.path.join(HERE, 'frames', vid); ix = json.load(open(os.path.join(d, 'index.json')))
    fr = ix['frames']; head = [f for f in fr if f[0] <= 30]
    rest = [f for f in fr if f[0] > 30]; k = n - len(head)
    pick = head + [rest[int(i * len(rest) / k)] for i in range(k)] if rest else head
    W, H = 320, 180; rows = (len(pick) + cols - 1) // cols
    M = Image.new('RGB', (cols * W, rows * H), 'black'); dr = ImageDraw.Draw(M)
    for i, (t, fn) in enumerate(pick):
        x, y = (i % cols) * W, (i // cols) * H
        M.paste(Image.open(os.path.join(d, fn)).resize((W, H)), (x, y))
        s = f'{int(t//60)}:{int(t%60):02d}'; dr.rectangle((x, y, x + 62, y + 26), fill='black'); dr.text((x + 4, y + 1), s, font=F, fill='yellow')
    M.save(os.path.join(d, 'montage.jpg'), quality=85); return os.path.join(d, 'montage.jpg')
if __name__ == '__main__':
    for v in sys.argv[1:]: print(make(v))
