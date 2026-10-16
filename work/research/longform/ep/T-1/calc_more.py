# T-1 '우리만' 숫자 — 2026-10-17 T-1 자료조사 담당. calc.py(정부 사례 6칸 일치)를 그대로 불러 조건만 바꾼다.
# 원문: 공동명의 기본공제 각각 2,500만원(문답 p.49 ➋ · 상세본 p.68) · 공제 한도 공동소유 지분 안분(상세본 p.60)
#       12억 판정은 집 전체 값(시행령 §156①) · 부득이한 사유 비거주 최장 3년 거주 인정('28~, 상세본 p.84~85·문답 p.60)
#       조정대상지역 일시적 2주택 기한 2년(시행령 §155①1, 2026.9.30 개정·'26.10.1 양도분~, 문답 p.55~56)
#       기한 넘기면 2주택 중과: §104⑦1 기본세율+20%p, 중과 주택은 장특 제외(§95② 괄호), 중과 한시 배제는 2026.5.9 양도분까지(시행령 §167의10)
# 가정: calc.py와 같음(필요경비 0, 2년 이상 보유, 지방소득세 10% 따로 표시).
import sys
sys.stdout.reconfigure(encoding='utf-8')
from calc import calc, tax55, EOK

def man(x): return f'{x/1e4:,.0f}만원'

def joint(sell, buy, hold, live, rg, share=0.5):
    """부부 공동명의: 사람마다 지분만큼 양도·취득, 12억 비율은 집 전체로(§156①). 기본공제는 사람마다."""
    tot = 0
    for _ in range(2):
        gain = (sell - buy) * share
        part = (sell - 12*EOK) / sell
        tg = gain * part
        r = calc(sell, buy, hold, live, rg)          # 공제율·한도·기본공제 조건은 집 기준
        ded = gain * r['rate'] / 100 * part
        cap = {'2028': 20*EOK, '2029': 10*EOK}.get(rg)
        if cap: ded = min(ded, cap * share)          # 한도 지분 안분(상세본 p.60)
        basic = r['basic']                           # 각각 250만 또는 2,500만(문답 p.49 ➋)
        base = max(0, tg - ded - basic)
        tot += tax55(base)
    return tot

def heavy2(sell, buy):
    """조정대상지역 2주택 중과: 12억 비과세 없음·장특 없음·기본세율+20%p(§104⑦1·§95②)."""
    base = max(0, (sell - buy) - 250e4)
    return tax55(base) + base * 0.20

if __name__ == '__main__':
    S, B = 20*EOK, 8*EOK
    print('== ① 부부 공동명의(50:50) — 같은 20억 집, 지방세 포함')
    for nm, h, l in (('정민 씨형 10년 보유·10년 거주', 10, 10), ('수현 씨형 10년 보유·2년 거주', 10, 2)):
        for rg in ('2026', '2029'):
            one = calc(S, B, h, l, rg)['tax']; two = joint(S, B, h, l, rg)
            print(f'  {nm} {rg}: 한 사람 명의 {man(one*1.1)} → 공동명의 둘 합 {man(two*1.1)} (차 {man((one-two)*1.1)})')
    print('== ② 부득이한 사유(전근 등) 비거주 최장 3년을 거주로 인정 — 수현 씨형 거주 2년 → 5년(정부안, 2028~)')
    for rg in ('2028', '2029'):
        a = calc(S, B, 10, 2, rg); b = calc(S, B, 10, 5, rg)
        print(f'  {rg}: 공제율 {a["rate"]}% {man(a["total"])} → {b["rate"]}% {man(b["total"])} (차 {man(a["total"]-b["total"])})')
    print('== ③ 12억을 조금 넘는 13억 집(취득 8억), 지방세 포함')
    for nm, h, l in (('10년 보유·10년 거주', 10, 10), ('10년 보유·2년 거주', 10, 2)):
        print('  ' + nm + ': ' + ' · '.join(f'{rg} {man(calc(13*EOK, B, h, l, rg)["total"])}' for rg in ('2026', '2027', '2028', '2029')))
    print('== ④ 살았던 해 1년의 값 — 수현 씨형(10년 보유) 2029년, 거주 2→3→4년')
    prev = None
    for l in (2, 3, 4, 5):
        t = calc(S, B, 10, l, '2029')['total']
        print(f'  거주 {l}년: 공제율 {8*l}% {man(t)}' + (f' (한 해 더 살면 {man(prev-t)} 줄어)' if prev else '')); prev = t
    print('== ⑤ 조정대상지역 일시적 2주택 — 2년 기한 넘겨 2주택 중과로 팔면(수현 씨형 20억 집, 2029년, 정부 문답 p.56 사례 구조)')
    h = heavy2(S, B)
    print(f'  기한 안(2028년, 1주택으로 계산) {man(calc(S, B, 10, 2, "2028")["total"])} · 기한 넘김(2029년 중과) {man(h*1.1)} · 같은 해 1주택이었다면 {man(calc(S, B, 10, 2, "2029")["total"])}')
    print(f'  배수: 2029년 중과 ÷ 2029년 1주택 = {h*1.1/calc(S, B, 10, 2, "2029")["total"]:.1f}배')
