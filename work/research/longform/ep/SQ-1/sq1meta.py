# SQ-1 meta.json — video/sq1.json(장 카드 시작)·voice.json·bg_used.json(실사 출처) → meta.json + desc_1126.txt(editor 설명란 서명용)
#   py -3.12 work/research/longform/ep/SQ-1/sq1meta.py   (sq1props.py 다음에, 녹음·말·숫자가 바뀌면 다시)
# 11/26 15:4x PD: H-6 h6meta.py 꼴.
#   제목 = copywriter copy/sq1/final.txt 1줄(질문꼴·결론 숫자 없음 C-36, tp4 짝 비교 2:0 유지)
#   썸네일 = thumb_sq1_b2.png(visual 11/26 09:22 bright1126 — c1b 문구 그대로·밝기+모니터에 우리 선, 짝 비교 2:0, copywriter 1초 시험은 c1b 168 2차 통과 11/25 19:01)
#   설명 첫 두 줄 = script 0장·3장 자막 값(calc_mix_out_1112·calc_krw_out_1120) · 11/27 올리기 전 확인(youtube-loop)에서 값이 바뀌면 FIRST2도 같이
import json, os, sys
sys.stdout.reconfigure(encoding='utf-8')
EP = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(EP, '..', '..', '..', '..', '..'))
VID = os.path.join(ROOT, 'work', 'video')
P = json.load(open(os.path.join(VID, 'sq1.json'), encoding='utf-8'))
V = json.load(open(os.path.join(EP, 'voice.json'), encoding='utf-8'))
MP = os.path.join(EP, 'meta.json')
m = json.load(open(MP, encoding='utf-8')) if os.path.exists(MP) else {}
TITLES = ['나스닥100에 SCHD를 섞으면 덜 떨어질까? 섞는 비율별 실제 결과']
THUMB = os.path.join(EP, 'thumb_sq1_b2.png')
THUMB_TOP, THUMB_TEXT = '', '나스닥100에만 넣었다면 / SCHD랑 반반이면 얼마?'   # c1b 문구(copywriter 11/24 18:58 c1b 요청·11/25 19:01 고름)

heads = ['여는 말']
starts, a = [0], 0
for s in P['scenes']:
    d = s.get('data') or {}
    if s['kind'] == 'ask' and str(d.get('n', '')).endswith('장'): starts.append(a); heads.append(d['q'])
    a += s['frames']
fps = P.get('fps', 30)
assert len(starts) == len(heads) == 9, (len(starts), len(heads))
chapters = [[round(st / fps), h] for st, h in zip(starts, heads)]
assert all(b[0] - a_[0] >= 10 for a_, b in zip(chapters, chapters[1:])), chapters
fmt = lambda f: f"{int(f / fps) // 60}:{int(f / fps) % 60:02d}"
CH = '\n'.join(f"{fmt(st)} {h}" for st, h in zip(starts, heads))

FIRST2 = ["나스닥100(QQQ)과 SCHD를 섞는 비율별로 2011년 10월 말 1억을 15년 굴려 보면(달러·분배 재투자·해마다 비율 맞춤) SCHD만 6.77억, 반반 10.10억, 나스닥100만 13.56억이었고, 가장 크게 빠진 폭은 −21.5%·−24.0%·−32.6%였어요.",
          "최근 5년으로 자르면 반반이 나스닥100만을 거의 따라왔고, 원화로 다시 세면 환율 몫이 더해졌어요. 미국 상품을 직접 샀을 때와 국내 상장 상품을 샀을 때의 세금 차이까지 한국은행·법제처 원문으로 셌습니다."]
