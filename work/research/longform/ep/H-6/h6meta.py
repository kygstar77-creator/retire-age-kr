# H-6 meta.json — video/h6.json(장 카드 시작)·voice.json·bg_used.json(실사 출처) → meta.json + desc_1123.txt(editor 설명란 서명용)
#   py -3.12 work/research/longform/ep/H-6/h6meta.py   (h6props.py 다음에, 녹음·말·숫자가 바뀌면 다시)
# 11/23 02시 PD: KOSPI-1 kospi1meta.py 꼴.
#   제목 = copywriter copy/h6/titles.md 11/22 18:55 1위 #12 · 설명 첫 줄 = 같은 파일 '가운데 값으로 다시' 설명 첫 줄 · 면책 줄 = 같은 파일 '설명란 면책 줄'
#   썸네일 = thumb_h6_a2.png 자리 — copywriter 3차(visual a3·a4 thumbpair 이긴 판, 관문 11/25 11:30) 뒤 THUMB·THUMB_TEXT만 고치고 다시
#   11/25 올리기 전 확인(youtube-loop)에서 75건·31평 31.45억·11월 막대가 바뀌면 FIRST2도 같이 고침
import json, os, sys
sys.stdout.reconfigure(encoding='utf-8')
EP = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(EP, '..', '..', '..', '..', '..'))
VID = os.path.join(ROOT, 'work', 'video')
P = json.load(open(os.path.join(VID, 'h6.json'), encoding='utf-8'))
V = json.load(open(os.path.join(EP, 'voice.json'), encoding='utf-8'))
MP = os.path.join(EP, 'meta.json')
m = json.load(open(MP, encoding='utf-8')) if os.path.exists(MP) else {}
# 11/24 05:1x PD: youtube-loop 05:02 [지시] C-36(결론 숫자 금지)·C-38 — 제목·썸네일 글 = c36/decision.md 판(copywriter 11/24 18:00까지 말 없으면 확정)
#   옛 제목 '은마아파트 재건축 인가 났는데, 34평 실거래는 1년 새 8억 넘게 내렸다'(결론 숫자) · 옛 썸네일 a3 '은마 34평 42억 8천이 / 1년 뒤 34억 3천으로'
TITLES = ['은마아파트 34평, 1년 전에 샀다면 지금 얼마일까?']
THUMB = os.path.join(EP, 'thumb_h6_n3.png')   # 자리 — visual 새 판(11/24 18:00) 나오면 그 파일로. a3는 결론 숫자라 C-36에 걸려 그대로 올리지 않음
THUMB_TOP, THUMB_TEXT = '은마아파트 34평 · 국토부 실거래', '재건축 인가 났는데 / 34평 값은 어디로?'

heads = ['여는 말', '은마는 지금 어디까지', '1년 실거래, 평형별', '거래는 언제 몰렸나', '세 가지 숙제',
         '세입자 계약 신고', '누구라면', '함정과 직접 확인', '정리']   # script.md ## 제목
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

FIRST2 = ["국토부 실거래 기준 은마아파트 84㎡ 가운데 값 — 2025년 10~12월 계약 42.80억(3건) → 2026년 10~11월 계약 34.50억(10건), 해제 거래 뺌.",
          "하락의 거의 절반은 7월 사업시행인가 전에 이미 와 있었고, 9~10월 두 달에 1년 거래 76건 중 34건이 몰렸어요. 전세·월세 계약 신고, 분담금·재초환(조합원 평균 예정액 4억 6천만원, 감면 전)·이주까지 국토교통부·강남구·법제처 원문으로 정리했습니다."]
