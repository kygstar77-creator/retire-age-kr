# usrate1104 그림 2장 — 미국이 한국보다 기준금리가 높았던 기간(calc.py) · 1999~2026 금리차 선
import os,json,datetime as dt
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
def Bs(n): return fm.FontProperties(fname=F + r'\pd700.ttf', size=n)
ORG, INK, SUB, GR = '#EA580C', '#111827', '#4B5563', '#94A3B8'
# 01 기간 막대
rows=[('1999.6~2001.3',628,GR,'약 1년 9개월'),('2005.8~2007.9',769,GR,'약 2년 1개월'),('2018.3~2020.3',712,GR,'약 1년 11개월'),('2022.9~지금',1503,ORG,'4년 1개월째 (계속)')]
fig,ax=plt.subplots(figsize=(9,5.6),dpi=100); y=4
for lab,v,c,t in rows:
    ax.text(-30,y,lab,ha='right',va='center',fontproperties=Bs(17),color=INK)
    ax.barh(y,v,color=c,height=0.6); ax.text(v+30,y,t,va='center',fontproperties=Bs(18),color=ORG if c==ORG else INK); y-=1
ax.set_xlim(-560,2300); ax.set_ylim(0.4,4.6); ax.axis('off')
fig.text(0.05,0.9,'미국 기준금리가 한국보다 높았던 기간',fontproperties=Bs(22),color=INK)
fig.text(0.05,0.83,'1999년 5월부터 날짜별로 맞대 봄 · 미국은 목표 범위 위쪽 값',fontsize=14,color=SUB)
fig.text(0.05,0.03,'미 연준 FRED(DFEDTAR·DFEDTARU) · 한국은행 ECOS 기준금리 일별(11월 3일 조회)로 직접 계산',fontsize=11,color='#6B7280')
fig.subplots_adjust(top=0.8,bottom=0.08,left=0.03,right=0.97); fig.savefig('pkg/img/01.png',dpi=100); plt.close(fig)
# 02 금리차 선
o=json.load(open('raw/rates_1103.json',encoding='utf-8')); kd=json.load(open('raw/ecos_daily_1103.json',encoding='utf-8'))
us={}
for d,v in o['DFEDTAR']+o['DFEDTARU']: us[dt.date.fromisoformat(d)]=float(v)
kr={dt.date(int(t[:4]),int(t[4:6]),int(t[6:])):float(v) for t,v,_ in kd}
ds=sorted(set(us)&set(kr)); g=[us[d]-kr[d] for d in ds]
fig,ax=plt.subplots(figsize=(9,5.6),dpi=100)
ax.axhline(0,color=GR,lw=1)
ax.fill_between(ds,g,0,where=[x>0 for x in g],color=ORG,alpha=.35,lw=0)
ax.fill_between(ds,g,0,where=[x<=0 for x in g],color=GR,alpha=.35,lw=0)
ax.plot(ds,g,color=INK,lw=1.2)
ax.text(dt.date(2010,1,1),-3.55,'한국이 더 높음',fontproperties=Bs(15),color=SUB)
ax.text(dt.date(2024,6,1),2.15,'가장 클 때 2%p',fontproperties=Bs(13),color=ORG,ha='center')
ax.text(dt.date(2027,1,1),1.0,'지금\n1%p',fontproperties=Bs(14),color=ORG,ha='left',va='center')
for s in ['top','right']: ax.spines[s].set_visible(False)
ax.set_ylabel('차이 (%p, 퍼센트포인트)',fontsize=12,color=SUB); ax.tick_params(labelsize=11,colors=SUB)
fig.text(0.05,0.92,'미국 기준금리 − 한국 기준금리',fontproperties=Bs(22),color=INK)
fig.text(0.05,0.86,'주황 = 미국이 더 높은 날',fontsize=14,color=ORG)
fig.text(0.05,0.02,'미 연준 FRED · 한국은행 ECOS(11월 3일 조회)로 직접 계산',fontsize=11,color='#6B7280')
fig.subplots_adjust(top=0.82,bottom=0.1,left=0.1,right=0.97); fig.savefig('pkg/img/02.png',dpi=100); plt.close(fig)
print('ok')
