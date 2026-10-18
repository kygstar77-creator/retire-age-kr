import sys, json, os; sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import blogimg as B
r1 = [['100엔 값', '943.59원', '853.02원'], ['100만원으로 받는 엔', '약 10만 6천 엔', '약 11만 7천 엔']]
B.table('pkg/img/01.png', '같은 100만원, 1년 사이 엔이 얼마나 늘었나', ['', '2025년 10월 16일', '2026년 10월 16일'], r1, hl_col=2,
        note='한국은행 원/엔 매매기준율(기준 환율) · 은행 창구 현찰 환율은 이보다 비쌈',
        src='한국은행 경제통계시스템(10월 18일 조회), 직접 계산', W=1640)
r2 = [['기준 환율', '846.63원', '약 11만 8천 엔'], ['현찰 살 때', '861.44원 (1.75% 비쌈)', '약 11만 6천 엔'],
      ['현찰 팔 때', '831.82원 (살 때보다 3.4% 낮음)', '10만 엔 되팔면 약 3만원 덜']]
B.table('pkg/img/02.png', '은행에서 엔을 살 때와 팔 때', ['100엔 기준', '하나은행 10월 16일', '100만원·10만 엔이면'], r2, hl_col=2,
        note='하나은행 10월 16일 마감 고시 회차 — 한국은행 기준 환율과 시각이 달라 값이 조금 다름 · 환율 우대를 받으면 달라짐',
        src='하나은행 고시(네이버 증권), 직접 계산', W=1640)
json.dump({'01.png': {'rows': r1}, '02.png': {'rows': r2}}, open('pkg/tables.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
