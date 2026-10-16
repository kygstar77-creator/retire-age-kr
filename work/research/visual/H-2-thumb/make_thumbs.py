# H-2 '잠실주공5단지 — 살 땐 가장 비싸고 전세는 가장 쌌다' 썸네일 시안(2026-10-16 visual-designer)
# 문구: ep/H-2/copy/titles.md 1위 짝(copywriter 07:57) = meta.json thumb_text_top / thumb_text / thumb_text_small (assert).
# 숫자: ep/H-2/calc_out.txt §1 잠실 84㎡대(거래 3건 이상) 매매 중앙·순수전세 중앙 — 파일에서 읽어 assert(43.45억·5.20억).
# 그림: 우리 막대(0에서 시작, 칸마다 자기 눈금). 5단지 = 주황(앞줄 이름과 같은 색), 나머지 회색. 사진·VS·노랑·큰 억 숫자 0(경쟁 5장 공통 문법 피함).
# 가려짐: 오른쪽 아래 x>960·y>576, 아래 5%(y>684) 글자 없음 — 렌더 뒤 자동 검사(zones.json).
import os, json, sys, re
from playwright.sync_api import sync_playwright
from PIL import Image
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
EP = os.path.join(ROOT, 'work', 'research', 'longform', 'ep', 'H-2')
meta = json.load(open(os.path.join(EP, 'meta.json'), encoding='utf-8'))
TOP, BIG, SMALL = meta['thumb_text_top'], meta['thumb_text'], meta['thumb_text_small']
assert (TOP, BIG, SMALL) == ('잠실주공5단지, 잠실 안에서', '살 땐 가장 비싸고 / 전세는 가장 쌌다', '국민평형 1년 실거래 · 전세 5억 남짓'), (TOP, BIG, SMALL)
B1, B2 = [s.strip() for s in BIG.split('/')]

# calc_out §1 잠실동 줄 읽기
cal = open(os.path.join(EP, 'calc_out.txt'), encoding='utf-8').read()
jam = cal.split('### 잠실동')[1].split('###')[0]
rows = {}
for m in re.finditer(r'- (\S+)\(건축 (\d+)\) (\d+)건 중앙 ([\d.]+)억 .*?순수전세 (\d+)건 ([\d.]+)억', jam):
    rows[m.group(1)] = (float(m.group(4)), float(m.group(6)))
assert rows['주공아파트5단지'] == (43.45, 5.20), rows['주공아파트5단지']
assert max(rows, key=lambda k: rows[k][0]) == '주공아파트5단지' and min(rows, key=lambda k: rows[k][1]) == '주공아파트5단지'
# 막대: 5단지 + 거래 많은 새 단지 셋(리센츠·잠실엘스·트리지움 — 제목·대본에 나오는 단지)
PICK = ['주공아파트5단지', '리센츠', '잠실엘스', '트리지움']
SALE = [rows[k][0] for k in PICK]; JS = [rows[k][1] for k in PICK]
print('매매', SALE, '전세', JS)

INK, OR, GREY, PAPER = '#16181D', '#FF5A00', '#A3A8B3', '#ECE6DA'
BASE = open(os.path.join(HERE, '..', 'E-2-thumb', 'e2f.html'), encoding='utf-8').read()
HEAD, TAIL = BASE.split('<body>')[0] + '<body>', '<script>' + BASE.split('<script>')[1]
VARIANTS = {}


def bars(vals, x0, ybot, hmax, bw, gap, grey, building=False, win='#FFFFFF', split=0):
    top = max(vals); s = ''
    for i, v in enumerate(vals):
        h = round(hmax * v / top); x = x0 + i * (bw + gap) + (split if i else 0); c = OR if i == 0 else grey
        s += f"<div style='position:absolute;left:{x}px;top:{ybot - h}px;width:{bw}px;height:{h}px;background:{c};border-radius:{4 if building else 8}px {4 if building else 8}px 0 0'></div>"
        if building:  # 창문 격자(2열) — 막대를 아파트 동 모양으로
            for wy in range(ybot - h + 14, ybot - 14, 24):
                for wx in (x + 10, x + bw - 24):
                    s += f"<div style='position:absolute;left:{wx}px;top:{wy}px;width:14px;height:12px;background:{win};opacity:.55'></div>"
    return s


def board(dark=False, building=False):
    bg, ink, grey, base = ('#14171F', '#FFFFFF', '#5B6273', '#3A4050') if dark else (PAPER, INK, GREY, '#8A8F99')
    yb, hm = 562, 172
    bw, gap = (74, 16) if building else (70, 18)
    p1x, p2x = 206, 736
    return f"""<div style='position:absolute;inset:0;background:{bg}'></div>
<div class='t' style='left:46px;top:26px;font-size:64px;color:{ink}'><span style='color:{OR}'>잠실주공5단지</span>, 잠실 안에서</div>
<div id='b1' class='t' data-fit='1190' style='left:44px;top:100px;font-size:136px;color:{ink}'>{B1}</div>
<div id='b2' class='t' data-fit='1190' style='left:44px;top:238px;font-size:136px;color:{ink}'>{B2.replace('가장 쌌다', f"<span style='color:{OR}'>가장 쌌다</span>")}</div>
<div class='t' style='left:48px;top:{yb - 70}px;font-size:62px;color:{ink}'>살 때</div>
<div class='t' style='left:592px;top:{yb - 70}px;font-size:62px;color:{ink}'>전세</div>
{bars(SALE, p1x, yb, hm, bw, gap, grey, building)}{bars(JS, p2x, yb, hm, bw, gap, grey, building)}
<div style='position:absolute;left:{p1x - 8}px;top:{yb}px;width:{4 * bw + 3 * gap + 16}px;height:5px;background:{base}'></div>
<div style='position:absolute;left:{p2x - 8}px;top:{yb}px;width:{4 * bw + 3 * gap + 16}px;height:5px;background:{base}'></div>
<div class='lab' style='left:48px;top:598px;font-size:44px;color:{ink}'>{SMALL}</div>
"""


