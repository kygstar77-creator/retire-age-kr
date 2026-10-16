# n1s_rank — N-1 롱폼(420buEFKB8k) '순자산 1억·5억은 어디쯤, 평균은 가운데가 아니다'를 자른 세로 쇼츠 props (firemap-video-producer 2026-10-17 07시)
#   py -3.12 work/research/cardshorts/n1s_rank/n1rankclip.py   → work/video/n1s_rank.json (틀 C1S — n1s_top10과 같은 길)
# n1s_top10(줄 28·33·35·36·37, 상위 10% 문턱·1년 변화)과 다른 줄·다른 질문: 내 순자산 자리(1억·5억)와 평균 vs 중간, 위 20% 몫.
# 연봉 줄(N-2·n2s_middle과 겹침)은 쓰지 않는다.
# 목소리 = N-1 롱폼 문장 wav 그대로(gemini-3.8-flash-tts Charon, 새 녹음 0). 문장 사이 쉼(rms<150, 0.2초 이상)에서만 자른다.
#   줄 27: '핀 세 개만 꽂아 볼게요.'(~1.22초)를 쉼(1.22~1.78)에서 떼고, 쉼(5.00~5.58)에서 둘로 나눔.
#   줄 24: '이제 두 번째 줄입니다. 이번엔 사람이 아니라 가구, 그리고 연봉이 아니라 순자산이에요.'(~4.68초)를 쉼(4.68~5.24)에서 뗌.
#   줄 25: 첫 문장 '이 조사는 …경계선을 직접 알려 줘요.'만(쉼 3.86~4.22 앞) — 둘째 문장은 연봉 비교라 뺌. 42.2초 → 45초 넘기려고 넣음(경계선 근거 한 줄).
#   줄 29: '연봉과 똑같은 이유로, '(5.68~6.84초)는 이 클립에 연봉이 없어 헷갈리므로 쉼(5.18~5.68)·쉼(6.84~7.02, 쉼표)에서 떼어 냄 — 29a·29b 둘로.
#   줄 43: 마지막 문장 '다만 순자산 줄은…'만(쉼 17.34~17.90 뒤 — 15.3초에서 자른 1차는 받아쓰기에 앞 문장 '두 줄에서 자리가…'가 들려 고침) — 앞은 연봉 이야기라 뺌.
# 화면 숫자 = video/n1.json ruler·meanmed·share 장면 data 그대로(새 계산 0).
import os, json, sys, wave
import numpy as np
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from w1g1clips import at, scene, build, VID

N1 = json.load(open(os.path.join(VID, 'n1.json'), encoding='utf-8'))
NL = [l for s in N1['scenes'] for l in s['lines']]
SC = {s['kind']: s for s in N1['scenes']}
T27A = '순자산 1억원이면 아래에서 20%와 30% 사이예요.'; T27B = '5억원이면 위에서 20%와 30% 사이고요.'
assert NL[27]['text'] == '핀 세 개만 꽂아 볼게요. ' + T27A + ' ' + T27B
T24C = '집·예금·주식을 모두 더하고 빚을 뺀 값입니다. 기준은 2025년 3월 말이에요.'
assert NL[24]['text'].endswith(' ' + T24C)
assert NL[26]['text'] == '가운데 가구, 중앙값은 2억 3,860만원입니다.'
assert NL[29]['text'].startswith('평균 순자산은 4억 7,144만원이에요.') and NL[29]['text'].endswith('평균 가구는 위에서 20%와 30% 사이에 있습니다.')
assert NL[30]['text'] == '위쪽 20% 가구가 전체 순자산의 64.56%를 갖고 있습니다. 1년 전보다 1.48%포인트 늘었어요.'
T43E = '다만 순자산 줄은 모든 나이의 가구가 섞인 줄이라, 젊을수록 아래쪽에 있는 게 자연스럽습니다.'
assert NL[43]['text'].endswith(' ' + T43E)

ru = SC['ruler']['data']; mm = SC['meanmed']['data']; sh = SC['share']['data']; ps = dict(ru['ps'])
pin = dict(ru['pins'])
assert 20 < pin['1억원'] < 30 and 70 < pin['5억원'] < 80   # 1억 = 아래 20~30%, 5억 = 위 20~30%(아래에서 70~80%)
assert ps[50] == 23860 and mm['med'] == 23860 and mm['mean'] == 47144 and 70 < mm['pin'] < 80
assert sh['q'][-1] == 64.56 and sh['prev5'] == 63.08 and round(sh['q'][-1] - sh['prev5'], 2) == 1.48


def L(*idx):
    return [{'n': i, 'text': NL[i]['text'], 'cap': NL[i].get('cap'), 'audio': NL[i]['audio'], 'frames': NL[i]['frames']} for i in idx]


