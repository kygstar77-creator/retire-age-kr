# N-3 meta.json — n3.json(장면 시각)·bg_used.json(실사 출처)·voice.json·copy/titles.md → meta.json 제목·설명·챕터·5문항
#   py -3.12 work/research/longform/ep/N-3/n3meta.py   (n3props.py 다음에)
# 11/15 02:2x PD(정기): H-4 h4meta.py 꼴. 제목·썸네일 글은 copywriter copy/titles.md 1위·10/28 확정판 그대로(지어내지 않음).
#   설명 첫 두 줄은 say_v1 3·5·13~16줄과 calc_out.txt A(1인·식대 비과세 월 20만) 숫자만 씀 → editor 설명란 서명 필요(desc_1115.txt)
import json, os, re, sys
sys.stdout.reconfigure(encoding='utf-8')
EP = os.path.dirname(os.path.abspath(__file__))
VID = os.path.normpath(os.path.join(EP, '..', '..', '..', '..', 'video'))
P = json.load(open(os.path.join(VID, 'n3.json'), encoding='utf-8'))
V = json.load(open(os.path.join(EP, 'voice.json'), encoding='utf-8'))
MP = os.path.join(EP, 'meta.json')
old = json.load(open(MP, encoding='utf-8')) if os.path.exists(MP) else {}
heads = [re.sub(r'^\[\d+\.\s*|\]$', '', h).strip() for h in re.findall(r'^## (.+)$', open(os.path.join(EP, 'script.md'), encoding='utf-8').read(), re.M)]
heads = [h for h in heads if not h.startswith('대조')][:9]
heads[0] = '예고'
starts, a = [0], 0
for s in P['scenes']:
    if s['kind'] == 'ask' and re.match(r'^\d+장$', (s.get('data') or {}).get('n', '')): starts.append(a)
    a += s['frames']
assert len(starts) == len(heads) == 9, (len(starts), len(heads), heads)
fps = P.get('fps', 30)
fmt = lambda f: f"{int(f / fps) // 60}:{int(f / fps) % 60:02d}"
chapters = [[round(st / fps), h] for st, h in zip(starts, heads)]
assert all(b[0] - a_[0] >= 10 for a_, b in zip(chapters, chapters[1:])), chapters
CH = '\n'.join(f"{fmt(st)} {h}" for st, h in zip(starts, heads))
credits = []
for c in json.load(open(os.path.join(EP, 'bg_used.json'), encoding='utf-8')):
    if c['desc_line'].startswith('end r41'):   # 끝 화면 n3_end_r41.png 바탕 = visual stock_credits.json window_dusk(8890683)
        credits.append('영상 일부: Yaroslav Shuraev / Pexels (https://www.pexels.com/video/woman-looking-through-a-glass-window-8890683/)')
    else: credits.append(c['desc_line'])
FIRST2 = ['연봉 5천이면 통장에는 한 달 357만원쯤 들어와요(본인 1인·식대 비과세 월 20만원, 2026년 보험료율·간이세액표 기준).',
          '국세청 2024년 귀속 근로소득 자료로 줄 세우면 연봉 5천은 직장인 백 명 중 앞에서 서른세 명 안이에요. 3천부터 1억까지 연봉이 천만원 오를 때 통장이 얼마 느는지도 셌습니다.']
