# jongbuse1010 제목 심사(제미나이 2회) — firemap-write 10/10 (sevbasis1010 judge_t.py 틀)
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
FACT = ('종부세 1세대 1주택 고령자 공제 60~64세 20%·65~69세 30%·70세 이상 40%, 장기보유 5~9년 20%·10~14년 40%·15년 이상 50%, 합계 80% 한도. '
        '나이·보유기간은 매년 6월 1일(과세기준일) 기준이라 1956년 6월 2일생은 올해 만 70세가 됐어도 30%. 70세 이상·15년 이상만 90%가 80%로 깎임. 공제율은 재산세 몫을 뺀 뒤 남은 종부세에 곱함.')
P = ('네이버 카페 글 제목 심사. 검색어 종부세(월 9,820)·종부세계산기(5,870).\n[경쟁 상위 제목]\n' + comp +
     '\n[본문 첫머리]\n' + lead + '\n[사실] ' + FACT + '\n[후보]\n' +
     '\n'.join(f'{k}. {v}' for k, v in T.items()) +
     '\n기준: ①1초에 주제 ②궁금증 장치 ③낚시·과장 아님 ④경쟁 틀 반복 아님 ⑤검색어 앞. 6=경쟁 평균,7=통과,8=목표. 답: 후보마다 한 줄 "K1: 점수 N — 이유", 마지막 "1위: 기호".')
raw = []
for i in (1, 2):
    t = ask(P); raw.append(t); print(t[:1200]); print('--')
open(H + '/judge_title_raw.md', 'a', encoding='utf-8').write('\n---\n'.join(raw) + '\n===\n')
