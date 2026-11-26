# SQ-1 자료조사 — 나스닥100과 SCHD, 15년 1억과 세후 (youtube-loop 2026-11-21 첫 판)
공개 칸 11/28 11:30 · 관문 11/27 11:30 · 축: 지수(나스닥100) + 배당ETF(SCHD) · 단독 세금 편 아님(세금은 한 장)
근거 파일: analysis.md(① 수요·② 검색어·④ S1~S14) · toc_compare.md(경쟁 16편·포화) · calc_mix_out_1112.txt · calc_krw_out_1120.txt · calc_dca_out_1120.txt · calc_tax_out_1121b.txt · tax_sources_1121.md · raw/law1121/(조문·표 캡처) · raw/comments_q_1121.txt

# 원문
확인일 2026-11-21(법령·세율표 캡처), 2026-11-15(운용사 페이지), 2026-11-20(ECOS 환율·야후 월봉)
- S1 SCHD·QQQ 월말 수정종가(배당 재투자 총수익) 2011-10~2026-10 — 야후 파이낸스 history(adjclose) https://finance.yahoo.com/quote/SCHD/history · https://finance.yahoo.com/quote/QQQ/history (2차 시세 → S7로 운용사 NAV와 대조해 ±0.05%p 안 확인)
- S2 원·달러 월말 매매기준율 — 한국은행 ECOS 731Y001 https://ecos.bok.or.kr/ (2011-10-31 1,104.5원 → 2026-10-30 1,335.3원, calc_krw_out_1120.txt)
- S7 운용사 NAV 연환산(2026-09-30) — QQQ 1년 23.75%·5년 16.31%·10년 20.89% https://www.invesco.com/qqq-etf/en/etf-insights/qqq-quarterly-outlook.html · SCHD 1년 23.36%·5년 9.48%·10년 12.44% https://www.schwabassetmanagement.com/products/schd
- S8 TIGER 미국나스닥100(133690) 총보수 연 0.0068%·분기 분배 https://investments.miraeasset.com/tigeretf/ko/product/search/detail/index.do?ksdFund=KR7133690008 (2026-11-13)
- S9 TIGER 미국배당다우존스(458730) 총보수 연 0.01%·월분배 https://investments.miraeasset.com/tigeretf/ko/product/search/detail/index.do?ksdFund=KR7458730009 (2026-11-13)
- S10 해외 상장 주식 양도 20%·기본공제 250만원·지방 2% — 소득세법 제94조①3호다목·제104조①12호나·제103조①2호, 지방세법 제103조의3①12호나 https://www.law.go.kr/법령/소득세법/제104조 · https://www.law.go.kr/법령/지방세법/제103조의3 (시행 2026.7.1)
- S11 국내 상장 해외 ETF 이익(분배·매매차익) = 배당소득, 원천징수 14%+지방 1.4% — 소득세법 제17조①5호·시행령 제26조의2④·제129조①2호나, 지방세법 제103조의13 https://www.law.go.kr/법령/소득세법시행령/제26조의2 · https://www.law.go.kr/법령/지방세법/제103조의13
- S12 금융소득 2천만원 이하 분리과세·넘으면 종합과세(비교산출세액) — 소득세법 제14조③6호·제62조 https://www.law.go.kr/법령/소득세법/제14조 · https://www.law.go.kr/법령/소득세법/제62조
- S15 미국 배당 제한세율 15% — 국세청 조세조약 제한세율표(2021.2) 미국 행 https://www.nts.go.kr/nts/na/ntt/selectNttInfo.do?mi=2516&nttSn=1293238 · 직투 배당은 14%에서 외국세를 빼고 원천징수(15%>14%라 국내 추가 0) 소득세법 제129조④ https://www.law.go.kr/법령/소득세법/제129조
- S16 종합소득 기본세율표 6~45% — 소득세법 제55조① 표(캡처 raw/law1121/소득세법_제55조_표.png, 마지막 개정 2022.12.31 → 2023~2026 귀속 같은 표) https://www.law.go.kr/법령/소득세법/제55조
- S17 종합소득 지방소득세 표준세율 = 소득세율의 1/10(1천분의 6~45) — 지방세법 제92조① 표(캡처 raw/law1121/지방세법_제92조_표.png, 2026-11-21) https://www.law.go.kr/법령/지방세법/제92조 · ②조례로 ±50% 가감 가능
- S18 외국납부세액공제 한도 = 종합소득산출세액 × 국외원천소득 ÷ 종합소득금액 — 소득세법 제57조① 계산식(캡처 raw/law1121/소득세법_제57조_식.png) https://www.law.go.kr/법령/소득세법/제57조
- S19 배당가산(Gross-up): 집합투자기구 이익(①5호)은 '대통령령으로 정하는 배당소득'만 가산 = 기관전용 사모집합투자기구 배당(시행령 제27조의3③) → 공모 상장 ETF 분배·매매차익은 가산 없음 https://www.law.go.kr/법령/소득세법/제17조 · https://www.law.go.kr/법령/소득세법시행령/제27조의3 (2026-11-21 확인)

