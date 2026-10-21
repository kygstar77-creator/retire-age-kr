# sevmonth1021 제목·표지 심사(제미나이 2회)

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

comp = """“퇴사 날짜만 바꿨는데 퇴직금 달라졌다” 왜 4월에 나가라는 걸까
퇴사 아무 날이나 하면 손해? | 퇴직금·연차수당·상여금 더 챙기는 퇴사 꿀팁
퇴사 시기만 바꿔도 퇴직금이 달라진다? 평균임금 계산법 총정리
고용노동부 퇴직금 계산기, 평균임금 3개월 계산법과 14일 지급기한 총정리"""
T = {'A': '퇴직금, 한 달 더 다녔는데 왜 줄어들까?', 'B': '퇴직금 4월 퇴사, 한 달 더 다니면 오히려 줄어들까?', 'C': '퇴직금 계산기, 한 달 더 다녔는데 왜 줄어들까?', 'D': '퇴직금 계산, 4월 말보다 한 달 더 다니면 줄어들까?'}
S = {'S1': '기본급만 받으면 해당 없음 / 연장수당 받고 10년 넘게 / 한 달 더 다니면 / 퇴직금 77만원 줄어요 / 4월 말 대신 5월 말 퇴사 · 그 달 월급은 따로 받아요'}
P = ('네이버 카페 글 제목·표지 문구 심사. 검색어 퇴직금·퇴직금 계산기·4월 퇴사.\n[경쟁 상위 제목]\n' + comp + '\n[본문 첫머리]\n' + lead + '\n[제목 후보]\n' + '\n'.join(f'{k}. {v}' for k, v in T.items()) + '\n[표지 문구]\n' + '\n'.join(f'{k}. {v}' for k, v in S.items()) + '\n기준: ①1초에 주제 ②궁금증 장치 ③낚시·과장 아님(본문과 일치) ④경쟁 틀 반복 아님 ⑤검색어 앞. 6=경쟁 평균,7=통과,8=목표. 답: 후보마다 한 줄로 점수(10점)와 이유, 표지도 점수와 이유. 한국어.')
raw = []

for i in (1, 2):

    t = ask(P); raw.append(t); print(t[:1500]); print('--')

open(H + '/judge_gm.md', 'a', encoding='utf-8').write('\n---\n'.join(raw) + '\n===\n')

