import sys; sys.path.insert(0, r'C:/Users/강영준/Documents/GitHub/retire-age-kr/work')
import blogimg as B
P = r'C:/Users/강영준/Documents/GitHub/retire-age-kr/work/research/gift1003/pkg/img/'
SRC = '상속세 및 증여세법 원문(2025년 10월 1일 시행본)'
B.table(P+'01.png', '증여재산공제, 누구에게 받느냐에 따라',
        ['주는 사람', '10년 공제 한도'],
        [['부모·조부모(합쳐서)', '5천만원 · 미성년 2천만원'],
         ['배우자', '6억원'],
         ['4촌 이내 혈족·3촌 이내 인척', '1천만원'],
         ['혼인·출산(부모·조부모)', '1억원 별도']],
        hl_col=1, src=SRC)
B.table(P+'02.png', '성인 손주가 1억원을 받을 때 증여세',
        ['어떻게 주나', '증여세'],
        [['할머니가 손주에게 바로', '630만 5천원'],
         ['엄마가 먼저 5천만원 준 뒤 할머니가', '1,261만원'],
         ['할머니→아들→손주 두 번', '970만원']],
        hl_col=1, src=SRC + ' · 10년 안 받은 돈 없음·기한 안 신고 3% 공제 가정')
