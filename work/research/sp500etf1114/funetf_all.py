# FunETF 상품 페이지의 '분배금 한눈에 보기'를 국내 상장 S&P500 ETF 다섯 개에 대해 받는다(운용사 공시를 모은 2차 자료)
import sys, re, subprocess
sys.stdout.reconfigure(encoding='utf-8')
def isin(code):
    body = 'KR7' + code + '00'
    digits = ''.join(str(int(c, 36)) for c in body)
    s = 0
    for i, d in enumerate(reversed(digits)):
        n = int(d)
        if i % 2 == 0: n *= 2
        s += n // 10 + n % 10
    return body + str((10 - s % 10) % 10)
for code in sys.argv[1:]:
    i = isin(code); out = f'raw/funetf_{code}.txt'
    subprocess.run([sys.executable, 'fetch_page.py', f'https://www.funetf.co.kr/product/etf/view/{i}', out], timeout=110)
    t = open(out, encoding='utf-8').read()
    k = t.find('분배금 한눈에 보기')
    print(code, i, re.sub(r'\n+', '|', t[k:k+900]) if k >= 0 else 'NO')
