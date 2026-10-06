# 배우자 상속공제 사례 계산 — 상증법 18·19·21·24·26·69조, 민법 1009조
# 가정: 거주자 사망, 상속인 배우자+자녀 2명, 상속재산은 부동산(금융재산공제·동거주택공제 없음),
#       채무·사전증여·유증 없음, 기한 안 신고(신고세액공제 3%), 일괄공제 5억 선택.
import sys; sys.stdout.reconfigure(encoding='utf-8')
EOK=1e8
def tax(base):
    br=[(1,0,.1),(5,0.1,.2),(10,0.9,.3),(30,2.4,.4),(1e9,10.4,.5)]
    lo=0
    for hi,b,r in br:
        if base<=hi: return b+(base-lo)*r if lo else base*r
        lo=hi
def run(estate, spouse_got, kids=2):
    share=1.5/(1.5+kids)
    limit=min(estate*share,30)
    sp=max(5,min(spouse_got,limit))
    base=max(0,estate-5-sp)
    t=tax(base) if base>0 else 0
    return sp,base,t,t*0.97,share
for E in (10,15,20,30,50,70):
    for lab,got in (('배우자 0원',0),('법정상속분만큼',E*1.5/3.5)):
        sp,b,t,f,s=run(E,got)
        print(f'재산{E}억 {lab:8s} 배우자받음 {got:6.3f}억 공제{sp:6.3f}억 과표{b:6.3f}억 산출{t:7.4f}억 신고후{f:7.4f}억')
print('배우자 법정상속분(자녀2) =',1.5/3.5)
