# D-ETF-1 meta.json — detf1.json(장면 시각)·bg_used.json(실사 출처)·copy/titles.md(제목) → meta.json
#   py -3.12 work/research/longform/ep/D-ETF-1/detfmeta.py   (de1props.py 다음에 · 다시 녹음·렌더 뒤 챕터 시각이 바뀌면 다시)
# 10/26 PD: j1meta.py 꼴. 챕터 이름 = script.md 장 머리 · 썸네일은 visual 2차 시험 뒤 thumb 칸만 채움
import json, os, re, sys
sys.stdout.reconfigure(encoding='utf-8')
EP = os.path.dirname(os.path.abspath(__file__))
VID = os.path.normpath(os.path.join(EP, '..', '..', '..', '..', 'video'))
P = json.load(open(os.path.join(VID, 'detf1.json'), encoding='utf-8'))
MP = os.path.join(EP, 'meta.json')
old = json.load(open(MP, encoding='utf-8')) if os.path.exists(MP) else {}
heads = [re.sub(r'^\[?\d+\.\s*', '', h).strip('[] ') for h in re.findall(r'^## (.+)$', open(os.path.join(EP, 'script.md'), encoding='utf-8').read(), re.M)]
starts, a = [0], 0
for s in P['scenes']:
    n = s['data'].get('n', '') if s['kind'] == 'ask' else ''
    if re.match(r'^\d+장$', n): starts.append(a)
    a += s['frames']
assert len(starts) == len(heads) == 7, (len(starts), len(heads), heads)
fmt = lambda f: f"{int(f / 30) // 60}:{int(f / 30) % 60:02d}"
chapters = [[round(st / 30), h] for st, h in zip(starts, heads)]
assert all(b[0] - a_[0] >= 10 for a_, b in zip(chapters, chapters[1:])), chapters
CH = '\n'.join(f"{fmt(st)} {h}" for st, h in zip(starts, heads))
credits = [c['desc_line'] for c in json.load(open(os.path.join(EP, 'bg_used.json'), encoding='utf-8'))]
TITLE = 'SCHD 배당금 느는 속도 꺾였다, 많이 주는 JEPI는 돈도 더 불었을까? JEPQ 등 배당 ETF 16개 비교'
TITLE_OLD = 'SCHD·JEPQ·JEPI 배당 ETF 16개, 많이 주는 ETF가 돈도 더 불었을까? 주가까지 합쳐 비교'  # 10/20 1위 — 10/27 이해 시험 1차 썸네일과 3/3 어긋남 → 짝 비교 2번 승리한 위 제목으로(copy/titles.md '10/27 짝 고침')
FIRST2 = ['SCHD 한 주당 배당금은 10년 평균 매년 10.8% 늘다 최근 12개월은 2.0% 느는 데 그쳤습니다. 많이 주는 JEPI는 지금 분배율 8%지만 배당을 다시 넣은 5년 총수익은 매년 7.5%로 S&P500(12.8%)보다 낮았고, HDV는 13.1%였습니다.',
          'SCHD·JEPQ·JEPI 등 배당 ETF 16개를 같은 잣대로 비교했습니다. SCHD 돈의 55%는 필수소비재·헬스케어·에너지 세 업종에 있었습니다(2026-10-15 보유 종목 합산).']
