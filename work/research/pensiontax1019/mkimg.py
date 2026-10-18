import sys, json, os; sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import blogimg as B
r1=[['55~69세','5.5%','66만원'],['70~79세','4.4%','52만 8천원'],['80세 이상·종신형','3.3%','39만 6천원']]
B.table('pkg/img/01.png','연금저축 연금 월 100만원, 나이별 세금',['나이','세율(지방소득세 포함)','한 해 1,200만원이면'],r1,hl_col=2,note='연금저축·IRP 연금수령 원천징수 기준 · 종신형은 2026년 1월 1일 이후 수령분',src='국세청, 소득세법 제129조, 직접 계산',W=1640)
r2=[['매달 뗀 세금 합계','110만원','이미 낸 돈'],['종합소득세로 정산','약 76만 6천원','110만원보다 적어 33만 4천원 환급'],['15% 분리과세 고르면','330만원','5.5%보다 높아 손해']]
B.table('pkg/img/02.png','연금저축 연금 한 해 2,000만원, 세금 세 가지 방법',['방법','한 해 세금','메모'],r2,hl_col=1,note='69세 이하·다른 소득 없음·본인 기본공제만 있다고 본 값 · 지방소득세 포함',src='소득세법 제47조의2·제55조·제64조의4, 직접 계산',W=1640)
json.dump({'01.png':{'rows':r1},'02.png':{'rows':r2}},open('pkg/tables.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
