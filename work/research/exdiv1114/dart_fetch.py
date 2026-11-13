# 2025 사업연도 결산배당: 코스피 '현금ㆍ현물배당결정' 공시 목록 (DART list API, pblntf_ty=I, corp_cls=Y)
import sys,json,urllib.request,time
sys.path.insert(0,r'C:/Users/강영준/Documents/GitHub/retire-age-kr/work')
sys.stdout.reconfigure(encoding='utf-8')
import apis
k=apis.key('dart')
out=[]
for bgn,end in [('20260115','20260214'),('20260215','20260314'),('20260315','20260415')]:
    p=1
    while True:
        u=f'https://opendart.fss.or.kr/api/list.json?crtfc_key={k}&bgn_de={bgn}&end_de={end}&pblntf_ty=I&corp_cls=Y&page_count=100&page_no={p}'
        d=json.load(urllib.request.urlopen(u,timeout=30))
        if d.get('status')!='000': print(bgn,p,d.get('status'),d.get('message')); break
        for x in d['list']:
            if '현금ㆍ현물배당결정' in x['report_nm']: out.append({k2:x[k2] for k2 in ('corp_name','stock_code','corp_code','report_nm','rcept_no','rcept_dt')})
        if p>=d['total_page']: break
        p+=1; time.sleep(0.15)
    print(bgn,end,'pages',p,'so far',len(out))
for o in out: o['report_nm']=o['report_nm'].strip()
json.dump(out,open('raw/dart_divlist.json','w',encoding='utf-8'),ensure_ascii=False,indent=0)
print(len(out), len({o['corp_code'] for o in out}))
