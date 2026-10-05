# 대출이자 v1 구현본 캡처 (firemap-product-dev, 2026-10-05 17:27)

- 코드: src/components/firemap/LoanCalc.jsx · 열기: firemap.kr/#loan(dev 빌드). **TOOL_PAGES·메뉴·사이트맵 미등록** — copywriter 문구(10/20)·editor-web 통과 뒤 /calc/loan 등록.
- 캡처: impl-375 · impl-375-dark · impl-320 · impl-1280 · impl-375-full (shot_impl.py, vite build 정적본)
- 숫자(시안 ② 엔진 값과 원 단위 일치): 65세 · 매달 1,520,056원 · 총이자 2억 4,722만원 · 더 갚기 10만원 → 61세·43개월 일찍·이자 3,408만원 덜 · 상환 317회
- 넘침: scrollWidth 375/320/1280 = 뷰포트와 같음(0)
- 주황 버튼 아래끝: 375 → 618px(시안 714보다 위) · **320 → 552px(첫 화면 568 안)** — 공통 흠 ② 실측
  - 320 처음엔 588(접힘선 밖) → 359 이하에서 더 갚기 카드 여백 16·값 칸 여백 축소·눈금 글자(0원/100만원) 숨김으로 552
- 시안과 다르게 한 것: 슬라이더 RangeField(기존 부품) 재사용 → 값 칸 누르면 직접 입력 가능. 색만 잉크 트랙·흰 손잡이 28px로 덮어씀(주황은 행동 1곳)
- 공통 흠 ①(조건 행이 편집 가능해 보이나): 연봉 v5 운영 ListRow 그대로(값 굵게·chevron), 시트 자동 열기 없음 — 시안 결정대로
- 이벤트: calc_input_start/calc_result(calc=loan, 공통) · loan_edit{row} · loan_extra{bucket 0/10/30/50/100만} · loan_retire_click{age_bucket} · loan_share — growth 계측 시안(10/20) 오면 이름 맞춤
- 다크: 앱이 OS 다크를 따르지 않아(현재 운영과 같음) 375-dark = 라이트와 같음
- 글자: 전부 시안 가안([카피 몫]) — 편집 통과 전 운영 금지
