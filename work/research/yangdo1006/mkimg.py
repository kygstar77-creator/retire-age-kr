# yangdo1006 본문 표 2장 — irpwd1006 mkimg 틀. firemap-write 2026-10-06
import sys, json, os; sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import blogimg as B
rows=[['3년','6%','12%','8%(2년)·12%(3년)'],['5년','10%','20%','20%'],['10년','20%','40%','40%'],['15년','30%','40%','40%']]
B.table('pkg/img/01.png','장기보유특별공제, 2년 살았는지로 표가 갈린다',['기간','표1 일반(보유)','표2 1주택(보유)','표2 1주택(거주)'],rows,hl_col=3,
        note='표2는 보유 기간 중 2년 이상 산 1세대1주택만 · 표2는 보유+거주를 더해 최대 80%',src='소득세법 제95조② 표1·표2, 시행령 제159조의4')
rows2=[['1년(2년 미만)','30%','3,056만원'],['2년','48%','1,809만원'],['5년','60%','1,201만원'],['10년 이상','80%','414만원']]
B.table('pkg/img/02.png','15억원에 판 1주택, 거주 햇수별 양도세',['거주 기간','공제율','세금(지방세 포함)'],rows2,hl_col=2,
        note='6억원에 사서 15년 보유 · 필요경비 0원 · 12억원 넘는 20%만 과세',src='소득세법 제55·95·103·104조, 시행령 제160조, 지방세법 제103조의3으로 계산')
json.dump({'01.png':{'rows':rows},'02.png':{'rows':rows2}},open('pkg/tables.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
print('ok')
