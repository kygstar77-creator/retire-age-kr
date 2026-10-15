# h1s_forest — H-1 롱폼(rVg0pQVo_wk, 10/15 공개) 둔촌동 장(올림픽파크포레온: 평당 값·거래 몰림·전세)을 자른 세로 쇼츠 props · 틀 'c2person'(C2P)
#   py -3.12 work/research/cardshorts/h1s_forest/h1forestclip.py   → work/video/h1s_forest.json + public/c2p/h1f_*.png
#   렌더: cd work/video && npx remotion render src/c2p_index.ts C2P out/h1s_forest.mp4 --props=h1s_forest.json
# 왜 c2person: ⓓ(최근 10편 한 틀 50% 초과 거부) — 지금 m1clip 5/9·c1clip 4/9라 m1clip은 업로드 거부, c1clip은 지시로 제외(10/15 23:10 운영실장).
# 10/15 23:2x 눈 검사: 37500921 항공 프레임에 '강선 1302' 단지 이름 보임 → 뺌 · 38350742 역 계단은 얼굴 또렷 → 27560146(뒷모습·작게)로 · 질문 '6년 새 아파트'는 '6년 된 새 집'으로 읽힐 수 있어 '집값은 거의 같은데 / 전세는?'
# 23:2x 58세 이해 시험: 배지 '참고 영상 · 해당 단지 아님'이 무엇이 아니라는 건지 헷갈림 → '화면 속 아파트는 포레온 아님'
# 그림 = Pexels 무료 영상(서울 아파트·역) 프레임, 그림 안 큰 글자 0 · 특정 단지 이름 보이는 37527858('강선')은 뺌 · 배지 '참고 영상 · 해당 단지 아님'(오인 막기).
#   출처는 stock/credits.json → 설명란 끝 줄. 실사 영상(생성 아님)이라 합성 표시 대상 아님.
# 목소리 = H-1 롱폼 문장 wav 그대로(Chirp 3 HD Charon, 새 녹음 0) · 줄은 h1.json 말 글자로 찾는다.
# 화면 숫자·글자 = h1.json(편집 통과 화면 글자) f_map·f_bars·f_period·f_rent·f_walk에 있는 것만 — need()로 기계 대조.
# 첫 줄 = 47 '이 단지 전세 가운데 값은 14억으로…'(35자·숫자, 꼴 ⓐ) · 39는 39자라 첫 줄 불가.
import os, json, sys, re, shutil
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
VID = os.path.join(WORK, 'video')
H1 = json.load(open(os.path.join(VID, 'h1.json'), encoding='utf-8'))
BYTEXT = {l['text']: l for s in H1['scenes'] for l in s['lines']}
H1TXT = json.dumps(H1, ensure_ascii=False)
def need(*xs):
    for x in xs: assert x in H1TXT, f'h1.json 화면 글자에 없음: {x}'
TAIL = 36

def L(t):
    hit = [k for k in BYTEXT if k.startswith(t)]; assert len(hit) == 1, (t, hit)
    l = BYTEXT[hit[0]]; assert l.get('audio') and os.path.exists(os.path.join(VID, 'public', l['audio'])), t
    return {'text': l['text'], 'audio': l['audio'], 'frames': l['frames']}

os.makedirs(os.path.join(VID, 'public', 'c2p'), exist_ok=True)
def pic(name):
    dst = 'h1f_' + {'38029457_1': 'tower', '38029457_6': 'tower2', '30975009_1': 'city', '30975009_6': 'city2', '37500921_1': 'aerial', '37500921_6': 'aerial2', '38350742_1': 'subway', '27560146_6': 'gate'}[name]   # 파일 이름 숫자가 숫자 대조·꼴 ⓒ에 걸려 글자 이름으로
    shutil.copyfile(os.path.join(HERE, 'pics', name + '.png'), os.path.join(VID, 'public', 'c2p', dst + '.png'))
    return f'c2p/{dst}.png'

