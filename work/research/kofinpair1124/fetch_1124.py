# kofinpair1124 발행 날(11/24 22:4x firemap-write-b) 다시 받기 — 운용사 5곳 + 네이버 증권 ETF 분석 10종
import subprocess, os, sys, json
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(H, 'raw1124')
D = sys.argv[1] if len(sys.argv) > 1 else '20261124'
U = {
 f'tiger_210780_{D}.json': f'https://investments.miraeasset.com/tigeretf/ko/product/chart/prdct-item-list.ajax?ksdFund=KR7210780003&prfPrd=Week01&fixDate={D}&listCnt=100',
 f'ace_0139P0.json': 'https://papi.aceetf.co.kr/api/funds/K55101EQ7660/pdf?size=50',
 f'rise_315960_{D}.json': f'https://kbam.co.kr/api/products/etfs/4494/holdings?base_dt={D}',
 f'rise_266160_{D}.json': f'https://kbam.co.kr/api/products/etfs/4454/holdings?base_dt={D}',
 f'kodex_279530_{D}.json': f'https://m.samsungfund.com/api/v1/kodex/product-pdf/2ETF96.do?gijunYMD={D}',
}
for c in ['161510','0105E0','279530','315960','266160','210780','0139P0','322410','104530','0153K0']:
    U[f'etf_{c}.json'] = f'https://m.stock.naver.com/api/stock/{c}/etfAnalysis'
for f, u in U.items():
    p = os.path.join(R, f)
    r = subprocess.run(['curl','-s','-m','30','-A','Mozilla/5.0','-o',p,'-w','%{http_code}',u], capture_output=True, text=True)
    print(f, r.stdout, os.path.getsize(p) if os.path.exists(p) else 0)
