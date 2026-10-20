# H-3 meta.json — h3.json(장면 시각)·bg_used.json(실사 출처)·copy/titles.md(제목) → meta.json
#   py -3.12 work/research/longform/ep/H-3/h3meta.py   (h3props.py 다음에 · 다시 녹음·렌더 뒤 챕터 시각이 바뀌면 다시)
# 10/21 PD: 챕터 이름 = script.md 장 머리(shot_plan '장' 칸과 같음, shot_check) · 썸네일은 visual 새 꼴 나오면 thumb 칸만 채움
import json, os, re, sys
sys.stdout.reconfigure(encoding='utf-8')
EP = os.path.dirname(os.path.abspath(__file__))
VID = os.path.normpath(os.path.join(EP, '..', '..', '..', '..', 'video'))
P = json.load(open(os.path.join(VID, 'h3.json'), encoding='utf-8'))
MP = os.path.join(EP, 'meta.json')
old = json.load(open(MP, encoding='utf-8')) if os.path.exists(MP) else {}
heads = [re.sub(r'^\[?(\d+\.|기초\])\s*|\]$', '', h).strip() for h in re.findall(r'^## (.+)$', open(os.path.join(EP, 'script.md'), encoding='utf-8').read(), re.M)]
heads = [h.replace('[0. ', '').strip('[] ') for h in heads]
# 장 시작 = 장 카드(ask n이 '기초'·'N장') · 정리는 board_summary 장면 · 처음은 0
starts, a = [0], 0
for s in P['scenes']:
    n = s['data'].get('n', '') if s['kind'] == 'ask' else ''
    if n == '기초' or re.match(r'^\d+장$', n) or (s['kind'] == 'pic' and s['data'].get('pic', '').endswith('board_summary.png')): starts.append(a)
    a += s['frames']
assert len(starts) == len(heads) == 14, (len(starts), len(heads), heads)
fmt = lambda f: f"{int(f / 30) // 60}:{int(f / 30) % 60:02d}"
chapters = [[round(st / 30), h] for st, h in zip(starts, heads)]
assert all(b[0] - a_[0] >= 10 for a_, b in zip(chapters, chapters[1:])), chapters
CH = '\n'.join(f"{fmt(st)} {h}" for st, h in zip(starts, heads))
credits = [c['desc_line'] for c in json.load(open(os.path.join(EP, 'bg_used.json'), encoding='utf-8'))['clips']]
TITLE = '압구정현대아파트가 있는 압구정동, 1년간 30억 안팎 거래 0건… 같은 돈이면 신천동·목동신시가지는 몇 ㎡'
TITLE2 = '압구정현대아파트 동네는 30억 안팎 거래 0건, 같은 돈이면 신천동·목동신시가지는 몇 ㎡'
FIRST2 = ['국토교통부 실거래 최근 1년(2025.11~2026.10 계약) 가운데 27억~33억에 팔린 아파트를 동네마다 세어 봤습니다. 송파 신천동은 175건(집 안 넓이 중앙 85㎡), 목동신시가지 1~7단지는 67건(96㎡), 강남 압구정동은 0건이었습니다.',
          '압구정동은 가장 싼 거래도 35억 7천만원(직거래 1건)이었고, 40억 안팎으로 올려도 집 안 넓이 중앙 50㎡였습니다(국토교통부 실거래 · 사거나 팔라는 뜻 아님).']
