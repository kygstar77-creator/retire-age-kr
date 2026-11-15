import re,glob,sys
sys.stdout.reconfigure(encoding='utf-8')
for f in sorted(glob.glob('raw/funetf_*.txt')):
    t=re.sub(r'\s+',' ',open(f,encoding='utf-8').read())
    name=re.search(r'ETF 상세 (.+?)\((\w+)\)은\(는\) (\S+)이 운용하는 (.+?) 추종',t)
    top=re.search(r'상위 구성종목은 (.+?) 등입니다',t)
    nav=re.search(r'기간별 수익률 (\S+) 기준 구분 1개월 3개월 6개월 1년 3년 5년 연초이후 상장이후 NAV \(%\) ((?:\S+ ){8})',t)
    real=re.search(r'실부담비율 (\S+)',t)
    asof=re.search(r'구성종목[^가-힣]{0,40}?(\d\d\.\d\d\.\d\d) 기준',t) or re.search(r'(\d\d\.\d\d\.\d\d) 기준[^.]{0,60}구성',t)
    print(f[11:-4],'|',name.group(1) if name else '?','|',name.group(4) if name else '','|',top.group(1) if top else '?','|NAV',nav.group(1) if nav else '',nav.group(2) if nav else '?','|실부담',real.group(1) if real else '?','|구성기준',asof.group(1) if asof else '?')
