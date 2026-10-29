# W-3: 2026 기업가치제고계획 공시 본문 전부에서 '고배당기업 여부 해당/미해당'과 배당성향·증가율 뽑기 (2026-10-19 youtube-loop)
import io, json, re, sys, time, zipfile, urllib.request
sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work'); sys.stdout.reconfigure(encoding='utf-8')
import apis
K = apis.key('DART')
L = json.load(open('raw/dart_hidiv.json', encoding='utf-8'))
out = []
for i, x in enumerate(L):
    try:
        z = zipfile.ZipFile(io.BytesIO(urllib.request.urlopen(f'https://opendart.fss.or.kr/api/document.xml?crtfc_key={K}&rcept_no={x["rcept_no"]}', timeout=60).read()))
        t = ''.join(z.read(n).decode('utf-8', 'replace') for n in z.namelist())
    except Exception as e:
        out.append({**x, 'err': str(e)[:80]}); continue
    t = re.sub(r'<[^>]+>', ' ', t); t = re.sub(r'\s+', ' ', t)
    m = re.search(r'고배당기업 여부\s*(미해당|해당)', t)
    r = {**x, 'status': m.group(1) if m else None}
    for k, pat in (('payout', r'직전 사업연도 \(\d{4}\) 배당성향\(%\)\s*([\d.\-]+)'), ('growth', r'이익배당금액 증가율\(%\)\s*([\d.\-]+)'),
                   ('div_prev', r'직전 사업연도 \(\d{4}\) 이익배당금액\(원\)\s*([\d,\-]+)')):
        mm = re.search(pat, t); r[k] = mm.group(1) if mm else None
    out.append(r)
    if i % 50 == 0: print(i, len(L), flush=True)
    time.sleep(0.12)
json.dump(out, open('raw/dart_hidiv_body.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
from collections import Counter
print(Counter(r.get('status') for r in out))
