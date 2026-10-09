import sys,os,re,json
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0,'.')
import importlib.util
spec=importlib.util.spec_from_file_location('jr','judge_run.py')
src=open('judge_run.py',encoding='utf-8').read().split("V=os.path.join")[0]
exec(src)
base="""네이버 카페 글 제목 심사. 글 요약: 육아휴직 급여를 월 통상임금별로 12개월 합계(200만원 2,160만원·250만원 이상은 모두 2,310만원), 부부 6+6 상한, 1~2주 단기휴직, 신청기한을 시행령 원문으로 정리. 첫 문장: 월 통상임금이 200만원인 사람과 400만원인 사람이 12개월 쓰면 150만원 차이.
후보 제목 3개와 경쟁 상위 제목 5개(네이버 블로그 탭 10/10)를 놓고 (참고: 본문 계산상 통상임금 200만원은 2,160만원, 400만원은 2,310만원이라 150만원 차이가 맞다.) 후보마다 1~10점(6=경쟁 평균, 7=통과, 8=목표). 기준: ① 1초에 주제가 보이나 ② 궁금증 장치 하나 ③ 낚시·과장 아님(본문과 일치) ④ 경쟁 제목 틀 반복 아님 ⑤ 검색어가 앞에 있나 ⑥ 한국인이 입으로 하는 말인가.
A. 육아휴직 급여 12개월, 통상임금 200만원과 400만원이 150만원 차이?
B. 육아휴직 급여 12개월 합계, 통상임금이 달라도 같은 이유
C. 육아휴직 급여 12개월 받으면 통상임금별로 얼마일까요
경쟁: 1 2026 육아휴직 급여 신청방법 금액 조건 총정리 / 2 2026 육아휴직급여 1년6개월, 6+6제도, 달라진 점 / 3 육아휴직 급여 신청방법, 고용24로 한 번에 끝내기 / 4 육아휴직 급여 6+6제도포함 신청방법부터 시기까지 총 정리 / 5 육아휴직 급여, 월 250만원 계속 받는 게 아니라고요?
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
open('title_review2.md','w',encoding='utf-8').write('\n'.join(out))
