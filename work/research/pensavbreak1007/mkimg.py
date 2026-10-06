# pensavbreak1007 본문 표 2장 — wagepeak1007 mkimg 틀. firemap-write 2026-10-06
import sys, json, os; sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import blogimg as B
rows=[['총급여 5,500만원 이하','495만원','561만원','66만원'],['총급여 5,500만원 초과','396만원','561만원','165만원']]
B.table('pkg/img/01.png','연금저축 해지, 받은 공제보다 더 내는 돈',['총급여','5년간 돌려받은 세액','해지 때 세금','더 내는 돈'],rows,hl_col=3,
        note='5년간 해마다 600만원 납입·수익 400만원 가정, 평가액 3,400만원',src='소득세법 제59조의3·제129조, 지방세법 제103조의13')
rows2=[['1순위','올해 넣은 돈·한도 넘긴 돈','세금 없음'],['2순위','퇴직금을 옮겨 온 돈(IRP에서 옮긴 경우)','퇴직소득세'],['3순위','공제받은 납입금·수익','16.5%(연금수령 아닌 인출)']]
B.table('pkg/img/02.png','연금저축에서 돈이 빠지는 순서',['순서','어떤 돈','세금'],rows2,hl_col=2,
        note='공제만 안 받은 돈은 확인을 받아야 1순위',src='소득세법 시행령 제40조의3')
json.dump({'01.png':{'rows':rows},'02.png':{'rows':rows2}},open('pkg/tables.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
print('ok')
