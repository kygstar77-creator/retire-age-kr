import sys,xml.etree.ElementTree as ET
sys.stdout.reconfigure(encoding='utf-8')
f=sys.argv[1]; want=sys.argv[2:]
t=ET.parse(f).getroot()
for u in t.iter('조문단위'):
    n=u.findtext('조문번호'); b=u.findtext('조문가지번호') or ''
    key=n+('의'+b if b else '')
    if key in want and u.findtext('조문여부')=='조문':
        print('=====',key,u.findtext('조문제목'))
        print(''.join(x.text or '' for x in u.iter() if x.tag in('조문내용','항내용','호내용','목내용'))[:int(9000)])
