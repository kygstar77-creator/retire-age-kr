# isapen1009 제목 심사 (earlyjob1007 틀) (parking1007 틀) — bigwa1006 title_judge 틀, gemini-3.1-flash-lite 고정·2회. firemap-write 10/6
import sys, os, json, urllib.request, re, time
sys.stdout.reconfigure(encoding='utf-8')
H=os.path.dirname(os.path.abspath(__file__))
KEY=[l.split('=',1)[-1].strip() for l in open(r'C:\Users\강영준\Documents\gemini_key.txt',encoding='utf-8-sig') if l.strip()][0]
M='gemini-3.1-flash-lite'
C={'J1':'ISA계좌 만기 연금저축 이전, 연말 연초에 나눠도 공제 한도는 300만원',
   'J2':'ISA 만기 자금 연금으로 옮길 때 해를 나눠도 공제가 한 번인 이유',
   'J3':'ISA 만기 연금저축 이전, 소득 없는 해에 옮기면 300만원 공제도 헛것',
   'J4':'ISA계좌 만기 3년 지나면 연금저축으로 옮길 때 놓치기 쉬운 세 가지'}
lead=open(os.path.join(H,'pkg','c00.txt'),encoding='utf-8').read().strip()
COMP=' / '.join(l for l in open(os.path.join(H,'comp_titles.txt'),encoding='utf-8').read().split('\n') if l.strip())
NUM=('ISA 만기 뒤 60일 안에 연금저축·IRP로 옮기면 옮긴 돈 10%(최대 300만원)가 세액공제 한도에 더해짐 · 3천만원이면 49만5천원/39만6천원 · '
     '12월·1월 나눠 옮겨도 300만원은 한 번(다음 해 = 300만 − 앞 해 적용분) · 소득 없는 해엔 돌려받을 세금 없음 · 3년 지나면 만기 전 이전도 만기로 봄 · 9/1 정부안에서 ISA 5년 제한 철회 보도')
P=('네이버 카페 글 제목 심사. 독자: ISA를 3년 채워 만기 처리를 고민하는 40~50대 직장인. 검색어 ISA계좌 월 73,300·ISA만기 990.\n'
   f'[경쟁 상위 제목] {COMP}\n[본문 첫머리] {lead}\n[본문 핵심 숫자] {NUM}\n[후보]\n'
   +'\n'.join(f'{k}. {v}' for k,v in C.items())+
   '\n기준: ①1초에 주제 ②궁금증 장치 하나 ③낚시·과장 아님(본문과 일치) ④경쟁 틀 반복 아님 ⑤검색어가 앞. 6=경쟁 평균, 7=통과, 8=목표.\n답 형식: 후보마다 한 줄 "T1: 점수 N — 이유". 마지막 줄 "1위: 기호".')
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
