# deplend1009 제목 심사 (earlyjob1007 틀) — bigwa1006 title_judge 틀, gemini-3.1-flash-lite 고정·2회. firemap-write 10/6
import sys, os, json, urllib.request, re, time
sys.stdout.reconfigure(encoding='utf-8')
H=os.path.dirname(os.path.abspath(__file__))
KEY=[l.split('=',1)[-1].strip() for l in open(r'C:\Users\강영준\Documents\gemini_key.txt',encoding='utf-8-sig') if l.strip()][0]
M='gemini-3.1-flash-lite'
C={'D1':'예금 2천만원이 급할 때 예금담보대출과 일부해지 이자 차이',
   'D2':'예금담보대출 받을 때와 정기예금 중도해지할 때 이자 차이',
   'D4':'예금담보대출과 일부해지 중 이자를 덜 잃는 쪽',
   'D5':'정기예금 중도해지 전에 예금담보대출 이자부터 비교해야 하는 이유',
   'D6':'예금 안 깨고 2천만원 쓸 때 예금담보대출과 일부해지 이자 차이',
   'D8':'예금담보대출 이자 내고 쓰면 정기예금 중도해지보다 얼마 남을까',
   'D9':'정기예금 6개월 지나 2천만원이 급할 때 예금담보대출과 일부해지 비교',
   'D10':'예금담보대출 이자 내고 쓰면 중도해지와 일부해지보다 얼마 더 남을까'}
lead=open(os.path.join(H,'pkg','c00.txt'),encoding='utf-8').read().strip()
COMP=' / '.join(l for l in open(os.path.join(H,'comp_titles.txt'),encoding='utf-8').read().split('\n') if l.strip())
NUM=('우리 WON플러스·하나의 정기예금, 5천만원 1년 예금 6개월(183일) 경과 후 2천만원 필요, 세후 이자 합계(2027.4.8): 통째로 해지 우리 69.8만원·하나 57.7만원 / 2천만원 일부해지 우리 102.1만원·하나 97.2만원 / 예금담보대출 둘 다 106.4만원 / 아무것도 안 하면 152.3만원 · '
     '예금담보대출은 일부해지보다 우리 4.3만원·하나 9.2만원 더 남음(대출금리 4.6% 가정, 근거 은행 상품설명서) · 가정: 오늘 고시 금리를 가입 금리로 봄')
P=('네이버 카페 글 제목 심사. 독자: 정기예금을 넣어 두고 목돈이 급해진 50대 전후. 검색어 예금담보대출 월 1,290·예금중도해지 월 190.\n'
   f'[경쟁 상위 제목] {COMP}\n[본문 첫머리] {lead}\n[본문 핵심 숫자] {NUM}\n[후보]\n'
   +'\n'.join(f'{k}. {v}' for k,v in C.items())+
   '\n기준: ①1초에 주제 ②궁금증 장치 하나 ③낚시·과장 아님(은행·금리 가정을 모르는 채 단정하면 감점) ④경쟁 틀 반복 아님 ⑤검색어가 앞. 6=경쟁 평균, 7=통과, 8=목표.\n답 형식: 후보마다 한 줄 "T1: 점수 N — 이유". 마지막 줄 "1위: 기호".')
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
