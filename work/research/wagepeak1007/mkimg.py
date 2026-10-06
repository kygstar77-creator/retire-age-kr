# wagepeak1007 본문 표 2장 — spouseinh1007 mkimg 틀. firemap-write 2026-10-06
import sys, json, os; sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import blogimg as B
rows=[['아무것도 안 함','1억800만원','퇴직 때 월급 360만원 × 30년'],['피크 직전 중간정산(퇴직금제도만)','1억6,800만원','25년치 1억5,000만 + 5년치 1,800만'],['피크 직전 DC 전환','1억6,980만원','25년치 1억5,000만 + 부담금 1,980만']]
B.table('pkg/img/01.png','임금피크제 퇴직금, 세 길로 받는 돈',['길','받는 돈(세전)','어떻게'],rows,hl_col=1,
        note='근속 25년 차 월급 600만원 · 피크 5년 80·70·60·60·60% · DC 운용수익 0% 가정',src='근로자퇴직급여 보장법 제8·20조, 근로기준법 제2조')
rows2=[['중간정산 사유(퇴직금제도)','정년 연장·보장하며 임금 줄이는 제도 시행'],['회사가 할 일','퇴직급여 줄 수 있다고 미리 알림'],['회사가 할 일','근로자대표와 협의해 DC 변경·산정기준 개선'],['안 지키면','500만원 이하 벌금'],['DC 부담금','해마다 임금 총액의 12분의 1 이상']]
B.table('pkg/img/02.png','임금피크제 앞두고 법에 적힌 것',['항목','내용'],rows2,hl_col=1,
        note='회사 규약에 따라 전환 시점·방식은 다름',src='근퇴법 시행령 제3조①6호, 근퇴법 제20·32조⑤·46조')
json.dump({'01.png':{'rows':rows},'02.png':{'rows':rows2}},open('pkg/tables.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
print('ok')
