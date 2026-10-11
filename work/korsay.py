# 숫자를 한국어 읽기로 바꾼다 — 2026-10-11 사장님 "17년이면 십칠 년이라고 읽어야 하는데 왜 일칠 년이라고 해?"
# Chirp 3 HD(ko-KR)는 '17년'·'1,415.2원' 같은 숫자를 자리별로 읽는 일이 있다. 녹음 전에 말(say)만 바꾸고 대본·화면 글자는 그대로 둔다.
#   py -3.12 work/korsay.py "배당 씨는 17년째에 바닥났어요."      # → 배당 씨는 십칠 년째에 바닥났어요.
#   py -3.12 work/korsay.py --test                                 # 아래 TESTS 전부 대조(틀리면 exit 1)
# 규칙: 기본은 한자어 수(일·이·삼…, 만·억·조). 고유어 단위(살·개·명·번·가지·곳·권·장·시·달·마리·잔·사람·편·통)는 1~99를 고유어(한·두·세·…·스무·서른…)로.
# 10/11 PD 고침(W-1·G-1·C-1 숫자 줄 112개를 돌려 보고 찾은 것):
#   ① '1천만원'→'일 천만원'(×) → '천만 원' · '3천만원'→'삼천만 원' · '7백만원'→'칠백만 원' · '1만 달러'→'만 달러' (숫자 뒤 천·백·만·억·조를 붙여 읽음, 1천·1백·1만의 '일'은 안 읽음)
#   ② '7,000을'→'칠천 을'(×) → '칠천을' — 조사(을·를·이·가·은·는·도·에·의·와·과·로·대·쯤·씩·째·까지·부터·만큼)는 띄우지 않는다
#   ③ '6월'→'육 월'(×) → '유월', '10월'→'시월'
#   ④ '2~3번'→'이 에서 세 번'(×) → '두세 번' (고유어 단위 범위: 한두·두세·서너·네다섯·대여섯·예닐곱·일고여덟·여덟아홉), 그 밖의 범위는 'A단위에서 B단위'
#   ⑤ '1번째'→'한 번째'(×) → '첫 번째'
#   ⑥ 대본의 출처 표시 '{F}'(W-1)를 소리 내지 않게 지움
import re, sys

SINO = '영일이삼사오육칠팔구'
def _four(n):  # 0~9999
    s = ''
    for v, u in ((1000, '천'), (100, '백'), (10, '십'), (1, '')):
        d = n // v % 10
        if d: s += ('' if (d == 1 and u) else SINO[d]) + u
    return s
def sino(n):
    if n == 0: return '영'
    out = []
    for v, u in ((10**12, '조'), (10**8, '억'), (10**4, '만'), (1, '')):
        q = n // v % 10000
        if q: out.append(('' if (q == 1 and u == '만') else _four(q)) + u)
    return ' '.join(out).strip()
def sino_dec(s):  # '5.81' → 오 점 팔일
    if '.' in s:
        a, b = s.split('.', 1)
        return sino(int(a or 0)) + ' 점 ' + ''.join(SINO[int(c)] for c in b)
    return sino(int(s))

NAT1 = ['', '한', '두', '세', '네', '다섯', '여섯', '일곱', '여덟', '아홉']
NAT10 = ['', '열', '스물', '서른', '마흔', '쉰', '예순', '일흔', '여든', '아흔']
def native(n):
    if not 1 <= n <= 99: return None
    t, o = divmod(n, 10)
    if o == 0 and t == 2: return '스무'
    return NAT10[t] + NAT1[o]
NATIVE_UNITS = ('살', '개', '명', '번', '가지', '곳', '권', '장', '시', '달', '마리', '잔', '사람', '편', '통')
NATIVE_PAIR = {1: '한두', 2: '두세', 3: '서너', 4: '네다섯', 5: '대여섯', 6: '예닐곱', 7: '일고여덟', 8: '여덟아홉'}   # A~A+1 고유어 어림
MONTH = {6: '유월', 10: '시월'}
PARTICLE = ('을', '를', '이', '가', '은', '는', '도', '에', '의', '와', '과', '로', '대', '쯤', '씩', '째', '까지', '부터', '만큼', '여')
RANGE_UNITS = r'(년째|년|개월|분기|만원|억원|원|%|세|월|일|배|주|시간|' + '|'.join(sorted(NATIVE_UNITS, key=len, reverse=True)) + ')'
BIG = r'(?:[천백십]?[만억조]|[천백])'   # 숫자 바로 뒤 큰 단위: '1천만', '7백만', '180억', '5천'

NUM = r'(\d{1,3}(?:,\d{3})+|\d+)(\.\d+)?'

def _is_native(after):
    for u in NATIVE_UNITS:
        if after.startswith(u):
            if u == '개' and after.startswith('개월'): return None
            if u == '시' and (after.startswith('시간') or after.startswith('시장') or after.startswith('시점')): return None
            if u == '장' and after.startswith('장기'): return None
            if u == '편' and after.startswith('편의'): return None
            return u
    return None

def _range(m):
    a, b, u = m.group(1), m.group(2), m.group(3)
    if re.fullmatch(r'\d', a) and re.fullmatch(r'\d', b) and u in NATIVE_UNITS and int(b) == int(a) + 1 and int(a) in NATIVE_PAIR:
        return NATIVE_PAIR[int(a)] + ' ' + u
    return f'{a}{u}에서 {b}{u}'

