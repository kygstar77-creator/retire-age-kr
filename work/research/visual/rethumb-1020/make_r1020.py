# 10/20 공개 롱폼 11편 아래판(순돌이 10/19 15:10 지시 ③, textpos-1019 report: 잘되는 18채널 90장 중 82장 큰 글 아래).
#   10/19 고른 판(rethumb-1019/decisions.json pick)의 사진·낱말을 그대로 쓰고 자리만 바꾼다(새 사실 없음, 숫자 출처는 make_r1019.py NUM 주석).
#   꼴: 왼쪽 위 흰 작은 줄 + 주황 알약(100px @1920 — T-1 t1n_c에서 168px 기준 읽힘 확인), 큰 글 두 줄(흰/주황) 화면 아래 40~45% 고정, 아래 짙은 그라데이션.
#   py -3.12 make_r1020.py [편키 ...] → ep/<폴더>/thumb_r20.png
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'rethumb-1019'))
import make_r1019 as R
from PIL import Image, ImageDraw
W, HH, X0, INK = 1920, 1080, 80, (10, 11, 14)
EPS = {  # 편키: (폴더, 사진, 사진 옵션, 흰 작은 줄, 알약, [큰 흰, 큰 주황])
    'W-1':   ('W-1', 'w1a.jpg', dict(y_anchor=0.6), '10월 초 · 107조 실적 나온 그 주', '평가액 −140만원 = 분기 배당 44번 치', ['삼성전자 100주가', '사흘 새 얼마 빠졌을까?']),
    'W-1-2': (os.path.join('W-1', 'w1016'), 'w2b.jpg', dict(y_anchor=0.4), '10월 중순 · 회사가 15조원 들여 자기 주식 산 뒤', '평가액 −300만원, 회사가 산 값보다 12% 아래', ['삼성전자 100주가', '사흘 새 얼마 줄었을까?']),
    'G-1':   ('G-1', 'g1b.jpg', dict(), '올해 1월 꼭대기 · 10월 6일 기준', '1월 꼭대기 값까지 +50.7% 올라야', ['꼭대기에 산 금 1천만원', '본전까지 얼마?']),
    'P-1':   ('P-1', 'p1a.jpg', dict(y_anchor=0.6), '65세 대신 60세부터 · 1969년생 · 월 100만원 가정', '76.7세부터 제때 받은 쪽이 더 많아진다', ['국민연금 5년 일찍 받으면', '몇 살부터 손해?']),
    'M-1':   ('M-1', 'm1b.jpg', dict(), '세금·건보료 떼고 필요한 원금', 'JEPQ 1억 3,800만원 · SCHD 4억 8,500만원', ['매달 배당 100만원', 'JEPQ? SCHD?']),
    'D-1':   ('D-1', 'd1b.jpg', dict(), '퇴직 후 1년 1,000만원과 1,001만원', '1만원 넘었을 뿐인데 1년 54만원 더', ['배당·이자 1만원 차이에', '건보료 차이는?']),
    'E-1':   ('E-1', 'e1a.jpg', dict(), '9월 말까지 1년', '2분기 영업이익은 1년 전의 6.6배', ['SK하이닉스 주가 5배', '이익도 5배?']),
    'E-2':   ('E-2', 'e2b.jpg', dict(), '2분기 장부를 열어 보니', '매출 100달러에 영업이익 1.4달러', ['테슬라 매출 10분기 최대', '남은 이익은?']),
    'J-gSK': ('june-gSKsQWjTabo', 'fb.jpg', dict(), '14억 모은 파이어족 이야기', '돈 때문이 아니었다', ['14억 모아 조기 은퇴', '왜 1년 만에 회사로?']),
    'J-cxl': ('june-cxls2Ve18-k', 'da.jpg', dict(), '작은 돈을 오래 지킨 사람의 이야기', "많은 사람이 놓치는 '6억의 함정'", ['출근 없이 배당금만으로', '살 수 있을까?']),
    'J-JVT': ('june-JVTYZ208hgw', 'qb.jpg', dict(), '투자 재능 없는 사람의 선택', '종목 고르기를 그만둔 이유', ['4년 투자로 거의 다 잃고', 'QQQM 하나로?']),
}

def shade(im, y0, y1, alpha, top=False):
    m = Image.new('L', im.size, 0); d = ImageDraw.Draw(m)
    for y in range(y0, y1):
        t = (y - y0) / max(1, (y1 - y0) * 0.45) if not top else (y1 - y) / max(1, (y1 - y0) * 0.45)
        d.line([(0, y), (W, y)], fill=int(alpha * min(1, t)))
    return Image.composite(Image.new('RGB', im.size, INK), im, m)

def make(out, ph, opt, small, pill, big, bigsize=210, ls=1.14):
    im = R.photo(ph, **opt); d0 = ImageDraw.Draw(im)
    bs = min(R.fit(d0, t, bigsize, 'black') for t in big)
    ss = R.fit(d0, small, 64, '700'); ps = R.fit(d0, pill, 100, '700', 1760 - 64)
    hb = len(big) * int(bs * ls); y = HH - 40 - hb
    im = shade(im, max(0, y - 160), HH, 175); im = shade(im, 0, 380, 210, top=True)
    d = ImageDraw.Draw(im)
    d.text((X0, 36), small, font=R.f(ss, '700'), fill=R.WHITE, stroke_width=3, stroke_fill=INK)
    yy = 36 + ss + 22; ft = R.f(ps, '700'); tw = d.textlength(pill, font=ft); phh = int(ps * 1.36)
    d.rounded_rectangle((X0, yy, X0 + tw + 64, yy + phh), 24, fill=R.ORANGE); d.text((X0 + 32, yy + phh // 2), pill, font=ft, fill=R.WHITE, anchor='lm')
    for k, t in enumerate(big):
        d.text((X0, y - int(bs * 0.12)), t, font=R.f(bs, 'black'), fill=R.WHITE if k == 0 else R.ORANGE, stroke_width=6, stroke_fill=INK); y += int(bs * ls)
    im.resize((1280, 720), Image.LANCZOS).save(out)
    n = [len(t.replace(' ', '')) for t in big]
    print(os.path.relpath(out, R.EPD), f'큰 글 {hb / HH:.0%} 글자 {n} 합 {sum(n)} 알약 {ps}px 큰 {bs}px')

if __name__ == '__main__':
    for k in sys.argv[1:] or list(EPS):
        fo, ph, opt, small, pill, big = EPS[k]
        make(os.path.join(R.EPD, fo, 'thumb_r20.png'), ph, opt, small, pill, big)
