# ubfraud1019 제목·표지 심사(제미나이 2회)
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
comp = '''실업급여 알바 신고, 하루만 일해도 해야 할까? 신고 방법 총정리
실업급여 부정수급 기준과 처벌, 최대 5배 추가징수
실업급여 받으면서 아르바이트 가능? 주 15시간 기준 정리
실업급여 부정수급 자진신고 하면 어떻게 될까
실업급여 수급 중 일용직 근로 신고 안 하면'''
T = {'A': '실업급여 부정수급 하루 알바 숨기면 얼마나 돌려줘야 할까'}
S = {'S2': '고용보험법 제61조 / 실업급여 받는 중 하루 알바 숨기면 / 4주치 185만원 날아감 / 신고하면 그날만 하루 늦게 받음 · 하한액·4주 기준 (파란 바탕, 노란 금액, 가방 아이콘)'}
P = ('네이버 카페 글 제목·표지 문구 심사. 검색어 실업급여 부정수급(월 6,050).\n[경쟁 상위 제목]\n' + comp + '\n[본문 첫머리]\n' + lead +
     '\n[제목 후보]\n' + '\n'.join(f'{k}. {v}' for k, v in T.items()) + '\n[표지 문구]\n' + '\n'.join(f'{k}. {v}' for k, v in S.items()) +
     '\n기준: ①1초에 주제 ②궁금증 장치 ③낚시·과장 아님(본문과 일치) ④경쟁 틀 반복 아님 ⑤검색어 앞. 6=경쟁 평균,7=통과,8=목표. 답: 후보마다 한 줄 "A: 점수 N — 이유", 표지도 "S1: 점수 N — 이유", 마지막 "1위: 기호".')
raw = []
for i in (1, 2):
    t = ask(P); raw.append(t); print(t[:1500]); print('--')
open(H + '/judge_raw.md', 'a', encoding='utf-8').write('\n---\n'.join(raw) + '\n===\n')
