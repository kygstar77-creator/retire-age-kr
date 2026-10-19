# B-screen-1019.md의 ⟨…⟩ 자리를 잰 값으로 채운다. py -3.12 build_doc.py
import os, json, statistics as st, re
HERE = os.path.dirname(os.path.abspath(__file__)); DOC = os.path.join(HERE, '..', 'B-screen-1019.md')
L = lambda f: json.load(open(os.path.join(HERE, f), encoding='utf-8')) if os.path.exists(os.path.join(HERE, f)) else {}
R = L('summary.json'); EYE = L('eye.json'); PA = L('pauses.json'); G1 = L('gatecheck.json'); G2 = L('gatecheck2.json'); CF = L('cutfix.json')
S = json.load(open(os.path.join(HERE, 'sample.json'), encoding='utf-8')); NAME = {v: c for k in ('short', 'long') for c, v in S[k]}
def q(v, p): v = sorted(v); return v[min(len(v) - 1, int(round(p * (len(v) - 1))))]
def med(v): return round(st.median(v), 2) if v else None
def iqr(v): return f'{q(v, .25)}~{q(v, .75)}' if v else '-'
f1 = lambda x: '-' if x is None else (f'{x:.1f}' if isinstance(x, float) else str(x))
comp = lambda kind: [r for r in R if r['kind'] == kind and not r['id'].startswith('OURS')]
ours = lambda kind: [r for r in R if r['kind'] == kind and r['id'].startswith('OURS')]
for r in R:
    e = EYE.get(f"{r['kind']}_{r['id']}") or {}
    r['live'] = e.get('live'); r['card'] = e.get('card'); r['ai'] = e.get('ai_person'); r['note'] = e.get('note', '')
    if r['kind'] == 'short' and r['id'] in CF: r['cf_pm'] = CF[r['id']]['cuts_pm']; r['cf_med'] = CF[r['id']]['scene_med']
    p = PA.get(f"{r['kind']}_{r['id']}") or {}
    r['p_pm'] = p.get('per_min'); r['p_med'] = p.get('med'); r['p_sh'] = p.get('share')
