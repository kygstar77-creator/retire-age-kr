# CC-1 meta.json — video/cc1.json(장 카드 시작)·voice.json·bg_used.json(실사 출처) → meta.json + desc_1128.txt(editor 설명란 서명용)
#   py -3.12 work/research/longform/ep/CC-1/cc1meta.py   (cc1props.py 다음에, 장 카드 글·녹음·숫자가 바뀌면 다시)
# 11/28 02:4x PD: SQ-1 sq1meta.py 꼴.
#   제목 = copywriter copy/cc1/titles.md 'C-36 다시 고름' 1위 #1(결론 숫자 없음 C-36·조건 꼴 C-38·상품 이름 맨 앞 C-30)
#   썸네일 = thumb_cc1_b1.png(visual 11/26 09:22 bright1126 — e2 문구 그대로·밝기만, 짝 비교 2:0 · e2 1초 시험 통과 copywriter 11/24 18:58)
#   설명 첫 두 줄 = research.md 대조 표·cc1_calc_out_1122 값(11/20 종가 기준 — copywriter 조건 '설명 첫 줄 11/20 종가 기준')
#   장 카드 글(heads)은 cc1.json에서 읽는다 — visual이 장 카드를 다시 만들어 글이 바뀌면 이 스크립트를 다시 돌린다
import json, os, sys
sys.stdout.reconfigure(encoding='utf-8')
EP = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(EP, '..', '..', '..', '..', '..'))
VID = os.path.join(ROOT, 'work', 'video')
P = json.load(open(os.path.join(VID, 'cc1.json'), encoding='utf-8'))
V = json.load(open(os.path.join(EP, 'voice.json'), encoding='utf-8'))
MP = os.path.join(EP, 'meta.json')
m = json.load(open(MP, encoding='utf-8')) if os.path.exists(MP) else {}
TITLES = ['KODEX 미국배당커버드콜액티브, 1년 전 1억 넣었다면 지금 얼마 남았을까',
          'KODEX 미국배당커버드콜액티브와 TIGER 미국배당다우존스, 1억씩 넣고 1년 뒤 남은 돈을 비교했다']
THUMB = os.path.join(EP, 'thumb_cc1_b1.png')
THUMB_TOP, THUMB_TEXT = '', '같은 1억, 배당 ETF 둘 / 1년 뒤 누가 더 남았나?'

heads = ['여는 말']
starts, a = [0], 0
for s in P['scenes']:
    d = s.get('data') or {}
    if s['kind'] == 'ask' and str(d.get('n', '')).endswith('장'): starts.append(a); heads.append(d.get('head') or d['q'])
    a += s['frames']
fps = P.get('fps', 30)
assert len(starts) == len(heads) == 9, (len(starts), len(heads))
chapters = [[round(st / fps), h] for st, h in zip(starts, heads)]
assert all(b[0] - a_[0] >= 10 for a_, b in zip(chapters, chapters[1:])), chapters
fmt = lambda f: f"{int(f / fps) // 60}:{int(f / fps) % 60:02d}"
CH = '\n'.join(f"{fmt(st)} {h}" for st, h in zip(starts, heads))

# 값: cc1_calc_out_1122(5·9행 1년, 3·7행 2023-06-20부터)·research.md 대조 표('1년 끝날별 앞선 쪽' 2025-12-05 +15.7% vs +2.6%)
FIRST2 = ["2025년 11월 20일 같은 날 KODEX 미국배당커버드콜액티브와 TIGER 미국배당다우존스에 1억씩 넣고 분배금을 받아 썼다면(분배금 15.4% 뗌), 2026년 11월 20일 종가 기준 남은 돈은 9,654만원과 1억 1,793만원이었어요. 받은 분배금은 커버드콜이 793만원, 일반형이 294만원이었고요.",
          "TIGER가 상장한 2023년 6월 20일부터 세면 1억 4,524만원과 1억 5,783만원이었고, 1년을 2025년 12월 5일에서 끝나게 자르면 커버드콜이 앞섰어요. 끝날을 어디로 잡느냐에 따라 답이 달라지는 것까지 삼성·미래에셋자산운용 원문과 세법으로 셌습니다."]
