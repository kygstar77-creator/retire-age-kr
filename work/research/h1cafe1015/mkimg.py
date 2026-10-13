# h1cafe1015 본문 표 그림 — 숫자는 longform/ep/H-1/cafe_table.md(cafetable.py 출력)만
import sys, json, os, re; sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import blogimg as B
src = open('../longform/ep/H-1/cafe_table.md', encoding='utf-8').read()
secs = re.split(r'\n### ', src)[1:]
def sch(s): return re.sub(r'^서울', '', s).replace('초등학교', '초')
out = {}
for i, sec in enumerate(secs, 1):
    head = sec.split('\n')[0]
    rows = []
    for l in sec.split('\n'):
        if not l.startswith('| ') or l.startswith('| 단지') : continue
        c = [x.strip() for x in l.strip('|').split('|')]
        name, ip, se, p84, top, rec, hi, vs, jr, st, el, mt = c
        rec = re.sub(r' 20(\d\d)\.(\d\d)', r' \1.\2', rec)
        rows.append([name, ip[2:4] + '.' + ip[5:] + ' · ' + se, p84, top, rec, vs, jr, st, (sch(el) + ' · ' + mt) if el != '-' else '-'])
    dong = head.split(' — ')[0]; info = head.split(' — ')[1]
    p = f'pkg/img/0{i}.png'
    B.table(p, f'{dong} 단지 {len(rows)}곳 1년 실거래 (84㎡대 평당 높은 순)',
            ['단지', '입주 · 세대', '84㎡대 평당', '많은 면적대', '최근', '최고 대비', '전세가율', '역', '초교 · 마트'],
            rows, hl_col=2, W=1640,
            note=info + ' · 괄호는 거래 건수 · 최근은 거래 많은 면적대 거래(계약 연.월·층) · 역·초교·마트는 걸어서 잰 거리 · 평당 = 거래금액 ÷ (전용면적 ÷ 3.3058) · 최근·최고 대비는 층이 다른 거래끼리 비교 · 건수 3건 이하는 참고만 · 초교는 가장 가까운 학교(배정 학교 아님) · 입주 = 사용승인 연.월',
            src='국토교통부 아파트 매매·전월세 실거래(해제·공공기관 매수 제외) · 국토교통부 공동주택 단지 정보 · © OpenStreetMap contributors 보행로 거리')
    out[f'0{i}.png'] = {'rows': rows}
json.dump(out, open('pkg/tables.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('ok', {k: len(v['rows']) for k, v in out.items()})
