# dep13y1019 제목·표지 심사(제미나이 2회)
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
comp = '''🏦 길게 묻을수록 손해본다? 1년 or 3년
우체국 예금금리 얼마일까? 1년·3년 정기예금 금리와 우대조건 비교
기준금리 3%인데 정기예금 지금 들까? 6개월·1년 가입 시기는?
정기예금 금리 비교 1억원 굴리기, 만기 세금 전략 꿀팁
4% 정기예금, '6개월 vs 1년' 뭐가 유리할까?'''
T = {'A': open(H+'/pkg/title.txt',encoding='utf-8').read().strip()}
S = {'S1': '우리은행 · 9월 공시 최고금리 / 정기예금 1년짜리가 더 높다 / 1년 3.6% · 3년 2.7% / 1억 3년, 금리 그대로면 1년짜리가 257만원 더 (흰 바탕, 남색 글자, 파랑·주황 숫자줄, 은행 건물 아이콘)'}
P = ('네이버 카페 글 제목·표지 문구 심사. 검색어 정기예금 금리·예금 1년 3년.\n[경쟁 상위 제목]\n' + comp + '\n[본문 첫머리]\n' + lead +
     '\n[제목 후보]\n' + '\n'.join(f'{k}. {v}' for k, v in T.items()) + '\n[표지 문구]\n' + '\n'.join(f'{k}. {v}' for k, v in S.items()) +
     '\n기준: ①1초에 주제 ②궁금증 장치 ③낚시·과장 아님(본문과 일치) ④경쟁 틀 반복 아님 ⑤검색어 앞. 6=경쟁 평균,7=통과,8=목표. 답: 후보마다 한 줄 "A: 점수 N — 이유", 표지도 "S1: 점수 N — 이유", 마지막 "1위: 기호".')
raw = []
for i in (1, 2):
    t = ask(P); raw.append(t); print(t[:1500]); print('--')
open(H + '/judge_gm.md', 'a', encoding='utf-8').write('\n---\n'.join(raw) + '\n===\n')
