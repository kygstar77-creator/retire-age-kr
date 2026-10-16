# n1s_top10 — N-1 롱폼(420buEFKB8k) '가구 순자산 상위 10% 문턱, 1년 새 5,428만원'을 자른 세로 쇼츠 props (firemap-video-producer 2026-10-16)
#   py -3.12 work/research/cardshorts/n1s_top10/n1topclip.py   → work/video/n1s_top10.json (틀 C1S — h1s_helio와 같은 길)
# 틀: C1S(layout c1clip). log.jsonl 최근 10편(10/18~10/22 예약분 + c2s_jungwoo·p1s_step) m1clip 5 · c2person 3 · c1clip 2 → m1clip은 6/10이 될 수 있어 뺌.
# 목소리 = N-1 롱폼 문장 wav 그대로(gemini-3.8-flash-tts Charon, 새 녹음 0). 줄 28은 문장 사이 쉼(3.08~3.52초)에서 둘로 나눔(새 녹음 아님).
# 화면 숫자 = video/n1.json 9·12·13장 data 그대로(새 계산 0). 연봉 줄(N-2와 겹침)은 쓰지 않는다.
# 줄 순서: 28앞에서 '그리고' 뗀 줄('상위 10% 문턱은 11억 20만원이에요.', 첫 줄 21자·숫자) → 28뒤('순자산 10억원은 아직 문턱 아래…') → 33(가운데 거의 그대로) → 35·36(위로 갈수록 올랐다) → 37(한 달 452만원꼴, 끝 줄 면책 아님).
import os, json, sys, wave
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from w1g1clips import at, scene, build, VID

N1 = json.load(open(os.path.join(VID, 'n1.json'), encoding='utf-8'))
NL = [l for s in N1['scenes'] for l in s['lines']]
SC = {s['kind']: s for s in N1['scenes']}
assert NL[28]['text'].startswith('그리고 상위 10% 문턱은 11억 20만원이에요.') and NL[33]['text'].startswith('가운데 가구, 중앙값은 2억 4,000만원에서')
assert NL[35]['text'].startswith('그런데 위로 갈수록 반대예요.') and NL[36]['text'].startswith('그리고 상위 10% 문턱은 10억 4,592만원에서') and NL[37]['text'].startswith('5,428만원을 열두 달로')

def L(*idx):
    return [{'n': i, 'text': NL[i]['text'], 'cap': NL[i].get('cap'), 'audio': NL[i]['audio'], 'frames': NL[i]['frames']} for i in idx]

# 줄 28을 문장 사이 쉼에서 나눔
SRC = NL[28]; CUT = 3.30
assert SRC['audio'] == 'audio/n-1/' + os.path.basename(SRC['audio'])
w = wave.open(os.path.join(VID, 'public', SRC['audio'])); sr = w.getframerate(); raw = w.readframes(w.getnframes()); prm = w.getparams(); w.close()
k = int(CUT * sr) * prm.sampwidth * prm.nchannels
def wr(name, data, text, n):
    o = wave.open(os.path.join(VID, 'public', 'audio', 'n-1', name), 'wb'); o.setparams(prm); o.writeframes(data); o.close()
    return {'n': n, 'text': text, 'cap': None, 'audio': f'audio/n-1/{name}', 'frames': round(len(data) / (sr * prm.sampwidth * prm.nchannels) * 30) + 8}
A_TXT = '그리고 상위 10% 문턱은 11억 20만원이에요.'; B_TXT = '순자산 10억원은 아직 문턱 아래, 위에서 10%와 20% 사이입니다.'
assert SRC['text'] == A_TXT + ' ' + B_TXT
k0 = int(0.45 * sr) * prm.sampwidth * prm.nchannels   # 10/16 꼴 ⓐ: 28뒤 첫 줄 39자 → 앞의 '그리고 '(0.13~0.35초)를 쉼(0.37~0.52초)에서 떼고 '상위 10% 문턱은…'(21자)을 첫 줄로
A0_TXT = A_TXT.replace('그리고 ', '')
S28A = wr('n1t_A0.wav', raw[k0:k], A0_TXT, 28); S28B = wr('n1t_B.wav', raw[k:], B_TXT, 28)