def say(text):
    t = re.sub(r'\{[A-Z]\d*\}\s*', '', text)          # 출처 표시 {F} 등은 소리 내지 않는다
    # 부호
    t = re.sub(r'(?<![\d가-힣A-Za-z])[−-](?=\d)', '마이너스 ', t)
    t = re.sub(r'\+(?=\d)', '플러스 ', t)
    # 범위 A~B단위
    t = re.sub(r'(\d[\d,.]*)\s*[~～]\s*(\d[\d,.]*)' + RANGE_UNITS, _range, t)
    # 범위 A~B → A에서 B
    t = re.sub(r'(\d[\d,.]*)\s*[~～]\s*(?=\d)', r'\1에서 ', t)
    out, pos = [], 0
    for m in re.finditer(NUM, t):
        out.append(t[pos:m.start()]); pos = m.end()
        s = m.group(1).replace(',', '') + (m.group(2) or ''); after = t[pos:]
        if '.' not in s:
            n = int(s)
            if after.startswith('월') and n in MONTH:
                out.append(MONTH[n]); pos += 1; continue
            if after.startswith('번째') and n == 1:
                out.append('첫 '); continue
            u = _is_native(after)
            if u and native(n):
                out.append(native(n) + ' '); continue
        if after.startswith('%'):
            out.append(sino_dec(s) + ' 퍼센트'); pos += 1; continue
        bm = re.match(BIG, after)
        if bm and '.' not in s:
            # '1천만원' → '천만', '3천만원' → '삼천만', '180억' → '백팔십억', '1억' → '일억'(억·조 앞 1은 읽는다)
            n = int(s); big = bm.group(0)
            head = '' if (n == 1 and big[0] in '천백십만') else sino(n).replace(' ', '')
            word = head + big; pos += len(big); after = t[pos:]
        else:
            word = sino_dec(s)
        nxt = after[:1]
        sep = '' if (not nxt or nxt in ' ,.)』」]?!·/' or after.startswith(PARTICLE)) else ' '
        out.append(word + sep)
    out.append(t[pos:])
    r = ''.join(out)
    r = r.replace('×', ' 곱하기 ').replace('÷', ' 나누기 ')
    return re.sub(r'\s{2,}', ' ', r).strip()

TESTS = [
    ('배당 씨는 17년째에 바닥났어요.', '배당 씨는 십칠 년째에 바닥났어요.'),
    ('1998년 시작은 11년째, 5.81억원 남음', '천구백구십팔 년 시작은 십일 년째, 오 점 팔일 억원 남음'),
    ('1,415.2원', '천사백십오 점 이 원'),
    ('13.57%', '십삼 점 오칠 퍼센트'),
    ('35살에 1억', '서른다섯 살에 일억'),
    ('9번과 6번', '아홉 번과 여섯 번'),
    ('6개월', '육 개월'),
    ('200만원', '이백만 원'),
    ('−140만원, +19.46%', '마이너스 백사십만 원, 플러스 십구 점 사육 퍼센트'),
    ('1989~2025년', '천구백팔십구 년에서 이천이십오 년'),
    ('3가지', '세 가지'), ('20살', '스무 살'), ('21개', '스물한 개'), ('100주', '백 주'),
    # 10/11 PD 고침
    ('돈이 1천만원 있었다', '돈이 천만 원 있었다'),
    ('분배금을 3천만원 넘게', '분배금을 삼천만 원 넘게'),
    ('차이가 7백만원이 넘는데도', '차이가 칠백만 원이 넘는데도'),
    ('그대로 1만 달러인데', '그대로 만 달러인데'),
    ('180억 달러가', '백팔십억 달러가'),
    ('영업이익 107조원을', '영업이익 백칠조 원을'),
    ('7,000을 넘던 지수가 6,600대까지', '칠천을 넘던 지수가 육천육백대까지'),
    ('6월 말 주주에게 8월에 지급', '유월 말 주주에게 팔 월에 지급'),
    ('10월 둘째 주', '시월 둘째 주'),
    ('2~3번', '두세 번'), ('3~4개', '서너 개'), ('5~10번', '다섯 번에서 열 번'),
    ('1번째', '첫 번째'), ('2번째', '두 번째'),
    ('3분의 1쯤', '삼 분의 일쯤'),
    ('{F} 둘을 합치면, 약 5만원 줄었어요.', '둘을 합치면, 약 오만 원 줄었어요.'),
    ('세금이 0원이에요.', '세금이 영 원이에요.'),
    ('에스앤피 500을 따라가는', '에스앤피 오백을 따라가는'),
    ('5억 넘게', '오억 넘게'),
    ('2002년이었습니다', '이천이 년이었습니다'),
    ('5.31%로', '오 점 삼일 퍼센트로'),
]

if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    if sys.argv[1:] == ['--test']:
        bad = [(a, b, say(a)) for a, b in TESTS if say(a) != b]
        for a, b, g in bad: print('틀림:', a, '→', g, '| 기대', b)
        print(f'{len(TESTS) - len(bad)}/{len(TESTS)} 통과'); sys.exit(1 if bad else 0)
    for a in sys.argv[1:] or [a for a, _ in TESTS]:
        print(a, '→', say(a))
