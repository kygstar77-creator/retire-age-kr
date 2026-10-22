# rtcancel1022 제목·표지 심사(제미나이 2회) — cc200vol1021/judge.py 꼴
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
lead = open(H + '/pkg/c00.txt', encoding='utf-8').read()  # 2차(레드팀 반영 뒤)
comp = '''실거래가에 ‘해제’ 표시가 붙었다면, 이 가격도 시세에 넣어야 할까요?
아파트 실거래가 조회, 등기일과 해제 표시까지 보는 법
아파트 실거래가 조회 방법, 해제 거래·층·거래량까지 읽는 법
아파트 실거래가 등기여부 확인방법은?
[아파트 실거래가 조회 방법｜국토교통부에서 매매 가격 확인하기]'''
T = {'A': '아파트 실거래가 해제 거래, 집값 띄우기였을까?', 'B': '아파트 실거래가 해제 표시, 정말 집값 띄우기일까?'}
S = {'S1': "(큰 글) 아파트 실거래가 / '해제' 붙은 거래 1,933건 / 4건 중 3건은 같은 날·같은 가격 재신고 (작은 글) 서울 최근 1년 계약 / (띠 그림 한 줄: 같은 날·같은 가격 다시 신고 1,438 · 비슷한 거래 281 · 다시 신고 없음 214)"}
P = ('네이버 카페 글 제목·표지 문구 심사. 검색어 아파트 실거래가·실거래가 해제.\n[경쟁 상위 제목]\n' + comp + '\n[본문 첫머리]\n' + lead
     + '\n[제목 후보]\n' + '\n'.join(f'{k}. {v}' for k, v in T.items()) + '\n[표지 문구]\n' + '\n'.join(f'{k}. {v}' for k, v in S.items())
     + '\n기준: ①1초에 주제 ②궁금증 장치 ③낚시·과장 아님(본문과 일치) ④경쟁 틀 반복 아님 ⑤검색어 앞. 6=경쟁 평균,7=통과,8=목표. 답: 후보마다 한 줄로 점수(10점)와 이유, 표지도 점수와 이유. 한국어.')
raw = []
for i in (1, 2):
    t = ask(P); raw.append(t); print(t[:1200]); print('--')
open(H + '/judge_gm.md', 'a', encoding='utf-8').write('\n---\n'.join(raw) + '\n===\n')