def sc(p, tag, lines, num, sub, *, cx=960, zoom=(1.0, 1.08), pan=0, focus=0.4, gray=False, red=(), green=()):
    ls = [L(t) for t in lines]
    for x in [num, sub]:
        for d in re.findall(r'\d[\d,.]*', x): need(d)
    fr = sum(l['frames'] for l in ls); assert fr <= 8 * 30 + 30, (num, fr)
    return {'pic': pic(p), 'cx': cx, 'year': tag, 'num': num, 'sub': sub, 'zoom': list(zoom), 'pan': pan, 'focus': focus,
            'gray': gray, 'blur': False, 'red': list(red), 'green': list(green), 'lines': ls, 'frames': fr}

need('14.00억', '12.50억', '12,032세대', '9,510세대', '2024.11 입주', '28.50억 vs 28.25억', '430m', '270m', '113건 중 94건(83%)', '1건', '49.6', '43.9',
     '매매 값이 같아도', '보증금이 더 드는 단지', '둔촌오륜역 출입구', '서울위례초등학교')
scenes = [
    sc('38029457_1', '올림픽파크포레온', ['이 단지 전세 가운데 값은 14억'], '14억', '전세 · 헬리오시티는 12억 5천만원', zoom=(1.25, 1.1), green=['14억으로']),
    sc('30975009_1', '2024.11 입주', ['재작년 말에 입주한'], '12,032세대', '헬리오시티 9,510세대보다 큰 단지', zoom=(1.0, 1.1), pan=-30),
    sc('30975009_6', '84㎡ 한 채 값', ['6년 가까이 늦게 지은'], '거의 같음', '28.25억 vs 헬리오시티 28.50억', cx=600, zoom=(1.05, 1.15), pan=30),
    sc('27560146_6', '걸어서', ['걸어서는 둔촌오륜역'], '430m', '둔촌오륜역 출입구까지', zoom=(1.1, 1.2)),
    sc('30975009_1', '걸어서', ['가장 가까운 초등학교는 역보다 더 가'], '270m', '가장 가까운 초등학교 · 배정 학교 아님', cx=1400, zoom=(1.3, 1.4), pan=-20),
    sc('30975009_6', '1년 실거래', ['손품 씨는 여기서 이상한 점'], '거래 몰림', '국토교통부 실거래 1년 · 손품 씨 = 가상 인물', zoom=(1.15, 1.25), pan=24),
    sc('38029457_6', '2026년 4~5월', ['모든 평형을 합치면'], '83%', '한 해 113건 중 94건이 봄 두 달', zoom=(1.0, 1.1), focus=0.3),
    sc('30975009_1', '그 앞 다섯 달', ['그 앞 다섯 달은', '왜 그때 몰렸는지는'], '1건', '이유는 실거래 자료에 없음', zoom=(1.3, 1.2), gray=True, red=['없었고요']),
    sc('38029457_6', '전세', ['손품 씨 눈에 들어온 건', '매매 값에서 전세가 차지하는'], '49.6%', '집값 중 전세 비율 · 헬리오시티 43.9%', cx=700, zoom=(1.2, 1.3), pan=-24),
    sc('38029457_1', '전세 사는 사람이면', ['전세로 사는 사람 입장에선'], '보증금 더', '전세 14억 vs 헬리오시티 12억 5천만원', zoom=(1.1, 1.0), focus=0.3),
]
scenes[-1]['frames'] += TAIL
p = {'fps': 30, 'name': 'h1s_forest', 'layout': 'c2person', 'question': ['집값은 거의 같은데', '전세는?'], 'hot': '전세',
     'badge': '화면 속 아파트는 포레온 아님', 'base': '국토교통부 실거래 2025.11~2026.10 · 84㎡대 가운데 값(중간값)', 'scenes': scenes}
json.dump(p, open(os.path.join(VID, 'h1s_forest.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
fr = sum(s['frames'] for s in scenes)
print(f'h1s_forest: {fr} 프레임 = {fr / 30:.1f}초 · 장면 {len(scenes)} · 최장 {max(s["frames"] for s in scenes) / 30:.1f}초 · 첫 줄 "{scenes[0]["lines"][0]["text"]}"')
