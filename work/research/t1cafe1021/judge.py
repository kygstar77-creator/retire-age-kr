# h2cafe1019 제목·표지 심사(제미나이 2회)
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
comp = '''장기보유특별공제 폐지? 2029년부터 1주택 양도세 이렇게 바뀐다
"10년 보유도 소용없다?" 2029년부터 달라지는 1주택 양도세
"미쳤네" 장특공 보유 40% 사라진다, 2029년 1주택 양도세 계산법
1세대 1주택자 장기보유특별공제 및 양도세, 어떻게 바뀌나 (2026. 8. 3 세제개편안)'''
T = {'A': '1주택 양도세 정부안, 실거주 짧으면 얼마 더 낼까', 'B': '1주택 양도세 정부안, 덜 살았으면 세금이 열두 배?', 'C': '1주택 양도세 정부안, 오래 산 집과 잠깐 산 집 차이'}
S = {'S1': '1주택 양도세 정부안 / 2년만 살았던 집 / 양도세 열두 배 / 1억 4,777만 vs 1,241만 / 10년 보유 20억 집 · 2029년 정부안'}
P = ('네이버 카페 글 제목·표지 문구 심사. 검색어 1주택 양도세·장기보유특별공제 정부안.\n[경쟁 상위 제목]\n' + comp + '\n[본문 첫머리]\n' + lead + '\n[제목 후보]\n' + '\n'.join(f'{k}. {v}' for k, v in T.items()) + '\n[표지 문구]\n' + '\n'.join(f'{k}. {v}' for k, v in S.items()) + '\n기준: ①1초에 주제 ②궁금증 장치 ③낚시·과장 아님(본문과 일치) ④경쟁 틀 반복 아님 ⑤검색어 앞. 6=경쟁 평균,7=통과,8=목표. 답: 후보마다 한 줄로 점수(10점)와 이유, 표지도 점수와 이유. 한국어.')
raw = []
for i in (1, 2):
    t = ask(P); raw.append(t); print(t[:1500]); print('--')
open(H + '/judge_gm.md', 'a', encoding='utf-8').write('\n---\n'.join(raw) + '\n===\n')
