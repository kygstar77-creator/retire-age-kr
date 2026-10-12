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


if __name__ == '__main__':
    for name, dd in SHORTS.items():
        p = build(name, dd)
        fr = sum(s['frames'] for s in p['scenes'])
        json.dump(p, open(os.path.join(VID, name + '.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        print(f"{name}: {fr} 프레임 = {fr / 30:.1f}초 · 줄 {[l['n'] for s in p['scenes'] for l in s['lines']]}")
