# -*- coding: utf-8 -*-
import json,io,os,glob,re,statistics as st
sgg=json.load(io.open('work/research/seoul_sgg.json',encoding='utf-8'))
def num(s): return int(re.sub(r'[^\d]','',s or '0') or 0)
def load(code,ym,kind):
    p=f'work/research/rt/{code}_{ym}_{kind}.json'
    if not os.path.exists(p): return []
    return json.load(io.open(p,encoding='utf-8'))
rows={}
for code,name in sgg.items():
    o=load(code,'202609','offi_trade'); a=load(code,'202609','trade')
    def per(rs):
        v=[]
        for r in rs:
            ar=float(r.get('excluUseAr') or 0); amt=num(r.get('dealAmount'))
            if ar>0 and amt>0:
                v.append(amt*10000/ar*3.3058)   # 3.3m2당 원
        return v
    po,pa=per(o),per(a)
    rows[name]={'offi_n':len(o),'apt_n':len(a),
        'offi_med':(st.median(po) if po else None),'apt_med':(st.median(pa) if pa else None)}
tot_o=sum(v['offi_n'] for v in rows.values()); tot_a=sum(v['apt_n'] for v in rows.values())
OUT=io.open('work/research/offiseoul/raw/calc.txt','w',encoding='utf-8')
import builtins
_p=print
def print(*a,**k): _p(*a,**k,file=OUT)
print('== 서울 25개 구 2026년 9월 계약분(2026-09-23 수집) ==')
print(f'오피스텔 매매 신고 {tot_o}건 / 아파트 매매 신고 {tot_a}건')
L=[]
for n,v in rows.items():
    if v['offi_med'] and v['apt_med'] and v['offi_n']>=3:
        ratio=v['offi_med']/v['apt_med']*100
        L.append((ratio,n,v['offi_med'],v['apt_med'],v['offi_n'],v['apt_n']))
L.sort()
print('\n구 | 오피 3.3m2당(만) | 아파트 3.3m2당(만) | 오피/아파트 % | 오피건수 | 아파트건수')
for ratio,n,om,am,on,an in L:
    print(f'{n} | {om/10000:,.0f} | {am/10000:,.0f} | {ratio:.1f}% | {on} | {an}')
print('\n-- 건수 3건 미만이라 뺀 구 --')
for n,v in rows.items():
    if not(v['offi_med'] and v['apt_med'] and v['offi_n']>=3):
        print(n, v['offi_n'], v['apt_n'])

OUT.close()
