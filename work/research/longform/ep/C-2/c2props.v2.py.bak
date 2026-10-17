# C-2 화면 재료 — script.md + voice.json(줄 길이·소리) + calc_n1_out.txt → work/video/c2.json (Remotion C2가 읽는다)
#   py -3.12 work/research/longform/ep/C-2/c2props.py
# 틀: 그림 장면(정우 씨 SVG 시트 visual/N1-person 6장, 16:9 전체) ↔ 흰 보드(통장 선·해마다 막대·환율·달력 벽·꺼낸 돈별 막대·줄였다면 표)를 말 줄마다 번갈아.
# 장면 = 말 줄 묶음, 그 안에서 줄마다(beat) 그림이 한 칸씩 바뀐다(U5 같은 화면 8초 이하). 줄은 번호가 아니라 말 글자 앞부분으로 찾는다(대본이 바뀌면 assert).
# 숫자: props 안 숫자 글자는 전부 calc_n1_out.txt 또는 script.md(말·[자막])에 있는 글자만 — 맨 아래 numcheck가 기계로 막는다. 차트 점 값은 calc 표에서 파싱.
import json, os, re, sys, shutil
sys.stdout.reconfigure(encoding='utf-8')
EP = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.normpath(os.path.join(EP, '..', '..', '..', '..'))
VID = os.path.join(WORK, 'video')
ART = os.path.join(WORK, 'research', 'visual', 'N1-person')
FPS, TAIL = 30, 75
CALC = open(os.path.join(EP, 'calc_n1_out.txt'), encoding='utf-8').read()
SCRIPT = open(os.path.join(EP, 'script.md'), encoding='utf-8').read()
V = json.load(open(os.path.join(EP, 'voice.json'), encoding='utf-8'))
ALL = [l for s in V['sections'] for l in s['lines']]
USED = set()

def L(t):
    hit = [i for i, l in enumerate(ALL) if l['text'].startswith(t)]; assert len(hit) == 1, (t, hit)
    i = hit[0]; assert i not in USED, ('두 번 씀', t); USED.add(i)
    l = ALL[i]; assert l.get('audio') and os.path.exists(os.path.join(VID, 'public', l['audio'])), t
    return {'text': l['text'], 'audio': l['audio'], 'frames': l['frames'], 'i': i}

# ───────── calc 표 파싱 ─────────
def block(head):
    m = re.search(re.escape(head) + r'.*?\n(.*?)(?=\n## |\Z)', CALC, re.S); assert m, head
    rows = []
    for y, a, r, b in re.findall(r'(\d{4}): ([\d.]+) → ([+-][\d.]+)% → ([\d.]+|못 꺼냄)', m.group(1)):
        rows.append([int(y), float(a), float(r), None if b == '못 꺼냄' else float(b)])
    return rows
JW = block('## 월 200만원 · 1998년 1월 시작')      # 정우
MS = block('## 월 200만원 · 2003년 1월 시작')      # 민수
YH = block('## 월 200만원 · 1997년 1월 시작')      # 영호
assert JW[0][:2] == [1998, 3.0] and JW[-1][0] == 2011 and JW[-1][3] is None and MS[-1] == [2025, 2.66, 15.1, 2.72] and YH[-1][3] == 15.9
RET = {y: r for y, a, r, b in JW}
def pts(rows, upto=9999, start=None):
    out = [[rows[0][0], rows[0][1]]]                       # 1월 시작 점(해 x=해 시작)
    for y, a, r, b in rows:
        if b is not None and y <= upto: out.append([y + 1, b])   # 연말 = 다음 해 시작 점
    return out

