# W-1 2화 '2. 삼성전자 100주와 15조원' BuybackDays 미리보기 props (2026-10-15 motion)
# 점 29개 = DART 자기주식취득결과보고서(raw/dart_20261012000421.xml) 하루 평균단가 원문 그대로. 화면 글자 숫자는 calc_out·script 자막에 있는 것만(assert).
# 길이: w1016/voice.json 있으면 실제 녹음 프레임, 없으면 P-1 녹음 속도(p1_timing.json spf) 어림.
#   py -3.12 work/research/longform/ep/W-1/w1016/motion_preview/buyprops.py  → w2_buy.json
import json, os, re, sys
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__)); EP = os.path.dirname(H); WORK = os.path.abspath(os.path.join(EP, '..', '..', '..', '..', '..'))
sys.path.insert(0, os.path.join(WORK, 'research', 'longform', 'loop'))
import speechcompare_script as SC
script = os.path.join(EP, 'script.md'); txt = open(script, encoding='utf-8').read()
calc = open(os.path.join(EP, 'calc_out.txt'), encoding='utf-8').read()
src_all = txt + calc
sec = next(s for s in SC.parse(script) if s['title'].startswith('2.'))
says = sec['lines']; assert len(says) == 3, says
caps, last = {}, None
for line in txt.splitlines():
    s = line.strip()
    if s.startswith('- '): last = s[2:].strip()
    elif s.startswith('[자막:') and last and last not in caps: caps[last] = s[4:].rstrip(']').strip()
voice = {}
vj = os.path.join(EP, 'voice.json')
if os.path.exists(vj):
    for s in json.load(open(vj, encoding='utf-8')).get('sections', []):
        for l in s['lines']:
            if l.get('audio'): voice[l['text']] = l
SPF = json.load(open(os.path.join(EP, '..', '..', 'P-1', 'motion_preview', 'p1_timing.json'), encoding='utf-8'))['spf']
lines = []
for t in says:
    v = voice.get(t)
    lines.append({'text': t, 'cap': caps.get(t), 'frames': (v['frames'] if v else max(12, round(SC.syl(SC.speak(t)) / SPF))) + 0, 'audio': v['audio'] if v else None})
beats, a = [], 0
for l in lines: beats.append(a); a += l['frames']

# 원문: 하루 평균단가 29일
t = open(os.path.join(EP, 'raw', 'dart_20261012000421.xml'), 'rb').read().decode('utf-8', 'ignore')
t = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', t))
days = [(f'{int(m)}/{int(d)}', int(v.replace(',', ''))) for m, d, _, _, v in re.findall(r'2026년 (\d\d)월 (\d\d)일 보통주식 ([\d,]+) ([\d,]+) ([\d,]+)', t)]
assert len(days) == 29 and '[B9] 취득 거래일 수 = 29' in calc
close = 232000
assert all(v > close for _, v in days) and '[B11] 하루 평균단가가 10/14 종가 이하인 날 수 = 0' in calc
lo = min(range(29), key=lambda i: days[i][1]); hi = max(range(29), key=lambda i: days[i][1])
assert days[lo] == ('9/15', 249701) and days[hi] == ('9/23', 283484)
months = [[i, d.split('/')[0] + '월'] for i, (d, _) in enumerate(days) if i == 0 or d.split('/')[0] != days[i - 1][0].split('/')[0]]

texts = {'closeText': '10/14 종가 232,000원', 'avgText': '회사가 산 평균값 263,823원', 'loText': '9/15 249,701원', 'hiText': '9/23 283,484원',
         'first': '8/24', 'last': '10/6', 'total': '15조원 · 29거래일', 'allAbove': '29일 모두 수요일 종가보다 높았어요',
         'dotName': '회사가 그날 산 평균값', 'stemName': '수요일 종가보다 높은 만큼',
         'unsold': '팔지 않았다면, 아직 확정된 손실은 아니에요'}
card = ['내 삼성전자 100주 · 10/8 → 10/14', '−300만원', '10/14 종가 232,000원 = 회사 평균 취득가보다 −12%']   # 2차 심사: 기준 두 개를 줄마다 밝힘   # script 2장 끝 (화면: 삼성전자 마감 …) 그대로(레드팀 10/15: 318만원은 가정 차이라 내 손실로 읽힘 → 뺌)
assert "'100주 월~수 −300만원 · 회사 평균 취득가보다 −12%'" in txt
for w in ['232,000원', '263,823원', '249,701원', '283,484원', '29거래일', '15조원', '회사가 그날 산 평균값',
          '회사가 산 평균값', '29일 모두', '수요일 종가보다 높았어요', '100주를 팔지 않았다면, 아직 확정된 손실은 아니에요']:
    assert w in src_all, w
assert 26382300 - 23200000 == 3182300

L = [l['frames'] for l in lines]
buy = {'seed': 'W-1-2-buy', 'days': [{'d': d, 'v': v} for d, v in days], 'min': 220000, 'max': 300000,
       'yticks': [[240000, '24만원'], [260000, '26만원'], [280000, '28만원']], 'months': months,
       'close': close, 'avg': 263823, 'lo': lo, 'hi': hi, 'card': card, **texts,
       'beats': beats}
scene = {'key': 'buy', 'kind': 'buy', 'title': '삼성전자 100주와 15조원', 'sub': '회사가 산 값 vs 수요일 종가', 'chapter': '2',
         'source': 'DART 2026.10.12 자기주식취득결과보고서 · 다음 금융(KRX 정규장 종가)', 'lines': lines, 'frames': sum(L) + 12}
json.dump({'scene': scene, 'buy': buy}, open(os.path.join(H, 'w2_buy.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('lines', L, 'total', scene['frames'], 'voice' if voice else '어림(P-1 spf)', 'lo', days[lo], 'hi', days[hi])
