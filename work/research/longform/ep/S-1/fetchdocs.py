# -*- coding: utf-8 -*-
"""S-1 잠정실적 공시 원문(document.xml) 받기 — 분기 첫 공시만. 이미 받은 건 건너뜀."""
import json, sys, os, io, zipfile, urllib.request, time
sys.stdout.reconfigure(encoding='utf-8')
K = open(r'C:/Users/강영준/Documents/dart_key.txt', encoding='utf-8-sig').read().strip().split('=')[-1].strip()
D = os.path.dirname(os.path.abspath(__file__))
def prelims():
    d = json.load(open(os.path.join(D, 'raw/dart_samsung_prelim.json'), encoding='utf-8'))
    first = {}
    for x in d:
        if x['report_nm'].strip().startswith('['): continue
        dt = x['rcept_dt']; m = int(dt[4:6]); day = int(dt[6:])
        if m not in (1, 4, 7, 10) or day > 20: continue
        k = dt[:6]
        if k not in first or dt < first[k]['rcept_dt']: first[k] = x
    return sorted(first.values(), key=lambda x: x['rcept_dt'])
if __name__ == '__main__':
    ps = prelims(); print(len(ps), ps[0]['rcept_dt'], ps[-1]['rcept_dt'])
    for x in ps:
        out = os.path.join(D, 'raw/docs', x['rcept_no'] + '.xml')
        if os.path.exists(out): continue
        z = urllib.request.urlopen(f"https://opendart.fss.or.kr/api/document.xml?crtfc_key={K}&rcept_no={x['rcept_no']}", timeout=60).read()
        try:
            zf = zipfile.ZipFile(io.BytesIO(z)); open(out, 'wb').write(zf.read(zf.namelist()[0]))
        except zipfile.BadZipFile:
            print('fail', x['rcept_no'], z[:120])
        time.sleep(0.4)
