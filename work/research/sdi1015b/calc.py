# 삼성SDI 지금 위치 계산 — 네이버 증권 일별 종가(수정주가, fchart) + 네이버 코스피 지수 + DART 분기 영업이익
import json, re, sys
sys.stdout.reconfigure(encoding='utf-8')
s=open('nv_sdi_long.xml','rb').read().decode('euc-kr','ignore')
sdi={x.split('|')[0]:float(x.split('|')[4]) for x in re.findall(r'data="([^"]+)"',s)}
kos={x['localDate']:x['closePrice'] for x in json.load(open('nv_kospi.json'))}
out=[]
def p(*a): out.append(' '.join(str(x) for x in a))
now='20261014'; c=sdi[now]
p('SDI 10/14 종가',c,'(10/13 종가는 네이버 565,000·야후 560,000으로 갈림 — 하루 등락률은 본문에 안 씀, 연합뉴스 정규장 +5.54%)')
p('SDI 1년 전 2025-10-14',sdi['20251014'],'배수 %.3f'%(c/sdi['20251014']),'상승 %.1f%%'%((c/sdi['20251014']-1)*100))
for lab,start in (('1년(2025-10-14~, 1년 전 같은 날 포함)', '20251014'),('5년(2021-10-15~, 수정주가)','20211015')):
    w={k:v for k,v in sdi.items() if start<=k<=now}
    hk=max(w,key=w.get); lk=min(w,key=w.get)
    pos=(c-w[lk])/(w[hk]-w[lk])*100
    p(lab,'최고',hk,w[hk],'최저',lk,w[lk],'| 고점 대비 %.1f%%'%((c/w[hk]-1)*100),'| 최저 대비 %.2f배'%(c/w[lk]),'| 범위 안 위치 %.1f%%'%pos)
p('SDI 6거래일 10/2→10/14',sdi['20261002'],c,'%.2f%%'%((c/sdi['20261002']-1)*100))
p('KOSPI 6거래일 10/2→10/14',kos['20261002'],kos[now],'%.2f pt'%(kos[now]-kos['20261002']),'%.2f%%'%((kos[now]/kos['20261002']-1)*100))
w={k:v for k,v in kos.items() if '20251015'<=k<=now}; hk=max(w,key=w.get)
p('KOSPI 1년 전 2025-10-14',kos.get('20251014'),'→',kos[now],'%.1f%%'%((kos[now]/kos['20251014']-1)*100),'| 1년 최고',hk,w[hk],'고점 대비 %.1f%%'%((kos[now]/w[hk]-1)*100))
p('SDI 1년 최고일 KOSPI 대비: SDI 4/29→10/14 %.1f%%'%((c/sdi['20260429']-1)*100))
# 분기 영업이익(연결, 억원) DART fnlttSinglAcnt
d=json.load(open('dart_fin.json',encoding='utf-8'))
def g(key,acc):
    for x in d[key]:
        if x['fs_div']=='CFS' and x['account_nm']==acc: return int(x['thstrm_amount'].replace(',',''))
q={}
for y in (2024,2025,2026):
    for rc,qq in (('11013','1Q'),('11012','2Q'),('11014','3Q')):
        k=f'{y}_{rc}'
        if k in d: q[f'{y} {qq}']=(g(k,'매출액'),g(k,'영업이익'))
    k=f'{y}_11011'
    if k in d:
        ys=[q[f'{y} {x}'] for x in ('1Q','2Q','3Q')]
        # 4분기 = 연간 - 3분기 보고서 누계(같은 해 보고서끼리; 분기 합은 이후 재작성분과 섞여 어긋난다)
        def cum(acc):
            for x in d[f'{y}_11014']:
                if x['fs_div']=='CFS' and x['account_nm']==acc: return int(x['thstrm_add_amount'].replace(',',''))
        q[f'{y} 4Q']=(g(k,'매출액')-cum('매출액'), g(k,'영업이익')-cum('영업이익'))
for k in sorted(q): p('분기',k,'매출 %.0f억'%(q[k][0]/1e8),'영업이익 %.0f억'%(q[k][1]/1e8))
p('2025 연간 영업이익 %.0f억'%(g('2025_11011','영업이익')/1e8),'매출 %.0f억'%(g('2025_11011','매출액')/1e8))
open('calc_out.txt','w',encoding='utf-8').write('\n'.join(out)+'\n'); print('\n'.join(out))
