# j1pair1104 자료조사 (firemap-write 2026-11-03 18:2x~) — 카페 2026-11-04 12:40 칸 · 세금(종부세) · J-1 롱폼(NNcjTE0L7yg, 11/4 11:30 공개) 짝 긴 글
영상은 20억·55세 한 사람의 고지서. 이 글은 ep/J-1/cafe.md 재료(공시가격 12~40억 × 네 갈래 × 산다/안 산다)를 글로 — 숫자는 J-1 calc_out·calc2_out 그대로, 새 계산 0. 영상에 없던 새 사실: 11/3 국회 의안 상태(소위 회부 뒤 처리 전·부수법안 지정 신청), 경쟁 3편이 모두 8/3 첫 안 기준이라는 점.

## 검증
- 수요: kwvol '종부세' 6,630(J-1 bench_check 10/22) · 자동완성 '종부세 개편안 시행일'·'종부세 개편안 공동명의'(J-1 Q1·Q4)
- 경쟁에서 터진 증거: 머니투데이 '69만원 내던 20억 아파트 종부세…거주용 27만원 vs 비거주 190만원' 조회 93,342·댓글 43(서플 표시, 11/3 확인)
- 우리 실측: J-1 짝 칸(slots 11/4 12:40, 회의 11/2 21:37 배정)

# 원문
| S | 원문 | 날짜·쪽 | 쓴 값 | 주소 |
|---|---|---|---|---|
| S1 | 국회 의안정보시스템 의안 2221046 종합부동산세법 일부개정법률안(정부) | 2026-11-03 18:2x 브라우저로 다시 엶 · 주요내용 가~아 · 소위 회부 09-28, 처리일 빈칸 | 14억 초과 · 거주 14억/비거주 12억 · 부부 9억/6억 · 하한 60→70% · 거주기간 공제 · 납부유예 65세·10년·10% · 처리 전 | https://likms.assembly.go.kr/bill/bi/billDetailPage.do?billId=ARC_O2S6R0Z9Z0P3V1Z0A5J3R1Y8B6L3L6 |
| S2 | 재정경제부 2026년 세제개편안 상세본(8/3) | J-1 raw/mofe_0803_6 p.60~67 (10/17 받음, 공표 자료) | 6~12억 세율 1.0→1.3% · 세액공제 5년 20%·10년 40%·15년 50%·합 80% · 2028 한도 600만원 · 적용 2027.1.1 · 납부유예 이자 3.1% | https://www.mofe.go.kr/nw/nes/detailNesDtaView.do?searchBbsId1=MOSFBBS_000000000028&menuNo=4010100&searchNttId1=MOSF_000000000078809 |
| S3 | 재정경제부 세제개편안 정부안 확정(9/1) | J-1 raw/mofe_0901 | 비거주 12억 유지 · 부부 비거주 각 6억 · 상한 150% 유지 | https://www.mofe.go.kr/nw/nes/detailNesDtaView.do?searchBbsId1=MOSFBBS_000000000028&menuNo=4010100&searchNttId1=MOSF_000000000079193 |
| S4 | 국세청 공동명의 1주택자 특례 안내 | J-1 10/17·11/2 확인 | 9.16~9.30 신청 · 다음 연도부터 계속 적용 | https://www.nts.go.kr/nts/cm/cntnts/cntntsView.do?mi=40406&cntntsId=238930 |
| S5 | 국세청 종합부동산세 납부 안내 | J-1 11/2 확인 | 정기고지 12.1~12.15 · 올해는 현행법 | https://www.nts.go.kr/nts/cm/cntnts/cntntsView.do?mi=2356&cntntsId=7738 |
| S6 | 파이어맵 계산 longform/ep/J-1/calc.py·calc2.py → calc_out.txt·calc2_out.txt | 9/1 정부안 · 공시가격 그대로 · 재산세 공정시장가액비율 45% 가정 | 공시가격별·네 갈래·문턱·공동명의 | https://youtu.be/NNcjTE0L7yg |

# 질문
1. 종부세 개편안 공동명의는 어떻게 되나(유튜브 댓글 좋아요 445) — https://www.youtube.com/watch?v=MxQmV3al5sQ&lc=Ugx-T1sJQ9fvFMIFEvl4AaABAg → 각자 9억 그대로(살면), 특례와 각자 중 유리한 쪽은 나이·산 햇수로 갈림(c04)
2. 한 집에 30년 산 것도 할인이 더 되나 — https://www.youtube.com/watch?v=SLh90bWU7Tw&lc=UgyoxJQTkHNS2dO4X2B4AaABAg → 15년부터 같음, 70세 20억 15년·30년 모두 38만원(c02)
3. 종부세 개편안 시행일·국회 — https://ac.search.naver.com/nx/ac?q=%EC%A2%85%EB%B6%80%EC%84%B8%20%EA%B0%9C%ED%8E%B8 → 통과하면 2027.6.1 기준분, 11/3 현재 소위 처리 전(c01·c06)
4. 9억에 산 집이 40억, 20년 실거주는 얼마나 — https://www.youtube.com/watch?v=SLh90bWU7Tw&lc=UgzXljFUVj1wr35OxBx4AaABAg → 공시 40억 55세·10년 거주 +820만원, 600만원 한도 때문(c02·표)

