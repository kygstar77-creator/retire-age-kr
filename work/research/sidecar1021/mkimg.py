# sidecar1021 본문 그림 2장 — 숫자는 업무규정·시행세칙 원문(raw/krx_rule_*.txt)과 KIND 공시 셈(calc3_out.txt)에서만
import sys, json, os, collections
sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import blogimg as B
r1 = [['무엇을 보나', '코스피200 선물 가격 ±5%', '코스피 지수 −8%·−15%·−20%'],
      ['무엇이 멈추나', '프로그램매매 주문만 5분', '모든 종목 거래 20분'],
      
      ['하루 몇 번', '한 번 · 오후 2시 50분 뒤 없음', '1·2단계 한 번씩 · 2시 50분 뒤 없음'], ['멈춘 동안 할 수 있는 것', '보통 주문 모두', '내 주문 취소만']]
B.table('pkg/img/01.png', '사이드카와 서킷브레이커, 내 주문은?', ['', '사이드카', '서킷브레이커'], r1,
        note='서킷브레이커는 떨어질 때만 · 8%가 1단계, 15%가 2단계, 20%(3단계)는 그날 장 종료', src='한국거래소 유가증권시장 업무규정 제16조·제25조, 시행세칙 제13조·제39조')
rows = [l.split() for l in open('raw/kind_sidecar_2026.txt', encoding='utf-8') if l[:1].isdigit()]
c = collections.Counter((r[1][:7], r[3]) for r in rows)
months = ['2026-02', '2026-03', '2026-04', '2026-05', '2026-06', '2026-07', '2026-08', '2026-09', '2026-10']
r2 = [[f'{int(m[5:])}월', f'{c[(m, "매수")]}번', f'{c[(m, "매도")]}번'] for m in months]
assert sum(c.values()) == 52
B.table('pkg/img/02.png', '올해 코스피 사이드카 52번, 달마다', ['달', '매수', '매도'], r2,
        note='1월·9월은 0번 · 10월은 21일 오전까지 · 작년(2025년)은 한 해 3번', src='한국거래소 KIND 공시 52건을 파이어맵이 직접 셈')
json.dump({'01.png': {'rows': r1}, '02.png': {'rows': r2}}, open('pkg/tables.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(r2)
