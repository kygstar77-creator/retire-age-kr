# schd1003 본문 그림 01 — 1년 변화(주가 vs 배당), 숫자 둘·차트 하나
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
fm.fontManager.addfont('C:/Windows/Fonts/malgunbd.ttf'); plt.rcParams['font.family']='Malgun Gothic'
fig,ax=plt.subplots(figsize=(10.8,10.8),dpi=100); fig.patch.set_facecolor('#FFFFFF')
lab=['주가\n27.53 → 32.66달러','배당(최근 1년 합계)\n1.0339 → 1.0541달러']; v=[18.6,2.0]
b=ax.bar(lab,v,color=['#9CA3AF','#2563EB'],width=0.55)
for r,x in zip(b,v): ax.text(r.get_x()+r.get_width()/2,x+0.6,f'+{x}%',ha='center',fontsize=56,fontweight='bold',color='#111827')
ax.set_ylim(0,23); ax.set_yticks([]); [ax.spines[s].set_visible(False) for s in ('top','right','left')]
ax.tick_params(axis='x',labelsize=24)
fig.suptitle('SCHD 1년 동안 얼마나 늘었나',fontsize=44,fontweight='bold',y=0.95)
fig.text(0.5,0.02,'주가: 2025.10.1 → 2026.10.1 종가(야후 파이낸스) · 배당: 슈왑 자산운용 분배금 내역',ha='center',fontsize=17,color='#6B7280')
plt.subplots_adjust(top=0.82,bottom=0.16); fig.savefig('pkg/img/01.png')
