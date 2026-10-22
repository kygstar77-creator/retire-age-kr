# kospidd1022 제목·표지 심사(제미나이 2회) — t1cafe1021/judge.py 꼴
import sys, os, json, urllib.request, time
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__))
KEY = [l.split('=', 1)[-1].strip() for l in open(r'C:\Users\강영준\Documents\gemini_key.txt', encoding='utf-8-sig') if l.strip()][0]
M = 'gemini-3.1-flash-lite'
def ask(text):
    err = ''
    for t in range(4):
        try:
            r = json.load(urllib.request.urlopen(urllib.request.Request(f'https://generativelanguage.googleapis.com/v1beta/models/{M}:generateContent?key={KEY}', data=json.dumps({'contents': [{'parts': [{'text': text}]}]}).encode(), headers={'Content-Type': 'application/json'}), timeout=90))
            return r['candidates'][0]['content']['parts'][0]['text']
        except Exception as e:
            err = str(e); time.sleep(5)
    return '(실패 ' + err + ')'
lead = open(H + '/pkg/c00.txt', encoding='utf-8').read()
comp = '''코스피 대폭락 회복 기간, 과거에는 얼마나 걸렸나
현재 코스피 하락은 역사적으로 어느정도 일까?
"코로나·미국 강등 때와 똑같다?" 코스피 20% 빠진 10월, 1년 뒤 계좌에 벌어질 일
하락장 버티는 법 "반토막 났을 때 판 사람과 버틴 사람" 주식 폭락 회복 기간
코스피 7.57% 폭락! 과거 폭락장은 얼마나 이어졌을까?'''
T = {'A': '코스피 하락장 예전엔 본전 찾는 데 몇 년 걸렸을까?', 'B': '코스피 고점 대비 39% 하락 예전엔 본전까지 몇 년?'}
S = {'S1': '코스피 / 코스피 하락장 본전까지 몇 년 / 1.9년~5.5년 / 고점에서 30% 넘게 빠진 다섯 번 · 1997년 이후'}
P = ('네이버 카페 글 제목·표지 문구 심사. 검색어 코스피 하락·코스피 폭락 회복.\n[경쟁 상위 제목]\n' + comp + '\n[본문 첫머리]\n' + lead
     + '\n[제목 후보]\n' + '\n'.join(f'{k}. {v}' for k, v in T.items()) + '\n[표지 문구]\n' + '\n'.join(f'{k}. {v}' for k, v in S.items())
     + '\n기준: ①1초에 주제 ②궁금증 장치 ③낚시·과장 아님(본문과 일치) ④경쟁 틀 반복 아님 ⑤검색어 앞. 6=경쟁 평균,7=통과,8=목표. 답: 후보마다 한 줄로 점수(10점)와 이유, 표지도 점수와 이유. 한국어.')
raw = []
for i in (1, 2):
    t = ask(P); raw.append(t); print(t[:1200]); print('--')
open(H + '/judge_gm.md', 'a', encoding='utf-8').write('\n---\n'.join(raw) + '\n===\n')
