# pentax1115 직접 계산 — 출처 국세청 원천징수 연금소득(cntntsId=7888, raw/nts_7888.txt): 연금소득공제표·기본세율표·사적연금 세율
# 단위 만원. 지방소득세 10% 더함. 인적공제는 본인 기본공제 150만원만(경로우대·배우자·세액공제 안 셈 = 한계)
import sys; sys.stdout.reconfigure(encoding='utf-8')
def ded(t):
    if t<=350: d=t
    elif t<=700: d=350+(t-350)*0.4
    elif t<=1400: d=490+(t-700)*0.2
    else: d=630+(t-1400)*0.1
    return min(d,900)
BR=[(1400,.06,0),(5000,.15,126),(8800,.24,576),(15000,.35,1544),(30000,.38,1994),(50000,.40,2594),(100000,.42,3594),(1e12,.45,6594)]
def gen(base):
    base=max(base,0)
    for up,r,dd in BR:
        if base<=up: return base*r-dd
def comp(T):  # 연금소득만 있는 사람 종합과세 (지방세 포함)
    return gen(T-ded(T)-150)*1.1
out=[]
P=lambda *a: out.append(' '.join(str(x) for x in a))
P('§1 사적연금만, 65세(70세 미만 5.5%), 국민연금 0')
for X in [1200,1500,1501,1600,2000,3000]:
    sep = X*0.055 if X<=1500 else X*0.165
    P(f'  X={X} 분리={sep:.1f} 종합={comp(X):.1f} 공제={ded(X):.0f} 과표={X-ded(X)-150:.0f}')
P('§2 국민연금 과세분 Y + 사적연금 X=2000: 16.5% 분리(330) vs 종합에서 늘어나는 세금')
for Y in [0,300,600,900,1200,1500,1800,2400,3000]:
    inc=comp(Y+2000)-comp(Y) if Y>0 else comp(2000)
    P(f'  Y={Y} 종합 추가세금={inc:.1f} 분리=330.0 → {"종합" if inc<330 else "분리"} 유리 (Y만 종합 {comp(Y) if Y>0 else 0:.1f})')
# 갈림점 찾기
for X in [1600,2000,3000]:
    lo=None
    for Y in range(0,10001,10):
        inc=comp(Y+X)-comp(Y) if Y>0 else comp(X)
        if inc>=X*0.165: lo=Y;break
    P(f'§3 X={X}: 국민연금 과세분 연 {lo}만원(월 {lo/12:.0f}만원)부터 16.5%가 싸짐')
P('§4 1,500 이하도 종합 고를 수 있음(국세청 주 2 "선택적 분리과세"): Y=0')
for X in [600,1000,1500]:
    P(f'  X={X} 분리 5.5%={X*0.055:.1f} 종합={comp(X):.1f}')
P('§5 경계: 1,500 vs 1,600 분리끼리', f'{1500*0.055:.1f} → {1600*0.165:.1f} (차 {1600*0.165-1500*0.055:.1f})')
P('§6 종신형 3%(지방세 3.3%) vs 5.5%, 1,200만원:', f'{1200*0.033:.1f} vs {1200*0.055:.1f}')
open('calc_out.txt','w',encoding='utf-8').write('\n'.join(out)); print('\n'.join(out))
