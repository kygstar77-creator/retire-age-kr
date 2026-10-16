# d1s_dep — D-1 롱폼(GMc2Rd1-JYA) '퇴직 후 피부양자 조건(소득 2,000만원·재산 5억 4,000만원)'을 자른 세로 쇼츠 props (firemap-video-producer 2026-10-16 07시)
#   py -3.12 work/research/cardshorts/d1s_dep/d1depclip.py   → work/video/d1s_dep.json (틀 C1S — n1s_top10과 같은 길)
# 이미 쓴 D-1 질문(d1_kunbo 1,000 vs 1,001만원 · d1s_when 고지서 언제 · d1s_pension 연금 있으면 절벽)과 다른 질문: 피부양자로 남는 조건.
# 목소리 = D-1 롱폼 문장 wav 그대로(gemini-3.8-flash-tts Charon, 새 녹음 0).
#   줄 11은 앞의 '가족 중 '(0.31~0.79초)를 무음 틈(0.85초, rms 8)에서 떼고 '직장가입자의…0원이에요.'(33자)를 첫 줄로(꼴 ⓐ 35자 이하).
#   줄 48은 마지막 문장 '조건은 소득과 재산 두 가지입니다.'(6.95초~)만 씀 — 앞 문장은 1,000만원 경계 이야기라 이 클립 질문과 다름.
# 화면 숫자 = video/d1.json check 장면 data(공단 피부양자 소득·재산요건 안내) 그대로(새 계산 0).
# 줄 순서: 11뒤 → 9 → 10 → 12 → 48끝 → 49 → 50 → 51 → 52(끝 줄 면책 아님).
import os, json, sys, wave
import numpy as np
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from w1g1clips import at, scene, build, VID

D1 = json.load(open(os.path.join(VID, 'd1.json'), encoding='utf-8'))
NL = [l for s in D1['scenes'] for l in s['lines']]
SC = {s['kind']: s for s in D1['scenes']}
assert NL[11]['text'] == '가족 중 직장가입자의 피부양자로 들어가면 본인 보험료는 0원이에요.'
assert NL[9]['text'].startswith('회사에 다닐 때는 월급을') and NL[10]['text'] == '퇴직하면 길이 갈립니다.' and NL[12]['text'].startswith('조건이 안 맞으면 지역가입자가')
assert NL[48]['text'].endswith('조건은 소득과 재산 두 가지입니다.') and NL[49]['text'].startswith('먼저 소득. 사업·금융·연금·근로 소득을 다 합쳐서 1년에 2,000만원 이하여야 해요.')
assert NL[50]['text'] == '재산 기준은 두 단계예요. 재산세 과세표준이 5억 4,000만원 이하면 통과입니다.'
assert NL[51]['text'] == '5억 4,000만원을 넘어도 9억원까지는 길이 남아 있는데, 그때는 1년 소득이 1,000만원 이하여야 해요.' and NL[52]['text'] == '하나라도 넘으면 지역가입자로 바뀝니다.'
ck = SC['check']['data']['items']
assert ck[0][1] == '1년 2,000만원 이하' and ck[1][1] == '재산세 과세표준 5억 4,000만원 이하' and ck[1][2] == '또는 9억원 이하 + 1년 소득 1,000만원 이하'


def L(*idx):
    return [{'n': i, 'text': NL[i]['text'], 'cap': NL[i].get('cap'), 'audio': NL[i]['audio'], 'frames': NL[i]['frames']} for i in idx]


def cut(n, t0, name, text):   # 무음 틈에서 앞을 떼고 10ms 페이드인(치직 막기) — 새 녹음 아님
    src = NL[n]; assert src['audio'].startswith('audio/d-1/')
    w = wave.open(os.path.join(VID, 'public', src['audio'])); prm = w.getparams(); sr = w.getframerate()
    x = np.frombuffer(w.readframes(w.getnframes()), np.int16).copy(); w.close(); assert prm.nchannels == 1
    y = x[int(t0 * sr):].astype(np.float32); k = int(0.01 * sr); y[:k] *= np.linspace(0, 1, k)
    o = wave.open(os.path.join(VID, 'public', 'audio', 'd-1', name), 'wb'); o.setparams(prm); o.writeframes(y.astype(np.int16).tobytes()); o.close()
    return {'n': n, 'text': text, 'cap': None, 'audio': f'audio/d-1/{name}', 'frames': round(len(y) / sr * 30) + 8}


