# ubcalc1010 표지 심사(제미나이 2회) — firemap-write 10/9
import sys, os, base64, re
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, H)

import json, urllib.request, time
KEY = [l.split('=', 1)[-1].strip() for l in open(r'C:\Users\강영준\Documents\gemini_key.txt', encoding='utf-8-sig') if l.strip()][0]
def ask(parts):
    for t in range(4):
        try:
            r = json.load(urllib.request.urlopen(urllib.request.Request(f'https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-lite:generateContent?key={KEY}', data=json.dumps({'contents': [{'parts': parts}]}).encode(), headers={'Content-Type': 'application/json'}), timeout=240))
            return r['candidates'][0]['content']['parts'][0]['text']
        except Exception as e: err = str(e); time.sleep(5)
    return '(실패 ' + err + ')'
cp = ('네이버 카페 글 대표사진 심사(휴대폰 목록 110px로 줄어 보임). 글 제목: "' + open(H + '/pkg/title.txt', encoding='utf-8').read().strip() +
      '". 사실: 실업급여 받는 날수는 전 회사 가입기간이 합쳐지면 늘어난다(고용보험법 제50조). 예: 40세, 지금 회사 11개월+전 회사 8개월이면 120일에서 150일로. ' +
      '점수: N(1~10, 6=경쟁평균, 7=통과) 형식 첫 줄, 이어서 읽히는 글자·약점·오독 위험.')
raw = []
for n in sys.argv[1:]:
    for i in (1, 2):
        t = ask([{'text': cp}, {'inline_data': {'mime_type': 'image/png', 'data': base64.b64encode(open(H + f'/covers_try/00_{n}.png', 'rb').read()).decode()}}])
        raw.append(f'[{n} {i}]\n' + t); m = re.search(r'점수[^0-9]{0,20}(\d+(?:\.\d+)?)', t); print(n, i, m.group(1) if m else t[:100])
open(H + '/judge_cover_raw.md', 'a', encoding='utf-8').write('\n---\n'.join(raw) + '\n===\n')
