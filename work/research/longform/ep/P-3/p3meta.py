# P-3 meta.json — p3.json(장면 시각)·bg_used.json(실사 출처)·voice.json → meta.json 설명·챕터·5문항
#   py -3.12 work/research/longform/ep/P-3/p3meta.py   (p3props.py 다음에)
# 11/9 18시 PD: K-1 k1meta.py 꼴. 제목·썸네일·desc_first2는 meta.json 값 그대로(copywriter·visual·youtube-loop 몫) · {CAFE}는 짝 글 나오면 cafe_url 칸
import json, os, re, sys
sys.stdout.reconfigure(encoding='utf-8')
EP = os.path.dirname(os.path.abspath(__file__))
VID = os.path.normpath(os.path.join(EP, '..', '..', '..', '..', 'video'))
P = json.load(open(os.path.join(VID, 'p3.json'), encoding='utf-8'))
V = json.load(open(os.path.join(EP, 'voice.json'), encoding='utf-8'))
MP = os.path.join(EP, 'meta.json')
old = json.load(open(MP, encoding='utf-8'))
heads = [re.sub(r'^\[?0\.\s*|^\d+\.\s*|\]$', '', h).strip() for h in re.findall(r'^## (.+)$', open(os.path.join(EP, 'script.md'), encoding='utf-8').read(), re.M)]
heads = [h.replace('"', '') for h in heads if not h.startswith('대조')]
heads[0] = '예고'
starts, a = [0], 0
for s in P['scenes']:
    if s['kind'] == 'ask' and re.match(r'^\d+장$', s['data'].get('n', '')): starts.append(a)
    a += s['frames']
assert len(starts) == len(heads) == 9, (len(starts), len(heads), heads)
fps = P.get('fps', 30)
fmt = lambda f: f"{int(f / fps) // 60}:{int(f / fps) % 60:02d}"
chapters = [[round(st / fps), h] for st, h in zip(starts, heads)]
assert all(b[0] - a_[0] >= 10 for a_, b in zip(chapters, chapters[1:])), chapters
CH = '\n'.join(f"{fmt(st)} {h}" for st, h in zip(starts, heads))
credits = [c['desc_line'] for c in json.load(open(os.path.join(EP, 'bg_used.json'), encoding='utf-8'))]
TPL = '\n'.join(old['desc_first2']) + '''

전체 표와 계산 근거(카페): {CAFE}

{CHAPTERS}

출처
· 피부양자 소득·재산 기준(연 2천만원·재산 과표 5억 4천만원·9억원, 부부 모두 충족): 국민건강보험법 시행규칙 [별표 1의2]
· 공적연금은 그해 받은 연금 전부를 소득으로 봄·소득 반영 시기·보험료율: 국민건강보험법 시행령 제41조·제44조
· 분리과세 이자·배당 1천만원 이하 합산 안 함·지역가입자 연금 50% 반영·피부양자 탈락자 경감(2026년 8월분 끝): 국민건강보험법 시행규칙 제44조·부칙<제907호> 제3조
· 2026년 보험료율 7.19%·재산 점수당 211.5원: 국민건강보험공단 2025.12.26 안내
· 장기요양보험료 건강보험료의 13.14%: 보건복지부 2025.11.4 보도자료
· 국민연금 2026년 2.1% 인상: 보건복지부 2026.1.9 보도자료
· 연금저축·IRP 같은 사적연금은 피부양자 소득에 넣지 않음: 국민건강보험공단 웹진 2023.9
계산 가정: 지역가입자 건강보험료는 연금 소득분만(재산이 거의 없을 때) · 2026년 요율 · 연금은 해마다 2.1%씩 오른다고 둔 경우 · 실제 보험료는 재산·다른 소득에 따라 다르니 공단(1577-1000)에서 내 금액을 확인하세요.

내레이션은 AI 음성 내레이션(Google Cloud Text-to-Speech Chirp 3 HD)이고, 일부 장면은 AI로 만든 그림(RealVisXL V5.0 — 식탁 위 돋보기와 찻잔·고지서와 돋보기·창가 찻잔과 접힌 고지서, 얼굴·글자 없음)입니다. 숫자는 모두 위 원문에서 가져와 파이어맵이 계산했습니다. 제도 설명이며 개별 상담이 아닙니다.
''' + '\n'.join(credits)
cafe = old.get('cafe_url') or 'https://cafe.naver.com/firemap'
m = dict(old)
m.update({
    'desc_tpl': TPL, 'desc': TPL.replace('{CAFE}', cafe).replace('{CHAPTERS}', CH), 'chapters': chapters,
    'voice': f"Chirp 3 HD Charon {V['speakingRate']} · {V['done']}줄 · {V['seconds']}초 · 2026-11-03 녹음·11/9 새 줄 32·0:2 다시 받기(editor 11/9 07:06 서명 say 4c0cbd01)",
    'missing': V['missing'],
    'publishAt': '2026-11-12T11:30:00+09:00',
    'answers': {
        'q1_바꿔끼우기': "아니오 — '피부양자 기준 2천만원' 법 조문 읽기가 아니라, 월 167만원이면 매달 67,926원·170·180·200만원 줄, 이자·배당 1,100만원이 섞이면 월 10만 8천원, 3년 미뤄 한 해 1,896만원인 연금도 해마다 2.1%씩 세 번 오르면 2,018만원으로 넘는다는 것을 2026년 요율로 직접 셌다(calc_out.txt).",
        'q2_연달아보기': '아니오 — 앞 편 K-1(금리, 경제·11/10)·다음 편 H-4(부동산·11/14)와 축이 다르다(정책·건보료). 앞 정책 편 J-1(종부세, 11/4)과 8일 간격.',
        'q3_약속이행': "예 — 제목 '국민연금 월 166만원 넘으면 건보료 매달 얼마'는 1장(문턱 2천만원=월 166만 6,667원)·2장(월 167만원 → 6만 8천원쯤, 170·180·200만원)이 답하고, 3~6장이 경감 끝·판정 시기·이자 섞임·재산·부부를 채운다.",
        'q4_조언으로들리나': "아니오 — 연금을 당겨 받으라·미루라·상품 가입 0. 7장은 당겨 받기를 '보험료 몇만원과 평생 연금을 맞바꾸는 선택, 어느 쪽이 나은지는 사람마다 다름'으로 숫자만 보여 주고, 할 일은 '통지서를 꺼내 내년 연금으로 셈해 보기'(8장)·'선 근처면 공단 고객센터에 먼저 묻기'(5장)까지다.",
        'q5_사람의몫': "예 — 2026년 8월분으로 끝난 경감 규정을 부칙에서 확인해 예전 기사 계산(80·60·40·20%)이 지금은 틀렸다고 바로잡고, 물가 인상만으로 저절로 넘는 해를 처음 셌다.",
    },
    'endscreen': {'how': 'Studio 최종 화면 — 업로드 뒤 할 일(다음 편 H-4 또는 J-1)', 'status': '미정'},
    'video': os.path.join(VID, 'out', 'p3_ds.mp4'),
    'todo': '11/9 18시 PD p3meta: desc·chapters·answers·publishAt 11/12 채움 · 남은 것: 렌더(check/render_parts_1109.sh)→deess→loudnorm→bgcheck·올리기 전 확인(youtube-loop 11/11, 1일 안)·gate·up·카페 짝 글 주소(cafe_url)',
})
json.dump(m, open(MP, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('meta.json · 챕터', len(chapters), '· 설명', len(m['desc']), '자 · 실사 출처', len(credits), '· 빠진 줄', m['missing'])
print(CH)
