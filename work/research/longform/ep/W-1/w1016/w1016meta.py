# W-1 2화 meta.json — 제목·썸네일 문구는 copy/titles.md 1위 그대로, 설명 숫자는 calc_out.txt, 챕터 시각은 video/w1016.json 장면 시작에서.
#   py -3.12 work/research/longform/ep/W-1/w1016/w1016meta.py   (w1016props.py 다시 돈 뒤 다시 돌린다 — 챕터 시각이 따라 바뀜)
# 썸네일(thumb)·카페 짝 글 주소는 있는 값을 지우지 않는다(이미 meta.json에 있으면 그대로 둠).
import json, os, re, sys
sys.stdout.reconfigure(encoding='utf-8')
EP = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.normpath(os.path.join(EP, '..', '..', '..', '..', '..'))
CO = open(os.path.join(EP, 'calc_out.txt'), encoding='utf-8').read()
TT = open(os.path.join(EP, 'copy', 'titles.md'), encoding='utf-8').read()
P = json.load(open(os.path.join(WORK, 'video', 'w1016.json'), encoding='utf-8'))
old = json.load(open(os.path.join(EP, 'meta.json'), encoding='utf-8')) if os.path.exists(os.path.join(EP, 'meta.json')) else {}

title = re.search(r'- title: \*\*(.+?)\*\*', TT)[1]
cand2 = re.search(r'title_candidates: \[위 1위, "(.+?)"\]', TT)[1]
for s in ['262000', '232000', '263,823', '-11.45', '-12.06', '-9.31', '-931371', '-0.55', '-60786', '-3,992,157', '3.4', '34.2', '2.6', '[C2] 1년 상승률(%, 비계절조정) = 3.7']:
    assert s in CO, s

# 챕터: 장 첫 장면 시작 시각
starts, t = {}, 0
for s in P['scenes']:
    starts.setdefault(s['key'], t); t += s['frames']
fmt = lambda f: f'{int(f / 30) // 60}:{int(f / 30) % 60:02d}'
CH = [('open', '삼성전자 100주, 사흘에 300만원'), ('week', '코스피 사흘에 9%'), ('buy', '회사가 15조원에 산 자사주 평균값'), ('kbars', '코스피 1천만원'),
      ('cal', '미국 소비자물가 3.7%와 1만 달러'), ('trio', '셋을 나란히'), ('next', '다음 주에 볼 날짜')]
