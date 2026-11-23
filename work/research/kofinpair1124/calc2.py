# kofinpair1124 — 운용사 구성종목(1차)으로 금융 비중·반도체 두 종목 비중 직접 합산 (firemap-write-b 2026-11-23)
# 금융 = 은행·보험·증권·카드·금융지주·재보험(de1s_kofin/prepub_1121.txt와 같은 기준). 한국자산신탁(부동산 신탁)·다우기술·일반 지주는 금융 아님.
import json, sys, os
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(H, 'raw')
FIN = {'DB손해보험','삼성카드','기업은행','NH투자증권','JB금융지주','우리금융지주','코리안리','BNK금융지주','삼성증권','한국금융지주',
       '하나금융지주','KB금융','신한지주','삼성화재','키움증권','iM금융지주','대신증권','현대해상','삼성생명','한화생명','미래에셋증권',
       '교보증권','현대차증권','서울보증보험'}
SEMI = {'삼성전자', 'SK하이닉스'}
def show(name, date, rows, note=''):
    tot = sum(w for _, w in rows)
    fin = sorted([(n, w) for n, w in rows if n in FIN], key=lambda x: -x[1])
    semi = sum(w for n, w in rows if n in SEMI)
    f = sum(w for _, w in fin)
    print(f'{name} | {date} | 종목 {len(rows)} | 비중 합 {tot:.2f} | 금융 {len(fin)}종목 {f:.2f}% | 삼성전자+SK하이닉스 {semi:.2f}% | 금융 상위3 {fin[:3]} {note}')
t = json.load(open(os.path.join(R, 'tiger_210780_20261120.json'), encoding='utf-8'))['rtnData']
show('TIGER 코스피고배당 210780', '2026-11-20', [(x['memItemname'].strip(), x['stockRate'] or 0) for x in t])
a = json.load(open(os.path.join(R, 'ace_0139P0_20261123.json'), encoding='utf-8'))
show('ACE 고배당주 0139P0', a['std_DT'], [(x['sec_NM'], x['wg']) for x in a['pdfList']])
for c, nm in (('315960', 'RISE 대형고배당10TR'), ('266160', 'RISE 고배당')):
    d = json.load(open(os.path.join(R, f'rise_{c}_20261120.json'), encoding='utf-8'))
    show(f'{nm} {c}', d['base_dt'], [(x['item_nm'], x['ratio']) for x in d['items']],
         f"(운용사 화면 상위 {len(d['items'])}종목만, 전체 {d['total_count']}종목)" if d['total_count'] > len(d['items']) else '')
k = json.load(open(os.path.join(R, 'kodex_279530_20261120.json'), encoding='utf-8'))['pdf']
L = k['list']; tot = sum(float(x['evalA'] or 0) for x in L)
show('KODEX 고배당주 279530', k['gijunYMD'], [(x['secNm'], float(x['evalA'] or 0) / tot * 100) for x in L])
print('PLUS 고배당주 161510 | 2026-11-20 | 금융 55.645% (cardshorts/de1s_kofin/prepub_1121.txt, 한화 API)')
print('SOL 코리아고배당 0105E0 | 2026-11-20 | 금융 56.463% (cardshorts/de1s_kofin/prepub_1121.txt, 신한 구성종목 평가금액)')
