# 쇼츠 위 제목 띠 실측 (2026-11-19, visual-designer)

방법: 경쟁 상위 채널 14곳(outlier_channels.json hits 상위) 중 쇼츠 탭이 열린 11곳의 최근 쇼츠 3편씩 = **32편**, https://i.ytimg.com/vi/<id>/oar2.jpg(1080×1920, 한 편당 한 컷)을 받아 5% 눈금자를 얹은 판(ruler_top50.png, 번호=아래 표 번호)에서 **위 제목 글자·띠가 끝나는 높이 / 화면 높이**를 읽음. 오차 ±2%p. 자동 가장자리 검출은 검은 띠·사진 가장자리를 헷갈려 버리고 눈으로 읽음.

| # | 편 주소 | 채널 | 꼴 | 제목 끝 높이(%) |
|---|---|---|---|---|
| 1 | https://youtube.com/shorts/J8xaL8yvyHo | 절세미녀 김희연 회계사 | 글자만 사진 위 | 20 |
| 2 | https://youtube.com/shorts/ZZmKOC5RueE | 절세미녀 김희연 회계사 | 글자만 사진 위 | 20 |
| 3 | https://youtube.com/shorts/v9HejYRXfw4 | 절세미녀 김희연 회계사 | 글자만 사진 위 | 19 |
| 4 | https://youtube.com/shorts/GxmxUj1_gZA | 서울경제TV | 고정 띠 | 34 |
| 5 | https://youtube.com/shorts/H4IjyKCp6XE | 서울경제TV | 고정 띠 | 34 |
| 6 | https://youtube.com/shorts/E6Ga6Z5dbh8 | 서울경제TV | 고정 띠 | 34 |
| 7 | https://youtube.com/shorts/boKS_u_0wv8 | 싱글파이어 | 고정 띠 | 19 |
| 8 | https://youtube.com/shorts/sxGYImPCUHk | 싱글파이어 | 고정 띠 | 21 |
| 9 | https://youtube.com/shorts/NJ6UcHcn4qg | 싱글파이어 | 고정 띠 | 21 |
| 10 | https://youtube.com/shorts/eScwSoNOBR0 | 똑재TV | 종이 카드(띠 없음) | 19 |
| 11 | https://youtube.com/shorts/TIe-gOtwklc | 똑재TV | 종이 카드(띠 없음) | 19 |
| 12 | https://youtube.com/shorts/KxVGbgjU6FM | 똑재TV | 제목이 가운데·위 띠 없음 | 확인 안 함(위 제목 없음) |
| 13 | https://youtube.com/shorts/N6hJfLSzzjE | 소수몽키 | 위 제목 없음(아래 자막) | 확인 안 함(위 제목 없음) |
| 14 | https://youtube.com/shorts/85Z4o8XrUKw | 소수몽키 | 고정 띠 | 22 |
| 15 | https://youtube.com/shorts/FK4rfHL44ZU | 소수몽키 | 고정 띠 | 22 |
| 16 | https://youtube.com/shorts/nON28iNuVoM | 은퇴머니 - 은퇴 현금흐름 설계 | 어두운 카드(띠 없음) | 21 |
| 17 | https://youtube.com/shorts/rx5grU6ktfc | 은퇴머니 - 은퇴 현금흐름 설계 | 어두운 카드(띠 없음) | 21 |
| 18 | https://youtube.com/shorts/XPUy6eJ_VkE | 은퇴머니 - 은퇴 현금흐름 설계 | 어두운 카드(띠 없음) | 21 |
| 19 | https://youtube.com/shorts/wAhgiel_L0s | 투자360 | 고정 띠 | 24 |
| 20 | https://youtube.com/shorts/p47FUQThXRc | 투자360 | 고정 띠 | 24 |
| 21 | https://youtube.com/shorts/OwxY6FtoO2g | 투자360 | 고정 띠 | 24 |
| 22 | https://youtube.com/shorts/6L6iz6sQ73o | YTN | 고정 띠 | 24 |
| 23 | https://youtube.com/shorts/YtOp0iEjuqs | YTN | 고정 띠 | 24 |
| 24 | https://youtube.com/shorts/3WXGsVyf2Hk | 미국 주식 채널 - 에디 Eddie | 글자만 어두운 바탕 | 18 |
| 25 | https://youtube.com/shorts/qu71gIlhaDE | 미국 주식 채널 - 에디 Eddie | 고정 띠 | 24 |
| 26 | https://youtube.com/shorts/hFf2vp4RK-o | 미국 주식 채널 - 에디 Eddie | 고정 띠 | 19 |
| 27 | https://youtube.com/shorts/H5d6vkHZog0 | 위키타카 | 고정 띠 | 22 |
| 28 | https://youtube.com/shorts/otreJJmyZQE | 위키타카 | 고정 띠 | 22 |
| 29 | https://youtube.com/shorts/2TQF7WfvCYk | 위키타카 | 고정 띠 | 22 |
| 30 | https://youtube.com/shorts/0RCdKaYcKIw | 자람들 - 자립하는사람들 | 고정 띠 | 27 |
| 31 | https://youtube.com/shorts/bCsGrAvuSvs | 자람들 - 자립하는사람들 | 고정 띠 | 27 |
| 32 | https://youtube.com/shorts/6R7ajWEoYO4 | 자람들 - 자립하는사람들 | 고정 띠 | 27 |

- 고정 띠(색 바탕이 따로 깔린 위 제목) 21편: 중앙 24% · 범위 19~34% (8개 채널 단위 중앙 약 23%).
- 띠 없이 위에 글자만 얹은 편(사진·종이·어두운 카드) 9편: 제목 끝 18~21%. 위 제목 없음 2편.
- 32편 중 위 제목을 화면 위 약 18~34%에 둔 편 30편. 가인지TV 원본 URL 목록 중 쇼츠 탭이 안 열린 채널(가인지TV 등 3곳 포함)은 이번 표본에 없음 → 지난 판 '가인지TV 약 18%'는 이 표로 재확인 못 함(확인 안 함).

한계(확인 안 함): ① oar2는 한 컷이라 '끝까지 고정'은 못 봄 ② 우리 쇼츠의 같은 값은 이번에 새로 재지 않음(지난 판 '약 5%'는 sb0 어림 그대로) ③ 채널 11곳이라 같은 채널 3편은 서로 닮음(독립 표본 아님, 채널 단위 중앙을 같이 적음) ④ 눈금자 읽기, 픽셀 자동 측정 아님.

값·코드는 바꾸지 않음. registry 후보 B-58.
