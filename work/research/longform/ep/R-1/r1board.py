# R-1 v6 비교판 — 새 화면 6장 · 지금 공개된 N-1 화면 · 경쟁 조회 상위 3편 화면을 한 장에(2026-10-03 cloud/r1-remake-1003)
#   python3 work/research/longform/ep/R-1/r1board.py
# 경쟁 썸네일(i.ytimg.com/vi/<ID>/maxresdefault.jpg)은 클라우드에서 403(프록시 거부)이라 받지 못했다 → 저장소에 이미 있는
# 스토리보드(yt-dlp 미리보기 이미지, research/yt/full/수페TV/<ID>_sb0.jpg)의 칸을 잘라 쓴다. 싱글파이어 IDwH4f-xA1g는 저장소에 화면이 없어 빈 칸.
# N-1은 영상 프레임이 저장소에 없다 → 공개 썸네일(meta.json thumb = thumb_n1l.png)만 놓는다.
import json, os, sys, urllib.request
from PIL import Image, ImageDraw, ImageFont
EP = os.path.dirname(os.path.abspath(__file__))
R = os.path.normpath(os.path.join(EP, '..', '..', '..'))          # work/research
FONT = os.path.normpath(os.path.join(R, '..', 'video', 'node_modules', 'pretendard', 'dist', 'public', 'static', 'alternative', 'Pretendard-Bold.ttf'))
OUR = ['00_open', '03_dep', '06_spytax', '10_rank', '15_posted', '17_thresh']
TOP3 = [('jSP16zTrEHY', '수페TV', 403909), ('IDwH4f-xA1g', '싱글파이어', 355077), ('rui4_d-5DvU', '수페TV', 325247)]   # study/2026-10-01.json views

def font(n):
    try: return ImageFont.truetype(FONT, n)
    except OSError: return ImageFont.load_default()

def try_thumb(vid, out):
    try:
        urllib.request.urlretrieve(f'https://i.ytimg.com/vi/{vid}/maxresdefault.jpg', out); return Image.open(out).convert('RGB'), None
    except Exception as e:  # 네트워크 막힘 기록
        return None, f'{type(e).__name__}: {e}'

def tile(sb, i):   # 3×3 스토리보드에서 i번째 칸(320×180)
    im = Image.open(sb).convert('RGB'); w, h = im.size[0] // 3, im.size[1] // 3
    return im.crop(((i % 3) * w, (i // 3) * h, (i % 3 + 1) * w, (i // 3 + 1) * h))

def main():
    W, PAD, TW, TH = 1920, 40, 600, 338
    H = 60 + (TH + 70) * 2 + 60 + (TH + 90) + 60 + (TH + 110) + 40
    bd = Image.new('RGB', (W, H), '#f6f7f9'); d = ImageDraw.Draw(bd)
    d.text((PAD, 18), 'R-1 v6 비교판 — 새 화면 · 공개된 N-1 · 경쟁 조회 상위 3편 (2026-10-03)', font=font(34), fill='#18191d')
    y = 80
    d.text((PAD, y), '① R-1 v6 새 화면 6장 (장면 끝 프레임, 1920×1080을 줄임)', font=font(28), fill='#ff5a00'); y += 44
    for k, name in enumerate(OUR):
        im = Image.open(os.path.join(EP, 'preview', 'stills', name + '.png')).convert('RGB').resize((TW, TH), Image.LANCZOS)
        x = PAD + (k % 3) * (TW + 20); yy = y + (k // 3) * (TH + 26)
        bd.paste(im, (x, yy)); d.text((x, yy + TH + 2), name, font=font(18), fill='#8a909b')
    y += 2 * (TH + 26) + 20
    d.text((PAD, y), '② 지금 공개된 N-1 — 영상 프레임은 저장소에 없음(확인 안 함). 공개 썸네일 thumb_n1l.png만', font=font(28), fill='#18191d'); y += 44
    n1 = Image.open(os.path.join(R, 'longform', 'ep', 'N-1', 'thumb_n1l.png')).convert('RGB').resize((TW, TH), Image.LANCZOS)
    bd.paste(n1, (PAD, y))
    d.text((PAD + TW + 30, y + 20), 'N-1 화면 지적(RULES 화면 글자·그래프 규칙, 10/3 22시):', font=font(24), fill='#4b515c')
    for j, t in enumerate(['· 상위 1%·상위 10%(겹치는 집단)를 나란히 그려 오해', '· "결정세액" 같은 원문 용어를 화면에 그대로',
                           '→ R-1 v6: 누적 구간 그래프 없음, 화면 글자는 쉬운 말', '   (실제 낸 세금·판 이익 세금·세금 뒤 통장)']):
        d.text((PAD + TW + 30, y + 64 + j * 38), t, font=font(24), fill='#4b515c')
    y += TH + 50
    d.text((PAD, y), '③ 경쟁 조회 상위 3편 (조회 수: study/2026-10-01.json) — 썸네일 내려받기 막힘 → 저장소 스토리보드 칸', font=font(28), fill='#18191d'); y += 44
    log = []
    for k, (vid, ch, views) in enumerate(TOP3):
        x = PAD + k * (TW + 20)
        im, err = try_thumb(vid, os.path.join('/tmp', f'{vid}.jpg'))
        if err: log.append(f'{vid}: {err}')
        sb = os.path.join(R, 'yt', 'full', ch, f'{vid}_sb0.jpg')
        if im is None and os.path.exists(sb):
            a, b = tile(sb, 5), tile(sb, 6 if vid == 'jSP16zTrEHY' else 8)
            im = Image.new('RGB', (640, 180), '#ffffff'); im.paste(a, (0, 0)); im.paste(b, (320, 0))
            im = im.resize((TW, int(TW * 180 / 640)), Image.LANCZOS); bd.paste(im, (x, y)); src = '스토리보드 칸 2개'
        elif im is not None:
            bd.paste(im.resize((TW, TH)), (x, y)); src = '썸네일'
        else:
            d.rectangle((x, y, x + TW, y + 180), outline='#8a909b', width=3); d.text((x + 20, y + 70), '저장소에 화면 없음 · 썸네일 다운로드 막힘', font=font(24), fill='#8a909b'); src = '없음'
        d.text((x, y + 196), f'{ch} {vid} · {views:,}회 · {src}', font=font(20), fill='#4b515c')
    out = os.path.join(EP, 'preview', 'board_r1_v6.png'); bd = bd.crop((0, 0, W, y + 240)); bd.save(out, optimize=True)
    open(os.path.join(EP, 'preview', 'board_download_log.txt'), 'w', encoding='utf-8').write('\n'.join(log) + '\n')
    print(out, bd.size, '다운로드 실패' if log else '', len(log))

if __name__ == '__main__':
    main()
