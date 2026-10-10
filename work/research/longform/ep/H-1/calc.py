# H-1 계산 재현 — 숫자는 전부 여기서 나온다(대본·카페·쇼츠 공통). 실행: py -3.12 work/research/longform/ep/H-1/calc.py > calc_out.txt
# 재료: raw/tour_{garak,dunchon,godeok}.json = work/research/sonpum2/tour.py 출력(2026-10-11 02시대 실행, 각 동네 실행 직후 video/tour.json을 복사)
#       work/research/rt/<구코드>_<월>_{trade,rent}.json = 국토교통부 아파트 매매·전월세 실거래(공공데이터포털 1613000, rtmolit.py, 2026-10-11 02:1x 받음)
# 원자료 단지명: 고덕아남 = '아남1', 가락쌍용1차 = '가락(1차)쌍용아파트'(국토부 실거래 aptNm 그대로)
# 네이버 부동산 등 민간 화면·매물 자료는 쓰지 않는다.
import json, os, sys, statistics as st, collections
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); RT = os.path.join(HERE, '..', '..', '..', 'rt')
PY = 3.305785
MS = ['202511', '202512', '202601', '202602', '202603', '202604', '202605', '202606', '202607', '202608', '202609', '202610']
def num(s): return float(str(s or '0').replace(',', '') or 0)
def eok(m): return f'{m/10000:.2f}억'
def load_rt(lawd, kind):
    out = []
    for m in MS:
        p = os.path.join(RT, f'{lawd}_{m}_{kind}.json')
        if os.path.exists(p): out += json.load(open(p, encoding='utf-8'))
    return out
TOUR = {k: json.load(open(os.path.join(HERE, 'raw', f'tour_{k}.json'), encoding='utf-8')) for k in ('garak', 'dunchon', 'godeok')}
def cx(k, name): return next(c for c in TOUR[k]['complexes'] if c['name'] == name)

print('# H-1 calc_out — 2026-10-11 실행. 단위 만원(금액), 평당 = 전용면적 기준 3.305785㎡\n')
print('## 1. 동네 개요(tour.py 출력 그대로)')
for k, d in TOUR.items():
    print(f"- {d['gu']} {d['umd']}: 기간 {d['period']} · 매매 {d['nTrade']}건(해제·공공기관 매수 제외) · 신규 전월세 {d['nNew']}건 · 비교 면적대 {d['topLabel']} · 공동주택 {d['nKapt']}곳 중 지도 단지 {len(d['complexes'])}곳 · 전월세 전환율 {d['conv']}%")

print('\n## 2. 대표 단지(각 단지에서 거래가 가장 많은 면적대 기준, 동떨어진 거래 = 그 면적대 중앙값 ±20% 밖)')
KEY = [('garak', '헬리오시티'), ('garak', '가락쌍용1차'), ('garak', '가락래미안파크팰리스'), ('dunchon', '올림픽파크포레온'), ('dunchon', '둔촌신동아'),
       ('godeok', '고덕 그라시움'), ('godeok', '래미안힐스테이트 고덕'), ('godeok', '고덕아남'), ('godeok', '고덕센트럴푸르지오')]
for k, n in KEY:
    c = cx(k, n); w = c['walk']; kp = c['kapt']
    def wm(x): return f"{x['name']} {x['m']}m" if x else '-'
    print(f"- {n}({TOUR[k]['umd']}) 입주 {kp['use'] or c['built']} · {kp['hh']:,}세대 · 세대당 주차 {kp['parkPer']} · {c['bandLabel']}(전용 중앙 {c['area']}㎡) 매매 {c['nb']}건(동떨어진 {c['nOdd']}) 중앙 {eok(c['saleMed'])}")
    print(f"    최근 {c['last']['ym']} {eok(c['last']['amt'])}({c['last']['floor']}층) · 최고 {c['max']['ym']} {eok(c['max']['amt'])}({c['max']['floor']}층) · 최고 대비 {c['fromMax']:+}%")
    print(f"    84㎡대 평당 중앙 {c['ppyTop']}만원({c['nTop']}건) · 같은 면적대 신규 순수전세 중앙 {eok(c['jeonse']) if c['jeonse'] else '-'}({c['nj']}건) · 전세가율 {c['jratio']}%")
    print(f"    걸어서(OSM 보행로) 역 {wm(w['station'])} · 초등학교 {wm(w['school'])} · 마트 {wm(w['mart'])} · 공원 {wm(w['park'])} · 관리사무소 등록 역 도보 {kp['subwayWalk']}")
    bym = collections.defaultdict(list)
    for x in c['deals']:
        if not x['odd']: bym[x['ym']].append(x['amt'])
    print('    달별 중앙(동떨어진 거래 뺌): ' + ' · '.join(f"{ym} {eok(st.median(v))}({len(v)}건)" for ym, v in sorted(bym.items())))

