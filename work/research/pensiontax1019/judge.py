# pensiontax1019 제목·표지 심사(제미나이 2회)
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
comp = '''연금 수령 세금 정리, 연금저축 IRP 55세 5.5% 연금소득세와 연 1,500만원 넘으면 달라지는 과세
연금저축 세액공제 148만원 받아도…55세 넘어 꺼낼 때 떼는 세금은 얼마일까?
부모님 연금저축, 한도 넘게 찾으면.. 세금 330만 원
70대 연금저축 ETF 세금, 연 1500만원이 중요한 이유
IRP 연금저축 수령방법, 한 해에 몰아 받으면 세금 3배 (2026 최신)'''
T = {'A': '연금저축 연금소득세는 연 1,500만원을 넘으면 더 나올까', 'B': '연금저축 세금, 연금이 1,500만원 넘으면 오히려 돌려받는 경우'}
S = {'S1': '연금저축 세금 / 1,500만원 넘으면 / 받는 연금 2,000만원이면 33만원 환급 / 다른 소득 없는 69세 이하 · 지방소득세 포함 (파란 바탕, 돼지저금통)'}
P = ('네이버 카페 글 제목·표지 문구 심사. 검색어 연금저축 세금.\n[경쟁 상위 제목]\n' + comp + '\n[본문 첫머리]\n' + lead +
     '\n[제목 후보]\n' + '\n'.join(f'{k}. {v}' for k, v in T.items()) + '\n[표지 문구]\n' + '\n'.join(f'{k}. {v}' for k, v in S.items()) +
     '\n기준: ①1초에 주제 ②궁금증 장치 ③낚시·과장 아님(본문과 일치) ④경쟁 틀 반복 아님 ⑤검색어 앞. 6=경쟁 평균,7=통과,8=목표. 답: 후보마다 한 줄 "A: 점수 N — 이유", 표지도 "S1: 점수 N — 이유", 마지막 "1위: 기호".')
raw = []
for i in (1, 2):
    t = ask(P); raw.append(t); print(t[:1500]); print('--')
open(H + '/judge_raw.md', 'a', encoding='utf-8').write('\n---\n'.join(raw) + '\n===\n')
