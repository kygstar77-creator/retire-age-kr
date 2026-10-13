# R-1 롱폼을 잘라 세로 쇼츠 props를 만든다 (firemap-video-producer 2026-10-12, w1g1clips.py를 본뜸 · 틀 = video/src/C1S.tsx 그대로).
#   py -3.12 work/research/cardshorts/r1clips.py       # → work/video/r1s_fx.json
# 목소리 = ep/R-1 voice.json wav 그대로(Chirp 3 HD Charon, 10/12 녹음, 새 녹음 없음). 줄 번호 = video/r1.json 장면 순서대로 센 전체 순번(0부터).
# 화면 숫자 = video/r1.json(편집 통과한 롱폼 화면 글자)·ep/R-1/facts.txt 그대로. 숫자를 새로 계산하지 않는다(배치·프레임만 정한다).
import os, json, sys
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from w1g1clips import load, mk, at, scene, build, VID

SHORTS = {}

# ── R-1: 달러로 산 ETF, 환율이 얼마나 깎았나 (줄 20·17·18 → 19·21 → 22·23·24 → 25 → 27·87) ──
RL, RS = load('r1')
L = mk(RL)
fx = RS['fx']['data']; sw = RS['swing']['data']
a = L(20, 17, 18)
b = L(19, 21)
c = L(22, 23, 24)
d = L(25)
e = L(27, 87)
src = RS['fx']['source']
SHORTS['r1s_fx'] = dict(
  question=['달러로 산 ETF,', '환율이 얼마나 깎았나?'], hot='환율',
  base='한국은행 매매기준율 · 1억 · 지나간 값',
  answer=dict(label='미국 ETF 1억 · 2025-10-02 → 2026-10-02', items=['환율만 −330만원'], arrow=False,
              note='1년 중엔 두 달 남짓 사이 −1,528만원 구간'),
  scenes=[
   scene('vs', '작년 그날 vs 올해 같은 날', src, a, full=True,   # full = 판을 90프레임 당겨 0초부터 첫 칸이 다 보이게(둘째 칸 시각은 +90)
         tiles=[['작년 그날 환율 (2025-10-02)', fx['a'], '원/달러 매매기준율', 0, 'ink'],
                ['올해 같은 날 (2026-10-02)', fx['b'], '원/달러 매매기준율', at(a, 1) + 90, 'fall']]),   # 22시 눈 검사: 빈 칸 7.9초 → 1,406원 말할 때
   scene('receipt', '환율 하나로 빠진 돈', src, b, head='미국 ETF 1억 · 환율만 본 값', size=46,
         rows=[['달러 값', '−3.30%', 'tax', 0], ['원금 1억 기준', fx['loss'], 'net', at(b, 1)]],
         side=['약 330만원', at(b, 1.3), '환율 하나 때문에 빠진 돈']),
   scene('vs', '1년 안에서는', RS['swing']['source'], c,
         tiles=[['1년 중 가장 높았던 날 (7/2)', '1,554.4원', '원/달러 매매기준율', 20, 'rise'],   # 22시 눈 검사: 같은 화면 9.1초·빈 판 3.4초 → 첫 칸 20프레임, 둘째 칸 줄 23 가운데
                ['가장 낮았던 날 (9/10)', '1,337.9원', '원/달러 매매기준율', at(c, 1.5), 'fall']]),
   scene('receipt', 'S&P500 1억, 두 달 남짓', RS['swing']['source'], d, head='S&P500(SPY) 1억 · 원화로 본 값', size=46,
         rows=[['2026-07-02', '123,037,245원', 'in', 0], ['2026-09-10', '107,755,946원', 'tax', 40]],
         side=['−1,528만원', 100, '두 달 남짓 · 달러 값은 올랐는데 환율로']),
   scene('vs', '끝날 하루 vs 그 사이', src, e,   # 22시 눈 검사: 같은 화면 13초 → 장면 나눔(숫자는 앞 장면과 같은 것)
         tiles=[['끝날 하루만 본 값 (1년)', '−330만원', '환율만 · 2025-10-02 → 2026-10-02', 0, 'ink'],
                ['그 사이 가장 컸던 구간', '−1,528만원', 'S&P500 1억 · 7/2 → 9/10', at(e, 0.62), 'fall']]),
  ],
)

