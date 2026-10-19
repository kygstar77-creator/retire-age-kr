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
comp = '''대치동의 대표 대단지, 래미안 대치 팰리스
"20년 된 아파트가 요즘 신축보다 낫다고?"…강남 명품 아파트 3곳 봤더니
대치 학군 들어가려면 얼마 필요할까? 34평대 대표 아파트 5곳 비교
은마보다 5000만원 더 비쌌다…신축이 구축을 앞지른 '이 아파트'의 속내
송파구 잠실동 아파트 시세 및 실거래가 분석(잠실엘스, 리센츠, 트리지움, 주공5단지)'''
T = {'A': open(H+'/pkg/title.txt',encoding='utf-8').read().strip()}
S = {'S1': '국토부 실거래 · 잠실·대치·반포 / 잠실주공5단지가 리센츠보다 비쌌다 / 전세는 5억 2천 vs 13억 5천 / 84㎡대 1년 실거래 · 은마·반포미도도 비교 (노랑 바탕, 남색 큰 글자, 주황 숫자줄, 집 아이콘)'}
P = ('네이버 카페 글 제목·표지 문구 심사. 검색어 은마·잠실주공5단지·재건축 신축 비교.\n[경쟁 상위 제목]\n' + comp + '\n[본문 첫머리]\n' + lead +
     '\n[제목 후보]\n' + '\n'.join(f'{k}. {v}' for k, v in T.items()) + '\n[표지 문구]\n' + '\n'.join(f'{k}. {v}' for k, v in S.items()) +
     '\n기준: ①1초에 주제 ②궁금증 장치 ③낚시·과장 아님(본문과 일치) ④경쟁 틀 반복 아님 ⑤검색어 앞. 6=경쟁 평균,7=통과,8=목표. 답: 후보마다 한 줄 "A: 점수 N — 이유", 표지도 "S1: 점수 N — 이유", 마지막 "1위: 기호".')
raw = []
for i in (1, 2):
    t = ask(P); raw.append(t); print(t[:1500]); print('--')
open(H + '/judge_gm.md', 'a', encoding='utf-8').write('\n---\n'.join(raw) + '\n===\n')
