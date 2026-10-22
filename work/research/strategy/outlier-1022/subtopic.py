# 돈 옆 생활 주제(하위 주제)별 숫자 — 10/21 전체 2,186편 + 10/22 넓은 표본 1,726편(겹침 제거) → subtopic_stats.json
import json, csv, sys, os, re, statistics as st, collections
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__)); O = os.path.join(H, '..', 'outlier-1021')
NEW = '2025-10-22'
S = {
 '요양·간병·부모 돌봄': r'요양원|요양병원|간병|돌봄|장기요양|요양보호|치매 (부모|엄마|아버지|어머니)|부모님 모시|모시고 사',
 '혼자 사는 노후·실버타운·노후 주거': r'혼자 사는|독거|실버타운|노인.{0,6}(원룸|주거|집)|노후.{0,4}(주거|집)|원룸을 택',
 '전원주택·귀농·시골집': r'전원주택|귀농|귀촌|시골집|시골 ?땅|체류형|농막|타운하우스|시골에서',
 '자동차 유지비·차 값': r'유지비|자동차세|기름값|연비|중고차|전기차.{0,12}(비용|수리비|충전|값)|(차|SUV|자동차).{0,10}(가격|비싼|저렴|싼|값)|휘발유차|하이브리드',
 '상속·이혼·가족 돈 법': r'상속|유산|유언|유류분|이혼|재산분할|위자료|양육비|공동 소유|명의',
 '직장·퇴직·공무원 현실': r'공무원|대기업|희망퇴직|명퇴|권고사직|정년|퇴직|재취업|사표|직장인|월급쟁이|부장|중년.{0,6}(직장|일자리)|일자리',
 '병원비·건강보험·실손': r'병원비|의료비|건강보험|건보|실손|본인부담|수술비|입원비|간병비|검진',
 '경제사·몰락 사건': r'IMF|외환위기|카드대란|버블|몰락|파산|부도|대공황|폭락.{0,4}(역사|사건)|그때 그',
 '식당·자영업 폐업': r'폐업|자영업|문 닫|텅 비|사장님들|가게.{0,6}(망|접)',
 '장례·사망 뒤 절차': r'장례|임종|사망신고|사망 후|부고|조의금|유품',
 '육아·교육비': r'학원비|사교육|교육비|육아휴직|양육비|아이 키우|육아 현실',
 '돈과 인간관계·심리': r'손절|인간관계|돈 (빌려|꿔)|(친구|형제|자식).{0,8}돈|돈.{0,6}(관계|사람|심리)',
}
S = {k: re.compile(v) for k, v in S.items()}
rows = {}
for p, tag in [(os.path.join(O, 'outliers.csv'), '1021'), (os.path.join(H, 'outliers_1022.csv'), '1022')]:
    for r in csv.DictReader(open(p, encoding='utf-8-sig')):
        if r['id'] not in rows: r['tag'] = tag; rows[r['id']] = r
rows = list(rows.values()); print('합친 아웃라이어', len(rows))
out = {}
for k, rg in S.items():
    m = [r for r in rows if rg.search(r['title'])]
    if not m: continue
    chs = {r['cid']: r['opened'] for r in m}; lg = [r for r in m if int(r['sec']) > 180]
    topc = collections.Counter(r['channel'] for r in m).most_common(3)
    out[k] = dict(n=len(m), n1022=sum(r['tag'] == '1022' for r in m), channels=len(chs), new_ch_share=round(sum(o >= NEW for o in chs.values()) / len(chs), 2),
        med_x=round(st.median(float(r['x_subs']) for r in m), 1), med_views=round(st.median(int(r['views']) for r in m)),
        long_n=len(lg), long_med_views=round(st.median(int(r['views']) for r in lg)) if lg else None, long_med_x=round(st.median(float(r['x_subs']) for r in lg), 1) if lg else None,
        top_channels=topc, top=[(int(r['views']), int(r['subs']), int(r['sec']), r['opened'], r['channel'], r['id'], r['title']) for r in sorted(m, key=lambda r: -int(r['views']))[:12]])
json.dump(out, open(os.path.join(H, 'subtopic_stats.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for k, s in out.items():
    print(f"\n## {k} | {s['n']}편(10/22 {s['n1022']}) {s['channels']}채널 새{s['new_ch_share']} 배수{s['med_x']} 조회{s['med_views']:,} | 롱 {s['long_n']}편 조회{s['long_med_views']} 배수{s['long_med_x']} | {s['top_channels']}")
    for t in s['top'][:9]: print(f"   {t[0]:>9,} 구독{t[1]:>5,} {t[2]:>5}s 개설{t[3][:7]} {t[4][:10]} {t[5]} {t[6][:62]}")
