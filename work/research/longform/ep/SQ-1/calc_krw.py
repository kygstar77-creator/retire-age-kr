"""SQ-1 새 것 ③: calc_mix(달러)를 원화로 — 넣는 날·끝나는 날 원/달러(한국은행 ECOS 731Y001 매매기준율, 월말 마지막 영업일 값)
자료: raw/ecos_usdkrw_daily_1116.json(이 스크립트가 받음, 1차) + calc_mix.py 결과 함수
가정: 1억원을 넣는 날 환율로 달러로 바꿈, 끝날 환율로 원화로 되바꿈. 세금·환전 수수료·보수 밖 비용은 빼지 않음. 과거값이지 앞으로의 기대가 아님."""
import json, os, sys
sys.path.insert(0, os.path.abspath('../../../../'))
import apis
RAW='raw/ecos_usdkrw_daily_1116.json'
if not os.path.exists(RAW):
    k=apis.key('ecos')
    u=f'https://ecos.bok.or.kr/api/StatisticSearch/{k}/json/kr/1/5000/731Y001/D/20111001/20261031/0000001'
    d=apis._j(u, t=60); json.dump(d, open(RAW,'w',encoding='utf-8'), ensure_ascii=False)
rows=json.load(open(RAW,encoding='utf-8'))['StatisticSearch']['row']
me={}
for r in rows:
    t=r['TIME']; me[(int(t[:4]),int(t[4:6]))]=(t,float(r['DATA_VALUE']))  # 달마다 마지막 값이 남음
import io, contextlib
with contextlib.redirect_stdout(io.StringIO()):
    import calc_mix as cm
print(f'ECOS 행 {len(rows)} · 첫 {rows[0]["TIME"]} · 끝 {rows[-1]["TIME"]}')
for lbl,st in [('15년',(2011,10)),('최근 10년',(2016,10)),('최근 5년',(2021,10))]:
    f0,f1=me[st],me[(2026,10)]
    fx=f1[1]/f0[1]
    print(f'{lbl}: 환율 {f0[0]} {f0[1]:,.1f}원 → {f1[0]} {f1[1]:,.1f}원 (×{fx:.3f})')
    for w in [1.0,0.5,0.0]:
        v,c,m,y=cm.run(w,start=st)
        yrs=(2026-st[0])
        vk=v*fx
        print(f'  SCHD {int(w*100):>3}%: 달러 1억→{v:.2f}억 · 원화 1억→{vk:.2f}억 (연 {(vk**(1/yrs)-1)*100:.2f}%) · 환율 몫 {(vk-v):+.2f}억')
