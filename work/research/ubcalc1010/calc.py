# ubcalc1010 계산 — 고용보험법 제45·46·50조 별표1 (src/utils/unemploymentBenefit.js 와 같은 식), 2026년 이직
import sys; sys.stdout.reconfigure(encoding='utf-8')
from datetime import date
import calendar
CAP=113500; MW=10320
def minus3(d):
    y,m=d.year,d.month-3
    if m<=0: y-=1; m+=12
    return date(y,m,min(d.day,calendar.monthrange(y,m)[1]))
def daily(last, monthly, hours=8):
    from datetime import timedelta
    end=last+timedelta(days=1); n=(end-minus3(end)).days
    avg=monthly*3/n; base=min(avg,CAP); byrate=int(base*0.6+1e-6)
    floor=int(hours*MW*0.8+1e-6)
    return n,avg,byrate,floor,max(byrate,floor)
T={'u':[120,150,180,210,240],'o':[120,180,210,240,270]}
def days(m,o=False):
    b=0 if m<12 else 1 if m<36 else 2 if m<60 else 3 if m<120 else 4
    return T['o' if o else 'u'][b]
n,avg,byrate,floor,d=daily(date(2026,9,30),3_000_000)
print('월300만 이직 9/30: 3개월일수',n,'평균임금',round(avg),'60%',byrate,'하한',floor,'일액',d)
for lab,m in [('전직장 합산 27+18=45개월',45),('현 직장만 18개월',18)]:
    ds=days(m); print(lab,ds,'일',d*ds,'원')
print('차이',d*180-d*150)
# 다른 구간 사례: 현 직장 11개월 + 전 직장 8개월 = 19개월
for m in (11,19,34,36,59,60): print(m,'개월',days(m),days(m,True))
