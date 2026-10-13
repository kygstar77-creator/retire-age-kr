# P-1 '8초 안에 판 바뀜' 설계표 (2026-10-13 motion) — U5(같은 화면 8초 이하) 렌더 전 어림
# 말 줄 길이 = 음절 ÷ 속도 + 줄 사이 쉼. 속도·쉼은 G-1 실제 녹음(voice.json, Chirp korsay)에서 잰 값.
# '(화면: …)' 줄이 나오면 판 하나가 시작된다고 본다(대본이 정한 판). 그 판이 바뀌지 않고 이어지는 말 길이 합이 8초 넘으면 위험.
#   py -3.12 work/research/longform/ep/P-1/motion_preview/p1timing.py  → 표 출력 + p1_timing.json
import json, os, re, sys
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__)); EP = os.path.dirname(H); WORK = os.path.abspath(os.path.join(EP, '..', '..', '..', '..'))
sys.path.insert(0, os.path.join(WORK, 'research', 'longform', 'loop'))
import speechcompare_script as SC

# 1) G-1 실제 녹음으로 속도·쉼 재기
g1 = json.load(open(os.path.join(WORK, 'research', 'longform', 'ep', 'G-1', 'voice.json'), encoding='utf-8'))
sy = fr = n = 0
for s in g1['sections']:
    for l in s['lines']:
        if l.get('frames'):
            sy += SC.syl(SC.speak(l['text'])); fr += l['frames']; n += 1
FPS = 30
SPF = sy / fr          # 음절/프레임(쉼 포함)
print(f'G-1 녹음 {n}줄 · 쉼 포함 {SPF*FPS:.2f}음절/초')

# 2) P-1 대본: 줄과 '(화면:' 표시 순서대로
txt = open(os.path.join(EP, 'script.md'), encoding='utf-8').read().split('\n---', 1)[0]
rows, chap, board = [], None, None
for line in txt.splitlines():
    s = line.strip()
    if line.startswith('## '):
        chap = line[3:].strip(); board = chap + ' (장 첫 판)'; rows.append({'chap': chap, 'board_start': board})
    elif s.startswith('(화면:'):
        board = s[4:].rstrip(')').strip(); rows.append({'chap': chap, 'board_start': board})
    elif s.startswith('- ') and chap:
        t = re.sub(r'\s*\(화면.*$', '', s[2:]).strip()
        if t: rows.append({'chap': chap, 'text': t, 'sec': round(SC.syl(SC.speak(t)) / SPF / FPS, 1)})

# 3) 판마다 말 길이 합
out, cur, t0 = [], None, 0.0
for r in rows:
    if 'board_start' in r:
        cur = {'chap': r['chap'], 'board': r['board_start'][:60], 'start': round(t0, 1), 'lines': []}; out.append(cur)
    else:
        cur['lines'].append([r['text'], r['sec']]); t0 += r['sec']
for b in out:
    b['sec'] = round(sum(x[1] for x in b['lines']), 1)
risk = [b for b in out if b['sec'] > 8]
for b in out:
    if not b['lines']: continue
    flag = '★위험' if b['sec'] > 8 else ''
    print(f"{int(b['start']//60)}:{b['start']%60:04.1f} {b['sec']:5.1f}초 {len(b['lines']):2d}줄 {flag:4s} [{b['chap'][:14]}] {b['board'][:44]}")
print(f'총 {t0/60:.1f}분 · 판 {sum(1 for b in out if b["lines"])}개 · 8초 넘는 판 {len(risk)}개')
json.dump({'spf': SPF, 'boards': out}, open(os.path.join(H, 'p1_timing.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
