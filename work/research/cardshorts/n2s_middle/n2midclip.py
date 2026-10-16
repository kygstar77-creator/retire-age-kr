# n2s_middle — N-2 롱폼(kXnAKjC-84Q) '직장인 100명 줄, 딱 한가운데 50등 월급은?'을 자른 세로 쇼츠 props (쇼츠 클립 담당 2026-10-16 22시)
#   py -3.12 work/research/cardshorts/n2s_middle/n2midclip.py   → work/video/n2s_middle.json (틀 C1S, layout c1clip — n1s_top10과 같은 길)
# 틀: log.jsonl 최근 9편 m1clip 5 · c1clip 2 · c2person 2 → m1clip은 6/10이 되어 빼고 c1clip(3/10).
# 목소리 = N-2 롱폼 문장 wav 그대로(voice.json · Chirp 3 HD Charon 1.1, 새 녹음 0). 줄 14 앞의 '그럼 '(0~0.40초)만 쉼(0.40~0.43초)에서 뗐다(꼴 ⓐ: 첫 줄이 접속사로 시작 금지).
# 질문 하나: 100명 줄 딱 한가운데 50등은 얼마? → 세전 290만원쯤(원문 중위 288만원), 뉴스 평균 375만원보다 아래. N-1 클립 n1s_top10(가구 순자산 문턱)과 다른 질문.
# 화면 숫자 = video/n2.json 장면 data·cap과 ep/N-2/facts.txt·calc_out.txt 그대로(새 계산 0). 등수 표(150·250·350·450만원)는 쓰지 않는다(전체 요약 금지).
# 10/16 1차 이해 시험(2명): '세전'·'0원 밑'·'몇 배'가 한 번에 안 와닿음 → 화면 글자를 '세금 떼기 전'·'0원보다 적을 순 없음'·'한가운데의 몇 배'로(말은 녹음 그대로)
# 10/17 2차 이해 시험(2명): '줄 앞쪽'이 많이 받는 쪽인지 모름·'평균 − 한가운데' 빼기식 낯섦 → '많이 받는 사람부터 한 줄로'·'많이 받는 쪽 절반'·'평균이 더 높은 만큼'
# 줄 순서: 14뒤('줄 딱 한가운데, 50등은 얼마를 받을까요?', 첫 줄 24자·숫자) → 0(100명 한 줄) → 15(290만원쯤) → 20·21(평균 375만원, 평균이란) → 22·23·24(왜 위로 끌리나) → 25·26(견주기, 통장 260만원쯤).
import os, json, sys, wave
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from w1g1clips import at, scene, build, VID

N2 = json.load(open(os.path.join(VID, 'n2.json'), encoding='utf-8'))
NL = [l for s in N2['scenes'] for l in s['lines']]
SC = {s['key']: s for s in N2['scenes']}
assert NL[0]['text'].startswith('우리나라 직장인 전체를 100명으로 줄여서') and NL[14]['text'] == '그럼 줄 딱 한가운데, 50등은 얼마를 받을까요?'
assert NL[15]['text'].startswith('세전 290만원쯤입니다.') and NL[20]['text'].endswith('세전 375만원이에요.') and NL[22]['text'].startswith('적게 받는 쪽은')
assert NL[24]['text'].startswith('그래서 줄 한가운데 사람은 평균보다') and NL[26]['text'] == '세전으로 290만원쯤이에요. 통장으로는 260만원쯤입니다.'


def L(*idx):
    return [{'n': i, 'text': NL[i]['text'], 'cap': NL[i].get('cap'), 'audio': NL[i]['audio'], 'frames': NL[i]['frames']} for i in idx]


# 줄 14 앞 '그럼 '을 쉼에서 뗌(새 녹음 아님) — 10ms 페이드 인으로 자른 자리 딸깍 막음
SRC = NL[14]; CUT = 0.42
w = wave.open(os.path.join(VID, 'public', SRC['audio'])); sr = w.getframerate(); prm = w.getparams(); raw = w.readframes(w.getnframes()); w.close()
assert prm.nchannels == 1 and prm.sampwidth == 2
import numpy as np
x = np.frombuffer(raw, np.int16)[int(CUT * sr):].astype(np.float32); fi = int(0.01 * sr); x[:fi] *= np.linspace(0, 1, fi)
o = wave.open(os.path.join(VID, 'public', 'audio', 'n-2', 'n2m_14b.wav'), 'wb'); o.setparams(prm); o.writeframes(x.astype(np.int16).tobytes()); o.close()
T14 = SRC['text'].replace('그럼 ', '', 1)
S14 = {'n': 14, 'text': T14, 'cap': None, 'audio': 'audio/n-2/n2m_14b.wav', 'frames': round(len(x) / sr * 30) + 8}

