# G-1 meta.json 만들기·갱신 — 숫자는 calc.json(공개 전날 calc.py 재실행분)에서만 (PD 2026-10-07)
# 사용: py -3.12 research/longform/ep/G-1/g1meta.py   → meta.json의 숫자 칸(제목·썸네일 문구·설명 틀)만 다시 쓰고, 나머지(thumb·chapters·publishAt·cafe_url 등)는 그대로 둔다.
# 제목 틀: copy/titles.md 1위(copywriter 10/6 12:51) — 숫자만 calc 기준으로 바뀜. 숫자가 바뀌면 카피 재심사 필요(titles.md '꼭 지킬 것').
import json, os, sys, datetime
D = os.path.dirname(os.path.abspath(__file__))
c = json.load(open(os.path.join(D, 'calc.json'), encoding='utf-8'))
mp = os.path.join(D, 'meta.json')
m = json.load(open(mp, encoding='utf-8')) if os.path.exists(mp) else {}

def man(won): return int(won / 10000 + 0.5)       # 만원 반올림 — 대본 [S] 말 단위(956만원)와 같게. titles.md 내림(975)은 10/2 쇼츠·카페 맞춤이었고, 이 영상 안 말과 제목이 달라지면 안 됨(PD 10/7)
rows = {r['name']: r for r in c['rows']}
y1, pk = rows['1년 전'], rows['1년 고점']
lo, hi = min(r['krx'] for r in c['rows']), max(r['krx'] for r in c['rows'])
assert lo == pk['krx'] and hi == y1['krx'], '가장 적은 칸=고점·가장 많은 칸=1년 전 가정이 깨짐 → 제목 틀 다시'
asof = c['asof']; ad = datetime.date.fromisoformat(asof)
asof_ko = f'{ad.year}년 {ad.month}월 {ad.day}일'
pkd = datetime.date.fromisoformat(pk['day']); y1d = datetime.date.fromisoformat(y1['day'])

title = f'금값 1천만원 영수증 4장, 산 날 따라 {man(lo)}만원부터 {man(hi)}만원까지'
title_swap = f'금값 1천만원 영수증 4장, {pkd.month}월 고점({pkd.month}/{pkd.day})에 산 사람은 {man(lo)}만원'
thumb_text = f'{pkd.month}월 고점에 샀다면 {pk["krx_pct"]:.1f}%'
thumb_text_swap = f'산 값 되찾으려면 +{c["need_pct"]:.1f}%'   # copywriter 10/7: '산 값까지'는 '고점까지' 전망으로 읽힐 소지(레드팀)

def won(x): return f'{x:,}원'
desc_tpl = (
f"같은 금 1천만원어치인데, 산 날에 따라 오늘({asof_ko} KRX 금시장 기준) {man(lo)}만원부터 {man(hi)}만원까지 남았습니다. "
f"{pkd.month}월 {pkd.day}일 1년 고점에 샀다면 {won(pk['krx'])}({pk['krx_pct']:.2f}%), {y1d.year}년 {y1d.month}월 {y1d.day}일에 샀다면 {won(y1['krx'])}({y1['krx_pct']:.2f}%)입니다(지나간 값 계산 · 투자 권유 아님).\n"
f"KRX 금값 변화를 달러 금값 × 환율 × KRX 웃돈 세 조각으로 나누고, KRX 금시장·금현물 ETF·골드뱅킹·골드바 네 길을 같은 1천만원으로 비교했습니다.\n\n"
"산 날 4개 × 산 길 4개 전체 표(카페): {CAFE}\n"
"금 1천만원 1년 성적, 길별로 먼저 잰 글: https://cafe.naver.com/firemap/216\n\n"
"{CHAPTERS}\n\n"
"출처\n"
"· KRX 금시장 금 1kg 일별 종가(원/g): 네이버 금융 국제시장 M04020000\n"
"· 금현물 ETF(411060) 종가 · 금 선물(GC=F) 뉴욕 종가: 야후 파이낸스 일별\n"
"· 원/달러 매매기준율: 한국은행 ECOS 731Y001\n"
"· 골드뱅킹: KB국민은행 골드 가격조회 일자별(그날 마지막 고시, 살 때 +1%·팔 때 -1%)\n"
"· 한국은행 보도자료 2026-08-03 「한국은행, 국내 생산 금 매입 협력 체계 구축」 · World Gold Council 2026-09-09 금 ETF 8월 보유·유입 · 미 재무부 Daily Treasury Par Yield Curve 10년\n"
"· 세금: 조세특례제한법 제126조의7(KRX 금 부가세 면제·인출 때 과세) · 부가가치세법 제30조(10%) · 소득세법 제94조·제17조·제129조(배당소득 15.4%)\n"
"계산 빠진 것: 증권사 수수료 · 골드바를 팔 때 받는 값 차이 · 국제값은 금 선물 × 매매기준율 어림\n\n"
"내레이션은 AI 음성 내레이션(Gemini TTS)이고, 숫자는 모두 위 원문에서 가져와 파이어맵이 계산했습니다. 금을 사거나 팔라는 말이 아닙니다.\n"
"파이어맵 카페: https://cafe.naver.com/firemap")

