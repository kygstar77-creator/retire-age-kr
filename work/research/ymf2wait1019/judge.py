# ymf2wait1019 제목·표지 심사(제미나이 2회)
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
comp = '''청년미래적금 2차 심사기간, 결과는 언제 나올까?
청년미래적금 2차 심사 발표일 계좌개설기간 주의사항
청년미래적금 심사기간, 11월 13일까지인데 "10월 말 먼저 결과 나온다고?"
청년미래적금 1차 80만명 탈락.. 2차도 '이것' 놓치면 또 떨어진다
2026 청년미래적금 심사 결과 언제? 11월 계좌 개설 일정·탈락 대처법 총정리'''
T = {'A': '청년미래적금 2차 심사 자녀가 신청했다면 부모님 동의부터'}
S = {'S2': '금융위원회 1차 결과 발표 / 청년미래적금 2차 심사 부모님 동의부터 / 1차 탈락 절반이 동의·서류 / 동의 안내 받는 대로 바로 · 계좌는 11월 16~27일 평일 (밝은 회색 바탕, 검정 주제어, 파란 숫자 줄, 파란 사람 둘 아이콘)'}
P = ('네이버 카페 글 제목·표지 문구 심사. 검색어 청년미래적금(월 927,600). 독자는 50~60대 부모가 많은 카페.\n[경쟁 상위 제목]\n' + comp + '\n[본문 첫머리]\n' + lead +
     '\n[제목 후보]\n' + '\n'.join(f'{k}. {v}' for k, v in T.items()) + '\n[표지 문구]\n' + '\n'.join(f'{k}. {v}' for k, v in S.items()) +
     '\n기준: ①1초에 주제 ②궁금증 장치 ③낚시·과장 아님(본문과 일치) ④경쟁 틀 반복 아님 ⑤검색어 앞. 6=경쟁 평균,7=통과,8=목표. 답: 후보마다 한 줄 "A: 점수 N — 이유", 표지도 "S1: 점수 N — 이유", 마지막 "1위: 기호".')
raw = []
for i in (1, 2):
    t = ask(P); raw.append(t); print(t[:1500]); print('--')
open(H + '/judge_raw.md', 'a', encoding='utf-8').write('\n---\n'.join(raw) + '\n===\n')
