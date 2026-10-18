# 10/18 visual — C-2·H-4 썸네일을 고정 틀(strategy/brand-1017/make_frame.py)로 그린다. 문구는 각 편 copy/titles.md·meta.json 그대로.
#   py -3.12 work/research/visual/frame1018.py <사진 폴더(Pexels 사진 jpg)>
import os, sys, importlib.util
sys.stdout.reconfigure(encoding='utf-8')
import cv2
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.abspath(os.path.join(HERE, '..', '..'))
spec = importlib.util.spec_from_file_location('mf', os.path.join(WORK, 'research', 'strategy', 'brand-1017', 'make_frame.py'))
mf = importlib.util.module_from_spec(spec); spec.loader.exec_module(mf)
EP = os.path.join(WORK, 'research', 'longform', 'ep')
PXDIR = sys.argv[1]


def mp4(name, pos):
    cap = cv2.VideoCapture(os.path.join(WORK, 'research', name) if '/' in name else os.path.join(WORK, 'video', 'public', 'bg', 'c2', name))
    cap.set(cv2.CAP_PROP_POS_FRAMES, int(cap.get(cv2.CAP_PROP_FRAME_COUNT) * pos))
    ok, f = cap.read()
    if not ok:
        raise SystemExit('사진 못 읽음 ' + name)
    return Image.fromarray(cv2.cvtColor(f, cv2.COLOR_BGR2RGB))


def jpg(pid):
    p = [f for f in os.listdir(PXDIR) if f.endswith(f'_{pid}.jpg')][0]
    return Image.open(os.path.join(PXDIR, p)).convert('RGB')


C2 = dict(tag='내 돈 계산', date='10월 19일 월요일', what='S&P500 · 퇴직금 3억 · 매달 200만원 꺼내 쓰기',
          q='같은 3억,<br>시작만 5년 차이')
H4 = dict(tag='손품', date='10월 27일 화요일', what='84㎡ 매매 실거래 · 2026년 7~9월', q='광명, 정말<br>서울보다 비쌀까?')

