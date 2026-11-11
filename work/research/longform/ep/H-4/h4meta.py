# H-4 meta.json — h4.json(장면 시각)·bg_used.json(실사 출처)·voice.json·copy/titles.md 2차 → meta.json 제목·설명·챕터·5문항
#   py -3.12 work/research/longform/ep/H-4/h4meta.py   (h4props.py 다음에)
# 11/11 PD(정기 20:4x): p3meta.py 꼴. 제목·썸네일 글·설명 첫 줄·태그는 copywriter copy/titles.md 2026-10-29 판 그대로(지어내지 않음),
#   썸네일 파일은 visual 11/11 09:20 thumb_h4n_g5.png(길이 칸 가림 고침) · {CAFE}는 짝 글 나오면 cafe_url 칸
import json, os, re, sys
sys.stdout.reconfigure(encoding='utf-8')
EP = os.path.dirname(os.path.abspath(__file__))
VID = os.path.normpath(os.path.join(EP, '..', '..', '..', '..', 'video'))
P = json.load(open(os.path.join(VID, 'h4.json'), encoding='utf-8'))
V = json.load(open(os.path.join(EP, 'voice.json'), encoding='utf-8'))
MP = os.path.join(EP, 'meta.json')
old = json.load(open(MP, encoding='utf-8')) if os.path.exists(MP) else {}
heads = [re.sub(r'^\[?0\.\s*|^\d+\.\s*|\]$', '', h).strip() for h in re.findall(r'^## (.+)$', open(os.path.join(EP, 'script.md'), encoding='utf-8').read(), re.M)]
heads = [h.replace('"', '') for h in heads if not h.startswith('대조')][:7]
heads[0] = '예고'
starts, a = [0], 0
for s in P['scenes']:
    if s['kind'] == 'ask' and re.match(r'^\d+장$', s['data'].get('n', '')): starts.append(a)
    a += s['frames']
assert len(starts) == len(heads) == 7, (len(starts), len(heads), heads)
fps = P.get('fps', 30)
fmt = lambda f: f"{int(f / fps) // 60}:{int(f / fps) % 60:02d}"
chapters = [[round(st / fps), h] for st, h in zip(starts, heads)]
assert all(b[0] - a_[0] >= 10 for a_, b in zip(chapters, chapters[1:])), chapters
CH = '\n'.join(f"{fmt(st)} {h}" for st, h in zip(starts, heads))
credits = [c['desc_line'] for c in json.load(open(os.path.join(EP, 'bg_used.json'), encoding='utf-8'))]
FIRST2 = ['광명 84㎡ 매매 실거래(2026년 7~9월 계약)를 서울 25개 구와 같은 잣대(가운데 값)로 줄 세웠어요. 광명보다 싼 서울 구 8곳도, 철산자이더헤리티지 전세와 옆 단지 매매도 봤습니다.',
          '광명 전체로는 26곳 가운데 18번째였고, 2019년 뒤 지은 단지만 보면 가운데 값이 15억 가까이였어요.']
