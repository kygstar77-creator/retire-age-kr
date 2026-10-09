import json,base64,urllib.request,sys,re
sys.stdout.reconfigure(encoding='utf-8')
KEY=[l.split('=',1)[-1].strip() for l in open(r'C:\Users\강영준\Documents\gemini_key.txt',encoding='utf-8-sig') if l.strip()][0]
ms=json.load(urllib.request.urlopen(f'https://generativelanguage.googleapis.com/v1beta/models?key={KEY}&pageSize=200'))['models']
print([m['name'] for m in ms if 'image' in m['name'] or 'imagen' in m['name']])
