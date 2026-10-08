# editor 10/8 같은 날 얼마…ㄹ까 5칸 → 명사 끝 후보 재심사(기존 채택안 대조로 같이)
# ltcgrade1007 제목 심사 — gemini-3.1-flash-lite 고정·2회. firemap-write 10/6
import sys, os, json, urllib.request, re, time
sys.stdout.reconfigure(encoding='utf-8')
H=os.path.dirname(os.path.abspath(__file__))
KEY=[l.split('=',1)[-1].strip() for l in open(r'C:\Users\강영준\Documents\gemini_key.txt',encoding='utf-8-sig') if l.strip()][0]
M='gemini-3.1-flash-lite'
C={'G': '장기요양등급 75점 문턱, 한 달 한도는 얼마나 갈릴까', 'N1': '장기요양등급 75점 문턱에서 갈리는 한 달 한도', 'N2': '장기요양등급 75점 한 점 차이로 갈리는 재가 한도', 'N3': '장기요양등급 75점 문턱, 2등급 3등급 한 달 한도 차이'}
lead=open(os.path.join(H,'pkg','c00.txt'),encoding='utf-8').read().strip()
COMP='노인장기요양등급 신청 절차 & 등급별 혜택 총정리 (환급·복지용구 포함) / "5단계 나뉩니다" 노인장기요양보험 등급 혜택 / 2026 치매 장기요양등급 신청방법 1~5등급 기준·방문요양·요양보호사 비용 총정리 / 노인장기요양보험 등급 기준부터 혜택까지 총정리｜1~5등급 점수와 2026년 지원금액 / 2026년 노인장기요양보험 등급 판정 기준과 소득별 본인부담금 얼마일까?'
P=('네이버 카페 글 제목 심사. 독자: 부모님 장기요양등급을 신청했거나 결과를 받은 40~60대. 검색어 장기요양등급 20,590.\n'
   f'[경쟁 상위 제목] {COMP}\n'
   f'[본문 첫머리] {lead}\n[본문 핵심 숫자] 2026 재가 월 한도 1등급 251만2,900·2등급 233만1,200·3등급 152만8,200원. 2→3등급 한도 차이 80만3천원(다른 칸은 20만원 남짓). 같은 233만원어치 쓰면 2등급 본인 35만원·3등급 103만원(한도 넘는 돈 전액 본인). 요양원 30일 본인부담 1등급 55만8천원. 75점부터 2등급\n[후보]\n'
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
open(os.path.join(H,'title_judge_v2_raw.md'),'w',encoding='utf-8').write('\n'.join(raw))
json.dump({'model':M,'scores':sc},open(os.path.join(H,'title_judge_v2.json'),'w',encoding='utf-8'),ensure_ascii=False,indent=1)
