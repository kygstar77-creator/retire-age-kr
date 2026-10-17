import sys, json, os; sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import blogimg as B
d=json.load(open('raw_20261017.json',encoding='utf-8')); krx,gc,fx=d['KRX'],d['GC'],d['FX']; OZ=31.1034768
def on(s,day): ks=[k for k in s if k<=day]; return s[ks[-1]]
def bf(s,day): ks=[k for k in s if k<day]; return s[ks[-1]]
prem={day:k/(bf(gc,day)*on(fx,day)/OZ)-1 for day,k in krx.items() if day>='2025-10-02'}
days=sorted(prem); ys=[round(prem[x]*100,2) for x in days]
xs=[x[2:7].replace('-','.') if i==0 or x[5:7]!=days[i-1][5:7] else x[2:10] for i,x in enumerate(days)]
xs=[x[2:].replace('-','.') for x in days]  # 25.10.02 꼴, 눈금은 8개만 찍힌다
mx=max(prem,key=prem.get); mn=min(prem,key=prem.get)
marks=[(days.index('2025-10-02'),ys[0],'산 날 +6.3%','ink'),(days.index(mx),round(prem[mx]*100,1),'가장 높을 때 +18.7%','red'),(days.index(mn),round(prem[mn]*100,1),'가장 낮을 때 -5.2%','red'),(days.index('2026-10-06'),round(prem['2026-10-06']*100,1),'판 날 -1.4%','ink')]
B.line('pkg/img/02.png','KRX 금 웃돈, 1년 동안 이만큼 흔들렸어요',xs,ys,marks=marks,unit='국제 값보다 비싼 정도(%)',src='네이버 증권 KRX 금 · 야후 파이낸스 금 선물 · 한국은행 ECOS 환율 · 파이어맵 계산(어림값)')
print(len(days), mx, round(prem[mx]*100,2), mn, round(prem[mn]*100,2), days[-1], ys[-1], round(prem['2026-10-06']*100,2))
