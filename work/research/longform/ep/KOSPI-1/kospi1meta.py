# KOSPI-1 meta.json — video/kospi1.json(장 카드 시작)·voice.json·bg_used.json(실사 출처) → meta.json + desc_1120.txt
#   py -3.12 work/research/longform/ep/KOSPI-1/kospi1meta.py   (kospi1props.py 다음에, 녹음·말·숫자가 바뀌면 다시)
# 11/20 PD: H-5 h5meta.py 꼴. 제목 = copywriter final.txt 1위 T8(11/20 18:54) · 설명 첫 줄 = copywriter titles.md '설명 첫 줄'
#   썸네일 = visual k1_p1(11/20 17:08) 자리 — copywriter 4차 '권유 반려(좁게)'로 visual p2 → thumbpair → youtube-loop 고름. 바뀌면 THUMB만 고치고 다시
#   11/23 아침 youtube-loop ECOS 다시 셈에서 24가 바뀌면 제목·썸네일·설명·말 같이(공개 조건 4)
import json, os, sys
sys.stdout.reconfigure(encoding='utf-8')
EP = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(EP, '..', '..', '..', '..', '..'))
VID = os.path.join(ROOT, 'work', 'video')
P = json.load(open(os.path.join(VID, 'kospi1.json'), encoding='utf-8'))
V = json.load(open(os.path.join(EP, 'voice.json'), encoding='utf-8'))
MP = os.path.join(EP, 'meta.json')
m = json.load(open(MP, encoding='utf-8')) if os.path.exists(MP) else {}
TITLES = [l.strip() for l in open(os.path.join(ROOT, 'work', 'research', 'copy', 'kospi1', 'final.txt'), encoding='utf-8') if l.strip()]
THUMB = os.path.join(EP, 'thumb_k1_p1.png')

heads = ['여는 말', '올해 코스피', '서킷브레이커와 사이드카', '지난 31년, 크게 빠진 날 그 뒤', '전날 값을 되찾기까지',
         '크게 빠진 해엔 크게 오른 날도', '1천만원을 넣었다면', '함정', '정리']   # script.md ## 제목
starts, a = [0], 0
for s in P['scenes']:
    if s['kind'] == 'ask' and str((s.get('data') or {}).get('n', '')).endswith('장'): starts.append(a)
    a += s['frames']
fps = P.get('fps', 30)
assert len(starts) == len(heads) == 9, (len(starts), len(heads))
chapters = [[round(st / fps), h] for st, h in zip(starts, heads)]
assert all(b[0] - a_[0] >= 10 for a_, b in zip(chapters, chapters[1:])), chapters
fmt = lambda f: f"{int(f / fps) // 60}:{int(f / fps) % 60:02d}"
CH = '\n'.join(f"{fmt(st)} {h}" for st, h in zip(starts, heads))

FIRST2 = ["코스피가 2026년 들어 하루에 5% 넘게 빠진 날은 24번이에요. 2026년 1월 2일~11월 20일 매일 마감 가격 기준(전날 마감 대비 하루 5% 넘게 빠진 날을 셈).",
          "1995년부터 작년까지 31년을 다 더하면 57번, IMF 외환위기 때도 한 해 9번이었어요. 코스피지수 8천 일 넘는 기록으로 크게 빠진 날 그 뒤 1년, 전날 값을 되찾기까지 걸린 날, 서킷브레이커가 걸린 날과 종가로 크게 빠진 날의 차이를 셌습니다."]