SC, LC = comp('short'), comp('long')
T = {}
T['SN'] = str(len(SC))
capok = [r for r in SC if r.get('cap_cx') and 529 <= r['cap_cx'] <= 544]
T['CN'] = str(len(capok))
G2c = {k: v for k, v in G2.items() if not k.startswith('OURS')}
T['BOXF'] = f"{sum(v['old'] > 0.30 for v in G2c.values())}/{len(G2c)}"
T['WHITEF'] = f"{sum(v.get('white', 0) > 0.30 for v in G2c.values())}/{len(G2c)}"
G1c = {k: v for k, v in G1.items() if not k.startswith('OURS')}
T['BGF'] = f"{sum(v['fail_bg'] for v in G1c.values())}/{len(G1c)}"
T['T288'] = str(sum((r.get('f_top288') or 0) >= 0.5 for r in SC))
lv = [r['live'] for r in SC if r['live'] is not None]
T['SLIVE'] = f1(med(lv)); T['SLIVEQ'] = iqr(lv); T['SCARD'] = str(sum((r['card'] or 0) >= 0.9 for r in SC))
cf = [r['cf_med'] for r in SC if r.get('cf_med') is not None and (r.get('dur') or 0) > 10]; cp = [r['cf_pm'] for r in SC if r.get('cf_pm') is not None and (r.get('dur') or 0) > 10]
T['CFMED'] = f1(med(cf)); T['CFQ'] = iqr(cf); T['CFPM'] = f1(med(cp))
lr = [r['rate'] for r in LC if r.get('rate')]; la = [r['rate_all'] for r in LC if r.get('rate_all')]
T['LR'] = f1(med(lr)); T['LRQ'] = iqr(lr); T['LRA'] = f1(med(la)); T['LRAQ'] = iqr(la)
ll = [r['lufs'] for r in LC if r.get('lufs')]; T['LL'] = f1(med(ll)); T['LLQ'] = iqr(ll)
T['LFLOOR'] = f1(med([r['floor_gap_db'] for r in LC if r.get('floor_gap_db')]))
# 사람 진행자(눈 실사 0.6↑, 쉼 5번↑ 잡힌 편)
HP = [r for r in SC + LC if (r['live'] or 0) >= 0.6 and (PA.get(f"{r['kind']}_{r['id']}") or {}).get('n', 0) >= 5]
T['HPM'] = f1(med([r['p_pm'] for r in HP])); T['HPMED'] = f1(med([r['p_med'] for r in HP])); T['HPSH'] = f"{med([r['p_sh'] for r in HP]) * 100:.1f}%" if HP else '-'
T['HUMANPAUSE'] = f"{len(HP)}편(실사 60%↑·쉼이 5번↑ 잡힌 편) 분당 {T['HPM']}번·중앙 {T['HPMED']}초·전체의 {T['HPSH']}"
F = [r for r in LC if r['live'] is not None and r['live'] < 0.6]
T['FN'] = str(len(F)); T['FNAMES'] = '·'.join(NAME.get(r['id'], r['id']) for r in F)
T['FLIVE'] = ', '.join(f"{NAME.get(r['id'], r['id'])} {int(r['live'] * 100)}%" for r in F)
lc = [r['cuts1_pm'] for r in LC]; T['LCUT'] = f"{f1(med(lc))}(25~75% {iqr(lc)})"; T['FCUT'] = f1(med([r['cuts1_pm'] for r in F]))
T['LCUTLOW'] = ', '.join(f"{NAME.get(r['id'])} {r['cuts1_pm']}" for r in LC if r['cuts1_pm'] < 3) or '없음'
T['LP90'] = f1(med([r['scene1_p90'] for r in LC if r.get('scene1_p90')])); T['FP90'] = f1(med([r['scene1_p90'] for r in F if r.get('scene1_p90')]))
T['LMED'] = f1(med([r['scene1_med'] for r in LC if r.get('scene1_med')]))
T['FBIG'] = f1(med([r['maxh_med'] for r in F if r.get('maxh_med') is not None])) + '%'
T['FBIGLIST'] = ', '.join(f"{NAME.get(r['id'])} {r['maxh_med']}" for r in F)
T['FLINES'] = f1(med([r['lines_med'] for r in F if r.get('lines_med') is not None]))
T['FLINESLIST'] = ', '.join(f"{NAME.get(r['id'])} {r['lines_med']}" for r in F)
ch = [r['cap_h'] for r in LC if r.get('cap_h') and (r.get('cap_frames') or 0) >= 0.7]
T['LCH'] = f1(med(ch)); T['LCHQ'] = iqr(ch); T['LCY'] = f1(med([r['cap_cy'] for r in LC if r.get('cap_cy') and (r.get('cap_frames') or 0) >= 0.7]))
T['LCX'] = f1(med([r['cap_cx'] for r in LC if r.get('cap_cx') and (r.get('cap_frames') or 0) >= 0.7]))
T['LN'] = str(len(LC))
# 표
yn = lambda b: '있음' if b else ('-' if b is None else '없음')
pct = lambda x: '-' if x is None else f'{int(round(x * 100))}%'
rows = ['| 채널 | 길이(초) | 실사(눈) | 자막 가운데 x·y | 자막 상자 높이 | 제목 위끝 y·상자 최대 | 글 오른끝 p95 | 컷/분(움직이는 칸)·장면 중앙 | 음량 LUFS | 빠르기 말만/쉼 포함 | AI 사람 |', '|---|---|---|---|---|---|---|---|---|---|---|']
for r in sorted(SC, key=lambda r: NAME.get(r['id'], '')) + ours('short'):
    rows.append(f"| {NAME.get(r['id'], '우리 ' + r['id'][5:])} | {f1(r['dur'])} | {pct(r['live'])} | {f1(r.get('cap_cx'))}·{f1(r.get('cap_cy'))} | {f1(r.get('cap_h'))} | {f1(r.get('title_y0'))}·{f1(r.get('title_hmax'))} | {f1(r.get('x1_p95'))} | {f1(r.get('cf_pm'))}·{f1(r.get('cf_med'))} | {f1(r.get('lufs'))} | {f1(r.get('rate'))}/{f1(r.get('rate_all'))} | {yn(r['ai'])} |")
def sm(k, rs=SC):
    v = [r[k] for r in rs if isinstance(r.get(k), (int, float))]
    return f"{f1(med(v))} ({iqr(v)})"
rows.append(f"| **경쟁 중앙 (25~75%)** | {sm('dur')} | {sm('live')} | {sm('cap_cx')}·{sm('cap_cy')} | {sm('cap_h')} | {sm('title_y0')}·{sm('title_hmax')} | {sm('x1_p95')} | {sm('cf_pm')}·{sm('cf_med')} | {sm('lufs')} | {sm('rate')}/{sm('rate_all')} | {sum(bool(r['ai']) for r in SC)}편 |")
T['쇼츠표'] = '\n'.join(rows) + '\n\n- 자막 x·y·높이는 1080×1920 기준 px. 정지 카드형(스마트건강정보·인생알림장·노후머니가이드)은 자막이 없어 목록 글이 잡혔다.\n- 우리 쇼츠 3편은 10/17~18 옛 틀(x 468·흰 판)이다. 자막 값 d1s·n1s는 흰 판 속 글이 잡혔다.'
rows = ['| 채널 | 실사(눈) | 컷/분 | 컷 사이 중앙·90%·최장(초) | 판 큰 글자 중앙(%) | 판 글자 줄 중앙 | 자막 상자 높이·가운데 y | 음량 LUFS | 빠르기 말만/쉼 포함 | AI 사람 |', '|---|---|---|---|---|---|---|---|---|---|']
for r in sorted(LC, key=lambda r: (r['live'] if r['live'] is not None else 9)) + ours('long'):
    rows.append(f"| {NAME.get(r['id'], '우리 C-2')} | {pct(r['live'])} | {f1(r['cuts1_pm'])} | {f1(r.get('scene1_med'))}·{f1(r.get('scene1_p90'))}·{f1(r.get('scene_max'))} | {f1(r.get('maxh_med'))} | {f1(r.get('lines_med'))} | {f1(r.get('cap_h'))}·{f1(r.get('cap_cy'))} | {f1(r.get('lufs'))} | {f1(r.get('rate'))}/{f1(r.get('rate_all'))} | {yn(r['ai'])} |")
