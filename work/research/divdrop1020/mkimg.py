import sys, os, json; sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
from blogimg import F, INK, SUB, LINE, BG, ACC, WARN
GRAY=(178,186,200)
R=json.load(open('results.json',encoding='utf-8'))
def bars(path, title, sub, rows, unit, note, maxv, color_first=WARN):
    W,H=900,140+len(rows)*104+70; im=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(im)
    d.text((40,32),title,font=F(38,True),fill=INK); d.text((40,86),sub,font=F(21),fill=SUB)
    y=140; L=40; maxw=W-80-170
    for i,(n,v,lab) in enumerate(rows):
        d.text((L,y),n,font=F(27,True),fill=INK)
        w=max(4,int(abs(v)/maxv*maxw)); c=color_first if i==0 else ACC
        d.rectangle((L,y+44,L+w,y+86),fill=c)
        d.text((L+w+14,y+48),lab,font=F(28,True),fill=c)
        y+=104
    d.text((40,H-46),note,font=F(18),fill=SUB)
    im.save(path)
rows=[('KODEX 200',R['drop']['069500'],None),('PLUS 고배당주',R['drop']['161510'],None),('KODEX 고배당주',R['drop']['279530'],None)]
rows=[(n,v,f'{v*100:.1f}%'.replace('-','−')) for n,v,_ in rows]
bars('pkg/img/01.png','코스피 급락한 날, 하루 평균 얼마나 빠졌나',
     f"코스피가 하루 3% 이상 빠진 {R['ndrop']}일 평균 · 2024년 4월~2026년 10월",rows,'%',
     '한국거래소 정규장 종가(네이버 증권 일별 시세)로 직접 계산',0.065)
rows2=[('KODEX 200',R['tot']['069500'],None),('PLUS 고배당주',R['tot']['161510'],None),('KODEX 고배당주',R['tot']['279530'],None)]
rows2=[(n,v,f'약 {round(v/1e4):,}만원') for n,v,_ in rows2]
bars('pkg/img/02.png','1천만원씩 넣었다면 지금',
     '2024년 4월 29일 종가에 사서 2026년 10월 20일까지 · 분배금 포함 · 세전',rows2,'',
     '분배금은 재투자 없이 받은 그대로 더함 · 한국거래소 종가·분배금 배당락일 기준',2.7e7,color_first=INK)
json.dump({'01.png':{'rows':[[n,l] for n,v,l in rows]},'02.png':{'rows':[[n,l] for n,v,l in rows2]}},open('pkg/tables.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
print('ok')