print('\n## 3. 84㎡대를 같은 잣대로 — 국토부 원자료에서 직접(단지명·동 일치, 전용 80~85㎡, 해제·공공기관 매수 제외)')
S_T, G_T = load_rt('11710', 'trade'), load_rt('11740', 'trade')
S_R, G_R = load_rt('11710', 'rent'), load_rt('11740', 'rent')
def t84(R, apt, umd):
    return [r for r in R if r['aptNm'].replace(' ', '') == apt and r['umdNm'] == umd and 80 <= num(r['excluUseAr']) < 85 and not r.get('cdealType') and r.get('buyerGbn') != '공공기관']
def j84(R, apt, umd):
    return [num(r['deposit']) for r in R if r['aptNm'].replace(' ', '') == apt and r['umdNm'] == umd and 80 <= num(r['excluUseAr']) < 85 and r.get('contractType') == '신규' and num(r['monthlyRent']) == 0]
B84 = {}
for apt, umd, T, R in [('헬리오시티', '가락동', S_T, S_R), ('올림픽파크포레온', '둔촌동', G_T, G_R), ('고덕그라시움', '고덕동', G_T, G_R), ('래미안힐스테이트고덕', '고덕동', G_T, G_R), ('아남1', '고덕동', G_T, G_R), ('가락(1차)쌍용아파트', '가락동', S_T, S_R)]:
    rows = t84(T, apt, umd); js = j84(R, apt, umd)
    if not rows: print(f'- {apt}: 84㎡대 매매 0건'); continue
    amts = [num(r['dealAmount']) for r in rows]; med = st.median(amts)
    ppy = st.median(num(r['dealAmount']) / (num(r['excluUseAr']) / PY) for r in rows)
    jm = st.median(js) if len(js) >= 3 else None
    B84[apt] = dict(n=len(rows), med=med, ppy=ppy, jn=len(js), jm=jm)
    print(f"- {apt}: 84㎡대 매매 {len(rows)}건 중앙 {eok(med)} · 평당 중앙 {ppy:,.0f}만원 · 최저 {eok(min(amts))} 최고 {eok(max(amts))} · 신규 순수전세 {len(js)}건 중앙 {eok(jm) if jm else '-'}" + (f" · 전세가율 {jm/med*100:.1f}%" if jm else ''))

print('\n## 4. 같은 평당가 두 단지')
h, o = B84['헬리오시티'], B84['올림픽파크포레온']
H, O = cx('garak','헬리오시티')['ppyTop'], cx('dunchon','올림픽파크포레온')['ppyTop']
print(f"- tour.py 84㎡대 평당(동떨어진 거래 뺌) 헬리오시티 {H:,} vs 올림픽파크포레온 {O:,} → 차이 {(O/H-1)*100:+.1f}% / 원자료 전부(직거래 포함) {h['ppy']:,.0f} vs {o['ppy']:,.0f} → {(o['ppy']/h['ppy']-1)*100:+.1f}% · 84㎡ 매매 중앙 {eok(h['med'])} vs {eok(o['med'])} → 차이 {eok(o['med']-h['med'])}")
print(f"- 입주: 헬리오시티 {cx('garak','헬리오시티')['kapt']['use']} · 올림픽파크포레온 {cx('dunchon','올림픽파크포레온')['kapt']['use']}")

print('\n## 5. 같은 동네 새 단지 vs 오래된 단지(84㎡대 평당 중앙, tour.py ppyTop)')
for k, a, b in [('garak', '헬리오시티', '가락쌍용1차'), ('dunchon', '올림픽파크포레온', '둔촌신동아'), ('godeok', '고덕 그라시움', '고덕아남'), ('godeok', '고덕 그라시움', '래미안힐스테이트 고덕')]:
    A, Bc = cx(k, a), cx(k, b)
    print(f"- {TOUR[k]['umd']}: {a}({A['kapt']['use']}) {A['ppyTop']:,}({A['nTop']}건) vs {b}({Bc['kapt']['use']}) {Bc['ppyTop']:,}({Bc['nTop']}건) → {(Bc['ppyTop']/A['ppyTop']-1)*100:+.1f}% · 역까지 걸어서 {A['walk']['station']['m']}m vs {Bc['walk']['station']['m']}m")

