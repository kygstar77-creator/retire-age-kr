# tsla1019 제목·표지 심사(제미나이 2회)
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
lead = open(H + '/pkg/c00.txt', encoding='utf-8').read()
comp = '''넷플릭스, 메타, 테슬라 실적발표 일정 "메타"실적에 주목해야하는 이유
테슬라 실적 발표 10월 22일, 지난 분기 매출 26% 늘 때 영업이익은 57% 줄었다
테슬라 3분기 실적 발표일 "차는 486,532대 팔았는데 남는 건?"
테슬라 실적발표 21일, 로드스터에도 5일째 내린 주가가 기다리는 숫자는?
테슬라 실적발표 한국시간'''
T = {'A': '테슬라 실적발표 다음 날, 지난 네 번 주가는 몇 % 움직였을까?', 'B': '테슬라 실적발표 한국 시각 22일 아침, 지난 네 번 다음 날 주가는?'}
S = {'S1': '미국 성장주 / 테슬라 실적발표 다음 날 주가는 / 지난 네 번 중 세 번 내림 / 한국 시각 10월 22일 아침 · 지난 7월엔 하루 -14.5% (노란 바탕, 자동차 그림)'}
P = ('네이버 카페 글 제목·표지 문구 심사. 검색어 테슬라 실적발표(월 590)·테슬라주가(월 494,800).\n[경쟁 상위 제목]\n' + comp + '\n[본문 첫머리]\n' + lead +
     '\n[제목 후보]\n' + '\n'.join(f'{k}. {v}' for k, v in T.items()) + '\n[표지 문구]\n' + '\n'.join(f'{k}. {v}' for k, v in S.items()) +
     '\n기준: ①1초에 주제 ②궁금증 장치 ③낚시·과장 아님(본문과 일치) ④경쟁 틀 반복 아님 ⑤검색어 앞. 6=경쟁 평균,7=통과,8=목표. 답: 후보마다 한 줄 "A: 점수 N — 이유", 표지도 "S1: 점수 N — 이유", 마지막 "1위: 기호".')
raw = []
for i in (1, 2):
    t = ask(P); raw.append(t); print(t[:1500]); print('--')
open(H + '/judge_raw.md', 'a', encoding='utf-8').write('\n---\n'.join(raw) + '\n===\n')
