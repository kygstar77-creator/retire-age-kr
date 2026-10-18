# yeoui1019 제목·표지 심사(제미나이 2회)
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
comp = '''여의도 아크로더원, 얼마까지 갈까?
브라이튼 여의도 매매, 지금 얼마에 나와 있을까? 84㎡부터 132㎡까지 현재 호가 총정리
여의도 아파트 급매, 지금이 마지막 기회일까? 35평 저층 매물 총정리
여의도·밤섬 한강뷰 아파트 시세
한강이 보이면 10억 더 비싸다고? 아파트 가격을 바꾸는 6가지 뷰'''
T = {'A': '여의도 구축 아파트 층별 가격, 같은 단지 저층과 위층은 얼마나 차이 날까', 'B': '여의도 구축 아파트 저층과 위층, 같은 단지 안에서 값이 얼마나 다를까?'}
S = {'S1': '국토교통부 실거래가 / 여의도 구축 아파트 저층 vs 위층 / 위층이 1.5% 남짓 비쌈 / 1970년대 입주 단지끼리 · 단지별로는 엇갈림 (파란 바탕, 노란 숫자, 건물 아이콘)'}
P = ('네이버 카페 글 제목·표지 문구 심사. 검색어 여의도 아파트(월 5,280).\n[경쟁 상위 제목]\n' + comp + '\n[본문 첫머리]\n' + lead +
     '\n[제목 후보]\n' + '\n'.join(f'{k}. {v}' for k, v in T.items()) + '\n[표지 문구]\n' + '\n'.join(f'{k}. {v}' for k, v in S.items()) +
     '\n기준: ①1초에 주제 ②궁금증 장치 ③낚시·과장 아님(본문과 일치) ④경쟁 틀 반복 아님 ⑤검색어 앞. 6=경쟁 평균,7=통과,8=목표. 답: 후보마다 한 줄 "A: 점수 N — 이유", 표지도 "S1: 점수 N — 이유", 마지막 "1위: 기호".')
raw = []
for i in (1, 2):
    t = ask(P); raw.append(t); print(t[:1500]); print('--')
open(H + '/judge_gm.md', 'a', encoding='utf-8').write('\n---\n'.join(raw) + '\n===\n')