def piece(n, t0, t1, name, text):   # 쉼에서 자르고 앞뒤 10ms 페이드(치직 막기) — 새 녹음 아님
    src = NL[n]; assert src['audio'].startswith('audio/n-1/')
    w = wave.open(os.path.join(VID, 'public', src['audio'])); prm = w.getparams(); sr = w.getframerate()
    x = np.frombuffer(w.readframes(w.getnframes()), np.int16).copy(); w.close(); assert prm.nchannels == 1
    y = x[int(t0 * sr):(int(t1 * sr) if t1 else len(x))].astype(np.float32); k = int(0.01 * sr)
    y[:k] *= np.linspace(0, 1, k); y[-k:] *= np.linspace(1, 0, k)
    o = wave.open(os.path.join(VID, 'public', 'audio', 'n-1', name), 'wb'); o.setparams(prm); o.writeframes(y.astype(np.int16).tobytes()); o.close()
    return {'n': n, 'text': text, 'cap': None, 'audio': f'audio/n-1/{name}', 'frames': round(len(y) / sr * 30) + 8}


S27A = piece(27, 1.60, 5.30, 'n1r_27a.wav', T27A)
S27B = piece(27, 5.30, None, 'n1r_27b.wav', T27B)
S24C = piece(24, 5.10, None, 'n1r_24c.wav', T24C)
T29A = '평균 순자산은 4억 7,144만원이에요. 중앙값의 두 배 가까이 됩니다.'; T29B = '맨 위가 평균을 끌어올려요. 평균 가구는 위에서 20%와 30% 사이에 있습니다.'
assert NL[29]['text'] == T29A + ' 연봉과 똑같은 이유로, ' + T29B
S29A = piece(29, 0.0, 5.40, 'n1r_29a.wav', T29A)
S29B = piece(29, 6.93, None, 'n1r_29b.wav', T29B)
T25A = "이 조사는 '여기부터 위 10%' 같은 경계선을 직접 알려 줘요."
assert NL[25]['text'].startswith(T25A + ' ')
S25A = piece(25, 0.0, 4.00, 'n1r_25a.wav', T25A)
S43E = piece(43, 17.60, None, 'n1r_43e.wav', T43E)
# 1차 이해 시험 2명 모두 줄 25 '경계선을 직접 알려 줘요'를 못 알아들음 → 뺌(42.2초, 45초 아래 — 빈 말보다 짧은 쪽)
a = [S27A, S27B, S24C]; b = L(26) + [S29A, S29B]; c = L(30); e = [S43E]
SRC_R = SC['ruler']['source']; SRC_M = SC['meanmed']['source']; SRC_S = SC['share']['source']

SH = dict(
  question=['순자산 1억·5억,', '상위 몇 %일까?'], hot='5억',   # 1차 시험 2명: 질문은 5억인데 첫 자막은 1억 → 둘 다 질문에
  base='2025년 가계금융복지조사 · 2025년 3월 말 가구 순자산',
  answer=dict(label='가구 순자산 줄에서 내 자리', items=['5억원 = 상위 20~30%', '1억원 = 하위 20~30%'], arrow=False,
              note='딱 중간 가구는 2억 3,860만원'),
  scenes=[
   scene('vs', '1억원·5억원은 어디쯤', SRC_R, a, full=True,
         tiles=[['순자산 1억원', '하위 20~30%', '아래에서 20%와 30% 사이', 0, 'ink'],
                ['순자산 5억원', '상위 20~30%', '순자산 = 집·예금·주식 − 빚 · 2025년 3월 말', 0, 'accent']]),
   scene('vs', '딱 중간 vs 평균', SRC_M, b,
         tiles=[['딱 중간 가구(중앙값)', '2억 3,860만원', '줄 한가운데 가구', 0, 'ink'],
                ['평균 순자산', '4억 7,144만원', '중간의 두 배 가까이 · 평균 가구는 상위 20~30%', at(b, 1), 'accent']]),
   scene('receipt', '위 20% 가구의 몫', SRC_S, c, head='전체 가구 순자산 중 상위 20% 가구 몫', size=46,
         rows=[['1년 전', '63.08%', 'dim', 0], ['2025년 3월 말', '64.56%', 'net', at(c, 0.1)], ['1년 새', '+1.48%포인트', 'in', at(c, 0.6)]],
         side=['64.56%', 0, '상위 20% 가구가 가진 몫']),
   scene('vs', '이 줄은 나이가 섞여 있다', SRC_R, e,
         tiles=[['이 순위에 섞인 가구', '모든 나이', '나이 구분 없이 순서대로 세움', 0, 'ink'],   # 1차 시험 2명: '순자산 줄'이 무슨 줄인지 모름
                ['젊은 가구', '아래쪽', '젊을수록 아래쪽에 있는 게 자연스러움', 0, 'accent']]),
  ],
)

if __name__ == '__main__':
    p = build('n1s_rank', SH)
    fr = sum(s['frames'] for s in p['scenes'])
    json.dump(p, open(os.path.join(VID, 'n1s_rank.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f"n1s_rank: {fr} 프레임 = {fr / 30:.1f}초 · 줄 {[l['n'] for s in p['scenes'] for l in s['lines']]} · 장면 {[round(s['frames'] / 30, 1) for s in p['scenes']]}")