# 경쟁
같은 주제 상위 16편(toc_compare.md '# 경쟁 목차', 2026-11-20 조회·자막) 요약
- 말한 것: 기간 수익률(대개 S&P500 기준선)·연도별 표(미국회계사 MPooDiIP2N4)·조합 비율 예시(부티플·여운봉)·환율 이야기(리치노마드 AKV7ZfGORDg)·커버드콜 섞은 상품(부티플 XpbnvNMADlg)
- 빠뜨린 것: ① 나스닥100을 기준선으로 SCHD와 같은 15년을 나란히 놓은 편 0 ② 섞는 비율별(100·50·0%) 실제 값 0 ③ 원화로 1억 넣었다 친 끝값 0 ④ **같은 수익이라도 '직투 vs 국내 상장'에 따라 판 해 세금이 얼마나 달라지는지** 숫자로 낸 편 0(세율 이름만 말함 — 농부의 경제학 D4n2AjX04N0 7:19 '22%·15.4%')
- 대표 1등: 집구석 경제학 _G3C_oVh2SU(157,829회·배수 12.37, 2026-11-12 확인) https://www.youtube.com/watch?v=_G3C_oVh2SU

# 질문
실제 질문(유튜브 댓글 2026-11-21 받음 raw/comments_q_1121.txt, commentThreads relevance 상위) → 우리 답
| # | 질문(원문 요지) | 출처 | 우리 답 | 장 |
|---|---|---|---|---|
| Q1 | "직투는 양도소득세만 있지 종합소득세와 관계없지 않나요?" | https://www.youtube.com/watch?v=z45kjKrdQEg&lc=Ugxw_rcHIoOgMU-S5Up4AaABAg | 판 차익은 맞음(양도소득 분리과세 22%, S10). 배당은 아님 — 직투 배당도 배당소득이라 금융소득 2천만원 계산에 들어감(S11·S12, 제17조①6호) | 6장 |
| Q2 | "해외직투 배당금도 2000만원 넘으면 과세되나요?" | https://www.youtube.com/watch?v=z45kjKrdQEg&lc=UgzyS84MEtWNwpbFYxV4AaABAg | 들어감. 다만 미국에서 15%를 이미 떼서 14% 원천징수는 추가 0, 넘는 해엔 외국납부세액공제(S18) | 6장 |
| Q3 | "VOO,QQQM 직투 말고 국내ETF S&P500이나 미국나스닥100으로 해도 상관없는건가요?" | https://www.youtube.com/watch?v=z45kjKrdQEg&lc=Ugx77hGqdnUca64jmlt4AaABAg | 같은 지수라도 일반 계좌 세금이 다름: 국내 상장은 판 차익도 배당소득 → 한 해에 몰아 팔면 종합과세. 15년 1억 SCHD만 기준 세후 직투 6.47억 vs 국내 상장 5.61억(다른 소득 0), 5년이면 국내 상장이 366만원 많음 | 6장 |
| Q4 | "국민연금 매달 150만원 + 쉬드 배당소득 합해 2천만원 종합소득세 계산을 하나요?" | https://www.youtube.com/watch?v=z45kjKrdQEg&lc=UgznaI8dCeagSEg4BH94AaABAg | 2천만원 기준은 이자·배당(금융소득)만 셈(S12). 넘으면 그때 연금 같은 다른 종합소득과 합쳐 누진세율 | 6장 |
| Q5 | "금융소득종합과세와 건보료는요?" | https://www.youtube.com/watch?v=XpbnvNMADlg&lc=Ugzuuv7rQUScnOJ8QyZ4AaABAg | 이번 조사 밖(숫자 없음) — '한계'에 적고 말로는 "건보료도 따로 따져 봐야 한다" 한 줄만 | 6장 끝 |
| Q6 | "tiger 미국배당다우존스는 절세계좌에서 과세이연 되는데요?" | https://www.youtube.com/watch?v=_G3C_oVh2SU&lc=Ugyu8ln5fkOTDaYik8N4AaABAg | 맞음, 연금저축·ISA 안이면 위 계산이 바뀜 — 이 편은 일반 계좌만 계산, 계좌 이름만 말함(권유 없음) | 6장 |
| Q7 | "나스닥100만 살까, SCHD를 섞을까?"(경쟁 첫 30초에서 '댓글에서 가장 많이 받은 질문') | https://www.youtube.com/watch?v=MPooDiIP2N4 | 15년 1억 달러 기준 SCHD 6.77억·반반 10.10억·QQQ 13.56억, 그러나 최근 5년은 차이가 좁고 낙폭은 QQQ가 큼 | 1~4장 |
얼마나 자주: 7편 상위 댓글(relevance) 중 질문 부호와 주제어가 있는 53줄(raw/comments_q_1121.txt) — 위 표는 그중 이 편 장에 답이 있는 것만 골랐음.

