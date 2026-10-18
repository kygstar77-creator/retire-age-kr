# schdfx1018 제목·표지 심사(제미나이 2회)
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
comp = '''SCHD 1,000만원 넣으면 배당금 얼마? 분기별로 계산해봤습니다
"SCHD 100주 다 모았는데 월 1만원?" 1억이면 배당 '이만큼' 주네
"10년 뒤 3배..." SCHD 배당성장 배당금 시뮬레이션
SCHD 배당투자 좋다고해서 샀는데 계속 손실입니다
미국 배당주 추천 전략, SCHD·VIG·JEPI 비교와 세후 배당금 투자법'''
T = {'D': 'SCHD 배당금 9월분, 환율 때문에 원화로는 얼마 받았을까?'}
S = {'S2': 'SCHD 배당금 / 원화로는 줄었다 / 6월보다 약 4만 4천원 덜 / 2천 주 · 세금 뗀 값 · 환율 1,537원 → 1,360원 (남색 바탕, 노란 영수증 달러 그림)'}
P = ('네이버 카페 글 제목·표지 문구 심사. 검색어 SCHD배당금(월 9,460).\n[경쟁 상위 제목]\n' + comp + '\n[본문 첫머리]\n' + lead +
     '\n[제목 후보]\n' + '\n'.join(f'{k}. {v}' for k, v in T.items()) + '\n[표지 문구]\n' + '\n'.join(f'{k}. {v}' for k, v in S.items()) +
     '\n기준: ①1초에 주제 ②궁금증 장치 ③낚시·과장 아님(본문과 일치) ④경쟁 틀 반복 아님 ⑤검색어 앞. 6=경쟁 평균,7=통과,8=목표. 답: 후보마다 한 줄 "A: 점수 N — 이유", 표지도 "S1: 점수 N — 이유", 마지막 "1위: 기호".')
raw = []
for i in (1, 2):
    t = ask(P); raw.append(t); print(t[:1500]); print('--')
open(H + '/judge_raw.md', 'a', encoding='utf-8').write('\n---\n'.join(raw) + '\n===\n')
