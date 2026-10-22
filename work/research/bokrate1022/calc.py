# 한국은행 기준금리(ECOS 722Y001 일별, 1999-05~2026-09-21) 변경일로
# '올린 뒤 다음 회의에서 쉬어 간' 경우를 찾아 그다음 변경이 인상이었는지·몇 달 뒤였는지 센다.
# 회의 간격: 2016년까지 매달(쉼 판정 40일 초과), 2017년부터 연 8회(60일 초과).
import json,datetime as dt,statistics as st
r=json.load(open('raw/ecos_base_daily.json',encoding='utf-8'))
ch=[];prev=None
for t,v,_ in r:
    v=float(v)
    if prev is not None and v!=prev: ch.append((dt.date(int(t[:4]),int(t[4:6]),int(t[6:])),prev,v))
    prev=v
D=lambda a,b:(b-a).days
hikes=[c for c in ch if c[2]>c[1]]
print('변경',len(ch),'인상',len(hikes))
res=[]
for i,c in enumerate(ch):
    if c[2]<=c[1]: continue
    nxt=ch[i+1] if i+1<len(ch) else None
    if nxt is None: print('마지막 인상',c);continue
    gap=D(c[0],nxt[0]); lim=60 if c[0].year>=2017 else 40
    if gap<=lim: continue   # 다음 회의에서 또 올림 = 쉬지 않음
    kind='인상' if nxt[2]>nxt[1] else '인하'
    res.append((c[0],nxt[0],kind,round(gap/30.44,1)))
for x in res: print(x)
up=[x for x in res if x[2]=='인상'];dn=[x for x in res if x[2]=='인하']
print('쉬어 간 경우',len(res),'다시 인상',len(up),'인하로 끝',len(dn))
m=sorted(x[3] for x in up);print('다시 올리기까지 개월',m,'중앙',st.median(m),'3개월 이내',sum(v<=3.5 for v in m))
# 2017년 뒤(연 8회)만
r17=[x for x in res if x[0].year>=2017];print('2017년 뒤',r17)
