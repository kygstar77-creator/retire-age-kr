import sys,re,xml.etree.ElementTree as ET
sys.stdout.reconfigure(encoding='utf-8')
def dump(f, nums, show_info=True):
    t=ET.parse(f).getroot()
    bi=t.find('기본정보')
    print('==',f, bi.findtext('법령명_한글'), '시행', bi.findtext('시행일자'), '공포', bi.findtext('공포일자'), bi.findtext('공포번호'))
    for j in t.iter('조문단위'):
        n=j.findtext('조문번호'); g=j.findtext('조문가지번호') or ''
        if j.findtext('조문여부')!='조문': continue
        key=n+('의'+g if g else '')
        if key in nums:
            print('---', key, (j.findtext('조문제목') or ''), j.findtext('조문시행일자'))
            txt=ET.tostring(j,encoding='unicode')
            for el in j.iter():
                if el.tag in ('조문내용','항내용','호내용','목내용') and el.text and el.text.strip():
                    print(el.text.strip())
dump('law.xml', sys.argv[1].split(','))
dump('sihaeng.xml', sys.argv[2].split(','))
