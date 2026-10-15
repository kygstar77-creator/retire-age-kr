# h1cafe1015 v2(10/15 사장님 "칸으로 비교한 거 너무 이해가 안 되는데") — 동네마다 세 칸 표(단지·입주·84㎡ 한 채 값)
# 숫자는 longform/ep/H-1/raw/tour_*.json(cafe_table.md와 같은 원자료)의 ppyTop(84㎡대 평당 가운데 값)·nTop(건수)만 쓴다.
# 한 채 값 = ppyTop × 25.41평(84 ÷ 3.3058), 억 단위 반올림. 84㎡대 거래 2건 미만(ppyTop 없음)은 빼고 건수만 note에 적는다.
import sys, json, os
sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
sys.stdout.reconfigure(encoding='utf-8')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import blogimg as B
PY = 84 / 3.3058
out = {}
for i, (k, dong) in enumerate((('garak', '송파구 가락동'), ('dunchon', '강동구 둔촌동'), ('godeok', '강동구 고덕동')), 11):
    d = json.load(open(f'../longform/ep/H-1/raw/tour_{k}.json', encoding='utf-8'))
    cs = sorted(d['complexes'], key=lambda c: -(c['ppyTop'] or 0))
    has = [c for c in cs if c['ppyTop']]
    rows, chk = [], []
    for c in has:
        v = c['ppyTop'] * PY / 10000
        flag = ' *' if c['nTop'] <= 3 else ''
        rows.append([c['name'], (c['kapt']['use'] or c['built'])[:4] + '년', f'약 {round(v)}억{flag}'])
        chk.append({'name': c['name'], 'use': c['kapt']['use'], 'ppyTop': c['ppyTop'], 'nTop': c['nTop'], 'won_eok': round(v, 2), 'shown': round(v)})
    left = len(cs) - len(has)
    note = '1년 동안 팔린 84㎡ 집 값을 줄 세운 한가운데 값'
    if any(r[2].endswith('*') for r in rows): note += ' · * 84㎡ 거래 3건 이하라 참고만'
    if left: note += f' · 84㎡ 거래가 1건 이하인 {left}곳은 글 끝 자세한 표에'
    p = f'pkg_v2/img/{i}.png'
    B.table(p, f'{dong} 84㎡ 한 채 값 (비싼 순)', ['단지', '입주', '84㎡ 한 채'], rows,
            hl_col=2, W=720, widths=[0.5, 0.2, 0.3], note=note, src='국토교통부 아파트 매매 실거래 ' + d['period'] + ' (계약 취소·공공기관이 산 거래 제외)')
    out[f'{i}.png'] = {'dong': dong, 'rows': chk, 'left': left}
json.dump(out, open('pkg_v2/tables_v2.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for f, v in out.items():
    print(f, v['dong'], [(r['name'], r['won_eok'], r['shown'], r['nTop']) for r in v['rows']], '빠짐', v['left'])
