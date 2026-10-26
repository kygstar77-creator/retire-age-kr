"""D-ETF-1 shot_plan.md '장면 계획' — 구상·도구·파일 칸을 PD가 실제로 만든 화면(work/video/detf1.json, 컴포지션 DETF1)으로 맞춘다. visual 2026-10-27.
파일 = broll이면 실사 mp4(public 기준 경로) · 그 장면 스틸, 판이면 Remotion 스틸(ep/D-ETF-1/stills/rNN.jpg, stills_at.mjs로 뽑음). 비교 그림 칸은 그대로(shotcmp/rNN.jpg).
사용: py -3.12 fill_files.py  (map.json = mapframes.py가 만든 줄→장면 짝)"""
import os, re, json, sys
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); WORK = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
P = os.path.join(WORK, 'research', 'longform', 'ep', 'D-ETF-1', 'shot_plan.md')
M = json.load(open(os.path.join(HERE, 'map.json'), encoding='utf-8'))
M2 = json.load(open(os.path.join(WORK, 'video', 'detf1.json'), encoding='utf-8'))['scenes']
cred = {}
for c in json.load(open(os.path.join(WORK, 'video', 'public', 'bg', 'detf', 'stock', 'credits.json'), encoding='utf-8')) if os.path.exists(os.path.join(WORK, 'video', 'public', 'bg', 'detf', 'stock', 'credits.json')) else []:
    if isinstance(c, dict) and 'id' in c: cred[str(c['id'])] = c
KN = {'brand': '여는 판', 'big': '큰 숫자 판', 'pair': '두 숫자 비교 판', 'ask': '물음 판', 'rows': '줄 표 판', 'bars': '막대 판', 'pic': '그림 판(fig 종이 그림)', 'list5': '순서 목록 판'}
def say(dd):
    for k in ('say', 'title', 'q', 'line', 'n'):
        if isinstance(dd.get(k), str) and dd[k]: return dd[k][:40]
    return ''
t = open(P, encoding='utf-8').read(); head, plan = t.split('# 장면 계획', 1); out = []; i = 0
for l in plan.splitlines():
    if l.startswith('|') and not re.match(r'\|\s*[-장]', l):
        i += 1; rid = f'r{i:02d}'; m = M[rid]; dd = m['data'] or {}; c = l.rstrip().rstrip('|').split('|')
        # c[0]='' , c[1]장, c[2]대본, c[3]구상, c[4]경쟁, c[5]도구, c[6]파일, c[7]비교, c[8]판정
        if m['kind'] == 'broll':
            src = dd.get('src', ''); lic = dd.get('license', '')
            c[3] = f" 실사 {lic} + 흰 글자 '{say(dd)}' (DETF1 장면 {m['scene']}) "
            c[5] = ' Pexels 스톡 영상 + Remotion 글자(DETF1 broll) '
            c[6] = f' {src} · stills/{rid}.jpg '
        else:
            c[3] = f" {KN.get(m['kind'], m['kind'])} — '{say(dd)}' (DETF1 장면 {m['scene']}, 종이 결 TallyFrame)" + (f" → 다음 장면 {m['extra']} {KN.get(M2[m['extra']]['kind'], '')} '{say(M2[m['extra']]['data'])}' " if 'extra' in m else ' ')
            c[5] = f" Remotion TallyFrame({m['kind']}) " + ('+ 우리 히트맵(fig_paper.py) ' if m['kind'] == 'pic' else '')
            c[6] = f' stills/{rid}.jpg ' + (f'· stills/{rid}b.jpg ' if 'extra' in m else '')
        l = '|'.join(c) + '|'
    out.append(l)
open(P, 'w', encoding='utf-8').write(head + '# 장면 계획' + '\n'.join(out) + ('\n' if not plan.endswith('\n') else ''))
print(i, '줄')
