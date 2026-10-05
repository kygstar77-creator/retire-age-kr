# depprot1006 이미지 01·02 — 숫자는 calc.py 그대로. firemap-write 2026-10-06 (00은 표지, 09:00 뒤 따로)
import sys, os
sys.stdout.reconfigure(encoding='utf-8')
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(D, '..', '..')); sys.path.insert(0, D)
import blogimg as B
from calc import protect
IMG = os.path.join(D, 'pkg', 'img')
def man(v):
    m = round(v/1e4); e, r = divmod(m, 10000)
    return (f"{e}억 {r:,}만원" if r else f"{e}억원") if e else f"{r:,}만원"
def row(name, ps):
    r = protect(ps); ok = sum(x[2] for x in r); ng = sum(x[3] for x in r)
    return [name, man(ok), ('0원' if ng < 1 else man(ng))]
rows = [row('한 곳에 3억', [3e8]), row('같은 은행 두 지점에 1억 5천씩', [3e8]),
        row('다른 세 곳에 1억씩', [1e8]*3), row('다른 네 곳에 7,500만원씩', [7.5e7]*4)]
B.table(os.path.join(IMG, '01.png'), '노후자금 3억, 나눠 맡기면 어디까지 보호될까', ['맡기는 방법', '보호', '한도 밖'], rows,
        hl_col=2, note='1년 정기예금 연 3.9%(세전) 만기 원리금 3억 1,170만원 기준. 같은 은행 지점끼리는 합산.',
        src='예금자보호법 시행령 제18조, 금융위원회 Q&A, 금감원 비교공시 2026년 9월, 파이어맵 계산')
B.table(os.path.join(IMG, '02.png'), '한 은행 안에서도 따로 1억씩 보호되는 돈', ['구분', '한도'],
        [['일반 예금·적금(계좌 모두 합산)', '1억원'], ['DC형·IRP 중 예금으로 굴리는 돈', '따로 1억원'],
         ['연금저축신탁·연금저축보험', '따로 1억원'], ['펀드·CMA·후순위채·출자금', '보호 안 됨']],
        hl_col=1, note='각 1억원은 원금과 이자를 합친 금액. IRP라도 펀드로 굴리는 부분은 빠짐.',
        src='금융위원회 「예금보호한도 상향 관련 주요 Q&A」(2025.7.22), 새마을금고중앙회 안내')
print(rows)
