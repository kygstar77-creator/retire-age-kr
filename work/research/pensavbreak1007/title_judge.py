# wagepeak1007 제목 심사 — gemini-3.1-flash-lite 고정·2회. firemap-write 10/6
import sys, os, json, urllib.request, re, time
sys.stdout.reconfigure(encoding='utf-8')
H=os.path.dirname(os.path.abspath(__file__))
KEY=[l.split('=',1)[-1].strip() for l in open(r'C:\Users\강영준\Documents\gemini_key.txt',encoding='utf-8-sig') if l.strip()][0]
M='gemini-3.1-flash-lite'
C={'A':'연금저축 해지하면 세액공제 받은 것보다 얼마나 더 떼일까',
   'B':'연금저축 해지 세금 16.5%, 공제 13.2% 받은 사람은 얼마 손해일까',
   'C':'연금저축 중도해지 전에 세금 없이 먼저 꺼낼 수 있는 돈',
   'D':'연금저축 해지하면 5년 낸 3천만원에서 얼마 떼일까'}
lead=open(os.path.join(H,'pkg','c00.txt'),encoding='utf-8').read().strip()
COMP='연금저축 절대 해지하지 마세요 | 세금 1원도 안 내고 원금만 쏙 빼 쓰는 중도인출 비법 / 연금저축펀드·IRP 중도해지하면?｜중도인출 조건과 세금 총정리 / 연금저축 해지 세금, 기타소득세 16.5%와 실제 부담액 총정리 / 연금저축 중도해지 세금과 불이익, 무조건 16.5%를 내야 할까? / 연금저축 해지 기타소득세 환급 조건과 계산법 (2026년 기준)'
P=('네이버 카페 글 제목 심사. 독자: 목돈이 급해 연금저축 해지를 고민하는 40~50대. 검색어 연금저축 27,930·연금저축해지 750.\n'
   f'[경쟁 상위 제목] {COMP}\n'
   f'[본문 첫머리] {lead}\n[본문 핵심 숫자] 5년간 해마다 600만원 납입·수익 400만원 가정: 해지 세금 561만원(16.5%). 돌려받은 공제는 총급여 5,500만원 이하 495만원(16.5%)·초과 396만원(13.2%) → 더 내는 돈 66만원·165만원. 공제 안 받은 납입금은 세금 없이 먼저 인출. 55세 이후 연금이면 187만원\n[후보]\n'
   +'\n'.join(f'{k}. {v}' for k,v in C.items())+
   '\n기준: ①1초에 주제 ②궁금증 장치 하나 ③낚시·과장 아님 ④경쟁 틀 반복 아님 ⑤검색어가 앞. 6=경쟁 평균, 7=통과, 8=목표.\n답 형식: 후보마다 한 줄 "A: 점수 N — 이유". 마지막 줄 "1위: 기호".')
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