# 우리만
원자료로 직접 계산한 새 숫자(경쟁 0편)
- 15년(2011-10→2026-10) 1억 달러 기준 SCHD 6.77억·반반 10.10억·QQQ 13.56억, 최대낙폭 −21.5%·−24.0%·−32.6% (calc_mix_out_1112.txt)
- 원화로 넣었다 치면 SCHD 8.18억·반반 12.21억·QQQ 16.39억, 그중 환율 몫 +1.41·+2.11·+2.83억 (calc_krw_out_1116.txt)
- 매달 100만원 15년: 5.34억·7.14억·8.81억 (calc_dca_out_1120.txt)
- **세후(일반 계좌, 2026-10 한 번에 팜)**: SCHD만 직투 6.47억 vs 국내 상장 5.61억(다른 소득 0) — 국내 상장은 판 해 차익 전부가 배당소득이라 그해 세금 2.02억, 15.4%로만 끝났다면 0.81억(+1.20억) · QQQ만 직투 12.87억 vs 9.62억 · 최근 5년은 국내 상장이 329만~405만원 많음 (calc_tax_out_1121b.txt)

# 왜
- 15년 QQQ가 앞선 이유: 원문(운용사)에 이유 문장 없음 → 말하지 않음. 지수 구성(나스닥100 = 나스닥 상장 비금융 100개, raw/ndx_methodology.txt)·업종 비중만 사실로 말함
- 국내 상장이 판 해에 세금이 커지는 이유: 시행령 제26조의2④가 국내 상장 주식 매매손익만 빼서 해외 주식 손익이 '집합투자기구 이익'(배당소득)에 들어가고(S11), 금융소득이 2천만원을 넘으면 제62조로 다른 소득과 합쳐 누진(S12·S16)
- 직투 배당에 국내 세금이 더 안 붙는 이유: 국내 14%에서 미국 15%를 빼면 0(제129조④, S15)
- 5년은 국내 상장이 조금 나은 이유: 차익이 작아 판 해 금융소득이 덜 커지고, 직투는 250만원 공제 뒤 22%라 15.4%보다 세율이 높음(S10·S11)