tpl = '\n'.join(FIRST2) + '''

크게 빠진 열다섯 번 전체 표(카페): {CAFE}
파이어맵: https://firemap.kr/?utm_source=youtube&utm_medium=description&utm_campaign=kospi-1
직접 보기: 한국은행 경제통계시스템(ECOS) https://ecos.bok.or.kr → 통계검색 → 802Y001 주식시장(일) → KOSPI 지수

{CHAPTERS}

출처
· 코스피 일별 종가(1995-01-03~2026-11-19): 한국은행 경제통계시스템 ECOS 802Y001 · 2026-11-20 종가 4,869.96(-5.21%)은 ECOS 공표 전이라 보도로 확인(이투데이 https://www.etoday.co.kr/news/view/2651045 · 서울경제 https://m.sedaily.com/article/20117003)
· 서킷브레이커(지수 8%·15%·20%)·사이드카(코스피200 선물 5%) 기준: 뉴시스 https://www.newsis.com/view/NISX20260306_0003538163 · 한경 생글 https://sgsg.hankyung.com/article/2022072222051
· 2026-11-06 서킷브레이커 '올해 11번째·역대 17번째'(보도 기준): 아시아경제 https://www.asiae.co.kr/article/2026110610032663847 · 경향신문 https://www.khan.co.kr/article/202611060908001
{STOCK}
계산 가정: 하루 = 전날 마감 대비 그날 마감 · 횟수를 센 것이지 위기 크기를 잰 게 아님 · 지수만 계산(ETF·펀드 보수, 배당, 세금은 빠짐)

내레이션은 AI 음성 내레이션(Google Cloud Text-to-Speech Chirp 3 HD)이에요. 숫자는 모두 위 원문에서 가져와 파이어맵이 계산했습니다. 지난 값이고, 앞으로를 예측하거나 사고팔라는 뜻이 아닙니다.'''
credits = list(dict.fromkeys(c['desc_line'] for c in json.load(open(os.path.join(EP, 'bg_used.json'), encoding='utf-8'))))
cafe = m.get('cafe_url') or 'https://cafe.naver.com/firemap'
desc = tpl.replace('{CAFE}', cafe).replace('{CHAPTERS}', CH).replace('{STOCK}', '\n'.join(credits))
m.update({
    'ep': 'KOSPI-1', 'series': '지수 — 코스피 지난 기록',
    'title': TITLES[0], 'title_by': 'firemap-copywriter 2026-11-20 18:54 copy/kospi1/final.txt 1위 T8(23→24 고침)', 'title_candidates': TITLES,
    'thumb_text_top': '코스피 5% 넘게 빠진 날', 'thumb_text': '2026년 들어 24번',
    'thumb': THUMB,
    'thumb_status': "11/20 PD: visual k1_p1 자리. copywriter 4차(11/20 18:54) 주제 3/3 통과·권유 반려(좁게, 노트북 화면 꺾이는 선) → visual p2(화면 흐림) → thumbpair → youtube-loop 고름. 바뀌면 kospi1meta.py THUMB 고치고 ytlong thumb",
    'desc_first2': FIRST2, 'desc_first2_src': 'copywriter titles.md 설명 첫 줄(11/20) + script 0장(57번·IMF 9번) · analysis ② 검색어 코스피·코스피지수·서킷브레이커',
    'tags': ['코스피', '코스피지수', '코스피 폭락', '서킷브레이커', '사이드카'],
    'desc_tpl': tpl, 'desc': desc, 'chapter_titles': heads, 'chapters': chapters,
    'chapters_note': f'video/kospi1.json 장 카드 시작 프레임(11/20 PD kospi1meta.py) — props 길이 {round(a / fps, 1)}초',
    'cafe_first': "대본 8장 '열다섯 번 전체 표는 파이어맵 카페에' → 카페 짝 글을 공개 같은 날 영상보다 먼저(11/24 아침 칸) — write·회의가 칸 배정",
    'voice': f"Chirp 3 HD Charon {V.get('speakingRate')} · {V.get('done')}줄 · {V.get('seconds')}초 · 11/20 7줄(24번) 다시 받기(editor 1d877fc7)",
    'missing': V.get('missing', 0),
    'publishAt': '2026-11-24T11:30:00+09:00', 'privacy': 'private', 'privacy_note': '예약 공개(private+publishAt) — 정해진 시각에 공개로 바뀜',
    'paid': False, 'coupang': None, 'synthetic': True, 'veo': False,
    'synthetic_note': 'AI 음성 내레이션 → containsSyntheticMedia True. AI 생성 그림 없음(판은 ECOS 값으로 그림, 실사는 Pexels)',
    'answers': {
        'q1_바꿔끼우기': "아니오 — ECOS 일별 종가 8천 일 넘게로 '올해 24번 vs 31년 합 57번'·크게 빠진 열다섯 번의 1년 뒤·전날 값 되찾기까지를 직접 셌다(calc2·3·4). 경쟁 10편 중 31년 일별 값 전부로 센 편 0(toc_compare).",
        'q2_연달아보기': '예 — 앞 편 11/22 H-5(부동산 송도)와 축이 다르고(지수), 뒤 11/28 SQ-1(배당ETF)과도 다름. 같은 축 연속 0(slot1124_compare ③).',
        'q3_약속이행': "예 — 제목 '24번, IMF 때보다 많았다'는 0장 3·7행에서 바로 답하고(24번·IMF 9번), 1~6장이 그 뒤를 채운다.",
        'q4_조언으로들리나': "아니오 — '예측은 안 해요'(0장)·끝 자막 '지난 값이며 매수·매도 권유가 아닙니다'. 할 일은 산 날과 오늘 코스피를 같이 적어 보기(기록 비교)뿐.",
        'q5_사람의몫': "예 — '서킷브레이커 걸린 날 ≠ 종가로 크게 빠진 날'(11/6 장중 -8.55%·종가 -6.02%)과 '지수 ≠ 내 계좌'(보수·배당·세금)는 흔한 말을 원자료로 가른 우리 판단."},
    'endscreen': {'how': 'Studio 최종 화면 — 업로드 뒤', 'status': '미정'},
    'made_by': 'firemap-video-producer', 'made_at': '2026-11-20',
    'video': os.path.join(VID, 'out', 'kospi1_dsl.mp4').replace('\\', '/'),
    'todo': '11/20 PD: 렌더·쉿소리·음량 끝 · 남은 것: 썸네일 p1/p2(youtube-loop) · 11/23 아침 ECOS 다시 셈(24 바뀌면 다시) · cafe_url · 최종 화면'})
json.dump(m, open(MP, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
open(os.path.join(EP, 'desc_1120.txt'), 'w', encoding='utf-8').write(m['title'] + '\n\n' + desc + '\n')
print(CH); print(f'설명 {len(desc)}자 · 실사 출처 {len(credits)}줄 · missing {m["missing"]} · 제목 {len(m["title"])}자')
