# chunga1104 청약 가점 계산 — 주택공급에 관한 규칙 별표1 2.나(2024.12.18 개정, 2026.6.15 시행판 그대로) 표대로
import sys; sys.stdout.reconfigure(encoding='utf-8')
def mujutaek(y):  # 무주택기간(년) → 점수, 1년 미만 2, 15년 이상 32
    return 32 if y >= 15 else 2 + 2*int(y)
def buyang(n): return min(35, 5 + 5*n)
def tong(y):   # 가입기간(년) → 점수
    if y < 0.5: return 1
    if y < 1: return 2
    return min(17, 2 + int(y))
def spouse(y):  # 배우자 가입기간 50%에 대한 점수, 3점 상한
    return min(3, tong(y/2))
print('무주택 만점 나이: 30세부터 15년 → 45세(30세 전 혼인이면 혼인신고일부터)')
S = [
 ('A 52세 부부+미혼 자녀 2(등본 같이)·30세 뒤 쭉 무주택·통장 10년·배우자 통장 10년', 22, 3, 10, 10),
 ('B A에 무주택 부모님 두 분 3년 넘게 등본에', 22, 5, 10, 10),
 ('C A에 부모님이 등본에 있으나 아버지가 집 한 채 소유', 22, 3, 10, 10),
 ('D A에서 31세 자녀가 직장 근처로 전입(등본 분리)', 22, 2, 10, 10),
 ('E 55세 부부만(자녀 결혼·독립)', 25, 1, 10, 10),
 ('F A인데 5년 3개월 전 집을 팔고 무주택이 됨', 5.25, 3, 10, 10),
]
for lab, m, n, t, sp in S:
    a, b, c = mujutaek(m), buyang(n), min(17, tong(t) + spouse(sp))
    print(f'{lab}: 무주택 {a} + 부양 {b}(부양가족 {n}명) + 통장 {c}(본인 {tong(t)}+배우자 {spouse(sp)}) = {a+b+c}')
print('부양가족 1명 = 5점, 무주택 1년 = 2점, 통장 1년 = 1점')
print('배우자 통장 6년 이상이면 50%=3년 → 5점 → 상한 3점:', spouse(6), '· 배우자 2년 → 1년 → 3점:', spouse(2), '· 배우자 1년 → 0.5년 → 2점:', spouse(1))
