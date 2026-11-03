# 신생아 특례 디딤돌 3억·30년·원리금균등·수도권·우대 없음 — 6년째(61회차)부터 남은 원금을 남은 25년에 새 금리로
# 원문: raw/rate.json(특례 금리표), raw/newlywed_rate.json(신혼 최저 2.55), raw/after_rate.json(8.5천 초과 종료 후 금리, 접수 달별)
import json, re, sys
sys.stdout.reconfigure(encoding='utf-8')
def pmt(P, r, n):
    i = r / 100 / 12
    return P * i / (1 - (1 + i) ** -n)
def bal(P, r, n, k):
    i = r / 100 / 12; m = pmt(P, r, n)
    return P * (1 + i) ** k - m * ((1 + i) ** k - 1) / i
P, N = 300_000_000, 360
spread = 2.55 - 1.80
cases = [("연소득 7천만원(6천~8.5천)", 2.90, round(2.90 + spread, 2)),
         ("연소득 1억(8.5천~1억) 11월 접수", 3.20, 4.77),
         ("연소득 1억(8.5천~1억) 9월 접수", 3.20, 4.40),
         ("맞벌이 1.6억(1.5~1.7억) 11월 접수", 4.15, 4.77)]
for name, r1, r2 in cases:
    m1 = pmt(P, r1, N); b = bal(P, r1, N, 60); m2 = pmt(b, r2, N - 60)
    print(f"{name}: 특례 {r1}% 월 {m1:,.0f}원 · 5년 뒤 남은 원금 {b:,.0f}원 · 종료 후 {r2}% 월 {m2:,.0f}원 · 차이 {m2-m1:,.0f}원")
s = open('raw/after_rate.json', encoding='utf-8').read().strip()
d = json.loads(re.sub(r'^\{arrJson\s*:', '{"arrJson":', s))['arrJson']
ser = [(j['STD_YEAR_MONTH'], float(j['STDRATE'])) for j in d]
mx = max(ser, key=lambda x: x[1]); mn = min(ser, key=lambda x: x[1])
print(f"종료 후 기준 금리 {ser[-1][0]}~{ser[0][0]} {len(ser)}달 · 최고 {mx} · 최저 {mn} · 11월 바로 앞 높은 값 {max(x[1] for x in ser[1:])}")
print("8.5천 이하 종료 후 최고(30년 6천~8.5천) =", round(2.90 + spread, 2), "· 2억 구간 30년 하한 =", round(4.50 + 0.2, 2))
