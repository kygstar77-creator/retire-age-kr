# P-1 실사 장 머리(StockShot) 재료 — 장 제목은 script.md, chip은 facts.txt/script.md 원문에 있는지 assert (motion 2026-10-12)
# 사용: py -3.12 work/research/longform/ep/P-1/motion_preview/stockprops.py → p1_stock.json + work/video/public/stock/ 복사
# 녹음 뒤: PD가 장마다 첫 말 앞에 dur(105프레임=3.5초)를 넣거나, 장 첫 말 줄 길이만큼 dur를 늘려 그 위에 깐다(8초 넘기지 않기 — U5).
import json, os, shutil, sys, hashlib
sys.stdout.reconfigure(encoding='utf-8')
EP = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.abspath(os.path.join(EP, '..', '..', '..', '..'))
PUB = os.path.join(ROOT, 'video', 'public', 'stock')
script = open(os.path.join(EP, 'script.md'), encoding='utf-8').read()
facts = open(os.path.join(EP, 'facts.txt'), encoding='utf-8').read()
credits = {c['id']: c for c in json.load(open(os.path.join(EP, 'stock', 'credits.json'), encoding='utf-8'))}
# (장, 제목, 영상 id, 시작 프레임, chip, chip 근거 조각들(모두 원문에 있어야 함), 글자 쪽, 가림 칸)
# 1장 달력은 '2021'(사실표 밖 연도)이 찍혀 있어 가린다. 5장 얼굴 클로즈업(5215217)은 제목이 얼굴에 앉아 선반 장면으로 바꿈(10/12 1차 스틸).
# 2차(심사 1차 8·5·5): 얼굴 있는 노동자(감액 대상처럼 읽힘)·베트남 거리(그 부부 수명처럼 읽힘)·영문 날짜 달력 → 얼굴·국적·글자 없는 컷으로. 글자 쪽 번갈아.
SHOTS = [
    ('1장', '하루 차이로 한 살?', 19875346, 30, '1969년생부터 65세', ['1969년생부터 65세'], None, []),
    ('4장', '평균까지 살면 누가 앞서나', 5612232, 60, '65세 기대여명 남 19.5년·여 23.7년(평균)', ['기대여명', '남 19.5년', '여 23.7년', '평균'], None, []),  # 3차: 34418451 운동화 옆줄=상표로 읽힘(레드팀)
    ('5장', '519만원 위의 계단', 18835800, 60, '국민연금법 제63조의2 · 2026-06-17 시행', ['제63조의2', '2026-06-17 시행'], None, [{'x': 410, 'y': 625, 'w': 220, 'h': 110}]),  # 노트북 상표
    ('6장', '445억원은 누구 몫?', 7593893, 30, '신청 없이 7월 말부터 환급', ['신청 없이 7월 말부터 환급'], None, []),
]
os.makedirs(PUB, exist_ok=True)
# 편마다 바뀜(레드팀 2차 '편을 넘겨 같은 틀'): 첫 글자 쪽·길이·칩 등장 시점을 편 이름 해시로. 한 편 안에서는 번갈아.
H = int(hashlib.md5('P-1'.encode()).hexdigest(), 16)
SIDE0 = ['left', 'right'][H % 2]; DUR = 96 + (H >> 3) % 25; CHIP_AT = 36 + (H >> 9) % 14
for c in credits.values(): c['used'] = False   # 매번 다시 표시(레드팀 10/12)
shots = []
for k, (ch, title, vid, frm, chip, proof, side, blur) in enumerate(SHOTS):
    side = side or [SIDE0, 'right' if SIDE0 == 'left' else 'left'][k % 2]
    assert len(chip) <= 28, f'칩 {len(chip)}자 > 28: {chip}'
    n = ch[0]
    assert f'## {n}. {title}' in script, f'장 제목 다름: {ch} {title}'
    for x in proof: assert x in script or x in facts, f'chip 근거 없음: {x}'
    c = credits[vid]; dur = DUR
    assert c['sec'] * 30 >= frm + dur, f'원본 짧음 {vid}'
    shutil.copyfile(os.path.join(EP, 'stock', c['file']), os.path.join(PUB, c['file']))
    shots.append({'seed': 'P-1', 'src': f"stock/{c['file']}", 'from': frm, 'chapter': ch, 'title': title, 'chip': chip, 'chipAt': CHIP_AT, 'dur': dur, 'blur': blur, 'side': side})
    c['used'] = True
json.dump({'shots': shots}, open(os.path.join(EP, 'motion_preview', 'p1_stock.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
json.dump(list(credits.values()), open(os.path.join(EP, 'stock', 'credits.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('설명란 줄(PD):'); [print(' ', credits[s[2]]['desc_line']) for s in SHOTS]
print('ok', len(shots), 'shots')
