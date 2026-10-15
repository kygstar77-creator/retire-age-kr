# 2026 1·2분기 배당결정 본문에서 1주당 배당금·기준일·지급일 뽑기 (DART document.xml)
import json, sys, urllib.request, re, io, zipfile, html
sys.path.insert(0, '../../')
import apis
key = apis.key('DART')
L = json.load(open('src/dart_div2026_list.json', encoding='utf-8'))
res = {}
for n, rows in L.items():
    for r in rows:
        nm = r['report_nm']
        if not nm.startswith('현금ㆍ현물배당결정') and not nm.startswith('[기재정정]현금ㆍ현물배당결정'): continue
        if '자회사' in nm: continue
        b = urllib.request.urlopen(f'https://opendart.fss.or.kr/api/document.xml?crtfc_key={key}&rcept_no={r["rcept_no"]}', timeout=40).read()
        z = zipfile.ZipFile(io.BytesIO(b))
        t = ''.join(z.read(f).decode('utf-8', 'replace') for f in z.namelist())
        t = html.unescape(re.sub(r'<[^>]+>', ' ', t)); t = re.sub(r'\s+', ' ', t)
        open(f'src/dart_{r["rcept_no"]}.txt', 'w', encoding='utf-8').write(t)
        m = re.search(r'1주당 배당금\(원\)\s*보통주식\s*([\d,]+)', t)
        k = re.search(r'배당기준일\s*([\d\-]+)', t); p = re.search(r'배당금지급 예정일자\s*([\d\-]+)', t)
        q = re.search(r'배당구분\s*(\S+)', t)
        print(n, r['rcept_dt'], q and q.group(1), m and m.group(1), k and k.group(1), p and p.group(1))
        res.setdefault(n, []).append([r['rcept_dt'], q and q.group(1), m and m.group(1), k and k.group(1), p and p.group(1), r['rcept_no']])
json.dump(res, open('src/dart_div2026.json', 'w', encoding='utf-8'), ensure_ascii=False)
