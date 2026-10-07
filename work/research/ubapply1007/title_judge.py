# ubapply1007 제목 심사 (parking1007 틀) — bigwa1006 title_judge 틀, gemini-3.1-flash-lite 고정·2회. firemap-write 10/6
import sys, os, json, urllib.request, re, time
sys.stdout.reconfigure(encoding='utf-8')
H=os.path.dirname(os.path.abspath(__file__))
KEY=[l.split('=',1)[-1].strip() for l in open(r'C:\Users\강영준\Documents\gemini_key.txt',encoding='utf-8-sig') if l.strip()][0]
M='gemini-3.1-flash-lite'
C={'T1':'실업급여 270일 받는 분이 신청을 4개월 미루면 얼마를 못 받을까',
   'T2':'실업급여 신청을 4개월 미루면 못 받게 되는 돈은 얼마일까',
   'T3':'실업급여 신청 시기, 퇴사 뒤 몇 개월부터 날수가 줄어들까',
   'T4':'실업급여 신청방법보다 먼저, 미루면 며칠이 사라지는지 계산해 봤어요'}
lead=open(os.path.join(H,'pkg','c00.txt'),encoding='utf-8').read().strip()
COMP=' / '.join(["실업급여 조건과 신청방법, 금액 총정리, 나는 얼마나 받을까?","고용24 실업급여 신청방법 이직확인서, 온라인 교육 등 준비물, 인터넷 제출 전 절차 총정리","실업급여 신청방법 2026, 고용24부터 실업인정까지 순서대로 정리","정년퇴직 실업급여 신청방법 어떻게 하면 될까","실업급여 신청방법 서류 준비물 조건 순서대로 총정리!"])
NUM=('이직 다음 날부터 12개월 안에서만 지급(고용보험법 48조) · 270일 수급자(50세 이상·10년 이상) 6/30 퇴사: 신청 2개월 뒤까지 270일 전부, 3개월 뒤 4일, 4개월 뒤 35일(약 238만원), 6개월 뒤 96일, 8개월 뒤 155일 못 받음 · 신청 순서와 이직확인서 10일 규정')
P=('네이버 카페 글 제목 심사. 독자: 퇴직 뒤 실업급여를 받으며 재취업을 알아보는 퇴직 뒤 실업급여를 앞둔 중장년. 검색어 실업급여신청방법 월 39,700.\n'
   f'[경쟁 상위 제목] {COMP}\n[본문 첫머리] {lead}\n[본문 핵심 숫자] {NUM}\n[후보]\n'
   +'\n'.join(f'{k}. {v}' for k,v in C.items())+
   '\n기준: ①1초에 주제 ②궁금증 장치 하나 ③낚시·과장 아님(예시 조건을 제목에 안 밝히면 일반화로 감점) ④경쟁 틀 반복 아님 ⑤검색어가 앞. 6=경쟁 평균, 7=통과, 8=목표.\n답 형식: 후보마다 한 줄 "T1: 점수 N — 이유". 마지막 줄 "1위: 기호".')
def ask():
    err=''
    for t in range(4):
        try:
            r=json.load(urllib.request.urlopen(urllib.request.Request(f'https://generativelanguage.googleapis.com/v1beta/models/{M}:generateContent?key={KEY}',
              data=json.dumps({'contents':[{'parts':[{'text':P}]}]}).encode(),headers={'Content-Type':'application/json'}),timeout=240))
            return r['candidates'][0]['content']['parts'][0]['text']
        except Exception as e: err=str(e); time.sleep(5)
    return f'(실패 {err})'
raw=[];sc={k:[] for k in C}
for rep in (1,2):
    t=ask(); raw.append(f'### 회{rep} {M}\n{t}\n')
    for k in C:
        m=re.search(k+r'\W{0,6}(?:점수)?\s*:?\s*(\d+(?:\.\d+)?)',t); sc[k].append(float(m.group(1)) if m else None)
    print(rep,{k:v[-1] for k,v in sc.items()},flush=True)
open(os.path.join(H,'title_judge_raw.md'),'w',encoding='utf-8').write('\n'.join(raw))
json.dump({'model':M,'scores':sc},open(os.path.join(H,'title_judge.json'),'w',encoding='utf-8'),ensure_ascii=False,indent=1)