chap = [[starts[k] // 30, n] for k, n in CH]
gaps = [b[0] - a[0] for a, b in zip(chap, chap[1:])] + [t // 30 - chap[-1][0]]
assert chap[0][0] == 0 and min(gaps) >= 10, ('챕터 10초 미만', gaps)

CAFE = old.get('cafe_url') or 'https://cafe.naver.com/firemap'
desc = '\n'.join([
    '삼성전자 주가는 10월 8일 262,000원에서 수요일 10월 14일 232,000원으로 사흘 −11.45%, 100주 평가액은 300만원 줄었습니다. 회사가 8월 24일~10월 6일에 15조원어치 산 자사주 평균값(1주 263,823원, 수수료 제외)보다 12.06% 낮은 값이에요.',
    '회사가 산 값과 견줬을 뿐, 싸다는 뜻이나 바닥·매수 신호는 아니에요. 지나간 종가로 한 계산이고, 투자 권유가 아닙니다.',
    '',
    f'금요일 마감까지 넣은 표(카페): {CAFE}',
    '지난 편 · 1화 지난주 사흘: https://youtu.be/0yWQeW38UJE',
    '',
    '같은 사흘(10/8 → 10/14 수요일 마감) 코스피를 그대로 따라간 1천만원은 93만원(−931,371원, −9.31%) 줄었고, 미국 S&P500을 따라가는 ETF(SPY) 1만 달러는 달러로 −0.55%, 원화로 6만원 남짓(−60,786원) 줄었어요. 셋을 모두 들고 있었다면 합쳐서 399만원(−3,992,157원). 팔지 않았다면 확정된 손실은 아닙니다.',
    '미국 9월 소비자물가는 1년 전 같은 달보다 3.7%(8월 3.4%) 올랐고, 휘발유는 34.2%, 식품·에너지를 뺀 근원 물가는 2.6% 올랐습니다. 같은 날 SPY가 내린 것이 물가 발표 때문인지는 확인되지 않아요.',
    '목요일·금요일 장은 이 계산에 넣지 않았어요.',
    '',
    *[f'{fmt(c[0] * 30)} {c[1]}' for c in chap],
    '',
    '출처: DART 자기주식취득결과보고서(2026.10.12)·SK하이닉스 기업설명회 안내(2026.10.14) · 한국은행 ECOS(코스피·원달러 매매기준율) · 다음 금융(KRX 정규장 종가) · 야후 파이낸스(SPY 종가) · 미국 노동통계국(BLS)·FRED(CPI)',
    '이 영상은 AI 음성 내레이션(구글 Chirp 3 HD)으로 만들었습니다. 화면 숫자는 원문 자료 그대로예요.',
])
m = {**old,
     'ep': 'W-1-2', 'series': '주간 코너 · 이번 주 뉴스가 내 돈에 얼마 2화',
     'title': title, 'title_candidates': [title, cand2], 'title_by': 'firemap-copywriter 2026-10-15 07:56 copy/titles.md 1위(결선 8.47)',
     'thumb_text': '삼성전자 100주 · 월~수 / 300만원 줄었다', 'thumb_text_swap': '삼성전자 100주 / −300만원 / 월~수 사흘',
     'thumb': old.get('thumb', ''), 'desc': desc, 'chapters': chap,
     'tags': ['삼성전자 주가', '삼성전자 자사주', '코스피', '미국 소비자물가', '이번 주 증시'],
     'publishAt': '2026-10-17T11:30:00+09:00', 'privacy': 'private', 'privacy_note': 'private + publishAt 예약(공개 시각에 public)',
     'paid': False, 'coupang': False, 'veo': False,
     'synthetic': True, 'synthetic_why': 'AI 목소리(Chirp 3 HD) 편은 전부 켬 — 10/12 회의 결정(R-1·W-1·G-1과 같은 기준), 실사 생성 장면 0',
     'voice': 'Chirp 3 HD Charon 1.1 + 쉼 태그(markup) · 36줄 · 10/15 하루 · 앞뒤 −6.0%·IQR 0.12',
     'video': os.path.join(WORK, 'video', 'out', 'w1016_ds.mp4'), 'missing': 0,
     'answers': {
         'q1_바꿔끼우기': '아니오 — 1화와 같은 짜임(세 칸 내 돈)이지만 이번 주에만 있는 원문으로 짰다: DART 자기주식취득결과보고서 29일 하루 평균단가 대 수요일 종가, 미국 9월 CPI 부문, 1화부터 두 주 누적.',
         'q2_연달아보기': '아니오 — 전날(10/16) P-1은 연금·정책, 다음 날(10/18) N-2는 소득 통계라 축이 다르다(이번 편은 주식·경제). 화면 그림 14가지(점 줄기·다리 막대·달력·작은 선 등).',
         'q3_약속이행': '예 — 제목 "수요일 종가, 회사가 15조원에 산 자사주 평균값보다 12% 낮았다"는 0:10 대본 줄과 2장 점 29개 그림이 답하고, 썸네일 300만원은 첫 줄 숫자다.',
         'q4_조언으로들리나': "아니오 — '싸다·사라·기회' 0, '싸다는 뜻은 아니에요'·'투자 권유도 아니에요' 말과 설명 둘째 줄, 원인 단정 0('물가 발표 때문이라고는 말할 수 없습니다').",
         'q5_사람이봐도': '예 — 숫자마다 출처 칩(DART·ECOS·BLS·KRX), 정확한 값은 화면, 말은 반올림, 처음 보는 58세 이해 시험 8장 뜻 맞음(understand_test.md).'},
     'experiment': {'X-W1-SEARCHFRONT': "제목 맨 앞 '삼성전자 주가'", 'X-VOICE-MARKUP': 'Chirp 쉼 태그 첫 적용(10/12 지시)'},
     'pinned_comment': '', 'endscreen': {'how': 'Studio 최종 화면 — 1화 0yWQeW38UJE', 'status': '미정'},
     'made_by': 'firemap-video-producer', 'made_at': old.get('made_at') or '2026-10-15'}
json.dump(m, open(os.path.join(EP, 'meta.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(title); print(desc); print('챕터 간격', gaps)