TPL = '\n'.join(FIRST2) + '''

세 동네 단지별 1년 거래 표(목동신시가지 1~14단지·압구정 현대·신천 장미·파크리오, 카페): {CAFE}
지난 편 · 잠실·대치·반포 84㎡ 1년 실거래: https://youtu.be/_fTgGr0dR0I

{CHAPTERS}

출처
· 국토교통부 아파트 매매·전월세 실거래(공공데이터포털, 2025.11~2026.10 계약, 2026-10-16 받음, 해제·공공기관 매수 제외 — 2026년 10월 거래는 신고 기한 30일이라 덜 들어옴)
· 건축물대장 총괄표제부 세대수(2026-10-17 조회)
· 국토교통부공고 제2025-1219호(토지거래허가구역)·제2025-1223호(조정대상지역)·제2025-1225호(투기과열지구) · 국토교통부 토지거래허가구역 업무처리기준(2025-04-21) · 금융위원회 「대출수요 관리 강화 방안」 FAQ(2025-10-15)
· 부동산 거래신고 등에 관한 법률 §11·시행령 §14·§14의2 · 도시 및 주거환경정비법 §39·§73·시행령 §37 · 소득세법 §89·§104·시행령 §154·§155 · 지방세법 §11·§13의2·시행령 §28의5(법제처, 2026-10-18~19 확인)
· 서울시 정비사업 정보몽땅 추진경과(2026-10-19 확인) · 서울특별시교육청 공고 제2026-157호
· 지도 자료 © OpenStreetMap 기여자(ODbL)
계산 가정: 30억 안팎 = 27억~33억 거래 · 넓이 = 전용면적(집 안 넓이, 1평 = 3.3058㎡) · 중간 가격·중간 크기 = 중앙값 · 평당 = 거래금액 ÷ (전용면적 ÷ 3.3058) · 전세 = 월세 없는 전세(신규·갱신 따로) · 전세가율 = 신규 전세 중앙 ÷ 매매 중앙 · 목동 = 법정동 목동(신시가지 1~7단지), 8~14단지는 신정동.

내레이션은 AI 음성 내레이션(Google Cloud Text-to-Speech Chirp 3 HD)이고, 일부 장면은 AI로 만든 그림(RealVisXL V5.0, 특정 단지 아님)입니다. 숫자는 모두 위 원문에서 가져와 파이어맵이 계산했습니다. 계산·비교 자료이며 어떤 집을 사거나 팔라는 권유가 아닙니다.
''' + '\n'.join(credits)
cafe = old.get('cafe_url') or 'https://cafe.naver.com/firemap'
m = dict(old)
m.update({
    'ep': 'H-3', 'series': 'C 부동산 — 대신 둘러봐 드립니다(손품 3화)',
    'title': TITLE, 'title_by': 'firemap-copywriter 2026-10-19 18:59 copy/titles.md 끝(1위 고침 — 레드팀 8.2·40·50·60세 2차 뜻 맞음)',
    'title_candidates': [TITLE, TITLE2],
    'thumb_text': old.get('thumb_text') or '신천 85㎡ vs 목동신시가지 96㎡', 'thumb_text_top': old.get('thumb_text_top') or '30억 안팎에 팔린 집 크기',
    'thumb_text_small': old.get('thumb_text_small') or '압구정동은 가장 싼 거래도 35억 넘어',
    'thumb': old.get('thumb'), 'thumb_status': old.get('thumb_status') or '10/21 PD: 새 꼴(N-2 thumb_A) 썸네일 visual 요청(시한 10/21 18:00) — 그림 시험 뒤 채움',
    'desc_first2': FIRST2, 'desc_tpl': TPL, 'desc': TPL.replace('{CAFE}', cafe).replace('{CHAPTERS}', CH), 'chapters': chapters,
    'tags': ['압구정현대아파트', '목동신시가지', '파크리오', '아파트 실거래가', '토지거래허가구역'],
    'publishAt': '2026-10-23T11:30:00+09:00', 'privacy': 'private', 'privacy_note': '예약 공개(private+publishAt) — 정해진 시각에 공개로 바뀜',
    'paid': False, 'coupang': None, 'synthetic': True, 'veo': False,
    'synthetic_note': 'AI 생성 그림 5장(RealVisXL V5.0 — 오래된 단지 2·열쇠·등교 뒷모습·창가 실루엣, 얼굴·상표 없음) + AI 음성 → containsSyntheticMedia True',
    'voice': 'Chirp 3 HD Charon 1.1 · 260줄 · 2026-10-21 한 날 녹음(say_v4, editor 10/19 17:08 서명)',
    'answers': {
        'q1_바꿔끼우기': "아니오 — H-1·H-2와 같은 손품 실거래 틀이지만 질문이 '같은 30억이면 몇 ㎡'로 다르다. 압구정 0건·신천 85㎡·목동신시가지 1~7단지 96㎡, 목동 번호가 7단지에서 주소가 갈린다는 것, 1년에 백 집 중 두 집도 안 팔렸다는 건수는 이 세 동네 자료에서만 나온 숫자다.",
        'q2_연달아보기': '아니오 — 앞 두 편(T-1 양도세·X-1 환율)과 축이 다르고(부동산), 손품은 화·금 칸이라 H-2(10/20)와 사흘 간격, 다음 편 J-1(종부세)과 축이 다르다.',
        'q3_약속이행': "예 — 제목 '압구정동 1년간 30억 안팎 거래 0건'은 4장 첫 줄(0건·가장 싼 거래 35.70억 직거래)이, '같은 돈이면 신천동·목동신시가지는 몇 ㎡'는 0장·2장(85㎡ 175건)·3장(96㎡ 67건)이 답하고 12장 정리에서 다시 말한다.",
        'q4_조언으로들리나': "아니오 — 사라·팔라·전망·대장주·재건축 전망·분담금 0, 3장 '어디가 낫다고는 말씀드리지 않을게요', 차이 이유는 '실거래 자료에 나오지 않습니다', 허가·대출·세금은 원문 규칙만.",
        'q5_사람의몫': "예 — 경쟁이 평당 가격으로 줄 세울 때 '같은 돈이면 몇 ㎡'로 바꿔 보고(5장 평당 착시를 숫자로 보임), 세대수 대비 1년 거래 비율을 처음 셌다(경쟁 9편 0편).",
    },
    'experiment': {'X-RE-LONG': '손품 3화 — 금요일 칸, H-1·H-2 첫날 노출과 견줌'},
    'endscreen': {'how': 'Studio 최종 화면 — 업로드 뒤 할 일(지난 편 H-2 _fTgGr0dR0I)', 'status': '미정'},
    'made_by': 'firemap-video-producer', 'made_at': old.get('made_at') or '2026-10-21',
    'video': os.path.join(VID, 'out', 'h3_ds.mp4'), 'missing': 0,
})
json.dump(m, open(MP, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('meta.json · 제목', len(TITLE), '자 · 챕터', len(chapters), '· 설명', len(m['desc']), '자 · 실사 출처', len(credits))
print(CH)
