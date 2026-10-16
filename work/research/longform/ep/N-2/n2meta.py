# N-2 meta.json 만들기(ytlong gate·up이 읽는다) — N-2 PD 2026-10-16
# 설명 끝 출처 줄: 실제로 쓴 배경(bg_used.json)만 Pexels credits desc_line·pilot 사진 sources.json에서 가져온다.
import json, os, sys
sys.stdout.reconfigure(encoding='utf-8')
EP = os.path.dirname(os.path.abspath(__file__)); W = os.path.abspath(os.path.join(EP, '..', '..', '..', '..'))
P = json.load(open(os.path.join(W, 'video', 'n2.json'), encoding='utf-8'))
used = json.load(open(os.path.join(EP, 'bg_used.json'), encoding='utf-8'))
cred = {str(c['id']): c for c in json.load(open(os.path.join(EP, 'stock', 'credits.json'), encoding='utf-8'))}
photo = {str(c['id']): c for c in json.load(open(os.path.join(W, 'research', 'visual', 'N-2-pilot', 'photo', 'sources.json'), encoding='utf-8'))}
lines = []
for u in used:
    i = os.path.splitext(os.path.basename(u))[0]
    if i in cred: lines.append(f"· 영상 {cred[i]['author']} / Pexels {cred[i]['page']}")
    elif i in photo: lines.append(f"· 사진 {photo[i]['photographer']} / Pexels {photo[i]['page']}")
thumb_photo = photo['761295']
lines.append(f"· 썸네일 사진 {thumb_photo['photographer']} / Pexels {thumb_photo['page']}")
lines = sorted(set(lines), key=lines.index)

# 챕터: 장 시작 초(10초 넘게 떨어진 것만)
st, a = [], 0
for s in P['scenes']: st.append(a / P['fps']); a += s['frames']
CH = [(0, '직장인 100명을 월급 순서로 한 줄로'), (1, '숫자 출처 · 통장 금액으로 세전 어림하기'), (2, '세전 150만원은 79등, 250만원은 59등'),
      (4, '줄 한가운데 50등은 세전 290만원쯤'), (7, '평균 375만원이 한가운데보다 높은 까닭'), (8, '내 자리는 한가운데와 견주기')]
ch = []
for si, name in CH:
    t = int(st[si]); ch.append(f'{t // 60}:{t % 60:02d} {name}')
ch[0] = '0:00 ' + CH[0][1]

