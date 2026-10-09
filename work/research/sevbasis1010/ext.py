# 법령 XML에서 조문 원문 뽑기. firemap-write 2026-10-06
import sys, re, xml.etree.ElementTree as ET
sys.stdout.reconfigure(encoding='utf-8')
f, *nums = sys.argv[1:]
t = ET.parse(f).getroot()
b = t.find('기본정보')
print('##', b.findtext('법령명_한글'), '시행', b.findtext('시행일자'), '공포', b.findtext('공포일자'), b.findtext('공포번호'))
for j in t.iter('조문단위'):
    if j.findtext('조문여부') != '조문': continue
    n = j.findtext('조문번호'); g = j.findtext('조문가지번호') or ''
    key = n + (('의'+g) if g else '')
    if key in nums:
        txt = ''.join(j.itertext())
        print(re.sub(r'\n\s*\n+', '\n', txt).strip()); print('----')
