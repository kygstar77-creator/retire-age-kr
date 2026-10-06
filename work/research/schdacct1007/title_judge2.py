# spouseinh1007 제목 심사 — gemini-3.1-flash-lite 고정·2회. firemap-write 10/6
import sys, os, json, urllib.request, re, time
sys.stdout.reconfigure(encoding='utf-8')
H=os.path.dirname(os.path.abspath(__file__))
KEY=[l.split('=',1)[-1].strip() for l in open(r'C:\Users\강영준\Documents\gemini_key.txt',encoding='utf-8-sig') if l.strip()][0]
M='gemini-3.1-flash-lite'
C={'E':'SCHD 배당금 ISA나 연금저축에서 받으면 미국 세금 얼마나 빠질까',
   'F':'SCHD 배당금 200만원 ISA나 연금저축에서 받으면 얼마 남을까',
   'G':'SCHD 배당금 연금저축에서 받으면 미국 세금 몇 % 돌려받을까'}
lead=open(os.path.join(H,'pkg','c00.txt'),encoding='utf-8').read().strip()
COMP=('SCHD ETF 투자방법 총정리｜미국 직접투자·국내 ETF·ISA·연금저축 비교 / 미국배당다우존스,SCHD의 특징과 장점은 뭘까? / 절세계좌(연금저축펀드, ISA, IRP)로 알차게 계란 나눠담기 / 연금저축·IRP·ISA, 무엇부터 채워야 할까? / 연금저축펀드 ISA로 투자하기 좋은 국내상장미국ETF를 분석해보자!')
P=('네이버 카페 글 제목 심사. 독자: 배당 ETF로 노후 현금흐름을 만들려는 40~60대. 검색어 SCHD배당금 월 9,310.\n'
   f'[경쟁 상위 제목] {COMP}\n'
   f'[본문 첫머리] {lead}\n[본문 핵심] ISA·연금저축은 SCHD 직접 못 사고 같은 지수 국내 상장 ETF. 2025년부터 펀드가 낸 미국 세금 선환급 폐지 → 세전 200만원이면 세 계좌 모두 170만원 들어옴. 연금저축은 2026년 7월부터 인출 때 연금소득세 한도로 미국 세금 공제\n[후보]\n'
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
open(os.path.join(H,'title_judge_raw2.md'),'w',encoding='utf-8').write('\n'.join(raw))
json.dump({'model':M,'scores':sc},open(os.path.join(H,'title_judge2.json'),'w',encoding='utf-8'),ensure_ascii=False,indent=1)