TPL = '\n'.join(FIRST2) + '''

전체 표와 계산 근거(카페): {CAFE}
내 연봉 넣어 보기(파이어맵 월급 계산기): https://firemap.kr/calc/salary?utm_source=youtube&utm_medium=description&utm_campaign=n-3

{CHAPTERS}

출처
· 근로소득 백분위(천분위) 자료, 2024년 귀속: 국세청(공공데이터포털 15082063, '근로소득 백분위(천분위) 자료_20251231')
· 근로소득 간이세액표: 소득세법 시행령 별표 2(2026.2.27 개정) · 식대 월 20만원 이하 비과세: 소득세법 제12조 제3호 러목 · 세율·근로소득공제: 소득세법 제55조①·제47조①
· 국민연금 보험료율(2026년 9.5%, 근로자 절반 4.75%): 국민연금법 부칙 · 기준소득월액 상한 659만원(2026.7~2027.6): 국민연금공단
· 건강보험료율 7.19%: 국민건강보험법 시행령 제44조① · 장기요양보험료(건강보험료의 13.14%): 노인장기요양보험법 시행령 제4조 · 고용보험 실업급여 0.9%(근로자): 고용보험 및 산재보험 보험료징수법 시행령 제12조①2호
계산 가정: 통장 금액은 달마다 떼는 돈(간이세액 100%) 기준이고, 연말정산 뒤 실제 세금은 사람마다 다를 수 있어요 · 국세청 순위는 계약서 연봉이 아니라 총급여(비과세 뺀 돈) 기준, 구간마다 평균만 공개돼 '앞에서 몇 명 안'으로 읽었습니다.

내레이션은 AI 음성 내레이션(Google Cloud Text-to-Speech Chirp 3 HD)이에요. 숫자는 모두 위 원문에서 가져와 파이어맵이 계산했습니다. 정보 제공용이고, 특정 상품을 사거나 팔라는 권유가 아니에요.
썸네일 사진: Szymon Shields / Pexels (https://www.pexels.com/photo/aerial-view-of-pedestrians-walking-on-a-long-street-crossing-in-city-16456831/) (자르기·어둡게·글자 추가)
''' + '\n'.join(credits)
cafe = old.get('cafe_url') or 'https://cafe.naver.com/firemap'
m = dict(old)
m.update({
    'ep': 'N-3', 'series': '경제 — 연봉 실수령액',
    'title': '연봉 실수령액, 연봉 5천이면 통장엔 월 357만원… 직장인 100명 중 몇 번째일까',
    'title_by': 'firemap-copywriter 2026-10-27 copy/titles.md 1위(짝 비교 2승×2, 10/28 고친 판에도 1위 그대로)',
    'title_candidates': ['연봉 실수령액, 연봉 5천이면 통장엔 월 357만원… 직장인 100명 중 몇 번째일까',
                         '연봉 실수령액 3천부터 1억까지, 통장엔 월 얼마 들어오고 100명 중 몇 번째일까'],
    'thumb_text_top': '2024년 국세청 직장인 전체 연봉 순위',
    'thumb_text': '연봉 5천은 100명 중 / 위에서 33명 안에',
    'thumb': old.get('thumb') or os.path.join(EP, 'thumb_n3n_c2.png'),
    'thumb_status': 'visual 11/10 09:20 길이 칸 가림 고침(c → c2, 글자·사진 그대로) · 문구 = copy/titles.md 10/28 확정판 · 1초 시험 visual/N-3-thumb/judges.md · 사진 Pexels 16456831',
    'desc_first2': FIRST2,
    'desc_first2_src': 'say_v1 3·5줄(357만원쯤·앞에서 서른세 명 안)·13~16줄(식대 20만원)·calc_out.txt A(1인·식대 비과세 월 20만·간이세액 100%) · copywriter 남은 궁금증 "설명 첫 줄에 1인 기준" 반영',
    'tags': ['연봉 실수령액', '월급 실수령액', '연봉 1억 실수령액', '2026 연봉 실수령액표', '연봉 상위 몇 프로'],
    'desc_tpl': TPL, 'desc': TPL.replace('{CAFE}', cafe).replace('{CHAPTERS}', CH), 'chapters': chapters,
    'voice': f"Chirp 3 HD Charon {V['speakingRate']} · {V['done']}줄 · {V['seconds']}초 · editor 11/14 07:07 두 줄 다시 녹음·readback 통과",
    'missing': V['missing'],
    'publishAt': '2026-11-20T11:30:00+09:00',
    'privacy': 'private', 'privacy_note': '예약 공개(private+publishAt) — 정해진 시각에 공개로 바뀜',
    'paid': False, 'coupang': None, 'synthetic': True, 'veo': False,
    'synthetic_note': 'AI 음성 내레이션 → containsSyntheticMedia True (AI 생성 그림은 쓰지 않음 — 실사 Pexels 11개·판 자체 제작)',
    'answers': {
        'q1_바꿔끼우기': '아니오 — 2026년 간이세액표·보험료율로 3천~1억 일곱 칸 통장 금액을 직접 계산하고(calc_out.txt), 국세청 2024년 귀속 천분위 자료로 같은 연봉의 줄 위치를 셌다. 천만원 오를 때 통장에 남는 비율(76.3%·74.9% 등)은 남이 낸 숫자가 아니다.',
        'q2_연달아보기': '아니오 — 앞 편 S-1(주식, 11/18)·H-4(부동산, 11/14), 다음 편 W-3(주식, 11/22)과 축이 다르다(경제·연봉). 앞 연봉 편 N-1(상위 몇 %)과 질문이 다르다(세후 통장 금액·오를 때 느는 몫).',
        'q3_약속이행': "예 — 제목 '5천이면 통장엔 월 357만원… 100명 중 몇 번째'는 첫 30초에 357만원·앞에서 서른세 명 안으로 답하고, 2~8장이 사다리·빠지는 돈·오를 때 느는 몫·거꾸로 계산·가족 수 차이·평균과 상위 25%를 채운다.",
        'q4_조언으로들리나': "아니오 — 상품 권유 0. 할 일은 원천징수영수증 총급여로 내 자리 찾기, 부양가족 신고·원천징수 비율 고르기(제도), 계산기에 내 숫자 넣기까지다.",
        'q5_사람의몫': "예 — '연봉 = 계약서 숫자'라는 흔한 말을 국세청 총급여 기준으로 바로잡고(5천 → 4,760만원으로 섬), 국세청이 구간 평균만 낸다는 한계를 말하고 '앞에서 몇 명 안'으로만 읽었다.",
    },
    'endscreen': {'how': 'Studio 최종 화면 — 업로드 뒤 할 일(다음 편 또는 N-1)', 'status': '미정'},
    'made_by': 'firemap-video-producer', 'made_at': '2026-11-15',
    'video': os.path.join(VID, 'out', 'n3_ds.mp4'),
    'click_ok': [177.1],
    'click_ok_note': "177.1초('빠지는 돈의 구성이' 줄 가운데): 문장 wav clickscan 0, 완성본 175.8~179초 잘라 제미나이 gemini-3-flash-preview·3.5-flash 둘 다 '잡음 없음, 빠지는의 지' (PD 11/15 05시, check/ 기록)",
    'todo': '11/15 05시 PD: 렌더·deess·screen·bgcheck·bench_check 끝(out/n3_ds.mp4) · 남은 것: editor 설명란 서명(desc_1115.txt) → 올리기 전 확인(youtube-loop, 11/19) → gate → up publishAt 11/20 11:30 · 카페 짝 글 주소(cafe_url)',
})
json.dump(m, open(MP, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
open(os.path.join(EP, 'desc_1115.txt'), 'w', encoding='utf-8', newline='\n').write(m['desc'])
print('meta.json · 챕터', len(chapters), '· 설명', len(m['desc']), '자 · 실사 출처', len(credits), '· 빠진 줄', m['missing'])
print(CH)
