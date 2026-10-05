# X-KR-1 판매 대표 이미지 1080×1080 (design/x-kr-1/spec.md ⓐ). 손 편집 금지 — 다시 그릴 수 있게.
#   py -3.12 make_thumb.py   (verify.py 가 만든 out/excel_values.json 의 판매 파일 값을 읽는다)
# 숫자는 엑셀이 실제로 계산한 값만 쓴다. checks.md 와 같은 값인지 assert.
import os, json
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'out')
INK, INK2, ORANGE, LINE, BG, WHITE = '#18191d', '#4e5968', '#ff5a00', '#e5e8eb', '#f6f7f9', '#ffffff'
# Pretendard 가 이 PC에 없다(C:/Windows/Fonts 실측) → 맑은 고딕. 디자이너 검수 때 알림.
REG, BOLD = 'C:/Windows/Fonts/malgun.ttf', 'C:/Windows/Fonts/malgunbd.ttf'
PICK = ['커피', '외식·배달', 'OTT·취미']  # 대표 이미지 3줄


def font(size, bold=False):
    return ImageFont.truetype(BOLD if bold else REG, size)


def main():
    xl = json.load(open(os.path.join(OUT, 'excel_values.json'), encoding='utf-8'))['가계부_은퇴나이_2026']
    oct_lines = xl['lines'][9:]  # 10월 줄(가장 최근 달)
    rows = sorted([(n, int(a), t) for n, a, t in oct_lines if n in PICK], key=lambda r: PICK.index(r[0]))
    assert [r[0] for r in rows] == PICK, rows
    checks = open(os.path.join(HERE, 'checks.md'), encoding='utf-8').read()
    for n, a, t in rows:
        assert f'{n} {a:,}원 {t}' in checks, (n, a, t)  # checks.md 와 같은 숫자
    assert f"큰 숫자 '{xl['B30']}'" in checks
    big = xl['B30']

    im = Image.new('RGB', (1080, 1080), BG)
    d = ImageDraw.Draw(im)
    X = 80
    d.text((X, 80), '가계부 엑셀 · 2026', font=font(28), fill=INK2)
    d.text((X, 140), '줄마다', font=font(64, True), fill=INK)
    d.text((X, 222), '은퇴 +N일', font=font(64, True), fill=INK)
    # 흰 카드 y 360~820
    d.rounded_rectangle((X, 360, 1000, 820), radius=32, fill=WHITE, outline=LINE, width=2)
    cx0, cx1, cx2 = X + 40, X + 330, 1000 - 40
    d.text((cx0, 392), '항목', font=font(24), fill=INK2)
    d.text((cx1, 392), '금액(월)', font=font(24), fill=INK2)
    d.text((cx2, 392), '은퇴 +N일', font=font(24, True), fill=INK2, anchor='ra')
    d.text((cx2, 426), '매달 반복된다고 가정할 때', font=font(22), fill=INK2, anchor='ra')
    y = 470
    for k, (n, a, t) in enumerate(rows):
        mid = y + 60
        d.text((cx0, mid), n, font=font(40), fill=INK, anchor='lm')
        d.text((cx1, mid), f'{a:,}원', font=font(40), fill=INK, anchor='lm')
        d.text((cx2, mid), t, font=font(56, True), fill=ORANGE, anchor='rm')
        if k < len(rows) - 1:
            d.line((cx0, y + 120, cx2, y + 120), fill=LINE, width=2)
        y += 110
    # 다크 카드 y 860~960 — 이 한 장만
    d.rounded_rectangle((X, 860, 1000, 960), radius=24, fill=INK)
    d.text((540, 910), f'은퇴 나이 {big}', font=font(44, True), fill=WHITE, anchor='mm')
    d.text((X, 1000), '예시 값 · 파이어맵 계산기와 같은 식 · 투자 조언 아님', font=font(22), fill=INK2)
    p = os.path.join(OUT, 'thumb_1080.png')
    im.save(p)
    print(p, rows, big)
    sheet_image()


