# npsimui1007 제목 심사 — gemini-3.1-flash-lite 고정·2회. firemap-write 10/6
import sys, os, json, urllib.request, re, time
sys.stdout.reconfigure(encoding='utf-8')
H=os.path.dirname(os.path.abspath(__file__))
KEY=[l.split('=',1)[-1].strip() for l in open(r'C:\Users\강영준\Documents\gemini_key.txt',encoding='utf-8-sig') if l.strip()][0]
M='gemini-3.1-flash-lite'
C={'K5':'국민연금 임의가입 최저 보험료로 10년 내면 매달 얼마 받을까',
   'K6':'국민연금 임의가입 10년만 내면 연금 얼마 받을까',
   'K7':'국민연금 임의가입 전업주부가 10년 내면 연금 얼마일까'}
lead=open(os.path.join(H,'pkg','c00.txt'),encoding='utf-8').read().strip()
COMP=('고3 국민연금 임의가입들 하시나요? / 국민연금이 200가까이 받게되면 임의가입효율이 최악이네요 / 공무원퇴직했어요.국민연금 임의가입할까요? / '
      '만60세이후 국민연금 임의계속가입 하시나요? / 만 60세 직장인 국민연금 추납 및 임의계속가입관련 문의드립니다.')
P=('네이버 카페 글 제목 심사. 독자: 소득 없는 전업주부·퇴직 뒤 가입이 끊긴 40~50대. 검색어 국민연금 임의가입 월 6,650.\n'
   f'[경쟁 상위 제목] {COMP}\n'
   f'[본문 첫머리] {lead}\n[본문 핵심 숫자] 임의가입 최저 보험료 월 96,230원(2026년 4월 중위수 101만3천원×9.5%), 10년 내면 예상 연금 월 22만6,090원(공단 예상연금월액표), 10년 낸 돈 1,154만7,600원은 약 4년 3개월이면 돌려받음(보험료율 9.5% 고정 가정)\n[후보]\n'
   +'\n'.join(f'{k}. {v}' for k,v in C.items())+
   '\n기준: ①1초에 주제 ②궁금증 장치 하나 ③낚시·과장 아님 ④경쟁 틀 반복 아님 ⑤검색어가 앞. 6=경쟁 평균, 7=통과, 8=목표.\n답 형식: 후보마다 한 줄 "K1: 점수 N — 이유". 마지막 줄 "1위: 기호".')
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