TPL = '\n'.join(FIRST2) + '''

전체 표와 계산 근거(카페): {CAFE}
파이어맵: https://firemap.kr/?utm_source=youtube&utm_medium=description&utm_campaign=h-4

{CHAPTERS}

출처
· 아파트 매매·전월세 실거래(신규·갱신 구분): 국토교통부 실거래가 공개시스템(rt.molit.go.kr)·공공데이터포털 국토교통부 아파트 매매/전월세 실거래 자료 — 광명시 2025년 11월~2026년 10월 계약, 서울 25개 구 2026년 7~9월 계약, 2026-10-16 받음
· 철산주공13단지·12단지 정비구역 지정: 경기도 광명시 고시 제2025-105호·제2025-190호(토지이음)
· 광명 조정대상지역·투기과열지구, 주택담보대출 한도(15억 이하 6억·15억 초과 4억): 관계부처 합동 '주택시장 안정화 대책'(2025-10-15, 정책브리핑)
· 토지거래허가구역 2025-10-20~2026-12-31: 국토교통부공고 제2025-1219호(경기도 토지거래허가구역 지정 현황)
· 허가 대상(매매 같은 소유권 이전 계약, 임대차 아님): 부동산 거래신고 등에 관한 법률 제11조
· 단지 검색 수: 네이버 검색광고 키워드 도구(한 달 검색 수)
계산 가정: 84㎡대 = 전용 80~85㎡ · 값은 거래를 줄 세운 가운데 값 · 분양권 거래는 매매 실거래에 들어 있지 않음 · 실제 대출 한도는 소득·다른 대출에 따라 다르니 은행에서, 허가·실거주 의무 세부 조건은 광명시청에서 확인하세요.

내레이션은 AI 음성 내레이션(Google Cloud Text-to-Speech Chirp 3 HD)이고, 일부 장면은 AI로 만든 그림(RealVisXL V5.0 — 오래된 아파트 계단, 사람·글자 없음)입니다. 숫자는 모두 위 원문에서 가져와 파이어맵이 계산했습니다. 시세 설명이고, 특정 단지를 사거나 팔라는 권유는 아니에요.
''' + '\n'.join(credits)
cafe = old.get('cafe_url') or 'https://cafe.naver.com/firemap'
m = dict(old)
m.update({
    'ep': 'H-4', 'series': '부동산 — 광명 실거래',
    'title': '광명 아파트 서울보다 비싸다? 15억은 2019년 뒤 지은 단지 이야기였다',
    'title_by': 'firemap-copywriter 2026-10-29 18:52 copy/titles.md 1위(37자·숫자 2·검색어 광명아파트 맨 앞)',
    'title_candidates': ['광명 아파트 서울보다 비싸다? 15억은 2019년 뒤 지은 단지 이야기였다', '광명 아파트 서울보다 비싸다? 그 말은 2019년 뒤 지은 단지 이야기였다'],
    'thumb_text_top': '광명 아파트 15억이라던데, 실거래 세어 보니',
    'thumb_text': '서울 25개 구 중 / 17곳이 광명보다 비쌌다',
    'thumb': os.path.join(EP, 'thumb_h4n_g5.png'),
    'thumb_status': '11/11 09:20 visual 길이 칸 가림 고침(g3 → g5, 글자·사진 그대로)',
    'desc_first2': FIRST2,
    'desc_first2_src': 'copy/titles.md 2026-10-29 설명 첫 줄 + 대본 3·34~36행(18번째·2019년 뒤 단지 15억 가까이)',
    'tags': ['광명아파트', '광명 실거래가', '철산자이더헤리티지', '하안주공', '철산동 아파트'],
    'desc_tpl': TPL, 'desc': TPL.replace('{CAFE}', cafe).replace('{CHAPTERS}', CH), 'chapters': chapters,
    'voice': f"Chirp 3 HD Charon {V['speakingRate']} · {V['done']}줄 · {V['seconds']}초 · 11/10 녹음 88줄 + 11/11 보강 36줄(editor 11/11 07:06 서명 say 54265c8e)·0:1·5:6 다시 받기",
    'missing': V['missing'],
    'publishAt': '2026-11-14T11:30:00+09:00',
    'privacy': 'private', 'privacy_note': '예약 공개(private+publishAt) — 정해진 시각에 공개로 바뀜',
    'paid': False, 'coupang': None, 'synthetic': True, 'veo': False,
    'synthetic_note': 'AI 음성 내레이션 + shot_plan.md의 AI 생성 장면(old_stair) → containsSyntheticMedia True',
    'answers': {
        'q1_바꿔끼우기': '아니오 — 광명 84㎡대 매매 171건을 서울 25개 구와 같은 석 달·같은 크기·가운데 값으로 줄 세워 26곳 중 18번째, 2019년 뒤 단지만 떼면 영등포구 위, 철산동 안 16억~6억 사다리와 신규·갱신 전세 차이를 국토교통부 원자료로 직접 셌다(calc_out.txt·calc_renew_out.txt).',
        'q2_연달아보기': '아니오 — 앞 편 P-3(정책·건보료, 11/12)·다음 편 N-3(연봉, 11/16)과 축이 다르다(부동산). 앞 부동산 편 H-3과 다른 지역·다른 질문(서울 비교).',
        'q3_약속이행': "예 — 제목 '서울보다 비싸다? 15억은 2019년 뒤 지은 단지 이야기'는 1장(26곳 중 18번째)·2장(2019년 뒤 단지 가운데 값 15억 가까이, 영등포구 위)이 답하고, 3~5장이 동 안 사다리·9억 예산·대출 한도와 허가를 채운다.",
        'q4_조언으로들리나': "아니오 — 특정 단지를 사라·팔라 0. 4장 끝은 '새 집에 세 들어 살지, 오래된 집을 내 집으로 가질지는 각자 정할 일', 할 일은 같은 동·같은 크기 1년 실거래 보기·계약 전 허가와 은행 한도 확인까지다.",
        'q5_사람의몫': "예 — '광명 15억' 말이 어디서 왔는지(새 단지 구성 차이)를 원자료로 갈라 보이고, 매매 실거래 0건인 인기 단지(분양권)와 신규·갱신 전세가 꼭 갱신이 싸지 않다는 것을 처음 셌다.",
    },
    'endscreen': {'how': 'Studio 최종 화면 — 업로드 뒤 할 일(다음 편 N-3 또는 H-3)', 'status': '미정'},
    'made_by': 'firemap-video-producer', 'made_at': '2026-11-11',
    'video': os.path.join(VID, 'out', 'h4_ds.mp4'),
    'todo': '11/11 21시 PD h4meta: 제목·설명·챕터·5문항·publishAt 11/14 · 남은 것: editor screen_text stamp → 렌더 → deess → screen·bgcheck → 올리기 전 확인(youtube-loop, 1일 안) → gate → up · 카페 짝 글 주소(cafe_url)',
})
json.dump(m, open(MP, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('meta.json · 챕터', len(chapters), '· 설명', len(m['desc']), '자 · 실사 출처', len(credits), '· 빠진 줄', m['missing'])
print(CH)
