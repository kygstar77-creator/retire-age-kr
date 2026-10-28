# 10/28 G-1·P-1·E-1 공개 썸네일 알약 문구만 고침(벤치마크 1027 ④-2) — A31 소수점·A52 날짜 꼬리. 사진·흰 줄·주황은 지금판(r19) 그대로.
#   py -3.12 make_r1028.py → ep/<편>/thumb_r28.png
# NUM: G-1 +50.7%(screen_text 495행) → '50% 넘게' · P-1 76.7세(meta thumb_text) → '77세쯤' · E-1 6.57배(facts 17·21행) → '6배 넘게'
import os, sys
H = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(H, '..', 'rethumb-1019')); import make_r1019 as M
EPS = {
    'G-1': ('g1b.jpg', '올해 1월 꼭대기에 산 금 1천만원', ['본전까지 얼마?'], '1월 꼭대기 값까지 50% 넘게 올라야', dict()),
    'P-1': ('p1a.jpg', '국민연금, 65세 대신 5년 일찍 받으면', ['몇 살부터 손해?'], '77세쯤부터 65세에 받은 쪽이 더 많아진다', dict(y_anchor=0.6)),
    'E-1': ('e1a.jpg', '9월 말까지 1년, SK하이닉스 주가 5배', ['이익도 5배?'], '2분기 영업이익은 1년 전의 6배 넘게', dict()),
}
if __name__ == '__main__':
    for k in (sys.argv[1:] or list(EPS)):
        ph, wt, org, pill, opt = EPS[k]
        M.thumb(os.path.join(M.EPD, k, 'thumb_r28.png'), ph, wt, org, pill, **opt)
