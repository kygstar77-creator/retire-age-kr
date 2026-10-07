# nhis_prop_b v4(hero 전면판) 첫 프레임 채점 — firemap-shorts 10/7 11:2x, rejudge_v3.py 그대로, gold1y/rejudge_v8.py 복사(질문 틀·모델·보정칸 그대로, 제목·내용 줄만 nhis_prop_b에 맞춤)
# gold1y v5·v6 재채점 (judge-drift-1006.md 고정 조건): 경쟁5 비교판 + judge_cafe.py와 같은 질문(쇼츠 문구만) + gemini-3.1-flash-lite, 2회(벌어지면 3회), 보정칸 gongjae1002
import sys, os, json, base64, urllib.request, re, time
sys.stdout.reconfigure(encoding='utf-8')
H=os.path.dirname(os.path.abspath(__file__)); V=os.path.join(H,'..','..','visual')
KEY=[l.split('=',1)[-1].strip() for l in open(r'C:\Users\강영준\Documents\gemini_key.txt',encoding='utf-8-sig') if l.strip()][0]
M='gemini-3.1-flash-lite'
def ask(t,p):
    parts=[{'text':t},{'inline_data':{'mime_type':'image/png','data':base64.b64encode(open(p,'rb').read()).decode()}}]
    for k in range(3):
        try:
            r=json.load(urllib.request.urlopen(urllib.request.Request(f'https://generativelanguage.googleapis.com/v1beta/models/{M}:generateContent?key={KEY}',data=json.dumps({'contents':[{'parts':parts}]}).encode(),headers={'Content-Type':'application/json'}),timeout=240))
            return r['candidates'][0]['content']['parts'][0]['text']
        except Exception as e: err=str(e); time.sleep(5)
    return '(실패 '+err+')'
def sc(t):
    m=re.search(r'점수[^0-9]{0,20}(\d+(?:\.\d+)?)',t); return float(m.group(1)) if m else None
TAIL='답 형식: 첫 줄 "점수: N"(1~10, 이 목록에서 경쟁 썸네일 옆에 있을 때 먼저 누르고 싶은가 + 168px에서 글자가 읽히는가. 6=경쟁 평균, 7=통과, 8=목표) · 읽히는 글자 · 1초 주제 한 문장 · 약점 · 8점이 되려면 고칠 것 2가지.'
PS=('유튜브 쇼츠 표지(휴대폰 목록 크기, 세로형 가로 168px) 심사. 이미지는 비교판이다. 맨 왼쪽 "우리"가 발행 전 시안, "경쟁1~5"는 같은 주제 최근 30일 쇼츠 상위 영상의 실제 표지.\n'
    '영상 제목: "건보료 집 한 채 공시가 3억→9억이면, 재산분은 월 40,910원→162,950원 약 4배 #shorts" (표지 없이 영상 첫 프레임이 곧 목록 그림)\n영상 내용: 29초 카드 4장. ①한 숫자 전면판(공시가는 3배인데 건보료 재산분은 약 4배, 첫 프레임엔 공시가 3배·건보료 재산분은 약 4배만) ②계기판(월 재산분 칸 하나에서 공시가 3억→5억→6억→9억, 40,910원→162,950원) ③이유(1주택 과세표준 공시가의 43~45%, 1억원 빼고 점수) ④빠진 것(소득·자동차·대출 공제). 국민건강보험법 시행령 별표 4 원문 계산.\n제약: 숫자는 본문에 있는 것만, 과장·낚시 금지, 인물 사진 없음.\n'+TAIL)
PC=('네이버 카페 글 대표사진(목록·검색 썸네일) 심사. 이미지는 휴대폰 목록 크기(정사각형 110px) 비교판이다. 맨 왼쪽 "우리 새 표지"가 발행 전 시안, "경쟁"은 같은 검색어 네이버 카페 탭 상위 글의 실제 썸네일.\n'
    '글 제목: "공공재개발 이주비 이자 지원"\n제약: 숫자는 본문에 있는 것만, 과장·낚시 금지, 인물 사진 없음.\n답 형식: 첫 줄 "점수: N"(1~10, 이 목록에서 경쟁 썸네일 옆에 있을 때 먼저 누르고 싶은가 + 110px에서 글자가 읽히는가. 6=경쟁 평균, 7=통과, 8=목표) · 110px에서 읽히는 글자 · 1초 주제 한 문장 · 약점 · 8점이 되려면 고칠 것 2가지.')
jobs=[('v4b',PS,os.path.join(H,'onesec','v4b_board168.png')),('gongjae1002(보정)',PC,os.path.join(V,'cafe-covers-1002','board_gongjae1002.png'))]
res={};raw=[]
for n,P,p in jobs:
    v=[]
    for r in range(2):
        t=ask(P,p); v.append(sc(t)); raw.append(f'### {n} 회{r+1} 점수 {v[-1]}\n{t}\n')
    if None not in v and abs(v[0]-v[1])>2:
        t=ask(P,p); v.append(sc(t)); raw.append(f'### {n} 회3 점수 {v[-1]}\n{t}\n')
    res[n]=v; print(n,v,flush=True)
json.dump({'model':M,'scores':res},open(os.path.join(H,'rejudge_v4b.json'),'w'),ensure_ascii=False)
open(os.path.join(H,'rejudge_v4b_raw.md'),'w',encoding='utf-8').write('\n'.join(raw))
