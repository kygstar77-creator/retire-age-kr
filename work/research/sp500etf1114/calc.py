# 국내 상장 S&P500 ETF 5개: 종가+분배금 재투자로 3년·1년 총수익을 직접 계산(야후 일별 종가·분배 이벤트)하고
# 운용사·FunETF 공시 NAV 수익률·실부담비율과 맞대 본다
import json, datetime as dt, sys
sys.stdout.reconfigure(encoding='utf-8')
names={'360750':'TIGER','379800':'KODEX','360200':'ACE','379780':'RISE','433330':'SOL'}
# FunETF 11/12 기준 (raw/funetf_*.txt) — NAV 수익률(분배금 재투자 세전), 총보수, TER, 실부담비율
fun={'360750':(1.87,81.82,93.69,0.0068,0.06,0.0939,209543),
     '379800':(1.91,82.29,94.93,0.0062,0.07,0.1067,105227),
     '360200':(1.89,81.72,94.39,0.0047,0.07,0.0922,38979),
     '379780':(2.05,82.16,94.07,0.0047,0.07,0.0973,15254),
     '433330':(1.70,81.56,None,0.0047,0.08,0.1424,2960)}
END=dt.date(2026,11,12)
def series(c):
    d=json.load(open(f'raw/yahoo_{c}.json',encoding='utf-8'))['chart']['result'][0]
    rows=[(dt.datetime.fromtimestamp(t+9*3600, dt.UTC).date(),v) for t,v in zip(d['timestamp'],d['indicators']['quote'][0]['close']) if v]
    divs={dt.datetime.fromtimestamp(int(k)+9*3600, dt.UTC).date():v['amount'] for k,v in d.get('events',{}).get('dividends',{}).items()}
    return rows,divs
def tr(c,start):
    rows,divs=series(c)
    rows=[r for r in rows if start<=r[0]<=END]
    sh=1.0; p0=rows[0][1]; got=0
    for day,px in rows[1:]:
        if day in divs: sh+=sh*divs[day]/px; got+=1
    return (sh*rows[-1][1]/p0-1)*100, rows[0][0], rows[-1][0], got
out=[]
for c in names:
    r1=tr(c,dt.date(2025,11,12)); r3=tr(c,dt.date(2023,11,13))
    f=fun[c]
    print(f"{names[c]}: 직접계산 1년 {r1[0]:.2f}% 3년 {r3[0]:.2f}% ({r3[1]}~{r3[2]}, 분배 {r3[3]}회) | 공시 NAV 1년 {f[0]} 3년 {f[1]} 5년 {f[2]} | 총보수 {f[3]}% TER {f[4]}% 실부담 {f[5]}% | 순자산 {f[6]}억")
    out.append((names[c],f))
r3=[f[1] for _,f in out]; print('공시 3년 최고-최저 %.2f%%p' % (max(r3)-min(r3)))
r1=[f[0] for _,f in out]; print('공시 1년 최고-최저 %.2f%%p' % (max(r1)-min(r1)))
for n,f in out:
    print(f"{n}: 1억원 3년 뒤 {1e8*(1+f[1]/100):,.0f}원 · 실부담비율/총보수 {f[5]/f[3]:.0f}배 · 1억원 1년 실부담 {1e8*f[5]/100:,.0f}원 · 총보수만 {1e8*f[3]/100:,.0f}원")
print('KODEX 기초지수 3년 84.12 vs NAV 82.29 차이 %.2f%%p, 5년 98.46 vs 94.93 차이 %.2f%%p' % (84.12-82.29, 98.46-94.93))
