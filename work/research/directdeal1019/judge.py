# directdeal1019 제목·표지 심사(제미나이 2회)
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
comp = '''아파트 직거래 증여세 30% 룰, 시세별 합법 절세 기준
서울 아파트 직거래 총정리 : 8월 3,514건 중 175건, 비중 5.0퍼센트로 2년 새 뛰었습니다.
가족간 부동산 거래, 얼마에 매매해야 할까? 증여세·양도세·취득세 기준
가족간 부동산 매매 세금 정리｜부모 자녀 간 저가양도 양도세·증여세·취득세 기준
부모 자식 간 아파트 저가양도 증여세 0원? 3억 원 한도와 양도세 폭탄 주의'''
T = {'A': open(H+'/pkg/title.txt',encoding='utf-8').read().strip()}
S = {'S1': '서울 개인끼리 직거래 742건 · 가족 여부 모름 / 아파트 직거래 중개보다 22% 쌌다 / 증여세 선은 3억·30% / 가족 간 거래 · 양도세·취득세는 5%부터 (흰 바탕, 검은 큰 글자, 파랑 숫자줄, 아파트 건물 아이콘)'}
P = ('네이버 카페 글 제목·표지 문구 심사. 검색어 아파트 직거래·가족간 매매 증여세.\n[경쟁 상위 제목]\n' + comp + '\n[본문 첫머리]\n' + lead +
     '\n[제목 후보]\n' + '\n'.join(f'{k}. {v}' for k, v in T.items()) + '\n[표지 문구]\n' + '\n'.join(f'{k}. {v}' for k, v in S.items()) +
     '\n기준: ①1초에 주제 ②궁금증 장치 ③낚시·과장 아님(본문과 일치) ④경쟁 틀 반복 아님 ⑤검색어 앞. 6=경쟁 평균,7=통과,8=목표. 답: 후보마다 한 줄 "A: 점수 N — 이유", 표지도 "S1: 점수 N — 이유", 마지막 "1위: 기호".')
raw = []
for i in (1, 2):
    t = ask(P); raw.append(t); print(t[:1500]); print('--')
open(H + '/judge_gm.md', 'a', encoding='utf-8').write('\n---\n'.join(raw) + '\n===\n')
