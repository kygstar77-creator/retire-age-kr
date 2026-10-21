# J-1 meta.json — j1.json(장면 시각)·bg_used.json(실사 출처)·copy/titles.md(제목) → meta.json
#   py -3.12 work/research/longform/ep/J-1/j1meta.py   (j1props.py 다음에 · 다시 녹음·렌더 뒤 챕터 시각이 바뀌면 다시)
# 10/22 PD: h3meta.py 꼴. 챕터 이름 = script.md 장 머리(shot_plan '장' 칸과 같음, shot_check) · 썸네일은 visual 2차 시험 뒤 thumb 칸만 채움
import json, os, re, sys
sys.stdout.reconfigure(encoding='utf-8')
EP = os.path.dirname(os.path.abspath(__file__))
VID = os.path.normpath(os.path.join(EP, '..', '..', '..', '..', 'video'))
P = json.load(open(os.path.join(VID, 'j1.json'), encoding='utf-8'))
MP = os.path.join(EP, 'meta.json')
old = json.load(open(MP, encoding='utf-8')) if os.path.exists(MP) else {}
heads = [re.sub(r'^\[?(\d+\.|기초\])\s*|\]$', '', h).strip() for h in re.findall(r'^## (.+)$', open(os.path.join(EP, 'script.md'), encoding='utf-8').read(), re.M)]
heads = [h.replace('[0. ', '').strip('[] ') for h in heads]
starts, a = [0], 0
for s in P['scenes']:
    n = s['data'].get('n', '') if s['kind'] == 'ask' else ''
    if n == '기초' or re.match(r'^\d+장$', n) or n == '댓글로 알려 주세요': starts.append(a)
    a += s['frames']
assert len(starts) == len(heads) == 13, (len(starts), len(heads), heads)
fmt = lambda f: f"{int(f / 30) // 60}:{int(f / 30) % 60:02d}"
chapters = [[round(st / 30), h] for st, h in zip(starts, heads)]
assert all(b[0] - a_[0] >= 10 for a_, b in zip(chapters, chapters[1:])), chapters
CH = '\n'.join(f"{fmt(st)} {h}" for st, h in zip(starts, heads))
credits = [c['desc_line'] for c in json.load(open(os.path.join(EP, 'bg_used.json'), encoding='utf-8'))]
TITLE = '종부세 정부안, 공시가격 20억 집 한 채 10년 살았으면 보유세 줄고 안 살면 140만원 넘게 는다'
TITLE2 = '종부세 정부안대로면 같은 공시가격 20억 집도 살면 줄고 안 살면 는다'
FIRST2 = ['국회 심사 중인 정부 종합부동산세법 개정안(2026.9.3 제출, 국회 통과 전) 기준으로, 공시가격 20억 집 한 채를 가진 55세·보유 10년의 2028년 한 해 보유세(재산세+종부세)를 계산했습니다. 그 집에 살면 618.9만원 → 596.4만원, 살지 않으면 759.8만원으로 늘어납니다.',
          '올해 12월 고지서는 지금 법 그대로이고, 정부안대로 통과되면 바뀐 계산은 2027년 고지서부터입니다(재정경제부 2026 세제개편안 상세본 · 파이어맵 계산 · 세무 상담 아님).']
