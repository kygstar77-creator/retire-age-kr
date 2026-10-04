# 표지 1초 시험 — 제미나이 비전(무료 한도). py -3.12 work/onesec.py <표지.png>  (firemap-write 2026-10-05, 이미지를 직접 보여 주고 점수를 받는다)
import sys, json, base64, urllib.request, urllib.error
sys.stdout.reconfigure(encoding='utf-8')
KEY=[l.split('=',1)[-1].strip() for l in open(r'C:\Users\강영준\Documents\gemini_key.txt',encoding='utf-8-sig') if l.strip()][0]
img=base64.b64encode(open(sys.argv[1],'rb').read()).decode()
Q=('이 이미지는 네이버 카페 글 목록에 168px 썸네일로 보이는 표지다. 1초만 봤다고 치고 답하라. 한국어로.\n'
   '1) 무엇에 대한 글로 보이나(한 줄) 2) 오해할 만한 점 3) 10점 만점 점수(1초에 주제 전달·숫자 가독·오해 없음) 4) 고칠 점 2개. 칭찬 말고 감점부터.')
for m in ['gemini-3-flash-preview','gemini-3.8-flash','gemini-3.7-flash','gemini-3.5-flash-lite','gemini-3.1-flash-lite']:
    body={'contents':[{'parts':[{'text':Q},{'inline_data':{'mime_type':'image/png','data':img}}]}]}
    rq=urllib.request.Request(f'https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={KEY}',json.dumps(body).encode(),{'Content-Type':'application/json'})
    try:
        r=json.load(urllib.request.urlopen(rq,timeout=90)); print(f'[{m}]'); print(r['candidates'][0]['content']['parts'][0]['text']); break
    except urllib.error.HTTPError as e: print(m,e.code)