PIC = {'s1998': (1079, 0.36), 's2001': (599, 0.38), 's2002': (899, 0.38), 's2009': (860, 0.36), 's2010': (859, 0.38), 's2011': (859, 0.36)}
os.makedirs(os.path.join(VID, 'public', 'c2p'), exist_ok=True)
# 10/14 PD: 흰 보드 장면에 끼우는 그림(CutAway, U5 같은 화면 8초) — visual 17:17 새 그림, 글자 0
CUT = ['s1997', 's1998b', 's2003m', 's2008', 's_two', 's_cal', 's1998c']
for k in list(PIC) + CUT: shutil.copyfile(os.path.join(ART, k + '.png'), os.path.join(VID, 'public', 'c2p', k + '.png'))
def cp(n): return f'c2p/{n}.png'

SRC = 'S&P500 총수익 지수 ^SP500TR 연말 종가 · 한국은행 ECOS 원/달러 연말 환율 · 파이어맵 계산(1월 초 1년 치 매도·양도세 22%·연 250만원 공제·물가 반영 안 함)'
SRC_PIC = '가상 인물 · 지수·환율은 실제 기록, 통장은 계산'

def S(kind, lines, **data):
    ls = [L(t) for t in lines]
    return {'kind': kind, 'lines': ls, 'frames': sum(l['frames'] for l in ls), 'data': data}

def pic(name, lines, year=None, cards=None, zoom=(1.0, 1.08), pan=0, gray=False, quote=None, src=SRC_PIC):
    cx, fy = PIC[name]
    return S('pic', lines, pic=f'c2p/{name}.png', cx=cx, fy=fy, year=year, cards=cards or [], zoom=list(zoom), pan=pan, gray=gray, quote=quote, source=src)

def chart(lines, title, show, beats, src=SRC, band=None, ymax=3.6, **extra):
    # show: 선마다 upto[k] = k번째 줄에서 보일 마지막 x(해) — beats[k] = 그 줄에서 붙는 꼬리표 [x, 값 글자, 색] 목록
    # extra: minus(꺼낸 돈 vs 줄어든 돈 두 칸) · line1(1억 선) · floor(바닥 선 2,400만원) · band2(줄마다 띠)
    return S('chart', lines, title=title, series=show, beats=beats, source=src, band=band, ymax=ymax, **extra)

def board(kind, lines, title, src=SRC, **d):
    return S(kind, lines, title=title, source=src, **d)

J = {'name': '정우 씨', 'color': 'accent', 'pts': pts(JW)}
M = {'name': '민수 씨', 'color': 'fall', 'pts': pts(MS)}
def upto(who, ys): return {**who, 'upto': ys}

