# 한 편 안에서 같은 실사 클립을 몇 번 쓰는지 센다 (registry B-60, 2026-11-24 motion-designer).
# 근거: 경쟁 실사 쓰는 롱폼 — 수페TV hDHVtwBMUzs·누룽지 C94230lZDQQ 같은 클립 재사용 0, 돈되는집 ta9n_bzD9mU(조회 7천)만 최대 4번
#       (대신 재사용 컷마다 그 줄의 대상 글자를 실사 위에 얹음). KOSPI-1은 파란 그래프 4번·책 더미 3번.
# 쓰는 법: py -3.12 work/clipcount.py research/longform/ep/<편>
#   ① bg_used.json(편 props 스크립트가 만든 실제 사용 수 — 렌더에 들어가는 값)이 있으면 그걸 먼저 센다.
#      KOSPI-1은 shot_plan엔 클립마다 1번이었지만 kospi1props.py broll()이 같은 ID를 되풀이해 3945008 9번·38557069 6번·5224014 6번.
#   ② 없으면 shot_plan.md '장면 계획' 표 '파일' 칸의 stock/<id> 를 센다.
#   'used'는 장면(scene) 수라 바로 이어 붙은 토막도 1씩 센다 — 화면에서 따로 보이는 횟수는 그보다 적을 수 있다.
# 기준(권장, 자동 막음 없음): 같은 클립 1번이 기본, 2번째는 그 줄의 대상 글자를 실사 위에 얹을 때만, 3번 이상은 다른 클립·판으로.
import os, re, sys, collections
sys.stdout.reconfigure(encoding='utf-8')
ep = sys.argv[1]
if not os.path.isabs(ep): ep = os.path.join(os.path.dirname(os.path.abspath(__file__)), ep)
p = os.path.join(ep, 'shot_plan.md')
bu = os.path.join(ep, 'bg_used.json')
if os.path.exists(bu):
    import json
    rows = [r for r in json.load(open(bu, encoding='utf-8')) if '/stock/' in r.get('file', '')]
    print('## bg_used.json (props 실제 사용)'); print('| 클립 ID | 이 편 사용 횟수 | 판정 |'); print('|---|---|---|')
    for r in sorted(rows, key=lambda r: -r.get('used', 0)):
        n = r.get('used', 0)
        print('| %s | %d | %s |' % (r['id'], n, '1번' if n <= 1 else ('2번 — 둘째 컷에 그 줄 대상 글자 얹기 확인' if n == 2 else '**3번 이상 — 다른 클립·판으로**')))
    print('\n클립 %d종 · 실사 장면 %d · 3번 이상 %d종\n' % (len(rows), sum(r.get('used', 0) for r in rows), sum(r.get('used', 0) >= 3 for r in rows)))
if not os.path.exists(p): print('shot_plan.md 없음:', p); sys.exit(0 if os.path.exists(bu) else 1)
print('## shot_plan.md 장면 계획')
L = open(p, encoding='utf-8').read().split('\n')
sec = None; hdr = None; use = collections.defaultdict(list)
for i, l in enumerate(L, 1):
    if l.startswith('# '): sec = l[2:].strip(); hdr = None; continue
    if not (sec and sec.startswith('장면 계획') and l.startswith('|')): continue
    cells = [c.strip() for c in l.strip('|').split('|')]
    if hdr is None: hdr = cells; continue
    if set(''.join(cells)) <= set('-: '): continue
    f = cells[hdr.index('파일')] if '파일' in hdr and hdr.index('파일') < len(cells) else l
    for cid in re.findall(r'stock/([A-Za-z0-9_\-]+)\.(?:mp4|mov|jpg|png|webm)', f):
        use[cid].append('%d행 %s' % (i, cells[0][:12]))
if not use: print('실사 클립 0'); sys.exit(0)
bad = 0
print('| 클립 ID | 이 편 사용 횟수 | 쓰인 줄 | 판정 |'); print('|---|---|---|---|')
for cid, rows in sorted(use.items(), key=lambda x: -len(x[1])):
    n = len(rows); v = '1번' if n == 1 else ('2번 — 둘째 컷에 그 줄 대상 글자 얹기 확인' if n == 2 else '**3번 이상 — 다른 클립·판으로**')
    bad += n >= 3
    print('| %s | %d | %s | %s |' % (cid, n, ' · '.join(rows), v))
print('\n클립 %d종 · 실사 칸 %d · 3번 이상 %d종' % (len(use), sum(map(len, use.values())), bad))
