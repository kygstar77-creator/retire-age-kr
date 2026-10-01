# 비교판: 우리 375px 첫 화면 | 같은 일을 하는 참조 화면들
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
D = Path(__file__).parent; C = D / "cap"
F = ImageFont.truetype("C:/Windows/Fonts/malgunbd.ttf", 36)
PAIRS = {
 "salary": ["salary", "naver-salary", "toss", "banksalad"],
 "severance": ["severance", "naver-severance", "toss", "banksalad"],
 "unemp": ["unemp", "naver-unemp", "toss", "banksalad"],
 "home": ["home", "toss", "banksalad", "calcnet"],
 "guide": ["guide", "banksalad", "toss", "calcnet"],
}
for name, keys in PAIRS.items():
    ims = [Image.open(C / f"{k}-m.png").convert("RGB") for k in keys]
    w, h = ims[0].size; pad = 40; top = 70
    board = Image.new("RGB", (len(ims)*(w+pad)+pad, h+top+pad), (230,230,230))
    d = ImageDraw.Draw(board)
    for i, (k, im) in enumerate(zip(keys, ims)):
        x = pad + i*(w+pad)
        board.paste(im.resize((w, h)), (x, top))
        d.text((x, 15), ("우리: " if i == 0 else "참조: ") + k, fill=(200,0,0) if i == 0 else (0,0,0), font=F)
    board.save(D / f"compare-{name}.png")
    board.resize((board.width//3, board.height//3)).save(D / f"compare-{name}-small.png")
    print(name, board.size)
