# hfguar1006 이미지 01·02 — 숫자는 calc.py run() 그대로. firemap-write 2026-10-06
import sys, os
sys.stdout.reconfigure(encoding='utf-8')
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(D, '..', '..')); sys.path.insert(0, D)
import blogimg as B
src = open(os.path.join(D, 'calc.py'), encoding='utf-8').read().split('for y in')[0]
exec(src)
IMG = os.path.join(D, 'pkg', 'img')
man = lambda v: f"{round(v/1e4):,}만원"
rows = []; rows2 = []
for y in (5, 10, 11, 12, 15, 20):
    n = run(y, 0.01, 0.0095); o = run(y, 0.015, 0.0075)
    d = round((n['fee']-o['fee'])/1e4)
    sgn = f"{abs(d):,}만원 " + ('덜 냄' if d < 0 else '더 냄')
    rows.append([f"{y}년", man(o['fee']), man(n['fee']), sgn])
    rows2.append([f"{y}년", man(o['balance']), man(n['balance']), f"{round(n['balance']/1e4)-round(o['balance']/1e4):+,}만원"])
B.table(os.path.join(IMG, '01.png'), '65세·4억 집, 보증료가 쌓인 누계', ['받은 햇수', '개편 전', '개편 후', '차이'], rows,
        hl_col=3, note='월지급금 101만 1천원 고정, 이자는 CD 3.21%+1.1%p 가정. 11년까지 개편 후가 적고 12년째부터 많아짐.',
        src='한국주택금융공사 월지급금 예시·금융위원회 보도자료, 파이어맵 계산')
B.table(os.path.join(IMG, '02.png'), '개편 전후 주택연금 보증료율', ['', '개편 전', '개편 후'],
        [['초기보증료(집값 기준)', '1.5%', '1.0%'], ['4억 집이면', '600만원', '400만원'], ['연 보증료(대출잔액 기준)', '0.75%', '0.95%']],
        hl_col=2, note='2026년 3월 1일 이후 신규 신청분부터 적용. 보증료는 현금으로 내지 않고 대출잔액에 얹힘.',
        src='금융위원회 보도자료 「2026년 주택연금 개선방안」, 한국주택금융공사')
print(rows)
