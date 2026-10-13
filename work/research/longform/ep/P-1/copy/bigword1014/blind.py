import sys, os, json, base64, urllib.request
sys.stdout.reconfigure(encoding='utf-8')
KEY=[l.split('=',1)[-1].strip() for l in open(r'C:\Users\강영준\Documents\gemini_key.txt',encoding='utf-8-sig') if l.strip()][0]
H=os.path.dirname(os.path.abspath(__file__))
T=('휴대폰 유튜브 목록에서 스친 썸네일 1장(가로 168px 실제 크기). 제목은 안 보입니다. 1초만 봤다고 치고 정확히 세 줄:\n'
   '주제: (무슨 영상인지 한 문장)\n큰 숫자 두 개의 뜻: (그 나이가 무엇의 나이인지 한 문장)\n누를까: 예/아니오 + 이유 한 마디')
import time
def ask(p):
  for t in range(6):
    try: return ask0(p)
    except Exception as e: print('retry',e,flush=True); time.sleep(20)
def ask0(p):
    parts=[{'text':T},{'inline_data':{'mime_type':'image/png','data':base64.b64encode(open(p,'rb').read()).decode()}}]
    r=json.load(urllib.request.urlopen(urllib.request.Request(f'https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-lite:generateContent?key={KEY}',data=json.dumps({'contents':[{'parts':parts}],'generationConfig':{'temperature':1.0}}).encode(),headers={'Content-Type':'application/json'}),timeout=120))
    return r['candidates'][0]['content']['parts'][0]['text'].strip()
out=[]
for k in sys.argv[1].split(','):
    for i in range(3):
        a=ask(os.path.join(H,k+'_168.png')); out.append(f'## {k} #{i+1}\n{a}\n'); print(f'## {k} #{i+1}\n{a}\n',flush=True)
open(os.path.join(H,'blind.md'),'a',encoding='utf-8').write('\n'.join(out))
