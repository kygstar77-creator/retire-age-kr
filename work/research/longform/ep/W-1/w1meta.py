# W-1 meta.json 만들기·갱신 — 숫자는 calc_out.txt에서만 (PD 2026-10-09 22:3x)
# 사용: py -3.12 research/longform/ep/W-1/w1meta.py   → meta.json의 제목·설명 틀(숫자 칸)만 다시 쓰고, 나머지(thumb·chapters·voice·after_publish 등)는 그대로 둔다.
# 10/10 06시 뒤 fetch_us → calc.py 재실행이면 이것도 다시 돌린다([F] 미국 칸). 제목·썸네일 문구는 copy/titles.md 1위(copywriter 10/9 12:51) — 10/10 12:00 오독 시험으로 2위 교체면 TITLE_RANK=2.
# 설명 첫 줄은 titles.md '꼭 지킬 것'의 문장 그대로. 나머지 문장은 대본 say_v2 표현에서 가져옴 → 렌더 전 aitell·editor 확인(desc_note).
import json, os, re, sys
sys.stdout.reconfigure(encoding='utf-8')
D = os.path.dirname(os.path.abspath(__file__))
TITLE_RANK = 1

c = {}
for ln in open(os.path.join(D, 'calc_out.txt'), encoding='utf-8'):
    m = re.match(r'\[(\w+)\] (.+?) = (.+)$', ln.strip())
    if m: c[m.group(1)] = m.group(3).strip()
def f(k): return float(c[k].replace(',', ''))
def i(k): return int(round(f(k)))

mp = os.path.join(D, 'meta.json')
m = json.load(open(mp, encoding='utf-8')) if os.path.exists(mp) else {}

# 제목 짝(titles.md) — 숫자가 calc_out과 다르면 멈춘다(카피 재심사 대상)
assert c['C5'] == '-5.07' and c['C8'] == '-1400000' and c['C9'] == '44.2', 'titles.md 1위 숫자(−5.07%·−140만원·44번치)가 calc_out과 다름 → copywriter 재심사'
assert c['B6'] == '31640' and c['A1'] == '107.4', 'titles.md 2위·썸네일 숫자가 calc_out과 다름'
t1 = '삼성전자 주가 사흘 −5.07%, 100주 평가액 −140만원 = 분기 배당 44번치'
t2 = '삼성전자 배당금 100주 세후 3만 1,640원, 같은 사흘 평가액은 −140만원'
th1, th2 = '107조(잠정) 공시한 사흘, 내 100주는?', '배당 44번치가 사흘에'
title, title_swap = (t1, t2) if TITLE_RANK == 1 else (t2, t1)
thumb_text, thumb_text_swap = (th1, th2) if TITLE_RANK == 1 else (th2, th1)

def won(x): return f'{x:,}원'
def man1(x): return f'{abs(x) / 10000:.1f}'.rstrip('0').rstrip('.')
us_up = f('F2') >= 0
f5 = i('F5')
us_line = (f"미국 S&P500을 따라가는 ETF(SPY) 1만 달러는 달러로 {'+' if us_up else ''}{c['F2'].replace('-', '−')}%였지만, "
           if us_up == (f5 < 0) else f"미국 S&P500을 따라가는 ETF(SPY) 1만 달러는 달러로 {'+' if us_up else ''}{c['F2'].replace('-', '−')}%, ")
us_line += f"원화로는 {man1(f5)}만원 {'줄었습니다' if f5 < 0 else '늘었습니다'}(원달러 {f('E1'):,.1f}원 → {f('E2'):,.1f}원, 한국은행 매매기준율)."

