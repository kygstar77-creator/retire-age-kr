import sys, os, json, base64, urllib.request, re, time
sys.stdout.reconfigure(encoding='utf-8')
HH=os.path.dirname(os.path.abspath(__file__))
KEY=[l.split('=',1)[-1].strip() for l in open(r'C:\Users\강영준\Documents\gemini_key.txt',encoding='utf-8-sig') if l.strip()][0]
M='gemini-3.1-flash-lite'
def ask(text,p):
    parts=[{'text':text},{'inline_data':{'mime_type':'image/png','data':base64.b64encode(open(p,'rb').read()).decode()}}]
    err=''
    for t in range(4):
        try:
            r=json.load(urllib.request.urlopen(urllib.request.Request(f'https://generativelanguage.googleapis.com/v1beta/models/{M}:generateContent?key={KEY}',data=json.dumps({'contents':[{'parts':parts}]}).encode(),headers={'Content-Type':'application/json'}),timeout=240))
            return r['candidates'][0]['content']['parts'][0]['text']
        except Exception as e: err=str(e); time.sleep(5)
    return f'(실패 {err})'
def prompt(pk):
    title=open(os.path.join(pk,'title.txt'),encoding='utf-8').read().strip()
    lead=open(os.path.join(pk,'c00.txt'),encoding='utf-8').read().strip()[:300]
    return ('네이버 카페 글 대표사진(목록·검색 썸네일) 심사. 이미지는 휴대폰 목록 크기(정사각형 110px) 비교판이다. 맨 왼쪽 "우리 새 표지"가 발행 전 시안, "경쟁"은 같은 검색어 네이버 카페 탭 상위 글의 실제 썸네일.\n'
     f'글 제목: "{title}"\n글 첫머리: {lead}\n'
     '제약: 숫자는 본문에 있는 것만, 과장·낚시 금지, 인물 사진 없음.\n'
     '답 형식: 첫 줄 "점수: N"(1~10, 이 목록에서 경쟁 썸네일 옆에 있을 때 먼저 누르고 싶은가 + 110px에서 글자가 읽히는가. 6=경쟁 평균, 7=통과, 8=목표) · 110px에서 읽히는 글자 · 1초 주제 한 문장 · 약점 · 8점이 되려면 고칠 것 2가지.')
def score(t):
    m=re.search(r'점수[^0-9]{0,20}(\d+(?:\.\d+)?)',t); return float(m.group(1)) if m else None
V=os.path.join(HH,'..','visual','cafe-covers-1002','board_gongjae1002.png')
jobs=[(k,os.path.join(HH,'covers_try',f'board_{k}.png'),os.path.join(HH,'pkg')) for k in 'H']+[('gongjae1002',V,os.path.join(HH,'..','gongjae1002','pkg'))]
res={};raw=[]
for k,b,pk in jobs:
    sc=[]
    for rep in (1,2):
        t=ask(prompt(pk),b); s=score(t); sc.append(s); raw.append(f'### {k} 회{rep} 점수 {s}\n{t}\n'); print(k,rep,s,flush=True)
    res[k]=sc
open(os.path.join(HH,'covers_try','judge_raw_H.md'),'w',encoding='utf-8').write('\n'.join(raw))
json.dump({'model':M,'scores':res},open(os.path.join(HH,'covers_try','judge_H.json'),'w',encoding='utf-8'),ensure_ascii=False)