VARIANTS['h2a'] = board()
VARIANTS['h2b'] = board(dark=True)
VARIANTS['h2c'] = board(building=True)


# ── 2차(10/16) — 1차 h2a 6.67(제미나이 7·7 · Claude 6 · 레드팀 7 겹침 1). 둘 다: 주황 막대에 값이 없어 '무슨 막대인지'·'전세 하락' 오독, '잠실 안에서'가 작아 범위를 놓침.
# h2d: 앞줄 64→78px, 칸 이름 아래에 5단지 값(반올림 '43억'·'5억', 주황 72px). h2e: 같은 판, 값은 calc_out 그대로 '43.45억'·'5.20억'(56px).
def board2(exact=False):
    ink, grey, base = INK, GREY, '#8A8F99'
    yb, hm = 562, 158
    bw, gap = 66, 14
    p1x, p2x = 214, 790
    v1, v2 = (f"{SALE[0]:.2f}억", f"{JS[0]:.2f}억") if exact else (f"{round(SALE[0])}억", f"{round(JS[0])}억")
    vs = 56 if exact else 76
    return f"""<div style='position:absolute;inset:0;background:{PAPER}'></div>
<div class='t' style='left:44px;top:22px;font-size:78px;color:{ink}'><span style='color:{OR}'>잠실주공5단지</span>, 잠실 안에서</div>
<div id='b1' class='t' data-fit='1190' style='left:44px;top:114px;font-size:132px;color:{ink}'>{B1}</div>
<div id='b2' class='t' data-fit='1190' style='left:44px;top:250px;font-size:132px;color:{ink}'>{B2.replace('가장 쌌다', f"<span style='color:{OR}'>가장 쌌다</span>")}</div>
<div class='t' style='left:0;width:198px;text-align:right;top:418px;font-size:58px;color:{ink}'>살 때</div>
<div class='t' style='left:0;width:200px;text-align:right;top:{562 - vs}px;font-size:{vs}px;color:{OR}'>{v1}</div>
<div class='t' style='left:500px;width:274px;text-align:right;top:418px;font-size:58px;color:{ink}'>전세</div>
<div class='t' style='left:500px;width:276px;text-align:right;top:{562 - vs}px;font-size:{vs}px;color:{OR}'>{v2}</div>
{bars(SALE, p1x, yb, hm, bw, gap, grey)}{bars(JS, p2x, yb, hm, bw, gap, grey)}
<div style='position:absolute;left:{p1x - 8}px;top:{yb}px;width:{4 * bw + 3 * gap + 16}px;height:5px;background:{base}'></div>
<div style='position:absolute;left:{p2x - 8}px;top:{yb}px;width:{4 * bw + 3 * gap + 16}px;height:5px;background:{base}'></div>
<div class='lab' style='left:48px;top:598px;font-size:44px;color:{ink}'>{SMALL}</div>
"""


VARIANTS['h2d'] = board2()
VARIANTS['h2e'] = board2(exact=True)


# ── 3차(10/16) — 2차 h2d 6.67(제미나이 3.5-lite 7·7 · Claude 5 · 레드팀 8 겹침 2). Claude: 앞줄 BH의 '5'가 's'로 보여 '잠실주공s단지', 값 글씨가 조연(작음), 베이지 판이 목록에서 가라앉음.
# h2f: 앞줄을 PD 700(숫자 5가 또렷한 글꼴)으로, 값 '43억'·'5억'을 108px 주인공으로(칸 이름 위 56px), 막대는 값 오른쪽. h2g: 같은 판, 아래 자료 칸만 다크 카드 1장(화면당 1개 규칙).
def board3(card=False):
    ink = INK
    yb, hm = 560, 150
    bw, gap = 58, 12
    p1x, p2x = 336, 846
    cbg, cink, grey, base = ('#16181D', '#FFFFFF', '#5B6273', '#3A4050') if card else (PAPER, INK, GREY, '#8A8F99')
    cardh = f"<div style='position:absolute;left:24px;top:388px;width:1232px;height:188px;background:{cbg};border-radius:20px'></div>" if card else ''
    return f"""<div style='position:absolute;inset:0;background:{PAPER}'></div>
<div class='lab' style='left:46px;top:20px;font-size:76px;color:{ink};letter-spacing:-1px'><span style='color:{OR}'>잠실주공5단지</span>, 잠실 안에서</div>
<div id='b1' class='t' data-fit='1190' style='left:44px;top:116px;font-size:128px;color:{ink}'>{B1}</div>
<div id='b2' class='t' data-fit='1190' style='left:44px;top:248px;font-size:128px;color:{ink}'>{B2.replace('가장 쌌다', f"<span style='color:{OR}'>가장 쌌다</span>")}</div>
{cardh}
<div class='lab' style='left:56px;top:398px;font-size:54px;color:{cink}'>살 때</div>
<div class='t' style='left:52px;top:458px;font-size:108px;color:{OR}'>{round(SALE[0])}억</div>
<div class='lab' style='left:648px;top:398px;font-size:54px;color:{cink}'>전세</div>
<div class='t' style='left:644px;top:458px;font-size:108px;color:{OR}'>{round(JS[0])}억</div>
{bars(SALE, p1x, yb, hm, bw, gap, grey)}{bars(JS, p2x, yb, hm, bw, gap, grey)}
<div style='position:absolute;left:{p1x - 8}px;top:{yb}px;width:{4 * bw + 3 * gap + 16}px;height:5px;background:{base}'></div>
<div style='position:absolute;left:{p2x - 8}px;top:{yb}px;width:{4 * bw + 3 * gap + 16}px;height:5px;background:{base}'></div>
<div class='lab' style='left:48px;top:604px;font-size:44px;color:{ink}'>{SMALL}</div>
"""


