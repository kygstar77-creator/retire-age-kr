# ubcalc1010 제목 심사(제미나이 2회) — firemap-write 10/9
import sys, os, json, urllib.request, time
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__))
KEY = [l.split('=', 1)[-1].strip() for l in open(r'C:\Users\강영준\Documents\gemini_key.txt', encoding='utf-8-sig') if l.strip()][0]
M = 'gemini-3.1-flash-lite'
def ask(text):
    err = ''
    for t in range(4):
        try:
            r = json.load(urllib.request.urlopen(urllib.request.Request(f'https://generativelanguage.googleapis.com/v1beta/models/{M}:generateContent?key={KEY}', data=json.dumps({'contents': [{'parts': [{'text': text}]}]}).encode(), headers={'Content-Type': 'application/json'}), timeout=240))
            return r['candidates'][0]['content']['parts'][0]['text']
        except Exception as e:
            err = str(e); time.sleep(5)
    return '(실패 ' + err + ')'
if __name__ != "__main__": raise SystemExit
T = json.loads(sys.argv[1])
lead = open(H + '/pkg/c00.txt', encoding='utf-8').read()
comp = open(H + '/comp_titles.txt', encoding='utf-8').read()
P = ('네이버 카페 글 제목 심사. 검색어 실업급여계산기(월 98,800)·실업급여 피보험기간·실업급여 합산.\n[경쟁 상위 제목(블로그 탭 "실업급여 피보험기간 합산")]\n' + comp +
     '\n[본문 첫머리]\n' + lead +
     '\n[사실] 고용보험법 제50조: 실업급여 받는 날수는 이직일 나이와 피보험기간으로 정해지고, 전 회사에서 자격을 잃은 날부터 3년 안에 현 회사에 들어왔으면 전 회사 기간을 합산, 단 전 회사 때 구직급여를 받았으면 그 기간은 제외. 40세·월 300만원이면 하루 66,048원이라 합산으로 구간이 한 칸 올라 30일 늘면 198만원 차이. 경쟁 글 대부분은 180일 요건 합산만 다루고 금액 차이는 없음.\n[후보]\n' +
     '\n'.join(f'{k}. {v}' for k, v in T.items()) +
     '\n기준: ①1초에 주제 ②궁금증 장치 ③낚시·과장 아님 ④경쟁 틀 반복 아님 ⑤검색어 앞. 6=경쟁 평균,7=통과,8=목표. 답: 후보마다 한 줄 "K1: 점수 N — 이유", 마지막 "1위: 기호".')
raw = []
for i in (1, 2):
    t = ask(P); raw.append(t); print(t[:900]); print('--')
open(H + '/judge_title_raw.md', 'a', encoding='utf-8').write('\n---\n'.join(raw) + '\n===\n')