# ── R-1: 해외 ETF 판 이익, 세금은 얼마·언제 내나 (줄 37·38 → 39·40 → 41·42·43 → 45·46 → 47) · 10/12 23시 비축 ──
tx = RS['spytax']['data']
srct = RS['spytax']['source']
a = L(37, 38)
b = L(39, 40)
c = L(41, 42, 43)
d = L(45, 46)
e = L(47)
SHORTS['r1s_spytax'] = dict(
  question=['해외 ETF 판 이익,', '세금은 얼마, 언제 내나?'], hot='언제',
  base='소득세법·한미 조세조약 · SPY 1억 계산 · 지나간 값',
  answer=dict(label='SPY 1억 · 1년 들고 판 뒤', items=['판 이익 세금 191만원', '내는 때: 다음 해 5월'], arrow=False,
              note='분배금 15%는 미국에서 먼저 뗌 · 공제 250만원'),
  scenes=[
   scene('vs', '세금은 두 군데서 뗀다', srct, a, full=True,
         tiles=[['분배금에서', '미국 15%', '한미 조세조약 · 국내에서 또 안 뗌', 0, 'ink'],
                ['판 이익에서', '국내 22%', '공제 250만원 넘는 부분만', at(a, 1) + 90, 'accent']]),
   scene('receipt', '분배금에서 빠진 돈', srct, b, head='SPY 1억 · 분배금 세금 · 단위 원', size=46,
         rows=[[tx['rows'][0][0], tx['rows'][0][1], 'tax', 0]],
         side=['16만 4천원', at(b, 1), '분배금에서 미국이 먼저 뗀 돈']),
   scene('receipt', '판 이익 세금 계산', srct, c, head=tx['head'], size=46,
         rows=[[tx['rows'][1][0], tx['rows'][1][1], 'in', 0], [tx['rows'][2][0], tx['rows'][2][1], 'dim', 110],
               [tx['rows'][3][0], tx['rows'][3][1], 'in', at(c, 2)], [tx['rows'][4][0], tx['rows'][4][1], 'tax', at(c, 2.3)]],
         side=['22%', at(c, 2), tx['side'][2]]),
   scene('vs', '세금 내는 때', srct, d,
         tiles=[['팔 때', '바로 안 빠짐', '통장엔 팔고 난 돈 그대로', 10, 'ink'],
                ['판 이익 세금 내는 때', '다음 해 5월', '내가 직접 신고 · 확정신고 5월 1일~31일', at(d, 1), 'accent']]),
   scene('receipt', '통장에 찍힌 돈이 전부는 아니다', srct, e, head='SPY 판 이익 세금 · 다음 해 5월 직접 신고', size=46,
         rows=[['판 이익 세금', '−1,916,240', 'tax', 0]],
         side=['다음 해 5월', 40, '다 써 버리면 신고할 때 당황']),
  ],
)

