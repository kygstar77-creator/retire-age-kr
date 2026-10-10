# 카페 글 재료: 세 동네 지도 단지 전체 표(raw/tour_*.json → cafe_table.md). 실행: py -3.12 cafetable.py
import json, os, sys
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__))
def eok(m): return f'{m/10000:.2f}억' if m else '-'
out = []
for k, title in (('garak', '송파구 가락동'), ('dunchon', '강동구 둔촌동'), ('godeok', '강동구 고덕동')):
    d = json.load(open(os.path.join(H, 'raw', f'tour_{k}.json'), encoding='utf-8'))
    out.append(f"\n### {title} — {d['period']} 매매 {d['nTrade']}건 · 지도 단지 {len(d['complexes'])}곳\n")
    out.append('| 단지 | 입주 | 세대 | 84㎡대 평당(건) | 거래 많은 면적대(건) | 최근 | 최고 | 최고 대비 | 전세가율 | 역(걸어서) | 초등학교 | 마트 |')
    out.append('|---|---|---|---|---|---|---|---|---|---|---|---|')
    for c in sorted(d['complexes'], key=lambda c: -(c['ppyTop'] or 0)):
        w = c['walk']
        def wm(x): return f"{x['name'].replace(' 출입구','')} {x['m']:,}m" if x else '-'
        out.append(f"| {c['name']} | {c['kapt']['use'] or c['built']} | {c['kapt']['hh']:,} | {(f'{c[chr(112)+chr(112)+chr(121)+chr(84)+chr(111)+chr(112)]:,}만원({c[chr(110)+chr(84)+chr(111)+chr(112)]})') if c['ppyTop'] else '-'} | {c['bandLabel']}({c['nb']}) | {eok(c['last']['amt'])} {c['last']['ym']} {c['last']['floor']}층 | {eok(c['max']['amt'])} {c['max']['ym']} {c['max']['floor']}층 | {c['fromMax']:+.1f}% | {str(c['jratio'])+'%' if c['jratio'] else '-'} | {wm(w['station'])} | {wm(w['school'])} | {wm(w['mart'])} |")
    if d['skipped']: out.append(f"\n빠진 곳: " + ', '.join(f'{a}({b})' for a, b in d['skipped']))
open(os.path.join(H, 'cafe_table.md'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
print('\n'.join(out))