desc_tpl = (
"영업이익 107.4조원은 회사가 공시한 잠정치, 평가액은 팔지 않으면 확정 손실이 아닙니다.\n"
f"삼성전자 주가는 10월 2일 {won(i('C1'))}에서 10월 8일 {won(i('C3'))}으로 거래일 사흘 {c['C5'].replace('-', '−')}%, 100주 평가액은 {i('C6')//10000:,}만원에서 {i('C7')//10000:,}만원으로 {abs(i('C8'))//10000}만원 줄었습니다. "
f"지난 분기(2분기, 8월 지급) 배당 100주 세후 {won(i('B6'))}의 {c['C9']}배입니다.\n"
f"같은 사흘 코스피를 그대로 따라간 1천만원은 {abs(i('S4'))}만원 {'줄었고' if i('S4') < 0 else '늘었고'}({c['D3'].replace('-', '−')}%), {us_line}\n"
"지난주 공시·종가로 한 계산이고, 투자 권유나 다음 주 전망이 아닙니다(수수료 빼고 계산).\n\n"
"내 배당에 세금이 얼마 붙는지(파이어맵 배당 세금 정리): https://firemap.kr/guide/dividend-tax-thresholds?utm_source=youtube&utm_medium=longform&utm_campaign=VIDEOID\n\n"
"{CHAPTERS}\n\n"
"출처\n"
"· 삼성전자 연결 영업(잠정)실적 공시: DART 접수번호 20261008800004 · 2분기 배당 결정: DART 20260730800137(기준일 6/30·지급 8/28) · 1년 전 3분기 배당: DART 20251030800075\n"
"· 삼성전자(005930.KS)·SPY 종가: 야후 파이낸스 일별 종가\n"
"· 코스피: 한국은행 ECOS 802Y001 · 원달러 매매기준율: 한국은행 ECOS 731Y001\n"
"· 미국 소비자물가: 세인트루이스 연준 FRED CPIAUCNS · 일정: 미국 노동통계국 CPI 발표 일정 · 한국은행 통화정책방향 결정회의 · 미국 연준 FOMC 일정표\n"
"· 배당 세금 15.4%(배당소득세 14% + 지방소득세 1.4%)로 계산\n"
"확인 안 함: 삼성전자 3분기 배당 금액(공시 전) · 증권사 수수료\n\n"
"이 영상은 종목 추천이 아닙니다.\n"
"내레이션은 AI 음성 내레이션(Gemini TTS)이고, 숫자는 모두 위 원문에서 가져와 파이어맵이 계산했습니다.\n"
"파이어맵 카페: https://cafe.naver.com/firemap"
)

