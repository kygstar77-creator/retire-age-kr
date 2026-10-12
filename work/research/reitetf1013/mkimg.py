# reitetf1013 본문 그림 — m1stot1013 mkimg 틀(blogimg) · 숫자는 calc_out.txt 그대로
import sys, json, os; sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import blogimg as B
r1=[['TIGER 리츠부동산인프라','-8.01%','396원 (+9.06%)','+1.05%','-0.34%'],['KODEX 한국부동산리츠인프라','-12.21%','387원 (+8.08%)','-4.13%','-5.38%']]
B.table('pkg/img/01.png','1억 넣고 1년 (2025년 10월 2일 → 2026년 10월 12일)',['상품','가격 변화','분배금 12번','세전 합','세후 합'],r1,hl_col=4,
        note='분배금 다시 사지 않음 · 세후는 분배금에서 15.4% 뗀 값 · 매매 수수료 뺌 · 지난 기록',src='야후 파이낸스 · 미래에셋자산운용 · 삼성자산운용')
json.dump({'01.png':{'rows':r1}},open('pkg/tables.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
B.bignum('pkg/img/02.png','KODEX 한국부동산리츠인프라 분배금 — 9월 지급분','60원',sub='평소 29~33원 → 2026년 9월 60원 · 지급기준일 9월 15일 · 실지급일 9월 17일',src='삼성자산운용 분배금 현황 2026년 10월 12일')
