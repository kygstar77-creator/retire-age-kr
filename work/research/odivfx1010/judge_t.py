# odivfx1010 제목 심사(제미나이 2회) — firemap-write 10/10 (sevbasis1010 judge_t.py 틀)
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
T = json.loads(open(sys.argv[1], encoding='utf-8').read())
lead = open(H + '/pkg/c00.txt', encoding='utf-8').read()
comp = open(H + '/comp_titles.txt', encoding='utf-8').read()
FACT = ('리얼티인컴(O) 월배당 10월 15일 지급분 0.2715달러(작년 10월 0.2695달러). 10월 8일 매매기준율 1,339.2원이면 주당 363.59원, 작년 10월(1,428.4원) 384.95원보다 5.55% 적음. '
        '올해 6월 지급분 411.27원(1,520.4원)→9월 364.58원(1,345.3원), 석 달 새 11.35% 감소. 100주 세후(미국 15%) 10월 30,905원, 작년 10월 32,721원. 지난 1년 12번 합계는 달러 +1.38%, 원화 +4.99%(환율 1,400원대 덕). 지금 환율이 1년 이어지면 원화 7.83% 감소.')
P = ('네이버 카페 글 제목 심사. 검색어 리얼티인컴(월 17,910)·리얼티인컴배당금(1,770).\n[경쟁 상위 제목]\n' + comp +
     '\n[본문 첫머리]\n' + lead + '\n[사실] ' + FACT + '\n[후보]\n' +
     '\n'.join(f'{k}. {v}' for k, v in T.items()) +
     '\n기준: ①1초에 주제 ②궁금증 장치 ③낚시·과장 아님 ④경쟁 틀 반복 아님 ⑤검색어 앞. 6=경쟁 평균,7=통과,8=목표. 답: 후보마다 한 줄 "K1: 점수 N — 이유", 마지막 "1위: 기호".')
raw = []
for i in (1, 2):
    t = ask(P); raw.append(t); print(t[:1200]); print('--')
open(H + '/judge_title_raw.md', 'a', encoding='utf-8').write('\n---\n'.join(raw) + '\n===\n')