# 왜
- 사는 집이 줄고 안 사는 집이 느는 이유: 공제가 거주 14억·비거주 12억(S1 다) + 세액공제가 산 햇수로(S1 마)
- 안 사는 집 14억 문턱: 내는 기준(§7① 14억 초과)과 공제(§8① 12억)가 따로(S1 가·다)
- 비싼 사는 집이 느는 이유: 공정시장가액비율·세율 인상(S1 나, S2) + 2028 세액공제 600만원 한도(S2)
- 15년 넘으면 같은 이유: 거주기간 공제 15년 50%가 끝(S2)
- 원문에 이유 없는 것: 거주와 비거주를 왜 나눴는지 — 의안 제안이유는 '실거주자의 조세 부담 완화' 한 줄(S1)

# 그래서
- 올해 12월 고지서는 지금 법(S5) — 바뀌면 2027.6.1 기준분부터(S2)
- 부부 공동명의: 특례는 매년 9.16~9.30 신청, 한 번 하면 계속 적용(S4) → 통과되면 다음 신청 기간 전에 각자 납부와 비교
- 65세 이상·10년 거주·보유세가 소득 10% 이상이면 납부유예 신청 가능(S1 아), 이자 연 3.1%(S2)
- 국회 진행은 의안번호 2221046으로 확인(S1)

# 누구라면
1. 그 집에 사는 1주택, 공시 23억 이하: 2028 보유세 조금 줄어듦
2. 그 집에 살지 않는 1주택: 14억 넘으면 바로 생김, 20억 +141만원
3. 부부 공동명의: 55세·10년은 각자, 70세·15년은 특례가 적음
4. 공시 40억대 사는 집: 600만원 한도로 +820만원

# 함정
1. 안 사는 집은 14억을 조금만 넘어도 12억 넘는 몫 전체에 세금(14.01억 → 54만원)
2. 공동명의 특례는 한 번 신청하면 계속 적용 — 규칙이 바뀌면 유리했던 쪽이 바뀔 수 있음(S4)
3. 8월 첫 안(비거주 9억·상한 200%) 기사 숫자 — 9/1 정부안에서 바뀜(S3). 경쟁 3편이 모두 첫 안 기준
4. '정부안 확정' 제목 — 법은 국회 소위 단계(S1)

# 한계
- 정부안은 국회 처리 전 — 숫자가 바뀔 수 있음(11/3 기준)
- 공시가격 그대로·재산세 공정시장가액비율 45% 가정(2027년 뒤 시행령)
- 거주 판정 기준·산 햇수 세는 시점은 시행령 위임, 아직 없음(확인 안 함)
- 공동명의 계산은 반반 지분·다른 주택 없음·세부담 상한 안 걸림 가정
- 납부유예 '집 팔 때 낸다'는 이번에 원문 다시 안 봐서 글에서 뺌