print('\n## 6. 한 건과 그 달 전체 — 낮은 거래 4건(84㎡대, 원자료 dealingGbn·rgstDate 그대로)')
for apt, umd, T, ym in [('헬리오시티', '가락동', S_T, ('2026', '2')), ('헬리오시티', '가락동', S_T, ('2026', '5')), ('올림픽파크포레온', '둔촌동', G_T, ('2026', '9'))]:
    rows = [r for r in t84(T, apt, umd) if (r['dealYear'], r['dealMonth']) == ym]
    rows.sort(key=lambda r: num(r['dealAmount']))
    print(f"- {apt} {ym[0]}.{ym[1].zfill(2)} 84㎡대 {len(rows)}건: " + ' / '.join(f"{r['dealDay']}일 {eok(num(r['dealAmount']))} {r['floor']}층 {r['dealingGbn']}" + (f" 등기 {r['rgstDate']}" if r.get('rgstDate') else ' 등기 칸 비어 있음') for r in rows))
    if len(rows) >= 2: print(f"    같은 달 최고-최저 {eok(num(rows[-1]['dealAmount']) - num(rows[0]['dealAmount']))}")
hel = t84(S_T, '헬리오시티', '가락동')
print(f"- 헬리오시티 84㎡대 1년 {len(hel)}건 중 23억대 이하 {sum(num(r['dealAmount']) < 240000 for r in hel)}건 · 27억 이상 {sum(num(r['dealAmount']) >= 270000 for r in hel)}건")
print(f"- 직거래 건수(84㎡대): 헬리오시티 {sum(r['dealingGbn']=='직거래' for r in hel)} / {len(hel)} · 올림픽파크포레온 {sum(r['dealingGbn']=='직거래' for r in t84(G_T,'올림픽파크포레온','둔촌동'))} / {len(t84(G_T,'올림픽파크포레온','둔촌동'))}")

print('\n## 7. 거래가 몰린 달 — 단지 전체 면적(해제·공공 제외)')
for apt, umd, T in [('헬리오시티', '가락동', S_T), ('올림픽파크포레온', '둔촌동', G_T), ('고덕그라시움', '고덕동', G_T), ('래미안힐스테이트고덕', '고덕동', G_T)]:
    rows = [r for r in T if r['aptNm'].replace(' ', '') == apt and r['umdNm'] == umd and not r.get('cdealType') and r.get('buyerGbn') != '공공기관']
    cm = collections.Counter(r['dealYear'] + r['dealMonth'].zfill(2) for r in rows)
    am = cm['202604'] + cm['202605']
    print(f"- {apt}: 1년 {len(rows)}건 · 4~5월 {am}건({am/len(rows)*100:.0f}%) · 2025.11~2026.03 {sum(cm[m] for m in MS[:5])}건 · 6~10월 {sum(cm[m] for m in MS[7:])}건")
    r84 = [r for r in rows if 80 <= num(r['excluUseAr']) < 85]; c84 = collections.Counter(r['dealYear'] + r['dealMonth'].zfill(2) for r in r84)
    print(f"    84㎡대만: 1년 {len(r84)}건 · 4~5월 {c84['202604']+c84['202605']}건({(c84['202604']+c84['202605'])/max(1,len(r84))*100:.0f}%)")
for lawd, umd, T in [('11710', '가락동', S_T), ('11740', '둔촌동', G_T), ('11740', '고덕동', G_T)]:
    rows = [r for r in T if r['umdNm'] == umd and not r.get('cdealType') and r.get('buyerGbn') != '공공기관']
    cm = collections.Counter(r['dealYear'] + r['dealMonth'].zfill(2) for r in rows)
    print(f"- {umd} 동 전체: 1년 {len(rows)}건 · 4~5월 {cm['202604']+cm['202605']}건({(cm['202604']+cm['202605'])/len(rows)*100:.0f}%) · 달별 " + ' '.join(f"{m[2:4]}.{m[4:]} {cm[m]}" for m in MS))

print('\n## 8. 가상 인물 손품 씨(계산용) — 래미안힐스테이트고덕 84㎡ 전세, 보증금 = 그 단지 84㎡ 신규 순수전세 1년 중앙값')
dep = B84['래미안힐스테이트고덕']['jm']
print(f"- 보증금 {eok(dep)}")
for apt in ('래미안힐스테이트고덕', '아남1', '고덕그라시움', '올림픽파크포레온', '헬리오시티'):
    b = B84[apt]
    print(f"- {apt} 84㎡ 매매 중앙 {eok(b['med'])} − 보증금 = 더 필요한 돈 {eok(b['med']-dep)}" + (f" · 그 단지 84㎡ 전세 중앙 {eok(b['jm'])}(전세로 옮기면 보증금 {eok(b['jm']-dep)} 더)" if b['jm'] else ''))
print('  (세금·중개보수·대출 조건은 넣지 않은 단순 차액. 취득세·대출 한도는 사람마다 달라 이 편에서 계산하지 않는다)')