VARIANTS['h2f'] = board3()
VARIANTS['h2g'] = board3(card=True)


# ── 4차(10/16) — 3차 h2f 6.58(제미나이 3.5-lite 7·6.5 · Claude 6 · 레드팀 7 겹침 2), h2g 6.25(레드팀 겹침 3 반려 — 어두운 띠+주황 숫자 = 경쟁 2 문법).
#   Claude 3회 연속: 가장 큰 글자가 문장이라 '자료 슬라이드' — 값이 주인공이어야. 레드팀: 이름 없는 회색 막대는 왼→오 '떨어졌다/뛰었다'(시간 흐름) 오독.
# h2h(형식 바꿈): 막대 없앰. 큰 두 줄 각각 오른쪽에 그 줄의 답 값(43억·5억, 170px 주황) — 문장↔값 두 줄 표. 작은 줄 52px로 올림.
# h2i: h2f 판 유지 + 막대 아래 칸 이름('5단지'·'새 단지 3곳', 38px) — 레드팀 처방 그대로.
def board4():
    ink = INK
    return f"""<div style='position:absolute;inset:0;background:{PAPER}'></div>
<div class='lab' style='left:46px;top:22px;font-size:76px;color:{ink};letter-spacing:-1px'><span style='color:{OR}'>잠실주공5단지</span>, 잠실 안에서</div>
<div style='position:absolute;left:44px;top:132px;width:1192px;height:6px;background:{ink}'></div>
<div id='b1' class='t' data-fit='690' style='left:44px;top:186px;font-size:100px;color:{ink}'>{B1}</div>
<div id='v1' class='t' style='left:0;width:1236px;text-align:right;top:152px;font-size:170px;color:{OR}'>{round(SALE[0])}억</div>
<div style='position:absolute;left:44px;top:330px;width:1192px;height:4px;background:#C9C1B2'></div>
<div id='b2' class='t' data-fit='690' style='left:44px;top:384px;font-size:100px;color:{ink}'>{B2}</div>
<div id='v2' class='t' style='left:0;width:1236px;text-align:right;top:350px;font-size:170px;color:{OR}'>{round(JS[0])}억</div>
<div style='position:absolute;left:44px;top:528px;width:1192px;height:6px;background:{ink}'></div>
<div class='lab' style='left:46px;top:560px;font-size:46px;color:{ink}'>{SMALL}</div>
"""


def board5():
    ink = INK; yb, hm = 522, 132; bw, gap = 58, 12; p1x, p2x = 336, 846; grey, base = GREY, '#8A8F99'
    lab = lambda x, w, t, c: f"<div class='lab' style='left:{x}px;width:{w}px;text-align:center;top:{yb + 8}px;font-size:36px;color:{c}'>{t}</div>"
    return f"""<div style='position:absolute;inset:0;background:{PAPER}'></div>
<div class='lab' style='left:46px;top:18px;font-size:74px;color:{ink};letter-spacing:-1px'><span style='color:{OR}'>잠실주공5단지</span>, 잠실 안에서</div>
<div id='b1' class='t' data-fit='1190' style='left:44px;top:108px;font-size:120px;color:{ink}'>{B1}</div>
<div id='b2' class='t' data-fit='1190' style='left:44px;top:234px;font-size:120px;color:{ink}'>{B2.replace('가장 쌌다', f"<span style='color:{OR}'>가장 쌌다</span>")}</div>
<div class='lab' style='left:56px;top:372px;font-size:52px;color:{ink}'>살 때</div>
<div class='t' style='left:52px;top:426px;font-size:104px;color:{OR}'>{round(SALE[0])}억</div>
<div class='lab' style='left:648px;top:372px;font-size:52px;color:{ink}'>전세</div>
<div class='t' style='left:644px;top:426px;font-size:104px;color:{OR}'>{round(JS[0])}억</div>
{bars(SALE, p1x, yb, hm, bw, gap, grey)}{bars(JS, p2x, yb, hm, bw, gap, grey)}
<div style='position:absolute;left:{p1x - 8}px;top:{yb}px;width:{4 * bw + 3 * gap + 16}px;height:4px;background:{base}'></div>
<div style='position:absolute;left:{p2x - 8}px;top:{yb}px;width:{4 * bw + 3 * gap + 16}px;height:4px;background:{base}'></div>
{lab(p1x - 20, bw + 40, '5단지', OR)}{lab(p1x + bw + gap - 10, 3 * bw + 2 * gap + 20, '새 단지 3곳', ink)}
{lab(p2x - 20, bw + 40, '5단지', OR)}{lab(p2x + bw + gap - 10, 3 * bw + 2 * gap + 20, '새 단지 3곳', ink)}
<div class='lab' style='left:48px;top:614px;font-size:44px;color:{ink}'>{SMALL}</div>
"""


