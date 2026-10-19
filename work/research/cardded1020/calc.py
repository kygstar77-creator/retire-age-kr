# 신용카드등 소득공제 계산 — 조세특례제한법 제126조의2 (2026-06-02 시행판), 2026년 사용분. 단위 만원
def ded(G, credit=0, debit=0, market=0, transit=0, culture=0, kids=0):
    low = G <= 7000
    m = G * 0.25
    cul = culture if low else 0
    cred = credit + (0 if low else culture)
    use = cred + debit + market + transit + cul
    if use <= m: return 0.0, 0.0, (350 if low else 275) if kids==1 else ((400 if low else 300) if kids>=2 else (300 if low else 250))
    s = cred*.15 + debit*.30 + market*.40 + transit*.40 + cul*.30
    if m <= cred: sub = m*.15
    elif m <= cred + debit + (cul if low else 0):
        sub = cred*.15 + (m-cred)*.30
    else:
        sub = cred*.15 + (debit+cul)*.30 + (m-cred-debit-cul)*.40
    d = s - sub
    base = 300 if low else 250
    if kids == 1: cap = 350 if low else 275
    elif kids >= 2: cap = 400 if low else 300
    else: cap = base
    sp = (market+transit+cul*0)*.40 + (cul*.30 if low else 0)
    sp = min(sp, 300 if low else 200)
    out = min(d, cap)
    if d > cap: out = cap + min(d-cap, sp)
    return d, out, cap

def reach(G, mix, kids):
    """mix=신용만/체크만: 공제가 한도에 처음 닿는 사용액"""
    lo, hi = 0, 20000
    for _ in range(60):
        mid = (lo+hi)/2
        kw = {'credit': mid} if mix == 'c' else {'debit': mid}
        d, o, cap = ded(G, kids=kids, **kw)
        if d >= cap: hi = mid
        else: lo = mid
    return hi

if __name__ == '__main__':
    print('== 한도에 닿는 사용액(만원)')
    for G in (3000, 5000, 7000, 9000):
        for mix in 'cd':
            print(G, '신용만' if mix=='c' else '체크만', [round(reach(G, mix, k)) for k in (0,1,2)],
                  '한도', [ded(G, credit=99999, kids=k)[2] for k in (0,1,2)])
    print('== 사례 총급여5000 자녀0/1/2')
    for k in (0,1,2):
        print(k, ded(5000, credit=2400, debit=800, market=100, transit=150, kids=k))
    print('== 사례 총급여5000 신용3600')
    for k in (0,1,2):
        d,o,c = ded(5000, credit=3600, kids=k); print(k, round(d,1), round(o,1), c)
    print('== 사례 총급여5000 신용3000 체크1500 시장200 대중200')
    for k in (0,1,2):
        d,o,c = ded(5000, credit=3000, debit=1500, market=200, transit=200, kids=k); print(k, round(d,1), round(o,1), c)
    print('== 총급여9000 신용6000 대중200')
    for k in (0,1,2):
        d,o,c = ded(9000, credit=6000, transit=200, kids=k); print(k, round(d,1), round(o,1), c)
