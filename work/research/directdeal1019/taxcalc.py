# directdeal1019 세금 예시 — 상증세법 35조①·시행령 26조②(기준금액 = 시가 30%와 3억 중 적은 것), 53조(성년 자녀 5천만원), 26조 세율, 69조 신고세액공제 3%
# 소득세법 101조·시행령 167조③(차액 3억 이상 또는 시가 5% 이상이면 시가로 양도가액 계산)
import sys; sys.stdout.reconfigure(encoding='utf-8')
def gift_tax(base):  # 과세표준(원) → 산출세액
    b = [(1e8, 0.10, 0), (5e8, 0.20, 1e7), (10e8, 0.30, 6e7), (30e8, 0.40, 1.6e8), (1e30, 0.50, 4.6e8)]
    for lim, r, ded in b:
        if base <= lim: return max(0, base * r - ded)
for sise, price in ((10e8, 7e8), (10e8, 6e8), (20e8, 15e8), (20e8, 14e8)):
    diff = sise - price; std = min(sise * 0.3, 3e8)
    gift = diff - std if diff >= std else 0
    base = max(0, gift - 5e7); t = gift_tax(base); t2 = t * 0.97
    yd = diff >= 3e8 or diff >= sise * 0.05
    print(f'시세 {sise/1e8:g}억 → {price/1e8:g}억에 매매: 차액 {diff/1e8:g}억 · 기준금액 {std/1e8:g}억 · 증여재산 {gift/1e8:g}억 · 공제 뒤 과표 {base/1e8:g}억 · 증여세 {t:,.0f}원(신고 3% 공제 뒤 {t2:,.0f}원) · 양도세 시가로 다시 계산: {yd}')
print('5% 선: 시세 10억이면', 10e8*0.05/1e4, '만원 · 20억이면', 20e8*0.05/1e4, '만원')
