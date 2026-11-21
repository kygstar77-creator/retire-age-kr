import sys
from pypdf import PdfReader
sys.stdout.reconfigure(encoding='utf-8')
for p in sys.argv[1:]:
    r = PdfReader(p); t = '\n'.join(pg.extract_text() or '' for pg in r.pages)
    open(p[:-4] + '.txt', 'w', encoding='utf-8').write(t)
    print('=====', p, len(r.pages)); 
    import re
    if 'DIVO' in t or 'Dividend Income' in t:
        for m in re.finditer(r'DIVO|CWP|Enhanced Dividend', t):
            print(t[max(0,m.start()-300):m.start()+700].replace('\n',' | ')); print('--'); break
    print(t[:1500])
