# h2cafe1019 본문 그림 2장 — 숫자는 H-2 calc_out.txt.orig1012(10/12 받은 신고분, 영상과 같은 값)에서만
import sys, json, os, re
sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import blogimg as B
src = open('../longform/ep/H-2/calc_out.txt.orig1012', encoding='utf-8').read()
sec = src.split('## 1.')[1].split('## 2.')[0]
rows2, dong = [], ''
NAME = {'주공아파트5단지': '잠실주공5단지', '쌍용대치아파트1동,2동,3동,5동,6동': '쌍용대치', '대치우성아파트1동,2동,3동,5동,6동,7동': '대치우성', '우성아파트': '잠실우성', '현대': '잠실현대', '현대1': '대치현대1'}
for ln in sec.splitlines():
    m = re.match(r'### (\S+)', ln)
    if m: dong = m.group(1).replace('동', ''); continue
    m = re.match(r'- (.+?)\(건축 (\d+)\) (\d+)건 중앙 ([\d.]+)억 · 평당 [\d,]+만원 .*?순수전세 (\d+)건 (-|[\d.]+억)(?: · 전세가율 ([\d.]+)%)?', ln)
    if not m: continue
    a, y, n, med, jn, jm, jr = m.groups()
    rows2.append([f'{dong} {NAME.get(a, a)}', y, n + '건', f'{float(med):.2f}억', jm if jm != '-' else '-', (jr + '%') if jr else '-'])
assert len(rows2) == 28, len(rows2)
B.table('pkg/img/02.png', '세 동네 84㎡대 1년 실거래 28개 단지', ['단지', '지은 해', '매매 건수', '매매 중간 가격', '새 전세 중간 가격', '전세가율'], rows2, W=1400,
        note='전용 80~85㎡ · 2025년 11월~2026년 10월 계약 · 매매 3건 이상 · 새 전세 3건 미만은 -', src='국토교통부 아파트 매매·전월세 실거래(10월 12일 받음)')
r1 = [['잠실주공5단지 (1978년)', '약 43억', '약 5억 2천'], ['리센츠 (2008년)', '약 34억', '약 13억 5천'], ['은마 (1979년)', '약 39억', '약 8억 3천'],
      ['래미안대치팰리스 (2015년)', '약 43억', '약 18억'], ['반포미도 (1987년)', '약 41억', '약 8억'], ['래미안원베일리 (2023년)', '약 59억', '약 21억']]
B.table('pkg/img/01.png', '84㎡ 한 채 값과 새 전세, 오래된 단지 vs 새 단지', ['단지 (지은 해)', '매매', '새 전세'], r1, hl_col=None,
        note='1년 동안 계약된 값의 한가운데 값 · 새 전세 = 월세 없는 신규 계약', src='국토교통부 아파트 매매·전월세 실거래(10월 12일 받음)')
json.dump({'01.png': {'rows': r1}, '02.png': {'rows': rows2}}, open('pkg/tables.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
