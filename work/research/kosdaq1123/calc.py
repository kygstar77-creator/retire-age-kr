# 첫 계산(씨앗) — ECOS 일별 종가(2003~) + 야후 ^KQ11(2000-10~2004, ECOS와 2003 겹침 대조용). 세전·지수 값만, 예측 없음.
import json, sys
sys.stdout.reconfigure(encoding='utf-8')
d = json.load(open('raw_ecos.json', encoding='utf-8'))
kq, kp = d['kosdaq'], d['kospi']
def at(rows, day):
    for t, v in rows:
        if t >= day: return t, v
last_q, last_p = kq[-1], kp[-1]
print('기준일', last_q, last_p)
mq = max(kq, key=lambda x: x[1]); print('코스닥 2003~ 최고 종가', mq, '지금/최고', round(last_q[1]/mq[1]*100,1), '%')
mp = max(kp, key=lambda x: x[1]); print('코스피 1995~ 최고 종가', mp, '지금/최고', round(last_p[1]/mp[1]*100,1), '%')
# 2000-03-10 코스닥 최고 2,834.40(1000 기준 환산 값, KRX — 원문 확인 필요)
PEAK2000 = 2834.40
print('코스닥 지금 ÷ 2000-03 최고(2,834.40, 원문 확인 전)', round(last_q[1]/PEAK2000*100,1), '%')
# 같은 날 시작 비교: 2003-01-02, 2006-01-02, 2016-01-04, 2021-01-04, 최근 1년
for day in ['20030102','20060102','20110103','20160104','20210104','20251120']:
    a, b = at(kq, day), at(kp, day)
    print(day, '코스닥', a, '→', round(last_q[1]/a[1]*100-100,1), '% | 코스피', b, '→', round(last_p[1]/b[1]*100-100,1), '%')
# 2003~ 연말 종가
ye = {}
for t, v in kq: ye[t[:4]] = (t, v)
print('코스닥 연말', [(k, round(v[1])) for k, v in ye.items()])
yp = {}
for t, v in kp: yp[t[:4]] = (t, v)
print('코스피 연말', [(k, round(v[1])) for k, v in yp.items()])
# 2026 고점 이후
y26 = [r for r in kq if r[0] >= '20260101']; m26 = max(y26, key=lambda x: x[1]); print('코스닥 2026 최고', m26, '지금/그때', round(last_q[1]/m26[1]*100-100,1))
