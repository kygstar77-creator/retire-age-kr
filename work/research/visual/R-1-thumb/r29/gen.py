# R-1 29차 배경 그림(글자 없음) — gemini 이미지 모델, py -3.12 gen.py <이름> <프롬프트키>
import json,base64,urllib.request,sys,os
sys.stdout.reconfigure(encoding='utf-8')
KEY=[l.split('=',1)[-1].strip() for l in open(r'C:\Users\강영준\Documents\gemini_key.txt',encoding='utf-8-sig') if l.strip()][0]
NO=" Absolutely no text, no letters, no numbers, no symbols printed anywhere, no faces, no portraits, no people, no logos. Banknotes seen only from the side edge so no printed design or portrait is visible."
P={
 'stacks':"Photorealistic product photo, wide 16:9. On a dark charcoal desk, two stacks of banknotes seen from the side edge: on the right a tall stack of pale green bills about four times taller, on the left a short low stack of warm beige-yellow bills. Soft studio light, medium brightness, strong contrast, the left 55% of the frame mostly empty dark-grey wall for text, the stacks sit in the right 45%." + NO,
 'fx':"Photorealistic photo, wide 16:9. A tall stack of pale green banknotes seen from the side edge on a dark desk, the top quarter of the stack is being sliced away and slides off to the right, a few bills falling. Medium brightness, dramatic side light, the left 55% of the frame mostly empty dark-blue-grey wall for text, the stack sits in the right 40%." + NO,
}
MODELS=['gemini-3-pro-image-preview','gemini-3.1-flash-image-preview','gemini-2.5-flash-image']
name,k=sys.argv[1],sys.argv[2]
for m in MODELS:
    try:
        r=json.load(urllib.request.urlopen(urllib.request.Request(f'https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={KEY}',data=json.dumps({'contents':[{'parts':[{'text':P[k]}]}],'generationConfig':{'responseModalities':['IMAGE'],'imageConfig':{'aspectRatio':'16:9'}}}).encode(),headers={'Content-Type':'application/json'}),timeout=300))
        for p in r['candidates'][0]['content']['parts']:
            d=p.get('inlineData') or p.get('inline_data')
            if d: open(name+'.png','wb').write(base64.b64decode(d['data'])); print('ok',m,name); sys.exit()
        print('no image',m,str(r)[:300])
    except SystemExit: raise
    except Exception as e: print('fail',m,str(e)[:200])
