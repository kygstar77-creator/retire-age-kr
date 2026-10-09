import sys,os,json
sys.path.insert(0,r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
sys.stdout.reconfigure(encoding='utf-8')
import cardshort as cs
spec=json.load(open('g1_climb.v4.json',encoding='utf-8'))
spec['cards']=[{"kind":"hero","sec":6,"head":["금 -34%,"],"label":"왜","big":"+51%?","head_size":180,"note":"고점에 산 금 1g 기준"}]
spec['layout']='cards'; json.dump(spec,open('g1_climb_v9.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
c=spec['cards'][0]
from PIL import Image,ImageDraw
probe=Image.new('RGB',(cs.W,cs.H)); b=cs.draw_card(ImageDraw.Draw(probe),spec,c,99,cs.CARD_TOP)
off=max(0,(cs.SAFE_B-b)//2)
cs.card_image(spec,c,0,off).save('onesec/v9_first.png'); print(b,off)
