# 상속세 계산 (상증법 제14·18~26·69조, 시행령 제9조) — 2026-10-10 현행
def tax(base):
    br=[(1e8,.1,0),(5e8,.2,1e7),(10e8,.3,9e7),(30e8,.4,2.4e8),(9e18,.5,10.4e8)]
    lo=0
    for hi,r,c in br:
        if base<=hi: return c+(base-lo)*r
        lo=hi
def run(name,house,dep,spouse,dongeo,funeral=5e6):
    gross=house+dep-funeral
    fin=min(max(dep*.2,2e7) if dep>2e7 else dep,2e8)
    ded=5e8+fin+(5e8 if spouse else 0)+(min(house,6e8) if dongeo else 0)
    ded=min(ded,gross)
    base=max(gross-ded,0); t=tax(base); credit=t*.03
    print(f"{name}: 과세가액 {gross/1e4:,.0f}만 공제 {ded/1e4:,.0f}만 과표 {base/1e4:,.0f}만 산출 {t/1e4:,.1f}만 신고공제 {credit/1e4:,.1f}만 납부 {(t-credit)/1e4:,.1f}만")
    return t-credit
a=run("1차 배우자+자녀",10e8,2e8,True,False)
b=run("2차 자녀만",10e8,2e8,False,False)
c=run("2차 자녀만+동거주택",10e8,2e8,False,True)
print(f"차이 {(b-c)/1e4:,.1f}만")
