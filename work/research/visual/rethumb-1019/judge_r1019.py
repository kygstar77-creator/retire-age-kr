# 10/19 저조 롱폼 재썸네일 심사 — C-2-thumb/n1019/judge_n1019.py(= P-1-thumb/judge_1014.py 방식) 복사.
#   모델 하나 고정(gemini-3.1-flash-lite, judge-drift-1006), 비교판 168px·480px 2장, 1~10(6=경쟁 평균·7=통과·8=목표), 지금 공개판(now)과 같이 채점.
#   경쟁은 편마다 visual/<편>-thumb/compare.json '경쟁'(없는 편은 가까운 주제 편 것, COMP_FROM 칸).
#   py -3.12 judge_r1019.py <편키>   → judge/<편키>_board168.png·_board480.png·_score.md, 점수는 judge/scores.json에 누적
import sys, os, json, base64, urllib.request, re
from PIL import Image, ImageDraw, ImageFont
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__)); VIS = os.path.dirname(H)
EPD = os.path.join(VIS, '..', 'longform', 'ep'); J = os.path.join(H, 'judge'); os.makedirs(J, exist_ok=True)
REF = os.path.join(EPD, 'N-2', 'pilot', 'preview', 'thumb_A.png')
F = ImageFont.truetype(r'C:\Windows\Fonts\malgunbd.ttf', 13)
KEY = [l.split('=', 1)[-1].strip() for l in open(r'C:\Users\강영준\Documents\gemini_key.txt', encoding='utf-8-sig') if l.strip()][0]
MODEL = os.environ.get('JUDGE_MODEL', 'gemini-3.1-flash-lite')

