# deprise1010 제목 심사(제미나이 2회) — ubcalc1010 judge_t 틀
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
P = ('네이버 카페 글 제목 심사. 검색어 정기예금금리(월 94,300)·예금금리비교(22,460).\n[경쟁 상위 제목(블로그 탭 "정기예금 금리 인상")]\n' + comp +
     '\n[본문 첫머리]\n' + lead +
     '\n[사실] 한국은행 통계: 예금은행 1년 정기예금 신규취급 평균 2025년 8월 2.51% → 2026년 8월 3.39%(+0.88%p). 같은 기간 산금채 1년물 월평균 2.49% → 3.64%(+1.14%p)라 예금이 시장금리보다 0.25%p 낮아짐. 1억 1년 세후 이자 212만원 → 287만원(+74만원). 기준금리 3.00%, 다음 결정 10월 22일. 경쟁 글은 4%·저축은행 순위·갈아타기 위주이고 시장금리 대비 예금 간격을 숫자로 짚은 글은 없음.\n[후보]\n' +
     '\n'.join(f'{k}. {v}' for k, v in T.items()) +
     '\n기준: ①1초에 주제 ②궁금증 장치 ③낚시·과장 아님 ④경쟁 틀 반복 아님 ⑤검색어 앞. 6=경쟁 평균,7=통과,8=목표. 답: 후보마다 한 줄 "K1: 점수 N — 이유", 마지막 "1위: 기호".')
raw = []
for i in (1, 2):
    t = ask(P); raw.append(t); print(t[:900]); print('--')
open(H + '/judge_title_raw.md', 'a', encoding='utf-8').write('\n---\n'.join(raw) + '\n===\n')