# 그래서
- 장마다 할 일(제도): ① 내 계좌가 일반·연금저축·ISA 중 어디인지 먼저 확인(세금이 계좌에 따라 다름) ② 국내 상장 해외 ETF를 일반 계좌에서 오래 들고 있다면, 판 해 금융소득이 2천만원을 넘는지 미리 셈 — 넘으면 다음 해 5월 종합소득세 신고(소득세법 제70조) ③ 직투는 판 다음 해 5월 양도소득세 신고(250만원 공제)
- 권유 없음: 어느 상품·어느 계좌를 고르라고 말하지 않음, 숫자와 조건만

# 누구라면
- 다른 소득 0인 은퇴자: 15년 SCHD 1억 직투 6.47억 vs 국내 상장 5.61억 — 판 해 한 번에 팔면 차이 8,630만원
- 다른 소득 5천만원인 직장인: 같은 조건 6.46억 vs 5.44억 — 차이 1.02억으로 커짐
- 5년만 들고 있는 사람: 국내 상장이 300만~400만원 남짓 많음(다른 소득 0) → '직투가 늘 낫다'가 아님
- 연금저축·ISA 안에서 사는 사람: 이 계산 밖(과세이연·분리과세 특례 — 계좌 규정은 따로)

# 함정
- 국내 상장 해외 ETF를 일반 계좌에서 15년 모아 **한 해에 한 번에 팔면** 차익 전부가 그해 금융소득 → 2천만원을 훌쩍 넘어 누진세율(SCHD만 1억 15년: 15.4%로 끝났을 때보다 1.20억 더). 나눠 팔면 달라짐(계산은 '한 번에 팜'만)
- 직투 배당도 2천만원 계산에 들어감(Q1·Q2의 흔한 오해) — 미국 15%가 이미 빠져 있어 원천징수는 더 없지만, 종합과세 해엔 신고 대상

# 한계
- 국내 상장 ETF는 'QQQ·SCHD와 똑같이 움직였다'고 친 가정. TIGER 미국배당다우존스는 2023 상장이라 15·10년 값은 가상
- 건강보험료(피부양자 자격·지역가입자 금융소득 반영): 확인 안 함 — 숫자 없이 말 한 줄
- 제129조⑦ 간접투자외국법인세액 이월공제·제57조② 10년 이월공제는 모형에 넣지 않음
- 종합소득금액(C)을 과세표준으로 근사(소득공제 전후 차이 무시) · 지방소득세 조례 ±50%(제92조②) 무시
- 한미조세조약 조문 원문은 안 열고 국세청 제한세율표(2021.2)로 확인 · 미국 쪽 W-8BEN 실무는 안 봄
- 현행 세법(2026.11)을 2011~2026 모든 해에 똑같이 적용 — 과거 실제 세금 아님
- 세금 값은 2026-10 말 한 번에 판 경우 하나. 나눠 팔기·환전 수수료·증권사 수수료는 뺌

