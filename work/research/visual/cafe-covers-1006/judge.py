import sys, os, json, base64, urllib.request, re, time
sys.stdout.reconfigure(encoding='utf-8')
H=os.path.dirname(os.path.abspath(__file__)); R=os.path.join(H,'..','..'); V=os.path.join(H,'..')
KEY=[l.split('=',1)[-1].strip() for l in open(r'C:\Users\강영준\Documents\gemini_key.txt',encoding='utf-8-sig') if l.strip()][0]
M='gemini-3.1-flash-lite'
def ask(text,p):
    parts=[{'text':text},{'inline_data':{'mime_type':'image/png','data':base64.b64encode(open(p,'rb').read()).decode()}}]
    for t in range(4):
        try:
            r=json.load(urllib.request.urlopen(urllib.request.Request(f'https://generativelanguage.googleapis.com/v1beta/models/{M}:generateContent?key={KEY}',
                data=json.dumps({'contents':[{'parts':parts}]}).encode(),headers={'Content-Type':'application/json'}),timeout=240))
            return r['candidates'][0]['content']['parts'][0]['text']
        except Exception as e: err=str(e); time.sleep(5)
    return f'(실패 {err})'
def prompt(pkgdir):
    title=open(os.path.join(pkgdir,'title.txt'),encoding='utf-8').read().strip()
    lead=open(os.path.join(pkgdir,'c00.txt'),encoding='utf-8').read().strip()[:300]
    return ('네이버 카페 글 대표사진(목록·검색 썸네일) 심사. 이미지는 휴대폰 목록 크기(정사각형 110px) 비교판이다. 맨 왼쪽 "우리 새 표지"가 발행 전 시안, "경쟁"은 같은 검색어 네이버 카페 탭 상위 글의 실제 썸네일.\n'
     f'글 제목: "{title}"\n글 첫머리: {lead}\n'
     '제약: 숫자는 본문에 있는 것만, 과장·낚시 금지, 인물 사진 없음.\n'
     '답 형식: 첫 줄 "점수: N"(1~10, 이 목록에서 경쟁 썸네일 옆에 있을 때 먼저 누르고 싶은가 + 110px에서 글자가 읽히는가. 6=경쟁 평균, 7=통과, 8=목표) · 110px에서 읽히는 글자 · 1초 주제 한 문장 · 약점 · 8점이 되려면 고칠 것 2가지.')
def score(t):
    m=re.search(r'점수[^0-9]{0,20}(\d+(?:\.\d+)?)',t); return float(m.group(1)) if m else None
jobs={'hfguar1006_B5':(os.path.join(H,'board_hfguar1006_B5.png'),os.path.join(R,'..','hfguar1006'+'')),}
pk={'hfguar1006_B5':'hfguar1006','retmid1005_v4':'retmid1005','retmid1005_v5':'retmid1005','gongjae1002':'gongjae1002'}
bd={k:os.path.join(H,f'board_{k}.png') for k in pk}; bd['gongjae1002']=os.path.join(V,'cafe-covers-1002','board_gongjae1002.png')
res={}; raw=[]
for k in pk:
    pkgdir=os.path.join(R,'..',pk[k],'pkg') if k=='gongjae1002' else os.path.join(R,pk[k],'pkg')
    if k=='gongjae1002': pkgdir=os.path.join(R,'..','research',pk[k],'pkg') if not os.path.exists(os.path.join(R,pk[k],'pkg')) else os.path.join(R,pk[k],'pkg')
    P=prompt(pkgdir); sc=[]
    for rep in range(1,4):
        if rep==3 and (len(sc)<2 or sc[0] is None or sc[1] is None or abs(sc[0]-sc[1])<=2): break
        t=ask(P,bd[k]); s=score(t); sc.append(s); raw.append(f'### {k} | {M} | 회{rep} | 점수 {s}\n{t}\n'); print(k,rep,s,flush=True)
    res[k]=sc
open(os.path.join(H,'judge_raw.md'),'w',encoding='utf-8').write('\n'.join(raw))
json.dump({'model':M,'scores':res},open(os.path.join(H,'judge.json'),'w',encoding='utf-8'),ensure_ascii=False,indent=1)