TPL = '\n'.join(FIRST2) + '''

공시가격 12억~40억 × 산다/안 산다 × 45세·55세·70세 전체 표(카페): {CAFE}

{CHAPTERS}

출처
· 국회 의안정보시스템 의안 2221046 종합부동산세법 일부개정법률안(정부, 2026.9.3 제출, 2026-10-19 확인)
· 재정경제부 2026년 세제개편안 상세본·문답자료(2026.9.1 보도자료 「2026년 세제개편안」)
· 종합부동산세법 §3·§7·§8·§9·§10·§10의2·§16·§20의2, 국회법 §86, 헌법 §53(법제처 국가법령정보센터, 2026-10-19 확인)
· 국세청 '공동명의 1주택자 특례' 안내(2026-10-19 확인) · 국토교통부 부동산공시가격 알리미
· 재정경제부 국회 제출 자료 추산 보도(SBS 2026.9.19)
계산 가정: 55세·그 집 보유 10년(따로 적은 곳 빼고) · 공시가격 그대로 · 보유세 = 재산세(도시지역분·지방교육세 포함)+종부세(농어촌특별세 포함) · 재산세 공정시장가액비율 45% 가정 · 거주·비거주 판정 기준은 시행령에 넘겨져 확인 안 함. 이 계산기는 재정경제부 문답자료 적용사례 9칸 중 8칸을 ±0.2만원으로 재현했습니다(8월 첫 안 기준).

내레이션은 AI 음성 내레이션(Google Cloud Text-to-Speech Chirp 3 HD)이고, 일부 장면은 AI로 만든 그림(RealVisXL V5.0 — 우편함·거실·민원 창구·물컵·찻잔, 얼굴·글자 없음)입니다. 숫자는 모두 위 원문에서 가져와 파이어맵이 계산했습니다. 계산·비교 자료이며 집을 사거나 팔거나 이사하라는 권유, 세무 상담이 아닙니다.
''' + '\n'.join(credits)
cafe = old.get('cafe_url') or 'https://cafe.naver.com/firemap'
m = dict(old)
m.update({
    'ep': 'J-1', 'series': '정책 — 1주택 종부세 정부안',
    'title': TITLE, 'title_by': 'firemap-copywriter 2026-10-19 18:59 copy/titles.md 1위 짝(레드팀 고친 판 · 40·50·60세 2차 뜻 맞음)',
    'title_candidates': [TITLE, TITLE2],
    'thumb_text_top': old.get('thumb_text_top') or '종부세 정부안 · 국회 심사 중 · 집 한 채',
    'thumb_text': old.get('thumb_text') or '공시가격 20억 보유세 / 거주 안 하면 140만원 늘어',
    'thumb_text_small': old.get('thumb_text_small') or '2028년 한 해',
    'thumb': old.get('thumb') or os.path.join(EP, 'thumb_j1n_b.png'),
    'thumb_status': old.get('thumb_status') or "10/22 PD: visual 17:23 thumb_j1n_b(1차 시험 통과·문구 2차 남음) — copywriter 10/21 18:54 문구 2차 1위('거주 안 하면 140만원 늘어')로 새판·1초 시험·짝 비교 뒤 교체",
    'desc_first2': FIRST2, 'desc_tpl': TPL, 'desc': TPL.replace('{CAFE}', cafe).replace('{CHAPTERS}', CH), 'chapters': chapters,
    'tags': ['종부세', '종합부동산세 개편안', '1주택 종부세', '공동명의 종부세', '보유세'],
    'publishAt': '2026-10-24T11:30:00+09:00', 'privacy': 'private', 'privacy_note': '예약 공개(private+publishAt) — 정해진 시각에 공개로 바뀜',
    'paid': False, 'coupang': None, 'synthetic': True, 'veo': False,
    'synthetic_note': 'AI 생성 그림 5장(RealVisXL V5.0 — 우편함·거실·창구·물컵·찻잔, 얼굴·상표·글자 없음, 화면에 "AI 생성 그림" 표시) + AI 음성 → containsSyntheticMedia True',
    'voice': 'Chirp 3 HD Charon 1.1 · 214줄 · 2026-10-21 녹음(say_v5, editor 10/21 17:09 서명) · 10/22 다시 받기 3줄(say.json 쉼표)',
    'answers': {
        'q1_바꿔끼우기': "아니오 — T-1(양도세 장특공)과 같은 정부 세법 개편이지만 세금·질문이 다르다(보유세·'그 집에 사나'·공동명의 특례). 공시가격별 산다/안 산다 갈림길(23억대·24억), 안 사는 집 14억 기준선의 54만원 계단, 공동명의 18억 계단 161.8만원은 우리 계산기로만 나온 숫자다.",
        'q2_연달아보기': '아니오 — 앞 편 H-3(부동산 실거래, 10/23)·다음 편 D-ETF-1(배당 ETF, 10/25)과 축이 다르다(정책·세금). T-1(10/21)과 사흘 간격.',
        'q3_약속이행': "예 — 제목 '20억 10년 살았으면 보유세 줄고 안 살면 140만원 넘게 는다'는 0장·3장(−22.5만원 / +140.9만원, 2028년 한 해)이 답하고 9장 정리에서 다시 말한다.",
        'q4_조언으로들리나': "아니오 — 사라·팔라·이사하라·전입하라 0, 국회 통과 전망 0, 공동명의는 '두 계산을 비교해 보시라'까지, 거주 판정 기준은 '확인 안 함'으로 말한다.",
        'q5_사람의몫': '예 — 재경부 추산 429만원이 어떤 사람 이야기인지(60세 미만·보유 5년 미만)를 계산기로 재현해 보이고, 같은 집이 산다/안 산다로 갈리는 공시가격(23억대)을 처음 셌다(경쟁 16편 0편).',
    },
    'experiment': {},
    'endscreen': {'how': 'Studio 최종 화면 — 업로드 뒤 할 일(다음 편 D-ETF-1 또는 T-1 Qg5Tj2fuJ3A)', 'status': '미정'},
    'made_by': 'firemap-video-producer', 'made_at': old.get('made_at') or '2026-10-22',
    'video': os.path.join(VID, 'out', 'j1.mp4'), 'missing': 0,
})
json.dump(m, open(MP, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('meta.json · 제목', len(TITLE), '자 · 챕터', len(chapters), '· 설명', len(m['desc']), '자 · 실사 출처', len(credits))
print(CH)
