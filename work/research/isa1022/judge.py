# isa1022 제목·표지 심사(제미나이 2회) — t1cafe1021/judge.py 꼴
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
comp = '''중개형 ISA 계좌 "국내주식은 원래 비과세?" 개설 전 알아야 할 단점 4가지
ISA 중개형 뜻 무엇일까? 서민형 조건·비과세 400만원 총정리
ISA 계좌 만들기, 중개형·신탁형·일임형과 서민형이 안 되는 이유
ISA 계좌란? 서민형 중개형 차이와 개편안까지 쉽게 정리
ISA 중개형 서민형 차이, 비과세 한도와 납입한도 쉽게 정리'''
T = {'A': 'ISA 중개형 비과세 200만원, 해마다 새로 생길까?', 'B': 'ISA 중개형 비과세 200만원은 해마다일까?', 'C': 'ISA 중개형에 고배당 ETF 3년, 세금 얼마 덜 낼까?'}
S = {'S1': 'ISA 중개형 비과세 200만원 / 해마다 아니고 통틀어서 / PLUS 고배당주 2천만원씩 3년 · 세금 약 50만원 덜 (파란 바탕, 돼지저금통 그림)'}
NL = chr(10)
P = ('네이버 카페 글 제목·표지 문구 심사. 검색어 ISA 중개형.' + NL + '[경쟁 상위 제목]' + NL + comp + NL + '[본문 첫머리]' + NL + lead
     + NL + '[제목 후보]' + NL + NL.join(f'{k}. {v}' for k, v in T.items()) + NL + '[표지 문구]' + NL + NL.join(f'{k}. {v}' for k, v in S.items())
     + NL + '기준: ①1초에 주제 ②궁금증 장치 ③낚시·과장 아님(본문과 일치) ④경쟁 틀 반복 아님 ⑤검색어 앞. 6=경쟁 평균,7=통과,8=목표. 답: 후보마다 한 줄로 점수(10점)와 이유, 표지도 점수와 이유. 한국어.')
raw = []
for i in (1, 2):
    t = ask(P); raw.append(t); print(t[:1200]); print('--')
open(H + '/judge_gm.md', 'a', encoding='utf-8').write(chr(10).join(raw) + chr(10) + '===' + chr(10))