DIS = '특정 상품을 사거나 팔라는 뜻이 아닙니다. 지난 값과 공개된 세법만 정리했고, 지난 값은 앞날을 말해 주지 않습니다.'
tpl = '\n'.join(FIRST2) + '\n' + DIS + '''

비율별 전체 표(100·70·50·30·0% × 15년·10년·5년, 달러·원화·세후)(카페): {CAFE}
파이어맵 배당 계산기: https://firemap.kr/dividend?utm_source=youtube&utm_medium=description&utm_campaign=sq-1

{CHAPTERS}

출처
· QQQ·SCHD 월말 수정 종가(분배 재투자) 2011-10~2026-10: 야후 파이낸스 history(2차 시세) — 운용사 공식 수익률과 대조 ±0.05%p · Invesco QQQ https://www.invesco.com/qqq-etf/en/etf-insights/qqq-quarterly-outlook.html · Schwab SCHD https://www.schwabassetmanagement.com/products/schd
· 지수 방법론: Nasdaq-100(Nasdaq 공식) · Dow Jones U.S. Dividend 100(S&P 다우존스 지수 공식)
· 원·달러 월말 매매기준율: 한국은행 ECOS 731Y001 https://ecos.bok.or.kr/
· 국내 상장 상품 보수·분배: TIGER 미국나스닥100(133690)·TIGER 미국배당다우존스(458730) 미래에셋자산운용 상품 페이지(2026-11-13)
· 해외 주식 양도소득 20%(+지방 2%)·기본공제 250만원: 소득세법 제94조·제103조·제104조, 지방세법 제103조의3 https://www.law.go.kr/법령/소득세법/제104조
· 국내 상장 해외 ETF 이익 = 배당소득 15.4%·금융소득 2천만원 넘으면 종합과세: 소득세법 제17조·제14조·제62조, 시행령 제26조의2 https://www.law.go.kr/법령/소득세법시행령/제26조의2
· 미국 배당 제한세율 15%: 국세청 조세조약 제한세율표 · 소득세법 제129조
{STOCK}
계산 가정: 2011-10-31 1억 넣고 2026-10-30까지 · 월말 값 · 매년 10월 말 비율 되돌림 · 분배 재투자 · 수수료 뺌 안 함 · 세후는 일반 계좌·한 번에 판 경우

내레이션은 AI 음성 내레이션(Google Cloud Text-to-Speech Chirp 3 HD)이에요. 숫자는 모두 위 원문에서 가져와 파이어맵이 계산했습니다.'''
credits = list(dict.fromkeys(c['desc_line'] for c in json.load(open(os.path.join(EP, 'bg_used.json'), encoding='utf-8'))))
cafe = m.get('cafe_url') or 'https://cafe.naver.com/firemap'
desc = tpl.replace('{CAFE}', cafe).replace('{CHAPTERS}', CH).replace('{STOCK}', '\n'.join(credits))
m.update({
    'ep': 'SQ-1', 'series': '배당ETF·지수 — 섞어 사기',
    'title': TITLES[0], 'title_by': 'copywriter copy/sq1/final.txt · tp4 짝 비교(11/21 15:14) 2:0 유지 · C-36 결론 숫자 없음', 'title_candidates': TITLES,
    'thumb_text_top': THUMB_TOP, 'thumb_text': THUMB_TEXT, 'thumb': THUMB,
    'thumb_status': '11/26 09:22 visual sq1_b2(c1b 문구 그대로·밝기+왼쪽 모니터 우리 선) 짝 비교 2:0 · c1b 1초 시험 168 2차 통과(copywriter 11/25 19:01) · C-39 경쟁 c1 2/2(visual 11/24 09:15)',
    'desc_first2': FIRST2, 'desc_first2_src': 'script 0장·3장 자막(calc_mix_out_1112·calc_krw_out_1120)',
    'tags': ['나스닥100', 'SCHD', '나스닥100 SCHD', 'QQQ', '배당 ETF'],
    'desc_tpl': tpl, 'desc': desc, 'chapter_titles': heads, 'chapters': chapters,
    'chapters_note': f'video/sq1.json 장 카드 시작 프레임(11/26 PD sq1meta.py) — props 길이 {round(a / fps, 1)}초',
    'cafe_first': "대본 8장 '비율별 전체 표는 파이어맵 카페에' → 카페 짝 글(ep/SQ-1/cafe.md 재료)을 공개 같은 날 영상보다 먼저 — write·회의가 칸 배정",
    'voice': f"Chirp 3 HD Charon {V.get('speakingRate')} · {V.get('done')}줄 · {V.get('seconds')}초",
    'missing': V.get('missing', 0),
    'publishAt': '2026-11-28T11:30:00+09:00', 'privacy': 'private', 'privacy_note': '예약 공개(private+publishAt) — 정해진 시각에 공개로 바뀜',
    'paid': False, 'coupang': None, 'synthetic': True, 'veo': False,
    'synthetic_note': 'AI 음성 내레이션 → containsSyntheticMedia True. AI 생성 그림 없음(판은 calc 값으로 그림, 실사는 Pexels)',
    'answers': {
        'q1_바꿔끼우기': "아니오 — QQQ·SCHD 월말 수정 종가와 ECOS 환율로 비율 5가지 × 15년·10년·5년을 직접 다시 셌고(calc_mix·calc_krw·calc_dca), 직투·국내 상장 세후를 법 조문으로 셈(calc_tax). 경쟁 16편 중 비율별·원화·세후를 한꺼번에 낸 편 0(toc_compare).",
        'q2_연달아보기': '예 — 앞 편 11/26 H-6(부동산)·뒤 편 11/30 CC-1(배당 커버드콜)과 이틀씩 띄움. 배당 축 앞 편 D-ETF-1과 질문이 다름(섞는 비율·세후).',
        'q3_약속이행': "예 — 제목 '섞으면 덜 떨어질까? 비율별 실제 결과'는 3장 다섯 줄 표(끝값·가장 크게 빠진 폭)가 바로 답하고, 썸네일 '나스닥100에만/SCHD랑 반반이면 얼마?'는 0장 막대 셋(6.77·10.10·13.56억)이 답한다.",
        'q4_조언으로들리나': "아니오 — 3장 '계산을 그렇게 했다는 뜻이고, 꼭 그렇게 하셔야 한다는 말은 아니에요'·8장 '지난 값은 앞날을 말해 주지 않습니다'·끝 자막 '계산·비교 자료이며 매수·매도 권유가 아닙니다'·설명 면책 줄.",
        'q5_사람의몫': "예 — '15년 답과 5년 답이 다르다'·'같은 지수라도 어디서 샀느냐가 세후 3억 넘게 가른다'·'일반 계좌에서 오래 들고 한 번에 팔수록 국내 상장 쪽이 불리'는 원자료로 갈라 낸 우리 판단."},
    'endscreen': {'how': 'Studio 최종 화면 — 업로드 뒤', 'status': '미정 — link-plan-1125.md 짝 표대로(채팅 세션 몫)'},
    'made_by': 'firemap-video-producer', 'made_at': '2026-11-26',
    'video': os.path.join(VID, 'out', 'sq1_dsl1126.mp4').replace('\\', '/'),   # 11/26 15:2x PD: editor 15:13 stamp 뒤 3토막 통렌더(check/render_parts_1126.sh) → trim_concat → deess --chirp-short
    'click_ok': [],
    'todo': '11/26 PD: 통렌더 끝 → screen·bgcheck·눈 검사·bench → youtube-loop 올리기 전 확인(research.md) → cafe_url → gate·예약 11/28 11:30 · 재생목록 PLMpE1OMAC7pM(지수) 공개 뒤'})
json.dump(m, open(MP, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
open(os.path.join(EP, 'desc_1126.txt'), 'w', encoding='utf-8').write(m['title'] + '\n\n' + desc + '\n')
print(CH); print(f'설명 {len(desc)}자 · 실사 출처 {len(credits)}줄 · missing {m["missing"]} · 제목 {len(m["title"])}자')
