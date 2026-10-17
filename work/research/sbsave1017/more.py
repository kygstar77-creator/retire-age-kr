# 추가 계산(10/17 09시대): 누구나 가입(join_deny=1)·12개월만 / 청주 단비 확인
exec(open('calc.py',encoding='utf-8').read().split("print('§0")[0])
base={(b['fin_co_no'],b['fin_prdt_cd']):b for g in ('020000','030300') for b in d[g]['base']}
for o in d['030300']['opt']:
    b=base[(o['fin_co_no'],o['fin_prdt_cd'])]
    if '단비' in b['fin_prdt_nm'] or '펫팸' in b['fin_prdt_nm']: print('청주', b['fin_prdt_nm'], o['save_trm'], o['intr_rate'], o['intr_rate2'], o['rsrv_type'], b['join_way'])
for name,R in (('은행',B),('저축은행',S)):
    bb=bestco(R,'12',lambda x:x['deny']=='1')
    v=sorted(x['r'] for x in bb.values())
    print(name,'누구나 12개월 회사별 최고 기본 중앙',st.median(v),len(v),'곳 | 3.5% 이상',sum(1 for x in v if x>=3.5),'곳')
    top=sorted(bb.values(),key=lambda x:-x['r'])[:6]
    for x in top: print('   ',x['co'],x['prd'],x['r'],x['rmax'],x['lim'],x['rs'])
# 예시 계산: 단리 적금 이자 = 월액 × 금리 × (n(n+1)/2)/12
def si(m, r, n=12): return m * r / 100 * (n * (n + 1) / 2) / 12
for m, r, lab in ((200000, 6.5, '애큐온 처음만난적금 월 20만(한도)'), (500000, 3.75, '저축은행 중앙 월 50만'), (500000, 3.05, '은행 중앙 월 50만')):
    g = si(m, r); print(f'{lab} {r}% 원금 {m*12:,} 세전 {g:,.0f} 세후 {g*(1-TAX):,.0f}')
g = si(500000, 3.75); print('비과세종합저축이면 세전 그대로', f'{g:,.0f}', '세금 아낌', f'{g*TAX:,.0f}')
print('600만원 목돈 3.75% 예금 1년 세후', f'{6000000*0.0375*(1-TAX):,.0f}', '/ 적금 세후 대비 배', round(6000000*0.0375/si(500000,3.75),2))
print('평균 맡긴 개월', 78/12)
# 12개월 기본 5% 이상 상품: 가입 대상
print('== 12개월 기본 5% 이상')
seen=set()
for o in d['030300']['opt']:
    if o['save_trm']!='12' or (o['intr_rate'] or 0)<5: continue
    b=base[(o['fin_co_no'],o['fin_prdt_cd'])]; k=(b['kor_co_nm'],b['fin_prdt_nm'])
    if k in seen: continue
    seen.add(k); print(' ',k[0],k[1],o['intr_rate'],o['rsrv_type'],b['max_limit'],'|',b['join_way'],'|',(b['join_member'] or '')[:50])
