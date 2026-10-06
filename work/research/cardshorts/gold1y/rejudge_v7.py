# gold1y v7(틀 교체: 반전 두 칸) 채점 — firemap-shorts 10/6 11:1x, rejudge_1006.py 복사(질문 틀·모델·보정칸 그대로, 제목·내용 줄만 spec에 맞춤)
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
    '영상 제목: "금 1천만원 1년, KRX·ETF·골드뱅킹 어디서 샀으면 얼마? #shorts"\n영상 내용: 2025-10-02→2026-10-02 국제 금값을 원화 1g으로 바꾸면 +3.38%인데 KRX 금시장은 -2.42%(1천만원→9,758,142원). 1년 전 KRX 금이 국제값보다 7.4% 비쌌고 지금은 1.4%. 사는 길(KRX·금 ETF·골드뱅킹)별 결과 순위.\n제약: 숫자는 본문에 있는 것만, 과장·낚시 금지, 인물 사진 없음.\n'+TAIL)
PC=('네이버 카페 글 대표사진(목록·검색 썸네일) 심사. 이미지는 휴대폰 목록 크기(정사각형 110px) 비교판이다. 맨 왼쪽 "우리 새 표지"가 발행 전 시안, "경쟁"은 같은 검색어 네이버 카페 탭 상위 글의 실제 썸네일.\n'
    '글 제목: "공공재개발 이주비 이자 지원"\n제약: 숫자는 본문에 있는 것만, 과장·낚시 금지, 인물 사진 없음.\n답 형식: 첫 줄 "점수: N"(1~10, 이 목록에서 경쟁 썸네일 옆에 있을 때 먼저 누르고 싶은가 + 110px에서 글자가 읽히는가. 6=경쟁 평균, 7=통과, 8=목표) · 110px에서 읽히는 글자 · 1초 주제 한 문장 · 약점 · 8점이 되려면 고칠 것 2가지.')
jobs=[('v7',PS,os.path.join(H,'onesec','v7_board168.png')),('gongjae1002(보정)',PC,os.path.join(V,'cafe-covers-1002','board_gongjae1002.png'))]
res={};raw=[]
for n,P,p in jobs:
    v=[]
    for r in range(2):
        t=ask(P,p); v.append(sc(t)); raw.append(f'### {n} 회{r+1} 점수 {v[-1]}\n{t}\n')
    if None not in v and abs(v[0]-v[1])>2:
        t=ask(P,p); v.append(sc(t)); raw.append(f'### {n} 회3 점수 {v[-1]}\n{t}\n')
    res[n]=v; print(n,v,flush=True)
json.dump({'model':M,'scores':res},open(os.path.join(H,'rejudge_v7.json'),'w'),ensure_ascii=False)
open(os.path.join(H,'rejudge_v7_raw.md'),'w',encoding='utf-8').write('\n'.join(raw))