DIS = '은마아파트를 사거나 팔라는 뜻이 아닙니다. 지난 실거래 값과 공개된 제도만 정리했습니다.'
tpl = '\n'.join(FIRST2) + '\n' + DIS + '''

은마 1년 실거래 76건 전체 표(카페): {CAFE}
파이어맵: https://firemap.kr/?utm_source=youtube&utm_medium=description&utm_campaign=h-6
직접 보기: 국토교통부 실거래가 공개시스템 https://rt.molit.go.kr → 아파트 → 서울 강남구 대치동 은마 → 면적·기간

{CHAPTERS}

출처
· 매매 실거래: 국토교통부 아파트 매매 실거래 상세(공공데이터포털 RTMSDataSvcAptTradeDev, 강남구 2025.10~2026.11, 2026-11-19·11-22 받음, 해제 거래 뺌)
· 전월세 실거래: 국토교통부 아파트 전월세 실거래(RTMSDataSvcAptRent, 은마 896건, 2026-11-19 받음)
· 신고 기한: 부동산 거래신고 등에 관한 법률 제3조① https://www.law.go.kr/법령/부동산거래신고등에관한법률/제3조
· 사업시행계획인가 2026-07-02: 강남구 보도자료 https://www.gangnam.go.kr/board/B_000031/1075184/view.do · 강남구 고시 제2026-130호 https://news.seoul.go.kr/citybuild/archives/541084
· 재초환 예정액(총액·1인당 평균): 강남구 보도자료 https://www.gangnam.go.kr/board/B_000031/1075588/view.do · 머니투데이 https://www.mt.co.kr/article/2026110614422041034
· 재초환 부과율·감경·납부유예: 재건축초과이익 환수에 관한 법률 제8조·제12조·제14조의2·제17조의2 https://www.law.go.kr/법령/재건축초과이익환수에관한법률
· 분담금 보도: 중앙일보 https://v.daum.net/v/20260530070229266 · 비즈니스워치 https://news.bizwatch.co.kr/article/real_estate/2026/09/24/0002 (조합 공식 문서는 확인 못 함)
· 분양신청·현금청산: 도시 및 주거환경정비법 제72조·제73조 https://www.law.go.kr/법령/도시및주거환경정비법/제73조
{STOCK}
계산 가정: 가운데 값 = 그 기간 거래를 값 순서로 줄 세운 한가운데 값 · 계약일 기준 · 최근 두 달은 신고 기한(30일) 안이라 건수가 늘 수 있음

내레이션은 AI 음성 내레이션(Google Cloud Text-to-Speech Chirp 3 HD)이에요. 숫자는 모두 위 원문에서 가져와 파이어맵이 계산했습니다.'''
credits = list(dict.fromkeys(c['desc_line'] for c in json.load(open(os.path.join(EP, 'bg_used.json'), encoding='utf-8'))))
cafe = m.get('cafe_url') or 'https://cafe.naver.com/firemap'
desc = tpl.replace('{CAFE}', cafe).replace('{CHAPTERS}', CH).replace('{STOCK}', '\n'.join(credits))
m.update({
    'ep': 'H-6', 'series': '부동산 — 재건축 실거래',
    'title': TITLES[0], 'title_by': 'youtube-loop 2026-11-24 05:02 c36/decision.md(C-36·C-38) — copywriter 11/24 18:00 확인 대기', 'title_candidates': TITLES,
    'thumb_text_top': THUMB_TOP, 'thumb_text': THUMB_TEXT, 'thumb': THUMB,
    'thumb_status': '11/24 18:2x PD: h6_n3 (copywriter 15:14 1초 시험 통과, A101 상대 시점 없음, 제목과 통째 겹침 아님 C-26) — C-39 경쟁 짝 비교 c36/c39_n3_*',
    'desc_first2': FIRST2, 'desc_first2_src': 'copywriter titles.md 설명 첫 줄(11/20 18:55 가운데 값) + script 0·3·4·5장(인가 전 절반·34/76건·4억 6천 감면 전) · 11/25 PD: loop 올리기 전 확인 값(국토부 11/25 받음)으로',
    'tags': ['은마아파트', '은마아파트 재건축', '은마아파트 실거래가', '재초환', '대치동 아파트'],
    'desc_tpl': tpl, 'desc': desc, 'chapter_titles': heads, 'chapters': chapters,
    'chapters_note': f'video/h6.json 장 카드 시작 프레임(11/23 PD h6meta.py) — props 길이 {round(a / fps, 1)}초',
    'cafe_first': "대본 8장 '설명란에 링크한 파이어맵 카페 글에 76건 표' → 카페 짝 글을 공개 같은 날 영상보다 먼저(11/26 07:40·10:10 칸) — write·회의가 칸 배정",
    'voice': f"Chirp 3 HD Charon {V.get('speakingRate')} · {V.get('done')}줄 · {V.get('seconds')}초 · 11/22 93·114행 재녹음(editor df67b678)",
    'missing': V.get('missing', 0),
    'publishAt': '2026-11-26T11:30:00+09:00', 'privacy': 'private', 'privacy_note': '예약 공개(private+publishAt) — 정해진 시각에 공개로 바뀜',
    'paid': False, 'coupang': None, 'synthetic': True, 'veo': False,
    'synthetic_note': 'AI 음성 내레이션 → containsSyntheticMedia True. AI 생성 그림 없음(판은 국토부 값으로 그림, 실사는 Pexels)',
    'answers': {
        'q1_바꿔끼우기': "아니오 — 국토부 매매 76건·전월세 893건을 평형별·월별로 직접 세어 '가운데 값 −8억 3천, 그중 절반은 인가 전'·'9~10월 34건 몰림 vs 강남구 전체는 평균보다 적음'·'전월세 신고 162→20건'을 갈랐다(calc·calc2·calc3·gangnam_count_1125 — 11/25 다시 받음). 경쟁 5편 중 실거래 전부로 센 편 0(toc_compare).",
        'q2_연달아보기': '예 — 앞 편 11/24 KOSPI-1(지수)·뒤 편 11/28 SQ-1(배당ETF)과 축이 다름. 부동산 앞 편 H-5(송도)는 11/22로 이틀 사이에 지수 한 편.',
        'q3_약속이행': "예 — 제목 '1년 전에 샀다면 지금 얼마일까?'는 0장에서 바로 답(42.80→34.50억, 8억 3천 빠짐)하고, 썸네일 '재건축 인가 났는데 / 34평 값은 어디로?'는 0장 '하락의 거의 절반은 인가 전'과 2장 인가 선(48%)이 받친다.",
        'q4_조언으로들리나': "아니오 — 설명 면책 줄·끝 자막 '계산·비교 자료이며 매수·매도 권유가 아닙니다'. 할 일은 내 평형 가운데 값을 직접 세 보기·재초환 평균을 내 몫으로 읽지 않기(제도 확인)뿐. '지금 살 때냐'(Q6)는 답하지 않음.",
        'q5_사람의몫': "예 — '매물 5배 ≠ 팔린 건수'·'재초환 평균 4억 6천 ≠ 내 몫(보유기간 감경)'·'분담금 두 보도가 다름, 조합 문서 미확인'은 흔한 말을 원자료로 가른 우리 판단."},
    'endscreen': {'how': 'Studio 최종 화면 — 업로드 뒤', 'status': '미정'},
    'made_by': 'firemap-video-producer', 'made_at': '2026-11-23',
    'video': os.path.join(VID, 'out', 'h6_c37.mp4').replace('\\', '/'),   # 11/24 10:3x PD: h6_dsl1124.mp4 앞 119프레임(인사 장면, C-37) 잘라 냄·-17.0 LUFS 그대로 · 그 전 11/24 PD: 통렌더 h6.mp4 → deesser i=0.8:m=0.7 + loudnorm(-12.1dB·-17.0 LUFS)
    'click_ok': [189.4],   # 11/24 10:3x PD: 인사 3.97초 잘라 낸 뒤 193.4 → 189.4
    'click_ok_note': "11/24 05:2x PD: 193.4초 = scenes.30 '은마는 그 여섯 곳 중에서도 가장 많이 빠졌고요'의 '가장' 첫소리(쉼 뒤). 통렌더 h6.mp4엔 안 잡히고 음량 맞춤(×1.42) 뒤 잡힘 — 10ms rms 꼴 같음(788→3838 ↔ 1132→5447)·4kHz 위 0%. 제미나이 3.6-flash 1초 듣기 '가장 많이 빠졌고요 / 판정: 말소리'(check/click1934_gemini.log)",
    'todo': '11/25 PD 06:2x: 올리기 전 확인 값(76건·34.50억·23곳)으로 FIRST2·답·판 데이터 고침 · 남은 것: editor 재서명(말 9줄·화면 글자·설명란) → 9줄 녹음 → 그 토막 렌더 → screen·bgcheck·bench 대조 → cafe_url → gate·예약 11/26 11:30'})
json.dump(m, open(MP, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
open(os.path.join(EP, 'desc_1123.txt'), 'w', encoding='utf-8').write(m['title'] + '\n\n' + desc + '\n')
print(CH); print(f'설명 {len(desc)}자 · 실사 출처 {len(credits)}줄 · missing {m["missing"]} · 제목 {len(m["title"])}자')