s4 = SC['s4']['data']; s7 = SC['s7']['data']; s8 = SC['s8']['data']
assert s7['avg'] == 375 and s7['mid'] == 290 and s4['items'][1]['small'] == '세전 기준 · 통장 약 260만원'
assert NL[15]['cap'] == '가운데 288만원 · 통장 2,568,400원' and NL[20]['cap'] == '평균 375만원 · 가운데 288만원 · 차 87만원'
SRC_T = SC['s4']['source']; SRC_A = SC['s7']['source']

a = [S14] + L(0); b = L(15); c = L(20, 21); d = L(22, 23, 24); e = L(25, 26)
b[0]['cap'] = '가운데 288만원'   # 꼴 ⓒ: 원 단위 7자리(통장 2,568,400원) 뺌 — cap은 화면에 안 나옴
SH = dict(
  question=['직장인 100명 한 줄,', '딱 한가운데 50등 월급은?'], hot='50등',
  base='국가데이터처 2024년 임금근로일자리 소득 · 2024년 12월 세전 월급 · 일자리 기준',
  answer=dict(label='50등 월급 · 세금 떼기 전', items=['290만원쯤', '평균 375만원보다 아래'], arrow=False,
              note='통장으로는 260만원쯤'),
  scenes=[
   scene('vs', '100명 한 줄', SRC_A, a, full=True,
         tiles=[['우리나라 직장인 전체를', '100명', '많이 받는 사람부터 한 줄로', 0, 'ink'],
                ['줄 딱 한가운데', '50등', '이 사람 월급은 얼마일까', 0, 'accent']]),
   scene('vs', '50등 월급', SRC_T, b,
         tiles=[['50등 월급 · 세금 떼기 전', '290만원쯤', '통계 원문 중위 288만원', 0, 'accent'],
                ['이보다 많이 받는 사람', '절반', '적게 받는 사람도 절반', at(b, 0.45), 'ink']]),
   scene('bars', '평균과 한가운데', SRC_A, c, head='세전 월급 · 2024년 12월', max=400,
         bars=[['뉴스 속 평균', 375, '375만원', 0, 'ink', '모두 더해 ÷ 사람 수'], ['딱 한가운데 50등', 288, '288만원', at(c, 0.6), 'accent', '말로 290만원쯤']]),
   scene('receipt', '평균이 위로 끌리는 까닭', SRC_A, d, head='평균이 한가운데보다 높은 까닭', size=52,   # 10/17 눈 검사: 44는 판 위아래가 비고 글씨가 작음, 62는 오른쪽 잘림 → 52 + 글자 줄임
         rows=[['가장 적게 받아도', '0원 아래는 없음', 'dim', 0], ['많이 받는 쪽엔', '한가운데의 몇 배도', 'in', at(d, 1.0)],
               ['평균이 더 높은 만큼', '87만원', 'net', at(d, 2.0)]]),
   scene('receipt', '내 자리 견주기', SRC_T, e, head='내 자리는 줄 한가운데와 견주기', size=52,
         rows=[['세금 떼기 전', '290만원쯤', 'in', 0], ['통장에 들어오는 돈', '260만원쯤', 'net', at(e, 1.45)], ['내 월급이 더 많으면', '많이 받는 쪽 절반', 'dim', at(e, 1.75)]]),
  ],
)

if __name__ == '__main__':
    p = build('n2s_middle', SH)
    fr = sum(s['frames'] for s in p['scenes'])
    json.dump(p, open(os.path.join(VID, 'n2s_middle.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f"n2s_middle: {fr} 프레임 = {fr / 30:.1f}초 · 줄 {[l['n'] for s in p['scenes'] for l in s['lines']]} · 14 자름 {S14['frames']}")
