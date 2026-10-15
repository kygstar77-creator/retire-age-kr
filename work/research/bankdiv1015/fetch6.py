# 자회사 배당결정 공시 본문에서 자회사(은행) 이름 확인
import json, sys, urllib.request, re, io, zipfile, html
sys.path.insert(0, '../../'); import apis
key = apis.key('DART'); L = json.load(open('src/dart_div2026_list.json', encoding='utf-8'))
for n, rows in L.items():
    for r in rows:
        if '자회사' not in r['report_nm']: continue
        z = zipfile.ZipFile(io.BytesIO(urllib.request.urlopen(f'https://opendart.fss.or.kr/api/document.xml?crtfc_key={key}&rcept_no={r["rcept_no"]}', timeout=40).read()))
        t = re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', ''.join(z.read(f).decode('utf-8', 'replace') for f in z.namelist()))))
        open(f'src/dart_sub_{r["rcept_no"]}.txt', 'w', encoding='utf-8').write(t)
        print(n, r['rcept_dt'], sorted(set(re.findall(r'[가-힣A-Z]{1,6}은행', t)))[:6])
