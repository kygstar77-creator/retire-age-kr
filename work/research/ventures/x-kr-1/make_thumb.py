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


if __name__ == '__main__':
    main()
