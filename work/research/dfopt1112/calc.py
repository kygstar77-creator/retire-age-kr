import pandas as pd, numpy as np
df=pd.read_excel('raw/q3.xlsx',sheet_name=0,header=None,engine='calamine').iloc[7:]
df.columns=['name','biz','guar','type','risk','sale','set','appr','amt_dc','amt_irp','amt','run_dc','run_irp','run','dsg_dc','dsg_irp','dsg','sites','r1m','r3m','r6m','r1y','r3y','fee']
num=lambda s: pd.to_numeric(s.replace('-',np.nan),errors='coerce')
for c in ['amt','run','dsg','r1m','r3m','r6m','r1y','r3y','fee']: df[c]=num(df[c])
df=df[df.name.notna()]
print('상품 수',len(df),'사업자 수',df.biz.nunique())
tot=df.amt.sum(); print('적립금 합계(원)',f'{tot:,.0f}', '조원',round(tot/1e12,2))
order=['초저위험','저위험','중위험','고위험']
for r in order:
    g=df[df.risk==r]; w=g.dropna(subset=['r1y'])
    wavg=(w.r1y*w.amt).sum()/w.amt.sum()
    print(r,'상품',len(g),'적립금 조원',round(g.amt.sum()/1e12,2),'비중%',round(g.amt.sum()/tot*100,1),
          '1Y 중앙',round(g.r1y.median(),2),'1Y 가중',round(wavg,2),'1Y 최고',g.r1y.max(),'최저',g.r1y.min(),'n1y',g.r1y.notna().sum(),
          '3M 음수',(g.r3m<0).sum(),'/',g.r3m.notna().sum(),'3Y 중앙',round(g.r3y.median(),2),'보수 중앙',g.fee.median(),
          '운용가입자',int(g.run.sum()))
print('운용 가입자 합계',int(df.run.sum()))
# 1억 1년 차이(가중 기준)
for r in order:
    g=df[(df.risk==r)].dropna(subset=['r1y']); wavg=(g.r1y*g.amt).sum()/g.amt.sum()
    print(r,'1천만원 1년',round(1e7*wavg/100))
hi=df[df.risk=='고위험'].dropna(subset=['r1y']).sort_values('r1y')
print('고위험 1Y 상위3'); print(hi.tail(3)[['name','r1y','r3m']].to_string())
print('고위험 1Y 하위3'); print(hi.head(3)[['name','r1y','r3m']].to_string())
print('guar',df.groupby('guar').amt.sum()/tot)
print('--- 추가')
ng=df[df.guar!='보장']
print('비보장 상품',len(ng),'3M 있음',ng.r3m.notna().sum(),'3M 음수',(ng.r3m<0).sum(),'1Y 있음',ng.r1y.notna().sum(),'1Y 음수',(ng.r1y<0).sum())
for r in order:
    g=df[df.risk==r]; print(r,'3M 중앙',round(g.r3m.median(),2),'6M 중앙',round(g.r6m.median(),2),'1Y 최고-최저',round(g.r1y.max()-g.r1y.min(),2))
print('보장 상품 3M 최저',df[df.guar=='보장'].r3m.min(), '보장 상품 수',(df.guar=='보장').sum())
print('지정 가입자 합계',int(df.dsg.sum()))
s=pd.read_excel('raw/q3.xlsx',sheet_name=1,header=None,engine='calamine'); print('시트2 1년 수익률 행',list(s.iloc[2,2:6]))