VARIANTS['h2h'] = board4()
VARIANTS['h2i'] = board5()


# ── 5차(10/16) — 4차 h2i 6.67(제미나이 8·8 · Claude 5 · 레드팀 7 겹침 2), h2h 5.5(레드팀 겹침 3 반려: 억 두 개 맞대기 = 경쟁 '33억 VS 41억'), h2f 6.0.
#   Claude: 값이 경쟁 숫자보다 작음·칸 이름 168px에서 깨짐·앞줄 작음. 레드팀: 칸 이름으로 시간 흐름 오독은 풀림.
# h2j: h2i 짜임 그대로, 앞줄 84px·값 130px·칸 이름 44px(큰 두 줄 112px로 자리 냄). h2k: h2j에서 값을 주황 알약(흰 글씨) 안에.
def board6(pill=False):
    ink = INK; yb, hm = 520, 150; bw, gap = 58, 12; p1x, p2x = 326, 920; SP = 40; grey, base = GREY, '#8A8F99'
    lab = lambda x, w, t, c: f"<div class='lab' style='left:{x}px;width:{w}px;text-align:center;top:{yb + 6}px;font-size:42px;color:{c}'>{t}</div>"
    def val(x, v):
        if pill:
            return (f"<div style='position:absolute;left:{x - 10}px;top:404px;width:{276 if len(v) > 2 else 200}px;height:118px;background:{OR};border-radius:20px'></div>"
                    f"<div class='t' style='left:{x}px;top:410px;font-size:110px;color:#fff'>{v}</div>")
        return f"<div class='t' style='left:{x}px;top:394px;font-size:130px;color:{OR}'>{v}</div>"
    return f"""<div style='position:absolute;inset:0;background:{PAPER}'></div>
<div class='lab' style='left:44px;top:12px;font-size:84px;color:{ink};letter-spacing:-1px'><span style='color:{OR}'>잠실주공5단지</span>, 잠실 안에서</div>
<div id='b1' class='t' data-fit='1190' style='left:44px;top:112px;font-size:112px;color:{ink}'>{B1}</div>
<div id='b2' class='t' data-fit='1190' style='left:44px;top:228px;font-size:112px;color:{ink}'>{B2.replace('가장 쌌다', f"<span style='color:{OR}'>가장 쌌다</span>")}</div>
<div class='lab' style='left:54px;top:346px;font-size:50px;color:{ink}'>살 때</div>
{val(48, f"{round(SALE[0])}억")}
<div class='lab' style='left:706px;top:346px;font-size:50px;color:{ink}'>전세</div>
{val(700, f"{round(JS[0])}억")}
{bars(SALE, p1x, yb, hm, bw, gap, grey, split=SP)}{bars(JS, p2x, yb, hm, bw, gap, grey, split=SP)}
<div style='position:absolute;left:{p1x - 8}px;top:{yb}px;width:{4 * bw + 3 * gap + 16 + SP}px;height:4px;background:{base}'></div>
<div style='position:absolute;left:{p2x - 8}px;top:{yb}px;width:{4 * bw + 3 * gap + 16 + SP}px;height:4px;background:{base}'></div>
{lab(p1x - 30, bw + 60, '5단지', OR)}{lab(p1x + bw + gap + SP - 30, 3 * bw + 2 * gap + 60, '새 단지 3곳', ink)}
{lab(p2x - 30, bw + 60, '5단지', OR)}{lab(p2x + bw + gap + SP - 30, 3 * bw + 2 * gap + 60, '새 단지 3곳', ink)}
<div class='lab' style='left:48px;top:614px;font-size:44px;color:{ink}'>{SMALL}</div>
"""


VARIANTS['h2j'] = board6()
VARIANTS['h2k'] = board6(pill=True)


