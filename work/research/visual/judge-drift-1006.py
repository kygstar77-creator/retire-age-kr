# 심사 흔들림 가르기(2026-10-06): 10/2 통과 표지를 (모델 x 질문 x 판) 4조건으로 재채점. py -3.12 judge-drift-1006.py
import sys, os, json, base64, urllib.request, re, time
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(H, '..'); C = os.path.join(H, 'cafe-covers-1002')
KEY = [l.split('=', 1)[-1].strip() for l in open(r'C:\Users\강영준\Documents\gemini_key.txt', encoding='utf-8-sig') if l.strip()][0]
def ask(m, text, p):
    parts = [{'text': text}, {'inline_data': {'mime_type': 'image/png', 'data': base64.b64encode(open(p, 'rb').read()).decode()}}]
    for t in range(3):
        try:
            r = json.load(urllib.request.urlopen(urllib.request.Request(f'https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={KEY}',
                data=json.dumps({'contents': [{'parts': parts}]}).encode(), headers={'Content-Type': 'application/json'}), timeout=240))
            return r['candidates'][0]['content']['parts'][0]['text']
        except Exception as e:
            err = str(e); time.sleep(4)
    return f'(실패 {err})'
def old_prompt(name):
    pkg = os.path.join(R, name, 'pkg')
    title = open(os.path.join(pkg, 'title.txt'), encoding='utf-8').read().strip()
    lead = open(os.path.join(pkg, 'c00.txt'), encoding='utf-8').read().strip()[:300]
    return ('네이버 카페 글 대표사진(목록·검색 썸네일) 심사. 이미지는 휴대폰 목록 크기(정사각형 110px) 비교판이다. 맨 왼쪽 "우리 새 표지"가 발행 전 시안, "경쟁"은 같은 검색어 네이버 카페 탭 상위 글의 실제 썸네일.\n'
     f'글 제목: "{title}"\n글 첫머리: {lead}\n'
     '제약: 숫자는 본문에 있는 것만, 과장·낚시 금지, 인물 사진 없음.\n'
     '답 형식: 첫 줄 "점수: N"(1~10, 이 목록에서 경쟁 썸네일 옆에 있을 때 먼저 누르고 싶은가 + 110px에서 글자가 읽히는가. 6=경쟁 평균, 7=통과, 8=목표) · 110px에서 읽히는 글자 · 1초 주제 한 문장 · 약점 · 8점이 되려면 고칠 것 2가지.')
NEW = ('이 이미지는 네이버 카페 글 목록에 168px 썸네일로 보이는 표지다. 1초만 봤다고 치고 답하라. 한국어로.\n'
   '1) 무엇에 대한 글로 보이나(한 줄) 2) 오해할 만한 점 3) 10점 만점 점수(1초에 주제 전달·숫자 가독·오해 없음) 4) 고칠 점 2개. 칭찬 말고 감점부터.')
def score(t):
    m = re.search(r'(?:점수[^0-9\n]{0,12}|\*\*)\s*(\d+(?:\.\d+)?)\s*(?:/\s*10|점)?', t)
    for pat in (r'점수[^0-9]{0,20}(\d+(?:\.\d+)?)', r'(\d+(?:\.\d+)?)\s*/\s*10', r'(\d+(?:\.\d+)?)\s*점'):
        m = re.search(pat, t)
        if m: return float(m.group(1))
    return None
M35, M31 = 'gemini-3.5-flash-lite', 'gemini-3.1-flash-lite'
covers = {'offimkt1002': (os.path.join(C, 'board_offimkt1002.png'), os.path.join(C, 'offimkt1002_168.png')),
          'gongjae1002': (os.path.join(C, 'board_gongjae1002.png'), os.path.join(C, 'gongjae1002_168.png')),
          'b10danji1003': (os.path.join(C, 'board_b10danji1003.png'), os.path.join(C, 'b10danji1003_168.png')),
          'b10cafe1002': (None, os.path.join(H, 'b10-cafe', '00_168.png'))}
conds = [('A 10/2판(비교판·옛질문·3.1-lite)', 'board', old_prompt, M31), ('B 비교판·옛질문·3.5-lite', 'board', old_prompt, M35),
         ('C 오늘판(단독168·감점부터·3.5-lite)', 'one', None, M35), ('D 단독168·감점부터·3.1-lite', 'one', None, M31)]
res = {}; raw = []
for name, (bd, one) in covers.items():
    for cn, kind, pf, m in conds:
        if kind == 'board' and not bd: continue
        for rep in (1, 2):
            t = ask(m, pf(name) if pf else NEW, bd if kind == 'board' else one)
            s = score(t); res.setdefault((name, cn), []).append(s); raw.append(f'### {name} | {cn} | 회{rep} | 점수 {s}\n{t}\n'); print(name, cn, rep, s, flush=True)
open(os.path.join(H, 'judge-drift-1006_raw.md'), 'w', encoding='utf-8').write('\n'.join(raw))
json.dump({f'{k[0]}|{k[1]}': v for k, v in res.items()}, open(os.path.join(H, 'judge-drift-1006.json'), 'w'), ensure_ascii=False, indent=1)