scenes = [
    # ── 0. 여는 장면 ──
    pic('s1998', ['외환위기가 한창이던 겨울', '퇴직금 3억을 미국', '"매달 200만원씩만 팔아'], year='1998년 1월',
        cards=[None, ['3억', '퇴직금 · 미국 대형주 지수'], ['월 200만원', '해마다 1월에 1년 치 2,400만원']], zoom=(1.25, 1.0), pan=-30, quote=[None, None, '이 정도면 평생 가겠지']),
    pic('s1998', ['이 통장은 언제 바닥났을까요?'], year='1998년 1월', cards=[['언제 바닥?', '같은 돈 · 같은 규칙']], zoom=(1.35, 1.48)),
    chart(['같은 돈, 같은 규칙으로 5년 늦게'], '5년 늦게 시작한 사람', [upto(M, [2026])], [[[2026, '2.72억원', 'fall']]], band=None),
    pic('s1998', ['둘을 가른 건 고른 상품이'], year='1998년 1월', cards=[['시작한 해', '고른 상품이 아니라']], zoom=(1.0, 1.1), pan=20),
    board('preview', ['끝에서는 언제, 얼마로'], '끝에서 볼 것', items=[['언제', '하락이 시작된 뒤 몇 년째에'], ['얼마로', '월 100만원 · 150만원']]),
    # ── 1. 정우 씨는 누구인가 ──
    board('who', ['정우 씨는 이 영상을 위해', '대신 숫자는 하나도', '미국 S&P500 총수익 지수와', '투자를 권하는 영상이 아니라'], '정우 씨는 누구인가', pic='c2p/s1998.png',
          chips=[['가상 인물', '이 영상을 위해 지어낸 사람'], ['숫자는 실제', 'S&P500 총수익 지수 1988~2025'], ['환율도 실제', '한국은행 ECOS 원/달러 연말 환율'], ['투자 권유 아님', '지난 기록을 다시 본 계산']]),
    board('fx', ['정우 씨보다 딱 1년 먼저', '영호 씨가 들어간 해에', '영호 씨의 달러 자산은', '정우 씨는 달러가 이미', '그래서 첫해 지수가'], '1년 차이, 환율',
          rates=[['1996년 말', '844.2원'], ['1997년 말', '1,415.2원'], ['1998년 말', '1,207.8원']],
          people=[['영호 씨', '1997년 1월 시작', '달러 +33.4%', '원화 +123.6%'], ['정우 씨', '1998년 1월 시작', '달러 +28.6%', '원화 +9.7%']],
          src='한국은행 ECOS 731Y004 원/달러 연말 환율 · S&P500 총수익 지수 ^SP500TR · 파이어맵 계산',
          cutaways=[[1, cp('s1997')], [3, cp('s1998b')]]),
    # ── 2. 처음 두 해 ──
    chart(['처음 두 해는 꺼내 쓰고도', '둘째 해 말엔 3억 2천만원'], '정우 씨 통장 연말 잔액', [upto(J, [1999, 2000])], [[[1999, '3.03억', 'accent']], [[2000, '3.20억', 'accent']]]),
    pic('s1998', ['"꺼내 쓰는데도 늘어나네."'], year='1999년', zoom=(1.4, 1.5), quote=['꺼내 쓰는데도 늘어나네']),
    board('tax', ['팔 때 낸 세금도 없었어요', '팔아서 생긴 차익은 지역'], '팔 때 세금 · 건보료',
          taxes=[['1998년', '양도세 0원'], ['1999년', '양도세 0원']], basic='차익이 연 250만원 공제 안',
          kunbo=[['이자', 1], ['배당', 1], ['사업', 1], ['근로', 1], ['연금', 1], ['기타소득', 1], ['양도소득', 0]],
          src='국민건강보험법 시행령 제41조① (지역가입자 소득 — 양도소득은 목록에 없음) · 소득세법 양도세 22%·연 250만원 기본공제'),
    # ── 3. 3년 연속 하락 ──
    pic('s2001', ['셋째 해부터 지수가 내리'], year='2000~2002년', cards=[['3년 연속 하락', '원화 기준 수익률']], zoom=(1.0, 1.1), pan=24),
    board('bars', ['그동안에도 해가 바뀔 때마다', '떨어진 값에 팔면'], '정우 씨 해마다 수익률(원화)', years=[1998, 1999, 2000, 2001, 2002], show=[5, 5],
          fmt=['+9.7%', '+14.8%', '-0.0%', '-7.2%', '-29.5%'], vals=[RET[y] for y in [1998, 1999, 2000, 2001, 2002]], sell=[None, '떨어진 값에 팔면 같은 2,400만원에 주식이 더 많이 나간다']),
    pic('s2001', ['하락 둘째 해 1월엔'], year='2001년 1월', cards=[['하던 대로', '월 200만원 그대로']], zoom=(1.3, 1.4), pan=-10),
    pic('s2002', ['"올해도 팔아야 하나."'], year='2002년 1월', zoom=(1.1, 1.0), quote=['올해도 팔아야 하나']),
    chart(['하락 셋째 해가 끝났을 때', '다섯 해 동안 꺼내 쓴 돈은'], '정우 씨 통장 연말 잔액', [upto(J, [2003, 2003])],
          [[[2001, '2.95억', 'accent'], [2002, '2.51억', 'accent'], [2003, '1.60억', 'accent']], [[2003, '−1.40억원', 'rise']]],
          band=[2000, 2003, '3년 연속 하락'], minus=['꺼낸 돈 1.2억원', '줄어든 돈 1.40억원'], cutaways=[[0, cp('s2002')]]),
    # ── 4. 회복은 왔는데 ──
    board('bars', ['이듬해 지수가 크게 올랐어요'], '정우 씨 해마다 수익률(원화)', years=[1998, 1999, 2000, 2001, 2002, 2003], show=[6],
          fmt=['+9.7%', '+14.8%', '-0.0%', '-7.2%', '-29.5%', '+28.4%'], vals=[RET[y] for y in range(1998, 2004)], sell=[None]),
    chart(['그런데 정우 씨 통장은 1억 7천만원', '오른 해에 불어날 돈 자체가'], '정우 씨 통장 연말 잔액', [upto(J, [2004, 2004])],
          [[[2004, '1.75억', 'accent']], [[2003, '1.60억', 'accent']]], band=[2003, 2004, '+28.4%']),
    chart(['바로 그해 1월, 다른 동네에서', '민수 씨는 첫해부터'], '같은 3억, 2003년 1월에 시작한 민수 씨', [upto(J, [2004, 2004]), upto(M, [2003, 2004])],
          [[[2003, '3.00억', 'fall']], [[2004, '3.54억', 'fall']]], cutaways=[[0, cp('s2003m')]]),
    board('bars', ['정우 씨에겐 그 뒤 네 해', '그 정도로는 정우 씨가'], '정우 씨 해마다 수익률(원화)', years=[2004, 2005, 2006, 2007], show=[4, 4],
          fmt=['-3.4%', '+1.8%', '+6.3%', '+6.5%'], vals=[RET[y] for y in range(2004, 2008)], sell=[None, '해마다 꺼내는 2,400만원'], cutaways=[[0, cp('s2010'), 0.55, 1.0]]),   # 10/15 22시 PD: 같은 화면 10.0초 → 첫 줄 뒷부분 그림(둘째 줄 2,400만원 칸은 보드로)
    pic('s2002', ['"오르긴 오르는데, 통장은'], year='2004~2007년', zoom=(1.35, 1.45), pan=20, quote=['오르긴 오르는데, 통장은 왜 줄지']),
    chart(['금융위기 직전, 정우 씨 통장은'], '정우 씨 통장 연말 잔액', [upto(J, [2008])], [[[2005, '1.46억', 'accent'], [2006, '1.24억', 'accent'], [2007, '1.06억', 'accent'], [2008, '0.87억', 'accent']]], line1=True),
    # ── 5. 금융위기 ──
    pic('s2001', ['그리고 금융위기가 왔어요.'], year='2008년', cards=[['금융위기', '']], zoom=(1.5, 1.6), pan=160, gray=True),
    board('fx08', ['지수는 달러로 37%', '원화로는 손실이 그 절반도'], '2008년 금융위기', usd='-37.0%', krw='-15.6%', rates=[['2007년 말', '938.2원'], ['2008년 말', '1,257.5원']],
          src='S&P500 총수익 지수 ^SP500TR · 한국은행 ECOS 원/달러 연말 환율 · 파이어맵 계산', cutaways=[[0, cp('s2008')]]),
    chart(['그래도 정우 씨의 연말 잔액은', '같은 해 민수 씨 통장엔'], '2008년 말 두 통장', [upto(J, [2009, 2009]), upto(M, [2004, 2009])],
          [[[2009, '0.53억', 'accent']], [[2009, '2.19억', 'fall']]]),
    pic('s2009', ['이듬해엔 지수가 다시 올랐어요.'], year='2009년', cards=[['+17.4%', '2009년 원화 수익률']], zoom=(1.0, 1.08), pan=-20),
    board('jar', ['그런데 연초에 한 해 치를'], '2009년 정우 씨 통장', steps=[['1월 꺼낸 뒤', '0.29억원'], ['그해 원화', '+17.4%'], ['연말', '0.34억원']], need='다음 해 몫 2,400만원'),
    pic('s2009', ['"이제 와서 오르면 뭐 하나."'], year='2009년', zoom=(1.35, 1.45), quote=['이제 와서 오르면 뭐 하나']),
    # ── 6. 바닥나는 해 ──
    pic('s2010', ['다음 해 연초에도 한 해 치를'], year='2010년', cards=[['또 1년 치', '2,400만원']], zoom=(1.0, 1.1), pan=20),
    board('jar', ['꺼내고 남은 1천만원 남짓이'], '2010년 정우 씨 통장', steps=[['1월 꺼낸 뒤', '0.10억원'], ['그해 원화', '+12.2%'], ['연말', '0.12억원']], need='다음 해 몫 2,400만원'),
    chart(['그해 말 통장에 남은 돈은'], '정우 씨 통장 연말 잔액', [upto(J, [2011])], [[[2009, '0.53억', 'accent'], [2010, '0.34억', 'accent'], [2011, '0.12억', 'accent']]], floor=True),
    pic('s2011', ['그리고 2011년 1월, 정우 씨는'], year='2011년 1월', cards=[['못 꺼냈다', '1,154만원 < 1년 치 2,400만원']], zoom=(1.0, 1.08), pan=-26),
    pic('s2011', ['시작한 지 열네 해째'], year='2011년 1월', cards=[['68살', '시작한 지 14년째']], zoom=(1.4, 1.5)),
    board('sum', ['그사이 정우 씨가 손에 쥔 돈은', '물가 오른 건 치지'], '정우 씨가 손에 쥔 돈', n=13, each='2,400만원', total='3.12억원', put='넣은 돈 3억원'),
    # ── 7. 민수 씨와 영호 씨 ──
    chart(['민수 씨는 지난해 말까지', '정우 씨와 다른 건 하나였어요'], '같은 3억 · 같은 규칙 · 시작한 해만 다름', [upto(J, [2011, 2011]), upto(M, [2026, 2026])],
          [[[2026, '2.72억', 'fall']], [[2011, '바닥 2011년', 'accent']]], band2=[[None], [2000, 2003, '정우 씨: 시작하자마자 3년 하락']], ymax=3.6, cutaways=[[0, cp('s_two')]]),
    board('yh', ['영호 씨는 지난해 말 16억'], '영호 씨 · 1997년 1월 시작', big=[['첫해 말', '6.17억원'], ['2025년 말', '15.90억원']], note='첫해 원화 +123.6% (달러 +33.4%)'),
    # ── 8. 37명 ──
    board('wall', ['지난 37년, 해마다 1월에', '그중 통장이 바닥난 사람은', '여섯 명 중 다섯은', '모두 열한 해에서', '나머지 서른한 명은'], '시작 해 37개 · 3억 · 월 200만원 · 팔아 쓰기',
          years=list(range(1989, 2026)), fail={'1998': '14년차', '1999': '13년차', '2000': '11년차', '2001': '11년차', '2002': '12년차', '2004': '18년차'}, count=['바닥 6', '남음 31'], cutaways=[[2, cp('s_cal')], [3, cp('s2011')]]),
    # ── 9. 얼마씩 ──
    board('amount', ['이번엔 서른일곱 명 모두', '월 100만원이면 바닥난', '월 300만원이면 절반'], '꺼내는 돈별 · 시작 해 37개 중 바닥',
          rows=[['월 100만원', 0], ['월 150만원', 5], ['월 200만원', 6], ['월 300만원', 17]], order=[[2], [0, 2], [0, 1, 2, 3]], cutaways=[[0, cp('s_cal')]]),   # 10/15 22시 PD: 재녹음 뒤 같은 화면 8.5초 → 그림 끼움
    board('race', ['정우 씨가 처음부터 150만원만'], '정우 씨 · 1998년 1월 시작', rows=[['월 200만원', 2011, '2011년 바닥 · 14년차'], ['월 150만원', 2019, '2019년 바닥 · 22년차']]),
    # ── 10. 줄였다면, 언제 ──
    pic('s2001', ['처음부터가 아니라 중간에', '하락 둘째 해 1월, 망설였던'], year='2001년 1월', cards=[None, ['월 100만원으로?', '하락 둘째 해 1월']], zoom=(1.0, 1.12), pan=-20),
    board('cut', ['정우 씨 통장은 지난해 말 6억', '같은 결심을 두 해 늦게', '그때 150만원으로만', '얼마나 줄이느냐만큼'], '중간에 줄였다면 · 1998년 시작 월 200만원',
          rows=[['2001년부터 월 100만원', '2025년 말 5.91억원 남음', 'ok'], ['2003년부터 월 100만원', '2025년 말 3.49억원 남음', 'ok'], ['2003년부터 월 150만원', '2015년 바닥', 'bad']], base='그대로 월 200만원 → 2011년 바닥', cutaways=[[2, cp('s2011')]]),   # 10/15 22시 PD: 같은 화면 11.0초 → 그림 끼움
    # ── 11. 끝 ──
    board('cta', ['내 통장은 몇 살까지'], '내 통장은 몇 살까지?', url='firemap.kr', fields=['내 돈', '매달 쓸 돈'], cutaways=[[0, cp('s1998c'), 0, 0.4]],
          src='이 영상은 투자 권유가 아닙니다 · 가상 인물 · 과거 지수 기록 계산이며 앞으로의 수익을 뜻하지 않습니다'),
]
assert len(USED) == len(ALL), ('안 쓴 줄', [ALL[i]['text'][:20] for i in range(len(ALL)) if i not in USED])
order = [l['i'] for s in scenes for l in s['lines']]; assert order == sorted(order), '줄 순서'
scenes[-1]['frames'] += TAIL

