# yangdo1006 제목 재심사(readcheck 제목 숫자·길이 지적 해소안) — gemini-3.1-flash-lite 고정·2회. firemap-write 10/6
import sys, os, json, urllib.request, re, time
sys.stdout.reconfigure(encoding='utf-8')
H=os.path.dirname(os.path.abspath(__file__))
KEY=[l.split('=',1)[-1].strip() for l in open(r'C:\Users\강영준\Documents\gemini_key.txt',encoding='utf-8-sig') if l.strip()][0]
M='gemini-3.1-flash-lite'
C={'E2':'양도세 12억 넘는 1주택, 거주 햇수에 따라 공제가 최대 30%와 80%로 갈려요','E3':'양도세 12억 넘는 집 한 채, 거주 햇수에 따라 공제가 크게 갈려요','E4':'양도세 12억 넘는 집 한 채, 직접 살았는지로 공제가 두 배 넘게 갈려요'}
lead=open(os.path.join(H,'pkg','c00.txt'),encoding='utf-8').read().strip()
P=('네이버 카페 글 제목 심사. 독자: 퇴직 뒤 집을 줄여 가려는 50~60대. 검색어 양도소득세 월 24,090·1세대1주택비과세 1,130.\n'
 '[경쟁 상위 제목] 1세대 1주택도 12억 넘으면 양도세 / 비과세 받아도 양도소득세 나오는 집 / 12억원 초과 1주택, 양도세는 어떻게 계산하나요? / 1주택 15억 아파트 양도세 계산법 (12억 초과·장특공 80%) / 고가주택 (12억 초과) 양도세, 1세대 1주택 비과세 관련해서\n'
 f'[본문 첫머리] {lead}\n[후보]\n'+'\n'.join(f'{k}. {v}' for k,v in C.items())+
 '\n기준: ①1초에 주제 ②궁금증 장치 하나 ③낚시·과장 아님 ④경쟁 틀 반복 아님 ⑤검색어가 앞. 6=경쟁 평균, 7=통과, 8=목표.\n답 형식: 후보마다 한 줄 "E2: 점수 N — 이유". 마지막 줄 "1위: 기호".')
def ask():
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
