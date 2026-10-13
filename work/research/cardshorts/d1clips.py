# D-1 롱폼을 잘라 세로 쇼츠 props를 만든다 (firemap-video-producer 2026-10-14, h1clips.py를 본뜸 · 틀 = video/src/C1S.tsx 그대로).
#   py -3.12 work/research/cardshorts/d1clips.py d1s_when      # → work/video/d1s_when.json
# 목소리 = video/d1.json의 wav 그대로(D-1 편 목소리, 새 녹음 없음). 줄 번호 = video/d1.json 장면 순서대로 센 전체 순번(0부터).
# d1.json 장면에는 key가 없어서 w1g1clips.load 대신 여기서 줄만 편다. 화면 숫자 = d1.json 데이터·ep/D-1/facts.txt 그대로.
# 질문은 이미 나간 카드 쇼츠 d1_kunbo('1,000만원 vs 1,001만원' 절벽)와 겹치지 않게 '언제 고지서에 붙나'(롱폼 9장 calendar).
import os, json, sys
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from w1g1clips import mk, at, scene, build, VID

SHORTS = {}

P = json.load(open(os.path.join(VID, 'd1.json'), encoding='utf-8'))
DL = [l for s in P['scenes'] for l in (s.get('lines') or [])]
SC = {s['kind']: s for s in P['scenes']}
L = mk(DL)
assert L(21)[0]['text'].startswith('이자와 배당을 합친') and L(46)[0]['text'].startswith('그러니까 올해 2026년에') and L(47)[0]['text'].startswith('그래서 퇴직한 첫해')
st = SC['statute']; cal = SC['calendar']
a = L(21, 22)
b = L(43, 44, 45)
c = L(46)
d = L(47)
SHORTS['d1s_when'] = dict(
  question=['배당·이자로 오른 건보료,', '고지서엔 언제 붙나?'], hot='언제',
  base='국민건강보험법 시행령·시행규칙 · 2026년 기준',
  answer=dict(label='1년 이자+배당 1,000만원 넘은 해 → 지역 건보료', items=['다음 해 11월분부터', '그다음 해 10월분까지'], arrow=False,
              note='연금소득은 다음 해 1월~12월분'),
  scenes=[
   scene('vs', '금융소득 1,000만원의 경계', st['source'], a, full=True,   # full = 판을 90프레임 당겨 0초부터 첫 칸이 다 보이게(둘째 칸 시각은 +90)
         tiles=[['1년 이자+배당 1,000만원 이하', '합산 안 함', '시행규칙 제44조① 단서', 0, 'ink'],
                ['1,000만원 초과', '전액 합산', '넘은 부분만이 아니라', at(a, 1) + 90, 'fall']]),
   scene('vs', '고지서에는 언제 반영되나', cal['source'], b,
         tiles=[['이자·배당·사업·근로 소득', '11월분부터', '전년도 소득 · 다음 해 10월분까지', 20, 'accent'],
                ['연금소득', '1월분부터', '전년도 연금 · 12월분까지', at(b, 1.55), 'ink']]),   # 02시 눈 검사: 첫 칸만 11초 → 줄 44 뒷부분에
   scene('receipt', '2026년에 1,001만원 받았다면', cal['source'], c, head='2026년 배당·이자 1,001만원 · 지역가입자', size=46,
         rows=[['받은 해', '2026년', 'in', 0], ['고지서 반영 시작', '2027년 11월분', 'tax', at(c, 0.5)], ['반영 끝', '2028년 10월분', 'in', at(c, 0.78)]],   # 02시 눈 검사: 첫 줄만 7.6초 → 당김
         side=['2027년 11월분', at(c, 0.5), '올해 고지서가 아니라']),
   scene('vs', '고지서가 생각과 다르면', cal['source'], d,
         tiles=[['퇴직 첫해 고지서가 생각과 다르면', '몇 년도 소득?', '그것부터 확인', 0, 'accent'],
                ['이자·배당 → 11월분', '연금 → 1월분', '반영 시작 달이 다름', at(d, 0.5), 'ink']]),
  ],
)


if __name__ == '__main__':
    for name, dd in SHORTS.items():
        if name not in sys.argv[1:]: continue
        p = build(name, dd)
        fr = sum(s['frames'] for s in p['scenes'])
        json.dump(p, open(os.path.join(VID, name + '.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        print(f"{name}: {fr} 프레임 = {fr / 30:.1f}초 · 줄 {[l['n'] for s in p['scenes'] for l in s['lines']]}")