# ── 6차(10/16) — 5차 h2j 6.33(제미나이 3.5-lite 6·6 · Claude 6 · 레드팀 7 겹침 2), h2k 6.33(레드팀 겹침 3 반려: 색 상자 흰 숫자 = 경쟁 띠·뱃지), h2i 5.67(제미나이 4차 8·8 → 5차 5·5 흔들림).
#   Claude: 글 덩어리 4개(앞줄·큰 줄·값+막대·작은 줄)라 밀도 높음, 작은 줄은 168px에서 안 읽힘 → 최소로. 레드팀: 값·막대 20% 키우기, '5단지' 칸 이름 또렷이.
# h2l: h2j 짜임, 큰 줄 116px·값 140px·막대 높이 170·작은 줄 34px 회색(빼지 않고 최소로)·'새 단지 3곳'은 회색으로 약하게.
# h2m: h2l에서 막대를 5단지·리센츠 둘로(제목에 나오는 견줌 상대), 막대 굵게(96px) — 칸 이름 '5단지'·'리센츠'.
def board7(two=False):
    ink = INK; yb, hm = 516, 166; grey, base, mute = GREY, '#8A8F99', '#7C818C'
    if two:
        bw, gap, SP = 96, 22, 0; S, J = SALE[:2], JS[:2]; p1x, p2x = 372, 930
    else:
        bw, gap, SP = 58, 12, 40; S, J = SALE, JS; p1x, p2x = 362, 924
    n = len(S); W = n * bw + (n - 1) * gap + SP
    lab = lambda x, w, t, c, fs: f"<div class='lab' style='left:{x}px;width:{w}px;text-align:center;top:{yb + 2}px;font-size:{fs}px;color:{c}'>{t}</div>"
    if two:
        labs = lambda px: lab(px - 20, bw + 40, '5단지', OR, 44) + lab(px + bw + gap - 20, bw + 40, '리센츠', ink, 44)
    else:
        labs = lambda px: lab(px - 30, bw + 60, '5단지', OR, 44) + lab(px + bw + gap + SP - 30, 3 * bw + 2 * gap + 60, '새 단지 3곳', mute, 40)
    return f"""<div style='position:absolute;inset:0;background:{PAPER}'></div>
<div class='lab' style='left:44px;top:12px;font-size:84px;color:{ink};letter-spacing:-1px'><span style='color:{OR}'>잠실주공5단지</span>, 잠실 안에서</div>
<div id='b1' class='t' data-fit='1190' style='left:44px;top:108px;font-size:116px;color:{ink}'>{B1}</div>
<div id='b2' class='t' data-fit='1190' style='left:44px;top:228px;font-size:116px;color:{ink}'>{B2.replace('가장 쌌다', f"<span style='color:{OR}'>가장 쌌다</span>")}</div>
<div class='lab' style='left:54px;top:352px;font-size:48px;color:{ink}'>살 때</div>
<div class='t' style='left:46px;top:392px;font-size:136px;color:{OR}'>{round(SALE[0])}억</div>
<div class='lab' style='left:716px;top:352px;font-size:48px;color:{ink}'>전세</div>
<div class='t' style='left:710px;top:392px;font-size:136px;color:{OR}'>{round(JS[0])}억</div>
{bars(S, p1x, yb, hm, bw, gap, grey, split=SP)}{bars(J, p2x, yb, hm, bw, gap, grey, split=SP)}
<div style='position:absolute;left:{p1x - 8}px;top:{yb}px;width:{W + 16}px;height:4px;background:{base}'></div>
<div style='position:absolute;left:{p2x - 8}px;top:{yb}px;width:{W + 16}px;height:4px;background:{base}'></div>
{labs(p1x)}{labs(p2x)}
<div class='lab' style='left:48px;top:628px;font-size:34px;color:{mute}'>{SMALL}</div>
"""


VARIANTS['h2l'] = board7()
VARIANTS['h2m'] = board7(two=True)


# ── 7차(10/16) — 6차 h2l 6.0(제미나이 6·6 · Claude 5 · 레드팀 7 겹침 2), h2m 6.0(레드팀 겹침 3 반려: 두 단지 맞대기 = VS, 막대 둘은 '가장'을 못 받침).
#   Claude·레드팀 둘 다: '살 때'·'전세'가 168px에서 사라져 '43억 → 5억 폭락'으로 읽힘(가장 큰 위험). Claude: 회색이 진해 '하나만 튐'이 약함.
# h2n: 칸 이름 '살 때'·'전세'를 BH 76px 굵게(값 높이 절반 이상) 값 바로 위에, 값 120px, 큰 줄 104px로 자리 냄, 회색 옅게(#C9CCD3).
# h2o: h2n에서 칸 이름을 값과 한 줄로('살 때 43억' / '전세 5억') — 이름과 값이 한 덩어리.
def board8(inline=False):
    ink = INK; yb, hm = 516, 170; grey, base, mute = '#C9CCD3', '#9AA0AA', '#7C818C'
    bw, gap, SP = 58, 12, 40; p1x, p2x = (370, 930)
    W = 4 * bw + 3 * gap + SP
    lab = lambda x, w, t, c, fs: f"<div class='lab' style='left:{x}px;width:{w}px;text-align:center;top:{yb + 2}px;font-size:{fs}px;color:{c}'>{t}</div>"
    labs = lambda px: lab(px - 30, bw + 60, '5단지', OR, 44) + lab(px + bw + gap + SP - 30, 3 * bw + 2 * gap + 60, '새 단지 3곳', mute, 40)
    if inline:
        vals = (f"<div class='t' style='left:46px;top:300px;font-size:76px;color:{ink}'>살 때</div>"
                f"<div class='t' style='left:46px;top:394px;font-size:124px;color:{OR}'>{round(SALE[0])}억</div>"
                f"<div class='t' style='left:700px;top:300px;font-size:76px;color:{ink}'>전세</div>"
                f"<div class='t' style='left:700px;top:394px;font-size:124px;color:{OR}'>{round(JS[0])}억</div>")
    else:
        vals = (f"<div class='t' style='left:48px;top:318px;font-size:76px;color:{ink}'>살 때</div>"
                f"<div class='t' style='left:46px;top:400px;font-size:120px;color:{OR}'>{round(SALE[0])}억</div>"
                f"<div class='t' style='left:710px;top:318px;font-size:76px;color:{ink}'>전세</div>"
                f"<div class='t' style='left:708px;top:400px;font-size:120px;color:{OR}'>{round(JS[0])}억</div>")
    return f"""<div style='position:absolute;inset:0;background:{PAPER}'></div>
<div class='lab' style='left:44px;top:10px;font-size:78px;color:{ink};letter-spacing:-1px'><span style='color:{OR}'>잠실주공5단지</span>, 잠실 안에서</div>
<div id='b1' class='t' data-fit='1190' style='left:44px;top:100px;font-size:104px;color:{ink}'>{B1}</div>
<div id='b2' class='t' data-fit='1190' style='left:44px;top:208px;font-size:104px;color:{ink}'>{B2.replace('가장 쌌다', f"<span style='color:{OR}'>가장 쌌다</span>")}</div>
{vals}
{bars(SALE, p1x, yb, hm, bw, gap, grey, split=SP)}{bars(JS, p2x, yb, hm, bw, gap, grey, split=SP)}
<div style='position:absolute;left:{p1x - 8}px;top:{yb}px;width:{W + 16}px;height:4px;background:{base}'></div>
<div style='position:absolute;left:{p2x - 8}px;top:{yb}px;width:{W + 16}px;height:4px;background:{base}'></div>
{labs(p1x)}{labs(p2x)}
<div class='lab' style='left:48px;top:628px;font-size:34px;color:{mute}'>{SMALL}</div>
"""


