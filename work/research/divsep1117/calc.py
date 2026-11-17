# divsep1117 — 고배당기업 배당 분리과세(조특법 104조의27) vs 종합과세(소득세법 55·56·62조) 직접 계산
# 단위 만원. 가정: 배당은 전부 고배당기업 현금배당(가산 대상), 다른 이자·배당 없음, O = 배당 뺀 다른 소득 과세표준(공제 뒤).
# 배당세액공제 한도 = 일반산출 − 비교산출(조세심판원 결정 요지) → 최종 = max(일반산출 − 가산액, 비교산출)
import sys; sys.stdout.reconfigure(encoding='utf-8')
B=[(1400,.06),(5000,.15),(8800,.24),(15000,.35),(30000,.38),(50000,.40),(100000,.42),(10**9,.45)]
def basic(x):
    t=0;lo=0
    for hi,r in B:
        if x>lo: t+=(min(x,hi)-lo)*r
        lo=hi
    return t
S=[(2000,.14),(30000,.20),(500000,.25),(10**9,.30)]
def sep(d):
    t=0;lo=0
    for hi,r in S:
        if d>lo: t+=(min(d,hi)-lo)*r
        lo=hi
    return t
def comb(o,d):
    if d<=2000: return .14*d+basic(o)
    g=.1*(d-2000)
    m1=280+basic(o+(d-2000)+g)
    m2=.14*d+basic(o)
    return max(m1-g,m2)
def row(o,d):
    c=comb(o,d)-basic(o); s=sep(d)
    return c,s
# 검산: 104조의27 표의 누진공제 값
assert abs(sep(30000)-5880)<1e-6 and abs(sep(500000)-123380)<1e-6
assert abs(basic(5000)-624)<1e-6 and abs(basic(8800)-1536)<1e-6 and abs(basic(15000)-3706)<1e-6
print('배당에 붙는 소득세(국세, 만원) — 종합 vs 분리, 지방세 10% 별도')
for d in (3000,5000,10000):
    print(f'\n배당 {d:,}만원')
    for o in (0,1400,3000,5000,8000,10000,15000,30000):
        c,s=row(o,d); print(f'  다른 과표 {o:>6,}: 종합 {c:8.1f} 분리 {s:8.1f} 차이(분리−종합) {s-c:+8.1f}  지방세 포함 {1.1*(s-c):+8.1f}')
    # 분리가 유리해지는 다른 과표(1만원 단위)
    be=next(o for o in range(0,200001) if row(o,d)[1] < row(o,d)[0]-1e-9)
    print(f'  → 분리과세가 싸지는 다른 소득 과세표준: {be:,}만원부터')
# 다른 소득 0원일 때 배당 얼마부터 분리가 유리?
be2=next((d for d in range(2001,2000001,10) if row(0,d)[1]<row(0,d)[0]-1e-9),None)
print('\n다른 소득 0원: 분리과세가 싸지는 배당액', be2)
for d in (3000,5000,10000,20000,30000):
    c,s=row(0,d); print(f'  배당 {d:,}: 종합 실효 {c/d*100:.1f}% 분리 실효 {s/d*100:.1f}%')
# 연금만 받는 경우(소득세법 47조의2 연금소득공제, 기본공제 150만원) — 월 300만원
def pension_deduct(p):
    if p<=350: d=p
    elif p<=700: d=350+.4*(p-350)
    elif p<=1400: d=490+.2*(p-700)
    else: d=630+.1*(p-1400)
    return min(d,900)
p=300*12; print(f'\n연금 월 300만원: 총연금 {p} 공제 {pension_deduct(p):.0f} 과세표준 {p-pension_deduct(p)-150:.0f}만원')
# 연봉 1억원 직장인(소득세법 47조 근로소득공제) — 근로소득공제·기본공제만
def wage_deduct(w):
    if w<=500: d=.7*w
    elif w<=1500: d=350+.4*(w-500)
    elif w<=4500: d=750+.15*(w-1500)
    elif w<=10000: d=1200+.05*(w-4500)
    else: d=1475+.02*(w-10000)
    return min(d,2000)
print(f'연봉 1억원: 근로소득공제 {wage_deduct(10000):.0f} 과세표준(기본공제만) {10000-wage_deduct(10000)-150:.0f}만원')
