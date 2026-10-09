import json,base64,urllib.request,sys
sys.stdout.reconfigure(encoding='utf-8')
KEY=[l.split('=',1)[-1].strip() for l in open(r'C:\Users\강영준\Documents\gemini_key.txt',encoding='utf-8-sig') if l.strip()][0]
P=("Photorealistic studio photo, vertical 9:16. A stack of shiny gold bars on a dark reflective surface, dramatic warm lighting, deep black background, top half of the frame left dark and empty for text overlay. No text, no letters, no numbers, no people, no logos.")
r=json.load(urllib.request.urlopen(urllib.request.Request(f'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent?key={KEY}',data=json.dumps({'contents':[{'parts':[{'text':P}]}],'generationConfig':{'responseModalities':['IMAGE']}}).encode(),headers={'Content-Type':'application/json'}),timeout=240))
for p in r['candidates'][0]['content']['parts']:
    d=p.get('inlineData') or p.get('inline_data')
    if d: open('gold_photo.png','wb').write(base64.b64decode(d['data']));print('ok')
