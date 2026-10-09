# hometown1009 제목 심사 (deplend1009 틀) — bigwa1006 title_judge 틀, gemini-3.1-flash-lite 고정·2회. firemap-write 10/6
import sys, os, json, urllib.request, re, time
sys.stdout.reconfigure(encoding='utf-8')
H=os.path.dirname(os.path.abspath(__file__))
KEY=[l.split('=',1)[-1].strip() for l in open(r'C:\Users\강영준\Documents\gemini_key.txt',encoding='utf-8-sig') if l.strip()][0]
M='gemini-3.1-flash-lite'
C={'T1':'에너지바우처 동절기, 연탄쿠폰 받으면 겨울 몫이 빠지는 이유','T2':'에너지바우처 연탄쿠폰 중복 안 되는 이유와 빠지는 겨울 몫','T3':'에너지바우처 동절기 사용 시작, 연탄쿠폰 같이 받으면 남는 돈'}
lead=open(os.path.join(H,'pkg','c00.txt'),encoding='utf-8').read().strip()
COMP=' / '.join(x for x in open(os.path.join(H,'comp_titles.txt'),encoding='utf-8').read().split(chr(10)) if x.strip())
NUM='한국에너지공단 누리집: 2026 총액 1인 295,200(괄호 40,700)·2인 407,500(58,800)·3인 532,700(75,800)·4인+ 701,300(102,000), 하·동절기 구분 없이 7.1~2027.5.31 자유 사용, 단 연탄쿠폰·연탄전환 바우처·긴급복지 연료비 희망 시 괄호 금액만(하절기만) → 1인 겨울 몫 254,500원 빠짐 · 신청 12.31까지 · 동절기 요금차감 10.1부터'
P=('네이버 카페 글 제목 심사. 독자: 기초생활수급 가구와 그 가족. 검색어 에너지바우처 월 55,200.\n'
   f'[경쟁 상위 제목] {COMP}\n[본문 첫머리] {lead}\n[본문 핵심 숫자] {NUM}\n[후보]\n'
   +'\n'.join(f'{k}. {v}' for k,v in C.items())+
   '\n기준: ①1초에 주제 ②궁금증 장치 하나 ③낚시·과장 아님(1인 기준 숫자를 모든 가구로 오독시키면 감점) ④경쟁 틀 반복 아님 ⑤검색어가 앞. 6=경쟁 평균, 7=통과, 8=목표.\n답 형식: 후보마다 한 줄 "T1: 점수 N — 이유". 마지막 줄 "1위: 기호".')
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