# 편키: (ep 폴더, 경쟁 가져올 thumb 폴더, 제목, 영상 내용, 지금 판 글자)
EP = {
    'W-1': ('W-1', 'W-1', '삼성전자 주주라면 지난주 사흘, 분기 배당 44번치가 평가액에서 빠졌다',
            '지나간 주(2026년 10월 2일→8일, 3분기 잠정 영업이익 107.4조 발표 주) 삼성전자 주가 −5.07%, 100주 평가액 2,760만→2,620만원(−140만원) = 100주 분기 배당 세후 3만 1,640원의 44.2배. 지금(10월 19일) 시황이 아니라 지나간 주 계산.',
            '"삼성전자 10/2~10/8 / 영업이익 107조(잠정)인데 / 내 100주 −140만"'),
    'W-1-2': (os.path.join('W-1', 'w1016'), 'W-1', '삼성전자 주가 수요일 종가, 회사가 15조원에 산 자사주 평균값보다 12% 낮았다',
              '지나간 주: 삼성전자 10월 8일 262,000원 → 10월 14일 232,000원(사흘 −11.45%), 100주 평가액 −300만원. 회사가 8/24~10/6에 15조원어치 산 자사주 평균 263,823원보다 12.06% 낮음. 싸다는 뜻·매수 신호 아님이라고 영상이 밝힘.',
              '"삼성전자 100주 월~수 / 300만원 줄었다"'),
    'G-1': ('G-1', 'G-1', '금 1천만원어치, 내가 산 날에 따라 지금 얼마 남았을까?',
            'KRX 금시장 기준, 2026년 1월 29일 1년 꼭대기에 1천만원어치 산 금이 10월 6일 종가로 6,634,298원(−33.66%). 산 값까지 되돌아가려면 +50.7%(전망 아닌 산수). 산 날 4개 × 산 길 4개(KRX·ETF·골드뱅킹·골드바) 비교. 지나간 값 계산.',
            '"금 1월 고점에 샀다면 / 선 그래프 / −33.7% KRX 금시장"'),
    'P-1': ('P-1', 'P-1', '국민연금 일찍 받으면 몇 살부터 손해일까? 5년·1년 당겨 계산해 보니',
            '1969년생·월 100만원 가정, 조기 감액률로 계산하면 5년 일찍(60세) 받으면 76.7세부터, 1년 일찍(64세) 받으면 80.7세부터 제때(65세) 받은 쪽의 받은 돈 합계가 더 많아짐. 언제 받으라고 권하지 않음.',
            '"국민연금·1969년생(65세 수령) 기준 / 일찍 받으면 몇 살부터 손해? / 5년 일찍 76.7세부터 · 1년 일찍 80.7세부터"(칸 2개 카드)'),
    'M-1': ('M-1', 'M-1', '배당으로 매달 100만원 받으려면 얼마 있어야 할까, 세금·건보료 떼고 거꾸로 계산 (JEPQ·SCHD·ACE)',
            '세금·건보료 뗀 월 100만원 분배에 드는 원금: JEPQ 1.38억, SCHD 4.85억, ACE 미국배당다우존스 5.10억(가장 적은 달 기준이면 8.92억, 1.75배). SCHD는 3달에 한 번 들어옴.',
            '"통장엔 평균이 안 들어온다 / 막대그래프 / 8.92억 필요"'),
    'D-1': ('D-1', 'D-1', '퇴직 후 배당·이자로 생활한다면 꼭 봐야 할 건보료 선, 넘으면 1년 54만원 넘게 더',
            '지역가입자 1인·다른 소득 0 가정, 연 금융소득(배당·이자) 1,000만원이면 월 건보료 22,800원, 1,001만원이면 67,850원(2.98배) — 1만원 차이에 1년 약 54만원 더.',
            '"이자·배당 1만원 차이 건보료 약 3배 / 막대 2.3만·6.8만"'),
    'E-1': ('E-1', 'W-1', 'SK하이닉스 주가가 오른 만큼 이익도 늘었을까? 삼성전자·마이크론까지 공시로 맞춰 봤다',
            '2025.9.29→2026.9.29 1년 주가: SK하이닉스 5.13배(+412.9%), 그 안 최대 낙폭 −54.7%. 2분기 영업이익은 1년 전 같은 분기의 6.57배(삼성 19.14배, 마이크론 11.97배). 공시 원문 비교. 지나간 1년 계산.',
            '"SK하이닉스 1년 +412.9% / 그중 6/22→7/30 −54.7% / 선 그래프 2개"'),
    'E-2': ('E-2', 'E-2', '테슬라 주주라면 볼 2분기 장부, 영업이익보다 이자수익이 더 컸다',
            '테슬라 2026년 2분기 10-Q: 이자수익 4억 2,200만 달러가 영업이익 3억 9,800만 달러보다 큼(이자수익 총액 기준). 매출 282억 달러 10분기 최대, 영업이익률 1.4% 10분기 최저.',
            '"테슬라 매출 늘었는데 영업이익률 1.4% / 막대그래프 10분기 최저"'),
    'J-gSK': ('june-gSKsQWjTabo', 'C-2', '파이어 같은 건 결국 환상이었어',
              '14억을 모아 조기은퇴한 파이어족이 1년 만에 회사로 돌아간 사례 분석 — 돈이 부족해서가 아니었음. 은퇴자 자산 바닥 이유(순서 위험·물가·의료비), 안 돌아오는 3가지 준비.',
              '"파이어 같은 건 결국 환상이었어 / 해변 의자 위 막대 인형 그림·14억 돈자루"(AI풍 그림)'),
    'J-cxl': ('june-cxls2Ve18-k', 'C-2', '배당금만으로 사는 삶, 정말 가능할까요?',
              '배당금만으로 사는 삶은 큰돈을 가진 사람이 아니라 작은 돈을 오래 지킨 사람의 이야기 — 왜 가능한지, 무엇부터, 많은 사람이 놓치는 "6억의 함정".',
              '"배당금만으로 사는 삶 정말 가능할까요? / 금화 더미 위 만두 인형 그림"(AI풍 그림)'),
    'J-JVT': ('june-JVTYZ208hgw', 'W-1', '투자 재능 없는 사람이 QQQM으로 5년 뒤 파이어하는 법',
              '4년 동안 전기차·코인·배당·채권 투자로 거의 다 잃은 사람이 종목 고르기를 그만두고 나스닥100 추종 QQQM 하나만 모음. 시뮬레이션상 5년 뒤 일을 그만둘 수 있음. 투자 권유 아님.',
              '"투자 재능 없는데 5년 뒤 파이어 방법은 QQQM 하나 / 흰 고양이 그림"(AI풍 그림)'),
    'J-wwf': ('june-wwfFszPl06g', 'W-1', 'QQQM 딱 하나로 파이어하는 법',
              'QQQM 하나에 매달 꾸준히 넣고, 은퇴(파이어)하면 필요한 만큼만 파는 전략 — 이 단순한 길을 택한 이유와 빛과 그림자. 투자 권유 아님.',
              '"QQQM 딱 하나면 파이어 끝 / 흰 고양이 그림·NASDAQ 100 팻말"(AI풍 그림)'),
    'J-zhT': ('june-zhTjJwy1mwQ', 'W-1', 'QQQM과 SCHD 파이어 시뮬레이션 결과는?',
              '파이어(조기 은퇴) 자금을 성장의 QQQM으로 모을지 배당의 SCHD로 모을지, 실제 25년 데이터로 거치식·적립식 시뮬레이션 비교.',
              '"QQQM vs SCHD 팻말 든 흰 고양이 / 성장이냐 VS 배당이냐"(AI풍 그림)'),
}


def comp(folder):
    p = os.path.join(VIS, folder + '-thumb')
    return {c['id']: os.path.join(p, 'src', c['id'] + '.jpg') for c in json.load(open(os.path.join(p, 'compare.json'), encoding='utf-8')) if c.get('who') == '경쟁'}


