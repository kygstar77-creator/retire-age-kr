# minus1015 본문 그림 — 숫자는 facts.txt [계산]만
import sys, os; sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import blogimg as B
B.bignum('pkg/img/01.png','500만원 30일 이자, 다섯 곳 중 가장 낮은 국민과 높은 우리의 차이','2,425원',sub='국민 5.00% 20,547원 · 우리 5.59% 22,972원 · 금리 차이 0.59%p',src='금융감독원 금융상품통합비교공시 2026년 9월 · 마이너스한도대출 대출금리 평균 · 파이어맵 계산')
B.bignum('pkg/img/02.png','500만원 국민 5.00% · 30일 쓸 돈을 열흘 일찍 갚으면','6,849원 줄어요',sub='20,547원 → 13,698원 · 우리 5.59%는 7,657원 · 은행 차이 2,425원의 약 세 배',src='KB Think 이자 계산 안내 · 매일 마감 잔액 × 연 금리 ÷ 365 · 파이어맵 계산')