rows.append(f"| **경쟁 중앙 (25~75%)** | {sm('live', LC)} | {sm('cuts1_pm', LC)} | {sm('scene1_med', LC)} | {sm('maxh_med', LC)} | {sm('lines_med', LC)} | {sm('cap_h', LC)} | {sm('lufs', LC)} | {sm('rate', LC)}/{sm('rate_all', LC)} | {sum(bool(r['ai']) for r in LC)}편 |")
T['롱폼표'] = '\n'.join(rows) + '\n\n- 1920×1080 기준. 판 큰 글자·줄은 bgcheck와 같은 잣대(426×240→852×480, 아래 20% 자막 띠 뺌). 진행자 위주 편은 판이 적어 큰 글자·줄 값의 뜻이 약하다.'
rows = ['| 영상 | 실사(눈) | 0.25초↑ 쉼 분당 | 쉼 중앙(초) | 쉼 90%(초) | 쉼 비율 |', '|---|---|---|---|---|---|']
for k, p in sorted(PA.items(), key=lambda kv: -(kv[1].get('share') or 0)):
    if p.get('n', 0) < 5: continue
    kind, vid = k.split('_', 1)
    rr = next((r for r in R if r['kind'] == kind and r['id'] == vid), {})
    rows.append(f"| {('쇼츠 ' if kind == 'short' else '롱폼 ') + NAME.get(vid, '우리 ' + vid[5:])} | {pct(rr.get('live'))} | {p['per_min']} | {p['med']} | {p['p90']} | {p['share'] * 100:.1f}% |")
T['쉼표'] = '\n'.join(rows) + f"\n\n- 쉼이 5번 미만 잡힌 편(음악이 깔렸거나 아주 짧은 편)은 뺐다. 사람 진행자(실사 60%↑) {T['HUMANPAUSE']}."
rows = ['| 쇼츠 | ① 배경 실사 프레임·연속 없음(초) | ② 자막(옛 x 250~690 / 새 330~750) | ⑥ UI 상자 1개↑ 프레임(지금 / 흰 판만) |', '|---|---|---|---|']
for k in sorted(set(G1) | set(G2), key=lambda k: (k.startswith('OURS'), NAME.get(k, k))):
    a = G1.get(k, {}); b = G2.get(k, {})
    rows.append(f"| {NAME.get(k, '우리 ' + k[5:])} | {pct(a.get('bg_frac'))}·{a.get('bg_run', '-')}{' ❌' if a.get('fail_bg') else ''} | {pct(a.get('cap_old'))} / {pct(a.get('cap_540'))} | {pct(b.get('old'))}{' ❌' if (b.get('old') or 0) > .3 else ''} / {pct(b.get('white'))}{' ❌' if (b.get('white') or 0) > .3 else ''} |")
T['관문표'] = '\n'.join(rows) + f"\n\n- ❌ = 우리 관문 기준(① 90%·3초, ⑥ 30%)이면 걸림. ⑥은 지금 {T['BOXF']}편, 흰 판만 세면 {T['WHITEF']}편이 걸린다. ① 배경은 {T['BGF']}편이 걸린다.\n- ② 자막은 우리 자막 자리(y 1100~1240·상자 56px↑)를 재는 검사라 경쟁은 대부분 걸린다(경쟁 자막은 y 1174~1398에 퍼짐). 경쟁 기준이 아니라 우리 틀 확인용이다."
doc = open(os.path.join(HERE, '_template.md'), encoding='utf-8').read()   # 틀에서 매번 새로 채운다
for part, f in (('판정', '_panjeong.md'), ('안전', '_safe.md'), ('한계', '_limit.md'), ('공식', '_official.md')):
    if f: doc = doc.replace(f'⟨{part}⟩', open(os.path.join(HERE, f), encoding='utf-8').read().strip())
doc = doc.replace('⟨롱폼판정⟩', open(os.path.join(HERE, '_long.md'), encoding='utf-8').read().strip())
for k, v in T.items(): doc = doc.replace(f'⟨{k}⟩', str(v))
open(DOC, 'w', encoding='utf-8').write(doc)
left = sorted(set(re.findall(r'⟨([^⟩]+)⟩', doc)))
print('남은 자리:', left)