VARIANTS['h2n'] = board8()


# ── 8차(10/16) — 7차 h2n 6.67(제미나이 8·8 · Claude 5 · 레드팀 7 겹침 2: '폭락' 오독 대부분 풀림). Claude 7회 연속 4~6: 값을 더 크게·회색 중간 진하기·바탕 대비.
# h2p: h2n 짜임, 값 138px·회색 중간(#B3B8C1). h2q: h2p 어두운 판(1차 h2b 레드팀 겹침 2로 반려 아님) — Claude 처방 그대로 한 번 재 본다.
def board9(dark=False):
    yb, hm = 516, 170
    ink, bg, grey, base, mute = ('#FFFFFF', '#14171F', '#5E6575', '#4A5060', '#9AA0AA') if dark else (INK, PAPER, '#B3B8C1', '#9AA0AA', '#7C818C')
    bw, gap, SP = 58, 12, 40; p1x, p2x = (380, 950)
    W = 4 * bw + 3 * gap + SP
    lab = lambda x, w, t, c, fs: f"<div class='lab' style='left:{x}px;width:{w}px;text-align:center;top:{yb + 2}px;font-size:{fs}px;color:{c}'>{t}</div>"
    labs = lambda px: lab(px - 30, bw + 60, '5단지', OR, 44) + lab(px + bw + gap + SP - 30, 3 * bw + 2 * gap + 60, '새 단지 3곳', mute, 40)
    vals = (f"<div class='t' style='left:48px;top:318px;font-size:76px;color:{ink}'>살 때</div>"
            f"<div class='t' style='left:46px;top:390px;font-size:138px;color:{OR}'>{round(SALE[0])}억</div>"
            f"<div class='t' style='left:710px;top:318px;font-size:76px;color:{ink}'>전세</div>"
            f"<div class='t' style='left:708px;top:390px;font-size:138px;color:{OR}'>{round(JS[0])}억</div>")
    return f"""<div style='position:absolute;inset:0;background:{bg}'></div>
<div class='lab' style='left:44px;top:10px;font-size:78px;color:{ink};letter-spacing:-1px'><span style='color:{OR}'>잠실주공5단지</span>, 잠실 안에서</div>
<div id='b1' class='t' data-fit='1190' style='left:44px;top:100px;font-size:104px;color:{ink}'>{B1}</div>
<div id='b2' class='t' data-fit='1190' style='left:44px;top:208px;font-size:104px;color:{ink}'>{B2.replace('가장 쌌다', f"<span style='color:{OR}'>가장 쌌다</span>")}</div>
{vals}
{bars(SALE, p1x, yb, hm, bw, gap, grey, split=SP)}{bars(JS, p2x, yb, hm, bw, gap, grey, split=SP)}
<div style='position:absolute;left:{p1x - 8}px;top:{yb}px;width:{W + 16}px;height:4px;background:{base}'></div>
<div style='position:absolute;left:{p2x - 8}px;top:{yb}px;width:{W + 16}px;height:4px;background:{base}'></div>
{labs(p1x)}{labs(p2x)}
<div class='lab' style='left:48px;top:628px;font-size:34px;color:{mute}'>{SMALL}</div>
"""




VARIANTS['h2p'] = board9()
VARIANTS['h2q'] = board9(dark=True)


