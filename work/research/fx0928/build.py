import sys, json
sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
sys.stdout.reconfigure(encoding='utf-8')
import blogimg
d=json.load(open('data.json',encoding='utf-8'))
def ser(s): return {r[0][:10]:r[1] for r in d['yahoo'][s]['rows']}
tnx,wti,gold=ser('^TNX'),ser('CL=F'),ser('GC=F')
krw={'2026-09-18':1380.3,'2026-09-21':1383.8,'2026-09-22':1384.3,'2026-09-23':1360.0}  # ECOS 731Y001 매매기준율
days=['2026-09-18','2026-09-21','2026-09-22','2026-09-23','2026-09-24','2026-09-25']
lab={'2026-09-18':'18일(금)','2026-09-21':'21일(월)','2026-09-22':'22일(화)','2026-09-23':'23일(수)','2026-09-24':'24일(목)','2026-09-25':'25일(금)'}
rows=[]
for x in days:
    rows.append([lab[x], f"{tnx[x]:.2f}%", f"{krw[x]:,.1f}원" if x in krw else '휴장', f"{wti[x]:.2f}", f"{gold[x]:,.2f}"])
for r in rows: print(r)
src='출처: 야후 파이낸스 시세(10년물·WTI·금), 한국은행 ECOS 매매기준율(원달러), 9월 27일 조회'
blogimg.table('pkg/img/02.png','날짜별 값 (2026년 9월)',['날짜','미국 10년물','원달러','WTI(달러)','금(달러)'],rows,hl_col=None,src=src,
  note='원달러 24·25일은 추석 연휴로 서울 외환시장이 쉬었어요')
def r2(v): return round(v,2)
t0,t1=r2(tnx['2026-09-18']),r2(tnx['2026-09-25']); w0,w1=r2(wti['2026-09-18']),r2(wti['2026-09-25']); g0,g1=r2(gold['2026-09-18']),r2(gold['2026-09-25'])
summ=[['미국 10년물 국채금리',f'{t0:.2f}%',f'{t1:.2f}%',f'{t1-t0:+.2f}%p'],
      ['원달러(23일까지)','1,380.3원','1,360.0원',f'{1360.0-1380.3:+.1f}원'],
      ['WTI 유가',f'{w0:.2f}달러',f'{w1:.2f}달러',f'{w1-w0:+.2f}달러({(w1/w0-1)*100:+.2f}%)'],
      ['금',f'{g0:,.2f}달러',f'{g1:,.2f}달러',f'{g1-g0:+.2f}달러({(g1/g0-1)*100:+.2f}%)']]
for r in summ: print(r)
blogimg.table('pkg/img/01.png','지난주 한 주 동안 (9월 18일 → 25일)',['항목','18일','25일','변화'],summ,hl_col=3,src=src,
  note='원달러는 추석 휴장으로 23일 값까지예요')
rate=[['한국은행 기준금리','3.00%','2026년 9월 25일'],['미국 연준 기준금리(목표범위)','3.75~4.00%','2026년 9월 27일']]
blogimg.table('pkg/img/03.png','기준금리는 지금',['','금리','기준일'],rate,src='출처: 한국은행 ECOS, 세인트루이스 연준 FRED(DFEDTARL·DFEDTARU)')
