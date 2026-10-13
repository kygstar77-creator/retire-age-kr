# qqqm1014 본문 그림 — reitetf1013 mkimg 틀(blogimg) · 숫자는 calc_out.txt·roll_out.txt 그대로
import sys, json, os; sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import blogimg as B
r1=[['QQQ','+23.93%','3.09달러 (0.51%)','+24.44%','1억 2,443만 8천원'],['QQQM','+23.95%','1.32달러 (0.53%)','+24.48%','1억 2,448만 3천원']]
B.table('pkg/img/01.png','1억 넣고 1년 (2025.10.13 → 2026.10.12 미국 종가)',['상품','가격 변화','분배금 4번','합계','1억원이'],r1,hl_col=4,
        note='분배금 다시 사지 않음 · 달러 수익률을 1억원에 그대로 곱함 · 환율·세금·수수료 뺌 · 지난 기록',src='네이버 증권 · 나스닥 분배 이력')
r3=[['2025년 4월 9일','+31.55%','+31.84%','QQQM +29만 4천원'],['2025년 6월 18일','+40.54%','+40.40%','QQQ +13만 9천원']]
B.table('pkg/img/03.png','산 날에 따라 가장 크게 갈린 두 날 (1년 보유, 1억 기준)',['산 날','QQQ','QQQM','더 남은 쪽'],r3,hl_col=3,
        note='분배금 다시 사지 않음 · 환율·세금·수수료 뺌 · 지난 기록',src='네이버 증권 · 나스닥 분배 이력')
json.dump({'01.png':{'rows':r1},'03.png':{'rows':r3}},open('pkg/tables.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
B.bignum('pkg/img/02.png','산 날을 바꿔 1년씩 계산했을 때 QQQM이 더 남은 금액(1억 기준)','-13만 9천 ~ +29만 4천원',sub='산 날 249개 중 238개에서 QQQM이 앞 · 가운데 값 5만 8천원 · 보수 차이는 연 3만원',src='야후 파이낸스 2024년 10월 14일~2025년 10월 10일 산 날 기준')