TPL = '\n'.join(FIRST2) + '''

ETF 16개 × 업종 12칸 히트맵·1억 넣으면 1년 통장 표(카페): {CAFE}

{CHAPTERS}

출처
· 운용사 보유 종목·섹터 표: 슈왑 SCHD(2026-10-15) · 아이셰어즈 HDV(2026-10-15) · 뱅가드 VIG·VYM(2026-09-30) · 아이셰어즈 DGRO · 스테이트스트리트 SPYD(2026-10-15) · JP모건 JEPI·JEPQ(2026-10-16) · 앰플리파이 DIVO(2026-09-30)
· 국내 ETF: 네이버 증권 ETF 분석(2026-10-16) · 운용사 구성종목(TIGER) · PLUS 팩트시트
· 가격·분배 이력: 야후 파이낸스(미국 2026-10-16 마감, 국내 2026-10-19)
· 한국은행 ECOS 원·달러 매매기준율(731Y001)
· 소득세법 제129조 · 국민건강보험법 시행규칙 제44조·제2조 별표 1의2(피부양자) · 한미 조세조약
계산 가정: 분배율 = 최근 12개월 1주당 분배금 합 ÷ 10/16 종가 · 총수익은 분배 재투자(달러) · 1억 계산은 최근 12개월 분배가 같다고 놓은 것(앞으로 같다는 뜻 아님)·가격·환율 변동 뺌 · 건보료는 지역가입자·다른 금융소득 0 가정 · 국내 상장 해외 ETF 세금은 15.4% 위쪽 경계(실제 세액은 운용사 과세표준 공시).
기준일: 영상 속 숫자는 2026-10-16 마감 기준입니다. 올리기 전 다시 확인(2026-10-27): 원·달러 매매기준율 10/26 1,324.3원(영상 1,348.5원) · SCHD 1년 총수익 달러 35.0%·원화 24.5%, TIGER 미국배당다우존스 23.0% · HDV는 10/21 분배를 더하면 최근 12개월 분배율 3.15%(영상 2.84%) · 나머지 분배율은 영상과 같습니다.

내레이션은 AI 음성 내레이션(Google Cloud Text-to-Speech Chirp 3 HD)입니다. 히트맵·점 그림·표는 위 원문 숫자로 파이어맵이 직접 만들었습니다. 계산·비교 자료이며 특정 ETF를 사거나 팔라는 권유가 아닙니다.
''' + '\n'.join(credits)
cafe = old.get('cafe_url') or 'https://cafe.naver.com/firemap'
m = dict(old)
m.update({
    'ep': 'D-ETF-1', 'series': '배당 ETF — 업종 히트맵',
    'title': TITLE, 'title_by': 'firemap-copywriter 2026-10-27 01:34 짝 고침(thumbpair title 2번 승, check/titlepair1027/n5) · 10/20 1위는 TITLE_OLD',
    'title_candidates': [TITLE, TITLE_OLD],
    'thumb_text_top': old.get('thumb_text_top') or 'SCHD 한 주당 받는 배당금 · 10년 평균 vs 최근 1년',
    'thumb_text': old.get('thumb_text') or '11%씩 늘던 배당금 / 최근엔 2%만 늘었다',
    'thumb': old.get('thumb') or '',
    'thumb_status': old.get('thumb_status') or "10/26 PD: copywriter 10/21 18:54 문구 2차 1위로 visual 새판·1초 시험·짝 비교·40·50·60세 그림 시험 남음(thumb_detf_d는 2차 3/3 오독)",
    'desc_first2': FIRST2, 'desc_tpl': TPL, 'desc': TPL.replace('{CAFE}', cafe).replace('{CHAPTERS}', CH), 'chapters': chapters,
    'tags': ['배당 ETF', 'SCHD', 'JEPI', 'JEPQ', '미국배당다우존스'],
    'publishAt': '2026-10-27T11:30:00+09:00', 'privacy': 'private', 'privacy_note': '예약 공개(private+publishAt) — 정해진 시각에 공개로 바뀜',
    'paid': False, 'coupang': None, 'synthetic': True, 'veo': False,
    'synthetic_note': 'AI 음성 내레이션(Chirp 3 HD) → containsSyntheticMedia True. AI 생성 그림 없음(실사는 Pexels, 그림은 자체 제작)',
    'voice': 'Chirp 3 HD Charon 1.1 · 105줄 · 2026-10-22 녹음(say_v1, editor 10/22 07:08 서명) · 끝 줄 10/26 요일 고침 다시 받기',
    'answers': {
        'q1_바꿔끼우기': '아니오 — 우리 W-1(배당주)·R-1(연금)과 다른 질문: ETF 16개를 같은 잣대(분배율·분배 성장·업종·낙폭·1억 통장)로 나란히 놓고, 보유 종목을 받아 업종을 직접 더한 히트맵은 경쟁 10편에 없다.',
        'q2_연달아보기': '아니오 — 앞 편 J-1(종부세 정책)·다음 편 K-1(국채금리 경제)과 축이 다르다(주식). 배당 축 W-3은 11/3로 일주일 띄움.',
        'q3_약속이행': "예 — 제목 앞 'SCHD 배당금 느는 속도 꺾였다'는 0:27(10년 평균 11% → 최근 1년 2%)·2장이, '많이 주는 JEPI는 돈도 더 불었을까'는 4장(JEPI 8% 주는데 5년 매년 7.5%, S&P500 12.8%, HDV 13.1%)이 답한다. JEPQ는 5년 총수익이 없어 질문 대상에서 뺐다.",
        'q4_조언으로들리나': "아니오 — 사라·팔라·추천·비율 섞기·전망 0, '고르는 순서'는 물어볼 질문 네 개만, 세금·건보료는 제도 설명과 조건 붙은 계산.",
        'q5_사람의몫': '예 — 운용사 원문 보유 종목을 업종별로 다시 더해(공식 섹터 표가 석 달 전일 때가 있어) SCHD 정보기술 9.2→12.2% 변화를 찾았고, DIVO 12월 튀는 분배를 빼면 4.32%라는 계산, 1억 JEPQ 건보료 함정 계산은 우리 몫이다.',
    },
    'experiment': {},
    'endscreen': {'how': 'Studio 최종 화면 — 업로드 뒤 할 일(다음 편 K-1 또는 W-1)', 'status': '미정'},
    'made_by': 'firemap-video-producer', 'made_at': old.get('made_at') or '2026-10-26',
    'video': os.path.join(VID, 'out', 'detf1_ds.mp4'), 'missing': 0,
})
json.dump(m, open(MP, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('meta.json · 제목', len(TITLE), '자 · 챕터', len(chapters), '· 설명', len(m['desc']), '자 · 실사 출처', len(credits))
print(CH)
