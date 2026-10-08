# npsage1009 제목 심사 (deplend1009 틀) — bigwa1006 title_judge 틀, gemini-3.1-flash-lite 고정·2회. firemap-write 10/6
import sys, os, json, urllib.request, re, time
sys.stdout.reconfigure(encoding='utf-8')
H=os.path.dirname(os.path.abspath(__file__))
KEY=[l.split('=',1)[-1].strip() for l in open(r'C:\Users\강영준\Documents\gemini_key.txt',encoding='utf-8-sig') if l.strip()][0]
M='gemini-3.1-flash-lite'
C={'N1':'64년생 국민연금 수령나이, 미뤄 받으면 몇 살부터 더 받을까',
   'N2':'64년생 국민연금 수령나이는 63세, 당겨 받을까 미뤄 받을까',
   'N3':'64년생 국민연금 수령나이, 1년만 미뤄도 몇 살이면 따라잡을까',
   'N4':'64년생 국민연금 수령나이 65세가 아니라면 언제 받는 게 나을까',
   'N5':'64년생 국민연금 수령나이, 당기면 몇 살부터 손해일까',
   'N6':'연기연금 64년생은 몇 살까지 살아야 더 받을까'}
lead=open(os.path.join(H,'pkg','c00.txt'),encoding='utf-8').read().strip()
COMP=' / '.join(l for l in open(os.path.join(H,'comp_titles.txt'),encoding='utf-8').read().split('\n') if l.strip())
NUM=('1964년생 정상 수령 63세(2027년, 부칙 제8조), 63세 월 100만원 기준: 61세 조기 88%·62세 조기 94%·64세 연기 107.2%·68세 연기 136% · 63세와 누적이 같아지는 나이: 61세 조기 77세8개월·62세 조기 78세8개월·64세 연기 77세11개월·68세 연기 81세11개월(명목, 물가 인상분 뺌) · 2026 연금개혁은 수령 나이·조기/연기 비율 안 바꿈')
P=('네이버 카페 글 제목 심사. 독자: 1964년생(올해 61~62세)과 그 가족. 검색어 국민연금수령나이 월 45,680·연기연금 월 290·국민연금연기 월 310.\n'
   f'[경쟁 상위 제목] {COMP}\n[본문 첫머리] {lead}\n[본문 핵심 숫자] {NUM}\n[후보]\n'
   +'\n'.join(f'{k}. {v}' for k,v in C.items())+
   '\n기준: ①1초에 주제 ②궁금증 장치 하나 ③낚시·과장 아님(본문에 없는 약속 감점) ④경쟁 틀 반복 아님 ⑤검색어가 앞. 6=경쟁 평균, 7=통과, 8=목표.\n답 형식: 후보마다 한 줄 "T1: 점수 N — 이유". 마지막 줄 "1위: 기호".')
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
