import sys, pandas as pd, numpy as np
sys.stdout.reconfigure(encoding='utf-8')
x='raw/q3.xlsx'
d=pd.read_excel(x,sheet_name=0,engine='calamine',header=None).iloc[7:].copy()
d=d[d[0].notna()]
cols=['name','co','guar','type','risk','sale','set','appr','aDC','aIRP','aTot','uDC','uIRP','uTot','jDC','jIRP','jTot','sites','r1m','r3m','r6m','r1y','r3y','fee']
print('ncol',d.shape[1]); d=d.iloc[:,:24]; d.columns=cols
def num(c): return pd.to_numeric(d[c].replace('-',np.nan),errors='coerce')
for c in ['aTot','r1m','r3m','r6m','r1y','r3y','fee','aDC','aIRP']: d[c]=num(c)
print('N',len(d)); print(d.guar.value_counts().to_dict()); print(d.risk.value_counts().to_dict())
print(pd.crosstab(d.guar,d.risk))
print('sale',d.sale.value_counts().to_dict())
T=d.aTot.sum(); print('total',T, 'check DC+IRP',(d.aDC.fillna(0)+d.aIRP.fillna(0)).sum())
print((d.groupby('risk').aTot.sum()/T*100).round(2))
print((d.groupby('guar').aTot.sum()/T*100).round(2))
s=pd.read_excel(x,sheet_name=1,engine='calamine',header=None); print(s.iloc[2].tolist()); print(s.iloc[4].tolist())
for r in [0.025,0.0656,0.0939,0.1395]: print(r, 1000*r,'만원')
nb=d[d.guar!='보장']
print('nonguar',len(nb),'3M valid',nb.r3m.notna().sum(),'neg',(nb.r3m<0).sum(),'zero',(nb.r3m==0).sum())
print('1Y valid',nb.r1y.notna().sum(),'pos',(nb.r1y>0).sum())
b=nb[nb.r1y.notna()&nb.r3m.notna()]; print('both',len(b), '1y pos among both',(b.r1y>0).sum())
for k,g in d.groupby('risk'):
    print(k,'n',len(g),'3M med',g.r3m.median(),'n3m',g.r3m.notna().sum(),'6M med',g.r6m.median(),'1Y med',g.r1y.median(),'1Y min/max',g.r1y.min(),g.r1y.max(),'fee med',g.fee.median(),'fee0 share',(g.fee==0).mean().round(3),'fee n',g.fee.notna().sum())
g=d[d.guar=='보장']; print('guar 3M med',g.r3m.median(),'fee med',g.fee.median(),'fee0',(g.fee==0).sum(),g.fee.notna().sum())
print('nonguar 6M valid',nb.r6m.notna().sum(),'6M pos',(nb.r6m>0).sum(),'6M med',nb.r6m.median())
# implied first 9 months: (1+1y)/(1+3m)-1
m=nb.r1y.notna()&nb.r3m.notna(); pre=(1+nb.r1y[m]/100)/(1+nb.r3m[m]/100)-1
print('pre9m >|3m loss| cases', (pre*100 > -nb.r3m[m]).sum(), 'of', m.sum())
print(d[d.r3y.round(2)==100.97][['name','co','risk','r1y','r3y']])
print('max r3y',d.r3y.max())
print('1Y neg nonguar',nb[nb.r1y<=0][['name','risk','r1y','r3m']])
print('3M nonneg nonguar',nb[nb.r3m>=0][['name','risk','r3m']])