ru = SC['ruler']; sh = SC['shift']; mo = SC['month']
ps = dict(ru['data']['ps']); rows = {r[0]: r for r in sh['data']['rows']}
assert ps[90] == 110020 and ps[50] == 23860 and rows[90][1:] == [104592, 110020, 5428] and rows[50][1:] == [24000, 23860, -140]
assert rows[70][3] == 824 and rows[80][3] == 2930 and mo['data'] == {'y': 5428, 'm': 452, 'at': [0, 1]}
assert [p for p in ru['data']['pins'] if p[0] == '10억원'][0][1] < 90   # 10억원은 문턱(위 10%) 아래
SRC_T = ru['source']

a = [S28A, S28B]; b = L(33); c = L(35, 36); e = L(37)
SH = dict(
  question=['순자산 10억,', '상위 10% 안일까?'], hot='10억',
  base='2025년 가계금융복지조사 · 2025년 3월 말 가구 순자산',   # 1차 이해 시험: '지나간 값' 둘 다 모름
  answer=dict(label='상위 10%에 들려면 필요한 순자산', items=['11억 20만원', '1년 새 +5,428만원'], arrow=False,
              note='딱 중간 가구는 −140만원 · 거의 그대로'),
  scenes=[
   scene('vs', '10억원은 어디쯤', SRC_T, a, full=True,   # full = 판 90프레임 당김(0초부터 첫 칸이 다 보이게)
         tiles=[['순자산 10억원', '상위 10~20%', '10억은 이 자리 · 상위 10%엔 못 듦', 0, 'ink'],   # 2·3차 시험: '위(에서) 10~20%'를 '10~20% 모자람·올랐다'로
                ['상위 10%에 들려면', '11억 20만원', '11억원에 20만원 더 · 순자산 = 집·예금·주식 − 빚', 0, 'accent']]),   # 10/16 눈 검사: 둘째 칸 4.6초 빈 판 → 0초부터(답 숫자 0초 화면)
   scene('vs', '가운데 가구 · 1년 사이', sh['source'], b,
         tiles=[['딱 중간 가구 · 1년 전', '2억 4,000만원', '2024년 3월 말 · 중앙값', 0, 'ink'],
                ['딱 중간 가구 · 1년 뒤', '2억 3,860만원', '−140만원(−0.6%) · 거의 그대로', at(b, 0.3), 'fall']]),
   scene('diverge', '1년 새 경계선이 움직인 돈', sh['source'], c, head='그 자리에 들려면 필요한 돈 · 1년 새 변화', max=5428, x0=480, half=200,   # 2차 눈 검사: 이름표 '위 30% 선' 왼쪽 잘림 → x0 480·half 200(이름표 70~250, 값 716~)   # 10/16 눈 검사: '+5,428만원' 오른쪽 잘림 → 왼쪽으로
         rows=[['중간 가구', -140, '−140만원', 0], ['위 30% 선', 824, '+824만원', at(c, 0.45)], ['위 20% 선', 2930, '+2,930만원', at(c, 0.75)],   # 2차 시험: '그 사람들이 번 돈'으로 읽음 → '선'
               ['위 10% 선', 5428, '+5,428만원', at(c, 1.1)]]),   # 줄 4개라 q 말칸(y 620)이 겹쳐 뺌
   scene('receipt', '한 달로 나누면', mo['source'], e, head='상위 10% 기준선 · 1년 새 오른 금액', size=46,
         rows=[['1년', '+5,428만원', 'in', 0], ['÷ 12달', '한 달 452만원꼴', 'net', at(e, 0.15)], ['누가 번 돈은 아님', '기준선이 오른 금액', 'dim', at(e, 0.6)]],   # 2차 시험: '누가 번 돈? 아님' 토막 말
         side=['452만원', at(e, 0.18), '기준선이 한 달에 오른 금액']),
  ],
)

if __name__ == '__main__':
    p = build('n1s_top10', SH)
    fr = sum(s['frames'] for s in p['scenes'])
    json.dump(p, open(os.path.join(VID, 'n1s_top10.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f"n1s_top10: {fr} 프레임 = {fr / 30:.1f}초 · 줄 {[l['n'] for s in p['scenes'] for l in s['lines']]} · 28 나눔 {S28B['frames']}+{S28A['frames']}")
