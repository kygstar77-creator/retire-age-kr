# sangokapply1017 계산 — 공고문(청약홈 2026000458)·국토부 실거래(부평구 28237, 2026-01~10)
import json, statistics as st, datetime as dt, sys
sys.stdout.reconfigure(encoding='utf-8')
P = 745_000_000            # 59B 6~10층(76세대, 59B 중 가장 많은 줄) 공고문 표
dep1, dep2 = 10_000_000, 27_250_000
mid = [74_500_000]*6
bal = 260_750_000
assert dep1+dep2+sum(mid)+bal == P
print('59B 6-10층', P, '계약금', dep1+dep2, '중도금 합', sum(mid), '잔금', bal)
days = ['2027-03-09','2027-08-10','2028-02-08','2028-11-07','2029-03-06','2029-07-10']
move = dt.date(2029,12,1)  # 입주 예정월 2029.12 — 첫날로 가정(입주지정기간 미정)
yrs = sum(m*((move-dt.date.fromisoformat(d)).days/365) for m,d in zip(mid,days))
print('중도금×기간(원·년)', round(yrs))
for r in (0.01, 0.0466):
    print(f'이자 연 {r*100:.2f}% 단리', round(yrs*r))
rows=[r for r in json.load(open('bupyeong_trade_2026.json',encoding='utf-8')) if not r.get('cdealType')]
for nm,lo,hi in [('부평캐슬&더샵퍼스트',58,60.5),('부평캐슬&더샵퍼스트',83,86),('부평신일해피트리더루츠',58,60.5),('부평두산위브더파크',58,60.5)]:
    v=[(r['_ym'],r['dealDay'],r['floor'],int(r['dealAmount'].replace(',',''))) for r in rows if r['aptNm']==nm and lo<=float(r['excluUseAr'])<=hi]
    rec=[p for y,_,_,p in v if y>='202607']
    print(nm,lo,'1~10월',len(v),'중앙',st.median([p for *_,p in v]),'| 7월~',len(rec),'중앙',st.median(rec),'최고',max(rec),'최저',min(rec))
    print('   최근5', sorted(v)[-5:])
