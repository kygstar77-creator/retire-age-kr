# earlyjob1007 제목 심사 (parking1007 틀) — bigwa1006 title_judge 틀, gemini-3.1-flash-lite 고정·2회. firemap-write 10/6
import sys, os, json, urllib.request, re, time
sys.stdout.reconfigure(encoding='utf-8')
H=os.path.dirname(os.path.abspath(__file__))
KEY=[l.split('=',1)[-1].strip() for l in open(r'C:\Users\강영준\Documents\gemini_key.txt',encoding='utf-8-sig') if l.strip()][0]
M='gemini-3.1-flash-lite'
C={'T16':'조기재취업수당 300만원 기준 예고, 10월 신청과 11월 신청은 얼마 차이일까',
   'T22':'조기재취업수당 300만원 기준 예고, 이번 달 신청하면 얼마 다를까',
   'T25':'조기재취업수당 300만원 기준 예고, 누구부터 못 받게 될까','T26':'조기재취업수당 300만원 기준 예고, 누구부터 적용될까'}
lead=open(os.path.join(H,'pkg','c00.txt'),encoding='utf-8').read().strip()
COMP=' / '.join(l for l in open(os.path.join(H,'comp_titles.txt'),encoding='utf-8').read().split('\n') if l.strip())
NUM=('고용노동부 9/29 행정예고: 지급 제외 새 직장 월급 574만원→300만원, 11월 1일 이후 수급자격 신청자부터(확정 아님, 의견 10/18까지) · '
     '수급자격 신청일 기준(10월 신청자는 574만원 그대로) · 50세 이상 10년 270일·하루 68,100원: 남은 240일 817만원, 135일 460만원, 134일 0원')
P=('네이버 카페 글 제목 심사. 독자: 퇴직 뒤 실업급여를 받으며 재취업을 알아보는 50대 전후. 검색어 조기재취업수당 월 8,160.\n'
   f'[경쟁 상위 제목] {COMP}\n[본문 첫머리] {lead}\n[본문 핵심 숫자] {NUM}\n[후보]\n'
   +'\n'.join(f'{k}. {v}' for k,v in C.items())+
   '\n기준: ①1초에 주제 ②궁금증 장치 하나 ③낚시·과장 아님(예고 단계인데 확정처럼 쓰면 감점) ④경쟁 틀 반복 아님 ⑤검색어가 앞. 6=경쟁 평균, 7=통과, 8=목표.\n답 형식: 후보마다 한 줄 "T1: 점수 N — 이유". 마지막 줄 "1위: 기호".')
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
open(os.path.join(H,'title_judge_raw_r6.md'),'w',encoding='utf-8').write('\n'.join(raw))
json.dump({'model':M,'scores':sc},open(os.path.join(H,'title_judge_r6.json'),'w',encoding='utf-8'),ensure_ascii=False,indent=1)
