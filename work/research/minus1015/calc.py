import sys; sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
sys.stdout.reconfigure(encoding='utf-8')
import apis, json
r = apis.finlife("credit")
want = {'국민은행':'국민','신한은행':'신한','농협은행주식회사':'농협','주식회사 하나은행':'하나','우리은행':'우리'}
rows = {}
for x in r:
    if x["상품유형"]=="마이너스한도대출" and x["금리구분"]=="대출금리" and x["은행"] in want:
        rows[want[x["은행"]]] = x
        print(want[x["은행"]], x["상품"], x["공시월"], '900초과', x["등급1"], '801~900', x["등급4"], '701~800', x["등급5"], '평균', x["등급avg"])
P = 5_000_000
def ia(rate, days): return int(P*rate/100*days/365)
print()
for b in ['국민','신한','농협','하나','우리']:
    a = rows[b]["등급avg"]
    print(b, a, [ia(a,d) for d in (10,20,30)])
k, w = rows['국민']["등급avg"], rows['우리']["등급avg"]
print('gap pp', round(w-k,2))
print('30일 국민→우리 차이', ia(w,30)-ia(k,30))
print('국민 20일 vs 30일 차이', ia(k,30)-ia(k,20))
print('우리 20일 vs 30일 차이', ia(w,30)-ia(w,20))
print('국민 10일 vs 30일', ia(k,30)-ia(k,10))
print('우리30 vs 국민20', ia(w,30), ia(k,20))
print('연: 500만 상시 국민/우리', int(P*k/100), int(P*w/100), int(P*w/100)-int(P*k/100))
print('연: 하루 5만원? 한달20일 12개월 국민', ia(k,20)*12, '30일', ia(k,30)*12, '차이', ia(k,30)*12-ia(k,20)*12)
