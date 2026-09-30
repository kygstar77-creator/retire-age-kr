import xml.etree.ElementTree as ET,sys,urllib.request,os
sys.stdout.reconfigure(encoding='utf-8')
D=os.path.dirname(os.path.abspath(__file__))
ef=sys.argv[1]
for m in sys.argv[2:]:
    raw=urllib.request.urlopen(f'http://www.law.go.kr/DRF/lawService.do?OC=test&target=eflaw&MST={m}&efYd={ef}&type=XML',timeout=30).read()
    open(f'{D}/l_{m}.xml','wb').write(raw)
    r=ET.fromstring(raw)
    print('===',m,r.findtext('.//법령명_한글'),r.findtext('.//공포일자'),r.findtext('.//공포번호'))
    for t in ['제개정이유내용','개정문내용']:
        for e in r.iter(t):
            print('['+t+']',(''.join(e.itertext())).strip()[:2500])
