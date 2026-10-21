# cc200vol1021 제목·표지 심사(제미나이 2회) — t1cafe1021/judge.py 꼴
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
comp = '''KODEX 200 타겟위클리커버드콜 VS KODEX 200 커버드콜액티브
KODEX 200타겟위클리커버드콜 ETF, 배당소득세 세금 계산방법 쉽다
KODEX 200타겟위클리커버드콜, 생활비는 필요하지만 성장도 포기하고 싶지 않다면
KODEX 200타겟위클리커버드콜 과세, 1억 투자하면 세금은 얼마일까? 월 500만원 현금흐름 만들기
월배당 커버드콜의 치명적 단점 3가지 (ft. KODEX 200타겟위클리커버드콜)'''
T = {'A': 'KODEX 200타겟위클리커버드콜, 급락한 날 덜 빠졌을까?', 'B': 'KODEX 200타겟위클리커버드콜, 폭락한 날 얼마나 덜 빠졌을까?'}
S = {'S1': 'KODEX 200타겟위클리커버드콜 / 급락한 날 0.3%p 덜 빠졌다 / −5.5% 대 −5.8% / KODEX 200이 3% 이상 빠진 42일 평균 · 10월 21일 종가'}
P = ('네이버 카페 글 제목·표지 문구 심사. 검색어 KODEX 200타겟위클리커버드콜·커버드콜.\n[경쟁 상위 제목]\n' + comp + '\n[본문 첫머리]\n' + lead
     + '\n[제목 후보]\n' + '\n'.join(f'{k}. {v}' for k, v in T.items()) + '\n[표지 문구]\n' + '\n'.join(f'{k}. {v}' for k, v in S.items())
     + '\n기준: ①1초에 주제 ②궁금증 장치 ③낚시·과장 아님(본문과 일치) ④경쟁 틀 반복 아님 ⑤검색어 앞. 6=경쟁 평균,7=통과,8=목표. 답: 후보마다 한 줄로 점수(10점)와 이유, 표지도 점수와 이유. 한국어.')
raw = []
for i in (1, 2):
    t = ask(P); raw.append(t); print(t[:1200]); print('--')
open(H + '/judge_gm.md', 'a', encoding='utf-8').write('\n---\n'.join(raw) + '\n===\n')
