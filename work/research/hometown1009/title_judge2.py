# hometown1009 제목 심사 (deplend1009 틀) — bigwa1006 title_judge 틀, gemini-3.1-flash-lite 고정·2회. firemap-write 10/6
import sys, os, json, urllib.request, re, time
sys.stdout.reconfigure(encoding='utf-8')
H=os.path.dirname(os.path.abspath(__file__))
KEY=[l.split('=',1)[-1].strip() for l in open(r'C:\Users\강영준\Documents\gemini_key.txt',encoding='utf-8-sig') if l.strip()][0]
M='gemini-3.1-flash-lite'
C={'T1':'고향사랑기부제 연말정산 20만원 넘으면 공제율이 떨어지는 이유','T2':'고향사랑기부제 연말정산 20만원 넘게 기부하면 공제율이 왜 내려갈까','T3':'고향사랑기부제 연말정산 10만원 넘게 기부하면 세금은 얼마나 돌려받을까'}
lead=open(os.path.join(H,'pkg','c00.txt'),encoding='utf-8').read().strip()
COMP=' / '.join(x for x in open(os.path.join(H,'comp_titles.txt'),encoding='utf-8').read().split(chr(10)) if x.strip())
NUM='조세특례제한법 제58조: 10만원 이하 100%, 10~20만원 44%, 20만원 초과 16.5%(지방소득세 포함, 고향사랑e음 안내와 같음), 한도=종합소득산출세액 · 답례품 기부액 30% 이내 · 10만 13만원어치, 20만 20만4천, 30만 25만500, 50만 34만3,500, 100만 57만6천(세금+답례품 상한) · 12월 31일까지 기부해야 올해 연말정산'
P=('네이버 카페 글 제목 심사. 독자: 연말정산을 앞둔 직장인·소득자. 검색어 고향사랑기부제 월 105,600.\n'
   f'[경쟁 상위 제목] {COMP}\n[본문 첫머리] {lead}\n[본문 핵심 숫자] {NUM}\n[후보]\n'
   +'\n'.join(f'{k}. {v}' for k,v in C.items())+
   '\n기준: ①1초에 주제 ②궁금증 장치 하나 ③낚시·과장 아님(합계(세금+답례품)를 현금 환급으로 오독시키면 감점) ④경쟁 틀 반복 아님 ⑤검색어가 앞. 6=경쟁 평균, 7=통과, 8=목표.\n답 형식: 후보마다 한 줄 "T1: 점수 N — 이유". 마지막 줄 "1위: 기호".')
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
open(os.path.join(H,'title_judge2_raw.md'),'w',encoding='utf-8').write('\n'.join(raw))
json.dump({'model':M,'scores':sc},open(os.path.join(H,'title_judge2.json'),'w',encoding='utf-8'),ensure_ascii=False,indent=1)
