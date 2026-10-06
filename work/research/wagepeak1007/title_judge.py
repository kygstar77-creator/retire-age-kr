# wagepeak1007 제목 심사 — gemini-3.1-flash-lite 고정·2회. firemap-write 10/6
import sys, os, json, urllib.request, re, time
sys.stdout.reconfigure(encoding='utf-8')
H=os.path.dirname(os.path.abspath(__file__))
KEY=[l.split('=',1)[-1].strip() for l in open(r'C:\Users\강영준\Documents\gemini_key.txt',encoding='utf-8-sig') if l.strip()][0]
M='gemini-3.1-flash-lite'
C={'B':'임금피크제 퇴직금 그대로 두면 왜 4천만원 넘게 줄어들까',
   'E':'임금피크제 퇴직금 그대로 두면 얼마나 줄어들까',
   'F':'임금피크제 퇴직금 중간정산·DC 전환하면 얼마 차이',
   'G':'임금피크제 퇴직금 그대로 두면 4천만원 넘게 줄어드는 계산'}
lead=open(os.path.join(H,'pkg','c00.txt'),encoding='utf-8').read().strip()
COMP=('임금피크제 앞두고 퇴직금 5천만원 차이? DB형이라면 꼭 확인해야 할 것 / 1971년생 임금피크제 시작 전, 퇴직금부터 지켜야 한다｜DB형·DC형 전환과 수천만원 차이 / 임금피크제 계산 — 월급보다 퇴직금이 더 줄어듭니다 / 2026 임금피크제 퇴직금 얼마나 될까? 1분안에 바로 확인하세요!! / 임금피크제 하면 퇴직금도 줄어들까? DB형 퇴직연금 꼭 확인하세요')
P=('상속세 배우자 공제 최소 5억부터 최대 30억까지 계산과 신고 요건 / 상속세 배우자공제 얼마까지? 5억 기본부터 30억 한도 총정리 / 상속세 면제한도 얼마까지?｜5억·10억·20억 계산기와 배우자 공제 총정리 / 배우자 상속공제 30억원, 정말 30억까지 상속세가 없을까? / 상속세 때문에 황혼이혼? 배우자 상속공제 30억원까지 가능한데 왜 개편 논의가 나올까')
P=('네이버 카페 글 제목 심사. 독자: 임금피크제를 앞둔 50대 직장인. 검색어 임금피크제 월 5,810.\n'
   f'[경쟁 상위 제목] {COMP}\n'
   f'[본문 첫머리] {lead}\n[본문 핵심 숫자] 근속 25년 차 월급 600만원·피크 5년 60%까지 감액 가정: 그대로 두면 퇴직금 1억800만원, 피크 직전 중간정산 1억6,800만원, DC 전환 1억6,980만원. 피크 직전 계산이면 25년치만 1억5,000만원(그대로 두면 4,200만원 줄어듦). 회사는 감소를 알리고 DC 변경·산정기준 개선 의무(어기면 500만원 이하 벌금)\n[후보]\n'
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