# ── 9차(10/16) — 8차 h2p 6.67(제미나이 7.5·6.5 · Claude 6 · 레드팀 7 겹침 2), h2q 5.92(레드팀 겹침 3 반려: 어두운 판 = 경쟁 야경 사진판), h2n 6.08.
#   둘 다: 주황 43억 → 주황 5억이 왼→오로 이어져 '폭락' 연결. 레드팀: 5억 색을 먹색으로 분리. Claude: 두 칸을 확실히 나누기(세로 선), 칸 이름 키우기.
# h2r: h2p + 전세 값 '5억'만 먹색(주황은 5단지 막대·앞줄 이름만) + 두 칸 사이 세로 선 + 칸 이름 86px.
def board10():
    yb, hm = 516, 170
    ink, bg, grey, base, mute = (INK, PAPER, '#B3B8C1', '#9AA0AA', '#7C818C')
    bw, gap, SP = 58, 12, 40; p1x, p2x = (380, 950)
    W = 4 * bw + 3 * gap + SP
    lab = lambda x, w, t, c, fs: f"<div class='lab' style='left:{x}px;width:{w}px;text-align:center;top:{yb + 2}px;font-size:{fs}px;color:{c}'>{t}</div>"
    labs = lambda px: lab(px - 30, bw + 60, '5단지', OR, 44) + lab(px + bw + gap + SP - 30, 3 * bw + 2 * gap + 60, '새 단지 3곳', mute, 40)
    vals = (f"<div class='t' style='left:48px;top:306px;font-size:86px;color:{ink}'>살 때</div>"
            f"<div class='t' style='left:46px;top:390px;font-size:138px;color:{OR}'>{round(SALE[0])}억</div>"
            f"<div class='t' style='left:710px;top:306px;font-size:86px;color:{ink}'>전세</div>"
            f"<div class='t' style='left:708px;top:390px;font-size:138px;color:{ink}'>{round(JS[0])}억</div>")
    return f"""<div style='position:absolute;inset:0;background:{bg}'></div>
<div class='lab' style='left:44px;top:10px;font-size:78px;color:{ink};letter-spacing:-1px'><span style='color:{OR}'>잠실주공5단지</span>, 잠실 안에서</div>
<div id='b1' class='t' data-fit='1190' style='left:44px;top:100px;font-size:104px;color:{ink}'>{B1}</div>
<div id='b2' class='t' data-fit='1190' style='left:44px;top:208px;font-size:104px;color:{ink}'>{B2.replace('가장 쌌다', f"<span style='color:{OR}'>가장 쌌다</span>")}</div>
{vals}
{bars(SALE, p1x, yb, hm, bw, gap, grey, split=SP)}{bars(JS, p2x, yb, hm, bw, gap, grey, split=SP)}
<div style='position:absolute;left:{p1x - 8}px;top:{yb}px;width:{W + 16}px;height:4px;background:{base}'></div>
<div style='position:absolute;left:{p2x - 8}px;top:{yb}px;width:{W + 16}px;height:4px;background:{base}'></div>
{labs(p1x)}{labs(p2x)}
<div style='position:absolute;left:690px;top:322px;width:5px;height:250px;background:{base}'></div>
<div class='lab' style='left:48px;top:628px;font-size:34px;color:{mute}'>{SMALL}</div>
"""




VARIANTS['h2r'] = board10()


# ── 10차(10/16) — 9차 h2r 6.67(제미나이 8·6 · Claude 6 · 레드팀 7 겹침 2: 폭락 연결 대부분 풀림), h2p 6.67, h2n 6.0.
#   레드팀: 세로 선이 왼쪽 바닥선·회색 막대에 붙어 '칸 나눔'이 아니라 '그래프 테두리'로 보임. h2s: 왼쪽 막대 24px 왼쪽으로, 선은 두 칸 가운데(676).
def board11():
    yb, hm = 516, 170
    ink, bg, grey, base, mute = (INK, PAPER, '#B3B8C1', '#9AA0AA', '#7C818C')
    bw, gap, SP = 58, 12, 40; p1x, p2x = (356, 950)
    W = 4 * bw + 3 * gap + SP
    lab = lambda x, w, t, c, fs: f"<div class='lab' style='left:{x}px;width:{w}px;text-align:center;top:{yb + 2}px;font-size:{fs}px;color:{c}'>{t}</div>"
    labs = lambda px: lab(px - 30, bw + 60, '5단지', OR, 44) + lab(px + bw + gap + SP - 30, 3 * bw + 2 * gap + 60, '새 단지 3곳', mute, 40)
    vals = (f"<div class='t' style='left:48px;top:306px;font-size:86px;color:{ink}'>살 때</div>"
            f"<div class='t' style='left:46px;top:390px;font-size:138px;color:{OR}'>{round(SALE[0])}억</div>"
            f"<div class='t' style='left:710px;top:306px;font-size:86px;color:{ink}'>전세</div>"
            f"<div class='t' style='left:708px;top:390px;font-size:138px;color:{ink}'>{round(JS[0])}억</div>")
    return f"""<div style='position:absolute;inset:0;background:{bg}'></div>
<div class='lab' style='left:44px;top:10px;font-size:78px;color:{ink};letter-spacing:-1px'><span style='color:{OR}'>잠실주공5단지</span>, 잠실 안에서</div>
<div id='b1' class='t' data-fit='1190' style='left:44px;top:100px;font-size:104px;color:{ink}'>{B1}</div>
<div id='b2' class='t' data-fit='1190' style='left:44px;top:208px;font-size:104px;color:{ink}'>{B2.replace('가장 쌌다', f"<span style='color:{OR}'>가장 쌌다</span>")}</div>
{vals}
{bars(SALE, p1x, yb, hm, bw, gap, grey, split=SP)}{bars(JS, p2x, yb, hm, bw, gap, grey, split=SP)}
<div style='position:absolute;left:{p1x - 8}px;top:{yb}px;width:{W + 16}px;height:4px;background:{base}'></div>
<div style='position:absolute;left:{p2x - 8}px;top:{yb}px;width:{W + 16}px;height:4px;background:{base}'></div>
{labs(p1x)}{labs(p2x)}
<div style='position:absolute;left:676px;top:322px;width:5px;height:250px;background:{base}'></div>
<div class='lab' style='left:48px;top:628px;font-size:34px;color:{mute}'>{SMALL}</div>
"""




