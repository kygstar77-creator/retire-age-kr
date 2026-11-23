# 운용사 PDF로 금융 비중 직접 합산 — 분류는 cardshorts/de1s_kofin/prepub_1121.txt와 같음(은행·보험·증권·카드·금융지주·재보험, 한국앤컴퍼니 등 일반 지주 제외)
import json, sys, os, glob
sys.stdout.reconfigure(encoding='utf-8')
FIN = {'DB손해보험','삼성카드','기업은행','NH투자증권','JB금융지주','우리금융지주','코리안리','BNK금융지주','삼성증권','한국금융지주',
       '하나금융지주','KB금융','신한지주','삼성화재','키움증권','iM금융지주','대신증권','현대해상','삼성생명','한화생명','미래에셋증권','DGB금융지주'}
H = os.path.dirname(os.path.abspath(__file__))
for f in sorted(glob.glob(os.path.join(H, 'raw', 'kodex_*.json'))):
    d = json.load(open(f, encoding='utf-8'))['pdf']; L = d['list']
    tot = sum(float(x['evalA'] or 0) for x in L); stk = sum(float(x['evalA'] or 0) for x in L if x['secNm'] != '원화예금')
    fin = [x for x in L if x['secNm'] in FIN]; s = sum(float(x['evalA']) for x in fin)
    print(os.path.basename(f), d['gijunYMD'], f'금융 {len(fin)}종목 {s/tot*100:.2f}% (현금 포함 분모) · 주식만 {s/stk*100:.2f}%')