# ── R-1: 1억 넣은 날만 바꾸면 1등도 바뀌나 · 10/13 22시 비축 ──
# 주의(10/13 22시): 위 r1s_fx·r1s_spytax 줄 번호는 10/12 r1.json 기준이다. 10/13 06시 새 판(G1oI47miUuo)에서 말 줄 16·17이 빠져
# 번호가 밀렸으니, 두 편을 다시 쓰지 말 것(이미 렌더·예약됨). 아래 r1s_startday는 10/13 새 판 r1.json 번호
# (줄 62·63 → 69·70 → 71·72·73 → 75·76 → 77·78). 이름을 주고 돌린다: py -3.12 r1clips.py r1s_startday
rk = RS['rank']['data']; st = RS['start']['data']; ca = RS['caseA']['data']
assert L(62)[0]['text'].startswith('세금 떼기 전에도, 뗀 뒤에도 SCHD') and L(78)[0]['text'].startswith('날짜가 정해진 돈이라면')
a = L(62, 63)
b = L(69, 70)
c = L(71, 72, 73)
d = L(75, 76)
e = L(77, 78)
SHORTS['r1s_startday'] = dict(
  question=['1억 넣은 날만 바꿔도', '1등이 바뀔까?'], hot='1등',
  base='야후 파이낸스 종가·분배금 · 한국은행 ECOS · 지나간 값',
  answer=dict(label='1억 · 넣는 날 251번 · 1년 들고 판 순서', items=['오늘 순서는 10번에 1번', '금이 1등인 날 74.5%'], arrow=False,
              note='달러 기준 · 세금 전 · 지나간 값'),
  scenes=[
   scene('bars', '세금·환율 떼고 1년 뒤', RS['rank']['source'], a, head='1억 · 2025-10-02 → 2026-10-02 · 세금·환율 뗀 뒤', full=True,   # full: 판 +90프레임
         bars=[[x[0], x[1], x[5], [0, at(a, 1) + 90, at(a, 1.3) + 90, at(a, 1.6) + 90][i], x[4], x[2]] for i, x in enumerate(rk['bars'])], max=rk['max']),   # 22시 눈 검사: '1억 1,599만원' 꼬리표가 왼쪽에서 잘림 → 큰 글자는 %, 금액은 아래
   scene('receipt', '넣는 날을 하루씩 옮기면', RS['start']['source'], b, head='넣는 날 251번 · 1년 들고 판 순서 · 달러·세금 전', size=40,   # 22시 눈 검사: 막대 6개 이름이 겹침 → 줄 목록
         rows=[[x[0].replace('>', ' > ').replace('S&P', 'S&P500'), x[2], 'hi' if x[4] == 'accent' else 'in', 20 + i * 14] for i, x in enumerate(st['bars'])],   # 22:4x 눈 검사: 줄 69 동안 빈 판 5초 → 처음부터
         side=['25일', at(b, 1.5), '오늘과 같은 순서 · 251일 중']),
   scene('vs', '251번 가운데', RS['start']['source'], c,
         tiles=[['오늘과 같은 순서', '10번에 1번', '251일 중 25일 (10.0%)', 0, 'ink'],
                ['금이 1등인 날', '74.5%', '251일 중 187일', at(c, 1), 'accent']]),
   scene('vs', '1년 안에 꺼낼 돈이라면', RS['caseA']['source'], d,
         tiles=[['1년 안에 꺼낼 돈', '집 계약금', '30대 · 쓸 날짜가 정해진 돈', 0, 'ink'],
                ['예금이면 1년 뒤', '1억 218만원', '102,182,680원 · 처음부터 정해짐', at(d, 0.8), 'ink']]),
   scene('vs', 'S&P500이었다면', RS['caseA']['source'], e,
         tiles=[['S&P500 · 꺼내는 날에 따라', '폭 2,574만원', '97,294,730원 ~ 123,037,245원', 0, 'fall'],
                ['날짜가 정해진 돈이면', '수익률보다 폭', '꺼내는 날 값이 얼마나 흔들리나', at(e, 0.7), 'accent']]),   # 빈 칸 5.3초 → 3.7초
  ],
)
assert ca['bars'][0][2] == '102,182,680원' and ca['bars'][1][2] == '123,037,245원' and ca['bars'][1][7] == '97,294,730원' and ca['callout'][0] == '폭 2,574만원'
assert st['note'][0] == '오늘 순서: 251일 중 25일(10.0%)' and st['note2'][0] == '금이 1위: 187일(74.5%)' and rk['bars'][3][2] == '1억 218만원'


if __name__ == '__main__':
    for name, dd in SHORTS.items():
        if name not in sys.argv[1:]: continue   # 10/13: 이름을 준 편만 쓴다(옛 번호 두 편을 덮지 않게)
        p = build(name, dd)
        fr = sum(s['frames'] for s in p['scenes'])
        json.dump(p, open(os.path.join(VID, name + '.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        print(f"{name}: {fr} 프레임 = {fr / 30:.1f}초 · 줄 {[l['n'] for s in p['scenes'] for l in s['lines']]}")
