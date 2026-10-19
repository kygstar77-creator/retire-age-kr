# kospioct1019 제목·표지 심사(제미나이 2회)
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
comp = '''코스피 급락 이유 총정리｜코스닥 매도 사이드카 발동, 미국 CPI 쇼크
오늘 코스피 상승 진짜일까 훼이크일까? 3% 급락 후 회복과 외국인 매수 진실 분석
국내 증시 폭락, 왜 떨어졌나? 코스피 급락 원인과 삼성전자·SK하이닉스 전망
코스피 급락, 지금 팔아야 할까? 계좌보다 먼저 확인할 3가지
골드만삭스 "20년간 딱 두 번 있었다"…코스피 급락, 코로나·미국 신용등급 강등 때와 비슷'''
T = {'D': '코스피 올해 흔들린 정도, 1997년 이후 순위로 따져 보니'}
S = {'S3': '코스피 지수 직접 계산 / 코스피 올해 흔들림 1997년 이후 몇 위 / 빠진 달 수 1위·고점 대비 5위 / 10월은 16일까지 17.1% 하락 (밝은 회색 바탕, 검정 주제어, 파란 숫자 줄, 파란 하락 화살표)'}
P = ('네이버 카페 글 제목·표지 문구 심사. 검색어 코스피 급락(오늘 이슈). 독자는 50~60대 퇴직 전후가 많은 카페.\n[경쟁 상위 제목]\n' + comp + '\n[본문 첫머리]\n' + lead +
     '\n[제목 후보]\n' + '\n'.join(f'{k}. {v}' for k, v in T.items()) + '\n[표지 문구]\n' + '\n'.join(f'{k}. {v}' for k, v in S.items()) +
     '\n기준: ①1초에 주제 ②궁금증 장치 ③낚시·과장 아님(본문과 일치) ④경쟁 틀 반복 아님 ⑤검색어 앞. 6=경쟁 평균,7=통과,8=목표. 답: 후보마다 한 줄 "A: 점수 N — 이유", 표지도 "S1: 점수 N — 이유", 마지막 "1위: 기호".')
raw = []
for i in (1, 2):
    t = ask(P); raw.append(t); print(t[:1500]); print('--')
open(H + '/judge_raw.md', 'a', encoding='utf-8').write('\n---\n'.join(raw) + '\n===\n')
