# coin1019 제목·표지 심사(제미나이 2회)
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
comp = '''코인 과세 2027년 시작, 세율 22%·250만원 공제 총정리
코인 세금 2027년부터 시행? 유예 법안 의원별 정리
가상자산 과세 2027년, 내 코인 취득가액은 어떻게 될까
코인으로 1000만원 벌면…세금은 165만원 낸다
코인 손실 이월공제 안 된다는데 지금 팔아야 할까'''
T = {'D': '코인 과세 시작 전 올해 말까지 오른 이익은 세금 0원'}
S = {'S2': '2027년 1월 시행 소득세법 / 코인 과세 시작 전 올해 말까지 오른 이익은 / 세금 0원 / 실제 산 값과 12월 31일 값 중 큰 쪽 (남색 바탕, 노란 세금 0원, 비트코인 아이콘)'}
P = ('네이버 카페 글 제목·표지 문구 심사. 검색어 코인과세(월 34,350).\n[경쟁 상위 제목]\n' + comp + '\n[본문 첫머리]\n' + lead +
     '\n[제목 후보]\n' + '\n'.join(f'{k}. {v}' for k, v in T.items()) + '\n[표지 문구]\n' + '\n'.join(f'{k}. {v}' for k, v in S.items()) +
     '\n기준: ①1초에 주제 ②궁금증 장치 ③낚시·과장 아님(본문과 일치) ④경쟁 틀 반복 아님 ⑤검색어 앞. 6=경쟁 평균,7=통과,8=목표. 답: 후보마다 한 줄 "A: 점수 N — 이유", 표지도 "S1: 점수 N — 이유", 마지막 "1위: 기호".')
raw = []
for i in (1, 2):
    t = ask(P); raw.append(t); print(t[:1500]); print('--')
open(H + '/judge_raw.md', 'a', encoding='utf-8').write('\n---\n'.join(raw) + '\n===\n')
