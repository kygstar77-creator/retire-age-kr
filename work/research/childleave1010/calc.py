def pay(w,months):
    t=0
    for m in range(1,months+1):
        if m<=3: a=min(max(w,70),250)
        elif m<=6: a=min(max(w,70),200)
        else: a=min(max(w*0.8,70),160)
        t+=a
    return t
for w in (200,250,300,400):
    print(w, [round(pay(w,k),1) for k in (3,6,12)], 'ratio12', round(pay(w,12)/(w*12)*100,1), '월별', [min(max(w,70),250),min(max(w,70),200),min(max(w*0.8,70),160)])
# 6+6 상한: 한 명 6개월
six=[250,250,300,350,400,450]; print(sum(six), sum(six)*2)
# 한 명 6개월 일반(300만)
print(pay(300,6))
