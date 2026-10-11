# 숫자를 한국어 읽기로 바꾼다 — 2026-10-11 사장님 "17년이면 십칠 년이라고 읽어야 하는데 왜 일칠 년이라고 해?"
# Chirp 3 HD(ko-KR)는 '17년'·'1,415.2원' 같은 숫자를 자리별로 읽는 일이 있다. 녹음 전에 말(say)만 바꾸고 대본·화면 글자는 그대로 둔다.
#   py -3.12 work/korsay.py "배당 씨는 17년째에 바닥났어요."      # → 배당 씨는 십칠 년째에 바닥났어요.
# 규칙: 기본은 한자어 수(일·이·삼…, 만·억·조). 고유어 단위(살·개·명·번·가지·곳·권·장·시·달·마리·잔·사람·편·주·통)는 1~99를 고유어(한·두·세·…·스무·서른…)로.
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

NUM = r'(\d{1,3}(?:,\d{3})+|\d+)(\.\d+)?'
def _num(m_int, m_dec):
    s = m_int.replace(',', '') + (m_dec or '')
    return s

def say(text):
    t = text
    # 부호
    t = re.sub(r'[−-](?=\d)', '마이너스 ', t)
    t = re.sub(r'\+(?=\d)', '플러스 ', t)
    # 범위 A~B단위 → A단위에서 B단위 (예: '천구백팔십구 년에서 이천이십오 년')
    t = re.sub(r'(\d[\d,.]*)\s*[~～]\s*(\d[\d,.]*)(년|만원|억원|원|%|세|살|월|일|개월|배)', r'\1\3에서 \2\3', t)
    # 범위 A~B → A에서 B
    t = re.sub(r'(\d[\d,.]*)\s*[~～]\s*(?=\d)', r'\1에서 ', t)
    def rep(m):
        s = _num(m.group(1), m.group(2)); after = t_after(m)
        if '.' not in s:
            n = int(s)
            for u in NATIVE_UNITS:
                if after.startswith(u) and native(n):
                    # '시간'·'번째'는 예외 없이 고유어 가능, '개월'은 한자어
                    if u == '개' and after.startswith('개월'): break
                    if u == '시' and (after.startswith('시간') or after.startswith('시장') or after.startswith('시점')): break
                    if u == '장' and after.startswith('장기'): break
                    if u == '편' and after.startswith('편의'): break
                    return native(n) + ' '
        word = sino_dec(s)
        if after.startswith('%'): return word + ' 퍼센트'
        return word + (' ' if after[:1] and after[:1] not in ' ,.)』」]' else '')
    out, pos = [], 0
    global _T
    _T = t
    for m in re.finditer(NUM, t):
        out.append(t[pos:m.start()]); out.append(rep(m)); pos = m.end()
        if t[pos:pos+1] == '%': pos += 1
    out.append(t[pos:])
    r = ''.join(out)
    r = r.replace('×', ' 곱하기 ').replace('÷', ' 나누기 ')
    return re.sub(r'\s{2,}', ' ', r).strip()

_T = ''
def t_after(m): return _T[m.end():]

if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    for a in sys.argv[1:] or ['배당 씨는 17년째에 바닥났어요.', '1998년 시작은 11년째, 5.81억원 남음', '1,415.2원', '13.57%', '35살에 1억', '9번과 6번', '6개월', '200만원', '−140만원, +19.46%', '1989~2025년', '3가지', '20살', '21개', '100주']:
        print(a, '→', say(a))
