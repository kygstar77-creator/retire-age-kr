# 생애최초 취득세 감면 — 집값별 취득세(본세)와 감면 뒤 낼 돈. 지방세법 11조①8호 · 지특법 36조의3 · 행안부 2026 개편안(8/26)
import sys; sys.stdout.reconfigure(encoding='utf-8')
def rate(p):  # p 원
    if p <= 6e8: return 0.01
    if p <= 9e8: return round((p/1e8*2/3 - 3)/100, 6)  # 소수 다섯째 반올림 → 넷째까지(% 기준)
    return 0.03
def after(tax, cap): return max(0, tax - cap)
print('집값 | 세율 | 취득세(본세) | 지금 감면 뒤(200) | 개편안 40세 미만(300)')
for p in [2e8, 3e8, 4e8, 6e8, 7.5e8, 9e8, 12e8]:
    r = rate(p); t = round(p*r)
    print(f'{p/1e8:g}억 | {r*100:.4f}% | {t:,} | {after(t,2e6):,} | {after(t,3e6):,} | 감면몫 {min(t,2e6)/t*100:.1f}%')
p=12.01e8; print(f'12.01억 | 3% | {round(p*0.03):,} | 감면 없음(12억 넘음)')
