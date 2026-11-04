# K-1 meta.json — k1.json(장면 시각)·bg_used.json(실사 출처)·voice.json(빠진 줄) → meta.json 설명·챕터·5문항
#   py -3.12 work/research/longform/ep/K-1/k1meta.py   (k1props.py 다음에 · 다시 녹음·렌더 뒤 챕터 시각이 바뀌면 다시)
# 11/4 PD: j1meta.py 꼴. 제목·썸네일·desc_first2·첫 댓글은 meta.json에 있는 값 그대로(copywriter·visual·youtube-loop 몫) · {CAFE}는 짝 글 나오면 cafe_url 칸
import json, os, re, sys
sys.stdout.reconfigure(encoding='utf-8')
EP = os.path.dirname(os.path.abspath(__file__))
VID = os.path.normpath(os.path.join(EP, '..', '..', '..', '..', 'video'))
P = json.load(open(os.path.join(VID, 'k1.json'), encoding='utf-8'))
V = json.load(open(os.path.join(EP, 'voice.json'), encoding='utf-8'))
MP = os.path.join(EP, 'meta.json')
old = json.load(open(MP, encoding='utf-8'))
heads = [re.sub(r'^\[?0\.\s*|^\d+\.\s*|\]$', '', h).strip() for h in re.findall(r'^## (.+)$', open(os.path.join(EP, 'script.md'), encoding='utf-8').read(), re.M)]
heads[0] = '예고'
starts, a = [0], 0
for s in P['scenes']:
    if s['kind'] == 'ask' and re.match(r'^\d+장$', s['data'].get('n', '')): starts.append(a)
    a += s['frames']
assert len(starts) == len(heads) == 7, (len(starts), len(heads), heads)
fmt = lambda f: f"{int(f / 30) // 60}:{int(f / 30) % 60:02d}"
chapters = [[round(st / 30), h] for st, h in zip(starts, heads)]
assert all(b[0] - a_[0] >= 10 for a_, b in zip(chapters, chapters[1:])), chapters
CH = '\n'.join(f"{fmt(st)} {h}" for st, h in zip(starts, heads))
credits = [c['desc_line'] for c in json.load(open(os.path.join(EP, 'bg_used.json'), encoding='utf-8'))]
FIRST2 = old['desc_first2']
TPL = '\n'.join(FIRST2) + '''

전체 표와 계산 근거(카페): {CAFE}

{CHAPTERS}

출처
· 미국 10년 국채금리: FRED DGS10·GS10(미 연준 H.15), 2026년 9월분·일별 10월 중순까지
· 한국 국고채 3·10년: 한국은행 경제통계시스템(ECOS) 721Y001·817Y002, 2026년 9월분
· 정기예금·주택담보대출(전체·고정형·변동형) 신규취급액 가중평균 금리: ECOS 121Y002·121Y006, 2025년 9월분과 2026년 9월분 비교
· COFIX(신규취급액·잔액·신잔액): 은행연합회 소비자포털 COFIX 공시, 2026년 9월분(10/15 공시)
· 한국은행 기준금리: ECOS 722Y001
계산 가정: 이자 세금 15.4% · 대출 3억원·30년 원리금균등 · '2021년 여름 고정형으로 빌린 대출'은 2021년 8월 고정형 평균 금리로 빌려 5년 뒤 남은 돈을 2026년 9월 평균 금리로 다시 정한 경우로 셈(은행·개인마다 다름) · 평균 금리라 내 통장·대출 금리와 다를 수 있습니다.

내레이션은 AI 음성 내레이션(Google Cloud Text-to-Speech Chirp 3 HD)이고, 일부 장면은 AI로 만든 그림(RealVisXL V5.0 — 번호표 쥔 손·식탁 위 휴대폰과 찻잔·열쇠와 서류 봉투·휴대폰 스크롤·창가 의자, 얼굴·글자 없음)입니다. 숫자는 모두 위 원문에서 가져와 파이어맵이 계산했습니다. 지나간 값을 비교한 자료이며 금리 전망이나 예금·대출 상품 가입 권유가 아닙니다.
''' + '\n'.join(credits)
cafe = old.get('cafe_url') or 'https://cafe.naver.com/firemap'
m = dict(old)
m.update({
    'desc_tpl': TPL, 'desc': TPL.replace('{CAFE}', cafe).replace('{CHAPTERS}', CH), 'chapters': chapters,
    'voice': f"Chirp 3 HD Charon {V['speakingRate']} · {V['done']}줄 · {V['seconds']}초 · 2026-11-03 녹음·11/4 02:21 3:15 다시 받기(editor 11/3 23:14 서명 say_v1)",
    'missing': V['missing'],
    'answers': {
        'q1_바꿔끼우기': "아니오 — 금리 '오른다·내린다' 뉴스 요약이 아니라, 한은 9월분 평균 금리로 1억 예금 세금 뗀 이자 +87만원·3억 대출 고정형 +21만원·2021년 고정 끝난 대출 +31만원을 우리 계산기로 셌다. 미국 10년(+0.9%p)과 한국 10년(+1.6%p)을 같은 1년 창으로 맞대 '미국 따라 올랐나'에 답한 편은 경쟁 목차에 없다(toc_compare).",
        'q2_연달아보기': '아니오 — 앞 편 J-1(종부세, 정책·11/4)·다음 편 P-3(건보료, 정책·11/8)과 축이 다르다(경제·금리). 앞 경제 편 X-1(환율, 10/22)과 2주 간격.',
        'q3_약속이행': "예 — 제목 '미국 국채금리 5%, 내 예금 이자·대출 이자는 정말 미국 따라 올랐을까?'는 2장(예금 +87만원)·3장(대출 고정형·변동형)·4장(미국 +0.9%p vs 한국 +1.6%p, 기준금리 두 번)이 답한다.",
        'q4_조언으로들리나': "아니오 — 예금 넣으라·대출 갈아타라·고정/변동 고르라 0, 금리 전망 0. 6장은 '내 예금 만기일·대출 고정 기간 끝나는 날을 확인'까지만 말하고, 평균 금리라 내 금리와 다를 수 있다고 말한다.",
        'q5_사람의몫': "예 — 같은 1년 미국·한국 금리 창을 9월분끼리 맞추고(8월판에서 맞던 '미국 절반도 안'이 9월분에선 틀려 지움), 2021년 여름 고정 대출이 다시 정해질 때의 한 달 차이를 원리금 식으로 처음 셌다.",
    },
    'endscreen': {'how': 'Studio 최종 화면 — 업로드 뒤 할 일(다음 편 P-3 또는 X-1 WcBOePkyOOQ)', 'status': '미정'},
    'video': os.path.join(VID, 'out', 'k1.mp4'),
    'todo': '11/4 14:3x PD k1meta: desc·chapters·answers·missing 채움 · 남은 것: 렌더(editor 화면 재서명 뒤 check/render_parts_1104.sh)·readback·올리기 전 확인(youtube-loop 11/5 오전)·카페 짝 글 주소(cafe_url) · 렌더 뒤 이 파일 다시 돌림(챕터 시각 k1.json 그대로면 같음)',
})
json.dump(m, open(MP, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('meta.json · 챕터', len(chapters), '· 설명', len(m['desc']), '자 · 실사 출처', len(credits), '· 빠진 줄', m['missing'])
print(CH)