def sheet_image():
    # 대표 이미지 2장째(순돌이 10/5 ③, 경쟁 4번 방식): verify.py가 Excel로 뽑은 실제 시트 2 화면(out/sheet2.png)
    # 디자인 반려 10/5 17:00 고칠 점 ①② — 카드 캔버스 폭 끝까지(좌우 60)·제목과 같은 왼쪽 축, 위쪽(은퇴 나이·큰 숫자·3칸)+자산 곡선만 크롭,
    # 입력 4줄·링크 줄·저축률 막대는 뺀다, 곡선의 은퇴 나이 지점에 주황 점 1. 글자 변경 0.
    sh = Image.open(os.path.join(OUT, 'sheet2.png')).convert('RGB')
    assert sh.size == (1042, 1710), sh.size  # 아래 크롭 좌표는 이 크기 실측(10/5 18:5x)
    top = sh.crop((20, 60, 945, 355))       # 은퇴 나이 라벨 ~ 3칸 밑줄
    cv = sh.crop((20, 683, 945, 1118))      # 자산 곡선 차트(테두리 포함)
    # 곡선 위 은퇴 나이 지점: x축 선(가장 긴 어두운 가로줄) 양 끝 = 20세·90세(make_xlsx 축 min 20·max 90)
    px = cv.load()
    best = (0, 0, 0, 0)
    for y in range(cv.height):
        run, st = 0, 0
        for x in range(cv.width + 1):  # 가장 긴 연속 구간(같은 줄의 눈금 글자 '0' 제외)
            if x < cv.width and sum(px[x, y]) < 200:
                st, run = (x, 1) if run == 0 else (st, run + 1)
                if run > best[0]:
                    best = (run, y, st, x)
            else:
                run = 0
    _, ay, x20, x90 = best
    age = int(json.load(open(os.path.join(OUT, 'excel_values.json'), encoding='utf-8'))['미리보기_12달']['B30'].rstrip('세'))
    ax = round(x20 + (age - 20) / 70 * (x90 - x20))
    oy = [y for y in range(cv.height) if (lambda c: c[0] > 230 and 60 < c[1] < 130 and c[2] < 60)(px[ax, y])]
    assert oy, (ax, '곡선 주황 픽셀 없음')
    ay_dot = sum(oy) / len(oy)
    M, PAD, GAP = 60, 20, 8
    W = 1080 - 2 * M - 2 * PAD
    k = W / top.width
    top = top.resize((W, round(top.height * k)), Image.LANCZOS)
    cv = cv.resize((W, round(cv.height * k)), Image.LANCZOS)
    im = Image.new('RGB', (1080, 1080), BG)
    d = ImageDraw.Draw(im)
    d.text((M, 60), '가계부 엑셀 · 2026', font=font(28), fill=INK2)
    d.text((M, 104), '「은퇴 나이」 시트 실제 화면', font=font(48, True), fill=INK)
    y0 = 188
    y1 = y0 + PAD + top.height + GAP + cv.height + PAD
    d.rounded_rectangle((M, y0, 1080 - M, y1), radius=20, fill=WHITE, outline=LINE, width=2)
    im.paste(top, (M + PAD, y0 + PAD))
    cy = y0 + PAD + top.height + GAP
    im.paste(cv, (M + PAD, cy))
    dx, dy, r = M + PAD + ax * k, cy + ay_dot * k, 11
    d.ellipse((dx - r, dy - r, dx + r, dy + r), fill=ORANGE, outline=WHITE, width=4)
    assert y1 < 1020, y1
    d.text((M, 1030), '예시 값 · 파이어맵 계산기와 같은 식 · 투자 조언 아님', font=font(22), fill=INK2)
    p = os.path.join(OUT, 'thumb_2_sheet.png')
    im.save(p)
    print(p, top.size, cv.size, 'card', (M, y0, 1080 - M, y1), 'dot', age, (round(dx), round(dy)), 'axis', x20, x90, ay)


if __name__ == '__main__':
    main()
