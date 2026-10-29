# W-3: DART 공시 본문에서 '고배당' 문장 찾기 (2026-10-19 youtube-loop)
import io, re, sys, zipfile, urllib.request
sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work'); sys.stdout.reconfigure(encoding='utf-8')
import apis
K = apis.key('DART')
for rno in sys.argv[1:]:
    z = zipfile.ZipFile(io.BytesIO(urllib.request.urlopen(f'https://opendart.fss.or.kr/api/document.xml?crtfc_key={K}&rcept_no={rno}', timeout=60).read()))
    t = ''.join(z.read(n).decode('utf-8', 'replace') for n in z.namelist())
    t = re.sub(r'<[^>]+>', ' ', t); t = re.sub(r'\s+', ' ', t)
    hits = [m.group(0) for m in re.finditer(r'.{0,140}고배당.{0,160}', t)]
    print(rno, 'len', len(t), 'hits', len(hits))
    for h in hits[:4]: print('   ', h)
