# ISA 중도해지 계산 — 조특법 제91조의18 ①②⑦, 소득세법 이자·배당 원천징수 14% + 지방소득세(소득세의 10%)
def won(x): return f"{round(x):,}원"
for profit in (3_000_000, 5_000_000, 10_000_000):
    for kind, cap in (("일반형", 2_000_000), ("서민형", 4_000_000)):
        isa = max(0, profit-cap)*0.09*1.1          # 3년 채움(또는 특별해지): 한도 넘는 몫만 9%+지방세
        normal = profit*0.14*1.1                    # 중도해지: 특례분 추징 → 일반 과세와 같아짐
        print(f"이익 {profit//10000}만원 {kind}: 3년 채움 {won(isa)} · 중도해지 {won(normal)} · 차이 {won(normal-isa)}")