DIS = '특정 상품을 사거나 팔라는 뜻이 아닙니다. 지난 값과 공개된 세법만 정리했고, 지난 값은 앞날을 말해 주지 않습니다.'
tpl = '\n'.join(FIRST2) + '\n' + DIS + '''

끝날별·기간별 전체 표(1년·2023-06-20부터·상장일부터, 받아 씀·다시 넣음)(카페): {CAFE}
파이어맵 배당 계산기: https://firemap.kr/dividend?utm_source=youtube&utm_medium=description&utm_campaign=cc-1

{CHAPTERS}

출처
· KODEX 미국배당커버드콜액티브(441640) 분배 이력 50건·종가·총보수 연 0.190%·분배 과세 문구: 삼성자산운용 https://m.samsungfund.com/etf/product/view.do?id=2ETFH4 (2026-11-22 확인)
· TIGER 미국배당다우존스(458730) 분배금 현황·종가·총보수 연 0.01%: 미래에셋자산운용 https://investments.miraeasset.com/tigeretf/ko/product/search/detail/index.do?ksdFund=KR7458730008 (2026-11-21 확인)
· 일별 종가·분배 기록 대조(2차): 야후 파이낸스 441640.KS·458730.KS, 네이버 금융 일별 시세
· 국내 상장 해외 ETF 분배금 = 배당소득, 원천징수 14%+지방 1.4%: 소득세법 제17조·제129조, 시행령 제26조의2, 지방세법 제103조의13 https://www.law.go.kr/법령/소득세법/제129조
· 금융소득 연 2,000만원 넘으면 종합과세: 소득세법 제14조·제62조 https://www.law.go.kr/법령/소득세법/제14조
{STOCK}
계산 가정: 각 기간 첫날 종가로 1억어치 사고 끝날(2026-11-20) 종가로 셈 · 분배금은 15.4% 떼고 받아 씀(다시 넣음은 받은 날 종가로 다시 삼) · 수수료 뺌 안 함 · 일반 계좌 기준, ISA·IRP는 계산 밖

내레이션은 AI 음성 내레이션(Google Cloud Text-to-Speech Chirp 3 HD)이에요. 숫자는 모두 위 원문에서 가져와 파이어맵이 계산했습니다.'''
credits = list(dict.fromkeys(c['desc_line'] for c in json.load(open(os.path.join(EP, 'bg_used.json'), encoding='utf-8'))))
cafe = m.get('cafe_url') or 'https://cafe.naver.com/firemap'
desc = tpl.replace('{CAFE}', cafe).replace('{CHAPTERS}', CH).replace('{STOCK}', '\n'.join(credits))
m.update({
    'ep': 'CC-1', 'series': '배당ETF — 커버드콜',
    'title': TITLES[0], 'title_by': "copywriter copy/cc1/titles.md 'C-36 다시 고름'(11/24 08:10) 1위 #1 · 결론 숫자 없음 C-36 · 대본 첫 문장과 같은 질문", 'title_candidates': TITLES,
    'thumb_text_top': THUMB_TOP, 'thumb_text': THUMB_TEXT, 'thumb': THUMB,
    'thumb_status': '11/26 09:22 visual cc1_b1(e2 문구 그대로·밝기만) 짝 비교 2:0 · e2 1초 시험 통과(copywriter 11/24 18:58) · C-39 경쟁 1위 yGuybuoroRI 대비 2/2(visual 11/24 17:20) · 11/26 07:59 copywriter 지금 판 유지',
    'desc_first2': FIRST2, 'desc_first2_src': "cc1_calc_out_1122 3·5·7·9행 · research.md 대조 '1년 끝날별 앞선 쪽'(2025-12-05) · 11/28 00:47 올리기 전 확인 바뀐 것 없음",
    'tags': ['KODEX 미국배당커버드콜액티브', 'TIGER 미국배당다우존스', '커버드콜 ETF', '배당 ETF', '미국 배당 ETF'],
    'desc_tpl': tpl, 'desc': desc, 'chapter_titles': heads, 'chapters': chapters,
    'chapters_note': f'video/cc1.json 장 카드 시작 프레임(11/28 PD cc1meta.py) — props 길이 {round(a / fps, 1)}초',
    'voice': f"Chirp 3 HD Charon {V.get('speakingRate')} · {V.get('done')}줄 · {V.get('seconds')}초",
    'missing': V.get('missing', 0),
    'publishAt': '2026-11-30T11:30:00+09:00', 'privacy': 'private', 'privacy_note': '예약 공개(private+publishAt) — 정해진 시각에 공개로 바뀜',
    'paid': False, 'coupang': None, 'synthetic': True, 'veo': False,
    'synthetic_note': 'AI 음성 내레이션 → containsSyntheticMedia True. AI 생성 그림 없음(판은 calc 값으로 그림, 실사는 Pexels)',
    'answers': {
        'q1_바꿔끼우기': "아니오 — 삼성 분배 이력 50건·미래에셋 분배 현황·일별 종가로 같은 날 1억 두 상품을 1년·2023-06-20부터·상장일부터 직접 셌고(cc1_calc), 끝날 여러 날로 잘라 앞선 쪽이 뒤집히는 것까지 셈(cc1_windows). 경쟁 16편 중 국내 상장 커버드콜 1억의 남은 돈을 세후 원으로, 일반형과 나란히 낸 편 0(research.md 경쟁).",
        'q2_연달아보기': '예 — 앞 편 11/28 SQ-1(나스닥100+SCHD 섞기)과 이틀 띄움, 질문이 다름(커버드콜 vs 일반형 남은 돈). 뒤 편 12/1 NDG-1(부동산).',
        'q3_약속이행': "예 — 제목 '1년 전 1억 넣었다면 지금 얼마 남았을까'는 0장·2장이 9,654만원으로 바로 답하고, 썸네일 '1년 뒤 누가 더 남았나?'는 2장 막대 둘(9,654만 vs 1억 1,793만)이 답한다.",
        'q4_조언으로들리나': "아니오 — 7장 '한 장면일 뿐'·끝날 따라 뒤집힘을 보여 줌 · 상품군 일반화 피함(상품 이름으로만 말함) · 끝 자막 '계산·비교 자료이며 매수·매도 권유가 아닙니다'·설명 면책 줄.",
        'q5_사람의몫': "예 — '분배금을 2.7배 받고도 1년 남은 돈은 적었다'·'끝날로 잡은 날이 마침 1년 중 가장 낮던 날'·'다시 넣은 쪽이 오히려 덜 남은 해도 있었다'는 원자료로 갈라 낸 우리 판단."},
    'endscreen': {'how': 'Studio 최종 화면 — 업로드 뒤', 'status': '미정 — link-plan-1125.md 짝 표대로(채팅 세션 몫)'},
    'made_by': 'firemap-video-producer', 'made_at': '2026-11-28',
    'video': os.path.join(VID, 'out', 'cc1_dsl1128.mp4').replace('\\', '/'),
    'click_ok': [],
    'todo': '11/28 02:4x PD: meta 첫 판 — 남은 것 visual 장 카드 7장 다시 만들기(shot_check 못함 7·파일 8, 11/28 12:00) → editor screen_text 재서명 → cc1props → 3토막 통렌더 → screen·bgcheck·눈 검사·scorecard·bench → cafe_url → gate·예약 11/30 11:30(관문 11/29 11:30) · 재생목록(배당) 공개 뒤'})
json.dump(m, open(MP, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
open(os.path.join(EP, 'desc_1128.txt'), 'w', encoding='utf-8').write(m['title'] + '\n\n' + desc + '\n')
print(CH); print(f'설명 {len(desc)}자 · 실사 출처 {len(credits)}줄 · missing {m["missing"]} · 제목 {len(m["title"])}자')