# 대조
대본 v1 전이라 '대본 값'은 쓸 말(예정). 대본 쓴 뒤 다시 맞춤.
| 원문 | 원값 | 대본 값 | 출처 |
|---|---|---|---|
| 15년 1억 SCHD·QQQ(달러) | 6.77억·13.56억 | 6억 8천·13억 6천 | S1 https://finance.yahoo.com/quote/SCHD/history (2차 — S7 운용사 NAV 대조) https://www.schwabassetmanagement.com/products/schd |
| 반반 15년 | 10.10억 | 10억 남짓 | S1 https://finance.yahoo.com/quote/QQQ/history · https://www.invesco.com/qqq-etf/en/etf-insights/qqq-quarterly-outlook.html (2차 — S7 대조) |
| 환율 2011-10-31 → 2026-10-30 | 1,104.5 → 1,335.3원 | 1,100원대 → 1,335원 | S2 https://ecos.bok.or.kr/ |
| 직투 양도세 | 20%+지방 2%, 250만원 공제 | 22%, 250만원 빼고 | S10 https://www.law.go.kr/법령/소득세법/제104조 |
| 국내 상장 해외 ETF 차익 | 배당소득 14%+1.4% | 배당소득, 15.4% | S11 https://www.law.go.kr/법령/소득세법시행령/제26조의2 |
| 금융소득 종합과세 기준 | 연 2,000만원 | 2천만원 | S12 https://www.law.go.kr/법령/소득세법/제14조 |
| 미국 배당 원천 | 15% | 15% | S15 https://www.nts.go.kr/nts/na/ntt/selectNttInfo.do?mi=2516&nttSn=1293238 |
| 최고 세율 | 45%(+지방 4.5%) | 최고 49.5% | S16·S17 https://www.law.go.kr/법령/소득세법/제55조 · https://www.law.go.kr/법령/지방세법/제92조 |
| 15년 SCHD 세후(다른 소득 0) | 직투 6.47억·국내 상장 5.61억 | 6억 5천 vs 5억 6천 | calc_tax_out_1121b · S10·S11·S12 https://www.law.go.kr/법령/소득세법/제62조 |
| 판 해 세금 vs 15.4%만 | 2.02억 vs 0.81억 | 2억 vs 8천만 | calc_tax_out_1121b · S12 https://www.law.go.kr/법령/소득세법/제62조 |
| 5년 SCHD 세후(다른 소득 0) | 직투 1.70억·국내 상장 1.74억(−366만원) | 국내 상장이 3백만원 남짓 많음 | calc_tax_out_1121b · S11 https://www.law.go.kr/법령/소득세법/제129조 |
| SCHD 직투 분배 세후(1억·세전 295만원, 11/24 v1.7 더함) | 295만 × (1 − 0.15) ≈ 251만원, 국내 추가 0 | 250만원 정도 | S15 https://www.nts.go.kr/nts/na/ntt/selectNttInfo.do?mi=2516&nttSn=1293238 · https://www.law.go.kr/법령/소득세법/제129조 |
| 2천만원 기준에 연금 넣나(Q4, 11/24 v1.7 더함) | 이자·배당만 셈, 넘으면 다른 종합소득(연금소득 포함)과 합산 | 연금은 2천만원 셀 때 안 넣음 | S12 https://www.law.go.kr/법령/소득세법/제14조 · https://www.law.go.kr/법령/소득세법/제62조 |
| 커버드콜 섞은 상품 사례(183행, 11/26 더함) | 1등 영상 제목 'QQQ+SCHD' 상품 = 나스닥100 데일리 커버드콜(자막) | 'QQQ와 SCHD를 합쳤다'고 소개된 상품이 커버드콜인 경우 | 2차 — https://www.youtube.com/watch?v=XpbnvNMADlg (breakdown/XpbnvNMADlg_transcript.txt) · https://investments.miraeasset.com/tigeretf/ko/product/search/detail/index.do?ksdFund=KR7133690008 (기초지수 칸 확인 방법) |

