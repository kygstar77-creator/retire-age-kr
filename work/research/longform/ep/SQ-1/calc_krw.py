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
# 11/20 copywriter 요청: 원화로 잰 최대 낙폭 — 달마다 (달러 평가액 × 그 달 마지막 영업일 매매기준율), 달러 낙폭과 같은 월말 간격
def run_krw(w, start=(2011,10), end=(2026,10)):
    ms=[m for m in cm.months if start<=m<=end]
    fx0=me[ms[0]][1]
    a=w; b=1-w; v=1.0; vk=1.0; peak=1.0; mdd=0.0; at=None; pk_m=ms[0]; pk_at=None
    for p,m in zip(ms,ms[1:]):
        a*=cm.S[m]/cm.S[p]; b*=cm.Q[m]/cm.Q[p]; v=a+b
        vk=v*me[m][1]/fx0
        if vk>peak: peak=vk; pk_m=m
        dd=vk/peak-1
        if dd<mdd: mdd=dd; at=(pk_m,m)
        if m[1]==10: a=v*w; b=v*(1-w)
    return vk, mdd, at
print('원화 최대 낙폭(월말 평가액×월말 매매기준율, 1억원을 넣는 날 환율로 달러 전환)')
for lbl,st in [('15년',(2011,10)),('최근 10년',(2016,10)),('최근 5년',(2021,10))]:
    for w in [1.0,0.5,0.0]:
        vk,mdd,at=run_krw(w,start=st)
        _,_,mu,_=cm.run(w,start=st)
        print(f'  {lbl} SCHD {int(w*100):>3}%: 원화 끝값 {vk:.2f}억 · 원화 최대낙폭 {mdd*100:.1f}% (고점 {at[0][0]}-{at[0][1]:02d} → 바닥 {at[1][0]}-{at[1][1]:02d}) · 달러 최대낙폭 {mu*100:.1f}%')
