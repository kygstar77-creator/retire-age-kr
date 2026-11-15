"""운용사 9/30 NAV 연환산(S13·S14)과 야후 adjclose 월봉 대조 (11/15 youtube-loop)"""
import json, datetime as dt
def load(s):
    r=json.load(open(f'raw/yh_{s}_1112.json',encoding='utf-8'))['chart']['result'][0]
    return {(dt.datetime.fromtimestamp(t,dt.UTC).year,dt.datetime.fromtimestamp(t,dt.UTC).month):a for t,a in zip(r['timestamp'],r['indicators']['adjclose'][0]['adjclose'])}
ref={'QQQ':{1:23.75,5:16.31,10:20.89},'SCHD':{1:23.36,5:9.48,10:12.44}}
for s in ('QQQ','SCHD'):
    d=load(s); e=(2026,9)
    for y,v in ref[s].items():
        b=(2026-y,9)
        if b not in d: print(s,y,'자료 없음'); continue
        c=((d[e]/d[b])**(1/y)-1)*100
        print(f'{s} {y}년 야후 {c:.2f}% · 운용사 {v:.2f}% · 차 {c-v:+.2f}%p · {"통과" if abs(c-v)<=0.5 else "벗어남"}')
