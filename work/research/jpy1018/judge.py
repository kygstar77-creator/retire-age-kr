# jpy1018 제목·표지 심사(제미나이 2회)
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
comp = '''일본 여행 환전 총정리｜엔화 환전·카드·현금 얼마나 필요할까
100엔 846원 18년 만에 최저가! 엔화 환전 시기와 매수 팁 정리
환율 2년 만에 최저 1330원대, 달러 엔화 환전 시기 판단 기준 정리
토스 엔화 환전 방법, 수수료 0원인데 일본에서 현금은 어떻게 뽑나요? (100엔 843원 엔저)
일본 여행 | 엔화 환전, 7월보다 6% 싸졌어요'''
T = {'A': '엔화 환전, 같은 100만원인데 작년보다 엔이 더 나오는 이유', 'B': '엔화 환전 100만원, 작년보다 1만 1천 엔 더 받는 지금 환율'}
S = {'S1': '엔화 환전 / 1년 전보다 더 받는다 / 100만원에 1만 1천 엔 더 / 100엔 943원 → 853원 · 한국은행 기준 환율 (파란 바탕, 은행 건물 그림)'}
P = ('네이버 카페 글 제목·표지 문구 심사. 검색어 엔화환전(월 40,450).\n[경쟁 상위 제목]\n' + comp + '\n[본문 첫머리]\n' + lead +
     '\n[제목 후보]\n' + '\n'.join(f'{k}. {v}' for k, v in T.items()) + '\n[표지 문구]\n' + '\n'.join(f'{k}. {v}' for k, v in S.items()) +
     '\n기준: ①1초에 주제 ②궁금증 장치 ③낚시·과장 아님(본문과 일치) ④경쟁 틀 반복 아님 ⑤검색어 앞. 6=경쟁 평균,7=통과,8=목표. 답: 후보마다 한 줄 "A: 점수 N — 이유", 표지도 "S1: 점수 N — 이유", 마지막 "1위: 기호".')
raw = []
for i in (1, 2):
    t = ask(P); raw.append(t); print(t[:1500]); print('--')
open(H + '/judge_raw.md', 'a', encoding='utf-8').write('\n---\n'.join(raw) + '\n===\n')
