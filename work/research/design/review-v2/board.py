# X-V1·X-CN-1 v2 디자인 검수 비교판 (firemap-designer 10/2) — scorecard/cap.py board() 틀, 우리 칸만 v2 로컬 캡처
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
D = Path(__file__).parent; R = D.parent; S = R.parent / "ventures/scorecard"
F = ImageFont.truetype("C:/Windows/Fonts/malgunbd.ttf", 36)
def board(name, items):
    ims = [(lab, Image.open(f).convert("RGB").resize((750, 1624))) for lab, f in items if Path(f).exists()]
    pad, top = 40, 70
    bd = Image.new("RGB", (len(ims)*(750+pad)+pad, 1624+top+pad), (230,230,230)); d = ImageDraw.Draw(bd)
    for i, (lab, im) in enumerate(ims):
        x = pad + i*(750+pad); bd.paste(im, (x, top)); d.text((x, 15), lab, fill=(200,0,0) if i < 2 else (0,0,0), font=F)
    bd.save(D / f"compare-{name}.png"); bd.resize((bd.width//3, bd.height//3)).save(D / f"compare-{name}-small.png"); print(name, bd.size)
tsc = R / "uk-pay/beat1/tsc-375-start.jpg"
board("xv1", [("우리 v2: X-V1", R/"uk-pay/v2/xv1-375.png"), ("우리 v1(반려)", S/"xv1-375.png"), ("1등: thesalarycalculator", tsc), ("기준: 토스", R/"quality/cap/toss-m.png")])
board("xcn1", [("우리 v2(17시 뒤)", R/"x-cn-1/v2/xcn1-375-after17.png"), ("우리 v1(반려)", S/"xcn1-375.png"), ("1등: 공식 누리집", S/"official-375.png"), ("기준: 토스", R/"quality/cap/toss-m.png")])
# v3 (firemap-venture-builder 10/5): 같은 판, 우리 칸만 v3 — v2를 둘째 칸에
board("xv1-v3", [("우리 v3: X-V1", R/"uk-pay/v3/xv1-375.png"), ("우리 v2(반려 6.67)", R/"uk-pay/v2/xv1-375.png"), ("1등: thesalarycalculator", tsc), ("기준: 토스", R/"quality/cap/toss-m.png")])
board("xcn1-v3", [("우리 v3: X-CN-1", R/"x-cn-1/v3/xcn1-375.png"), ("우리 v2(반려 6.83)", R/"x-cn-1/v2/xcn1-375-after17.png"), ("1등: 공식 누리집", S/"official-375.png"), ("기준: 토스", R/"quality/cap/toss-m.png")])
