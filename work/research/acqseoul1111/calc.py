# 서울 25개 구 아파트 매매 실거래(2026-08~10, 11/11 받음)로 1주택 취득세 계산
# 세율: 지방세법 제11조①8 (6억 이하 1%, 6~9억 (가액억×2/3−3)% 소수 넷째자리, 9억 초과 3%)
# 지방교육세: 제151조①1 다목 — 세율×50%로 산출한 금액의 20% = 취득세×10%
# 농특세: 전용 85㎡ 초과만 과세표준×0.2% (농특세법 제5조①6·제4조11, 송파구청 계산식)
import json, glob, os, re, statistics, sys, collections
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__))
SGG = json.load(open(os.path.join(H, '..', 'seoul_sgg.json'), encoding='utf-8'))
def num(s): return float(re.sub(r'[^\d.]', '', str(s) or '0') or 0)
def rate(p):  # p 원
    e = p / 1e8
    if e <= 6: return 0.01
    if e <= 9: return round((e * 2 / 3 - 3) / 100, 6)   # % → 소수, 원문은 소수점 넷째자리(%) 반올림
    return 0.03
def rate_pct(p):
    e = p / 1e8
    if e <= 6: return 1.0
    if e <= 9: return round(e * 2 / 3 - 3, 4)
    return 3.0
def tax(p, area):
    r = rate_pct(p) / 100
    acq = p * r; edu = acq * 0.1; nong = p * 0.002 if area > 85 else 0
    return acq, edu, nong, acq + edu + nong
rows = []
for f in glob.glob(os.path.join(H, 'raw', '*_2026*.json')):
    code = os.path.basename(f).split('_')[0]
    for r in json.load(open(f, encoding='utf-8')):
        if r.get('cdealType'): continue          # 해제
        if r.get('buyerGbn') == '공공기관': continue
        p = num(r.get('dealAmount')) * 1e4
        rows.append((code, SGG.get(code, code), p, num(r.get('excluUseAr')), r.get('dealYear'), r.get('dealMonth')))
print('전체 건수', len(rows))
b = collections.Counter('6억 이하' if p <= 6e8 else ('6~9억' if p <= 9e8 else '9억 초과') for _, _, p, _, _, _ in rows)
for k in ('6억 이하', '6~9억', '9억 초과'): print(k, b[k], f'{b[k]/len(rows)*100:.1f}%')
print('서울 전체 중간값', statistics.median(p for _, _, p, _, _, _ in rows))
print()
out = []
for code, name in SGG.items():
    ps = [p for c, _, p, _, _, _ in rows if c == code]
    a84 = [p for c, _, p, a, _, _ in rows if c == code and 80 <= a <= 85]
    if not ps: continue
    m = statistics.median(ps); m84 = statistics.median(a84) if a84 else None
    t = tax(m, 84)[3]
    out.append((name, len(ps), m, rate_pct(m), t, len(a84), m84, tax(m84, 84)[3] if m84 else None))
out.sort(key=lambda x: -x[2])
for o in out:
    print(f'{o[0]}\t{o[1]}건\t중간 {o[2]/1e8:.2f}억\t세율 {o[3]}%\t세금 {o[4]/1e4:,.0f}만\t84형 {o[5]}건\t{(o[6] or 0)/1e8:.2f}억\t{(o[7] or 0)/1e4:,.0f}만')
print('중간값 9억 초과 구', sum(1 for o in out if o[2] > 9e8), '/', len(out))
print('중간값 6억 이하 구', sum(1 for o in out if o[2] <= 6e8))
print('84형 중간 9억 초과 구', sum(1 for o in out if o[6] and o[6] > 9e8), '/ 84형 있는 구', sum(1 for o in out if o[6]))
# 경계 예시
for p in (6e8, 6.01e8, 7.5e8, 9e8, 9.01e8, 12e8):
    a, e, n, t = tax(p, 84); print(f'{p/1e8}억 84㎡: 세율 {rate_pct(p)}% 취득세 {a:,.0f} 교육 {e:,.0f} 합 {t:,.0f}')
for p in (9e8, 12e8):
    a, e, n, t = tax(p, 100); print(f'{p/1e8}억 100㎡: 농특 {n:,.0f} 합 {t:,.0f}')
# 지식iN 질문 6.8억 · 85㎡ 초과 12억 차이 · 9억 경계
a, e, n, t = tax(6.8e8, 84); print(f'6.8억 84㎡: 세율 {rate_pct(6.8e8)}% 취득세 {a:,.0f} 교육 {e:,.0f} 합 {t:,.0f}')
print('6억→9억 세금 배수', tax(9e8, 84)[3] / tax(6e8, 84)[3], '집값 배수', 9 / 6)
print('12억 85㎡ 초과 농특', tax(12e8, 100)[2])