JOBS = [
    # C-2: 큰 숫자 = 왼쪽(1998) 결과. 사진 = 빈 지갑(12412380) / 노부부 손(6785719)
    ('C-2', 'thumb_f1a', dict(C2, label='1998년에 시작한 사람', big='2011년 바닥', sub='2003년 시작 → 2025년 말 2억 7천 남음'), ('mp4', '12412380.mp4', 0.4)),
    ('C-2', 'thumb_f1b', dict(C2, label='1998년에 시작한 사람', big='2011년 바닥', sub='2003년 시작 → 2025년 말 2억 7천 남음'), ('mp4', '6785719.mp4', 0.4)),
    ('C-2', 'thumb_f1c', dict(C2, label='2003년에 시작한 사람, 2025년 말', big='2억 7천 남음', sub='1998년 시작 → 2011년에 돈 바닥'), ('mp4', '12412380.mp4', 0.4)),
    # H-4: copy/titles.md 1위 짝 그대로. 사진 = 서울 빽빽한 주거(36178449) / 호수 야경 아파트(18705526, 민규 장) / 복도식 외벽(3736898, 형길 장) — 15928940은 단지 이름 글자 보여 탈락
    ('H-4', 'thumb_h4a', dict(H4, label='광명보다 싼 서울 구', big='8곳', sub='나머지 17곳은 광명보다 비쌈'), ('jpg', '36178449')),
    ('H-4', 'thumb_h4b', dict(H4, label='광명보다 싼 서울 구', big='8곳', sub='나머지 17곳은 광명보다 비쌈'), ('jpg', '18705526')),
    ('H-4', 'thumb_h4c', dict(H4, label='광명보다 싼 서울 구', big='8곳', sub='나머지 17곳은 광명보다 비쌈'), ('jpg', '3736898')),
    # 2차(Claude 독자 09시): '2011년 바닥'이 주가 저점으로도 읽힘 → copy 원문 '2011년에 돈 바닥'의 '돈'을 큰 글에 / H-4 '8곳'이 무엇인지 안 읽힘 → '서울 8곳'
    ('C-2', 'thumb_f1d', dict(C2, label='1998년에 시작한 사람', big='2011년 돈 바닥', sub='2003년 시작 → 2025년 말 2억 7천 남음'), ('mp4', '12412380.mp4', 0.4)),
    ('H-4', 'thumb_h4d', dict(H4, label='광명보다 싼 서울 구', big='서울 8곳', sub='나머지 17곳은 광명보다 비쌈'), ('jpg', '18705526')),
    # 2차 레드팀: '광명보다 싼 서울 구'가 168px에서 '비싼'으로 뒤집혀 읽힘 → 큰 글에 '쌈'까지 · 사진은 지역 없는 복도식(h4c)
    ('H-4', 'thumb_h4e', dict(H4, label='서울 25개 구 중 광명보다 싼 곳', big='8곳만 더 쌈', sub='나머지 17곳은 광명보다 비쌈'), ('jpg', '3736898')),
    # 10/17 고정 틀 전환 — 다시 녹음 6편 중 이미 문구가 있는 H-2·T-1·X-1 (옛 h2y·t1j·x1f와 같은 문구, copy/titles.md·meta.json)
    ('H-2', 'thumb_h2f1', dict(tag='손품', date='10월 20일 화요일', what='잠실주공5단지 · 국민평형 84㎡대 · 최근 1년 거래', q='살 땐 가장 비싸고<br>전세는 가장 쌌다',
                               label='잠실동 안에서 잠실주공5단지', big='매매 43억', sub='전세는 5억 남짓 · 잠실동에서 가장 쌈'), ('jpg', '11932032')),
    ('T-1', 'thumb_t1f1', dict(tag='내 돈 계산', date='10월 21일 수요일', what='같은 20억 집 · 정부안 2029년', q='거주 10년 vs 2년,<br>양도세는?',
                               label='2년만 산 사람 양도세', big='약 12배', sub='10년 산 사람과 견주면 · 국회 통과 전 정부안'), ('jpg', '20472686')),
    ('X-1', 'thumb_x1f1', dict(tag='내 돈 계산', date='10월 22일 목요일', what='같은 S&P500 · 원화 기준', q='주가는 올랐는데<br>내 1억은?',
                               label='7월 초에 산 1억', big='−11%', sub='작년 이맘때 산 1억은 +10%'), ('mp4', '16846101.mp4', 0.5)),
    # 3차(Claude 2차: 라벨 36px는 168px에서 안 읽힘 → 큰 글 하나가 주어까지 품게)
    ('H-4', 'thumb_h4f', dict(H4, label='서울 25개 구와 비싼 순으로 세우면', big='광명 18번째', sub='성북구 다음, 관악구 앞'), ('jpg', '3736898')),  # copy 2위 짝
    ('T-1', 'thumb_t1f2', dict(tag='내 돈 계산', date='10월 21일 수요일', what='같은 20억 집 · 정부안 2029년', q='거주 10년 vs 2년,<br>양도세는?',
                               label='10년 산 사람보다', big='2년 살면 약 12배', sub='국회 통과 전 정부안 · 2029년에 팔 때'), ('jpg', '20472686')),
    ('H-2', 'thumb_h2f2', dict(tag='손품', date='10월 20일 화요일', what='잠실주공5단지 · 국민평형 84㎡대 · 최근 1년 거래', q='살 땐 가장 비싸고<br>전세는 가장 쌌다',
                               label='매매는 43억, 잠실동에서 가장 비싼데', big='전세 5억 남짓', sub='잠실동 84㎡대 단지 중 전세는 가장 쌈'), ('jpg', '11932032')),
    # 4차(레드팀 2차: '2년만 산 사람'의 '산'이 '샀다'로 읽혀 보유 2년 오해 → '거주')
    ('T-1', 'thumb_t1f3', dict(tag='내 돈 계산', date='10월 21일 수요일', what='같은 20억 집 · 정부안 2029년', q='거주 10년 vs 2년,<br>양도세는?',
                               label='2년만 거주한 사람 양도세', big='약 12배', sub='10년 거주한 사람과 견주면 · 국회 통과 전 정부안'), ('jpg', '20472686')),
    # 5차(레드팀 3차): H-2 사진이 다른 단지인데 윗줄 '잠실주공5단지'로 오인 → 단지 모양 안 보이는 노을 실루엣(5336495, 尾 賀) / T-1 '2년 살면'이 보유 2년으로 → 윗줄에 '10년 보유'
    ('H-2', 'thumb_h2f3', dict(tag='손품', date='10월 20일 화요일', what='잠실주공5단지 · 국민평형 84㎡대 · 최근 1년 거래', q='살 땐 가장 비싸고<br>전세는 가장 쌌다',
                               label='매매는 43억, 잠실동에서 가장 비싼데', big='전세 5억 남짓', sub='잠실동 84㎡대 단지 중 전세는 가장 쌈'), ('jpg', '5336495')),
    ('T-1', 'thumb_t1f4', dict(tag='내 돈 계산', date='10월 21일 수요일', what='같은 20억 집 · 10년 보유 · 정부안 2029년', q='거주 10년 vs 2년,<br>양도세는?',
                               label='2년만 거주한 사람 양도세', big='약 12배', sub='10년 거주한 사람과 견주면 · 국회 통과 전 정부안'), ('jpg', '20472686')),
]
ONLY = sys.argv[2].split(',') if len(sys.argv) > 2 else None
JOBS = [j for j in JOBS if not ONLY or j[1] in ONLY]

for ep, name, d, src in JOBS:
    ph = mp4(src[1], src[2]) if src[0] == 'mp4' else jpg(src[1])
    im = mf.long_img(d, ph)
    out = os.path.join(EP, ep, name + '.png')
    im.save(out)
    for w in (320, 168):
        im.resize((w, round(w * 720 / 1280)), Image.LANCZOS).save(os.path.join(HERE, f'{ep}-thumb', f'{name}_{w}.png'))
    print(out)
