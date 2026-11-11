# 갱신요구권 '사용' 계약: 종전 전세 → (보증금 + 월세)로 갱신. 법 한도 = 보증금 5% 증액(제7조②·시행령 제8조) + 줄인 보증금 × 상한(제7조의2·시행령 제9조)
import json, glob, os, statistics as st, sys
sys.stdout.reconfigure(encoding='utf-8')
D = os.path.dirname(os.path.abspath(__file__))
def n(s):
    s = (s or '').replace(',', '').strip(); return int(s) if s else 0
def cap(y, m, d):
    dt = (y, m, d); base = 3.00 if dt >= (2026, 8, 27) else (2.75 if dt >= (2026, 7, 16) else 2.50); return base + 2
res = []
for f in glob.glob(os.path.join(D, 'raw', '*.json')):
    for r in json.load(open(f, encoding='utf-8')):
        if r.get('contractType') != '갱신' or r.get('useRRRight') != '사용': continue
        pd, pm, dp, mr = n(r['preDeposit']), n(r['preMonthlyRent']), n(r['deposit']), n(r['monthlyRent'])
        if pm != 0 or pd == 0 or mr == 0: continue
        c = cap(int(r['dealYear']), int(r['dealMonth']), int(r['dealDay']))
        room = pd * 1.05 - dp                       # 5% 올린 전세 기준으로 남는 보증금(만원)
        mx = max(0.0, room) * c / 100 / 12          # 월세 한도(만원)
        res.append(dict(pd=pd, dp=dp, mr=mr, mx=mx, over=mr - mx, kind='줄임' if dp < pd else '그대로·올림'))
print('갱신요구권 사용 + 종전 전세 → 월세 붙음:', len(res))
for k in ('줄임', '그대로·올림'):
    sub = [x for x in res if x['kind'] == k]
    if not sub: continue
    ov = [x for x in sub if x['over'] > 0.5]       # 반올림 여유 5천원
    print(f" 보증금 {k}: {len(sub)}건 · 한도 넘음 {len(ov)} ({len(ov)/len(sub)*100:.0f}%) · 넘은 금액 중앙 {st.median([x['over'] for x in ov]) if ov else 0:.1f}만원/월 · 월세 중앙 {st.median([x['mr'] for x in sub])}")
ov = [x for x in res if x['over'] > 0.5]
print(f"합계 한도 넘음 {len(ov)}/{len(res)} ({len(ov)/len(res)*100:.0f}%) · 넘은 금액 중앙 {st.median([x['over'] for x in ov]):.1f}만원")
# 예: 전세 4억 4천 → 보증금 3억 4천 + 월세 ? (중앙값 근처 사례 수치)
pd, dp = 44000, 34000
for c in (5.0,):
    print('예시 종전 4.4억→보증금 3.4억, 상한', c, '% → 월세 한도', round((pd*1.05-dp)*c/100/12, 1), '만원 · 증액 없이 전환만', round((pd-dp)*c/100/12, 1))
