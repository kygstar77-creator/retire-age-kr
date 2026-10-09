# acqtax1010 제목 심사(제미나이 2회) — firemap-write 10/9
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
if __name__ != "__main__": raise SystemExit
T = json.loads(sys.argv[1])
lead = open(H + '/pkg/c00.txt', encoding='utf-8').read()
comp = open(H + '/comp_titles.txt', encoding='utf-8').read()
P = ('네이버 카페 글 제목 심사. 검색어 취득세(월 11,250)·취득세계산기(32,200)·2주택취득세(1,600)·일시적2주택(1,510).\n[경쟁 상위 제목(블로그 탭 "취득세 일시적 2주택")]\n' + comp +
     '\n[본문 첫머리]\n' + lead +
     '\n[사실] 지방세법 시행령 2026.9.30 개정·10.1 시행: 취득세 일시적 2주택 처분기한이 헌 집·새 집 모두 조정대상지역이면 3년→2년. 8월 26일까지 계약·계약금 낸 경우는 종전 3년. 양도세 쪽 기준일은 8월 3일이라 8/4~8/26 계약자는 양도세 2년·취득세 3년. 못 팔면 8% 중과(10억 집 +5,100만원). 경쟁 1위·4위 글은 취득세가 여전히 3년이라고 씀.\n[후보]\n' +
     '\n'.join(f'{k}. {v}' for k, v in T.items()) +
     '\n기준: ①1초에 주제 ②궁금증 장치 ③낚시·과장 아님 ④경쟁 틀 반복 아님 ⑤검색어 앞. 6=경쟁 평균,7=통과,8=목표. 답: 후보마다 한 줄 "K1: 점수 N — 이유", 마지막 "1위: 기호".')
raw = []
for i in (1, 2):
    t = ask(P); raw.append(t); print(t[:900]); print('--')
open(H + '/judge_title_raw.md', 'a', encoding='utf-8').write('\n---\n'.join(raw) + '\n===\n')
