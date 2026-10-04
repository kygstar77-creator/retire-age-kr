# 건보료 재산분 계산 — 시행령 별표4(byl4.txt) 등급표 + 제44조② 211.5원 + 장기요양 0.9448/7.19. firemap-write 2026-10-05
import re, json
rows=[]
for l in open('byl4.txt',encoding='utf-8'):
    for m in re.finditer(r'(\d+) ([\d,]+)(?: 초과)? ?(?:~ )?([\d,]*)(?: 이하)? ?([\d,]+)(?=\s|$)', l): pass
# 등급표는 직접 파싱: '등급 금액 점수' 3칸 + 3칸
T={}
for l in open('byl4.txt',encoding='utf-8'):
    t=l.split()
    # 한 줄 = [g, lo, 초과, ~, hi, 이하, pt] x2, 또는 1등급(450 이하)
    i=0
    while i<len(t):
        if t[i].isdigit() and i+2<len(t) and t[i+1].replace(',','').isdigit() and (t[i+2]=='이하' or t[i+2]=='초과'):
            g=int(t[i])
            if t[i+2]=='이하': hi=int(t[i+1].replace(',','')); lo=0; pt=int(t[i+3].replace(',','')); i+=4
            elif i+3<len(t) and t[i+3]=='~': lo=int(t[i+1].replace(',','')); hi=int(t[i+4].replace(',','')); pt=int(t[i+6].replace(',','')); i+=7
            else: lo=int(t[i+1].replace(',','')); hi=10**12; pt=int(t[i+3].replace(',','')); i+=4
            T[g]=(lo,hi,pt)
        else: i+=1
assert len(T)==60, len(T)
def score(man):  # 만원
    if man<=0: return 0,0
    for g,(lo,hi,pt) in sorted(T.items()):
        if lo<man<=hi: return g,pt
def mo(pt):
    k=pt*211.5; k=int(k//10*10)
    ltc=int(k*0.9448/7.19//10*10)
    return k,ltc
if __name__=='__main__':
    print('grades',len(T),T[1],T[18],T[60])
    out=[]
    for gwapyo in [10000,15000,20000,25000,30000,40000,50000,60000,80000]: # 과표 만원
        net=gwapyo-10000
        g,pt=score(net); k,l=mo(pt)
        print(f'과표 {gwapyo/10000:.1f}억 → 순 {net}만 등급{g} 점수{pt} 건보 {k:,} 요양 {l:,} 합 {k+l:,}')
    print('--- 공시가격 → 과표')
    for gp in [30000,50000,60000,90000]:
        for label,rate in [('일반60',0.60),('1세대1주택2026',0.43 if gp<=30000 else 0.44 if gp<=60000 else 0.45)]:
            gwa=gp*rate; net=gwa-10000; g,pt=score(net); k,l=mo(pt)
            print(f'공시 {gp/10000:.0f}억 {label} 과표 {gwa:.0f}만 순{net:.0f} 등급{g} 점수{pt} 건보 {k:,} 합 {k+l:,}')
    print('대출공제 5천만 예: 과표2.64억 → ', score(26400-10000), score(26400-10000-5000))
