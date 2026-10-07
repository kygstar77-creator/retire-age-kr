# sanghan1008 제목 심사 — parking1007 title_judge 틀, gemini-3.1-flash-lite 고정·2회. firemap-write 10/7
import sys, os, json, urllib.request, re, time
sys.stdout.reconfigure(encoding='utf-8')
H=os.path.dirname(os.path.abspath(__file__))
KEY=[l.split('=',1)[-1].strip() for l in open(r'C:\Users\강영준\Documents\gemini_key.txt',encoding='utf-8-sig') if l.strip()][0]
M='gemini-3.1-flash-lite'
C={'T1':'본인부담상한제 환급금 10월 8일부터 체납 보험료 빼고 주면 얼마 받을까',
   'T2':'본인부담상한제 환급금 건보료 밀렸으면 10월 8일부터 달라지는 것',
   'T3':'본인부담상한제 상한액 내 건강보험료로 보면 몇 분위일까',
   'T4':'본인부담상한제 환급금 밀린 건보료가 있으면 이제 먼저 빼고 준다는데'}
lead=open(os.path.join(H,'pkg','c00.txt'),encoding='utf-8').read().strip()
COMP=' / '.join(l for l in open(os.path.join(H,'comp_titles.txt'),encoding='utf-8').read().split('\n') if '상한' in l)
P=('네이버 카페 글 제목 심사. 독자: 퇴직 전후 50~60대, 병원비가 늘어 본인부담상한제 환급을 찾아보는 사람. 검색어 본인부담상한제 월 32,180.\n'
   f'[경쟁 상위 제목] {COMP}\n'
   f'[본문 첫머리] {lead}\n'
   '[본문 핵심 숫자] 2026.10.8 시행 국민건강보험법 제44조③: 보험료 체납이면 환급금에서 체납액 공제 후 지급 가능 · 작년 226만명 평균 136만원 · 2026 상한액 90만~843만원 · 월 건보료 구간표(지역 월 3만원이면 4~5분위 170만원) · 50대 평균 약 110만원\n[후보]\n'
   +'\n'.join(f'{k}. {v}' for k,v in C.items())+
   '\n기준: ①1초에 주제 ②궁금증 장치 하나 ③낚시·과장 아님 ④경쟁 틀 반복 아님 ⑤검색어가 앞. 6=경쟁 평균, 7=통과, 8=목표.\n답 형식: 후보마다 한 줄 "T1: 점수 N — 이유". 마지막 줄 "1위: 기호".')
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
