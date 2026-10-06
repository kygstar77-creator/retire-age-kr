# schdacct1007 본문 표 2장 — spouseinh1007 mkimg 틀. firemap-write 2026-10-06
import sys, json, os; sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import blogimg as B
rows=[['일반계좌 SCHD 직접','30만원','없음','금융소득 2천만원 넘으면 합산','170만원'],
      ['ISA 국내 상장 ETF','30만원','한도 안이면 0원','한도 넘는 몫 9.9%','170만원'],
      ['연금저축·IRP 국내 상장 ETF','30만원','0원(미룸)','꺼낼 때 3.3~5.5%','170만원']]
B.table('pkg/img/01.png','SCHD 배당 세전 200만원, 계좌별로',['계좌','미국 세금','지금 국내 세금','나중에','들어오는 돈'],rows,hl_col=4,
        note='같은 배당을 받는다고 놓은 단순 비교 · 운용보수·환율·지급 시점 차이 뺌 · ISA 한도 200만원(서민형 400만원)',src='조세특례제한법 제91조의18, 소득세법 제129조·제57조의2')
rows2=[['70세 미만','5.5%','9만 3,500원'],['70~79세','4.4%','7만 4,800원'],['80세 이상','3.3%','5만 6,100원']]
B.table('pkg/img/02.png','170만원을 연금으로 꺼낼 때 연금소득세',['나이','세율','세금'],rows2,hl_col=2,
        note='2026년 7월 1일 이후 꺼내는 돈부터 펀드가 미국에 낸 세금의 55%를 소득세 몫(지방세 뺀 금액) 한도로 빼 줌 · 못 뺀 몫은 다음 인출로',src='소득세법 제129조①·⑧~⑩·시행령 제189조의2④, 부칙(2025.12.23)')
json.dump({'01.png':{'rows':rows},'02.png':{'rows':rows2}},open('pkg/tables.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
print('ok')
