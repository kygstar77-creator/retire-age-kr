import json,statistics as st
r=json.load(open('raw/mortgage.json',encoding='utf-8'))
a=[x for x in r if x['담보']=='아파트' and '분할' in x['상환방식']]
for t in ['변동금리','고정금리']:
    v=[x['대출최저'] for x in a if x['금리유형']==t and x['대출최저']]
    print(t,len(v),'최저금리 중앙',st.median(v),'범위',min(v),max(v),'은행수',len({x['은행'] for x in a if x['금리유형']==t}))
print('아파트 분할상환 옵션',len(a),'은행',len({x['은행'] for x in a}))
def cap(inc,rate,yrs=30,dsr=0.4):
    m=rate/100/12;n=yrs*12
    return inc*dsr/12/(m/(1-(1+m)**-n))
def pay(p,rate,yrs=30):
    m=rate/100/12;n=yrs*12
    return p*m/(1-(1+m)**-n)
base=st.median([x['대출최저'] for x in a if x['금리유형']=='변동금리'])
print('기준금리(변동 최저 중앙)',base)
for inc in [5000,7000,10000,15000]:
    c0=cap(inc*1e4,base); c3=cap(inc*1e4,base+3)
    print(inc,'만원: 스트레스없음 %.0f만 / +3%%p %.0f만 / 줄어듦 %.0f만 (%.1f%%)'%(c0/1e4,c3/1e4,(c0-c3)/1e4,100*(c0-c3)/c0), '실제월상환(한도대출) %.0f만'%(pay(c3,base)/1e4))
# 6억 다 받으려면 연봉
lo,hi=1e7,1e9
for _ in range(100):
    mid=(lo+hi)/2
    if cap(mid,base+3)<6e8: lo=mid
    else: hi=mid
print('6억 받으려면 연소득 %.0f만'%(hi/1e4), '6억 월상환 %.0f만'%(pay(6e8,base)/1e4))
