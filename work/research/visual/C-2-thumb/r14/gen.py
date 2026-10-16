# C-2 14차 바탕 그림(글자 없음) — R-1 r29/gen.py 복사, 프롬프트만 통장 두 권. py -3.12 gen.py <이름> <키>
import json,base64,urllib.request,sys,os
sys.stdout.reconfigure(encoding='utf-8')
KEY=[l.split('=',1)[-1].strip() for l in open(r'C:\Users\강영준\Documents\gemini_key.txt',encoding='utf-8-sig') if l.strip()][0]
NO=" Absolutely no text, no letters, no numbers, no symbols printed anywhere, no faces, no portraits, no people, no logos. Banknotes seen only from the side edge so no printed design or portrait is visible."
P={
 'books':"Photorealistic top-down product photo, wide 16:9. Two open blank bank passbooks (small booklets with plain ruled pages) lying side by side on a warm medium-brown wooden desk, occupying only the lower 55% of the frame, upper 45% is plain empty wooden desk surface for text. LEFT booklet: thin, old, worn and creased, slightly faded grey-blue cover edge, pages mostly empty. RIGHT booklet: thick, fresh, crisp navy-blue cover edge, many pages. Soft daylight from top-left, medium brightness, rich contrast, slight shadow under booklets. Bottom-right corner area plain wood." + NO,
 'books2':"Photorealistic photo, wide 16:9, slight 30 degree angle. Warm wooden kitchen table. Lower half of frame: two closed bank passbook booklets side by side with a gap between them; left one thin, worn, bent corner, faded grey cover; right one thick, swollen with many pages, deep blue cover, a fountain pen beside it. Upper half: soft out-of-focus warm beige wall, empty for text. Medium brightness, warm light, strong contrast." + NO,
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