VARIANTS['h2s'] = board11()


# ── 11차(10/16) — 10차 h2s 6.92(제미나이 3.1-lite 7.5·3.5-lite 8 · Claude 6 · 레드팀 7 겹침 2). Claude 10차: 값(138px)이 큰 줄(104px)과 같은 무게 — '큰 두 줄이 가장 큰 글'을 지키게 큰 줄 1.15배·값 줄임.
# h2t: h2s 짜임, 큰 줄 120px · 칸 이름 64px · 값 118px · 막대 150.
def board12():
    yb, hm = 516, 150
    ink, bg, grey, base, mute = (INK, PAPER, '#B3B8C1', '#9AA0AA', '#7C818C')
    bw, gap, SP = 58, 12, 40; p1x, p2x = (356, 950)
    W = 4 * bw + 3 * gap + SP
    lab = lambda x, w, t, c, fs: f"<div class='lab' style='left:{x}px;width:{w}px;text-align:center;top:{yb + 2}px;font-size:{fs}px;color:{c}'>{t}</div>"
    labs = lambda px: lab(px - 30, bw + 60, '5단지', OR, 44) + lab(px + bw + gap + SP - 30, 3 * bw + 2 * gap + 60, '새 단지 3곳', mute, 40)
    vals = (f"<div class='t' style='left:48px;top:350px;font-size:64px;color:{ink}'>살 때</div>"
            f"<div class='t' style='left:46px;top:412px;font-size:118px;color:{OR}'>{round(SALE[0])}억</div>"
            f"<div class='t' style='left:710px;top:350px;font-size:64px;color:{ink}'>전세</div>"
            f"<div class='t' style='left:708px;top:412px;font-size:118px;color:{ink}'>{round(JS[0])}억</div>")
    return f"""<div style='position:absolute;inset:0;background:{bg}'></div>
<div class='lab' style='left:44px;top:10px;font-size:78px;color:{ink};letter-spacing:-1px'><span style='color:{OR}'>잠실주공5단지</span>, 잠실 안에서</div>
<div id='b1' class='t' data-fit='1190' style='left:44px;top:94px;font-size:120px;color:{ink}'>{B1}</div>
<div id='b2' class='t' data-fit='1190' style='left:44px;top:218px;font-size:120px;color:{ink}'>{B2.replace('가장 쌌다', f"<span style='color:{OR}'>가장 쌌다</span>")}</div>
{vals}
{bars(SALE, p1x, yb, hm, bw, gap, grey, split=SP)}{bars(JS, p2x, yb, hm, bw, gap, grey, split=SP)}
<div style='position:absolute;left:{p1x - 8}px;top:{yb}px;width:{W + 16}px;height:4px;background:{base}'></div>
<div style='position:absolute;left:{p2x - 8}px;top:{yb}px;width:{W + 16}px;height:4px;background:{base}'></div>
{labs(p1x)}{labs(p2x)}
<div style='position:absolute;left:676px;top:356px;width:5px;height:216px;background:{base}'></div>
<div class='lab' style='left:48px;top:628px;font-size:34px;color:{mute}'>{SMALL}</div>
"""


VARIANTS['h2t'] = board12()


def check_zones(page):
    return page.evaluate("""()=>{const bad=[];document.querySelectorAll('body *').forEach(e=>{
      if(e.tagName==='SCRIPT'||!e.textContent.trim())return;
      if(e.children.length&&[...e.children].some(c=>c.textContent.trim()&&c.tagName!=='SPAN'&&c.tagName!=='BR'))return;
      const r=document.createRange();r.selectNodeContents(e);const b=r.getBoundingClientRect();
      if((b.right>960&&b.bottom>576)||b.bottom>684||b.right>1280||b.left<0)bad.push(e.textContent.trim().slice(0,20)+' '+Math.round(b.left)+'-'+Math.round(b.right)+','+Math.round(b.bottom));});
      return bad}""")


def main(keys):
    zp = os.path.join(HERE, 'zones.json')
    report = json.load(open(zp, encoding='utf-8')) if os.path.exists(zp) else {}
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1280, 'height': 720})
        for k in keys:
            html = os.path.join(HERE, f'{k}.html')
            open(html, 'w', encoding='utf-8').write(HEAD + VARIANTS[k] + '\n' + TAIL)
            pg.goto('file:///' + html.replace(chr(92), '/')); pg.wait_for_selector('body[data-ready]')
            out = os.path.join(EP, f'thumb_{k}.png'); pg.screenshot(path=out)
            report[k] = check_zones(pg)
            sizes = pg.evaluate("()=>[...document.querySelectorAll('[data-fit]')].map(e=>e.id+':'+getComputedStyle(e).fontSize)")
            im = Image.open(out)
            im.resize((320, 180), Image.LANCZOS).save(os.path.join(HERE, f'{k}_320.png'))
            im.resize((168, 94), Image.LANCZOS).save(os.path.join(HERE, f'{k}_168.png'))
            print(k, os.path.getsize(out) // 1024, 'KB', sizes, '가려짐 위반:', report[k] or '없음')
        b.close()
    json.dump(report, open(zp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)


if __name__ == '__main__':
    main(sys.argv[1].split(',') if len(sys.argv) > 1 else list(VARIANTS))
