# H-5 meta.json 설명·챕터 채우기 — video/h5.json(장 카드 시작)·voice.json·bg_used.json(실사 출처) → meta.json desc·chapters + desc_1118.txt(editor 설명란 서명용)
#   py -3.12 work/research/longform/ep/H-5/h5meta.py   (h5props.py 다음에, 녹음·말이 바뀌면 다시)
# 11/18 14시대 PD: JT-1 jt1meta.py 꼴. 바꾼 것
#   ① 11/17 국토부 다시 받기(facts F4'·F5') 숫자로 설명 첫 두 줄·단지 수 고침: 7.35억→7.40억(7억 4천만원)·30곳→32곳·바닥보다 9%→10%
#   ② 썸네일 thumb_h5_o1n.png(주황 줄 '지금 7억 4,000만원' — o1과 같은 꼴, 숫자만) · 사진 출처 visual/H-5-thumb/photo/sources.json
#   ③ 카페 줄 아래 사이트 줄(ytlong C9 11/11 — 맞는 계산기 없어 H-4처럼 메인) · '권유 아님' 줄(disclaim)
import json, os, re, sys
sys.stdout.reconfigure(encoding='utf-8')
EP = os.path.dirname(os.path.abspath(__file__))
VID = os.path.normpath(os.path.join(EP, '..', '..', '..', '..', 'video'))
P = json.load(open(os.path.join(VID, 'h5.json'), encoding='utf-8'))
V = json.load(open(os.path.join(EP, 'voice.json'), encoding='utf-8'))
MP = os.path.join(EP, 'meta.json')
m = json.load(open(MP, encoding='utf-8'))
m['chapter_titles'] = ['결론부터', '처음 보시는 분을 위해', '5년 흐름, 고점·바닥·지금', '단지 서른세 곳, 얼마나 돌아왔나',
                       "'반값'과 '6~70%'는 어디서 나왔나", '전세는 매매의 몇 %', '직접 확인하는 법', '정리']   # script.md ## 제목·toc '우리 목차'
heads = m['chapter_titles']
starts, a = [0], 0
for s in P['scenes']:
    if s['kind'] == 'ask' and re.match(r'^(\d+장|기초)$', (s.get('data') or {}).get('n', '')): starts.append(a)
    a += s['frames']
assert len(starts) == len(heads) == 8, (len(starts), len(heads))
fps = P.get('fps', 30)
fmt = lambda f: f"{int(f / fps) // 60}:{int(f / fps) % 60:02d}"
chapters = [[round(st / fps), h] for st, h in zip(starts, heads)]
assert all(b[0] - a_[0] >= 10 for a_, b in zip(chapters, chapters[1:])), chapters
CH = '\n'.join(f"{fmt(st)} {h}" for st, h in zip(starts, heads))

FIRST2 = ["송도동 아파트 84㎡대 실거래를 같은 잣대(중간 가격)로 세어 보니, 고점 1년(2021년 7월~2022년 6월) 9억에서 2026년 7~10월 7억 4천만원, 고점의 82%예요.",
          "단지 33곳은 71~97%였고, 가장 낮았던 1년보다는 10% 높아요. '반값'·'6~70%'라는 말이 어디서 나왔는지, 전세는 매매의 몇 %인지도 국토교통부 원자료로 셌습니다."]
SITE = '파이어맵: https://firemap.kr/?utm_source=youtube&utm_medium=description&utm_campaign=h-5'
DIS = '지나간 거래 값이고, 특정 단지를 사거나 팔라는 뜻이 아닙니다.'
tpl = m['desc_tpl']
old2 = tpl.split('\n\n', 1)[0]
tpl = '\n'.join(FIRST2) + '\n\n' + tpl.split('\n\n', 1)[1]
tpl = tpl.replace('단지 30곳 전체 표', '단지 33곳 전체 표')
if 'firemap.kr' not in tpl:
    tpl = tpl.replace('(카페): {CAFE}\n', '(카페): {CAFE}\n' + SITE + '\n', 1)
tpl = tpl.replace('시세 설명이고, 특정 단지를 사거나 팔라는 권유는 아니에요.', DIS)
tpl = tpl.replace('값은 거래를 가격 순서로 줄 세운 가운데 값', '값은 거래를 가격 순서로 줄 세운 중간 가격(가운데 값)')
credits = list(dict.fromkeys(c['desc_line'] for c in json.load(open(os.path.join(EP, 'bg_used.json'), encoding='utf-8'))))
src = json.load(open(os.path.join(EP, '..', '..', '..', 'visual', 'H-5-thumb', 'photo', 'sources.json'), encoding='utf-8'))['songdo_park_canal_18495181.jpg']
thumb_credit = f"{src['by']} / Pexels ({src['url']})"
cafe = m.get('cafe_url') or 'https://cafe.naver.com/firemap'
desc = tpl.replace('{CAFE}', cafe).replace('{CHAPTERS}', CH).replace('{STOCK}', '\n'.join(credits)).replace('{THUMB_CREDIT}', thumb_credit)
m.update({'desc_tpl': tpl, 'desc': desc, 'desc_first2': FIRST2, 'chapters': chapters,
          'desc_first2_src': "11/18 PD: facts F4'(7.40억·82%·바닥보다 10%)·F5'(32곳 71~97%) — 11/17 국토부 다시 받기 · 이전 " + old2.replace('\n', ' / ')[:60] + '…',
          'thumb': os.path.join(EP, 'thumb_h5_o1n.png'), 'thumb_text': '고점 때 9억이던 값 / 지금 7억 4,000만원',
          'thumb_status': "11/18 PD: o1(copywriter 11/14 1초 시험 통과·1위)과 같은 꼴, 주황 줄 숫자만 7억 3,500만원→7억 4,000만원(F4' 7.40억, say 41행 '7억 4천만원쯤') — visual/H-5-thumb/make_h5.py fix1118 · copywriter 재확인 요청",
          'voice': f"Chirp 3 HD Charon {V.get('speakingRate')} · {V.get('done')}줄 · {V.get('seconds')}초 · 11/17 20줄+2줄 재녹음(editor 555e65b4)",
          'missing': V.get('missing'), 'chapters_note': f'video/h5.json 장 카드 시작 프레임(11/18 PD h5meta.py) — 렌더 전 props 길이 {round(a / fps, 1)}초'})
json.dump(m, open(MP, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
open(os.path.join(EP, 'desc_1118.txt'), 'w', encoding='utf-8').write(m['title'] + '\n\n' + desc + '\n')
print(CH); print(f'설명 {len(desc)}자 · 실사 출처 {len(credits)}줄 · missing {V.get("missing")}')