def fitim(p, W):
    im = Image.open(p).convert('RGB'); w, h = im.size; t = round(w * 9 / 16)
    if t < h: im = im.crop((0, (h - t) // 2, w, (h - t) // 2 + t))
    return im.resize((W, round(W * 9 / 16)), Image.LANCZOS)


def boards(k):
    folder, cf = EP[k][0], EP[k][1]
    ours = {'now': os.path.join(EPD, folder, 'thumb_before_1019.png'), 'r19a': os.path.join(EPD, folder, 'thumb_r19a.png'), 'r19b': os.path.join(EPD, folder, 'thumb_r19b.png')}
    items = [(n, p, f'우리 {n}') for n, p in ours.items()] + [('N-2', REF, '우리 다른 편(기준)')] + [(c, p, '경쟁') for c, p in list(comp(cf).items())[:5]]
    out = []
    for W, name in ((168, 'board168.png'), (480, 'board480.png')):
        HH = round(W * 9 / 16); cols = 3; pad = 12; rows = (len(items) + cols - 1) // cols
        bd = Image.new('RGB', (cols * (W + pad) + pad, rows * (HH + 30) + pad), 'white'); d = ImageDraw.Draw(bd)
        for n, (key, p, lab) in enumerate(items):
            x = pad + (n % cols) * (W + pad); y = pad + (n // cols) * (HH + 30)
            bd.paste(fitim(p, W), (x, y)); d.text((x, y + HH + 4), lab, fill='black', font=F)
        fn = os.path.join(J, f'{k}_{name}'); bd.save(fn); out.append(fn)
    return out


def ask(text, paths):
    parts = [{'text': text}] + [{'inline_data': {'mime_type': 'image/png', 'data': base64.b64encode(open(p, 'rb').read()).decode()}} for p in paths]
    r = json.load(urllib.request.urlopen(urllib.request.Request(f'https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={KEY}',
        data=json.dumps({'contents': [{'parts': parts}]}).encode(), headers={'Content-Type': 'application/json'}), timeout=240))
    return f'[모델 {MODEL}]\n' + r['candidates'][0]['content']['parts'][0]['text']


def parse(out):
    """'점수' 줄마다 그 앞에서 가장 가까이 나온 시안 이름(now·r19a·r19b)에 붙인다(모델이 머리글 꼴을 바꿔도 읽히게)."""
    sc = {}
    for m in re.finditer(r'점수\W{0,6}(\d+(?:\.\d)?)', out):
        ls = out.rfind('\n', 0, m.start()) + 1
        # 머리글(#) 줄이면 그 줄의 이름, 아니면 줄 앞 머리글의 이름(모델이 본문에 서식 견본 'r19a 점수'를 베끼는 일이 있어서)
        names = list(re.finditer(r'\b(now|r19a|r19b)\b', out[:m.start()] if out[ls:].lstrip().startswith('#') else out[:ls]))
        if names and names[-1].group(1) not in sc: sc[names[-1].group(1)] = float(m.group(1))
    return sc


def score(k):
    folder, cf, title, body, now_txt = EP[k]
    paths = boards(k)
    t = ('한국 재테크 유튜브 썸네일 심사입니다. 이미지 2장 = 같은 비교판(1장째 휴대폰 목록 크기 168px, 2장째 480px). "우리 now"는 지금 공개된 판, "우리 r19a·r19b"는 바꿀 후보, '
         '"우리 다른 편(기준)"은 채널 주인이 좋다고 고른 다른 편 썸네일(같은 꼴인지 보는 기준), "경쟁"은 같은·가까운 주제 상위작.\n'
         f'영상 내용: {body}\n제목(썸네일 옆에 같이 보임, 바꾸지 않음): "{title}".\n지금 판(now) 글자: {now_txt}.\n'
         '시청자는 50~60대. 제약: 얼굴 정면 사진 금지(손·뒷모습은 됨), 과장·낚시·권유 금지, 영상 내용과 어긋나는 말 금지, 지나간 시황 값을 지금 값처럼 보이게 하면 감점, 오른쪽 아래 비움. '
         '채널 주인 평: 위 머리띠·작은 글 여러 줄·둥근 카드·도표 꾸밈은 "AI가 만든 디자인 티", 꽉 찬 사진+큰 주황 글자 기준 편은 좋다. 모방 금지: 경쟁과 비슷한 점(배치·색·글씨 꾸밈·말투)이 2개 넘으면 감점.\n'
         '질문: "경쟁 상위작 옆에 놓았을 때 같은 수준 이상으로 보이고, 먼저 누르고 싶은가. 경제 지식 없는 58세가 1초에 뜻을 바로 아는가."\n'
         '시안마다(now·r19a·r19b): 첫 줄 "r19a 점수: N"(1~10 정수, 6=경쟁 평균, 7=통과, 8=목표) · 1초에 주제를 알 수 있나(예/아니오) · AI 디자인 티(높음/중간/낮음) · 사실과 어긋나 보이거나 낚시로 보이는 말 · 경쟁과 비슷한 점 개수 · 8점이 되려면 고칠 것 2가지.\n'
         '마지막 줄: "1위: r19?" 또는 "1위: now"')
    out = ask(t, paths)
    open(os.path.join(J, f'{k}_score.md'), 'w', encoding='utf-8').write(out)
    sc = parse(out)
    sp = os.path.join(J, 'scores.json'); allsc = json.load(open(sp, encoding='utf-8')) if os.path.exists(sp) else {}
    allsc[k] = sc; json.dump(allsc, open(sp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(k, sc, '|', out.strip().splitlines()[-1])


if __name__ == '__main__':
    for k in (sys.argv[1:] or list(EP)): score(k)
