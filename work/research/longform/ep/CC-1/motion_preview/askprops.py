# CC-1 장 카드 8장(ChapterAsk) 데이터 — 2026-11-27 motion. 글자는 전부 script.md 말·자막에서 온다(assert).
# 출력 cc1_asks.json: {"asks": {"1": {...}, ...}, "preview": {...}} — PD cc1props.py ask(ch, idx)가 'asks'[ch]를 data에 더해 쓴다.
import json, os, re, sys
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__)); EP = os.path.dirname(H)
SC = open(os.path.join(EP, 'script.md'), encoding='utf-8').read()
HEADS = [re.sub(r'^\[?\d+\.\s*|\]$', '', h).strip() for h in re.findall(r'^## (.+)$', SC, re.M)]
assert len(HEADS) == 9, HEADS
NOSP = re.sub(r'\s', '', SC)

# 장마다: q(질문) · top(기준) · cells(단서, 값은 '?') · mark(손 동그라미) · foot(식) · layout
# 근거(script.md 말): 2장 36행 '2025년 11월 20일에 두 상품에 1억씩' · 자막 '세후 분배금 + 평가액' / 3장 '2023년 6월로 돌아가 같은 날 1억씩' · 화면 '커버드콜 ? · 일반형 ?'
# 4장 '주식 한 주로 보면' · '한 주 가격' · '받은 분배금' / 5장 '1억을 넣었다면 … 세금 떼고 매달' · 화면 '받아 씀 · 다시 넣음' / 6장 화면 '분배금 × 15.4%' · '국내에 상장된 해외 ETF 분배금'
# 7장 '조심할 곳이 세 군데' · '기간을 어디서 자르느냐' · '앱 차트에 나오는 가격' · '액티브 상품' / 8장 '매달 꺼내 쓸 돈' · '오래 쌓아 둘 돈'
A = {   # 11/27 4차(심사 3차 5·4·6): 끊긴 문장(6장)·'?만원대'(5장)·숫자 나열(7장) 고침 · 장마다 주황 동그라미 하나 · 선 굵고 진하게 · 세로 목록 왼쪽 맞춤
    1: dict(q=HEADS[1], cells=['커버드콜', '일반형'], mark=0, foot='배당 + ? = 분배금'),
    2: dict(q=HEADS[2], top='2025년 11월 20일 · 두 상품에 1억씩', cells=['커버드콜?', '일반형?'], mark=-1, foot='분배금 + 평가액'),
    3: dict(q='2023년 6월부터', top='더 길게 보면 · 같은 날 1억씩', cells=['받은 분배금?', '남은 돈?'], mark=1),
    4: dict(q=HEADS[4], top='주식 한 주로 보면', cells=['한 주 가격?', '받은 분배금?'], mark=0),
    5: dict(q='매달 얼마 들어왔나', top='1억을 넣었다면 · 세금 떼고', cells=['커버드콜?', '일반형?'], mark=0),
    6: dict(q='세금은 들어올 때 이미 떼고', top='1억이면 · 분배금 × 15.4%', cells=['커버드콜?', '일반형?'], mark=0),
    7: dict(q=HEADS[7], cells=['기간을 어디서 자르느냐', '앱 차트에 나오는 가격', '액티브 상품'], mark=1, layout='col', num=True),
    8: dict(q='정리', cells=['매달 꺼내 쓸 돈 → 매달 들어온 돈', '오래 쌓아 둘 돈 → 남은 돈'], mark=-1, layout='col'),
}
# 1장은 11/27 심사 A·B '같음' — 틀만 맞추고 글자는 거의 그대로(단서 칸 두 상품 이름).
def chk(s):
    for part in re.split(r'\s*[·?=→]\s*|\s*\+\s*|\s*×\s*', s):
        part = part.strip()
        if part: assert re.sub(r'\s', '', part) in NOSP, f'script.md에 없는 말: {part!r} (in {s!r})'
for ch, d in A.items():
    for k in ('q', 'top', 'foot'):
        if d.get(k): chk(d[k])
    for c in d['cells']: chk(c)
    d['seed'] = f'cc1ask{ch}'; d['n'] = f'{ch}장'
# 미리보기용 자막(장 첫 말 줄) — script.md 장 머리 다음 첫 '- ' 줄
blocks = re.split(r'^## .+$', SC, flags=re.M)[1:]
first = [next(l[2:].strip() for l in b.splitlines() if l.startswith('- ')) for b in blocks]
prev = [{'data': {**A[ch], 'end': 120}, 'frames': 120, 'lines': [{'text': first[ch], 'cap': None, 'frames': 120, 'audio': None}]} for ch in range(1, 9)]
json.dump({'asks': {str(k): v for k, v in A.items()}, 'preview': {'cards': prev}}, open(os.path.join(H, 'cc1_asks.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('ok 8장 · 글자 전부 script.md 안')
