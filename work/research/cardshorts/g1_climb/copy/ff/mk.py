# copywriter 10/10: 그림은 v9 hero 그대로, 문구만 바꿔 1초 시험(문구 몫 분리)
import sys,os,json,subprocess
sys.path.insert(0,r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
sys.stdout.reconfigure(encoding='utf-8')
import cardshort as cs
from PIL import Image,ImageDraw
H=os.path.dirname(os.path.abspath(__file__)); G=os.path.join(H,'..','..')
spec=json.load(open(os.path.join(G,'g1_climb_v9.json'),encoding='utf-8'))
V={
 'n1':{"kind":"hero","sec":6,"head":["고점에 산 금 1천만원"],"label":"지금은","big":"663만원","head_size":104,"note":"되찾으려면 +50.7% · KRX 금 1/29→10/6"},
 'n3':{"kind":"hero","sec":6,"head":["고점에 산 금 1천만원,"],"label":"산 값 되찾으려면","big":"+51%","head_size":104,"note":"지금 663만원 · KRX 금 1/29→10/6"},
 'n2':{"kind":"hero","sec":6,"head":["금 34% 빠지면"],"label":"산 값까지","big":"+51%","head_size":150,"note":"고점에 산 금 1g 기준 · KRX 1/29→10/6"},
}
for k,c in V.items():
    probe=Image.new('RGB',(cs.W,cs.H)); b=cs.draw_card(ImageDraw.Draw(probe),spec,c,99,cs.CARD_TOP)
    off=max(0,(cs.SAFE_B-b)//2); p=os.path.join(H,k+'.png'); cs.card_image(spec,c,0,off).save(p); print(k,b,off)
