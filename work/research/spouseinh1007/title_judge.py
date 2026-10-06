# spouseinh1007 제목 심사 — gemini-3.1-flash-lite 고정·2회. firemap-write 10/6
import sys, os, json, urllib.request, re, time
sys.stdout.reconfigure(encoding='utf-8')
H=os.path.dirname(os.path.abspath(__file__))
KEY=[l.split('=',1)[-1].strip() for l in open(r'C:\Users\강영준\Documents\gemini_key.txt',encoding='utf-8-sig') if l.strip()][0]
M='gemini-3.1-flash-lite'
C={'A':'상속세 배우자공제 20억 집이면 배우자 몫 따라 세금 얼마나 달라질까',
   'B':'상속세 배우자공제 배우자가 한 푼도 안 받으면 세금 얼마나 더 낼까',
   'C':'상속세 배우자공제 기한 넘기면 5억만 빠지는 이유',
   'D':'상속세 배우자공제 20억 집 배우자 몫 따라 세금 얼마 차이'}
lead=open(os.path.join(H,'pkg','c00.txt'),encoding='utf-8').read().strip()
COMP=('상속세 배우자 공제 최소 5억부터 최대 30억까지 계산과 신고 요건 / 상속세 배우자공제 얼마까지? 5억 기본부터 30억 한도 총정리 / 상속세 면제한도 얼마까지?｜5억·10억·20억 계산기와 배우자 공제 총정리 / 배우자 상속공제 30억원, 정말 30억까지 상속세가 없을까? / 상속세 때문에 황혼이혼? 배우자 상속공제 30억원까지 가능한데 왜 개편 논의가 나올까')
P=('네이버 카페 글 제목 심사. 독자: 부모 중 한 분이 돌아가셨거나 상속을 준비하는 40~60대. 검색어 상속세배우자공제 월 970.\n'
   f'[경쟁 상위 제목] {COMP}\n'
   f'[본문 첫머리] {lead}\n[본문 핵심 숫자] 배우자+자녀2·시가 20억 집: 배우자 0원이면 상속세 약 2억3,280만원, 배우자가 법정상속분(약 8억5,714만원) 받으면 약 1억2,887만원 → 1억원 넘게 차이. 분할기한 넘기면 5억만 공제\n[후보]\n'
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
