import sys,os,re,json
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0,'.')
import importlib.util
spec=importlib.util.spec_from_file_location('jr','judge_run.py')
src=open('judge_run.py',encoding='utf-8').read().split("V=os.path.join")[0]
exec(src)
base="""네이버 카페 글 제목 심사. 글 요약: 상속세 공제를 상속세및증여세법 2026년 시행본으로 정리. 같은 재산(집 10억원·예금 2억원)으로 부모 첫 상속(배우자+자녀, 공제 10억4천만원) 세금 2,037만원, 남은 부모 상속(자녀만, 일괄공제 5억원만) 1억3,240만5천원, 10년 같이 산 무주택 자녀가 집을 받으면 동거주택 상속공제 6억원이 더해져 533만5천원. '면제한도 10억'은 배우자공제 5억이 붙을 때 얘기라는 내용. 동거주택 공제 요건 3가지 포함.
후보 제목 3개와 경쟁 상위 제목 5개(네이버 블로그 탭 10/10)를 놓고 후보마다 1~10점(6=경쟁 평균, 7=통과, 8=목표). 기준: ① 1초에 주제가 보이나 ② 궁금증 장치 하나 ③ 낚시·과장 아님(본문과 일치) ④ 경쟁 제목 틀 반복 아님 ⑤ 검색어가 앞에 있나 ⑥ 한국인이 입으로 하는 말인가.
A. 상속세 면제한도 10억의 함정과 부모님과 같이 산 자녀가 덜 내는 이유
B. 상속세 면제한도 두 번째 상속에선 배우자공제가 빠지는 이유
C. 상속세 면제한도 10억이 두 번째 상속에서 안 통할 때 덜 내는 방법
경쟁: 1 상속세 면제한도 2026｜배우자·자녀 있으면 얼마까지 공제될까? 5억·배우자공제 계산 / 2 상속세 면제한도 얼마까지? 배우자·자녀 상속공제 총정리 / 3 상속세 면제한도 5억·10억 기준, 자녀·배우자 공제 총정리 / 4 상속세 면제한도, 5억일까 10억일까? 배우자·자녀 공제 쉽게 정리 / 5 "서울 아파트 한 채인데 상속세가 1억?" 2026 상속세 면제 한도(10억 룰)와 사전증여 10년 합산
답 형식: "A: 점수 / B: 점수 / C: 점수" 한 줄, 그다음 1위 이유와 고칠 곳 2줄."""
roles={'제미나이':'','레드팀':'당신은 레드팀입니다. 칭찬 말고 감점부터 하세요. 본문과 안 맞는 약속·낚시·말이 안 되는 한국어를 찾으세요.\n'}
import urllib.request
def ask_txt(t):
    err=''
    for _ in range(4):
        try:
            r=json.load(urllib.request.urlopen(urllib.request.Request(f'https://generativelanguage.googleapis.com/v1beta/models/{M}:generateContent?key={KEY}',data=json.dumps({'contents':[{'parts':[{'text':t}]}]}).encode(),headers={'Content-Type':'application/json'}),timeout=240))
            return r['candidates'][0]['content']['parts'][0]['text']
        except Exception as e: err=str(e); time.sleep(5)
    return '(실패 '+err+')'
out=[]
for k,pre in roles.items():
    t=ask_txt(pre+base); print('==',k); print(t[:900]); out.append(f'## {k} ({M})\n{t}\n')
open('title_review4.md','w',encoding='utf-8').write('\n'.join(out))