title = '내 월급 순위는? 직장인 100명을 월급 순서로 한 줄 세워 보면'
desc = '\n'.join([
    '직장인 전체를 100명으로 줄여 세전 월급 순서로 한 줄 세우면, 딱 한가운데 50등은 세전 290만원쯤(통장 약 260만원)입니다. 세전 150만원은 79등, 250만원은 59등, 350만원은 38등, 450만원은 27등이고, 한 달 1,000만원 이상은 100명 중 4명입니다.',
    '뉴스에 나오는 평균 월급 375만원은 한가운데보다 높습니다. 내 자리는 평균 말고 줄 한가운데와 견줘 보세요(국가데이터처 2024년 12월 세전 월 보수 · 일자리 기준).',
    '',
    '내 통장 금액으로 세전·실수령 계산(파이어맵 월급 계산기): https://firemap.kr/calc/salary?utm_source=youtube&utm_campaign=n2',
    '지난 편 · 1년 연봉으로 본 상위 몇 %: https://youtu.be/420buEFKB8k',
    '',
    *ch,
    '',
    '출처',
    '· 국가데이터처 「2024년 임금근로일자리 소득(보수) 결과」(2026.2.23 보도자료) 3쪽 소득구간별 분포 2024년 줄 · 평균소득 375만원 · 중위소득 288만원',
    '· 통장 금액: 파이어맵 월급 계산기(소득세법 시행령 별표2 근로소득 간이세액표 2026.2.27 개정 · 4대보험 2026년 요율 · 본인 1명 · 식대 비과세 월 20만원 가정)',
    '읽는 법: 등수는 원문 구간 경계(150·250·350·450·1,000만원)에서만 읽었습니다(100명 중 등수 = 그 월급 이상 비율, 79.4%→79등). 가운데 288만원은 말로 290만원쯤이라 했습니다. 통계 단위는 사람이 아니라 일자리라 두 곳에서 일하면 두 번 셉니다. 그달 하루 이상 일한 일자리가 들어 있고, 상여금 포함 여부는 원문에 따로 적혀 있지 않습니다.',
    '',
    '배경 영상·사진(Pexels 무료 라이선스 https://www.pexels.com/license/ · 얼굴·상표 없는 장면만)',
    *lines,
    '',
    '내레이션은 AI 음성 내레이션(Google Cloud Text-to-Speech Chirp 3 HD)이고, 숫자는 모두 위 원문에서 가져와 파이어맵이 계산했습니다. 통계를 읽는 자료이며 어떤 직장·직업을 고르라는 권유가 아닙니다.',
])
m = {
    'ep': 'N-2', 'series': 'N 나 vs 남들(통계로 본 내 자리)',
    'title': title, 'title_by': 'N-2 PD 2026-10-16 — 시범 대본 질문 그대로, 58세 이해 시험 11~14차 8명 모두 뜻 맞힘(copywriter 결선 없음 — 사장님 당일 지시로 PD가 정함)',
    'thumb': 'thumb.png', 'thumb_src': 'pilot/preview/thumb_A.png',
    'thumb_status': '임시판 — 시범 thumb_A(judge_pilot 제미나이 7.5~8.5, 10/16 02시 롱폼 총괄 PD). 정식 1초 시험 3명(제미나이·GPT 웹·레드팀)·visual 관문 안 거침. 58세 이해 시험 11~14차 8명 모두 주제 맞힘. 48시간 클릭률 보고 visual·copywriter 교체',
    'desc': desc, 'chapters': ch,
    'tags': ['월급 순위', '직장인 월급', '평균 월급', '월급 중위값', '내 월급 몇 등'],
    'publishAt': '2026-10-18T13:40:00+09:00', 'privacy': 'private', 'privacy_note': '예약 공개(private+publishAt) — 정해진 시각에 공개로 바뀜',
    'paid': False, 'synthetic': True, 'veo': False,
    'synthetic_note': '다른 롱폼과 같게 True(AI 음성 내레이션) — 영상 디자인 총괄 10/16 지시',
    'coupang': None,
    'voice': 'Chirp 3 HD Charon 1.1 · 쉼 태그 끔(켠 판 편 전체 5.35~5.44 < 5.5) · 29줄 · 10/16 하루 · 튀는 줄 0(3줄 다시 받음)·앞뒤 −3.2%·IQR 0.18 · 편 전체 5.74음절/초',
    'answers': {
        'q1_바꿔끼우기': "아니오 — N-1(국세청 1년 연봉 천분위·세금·순자산 4주제)과 원자료(국가데이터처 2024년 12월 월 보수 분포)·질문('100명 줄에서 몇 등')·화면(실사 배경+100명 줄)이 모두 다르다.",
        'q2_연달아보기': '아니오 — 앞뒤 롱폼(10/17 W-1 2화 주가·10/19 C-2 인출)과 주제 축이 다르다(경제·통계).',
        'q3_약속이행': "예 — 제목 '내 월급 순위는?'에 2~6장이 세전 150·250·290·350·450만원의 100명 중 등수(79·59·50·38·27등)로, 7장이 1,000만원 이상 4명으로, 8장이 '한가운데와 견주기'로 답한다.",
        'q4_조언으로들리나': '아니오 — 직장·이직·투자 권유 0, 전망 0. 통계를 읽는 법(평균 vs 한가운데, 통장 금액 → 세전 어림)만.',
        'q5_사람의몫': '예 — 경쟁 상위 3편이 쓰지 않은 가장 새 원문 표를 화면에 보이고, 원문 구간 경계값만 등수로 읽고(보간 0), 58세 이해 시험 14차까지 고친 말로 풀었다.',
    },
    'experiment': {'X-LF-BG': '10/16 총괄 새 기준 — 모든 장면 Pexels 실사 배경(6.5초마다 다른 클립·구간) 첫 롱폼', 'X-N2-PILOT': '사장님 미리보기 시범판(질문 하나·한 방향·2분대)'},
    'first_comment_plan': 'pilot/first_comment.txt — 공개(10/18 11:30) 직후 나이별 줄(표7 5세 칸 가운데)·카페 짝 글 주소. 고정은 채팅 세션',
    'made_by': 'N-2 PD (firemap-video-producer 롱폼 담당)', 'missing': P.get('missing', 0),
    'video': os.path.join(W, 'video', 'out', 'n2_ds.mp4'),
}
json.dump(m, open(os.path.join(EP, 'meta.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('설명', len(desc), '자 · 챕터', ch, '· 배경 출처', len(lines))
