# 블로그 경쟁 강도: 네이버 블로그 탭 상위 결과가 얼마나 최근 글인가(7일 안 글 비율). 새 글이 매일 밀려오는 키워드는 오래 못 버틴다.
import sys, json, re, time, urllib.request, urllib.parse
sys.stdout.reconfigure(encoding='utf-8')
UA={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126 Safari/537.36'}
allk=json.load(open('kw_blog_all.json',encoding='utf-8'))
INC=re.compile(r'SCHD|JEP[IQ]|QQQ|VOO|SPY|TLT|TMF|QLD|TQQQ|SOXL|ETF|배당|커버드콜|리얼티|나스닥|S&P|미국주식|미국채|국채|채권|ISA|IRP|연금|퇴직|연말정산|세액공제|소득공제|종합과세|소득세|양도세|양도소득|취득세|종부세|종합부동산|재산세|건강보험|건보|피부양|예금|적금|파킹|CMA|금리|환율|달러|환전|금값|금시세|금투자|청약|특별공급|특공|생애최초|디딤돌|보금자리|신생아|주담대|주택담보|전세|월세|보증보험|DSR|LTV|갭투자|아파트|실거래|재건축|재개발|분양|토지거래|부동산|재테크|파이어|노후|월급|연봉|실수령|가계부|순자산|신용점수|부업|앱테크|청년미래|청년도약|대출',re.I)
EXC=re.compile(r'주가$|시세$|지수$|증시|선물|코스피|코스닥|삼성|하이닉스|은행$|증권$|카드|보험사|채용|로그인|고객센터|앱$|어플|홈페이지|날씨|뉴스',re.I)
c=[(k,v['pc']+v['mo'],v) for k,v in allk.items() if INC.search(k) and not EXC.search(k)]
c=[x for x in c if int(sys.argv[2])<=x[1]<=int(sys.argv[3])]
c.sort(key=lambda x:-x[1]); c=c[:int(sys.argv[1])]
print(len(c),'candidates',file=sys.stderr)
def fresh(k):
    u='https://search.naver.com/search.naver?ssc=tab.blog.all&sm=tab_jum&query='+urllib.parse.quote(k)
    try: s=urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=20).read().decode('utf-8','ignore')
    except Exception: return None
    d=re.findall(r'>(\d{4}\.\d{1,2}\.\d{1,2}\.|\d+(?:일|시간|분|주) 전|어제)<',s)[:10]
    if not d: return None
    wk=sum(1 for x in d if ('시간' in x or '분' in x or x=='어제' or (x.endswith('일 전') and int(x.split('일')[0])<=7) or x=='2026.09.20.'))
    old=sum(1 for x in d if re.match(r'\d{4}\.',x) and x!='2026.09.20.')
    return {'n':len(d),'week':wk,'old':old}
out=[]
for i,(k,vol,v) in enumerate(c):
    f=fresh(k); time.sleep(0.5)
    if f: out.append({'k':k,'vol':vol,'mo':v['mo'],'comp':v['comp'],**f})
    if i%20==0: print(i,file=sys.stderr)
json.dump(out,open('kw_blog_comp.json','w',encoding='utf-8'),ensure_ascii=False,indent=0)
print(len(out))
