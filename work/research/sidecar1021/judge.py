# sidecar1021 제목·표지 심사(제미나이 2회) — t1cafe1021/judge.py 꼴
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
comp = '''서킷브레이커 뜻 발동 의미 사이드카 차이 총정리
국장에 무슨 일이? 매도 사이드카·서킷브레이커 차이점 총정리
주식시장 갑자기 멈췄다? 사이드카·서킷브레이커 차이 총정리
서킷 브레이커 뜻과 사이드카 차이, 발동되면 내 주문은 어떻게 될까
사이드카 서킷브레이커 차이 쉽게 정리｜발동 조건과 10월 15일 코스피 7.57% 폭락 때 일어난 일'''
T = {'A': '사이드카 발동, 올해 52번째인데 내 주문도 멈출까?'}
S = {'S1': '오늘 코스피 매수 사이드카 / 사이드카 걸려도 보통 주문은 그대로 / 올해 코스피 52번째 / 거래소 공시 기준 · 10월 21일 오전 10시 51분'}
P = ('네이버 카페 글 제목·표지 문구 심사. 검색어 사이드카·서킷브레이커.\n[경쟁 상위 제목]\n' + comp + '\n[본문 첫머리]\n' + lead
     + '\n[제목 후보]\n' + '\n'.join(f'{k}. {v}' for k, v in T.items()) + '\n[표지 문구]\n' + '\n'.join(f'{k}. {v}' for k, v in S.items())
     + '\n기준: ①1초에 주제 ②궁금증 장치 ③낚시·과장 아님(본문과 일치) ④경쟁 틀 반복 아님 ⑤검색어 앞. 6=경쟁 평균,7=통과,8=목표. 답: 후보마다 한 줄로 점수(10점)와 이유, 표지도 점수와 이유. 한국어.')
raw = []
for i in (1, 2):
    t = ask(P); raw.append(t); print(t[:1200]); print('--')
open(H + '/judge_gm.md', 'a', encoding='utf-8').write('\n---\n'.join(raw) + '\n===\n')