# 대조
| 항목 | 원문·계산 값 | 글 값 | 출처 |
|---|---|---|---|
| 20억 사는 집(55세·10년) | 618.9 → 596.4(−22.5) | 22만원쯤 줄어요 · 619만원에서 596만원 · −22만원(그림) | S6 · https://likms.assembly.go.kr/bill/bi/billDetailPage.do?billId=ARC_O2S6R0Z9Z0P3V1Z0A5J3R1Y8B6L3L6 |
| 20억 안 사는 집 | 618.9 → 759.8(+140.9) | 140만원 넘게 · 141만원쯤 · +141만원(그림) | S6 · https://likms.assembly.go.kr/bill/bi/billDetailPage.do?billId=ARC_O2S6R0Z9Z0P3V1Z0A5J3R1Y8B6L3L6 |
| 사는 집 23억·24억·25억·30억·40억 | −11.2 · +9.8 · +30.8 · +135.9 · +820.1 | 23억까지 줄다가 24억부터 · 31만원쯤 · 136만원쯤 · 820만원쯤 | S6 · https://www.mofe.go.kr/nw/nes/detailNesDtaView.do?searchBbsId1=MOSFBBS_000000000028&menuNo=4010100&searchNttId1=MOSF_000000000078809 |
| 안 사는 집 30억 | +775.0 | 775만원쯤 | S6 |
| 비거주 문턱 | 14.0억 0.0 · 14.01억 54.0 | 14억 100만원이면 54만원 | S6 · https://likms.assembly.go.kr/bill/bi/billDetailPage.do?billId=ARC_O2S6R0Z9Z0P3V1Z0A5J3R1Y8B6L3L6 |
| 20억 네 갈래 | −75.5 · −22.5 · −7.5 · +140.9 | 그림 −76·−22·−8·+141만원 | S6 |
| 70세 15년·30년 | 38.0 · 38.0 | 똑같이 38만원 | S6 · https://www.mofe.go.kr/nw/nes/detailNesDtaView.do?searchBbsId1=MOSFBBS_000000000028&menuNo=4010100&searchNttId1=MOSF_000000000078809 |
| 공동명의 55세·10년 | 각자 53.8 · 특례 114.0 | 54만원 · 114만원 | S6 · https://www.mofe.go.kr/nw/nes/detailNesDtaView.do?searchBbsId1=MOSFBBS_000000000028&menuNo=4010100&searchNttId1=MOSF_000000000079193 |
| 공동명의 70세·15년 | 각자 53.8 · 특례 38.0 | 54만원 · 38만원 | S6 · https://www.mofe.go.kr/nw/nes/detailNesDtaView.do?searchBbsId1=MOSFBBS_000000000028&menuNo=4010100&searchNttId1=MOSF_000000000079193 |
| 공제·기준 | 거주 14억 · 비거주 12억 · 14억 초과 · 부부 9억/6억 | 같음 | S1 · https://www.mofe.go.kr/nw/nes/detailNesDtaView.do?searchBbsId1=MOSFBBS_000000000028&menuNo=4010100&searchNttId1=MOSF_000000000079193 |
| 비율·세율 | 하한 60→70% · 6~12억 1.0→1.3% | 60%에서 70% · 과세표준 6억~12억 구간 | S1 · S2 |
| 세액공제 | 15년 50% · 2028 한도 600만원 | 15년이면 50% · 600만원 한도 | S2 · https://www.mofe.go.kr/nw/nes/detailNesDtaView.do?searchBbsId1=MOSFBBS_000000000028&menuNo=4010100&searchNttId1=MOSF_000000000078809 |
| 적용 | 2027.1.1 성립분(기준일 2027.6.1) · 올해 현행 | 2027년 6월 1일 기준분 · 올해 12월 고지서는 지금 법 | S2 · S5 |
| 특례 신청 | 9.16~9.30 · 계속 적용 | 9월 16일부터 30일 · 다음 해에도 그대로 | S4 |
| 납부유예 | 65세·10년·10% · 3.1% | 같음 | S1 · S2 |
| 국회 상태 | 소위 회부 09-28 · 처리일·의결일 빈칸(11/3) | 소위원회에 회부된 뒤 아직 처리 전 | S1 |

# 올리기 전 확인
- 날짜: 2026-11-03 (발행 칸 11/4 12:40 — 발행 회차가 11/4에 S1 다시 엶·영상 공개 확인)
- 다시 연 출처: S1 11/3 18:2x 브라우저(의결일자 빈칸·소위 처리일 빈칸) · S2·S3 재경부 보도자료(J-1 11/2 10:29 PD 다시 받음, 공표 자료) · S4·S5 국세청(J-1 11/2 PD 다시 받음)
- 다시 연 주소: https://youtu.be/NNcjTE0L7yg (slots PD 11/3 06:04 11/4 11:30 예약 — 발행 회차가 공개 확인) · https://likms.assembly.go.kr/bill/bi/billDetailPage.do?billId=ARC_O2S6R0Z9Z0P3V1Z0A5J3R1Y8B6L3L6 · https://www.mofe.go.kr/nw/nes/detailNesDtaView.do?searchBbsId1=MOSFBBS_000000000028&menuNo=4010100&searchNttId1=MOSF_000000000078809 · https://www.mofe.go.kr/nw/nes/detailNesDtaView.do?searchBbsId1=MOSFBBS_000000000028&menuNo=4010100&searchNttId1=MOSF_000000000079193 · https://www.nts.go.kr/nts/cm/cntnts/cntntsView.do?mi=40406&cntntsId=238930 · https://www.nts.go.kr/nts/cm/cntnts/cntntsView.do?mi=2356&cntntsId=7738
- 기준일: 2026-11-03 (정부안 2026-09-01 확정·09-03 제출 · 계산은 공시가격 그대로 가정)
- 바뀐 것: 없음 — 국회 처리 상태 그대로(소위 처리 전), 숫자·법 조건 그대로 · 새로 본 것: 소관위 상정 09-28·소위 회부, '세입예산안 부수 법률안 지정 신청'
- 새로 찾은 것: 경쟁 3편(kbthink·뉴시스·머니투데이) 모두 8/3 첫 안(비거주 9억) 기준 — 9/1 정부안 반영 글 못 찾음
- 조사 뒤 공표: data/release_calendar.json 중 이 글에 걸리는 것 없음(확인은 발행 회차)
