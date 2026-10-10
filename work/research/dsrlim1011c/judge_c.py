# dsrlim1011c 표지 심사(제미나이 2회)
import sys, os, base64, re, json, urllib.request, time
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__))
KEY = [l.split('=', 1)[-1].strip() for l in open(r'C:\Users\강영준\Documents\gemini_key.txt', encoding='utf-8-sig') if l.strip()][0]
def ask(parts):
    err = ''
    for t in range(4):
        try:
            r = json.load(urllib.request.urlopen(urllib.request.Request(f'https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-lite:generateContent?key={KEY}', data=json.dumps({'contents': [{'parts': parts}]}).encode(), headers={'Content-Type': 'application/json'}), timeout=240))
            return r['candidates'][0]['content']['parts'][0]['text']
        except Exception as e: err = str(e); time.sleep(5)
    return '(실패 ' + err + ')'
cp = ('네이버 카페 글 대표사진 심사(휴대폰 목록 110px로 줄어 보임). 글 제목: "' + open(H + '/pkg/title.txt', encoding='utf-8').read().strip() + '". ' +
      open(H + '/judge_fact.txt', encoding='utf-8').read() + ' 점수: N(1~10, 6=경쟁평균, 7=통과) 형식 첫 줄, 이어서 읽히는 글자·약점·오독 위험.')
raw = []
for n in sys.argv[1:]:
    for i in (1, 2):
        t = ask([{'text': cp}, {'inline_data': {'mime_type': 'image/png', 'data': base64.b64encode(open(H + f'/covers_try/00_{n}.png', 'rb').read()).decode()}}])
        raw.append(f'[{n} {i}]\n' + t); m = re.search(r'점수[^0-9]{0,20}(\d+(?:\.\d+)?)', t); print(n, i, m.group(1) if m else t[:100])
open(H + '/judge_cover_raw.md', 'a', encoding='utf-8').write('\n---\n'.join(raw) + '\n===\n')
