# X-KR-1 대표 이미지 v2 비교판 (firemap-venture-builder 10/5) — 우리 1장째·2장째(실제 시트) / 크몽 '가계부' 검색 1페이지(경쟁 1~4, 디자이너 10/1 실측 화면)
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
D = Path(__file__).parent; O = D.parent.parent / "ventures/x-kr-1/out"
F = ImageFont.truetype("C:/Windows/Fonts/malgunbd.ttf", 32)
H = 900
items = [("우리 1장째(수정 없음)", O/"thumb_1080.png"), ("우리 2장째: 실제 시트 화면(새)", O/"thumb_2_sheet.png"), ("경쟁: 크몽 '가계부' 1페이지(2·3·4번 포함)", D/"comp-kmong-search.jpg")]
ims = []
for lab, f in items:
    im = Image.open(f).convert("RGB"); k = H / im.height; ims.append((lab, im.resize((int(im.width * k), H))))
pad, top = 40, 70
bd = Image.new("RGB", (sum(i.width for _, i in ims) + pad * (len(ims) + 1), H + top + pad), (230, 230, 230)); d = ImageDraw.Draw(bd)
x = pad
for i, (lab, im) in enumerate(ims):
    bd.paste(im, (x, top)); d.text((x, 18), lab, fill=(200, 0, 0) if i < 2 else (0, 0, 0), font=F); x += im.width + pad
bd.save(D / "compare-v2.png"); print(bd.size)