# 올리기 전 확인
확인일 2026-11-26(youtube-loop 16:4x~17:xx) · 공개 11/28 11:30 · 관문 11/27 11:30 · 다음 확인: 11/27 관문 때 gate가 이 날짜(1일 안)로 통과
- 운용사: QQQ NAV 9/30 1년 23.75%·5년 16.31%·10년 20.89% 그대로(10/28 글) https://www.invesco.com/qqq-etf/en/etf-insights/qqq-quarterly-outlook.html · SCHD 운용사 페이지 403(막힘) https://www.schwabassetmanagement.com/products/schd → 야후로 대신: 11/25 종가 SCHD 35.29·QQQ 633.93, 분기 분배 행(12/10·3/25·6/24·9/23) https://finance.yahoo.com/quote/SCHD/history · https://finance.yahoo.com/quote/QQQ/history
- 국내 상장: TIGER 미국나스닥100 총보수 연 0.0068%·분기(1·4·7·10월) 그대로 https://investments.miraeasset.com/tigeretf/ko/product/search/detail/index.do?ksdFund=KR7133690008 · TIGER 미국배당다우존스 연 0.01%·매월 그대로 https://investments.miraeasset.com/tigeretf/ko/product/search/detail/index.do?ksdFund=KR7458730009 (두 쪽 기준일 2026.11.26)
- 환율: https://ecos.bok.or.kr/ 열림(본문은 앱 화면이라 글자로 못 읽음) — 쓴 값은 2011-10-31·2026-10-30 월말 확정값이라 바뀌지 않음
- 법령 12조(국가법령정보센터 웹, raw/law1126/ ↔ raw/law1121/ 본문 비교 12개 모두 같음): 소득세법 [시행 2026. 7. 1. 법률 제21221호] 제14조·제17조·제55조·제57조·제62조·제104조·제129조 https://www.law.go.kr/법령/소득세법/제14조 · https://www.law.go.kr/법령/소득세법/제17조 · https://www.law.go.kr/법령/소득세법/제55조 · https://www.law.go.kr/법령/소득세법/제57조 · https://www.law.go.kr/법령/소득세법/제62조 · https://www.law.go.kr/법령/소득세법/제104조 · https://www.law.go.kr/법령/소득세법/제129조 · 시행령 [시행 2026. 10. 1. 대통령령 제36737호] 제26조의2·제27조의3 https://www.law.go.kr/법령/소득세법시행령/제26조의2 · https://www.law.go.kr/법령/소득세법시행령/제27조의3 · 지방세법 [시행 2026. 7. 1.] 제92조·제103조의3·제103조의13 https://www.law.go.kr/법령/지방세법/제92조 · https://www.law.go.kr/법령/지방세법/제103조의3 · https://www.law.go.kr/법령/지방세법/제103조의13
- 경쟁 사례: 1등 영상 그대로 공개·조회 233,206(11/26 videos.list) https://www.youtube.com/watch?v=XpbnvNMADlg
- 조세조약: 국세청 제한세율표 글(2021.02.09, 첨부 xlsx — raw/law1121/nts_treaty_rates_2021_02.xlsx 미국 배당 15%) 그대로 열림 https://www.nts.go.kr/nts/na/ntt/selectNttInfo.do?mi=2516&nttSn=1293238
- 기준일: 수익률·환율 = 2026-10 월말 종가·월말 매매기준율(10/30) · 운용사 NAV = 9/30 · 총보수 = 11/26 운용사 페이지 · 세법 = 2026-11-26 현행(소득세법 7/1·시행령 10/1 시행분)
- 바뀐 것: 없음 — 쓴 숫자는 모두 10월 말 확정값, 법령 12조 본문 11/21과 같음, 조사(11/21) 뒤 공표 일정(release_calendar) 끼인 것 없음
- 새로 찾은 것: 대본 다시 심사(v1.7) 레드팀 — 국내 상장 ETF 분배금 원천징수는 미국에서 뗀 세금만큼 빼고 뗌(제129조, calc_tax 가정 2와 같음)인데 151행 자막 '원천징수 15.4%'만 보면 이중으로 떼는 것처럼 읽힘 → 설명란 한 줄로 풀기(PD·editor에 요청) · 11월 세법 개정 통과 소식은 법령 현행본 머리에 없음(국회 통과 뒤 공포 전 법은 확인 안 함)
