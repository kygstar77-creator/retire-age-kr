# R-1 최종 비교판 — 우리 장면·썸네일을 참고 영상의 같은 종류 장면(저장소 프레임·스토리보드 잘라 씀) 옆에 놓는다(2026-10-03 cloud/r1-remake-1003)
#   python3 work/research/longform/ep/R-1/r1board.py → preview/board_r1_v6.png
# 참고 영상 화면은 이 클라우드에서 유튜브가 막혀 새로 받지 못했다 → 저장소에 이미 있는 프레임(research/yt/full/<채널>/<ID>/*.jpg)·스토리보드(<ID>_sb0.jpg)·썸네일(research/yt/design)만 쓴다.
import glob, os
from PIL import Image, ImageDraw, ImageFont
EP = os.path.dirname(os.path.abspath(__file__))
R = os.path.normpath(os.path.join(EP, '..', '..', '..'))
FONT = os.path.normpath(os.path.join(R, '..', 'video', 'node_modules', 'pretendard', 'dist', 'public', 'static', 'alternative', 'Pretendard-Bold.ttf'))
ST = os.path.join(EP, 'preview', 'stills')
REF = {  # ID: (채널, 조회 수와 출처)
    'F0xqJOo4DHQ': ('소수몽키', '1,400,000회(yt/full/소수몽키/index.json)'),
    '6qO_-JdXg1Y': ('소수몽키', '1,000,000회(yt/full/소수몽키/index.json)'),
    'jSP16zTrEHY': ('수페TV', '403,909회(study/2026-10-01.json)'),
    'VSstiIDWuKw': ('수페TV', '84,000회(yt/full/수페TV/index.json)'),
    '8ZObNM1xeGo': ('수페TV', '287,545회(yt/design/수페TV/meta.json)'),
}

def font(n):
    try: return ImageFont.truetype(FONT, n)
    except OSError: return ImageFont.load_default()

def frame(ch, vid, k):
    fs = sorted(glob.glob(os.path.join(R, 'yt', 'full', ch, vid, '*.jpg')))
    return Image.open(fs[k]).convert('RGB')

def sb_tile(ch, vid, i):
    im = Image.open(os.path.join(R, 'yt', 'full', ch, f'{vid}_sb0.jpg')).convert('RGB'); w, h = im.size[0] // 3, im.size[1] // 3
    return im.crop(((i % 3) * w, (i // 3) * h, (i % 3 + 1) * w, (i // 3 + 1) * h))

def thumb(ch, vid):
    return Image.open(sorted(glob.glob(os.path.join(R, 'yt', 'design', ch, f'*_{vid}.jpg')))[0]).convert('RGB')

def ours(name):
    return Image.open(os.path.join(ST, name) if not name.startswith('/') else name).convert('RGB')

ROWS = [  # (장면 종류, 우리 이미지, [(참고 이미지 함수, 참고 ID, 설명)])
    ('표·영수증 판', lambda: ours('08_spytax.png'), [(lambda: frame('소수몽키', 'F0xqJOo4DHQ', 4), 'F0xqJOo4DHQ', '번호 표 판'), (lambda: frame('수페TV', 'VSstiIDWuKw', 4), 'VSstiIDWuKw', 'ETF 표 판')]),
    ('막대·순위 + 표시', lambda: ours('15_start.png'), [(lambda: frame('소수몽키', '6qO_-JdXg1Y', 8), '6qO_-JdXg1Y', '막대 그래프 + 말풍선'), (lambda: sb_tile('수페TV', 'jSP16zTrEHY', 5), 'jSP16zTrEHY', '지수 게이지')]),
    ('선 그래프 + 값 꼬리표', lambda: ours('06_swing.png'), [(lambda: frame('수페TV', 'VSstiIDWuKw', 32), 'VSstiIDWuKw', '차트 + 검은 값 표'), (lambda: sb_tile('수페TV', 'jSP16zTrEHY', 6), 'jSP16zTrEHY', '선 그래프 + 값 박스')]),
    ('사례·설명 판', lambda: ours('16_caseA.png'), [(lambda: frame('소수몽키', '6qO_-JdXg1Y', 32), '6qO_-JdXg1Y', '설명 판 + 형광 띠'), (lambda: frame('소수몽키', 'F0xqJOo4DHQ', 36), 'F0xqJOo4DHQ', '사진 판 + 띠 글자')]),
    ('썸네일', lambda: ours(os.path.join(EP, 'thumb_r1_final.png')), [(lambda: thumb('수페TV', '8ZObNM1xeGo'), '8ZObNM1xeGo', '같은 분야(노후 금액)'), (lambda: thumb('수페TV', 'jSP16zTrEHY'), 'jSP16zTrEHY', '환율·ETF')]),
]

def main():
    W, PAD, TW, TH = 2400, 30, 760, 428
    H = 120 + len(ROWS) * (TH + 96) + 260
    bd = Image.new('RGB', (W, H), '#f6f7f9'); d = ImageDraw.Draw(bd)
    d.text((PAD, 24), 'R-1 최종 비교판 — 왼쪽: 우리(1920×1080 장면 끝 프레임·썸네일) · 오른쪽 두 칸: 참고 영상의 같은 종류 장면(저장소 프레임·스토리보드)', font=font(34), fill='#18191d')
    d.text((PAD, 72), '참고 화면은 이 클라우드에서 유튜브가 막혀 새로 받지 못함 — 저장소에 이미 있던 프레임(해상도 낮음)만 씀', font=font(24), fill='#8a909b')
    y = 120
    for kind, ourf, refs in ROWS:
        d.text((PAD, y), kind, font=font(30), fill='#ff5a00')
        y += 42
        bd.paste(ourf().resize((TW, TH), Image.LANCZOS), (PAD, y))
        d.text((PAD, y + TH + 6), '우리 R-1', font=font(22), fill='#18191d')
        for j, (rf, vid, desc) in enumerate(refs):
            x = PAD + (j + 1) * (TW + 30)
            bd.paste(rf().resize((TW, TH), Image.LANCZOS), (x, y))
            d.text((x, y + TH + 6), f'{REF[vid][0]} · {desc} · {REF[vid][1]}', font=font(20), fill='#4b515c')
        y += TH + 54
    d.text((PAD, y), '참고 영상 링크', font=font(28), fill='#18191d'); y += 40
    for vid, (ch, views) in REF.items():
        d.text((PAD, y), f'{ch}  https://www.youtube.com/watch?v={vid}  · {views}', font=font(24), fill='#18191d'); y += 34
    bd = bd.crop((0, 0, W, y + 20))
    out = os.path.join(EP, 'preview', 'board_r1_v6.png'); bd.save(out, optimize=True); print(out, bd.size)

if __name__ == '__main__':
    main()
