# bigwa1006 제목 재심사(copywriter 1위 C가 틀 v2 '~요' 끝에 걸림) — gemini-3.1-flash-lite 고정·2회. firemap-write 10/6
import sys, os, json, urllib.request, re, time
sys.stdout.reconfigure(encoding='utf-8')
H=os.path.dirname(os.path.abspath(__file__))
KEY=[l.split('=',1)[-1].strip() for l in open(r'C:\Users\강영준\Documents\gemini_key.txt',encoding='utf-8-sig') if l.strip()][0]
M='gemini-3.1-flash-lite'
C={'K1':'비과세종합저축 기초연금 못 받는 65세는 이자 세금 얼마 더 낼까',
   'K2':'비과세종합저축 기초연금 없으면 5천만원 이자 세금 얼마나 붙을까',
   'K3':'비과세종합저축 65세라도 기초연금 못 받으면 세금 얼마',
   'K4':'비과세종합저축 가입 조건 바뀐 뒤 기초연금 못 받는 65세 이자 세금은 얼마일까'}
lead=open(os.path.join(H,'pkg','c00.txt'),encoding='utf-8').read().strip()
COMP=('올해부터 65세 비과세종합저축 새 가입은 기초연금 수급자만 되고... / "이자가 통째로 내 주머니로!" 2026년 비과세 종합저축 개편 및 절세 혜택 총정리 / '
      '비과세종합저축 5000만원, 이자 15.4% 아끼려면 가입 자격 확인 (2026년 9월 최신) / 2026년 기초연금 받는다면 필독! 은행도 안 알려주는 비과세 종합저축으로 115만원 지키는 법 / '
      '비과세종합저축 가입 대상 및 한도, 가입 방법부터 가입 시 주의사항까지 살펴볼게요')
P=('네이버 카페 글 제목 심사. 독자: 65세 전후 부모님 예금을 챙기는 40~60대와 본인. 검색어 비과세종합저축 월 4,170.\n'
   f'[경쟁 상위 제목] {COMP}\n'
   f'[본문 첫머리] {lead}\n[본문 핵심 숫자] 5천만원 1년 정기예금(3.33%) 이자 166만5천원, 일반 예금이면 세금 15.4% 25만6천원, 비과세종합저축이면 0원\n[후보]\n'
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