keep = dict(m)
m.update({
 "ep": "W-1",
 "title": title, "title_swap": title_swap, "title_candidates": [t1, t2],
 "title_by": f"firemap-copywriter copy/titles.md {TITLE_RANK}위(10/9 12:51, 3명 8.40) · 10/10 12:00 오독 시험 결과로 2위 교체 가능(TITLE_RANK) · 48h CTR이 채널 중앙값 아래면 title_swap 1회",
 "thumb_text": thumb_text, "thumb_text_swap": thumb_text_swap,
 "desc_tpl": desc_tpl,
 "desc": keep.get('desc') if keep.get('desc_tpl') == desc_tpl else desc_tpl,
 "desc_note": "w1meta.py가 calc_out에서 숫자를 채운다. 녹음·렌더 뒤 work/video/chapters.py video/w1.json ep/W-1로 {CHAPTERS}. 렌더 전 desc_tpl 문장 aitell·editor 확인",
 "calc_asof": c.get('F1'),
})
m.setdefault("thumb", None)
m.setdefault("thumb_status", "대기 — firemap-visual-designer 확정본(10/10 14:00 기한, visual/W-1-thumb) · 1초 시험 3명 평균 7 이상")
# 장면 번호 = video/w1.json scenes 순서(10/9 22:2x 확인). 제목은 대본 장 머리 그대로(editor 통과 말)
m.setdefault("chapters", [[0, "이번 주 영수증 세 장"], [4, "이번 주는 사흘짜리였어요"], [7, "첫 번째 영수증 — 삼성전자 100주"], [14, "두 번째 영수증 — 코스피 1천만원"], [17, "세 번째 영수증 — 미국 주식 1만 달러"], [20, "세 장 합치기"], [21, "다음 주에 볼 날짜"], [24, "정리"]])
m.setdefault("tags", ["삼성전자 주가", "코스피", "원달러환율", "삼성전자 배당금", "삼성전자 영업이익"])
m.setdefault("tags_by", "kwvol 10/9 12:4x 검색량 순(copy/titles.md 검증): 삼성전자주가 17,532,300 · 코스피 7,231,900 · 원달러환율 501,200 · 삼성전자배당금 307,300 · 삼성전자영업이익 10,760")
m.setdefault("publishAt", "2026-10-11T19:30:00+09:00")
m.setdefault("privacy", "private")
m.setdefault("privacy_note", "예약 공개 — publishAt 시각에 자동 public(slots.json 10/11 19:30 롱폼 칸, 매주 토 고정 코너 1화)")
m.setdefault("paid", False); m.setdefault("synthetic", False); m.setdefault("veo", False)
m.setdefault("coupang", "안 붙임 — 주식·지수(금융) 주제라 쿠팡 금지 규칙")
m.setdefault("voice", {"model": "gemini-3.8-flash-tts", "voice": "Charon", "rec": None, "check": "10/10 16:01 창 녹음 뒤(runbook_1010, --gate 0.10)"})
m.setdefault("playlist", "주간 '이번 주 뉴스가 내 돈에 얼마'(X-SERIES-1 ④) — 2화부터 재생목록 만들기")
m.setdefault("answers", {
 "q1_바꿔끼우기": "아니오 — 그 주 공시·종가(DART 잠정실적·배당 결정, ECOS 코스피·환율, SPY 종가)로 100주·1천만원·1만 달러 세 영수증을 원 단위로 계산한 편이라, 주 단어만 바꾸면 숫자·원문 표·장면이 전부 달라진다.",
 "q2_연달아보기": "아니오 — 앞 편들(A-1·M-1·C-1)은 상품을 1년 이상 기간으로 잰 계산이고, W-1은 한 주 뉴스를 내 돈 영수증으로 바꾸는 새 고정 코너다. 장면 26·종류 23, 새 부품 parts/weekly.tsx 6개.",
 "q3_약속이행": "예 — 제목 '사흘 −5.07%·100주 평가액 −140만원·배당 44번치'는 2장 영수증 1(종가·평가·세후 배당)이 그대로 답하고, 썸네일 '107조(잠정) 공시한 사흘, 내 100주는?'은 0장·2장 공시 원문 표와 영수증 1이 답한다.",
 "q4_조언으로들리나": "아니오 — 원인 추측·전망·매수/매도 말 0, 말하는 줄에 '투자 권유가 아니라 지난주 공시·종가로 한 계산'(youtube-loop 10/10 추가분), 평가액은 팔지 않으면 확정 아님을 화면·설명 첫 줄에. 쿠팡·상품 링크 없음.",
 "q5_사람의몫": "예 — 경쟁 5편이 원인·전망만 말할 때, 같은 주 뉴스를 원 단위 영수증 세 장(평가액 vs 세후 배당 대비, 환율 떼어 보기)으로 바꾸고 DART·한국은행 원문 표만 보여 주는 편집 판단."
})
m.setdefault("experiment", {"W1-NEWS": "그 주 뉴스 이름을 제목 맨 앞(analysis ⑧)", "X-PD-GATE": "B(--gate 0.10)", "X-SERIES-1": "④ 주식 뉴스형 고정 코너 1화"})
m.setdefault("endscreen", {"video": "eTjVs1vDTwg", "ep": "M-1", "how": "API 미지원 — 업로드 직후 Studio 최종 화면 '특정 동영상 = M-1'(배당 이어짐)", "status": "업로드 뒤 할 일"})
m.setdefault("after_publish", ["cafe.md 카페 글은 영상과 같은 시각 또는 먼저(analysis.md 132행, firemap-write)"])
m.setdefault("video", "C:/Users/강영준/Documents/GitHub/retire-age-kr/work/video/out/w1_ds.mp4")  # 렌더 → deess 뒤 파일(M-1 m1_ds 같은 틀)
m.setdefault("made_by", "firemap-video-producer"); m.setdefault("made_at", "2026-10-09 22:3x")
m.setdefault("todo_pd", "10/10 06시 뒤 calc 재실행 확인 → w1meta.py 다시 → 16:01 runbook_1010 녹음 → w1props → lfrender text(editor stamp) → lfrender render W-1 → 스틸 눈 검사·motioncheck → chapters.py video/w1.json ep/W-1 → scorecard 우리 칸 → ytlong gate → up(10/11 19:30) · 관문 기한 10/10 19:30")
json.dump(m, open(mp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('title:', title); print('---'); print(desc_tpl.split('\n\n')[0])
