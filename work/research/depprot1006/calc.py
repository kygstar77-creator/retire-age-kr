# depprot1006 계산 — 노후자금 3억을 나눠 맡기면 어디까지 보호되나. firemap-write 2026-10-06
# 규칙: 금융회사(조합·금고)별 1인당 원금+소정의 이자 합쳐 1억(예금자보호법 32조②·시행령 18조⑦, 금융위 QA 8·9번)
# 같은 금융회사 여러 계좌·지점은 합산(QA 8번, 새마을금고 안내). 이자는 1년 정기예금 단리 세전, 만기 시점 기준.
import sys; sys.stdout.reconfigure(encoding='utf-8')
LIMIT = 100_000_000
R = 0.039   # 금감원 금융상품통합비교공시 2026-09 저축은행 12개월 정기예금 회사별 최고 기본금리 중앙값
def protect(principals, r=R):
    out = []
    for p in principals:
        due = p * (1 + r)
        out.append((p, due, min(due, LIMIT), max(0, due - LIMIT)))
    return out
def show(name, principals):
    rows = protect(principals)
    tot = sum(x[1] for x in rows); ok = sum(x[2] for x in rows); ng = sum(x[3] for x in rows)
    print(f"{name}: 원리금 {tot/1e4:,.0f}만 · 보호 {ok/1e4:,.0f}만 · 보호 밖 {ng/1e4:,.0f}만")
    return tot, ok, ng
if __name__ == '__main__':
    print('원금 상한(이자 포함 1억 안):', f"{LIMIT/(1+R)/1e4:,.1f}만원", '| 3.5%면', f"{LIMIT/1.035/1e4:,.1f}만원")
    show('A 한 곳에 3억', [300_000_000])
    show('B 같은 은행 두 지점 1.5억씩(합산)', [300_000_000])
    show('C 서로 다른 세 곳 1억씩', [100_000_000]*3)
    show('D 서로 다른 네 곳 7,500만씩', [75_000_000]*4)
    print('C 한 곳당 넘는 이자:', f"{100_000_000*R/1e4:,.0f}만")
