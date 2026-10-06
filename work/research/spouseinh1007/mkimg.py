# spouseinh1007 본문 표 2장 — bigwa1006 mkimg 틀. firemap-write 2026-10-06
import sys, json, os; sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import blogimg as B
rows=[['15억원','8,730만원','5,959만원','약 2,771만원'],['20억원','2억3,280만원','1억2,887만원','약 1억393만원'],['30억원','6억2,080만원','3억1,594만원','약 3억486만원']]
B.table('pkg/img/01.png','집값별 상속세, 배우자 몫에 따라',['집값','배우자 0원','배우자 법정상속분','차이'],rows,hl_col=3,
        note='배우자+자녀 2명 · 집만 상속 · 빚·생전 증여 없음 · 일괄공제 5억 · 기한 안 신고(3% 공제) 가정',src='상속세 및 증여세법 제19·21·26·69조, 민법 제1009조')
rows2=[['상속세 신고기한','돌아가신 달 말일부터 6개월'],['배우자 몫 분할기한','신고기한 다음 날부터 9개월'],['집·땅처럼 등기 필요','등기까지 끝나야 인정'],['기한을 넘기면','배우자공제 5억원만'],['소송 등 부득이한 사유','기한 안 신고 시 6개월 더']]
B.table('pkg/img/02.png','배우자공제 5억 넘게 받으려면 지킬 날짜',['단계','기준'],rows2,hl_col=1,
        note='분할 사실도 분할기한까지 세무서에 신고',src='상속세 및 증여세법 제19조②③, 제67조①')
json.dump({'01.png':{'rows':rows},'02.png':{'rows':rows2}},open('pkg/tables.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
print('ok')