# 바닥나는 해 칸: 4번째 줄('이 통장은 언제') 시작부터 '?' → '그해 말 통장에 남은 돈' 줄 끝에서 '2011년'
t = 0; box_on = box_flip = None
for s in scenes:
    for l in s['lines']:
        if l['text'].startswith('이 통장은 언제'): box_on = t
        if l['text'].startswith('그해 말 통장에 남은'): box_flip = t + l['frames'] - 20
        t += l['frames']
for s in scenes:
    for l in s['lines']: l.pop('i')

# 숫자 대조: props 글자 속 숫자 덩이(쉼표·소수 포함)는 calc·대본에 그대로 있어야 한다
def strings(x):
    if isinstance(x, dict):
        for k, v in x.items():
            if k in ('audio', 'pic', 'color', 'kind'): continue
            yield from strings(v)
    elif isinstance(x, list):
        for v in x: yield from strings(v)
    elif isinstance(x, str): yield x
SRCDOC = CALC + SCRIPT
bad = []
for s in scenes:
    for st in strings({k: v for k, v in s.items() if k != 'lines'}):
        for d in re.findall(r'\d[\d,.]*', st):
            d = d.rstrip('.,')
            if d not in SRCDOC: bad.append((st, d))
assert not bad, bad

p = {'fps': FPS, 'scenes': scenes, 'boxOn': box_on, 'boxFlip': box_flip, 'boxQ': '?', 'boxA': '2011년', 'boxLabel': '바닥나는 해',
     'badge': '가상 인물', 'missing': 0}
json.dump(p, open(os.path.join(VID, 'c2.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
fr = sum(s['frames'] for s in scenes)
print(f'c2.json: {fr} 프레임 = {fr / FPS:.1f}초 · 장면 {len(scenes)} · 줄 {len(ALL)} · 종류 {len(set(s["kind"] for s in scenes))} · 최장 줄 {max(l["frames"] for s in scenes for l in s["lines"]) / FPS:.1f}초 · 숫자 대조 통과')