S11 = cut(11, 0.85, 'd1d_11b.wav', '직장가입자의 피부양자로 들어가면 본인 보험료는 0원이에요.')
S48 = cut(48, 6.90, 'd1d_48d.wav', '조건은 소득과 재산 두 가지입니다.')
a = [S11] + L(9); b = L(10, 12); c = [S48] + L(49); d = L(50, 51); e = L(52)
SRC_C = SC['check']['source']; SRC_F = SC['fork']['source']

SH = dict(
  question=['퇴직 후 건보료 0원,', '피부양자 조건은?'], hot='0원',
  base='국민건강보험공단 피부양자 소득·재산요건 안내 · 2026년 기준',
  answer=dict(label='본인 보험료 0원(피부양자)이 되는 조건 2가지', items=['1년 소득 2,000만원 이하', '재산 5억 4,000만원 이하'], arrow=False,   # 2차 시험 2명: '조건 · 이하여야 — 소득…' 순서 뒤죽박죽·1년인지 모름
              note='재산이 5억 4,000만원~9억원이면 1년 소득 1,000만원 이하로'),   # 1차 이해 시험 2명: '둘 다 이하'와 장면 4 '9억까지 길' 앞뒤 안 맞아 보임
  scenes=[
   scene('vs', '퇴직하면 건보료는', SRC_F, a, full=True,
         tiles=[['가족 직장가입자 밑 피부양자', '본인 0원', '직장 다니는 가족의 건강보험에 올라감', 0, 'accent'],
                ['회사 다닐 때', '월급 기준', '월급에서 보험료가 나감', 0, 'ink']]),
   scene('vs', '길이 갈린다', SRC_F, b,
         tiles=[['조건이 맞으면 · 피부양자', '0원', '본인 보험료 없음', 0, 'accent'],
                ['조건이 안 맞으면 · 지역가입자', '소득·재산', '이 두 가지로 보험료 계산', at(b, 0.5), 'fall']]),   # 10/16 1차 눈 검사: 둘째 칸 빈 판 2.4초 → 줄 10 가운데
   scene('receipt', '조건 ① 소득', SRC_C, c, head='피부양자 조건 ① 소득', size=40,
         rows=[['조건', '소득·재산 두 가지', 'dim', 0], ['합치는 소득', '사업·금융·연금·근로', 'in', at(c, 1.0)],
               ['1년 합계', '2,000만원 이하', 'net', at(c, 1.3)], ['사업소득', '원칙적으로 없어야', 'dim', at(c, 1.7)]],
         side=['2,000만원', 0, '1년 소득 합계 한도']),   # 1차 렌더 빈 곳 최대 41%(영수증 첫 판 줄 1개) → 답 숫자 0초·줄 일찍
   scene('receipt', '조건 ② 재산', SRC_C, d, head='피부양자 조건 ② 재산 · 재산세 고지서의 과세표준(시세 아님)', size=40,   # 1차 시험 2명: 과세표준을 집값으로 읽음
         rows=[['5억 4,000만원 이하', '통과', 'net', 0], ['5억 4,000만원~9억원', '소득 1,000만원 이하면 통과', 'in', at(d, 1.0)],
               ['9억원 넘음', '지역가입자로', 'dim', at(d, 1.6)]],
         side=['5억 4,000만원', 0, '재산세 과세표준 기준']),
   scene('vs', '하나라도 넘으면', SRC_C, e,
         tiles=[['조건 ① 소득 · ② 재산 다 맞으면', '피부양자 0원', '본인 보험료 없음', 0, 'accent'],
                ['하나라도 넘으면', '지역가입자', '소득·재산으로 보험료 계산', 0, 'fall']]),
  ],
)

if __name__ == '__main__':
    p = build('d1s_dep', SH)
    fr = sum(s['frames'] for s in p['scenes'])
    json.dump(p, open(os.path.join(VID, 'd1s_dep.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f"d1s_dep: {fr} 프레임 = {fr / 30:.1f}초 · 줄 {[l['n'] for s in p['scenes'] for l in s['lines']]} · 장면 {[round(s['frames'] / 30, 1) for s in p['scenes']]}")