base = {
 'ep': 'G-1',
 'thumb': m.get('thumb'), 'thumb_status': m.get('thumb_status', '없음 — [썸네일 요청] firemap-visual-designer (PD 10/7)'),
 'title_by': 'firemap-copywriter copy/titles.md 1위 틀(C3, 3명 7.93) · 숫자는 g1meta.py가 calc.json에서 · 48h CTR이 채널 중앙값 아래면 title_swap+thumb_text_swap 짝으로 한 번 교체',
 'tags': ['금값', '금시세', '골드바', '금현물 ETF', 'KRX 금시장'],
 'publishAt': m.get('publishAt'), 'privacy': 'private', 'privacy_note': '예약 공개 — publishAt 시각에 자동 public(slots.json 롱폼 칸, 회의가 배정)',
 'paid': False, 'synthetic': False, 'veo': False,
 'coupang': '안 붙임 — 금 투자(금융·투자 주제), 시험 4편 중 1편 규칙도 이 편 아님',
 'voice': {'model': 'gemini-3.8-flash-tts', 'voice': 'Charon'},
 'video': m.get('video', 'C:/Users/강영준/Documents/GitHub/retire-age-kr/work/video/out/g1_ds.mp4'),
 'chapters': m.get('chapters', []), 'desc': m.get('desc', ''),
 'desc_note': '녹음·렌더 뒤 chapters.py로 {CHAPTERS}, 카페 전체 표 글(cafe.md → firemap-write) 발행 뒤 {CAFE}를 그 주소로 채워 desc에. {CAFE}가 빈 채로는 올리지 않는다(대본 7장 "설명란의 카페 글" 약속).',
 'cafe_url': m.get('cafe_url'),
 'experiment': m.get('experiment', {'X-YT-OPEN-1': 'B(첫 30초 구성, analysis ⑧)'}),
 'endscreen': m.get('endscreen', {'video': None, 'how': 'Studio 최종 화면 — 같은 시청자 잇기는 공개 직전 채널 영상 중 노출 가장 많은 편(회의 판단)', 'status': '업로드 뒤 할 일'}),
 'made_by': 'firemap-video-producer', 'made_at': m.get('made_at', datetime.datetime.now().strftime('%Y-%m-%d %H:%M')),
}
m.update(base)
m.update({'asof': asof, 'title': title, 'title_swap': title_swap, 'title_candidates': [title, title_swap],
          'thumb_text': thumb_text, 'thumb_text_swap': thumb_text_swap, 'desc_tpl': desc_tpl})
m.setdefault('answers', {})
json.dump(m, open(mp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(title); print(thumb_text); print('기준일', asof, '→', mp)
