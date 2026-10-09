# eitclate1009 제목 심사 (deplend1009 틀) — bigwa1006 title_judge 틀, gemini-3.1-flash-lite 고정·2회. firemap-write 10/6
import sys, os, json, urllib.request, re, time
sys.stdout.reconfigure(encoding='utf-8')
H=os.path.dirname(os.path.abspath(__file__))
KEY=[l.split('=',1)[-1].strip() for l in open(r'C:\Users\강영준\Documents\gemini_key.txt',encoding='utf-8-sig') if l.strip()][0]
M='gemini-3.1-flash-lite'
C={'E7':'근로장려금 기한 후 신청 마감일에 내면 지급 기한이 한 달 밀리는 이유',
   'E11':'근로장려금 기한 후 신청 하루 차이로 지급 기한 한 달 달라지는 이유',
   'E12':'근로장려금 기한 후 신청 12월 1일에 내면 한 달 더 기다리는 이유',
   'E13':'근로장려금 기한 후 신청 11월 30일과 12월 1일 차이',
   'E8':'근로장려금 기한 후 신청 마감 하루 전과 마감일 지급 기한 차이'}
lead=open(os.path.join(H,'pkg','c00.txt'),encoding='utf-8').read().strip()
COMP=' / '.join(l for l in open(os.path.join(H,'comp_titles.txt'),encoding='utf-8').read().split('\n') if l.strip())
NUM=('조세특례제한법 제100조의7①: 기한 후 신청은 신청한 달 말일+3개월 안에 결정(2개월 연장 단서), 제100조의8③ 결정일+30일 안에 환급 → 법정 늦어도 받는 날 10월 신청 2027.3.2 · 11월(30일까지) 3.30 · 12월 1일 4.30 · '
     '기한 후 신청 12월 1일까지, 95% 지급 · 5% 감액 예: 단독 1,500만원 약 4만4천원, 맞벌이 최대 16만5천원 · 실제 지급은 법정 기한보다 빠를 수 있음')
P=('네이버 카페 글 제목 심사. 독자: 5월 정기 신청을 놓친 저소득 근로·자영 가구(60세 이상이 수급 가구의 46%). 검색어 근로장려금 월 155,200.\n'
   f'[경쟁 상위 제목] {COMP}\n[본문 첫머리] {lead}\n[본문 핵심 숫자] {NUM}\n[후보]\n'
   +'\n'.join(f'{k}. {v}' for k,v in C.items())+
   '\n기준: ①1초에 주제 ②궁금증 장치 하나 ③낚시·과장 아님(법정 기한과 실제 지급일을 혼동시키면 감점) ④경쟁 틀 반복 아님 ⑤검색어가 앞. 6=경쟁 평균, 7=통과, 8=목표.\n답 형식: 후보마다 한 줄 "T1: 점수 N — 이유". 마지막 줄 "1위: 기호".')
def ask():
    err=''
    for t in range(4):
        try:
            r=json.load(urllib.request.urlopen(urllib.request.Request(f'https://generativelanguage.googleapis.com/v1beta/models/{M}:generateContent?key={KEY}',
              data=json.dumps({'contents':[{'parts':[{'text':P}]}]}).encode(),headers={'Content-Type':'application/json'}),timeout=240))
            return r['candidates'][0]['content']['parts'][0]['text']
        except Exception as e: err=str(e); time.sleep(5)
    return f'(실패 {err})'
P=P.replace('기준:','주의: 실제 마감은 12월 1일이다. 제목이 마감을 11월로 오해시키면 ③에서 크게 감점. 기준:')
raw=[];sc={k:[] for k in C}
for rep in (1,2):
    t=ask(); raw.append(f'### 회{rep} {M}\n{t}\n')
    for k in C:
        m=re.search(k+r'\W{0,6}(?:점수)?\s*:?\s*(\d+(?:\.\d+)?)',t); sc[k].append(float(m.group(1)) if m else None)
    print(rep,{k:v[-1] for k,v in sc.items()},flush=True)
open(os.path.join(H,'title_judge3_raw.md'),'w',encoding='utf-8').write('\n'.join(raw))
json.dump({'model':M,'scores':sc},open(os.path.join(H,'title_judge3.json'),'w',encoding='utf-8'),ensure_ascii=False,indent=1)
