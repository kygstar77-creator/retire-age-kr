# -*- coding: utf-8 -*-
"""1세대 1주택 2026 종부세 직접 계산 (firemap-write 2026-10-26)
근거: 종부세법 8·9·10조, 시행령 2조의4(60%)·4조의3(공제 재산세 식), 시행규칙 별지 31호 부표 작성방법
(⑦ = (공시가-12억)×60%×재산세 공정비율×0.4%, ⑨ = ⑥부과 재산세 × ⑦/⑧),
지방세법 110조③·시행령 109조의2(과표상한 5%)·109조①2(1주택 2026 45%)·111조(세율표: 3억 초과 0.4% 누진공제 63만),
농어촌특별세법 5조(종부세의 20%).
가정: 작년 공시가 = 올해 / 1.1867 (서울 평균 상승률, 국토부 2026 공시), 재산세 감면·조례 가감 없음."""
import sys

E = 100_000_000


def prop_rate(tb):  # 지방세법 111 주택 표준세율(서식 세율표)
    if tb <= 60_000_000: return tb * 0.001
    if tb <= 150_000_000: return tb * 0.0015 - 30_000
    if tb <= 300_000_000: return tb * 0.0025 - 180_000
    return tb * 0.004 - 630_000


def jb_rate(tb):  # 종부세법 9조①1 (2주택 이하)
    for lim, r, d in [(3*E, .005, 0), (6*E, .007, 600_000), (12*E, .010, 2_400_000),
                      (25*E, .013, 6_000_000), (50*E, .015, 11_000_000), (94*E, .020, 36_000_000)]:
        if tb <= lim: return tb * r - d
    return tb * .027 - 99_800_000


def year(pub, prev_pub=None, credit=0.0):
    R = 0.45  # 1주택 6억 초과 재산세 공정시장가액비율(2026)
    std_tb = pub * R
    tb = std_tb
    if prev_pub is not None:  # 과표상한
        cap = prev_pub * R + std_tb * 0.05
        tb = min(std_tb, cap)
    prop = prop_rate(tb)          # ⑥ 부과 재산세(본세)
    prop_std = prop_rate(std_tb)  # ⑧ 총표준세율 재산세
    jtb = max(0, pub - 12*E) * 0.60
    jb = jb_rate(jtb)
    p7 = max(0, pub - 12*E) * 0.60 * R * 0.004
    ded = prop * p7 / prop_std if prop_std else 0
    after = max(0, jb - ded)
    fin = after * (1 - credit)
    return dict(pub=pub, tb=tb, prop=prop, jtb=jtb, jb=jb, ded=ded, after=after,
                jbfin=fin, nong=fin * 0.2, total=fin * 1.2)


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    G = 1.1867
    for p in [12.5, 13, 14, 15, 16, 18, 20, 25]:
        pub = p * E
        prev = round(pub / G, -6)
        a = year(pub, prev)
        b = year(pub, None)
        last = year(prev, None)  # 시행령 5조②: 직전 연도 법, 과표상한(110조③) 빼고 — 2025 1주택 비율도 45% 가정
        cap150 = (last['prop'] + last['after']) * 1.5
        now = a['prop'] + a['after']
        print(f"공시 {p}억(작년 {prev/E:.2f}억): 재산세본세 {a['prop']:,.0f}(상한없으면 {b['prop']:,.0f}) "
              f"종부과표 {a['jtb']:,.0f} 산출 {a['jb']:,.0f} 재산세공제 {a['ded']:,.0f}(상한없으면 {b['ded']:,.0f}) "
              f"공제후 {a['after']:,.0f} +농특 {a['total']:,.0f}")
        for c in [0.2, 0.4, 0.5, 0.8]:
            print(f"    세액공제 {int(c*100)}% → 종부+농특 {year(pub, prev, c)['total']:,.0f}")
        print(f"    세부담상한 확인: 올해 {now:,.0f} vs 작년×150% {cap150:,.0f} → {'걸림' if now > cap150 else '안 걸림'}"
              + (f" · 상한 적용 종부세 {max(0, cap150 - a['prop']):,.0f}" if now > cap150 else ''))
