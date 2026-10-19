# c2cafe1019 제목·표지 심사(제미나이 2회)
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
comp = '''3억원을 IRP에 넣고 매달 200만원씩 쓰면 몇 년 버틸까?
S&P500 ETF 은퇴 후 인출 주의점, 시퀀스 리스크
S&P500 은퇴 계좌 바닥난 이유, 4% 룰의 함정
은퇴 후 7%까지 인출해도 괜찮아요! 30년 후 10억은 77억
퇴직금 s&p500에 몰빵하고 6% 인출하면'''
T = {'A': 'S&P500에 퇴직금 넣고 매달 꺼내 쓰면 몇 년 버틸까?', 'B': 'S&P500 퇴직금으로 매달 생활비 쓰면 몇 년 갈까?'}
S = {'S1': '1989~2025년 37번 계산 / S&P500 퇴직금 3억 매달 200만원 꺼내면 / 시작한 해가 갈랐다 / 1998년 시작 2011년 바닥 · 2003년 시작 2억 7천 남음 (노란 바탕, 남색 글자, 주황 숫자줄, 돼지저금통 아이콘)'}
P = ('네이버 카페 글 제목·표지 문구 심사. 검색어 S&P500 은퇴 인출·퇴직금 3억.\n[경쟁 상위 제목]\n' + comp + '\n[본문 첫머리]\n' + lead +
     '\n[제목 후보]\n' + '\n'.join(f'{k}. {v}' for k, v in T.items()) + '\n[표지 문구]\n' + '\n'.join(f'{k}. {v}' for k, v in S.items()) +
     '\n기준: ①1초에 주제 ②궁금증 장치 ③낚시·과장 아님(본문과 일치) ④경쟁 틀 반복 아님 ⑤검색어 앞. 6=경쟁 평균,7=통과,8=목표. 답: 후보마다 한 줄 "A: 점수 N — 이유", 표지도 "S1: 점수 N — 이유", 마지막 "1위: 기호".')
raw = []
for i in (1, 2):
    t = ask(P); raw.append(t); print(t[:1500]); print('--')
open(H + '/judge_gm.md', 'a', encoding='utf-8').write('\n---\n'.join(raw) + '\n===\n')
