# H-1 롱폼을 잘라 세로 쇼츠 props를 만든다 (firemap-video-producer 2026-10-14, r1clips.py를 본뜸 · 틀 = video/src/C1S.tsx 그대로).
#   py -3.12 work/research/cardshorts/h1clips.py h1s_gap      # → work/video/h1s_gap.json
# 목소리 = ep/H-1 voice.json wav 그대로(Chirp 3 HD Charon, 새 녹음 없음). 줄 번호 = video/h1.json 장면 순서대로 센 전체 순번(0부터).
# 화면 숫자 = video/h1.json gap1·gap2·person 데이터(편집 통과한 롱폼 화면 글자) 그대로. 숫자를 새로 계산하지 않는다.
# 컷 = longform/ep/H-1/shorts_cuts.md 'D. 손품 씨 계산서'(N1~N3 새 줄이 필요 없는 컷). 끝 줄은 카페 줄(97) 대신 '어디로 가라는 말은 아니에요'
#      — H-1 카페 짝 글 주소가 아직 없어서. 설명란 첫 줄에 롱폼 링크.
import os, json, sys
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from w1g1clips import load, mk, at, scene, build, VID

SHORTS = {}

HL, HS = load('h1')
L = mk(HL)
g1 = HS['gap1']['data']; g2 = HS['gap2']['data']; ps = HS['person']['data']
src = HS['gap1']['source']
assert L(9)[0]['text'].startswith('지금은 고덕동 래미안힐스테이트고덕') and L(75)[0]['text'].startswith('지금 보증금으로') and L(87)[0]['text'].startswith('어디로 가라는')
R1 = {r[0]: r for r in g1['rows']}; R2 = {r[0]: r for r in g2['rows']}
a = L(9, 10)
b = L(75, 76, 77, 78)
c = L(79)
d = L(81, 82, 83, 84)
e = L(85, 86)   # 10/14 꼴 관문 ⓑ: 끝 면책 줄 87('어디로 가라는 말은 아니에요') 뺌 — 끝 = '오래된 축에 드는 단지예요'
SHORTS['h1s_gap'] = dict(
  question=['전세 9억 5천,', '84㎡로 옮기면 얼마 더?'], hot='얼마 더',
  base='가상 인물 계산 · 국토교통부 실거래 1년(2025.11~2026.10)',
  answer=dict(label='보증금 9.50억 · 84㎡대 1년 가운데 값과 차이', items=['사려면 +5.70억~+19.00억', '전세면 −4.20억~+4.50억'], arrow=False,
              note='세금·중개보수·대출 넣지 않은 단순 차액'),
  scenes=[
   scene('vs', '지금 사는 곳', HS['person']['source'], a, full=True,   # full = 판을 90프레임 당겨 0초부터 첫 칸이 다 보이게(둘째 칸 시각은 +90)
         tiles=[['지금 사는 곳 (가상 인물)', '고덕동 전세', ps['home'][1], 0, 'ink'],   # 02시 눈 검사: '래미안힐스테이트고덕' 큰 글자 잘림 → 동네, 단지는 아래 줄
                [ps['deposit'][0], g1['deposit'][1], ps['deposit'][2], 0, 'accent']]),   # 0초 빈 칸 → 처음부터
   scene('receipt', '사려면 더 드는 돈', src, b, head='보증금 9.50억 그대로 · 84㎡대 매매 가운데 값', size=44,
         rows=[['래미안힐스테이트고덕', R1['래미안힐스테이트고덕'][2], 'in', 0],
               ['고덕아남', R1['고덕아남'][2], 'in', at(b, 1)],
               ['고덕그라시움', R1['고덕그라시움'][2], 'in', at(b, 2)],
               ['올림픽파크포레온', R1['올림픽파크포레온'][2], 'tax', at(b, 3)],
               ['헬리오시티', R1['헬리오시티'][2], 'tax', at(b, 3.3)]],
         side=['19억 안팎', at(b, 3.5), '헬리오시티·포레온 · 매매 − 보증금']),
   scene('vs', '이 계산에 넣지 않은 것', src, c,
         tiles=[['넣은 것', '가운데 값 − 보증금', '국토교통부 실거래 1년', 0, 'ink'],
                ['넣지 않은 것', '세금·중개보수·대출', '대출 한도는 사람마다 달라 계산 안 함', at(c, 0.45), 'fall']]),
   scene('receipt', '전세로만 옮기면', src, d, head='보증금 9.50억 · 84㎡대 전세 가운데 값', size=44,
         rows=[['고덕그라시움 (' + R2['고덕그라시움'][1] + ')', R2['고덕그라시움'][2], 'in', 30],   # 02시 눈 검사: 줄 81 동안 빈 판 → 바로
               ['헬리오시티 (' + R2['헬리오시티'][1] + ')', R2['헬리오시티'][2], 'in', at(d, 2)],
               ['올림픽파크포레온 (' + R2['올림픽파크포레온'][1] + ')', R2['올림픽파크포레온'][2], 'tax', at(d, 3)]],
         side=['+4.50억', at(d, 3.2), '포레온 전세로 옮길 때']),
   scene('vs', '반대로 남는 곳', src, e,
         tiles=[['고덕아남 (' + R2['고덕아남'][1] + ')', R2['고덕아남'][2], '보증금이 남음', 0, 'ink'],
                ['고덕아남 입주', '1996.03', '고덕동 지도 단지 중 두 번째로 오래됨', at(e, 1), 'ink']]),
  ],
)
assert R1['헬리오시티'][2] == '+19.00억' and R2['고덕아남'][2] == '−4.20억' and g1['deposit'][1] == '9.50억' and '1996.03' in g2['extra'][0]


if __name__ == '__main__':
    for name, dd in SHORTS.items():
        if name not in sys.argv[1:]: continue
        p = build(name, dd)
        fr = sum(s['frames'] for s in p['scenes'])
        json.dump(p, open(os.path.join(VID, name + '.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        print(f"{name}: {fr} 프레임 = {fr / 30:.1f}초 · 줄 {[l['n'] for s in p['scenes'] for l in s['lines']]}")
