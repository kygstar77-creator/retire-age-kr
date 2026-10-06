# parking1007 제목 심사 — bigwa1006 title_judge 틀, gemini-3.1-flash-lite 고정·2회. firemap-write 10/6
import sys, os, json, urllib.request, re, time
sys.stdout.reconfigure(encoding='utf-8')
H=os.path.dirname(os.path.abspath(__file__))
KEY=[l.split('=',1)[-1].strip() for l in open(r'C:\Users\강영준\Documents\gemini_key.txt',encoding='utf-8-sig') if l.strip()][0]
M='gemini-3.1-flash-lite'
C={'T1':'파킹통장 5천만원 넣으면 한 달 이자 얼마나 차이 날까',
   'T2':'파킹통장 최고 6% 금리, 5천만원 넣으면 실제로는 몇 %일까',
   'T3':'파킹통장 금리 1%와 3% 사이, 5천만원 한 달 이자는 얼마',
   'T4':'파킹통장 금리 높은 곳에 5천만원 두면 한 달 이자 얼마일까'}
lead=open(os.path.join(H,'pkg','c00.txt'),encoding='utf-8').read().strip()
COMP=' / '.join(l for l in open(os.path.join(H,'comp_titles.txt'),encoding='utf-8').read().split('\n') if '파킹' in l)
P=('네이버 카페 글 제목 심사. 독자: 퇴직금·비상금 수천만원을 잠깐 둘 곳을 찾는 50대 전후. 검색어 파킹통장 월 125,600.\n'
   f'[경쟁 상위 제목] {COMP}\n'
   f'[본문 첫머리] {lead}\n[본문 핵심 숫자] 5천만원 세후 한 달 이자: 토스 1% 35,250원 · 카카오 1.8% 63,450원 · 고려저축 3.1% 109,275원 · 최고 6% 통장(200만원까지만)에 5천만원 넣으면 전체 2.16%\n[후보]\n'
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
