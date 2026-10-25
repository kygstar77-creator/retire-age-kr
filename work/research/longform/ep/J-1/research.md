# J-1 자료조사 — 1주택 종부세 정부안, 살면 줄고 안 살면 는다 (2026-10-17 00:0x~ 자료조사 담당 · 사장님 10/16 23:4x '자료조사 공들여서, 전부')
편: 칸 2026-10-24(토) 11:30(순돌이 10/16 11:4x 'J-1은 10/24로') · 대본 script.md v4 · 계산 calc.py → calc_out.txt(라벨만 고침) · **calc2.py → calc2_out.txt(이번에 새로: 부부 공동명의·댓글 질문·정부 사례 불일치 원인)**
'확정' 말 정리(이해 시험 10/15 지적): 9/1 재경부 보도자료 제목이 「2026년 세제개편안」 정부안 확정 — **정부 안에서 확정된 '정부안'이고, 법은 국회가 정한다.** 대본·자막·calc 라벨에서 '확정안'을 모두 '9월 국무회의에서 정한 정부안(국회 통과 전)'으로 바꿨다.

# 원문
| # | 원문 | 이번에 확인한 날짜 | 쪽·표·조문 | 대본에 쓴 것 |
|---|---|---|---|---|
| L1 | 의안 2221046 종합부동산세법 일부개정법률안(정부) — 국회 의안정보시스템 https://likms.assembly.go.kr/bill/bi/billDetailPage.do?billId=ARC_O2S6R0Z9Z0P3V1Z0A5J3R1Y8B6L3L6 | **2026-10-17 00:1x 다시 열어 봄**: 제안일자 2026-09-03 · 소관위 재정경제기획위원회 · **의결일자·의결결과 빈칸 = 처리 전** | 주요내용 가(§7① 1주택 14억 초과)·다(§8① 거주 14억·비거주 12억·부부공동명의 거주 9억·비거주 6억)·마(§9⑧ 거주기간 공제)·아(§20의2 납부유예) | 0장·3장·7장·8장(공동명의) |
| L2 | 재정경제부 「2026년 세제개편안」 보도자료(2026-08-03) https://www.mofe.go.kr/nw/nes/detailNesDtaView.do?searchBbsId1=MOSFBBS_000000000028&menuNo=4010100&searchNttId1=MOSF_000000000078809 — 첨부 상세본(raw/mofe_0803_6) · 문답자료(raw/mofe_0803_8) | 2026-10-17 00:2x 페이지 다시 받음(234KB, 열림) | 상세본 p.60~66(공제·FMV·세율표 3벌·세액공제·상한)·p.91(비거주기간 거주 인정) · 문답 p.41(공동명의: 개별 납부 거주 각 9억/비거주 각 4억, 특례 신청 시 14억/9억)·p.44~45 적용사례 3건 | 1·2·4·5·6장 |
| L3 | 재정경제부 「2026년 세제개편안」 정부안 확정 보도자료(2026-09-01 국무회의) https://www.mofe.go.kr/nw/nes/detailNesDtaView.do?searchBbsId1=MOSFBBS_000000000028&menuNo=4010100&searchNttId1=MOSF_000000000079193 (raw/mofe_0901) | 2026-10-17 00:2x 페이지 다시 받음(214KB) | 3번 표: 비거주 1주택 9억안 → 12억 유지 · **부부 공동명의 비거주 각 4억안 → 각 6억** · 4번: 세부담 상한 200%안 → 150% 유지 · 5행 '국무회의에서 정부안을 최종 확정' | 0·6·8장, '확정' 말 정리 |
| L4 | 국세청 '공동명의 1주택자 특례' 안내 https://www.nts.go.kr/nts/cm/cntnts/cntntsView.do?mi=40406&cntntsId=238930 | 2026-10-17 00:3x 읽음 | '해당연도 9.16.∼9.30.까지 관할세무서장에게 신청' · 다음 연도부터 '별도 신청없이 계속 적용' · 부부가 1주택만 공동 소유, 다른 세대원 무주택 | 8장 그래서·함정 |
| L5 | 국세청 종합부동산세 납부 종합 안내 https://www.nts.go.kr/nts/cm/cntnts/cntntsView.do?mi=2356&cntntsId=7738 | 2026-10-17 00:3x 읽음 | '합산배제신고는 9.16.~9.30., 정기고지 신고는 12.1.~12.15.' · '고지서를 발부받아 납부' | 0장(올해 고지서는 지금 법)·7장 |
| L6 | 현행 종합부동산세법 §8①(1세대 1주택 공제 12억)·§9⑤~⑧(연령·보유 세액공제, 합계 80%)·§10(세부담 상한 150%) — 국가법령정보센터 https://www.law.go.kr/법령/종합부동산세법 | 이번에 조문 화면을 다시 열지 못함(자바스크립트 화면, 확인 안 함) → 상세본 '현행' 칸(L2 p.60~64)으로 대조 | — | 1·4장 '지금 법' 값 |
- 재경부 '비거주 30억 내년 +429만원' 추산(2차): SBS 2026-09-19 보도 https://www.youtube.com/watch?v=MxQmV3al5sQ · 파이낸셜뉴스 2026-09-13 https://www.fnnews.com/news/202609131016000055 · 세계일보 2026-09-13 https://www.segye.com/newsView/20260913504424 — 세 곳 모두 '재정경제부가 국회에 제출한 자료'(부총리 후보자 인사청문 자료)·현행 774.7만원 → 1,203.8만원·만 60세 미만·세액공제와 상한 적용 전. 재경부 원자료는 국회 제출 자료라 공개본을 못 찾음(2026-10-19 17:5x 기준 리뉴얼 담당 다시 찾음, 확인 안 함). 우리 calc 재현값 +429.1(facts V3)과 같음.
- 2026-10-19 17:5x 기준 리뉴얼 담당이 다시 연 것: L1 의안정보(제안일자 2026-09-03·의결일자 빈칸 = 아직 처리 전) · L2·L3 재경부 보도자료 화면(제목 '2026년 세제개편안 발표'·'정부안 확정') · L4·L5 국세청 안내 화면 · L6 law.go.kr 종합부동산세법 화면(조문 글은 raw/law1019 법제처 API 2026-10-19 15:0x) · 헌법 §53 https://www.law.go.kr/법령/대한민국헌법/제53조(raw/law1019/대한민국헌법_53.txt, '15일 이내에 대통령이 공포')

# 질문
실제 질문(댓글 2026-10-17 00:0x raw/yt_comments_1017.json · 자동완성 2026-10-17 00:0x raw/naver_ac_1017.json — 수집 코드 ep/H-3/getq.py·getac.py) → 우리 답
| # | 질문(원문 요지) | 출처 | 우리 답(calc2_out·calc_out) | 장 |
|---|---|---|---|---|
| Q1 | "언제는 공동명의하라고 하더니… 혜택을 다 없애네"(좋아요 445) · "공동명의라고 2주택이라니, 특례신청 언제 하는지" | https://www.youtube.com/watch?v=MxQmV3al5sQ&lc=Ugx-T1sJQ9fvFMIFEvl4AaABAg · https://www.youtube.com/watch?v=SLh90bWU7Tw&lc=UgynuYRg-n0pOYYxRel4AaABAg · 자동완성 '종부세 개편안 공동명의' | 정부안은 공동명의 거주 각 9억 공제를 **그대로** 둔다(L1·L3). 공시 20억·55세·10년 거주 부부: 2028 각자 납부 종부세 53.8 vs 특례 114.0만원 → 각자가 60만원쯤 적음. 70세·15년이면 특례가 15.7만원 적음. 비거주면 각 6억(8월안 4억에서 올림). 특례는 9.16~9.30 신청, 한 번 하면 계속 적용(L4) | 8장 |
| Q2 | "한집에 30년 산 게 죄입니까???"(좋아요 87) | https://www.youtube.com/watch?v=SLh90bWU7Tw&lc=UgyoxJQTkHNS2dO4X2B4AaABAg | 거주공제는 15년 이상이 50%로 끝(상세본 p.64). 공시 20억·70세: 15년과 30년이 2028 종부세 38.0만원으로 같음. 이 사람은 2026 527.9 → 2028 520.4만원(−7.5) | 4장 |
| Q3 | "9억에 산 집이 40억 됐음… 20년 보유 실거주"(좋아요 61) | https://www.youtube.com/watch?v=SLh90bWU7Tw&lc=UgzXljFUVj1wr35OxBx4AaABAg | 시가 40억 ≈ 공시 27~28억(정부 사례 짝 비율 67~70% 가정). 65세 이상·20년 거주면 2028 보유세 +24~31만원, 60세면 +36~47만원 | 4장 |
| Q4 | '종부세 개편안 시행일'·'종부세 개편안 국회'(자동완성) | https://ac.search.naver.com/nx/ac?q=%EC%A2%85%EB%B6%80%EC%84%B8%20%EA%B0%9C%ED%8E%B8 | 2027.1.1 이후 납세의무 성립분(과세기준일 2027.6.1) — 상세본 적용시기. 10/17 현재 소위 회부 뒤 처리 전(L1) | 0·7장 |
| Q5 | '종부세 고지서 발송일'·'종부세 납부기간'(자동완성) | https://ac.search.naver.com/nx/ac?q=%EC%A2%85%EB%B6%80%EC%84%B8%20%EA%B3%A0%EC%A7%80%EC%84%9C | 올해 고지는 지금 법. 국세청 안내 '정기고지 신고 12.1.~12.15.'(L5) — 고지서 발송 날짜는 국세청 원문에서 못 찾음(확인 안 함) | 0·7장 |
| Q6 | '종부세 1주택 공제'·'1주택 2주택 차이'(자동완성) | https://ac.search.naver.com/nx/ac?q=%EC%A2%85%EB%B6%80%EC%84%B8%201%EC%A3%BC%ED%83%9D | 1주택 거주 14억·비거주 12억, 그 밖(2주택 등) 4억 + 5억×거주주택 비중(L1 다) | 1장 자막 |
| Q7 | 경쟁 SBS(2026-09-19) '국세청이 공동명의 부부 8,600명에게 유리한 방식 안내, 특례 취소가 유리한 2,900명' · '9월을 놓쳐도 12월 신고로 고를 수 있다' (목차 대조 10/19) | https://www.youtube.com/watch?v=MxQmV3al5sQ&t=93 | 법 원문 대조(법제처 API 2026-10-19 15:0x): 종부세법 §10의2② 9.16~9.30 신청 · §16③ 12.1~12.15 신고납부 방식은 있음 · 시행령 §5의2④ 신청서·⑤ 다음 해부터 변경 사항은 변경신청 — **특례 '취소'·12월 신고로 특례 선택은 법·시행령 문구에서 못 찾음(확인 안 함)** → 대본은 '그만두는 방법은 국세청 안내에 따로 없어서 세무서에 물어보라' 그대로, 새 말 안 넣음 | 5장(공동명의) |
| Q8 | 경쟁 SBS(2026-09-14) 재경부 '전입 신고 기준 실거주' 답변 보도 · 너굴경제 '공시 14억도 약 70만원'(2026-09-02) | https://www.youtube.com/watch?v=TtLcneZn1wA&t=132 · https://www.youtube.com/watch?v=FyqME4Q_Scg&t=601 | 거주 판정 기준은 시행령 위임 — 보도 원문 확인 안 함 → 대본 그대로('아직 정해진 게 없어요'). 14억은 안 §7① '초과'만 납세의무 → 14억 집 0원(우리 4장·calc) — 경쟁 말이 틀림, 대본 그대로 | 4장 |
| Q9 | 세부담 상한(경쟁 16편 중 5편이 다룸, 목차 대조 10/19) | https://www.youtube.com/watch?v=2ovOIkT8AW0&t=975 | 8월 첫 안 200% → 9/1 정부안 150% 유지(L3 4번 · facts B7) · 이 사례(공시 20억·55세·10년) 2026 618.9 → 2028 596.4만원이라 상한 안 걸림(calc_out) | 2장 |

# 우리만
1. **부부 공동명의 각자 납부 vs 특례**(calc2, 경쟁 0편): 55세·10년 거주 2028 종부세 — 20억 각자 53.8 / 특례 114.0 · 30억 380.2 / 600.8 → 각자가 적음. 70세·15년 거주 — 20억 53.8 / 38.0 · 30억 380.2 / 281.3 → 특례가 적음. 비거주 55세 30억 — 각자 685.4 / 특례 1,239.8.
2. **정부 사례③ 2027 불일치 원인**(calc2 끝): 정부 표 같은 칸의 '세액공제 한도 전 2,141.1'은 산출세액 2,676.4(×80%)를 뜻하고 calc 값과 같다. 여기서 한도 800을 빼고 농특세 20%를 붙이면 2,251.7. 정부 표 종부세 1,942.1을 거꾸로 풀면 산출세액 2,418.4여야 하는데, 그러면 한도 전 금액은 1,934.7이어야 한다 → **같은 칸 두 숫자가 서로 안 맞는다(정부 표 안의 불일치).** 가장 가까운 설명은 12~25억 구간을 현행 1.3%로 둔 계산(1,939.7, 2.4 차)이지만 0.2 안에 안 들어 원인을 그것으로 단정하지 않는다. 같은 사례 2028(3,295.7)은 일치 → 세율표·한도 600은 맞다. 대본은 그 한 칸을 쓰지 않는다(기존과 같음), 자막에 '정부 표 안에서 두 숫자가 안 맞아 뺌'.
3. 15년과 30년 거주가 같다(공제 상한) · 65세 넘고 15년 넘게 살면 연령+거주 합이 80% 한도라 65세와 70세가 같은 값(calc2 Q3: 27억 65세·70세 모두 +24.3).
4. 기존: 비거주 문턱 14억(0 → 54만원) · 거주면 23억대까지 줄어듦 · 9월 정부안으로 정부 사례 다시 계산(30억 비거주 1,780.5 → 1,505.3).

# 왜
- 살면 줄고 안 살면 느는 이유: ① 공제가 거주 14억·비거주 12억(L1 §8①) ② 세액공제가 2028부터 '산 햇수'만 셈(L2 p.64, 안 §9⑧). 정부가 적은 개정이유는 과세대상·기본공제·FMV 모두 '세부담 적정화'(상세본 p.61~63) 한 줄뿐 — 거주로 나눈 이유는 따로 안 적음. 같은 묶음 양도세 장특공 개편 취지엔 '거주 중심으로 세제 혜택을 부여'(문답 p.37).
- 비거주 문턱: 내는 사람 기준(§7① 14억)과 공제(§8① 12억)가 따로 정해져서(L1).
- 공제가 2억 늘어도 덜 주는 이유: 공정시장가액비율 60 → 70%(개정이유 '세부담적정화', 상세본 p.63), 세율 6~12억 1.0 → 1.3%(문답 p.43 '세부담 정상화를 위해 6~12억 구간 세율 인상').
- 금액 한도 600만원: 정부 설명 '한도 없는 세액공제로 주택가격이 높을수록 큰 혜택 → 과세형평'(문답 p.44).
- 공동명의 각자 납부가 유리한 경우가 있는 이유: 각자 9억씩 18억을 빼 주는데(L1), 특례는 14억 + 세액공제. 세액공제(나이·햇수)가 크면 특례가, 작으면 각자가 유리해진다 — 산수로 설명.
- '확정'으로 들린 이유: 9/1 보도자료 제목이 '정부안 확정'(L3 21행). 정부 안의 절차가 끝났다는 뜻.

# 그래서
투자·이사 권유 아님. 제도상 할 일·기한·한도만.
1. 올해(2026) 고지서는 지금 법 — 12월 고지분 그대로(L5). 바뀐 계산은 정부안이 통과되면 2027년 6월 1일 기준분부터.
2. 부부 공동명의 1주택: 특례(한 사람 1주택으로 계산)는 **매년 9.16~9.30 관할 세무서 신청**, 한 번 하면 다음 해부터 계속 적용(L4) → 정부안이 통과되면 다음 신청 기간 전에 각자 납부와 다시 견줘 볼 것(나이·산 햇수에 따라 갈림, calc2).
3. 납부유예: 정부안대로면 만 65세 이상·10년 이상 거주·보유세가 직전 소득의 10% 이상이면 신청 가능, 이자 연 3.1%(L2 p.66~67) — '27.1.1 이후 신청분.
4. 전근·진학·요양으로 떠나 있으면 최대 3년 산 것으로 쳐 줌(상세본 p.91) — 세액공제 계산용, 기본공제 14억 판정과는 별개(시행령, 확인 안 함).
5. 국회 진행은 의안정보시스템 의안번호 2221046으로 직접 확인(L1).

# 누구라면
- 그 집에 사는 1주택, 공시 23억 이하: 2028 보유세가 오히려 조금 줄어듦(55세·10년).
- 그 집에 살지 않는 1주택: 14억 넘으면 54만원부터 바로 생김, 20억이면 +140만원쯤.
- 부부 공동명의: 나이·산 햇수가 짧으면 각자 납부, 길면 특례가 적게 나옴(calc2).
- 고령·장기거주·고가(공시 40억, 70세·15년): 금액 한도 600만원에 걸려 보유세가 두 배 넘게.
- 15년 넘게 산 사람: 더 오래 살아도 할인은 같음(Q2).

# 함정
1. 비거주 문턱 — 공시 14억을 조금만 넘어도 12억 넘는 몫 전체에 세금(0 → 54만원).
2. 공동명의 특례는 한 번 신청하면 계속 적용 — 규칙이 바뀌면 유리했던 쪽이 불리해질 수 있다(L4 '별도 신청없이 계속 적용').
3. 정부 8월 예시표는 첫 안(비거주 9억·상한 200%) 기준 — 그대로 보면 실제 정부안보다 크게 보인다.
4. '확정'이라는 보도자료 제목 — 법은 아직 국회 소위 단계.
5. 세액공제 금액 한도 — 공제율 80%를 다 받아도 2028년부터 600만원까지만.

# 예외
- 거주·비거주 판정 기준(주민등록·과세기준일 등)은 시행령 위임 — 확인 안 함.
- 재산세 공정시장가액비율 45%는 가정(2027 이후 시행령).
- 시가 40억 → 공시 27~28억은 정부 사례 짝 비율로 잡은 가정(실제 공시가격은 고지서로).
- 공동명의 계산은 반반 지분·두 사람 다른 주택 없음·세부담 상한 안 걸림 가정.
- 정부 사례③ 2027 1칸 불일치(위 우리만 2).
- 일시적 2주택·상속주택 등 특례주택은 이번 편 밖(문답 p.41).

# 한계
기준 리뉴얼 10/19(registry A-01) — 확인 못 한 것·원문에 이유 없는 것·자료 기준일의 한계.
- 자료 기준일: 법안은 2026-09-03 제출 정부안(의안 2221046), 2026-10-19 현재 소위원회 단계 — 국회에서 숫자가 바뀔 수 있고, 공개 전날(10/23) 의안정보를 다시 본다. 재산세는 2027년 뒤 공정시장가액비율이 시행령으로 매년 정해져 calc는 45%로 가정했다. 공시가격은 해마다 바뀌는데 계산은 '공시가격 그대로'로 놓았다.
- 원문에 이유 없는 것: 사는 집과 안 사는 집을 왜 나눴는지(정부 자료엔 '세부담 적정화' 한 줄뿐) · 공제 2억이 늘었는데 비율·세율도 같이 올린 까닭의 자세한 설명.
- 확인 못 한 것: 거주 판정 기준과 산 햇수를 언제부터 세는지(시행령 위임, 아직 없음) · 떠나 있는 동안(전근 등) 14억 공제를 주는지 · 공동명의 특례를 '그만두는' 절차(국세청 안내에 없음) · 재경부 +429만원 원자료(보도로만, 세 곳) · 국세청 '8,600명 안내'(SBS 보도, 원문 못 찾음) · 2027년 이후 재산세 비율.
- 2차뿐인 것: 재경부 +429만원 한 줄 — 보도 세 곳(SBS·파이낸셜뉴스·세계일보)과 우리 재현 계산으로 맞춤.
- 가정 한계: 시가 40억 → 공시 28억 안팎은 정부 예시 짝 비율로 잡은 가정 · 공동명의는 반반 지분·다른 집 없음 · 사례 인물(55세·10년 등)은 가상 · 세부담 상한 걸리는지는 사례마다 다름.

# 대조
| 원문(파일·줄) | 원값 | 대본 말 | 대본 자막 | 출처 |
|---|---|---|---|---|
| calc_out 55세·10년 거주 20억 | 618.9 → 596.4(−22.5) | 오히려 조금 줄어요 | −22.5 | https://likms.assembly.go.kr/bill/bi/billDetailPage.do?billId=ARC_O2S6R0Z9Z0P3V1Z0A5J3R1Y8B6L3L6 · https://www.mofe.go.kr/nw/nes/detailNesDtaView.do?searchBbsId1=MOSFBBS_000000000028&menuNo=4010100&searchNttId1=MOSF_000000000078809 |
| calc_out 55세·거주 0 20억 | 618.9 → 759.8(+140.9) | 140만원쯤 | +140.9 | https://likms.assembly.go.kr/bill/bi/billDetailPage.do?billId=ARC_O2S6R0Z9Z0P3V1Z0A5J3R1Y8B6L3L6 · https://www.mofe.go.kr/nw/nes/detailNesDtaView.do?searchBbsId1=MOSFBBS_000000000028&menuNo=4010100&searchNttId1=MOSF_000000000078809 |
| calc_out 거주 23억·24억 | −11.2 · +9.8 | 23억과 24억 사이 | 원값 | https://likms.assembly.go.kr/bill/bi/billDetailPage.do?billId=ARC_O2S6R0Z9Z0P3V1Z0A5J3R1Y8B6L3L6 · https://www.mofe.go.kr/nw/nes/detailNesDtaView.do?searchBbsId1=MOSFBBS_000000000028&menuNo=4010100&searchNttId1=MOSF_000000000078809 |
| calc_out 비거주 문턱 | 14억 0 · 14.01억 54.0 | 50만원 넘게 | 54.0 | https://likms.assembly.go.kr/bill/bi/billDetailPage.do?billId=ARC_O2S6R0Z9Z0P3V1Z0A5J3R1Y8B6L3L6 · https://www.mofe.go.kr/nw/nes/detailNesDtaView.do?searchBbsId1=MOSFBBS_000000000028&menuNo=4010100&searchNttId1=MOSF_000000000078809 |
| calc_out 70세·15년 40억 | 1,348.0 → 2,783.3 | 두 배 넘게 | +1,435.3 | https://likms.assembly.go.kr/bill/bi/billDetailPage.do?billId=ARC_O2S6R0Z9Z0P3V1Z0A5J3R1Y8B6L3L6 · https://www.mofe.go.kr/nw/nes/detailNesDtaView.do?searchBbsId1=MOSFBBS_000000000028&menuNo=4010100&searchNttId1=MOSF_000000000078809 |
| calc_out 사례② 9월 정부안 | 1,780.5 → 1,505.3 · 2026 916.3 | 270만원 넘게 적게 · 590만원쯤 늘어 | 원값 | https://likms.assembly.go.kr/bill/bi/billDetailPage.do?billId=ARC_O2S6R0Z9Z0P3V1Z0A5J3R1Y8B6L3L6 · https://www.mofe.go.kr/nw/nes/detailNesDtaView.do?searchBbsId1=MOSFBBS_000000000028&menuNo=4010100&searchNttId1=MOSF_000000000078809 |
| calc2 공동명의 55세 20억 2028 | 각자 53.8 · 특례 114.0 | 60만원쯤 적게 | 원값 | https://likms.assembly.go.kr/bill/bi/billDetailPage.do?billId=ARC_O2S6R0Z9Z0P3V1Z0A5J3R1Y8B6L3L6 · https://www.mofe.go.kr/nw/nes/detailNesDtaView.do?searchBbsId1=MOSFBBS_000000000028&menuNo=4010100&searchNttId1=MOSF_000000000078809 |
| calc2 공동명의 70세 20억 2028 | 각자 53.8 · 특례 38.0 | 15만원쯤 적게 | 원값 | https://likms.assembly.go.kr/bill/bi/billDetailPage.do?billId=ARC_O2S6R0Z9Z0P3V1Z0A5J3R1Y8B6L3L6 · https://www.mofe.go.kr/nw/nes/detailNesDtaView.do?searchBbsId1=MOSFBBS_000000000028&menuNo=4010100&searchNttId1=MOSF_000000000078809 |
| calc2 공동명의 55세 30억 2028 | 각자 380.2 · 특례 600.8 | 220만원쯤 | 원값 | https://likms.assembly.go.kr/bill/bi/billDetailPage.do?billId=ARC_O2S6R0Z9Z0P3V1Z0A5J3R1Y8B6L3L6 · https://www.mofe.go.kr/nw/nes/detailNesDtaView.do?searchBbsId1=MOSFBBS_000000000028&menuNo=4010100&searchNttId1=MOSF_000000000078809 |
| calc2 Q2 15년·30년 | 둘 다 38.0 | 똑같아요 | 원값 | https://likms.assembly.go.kr/bill/bi/billDetailPage.do?billId=ARC_O2S6R0Z9Z0P3V1Z0A5J3R1Y8B6L3L6 · https://www.mofe.go.kr/nw/nes/detailNesDtaView.do?searchBbsId1=MOSFBBS_000000000028&menuNo=4010100&searchNttId1=MOSF_000000000078809 |
| calc2 Q3 공시 27·28억 65세+ 20년 | +24.3 · +31.3 | 30만원 안팎 | 원값 | https://likms.assembly.go.kr/bill/bi/billDetailPage.do?billId=ARC_O2S6R0Z9Z0P3V1Z0A5J3R1Y8B6L3L6 · https://www.mofe.go.kr/nw/nes/detailNesDtaView.do?searchBbsId1=MOSFBBS_000000000028&menuNo=4010100&searchNttId1=MOSF_000000000078809 |
| L1 likms 2026-10-17 | 의결일자 빈칸 | 아직 소위원회 단계 | 10.17 현재 처리 전 | https://likms.assembly.go.kr/bill/bi/billDetailPage.do?billId=ARC_O2S6R0Z9Z0P3V1Z0A5J3R1Y8B6L3L6 |
| L3 공동명의 비거주 | 각 4억안 → 각 6억 | 6억씩 | 원값 | https://www.mofe.go.kr/nw/nes/detailNesDtaView.do?searchBbsId1=MOSFBBS_000000000028&menuNo=4010100&searchNttId1=MOSF_000000000079193 |
| L4 국세청 | 9.16~9.30 · 계속 적용 | 9월 16일부터 30일까지 · 다음 해에도 그대로 | 원값 | https://www.nts.go.kr/nts/cm/cntnts/cntntsView.do?mi=40406&cntntsId=238930 |
| L2 상세본 p.66 납부유예 | 65세·10년·10% · 이자 3.1% | 원값 그대로 말 | 원값 | https://www.mofe.go.kr/nw/nes/detailNesDtaView.do?searchBbsId1=MOSFBBS_000000000028&menuNo=4010100&searchNttId1=MOSF_000000000078809 |
| facts V3 재경부 추산(2차) | 비거주 공시 30억 2027 +429.1만원(774.7 → 1,203.8) · 70세·10년 보유 +326.6 | 430만원 정도 · 330만원 정도 | 원값 | 2차 https://www.youtube.com/watch?v=MxQmV3al5sQ · https://www.fnnews.com/news/202609131016000055 · https://www.segye.com/newsView/20260913504424 |
| facts B3 공제 | 거주 12억 → 14억 · 비거주 12억 · 부부 거주 각 9억·비거주 각 6억 | 12억에서 14억으로 · 9억씩 · 6억으로 | 원값 | https://likms.assembly.go.kr/bill/bi/billDetailPage.do?billId=ARC_O2S6R0Z9Z0P3V1Z0A5J3R1Y8B6L3L6 · https://www.mofe.go.kr/nw/nes/detailNesDtaView.do?searchBbsId1=MOSFBBS_000000000028&menuNo=4010100&searchNttId1=MOSF_000000000079193 |
| facts B2 납세의무 | 1주택 14억 초과(거주 구분 없음) | 14억까지는 안 나옵니다 | 원값 | https://likms.assembly.go.kr/bill/bi/billDetailPage.do?billId=ARC_O2S6R0Z9Z0P3V1Z0A5J3R1Y8B6L3L6 |
| facts B4 공정시장가액비율 | 60% → 70% | 60% · 70% | 원값 | https://likms.assembly.go.kr/bill/bi/billDetailPage.do?billId=ARC_O2S6R0Z9Z0P3V1Z0A5J3R1Y8B6L3L6 · https://www.mofe.go.kr/nw/nes/detailNesDtaView.do?searchBbsId1=MOSFBBS_000000000028&menuNo=4010100&searchNttId1=MOSF_000000000078809 |
| facts B5 세율 | 과표 6~12억 1.0 → 1.3% | 6억을 넘는 구간부터 | 원값 | https://www.mofe.go.kr/nw/nes/detailNesDtaView.do?searchBbsId1=MOSFBBS_000000000028&menuNo=4010100&searchNttId1=MOSF_000000000078809 |
| facts B6 세액공제 | 연령 60세 20%·65세 30%·70세 40% · 거주 5년 20%·10년 40%·15년 50% · 합계 80% · 2028 한도 600만원 | 예순에 20% · 30% · 40% · 15년 50% · 80% · 600만원 | 5년 20%·10년 40% | https://www.mofe.go.kr/nw/nes/detailNesDtaView.do?searchBbsId1=MOSFBBS_000000000028&menuNo=4010100&searchNttId1=MOSF_000000000078809 · https://www.law.go.kr/법령/종합부동산세법 |
| facts B7 세부담 상한 | 150% 유지(200%안 철회) | 1.5배 | 원값 | https://www.mofe.go.kr/nw/nes/detailNesDtaView.do?searchBbsId1=MOSFBBS_000000000028&menuNo=4010100&searchNttId1=MOSF_000000000079193 |
| facts B8 적용 시기 | 2027.1.1 이후 납세의무 성립분(기준일 2027.6.1) | 2027년 12월 고지서 · 내년 고지서부터 | 원값 | https://www.mofe.go.kr/nw/nes/detailNesDtaView.do?searchBbsId1=MOSFBBS_000000000028&menuNo=4010100&searchNttId1=MOSF_000000000078809 |
| facts B9 납부유예 | 총급여 7천 → 8천만원 · 65세·10년·10% · 이자 연 3.1% | 7천만원 · 8천만원 · 연 3.1% | 원값 | https://www.mofe.go.kr/nw/nes/detailNesDtaView.do?searchBbsId1=MOSFBBS_000000000028&menuNo=4010100&searchNttId1=MOSF_000000000078809 |
| facts B10 비거주기간 인정 | 최대 3년 · 1년 이상 요양 | 1년 넘게 · 3년까지 | 원값 | https://www.mofe.go.kr/nw/nes/detailNesDtaView.do?searchBbsId1=MOSFBBS_000000000028&menuNo=4010100&searchNttId1=MOSF_000000000078809 |
| facts L7 현행법 | 과세기준일 6월 1일 · 1주택 12억 · 부부 각 9억 | 6월 1일 · 12억 · 9억 | 원값 | https://www.law.go.kr/법령/종합부동산세법 |
| facts C7 고지서 순서(calc3) | 8억 × 60% = 4.8억 · 산출 276.0 · 재산세 겹친 부분 86.4 · 공제 40% · 농특세 20% · 종부세 136.5 · 보유세 618.9 | 8억 · 5억 조금 안 · 276만원 · 86만원 · 40% · 20% · 136만원 · 619만원 | 원값 | https://www.law.go.kr/법령/종합부동산세법 · https://www.mofe.go.kr/nw/nes/detailNesDtaView.do?searchBbsId1=MOSFBBS_000000000028&menuNo=4010100&searchNttId1=MOSF_000000000078809 |
| facts C9 안 사는 20억 내년 | 618.9 → 704.4(+85.4) | 85만원 정도 | 원값 | https://likms.assembly.go.kr/bill/bi/billDetailPage.do?billId=ARC_O2S6R0Z9Z0P3V1Z0A5J3R1Y8B6L3L6 · https://www.mofe.go.kr/nw/nes/detailNesDtaView.do?searchBbsId1=MOSFBBS_000000000028&menuNo=4010100&searchNttId1=MOSF_000000000078809 |
| facts C8 공동명의 비거주 문턱(calc3) | 18억 0 · 18.02억 161.8 · 거주 0.5 | 160만원 정도 · 거의 0원 | 원값 | https://likms.assembly.go.kr/bill/bi/billDetailPage.do?billId=ARC_O2S6R0Z9Z0P3V1Z0A5J3R1Y8B6L3L6 · https://www.mofe.go.kr/nw/nes/detailNesDtaView.do?searchBbsId1=MOSFBBS_000000000028&menuNo=4010100&searchNttId1=MOSF_000000000079193 |
| L5 국세청·종부세법 §16①② | 고지 납부 12.1~12.15 · 고지서 납부기간 5일 전까지 발급 | 12월 1일부터 보름 · 닷새 전 | 원값 | https://www.nts.go.kr/nts/cm/cntnts/cntntsView.do?mi=2356&cntntsId=7738 · https://www.law.go.kr/법령/종합부동산세법 |
| raw/law1019 헌법 §53 | 15일 이내 공포 | 15일 안에 | 원값 | https://www.law.go.kr/법령/대한민국헌법/제53조 |

# 올리기 전 확인
2026-10-23 00:46 firemap-youtube-loop — 공개 칸 2026-10-24(토) 11:30, 대조 칸 출처 10곳 전부 다시 받음(curl, 응답 200)
- https://likms.assembly.go.kr/bill/bi/billDetailPage.do?billId=ARC_O2S6R0Z9Z0P3V1Z0A5J3R1Y8B6L3L6 — [2221046] 소관위 재정경제기획위원회 · 제안일자 2026-09-03 · **의결일자·의결결과 빈칸 = 10/23 지금도 처리 전**(화면 자막 '10.19 현재 처리 전'은 그대로 맞음)
- https://www.mofe.go.kr/nw/nes/detailNesDtaView.do?searchBbsId1=MOSFBBS_000000000028&menuNo=4010100&searchNttId1=MOSF_000000000078809 — 제목 '2026년 세제개편안 발표' 그대로(첨부 상세본·문답 raw/mofe_0803_* 값은 공표 자료라 안 바뀜)
- https://www.mofe.go.kr/nw/nes/detailNesDtaView.do?searchBbsId1=MOSFBBS_000000000028&menuNo=4010100&searchNttId1=MOSF_000000000079193 — 제목 '2026년 세제개편안 정부안 확정' 그대로
- https://www.nts.go.kr/nts/cm/cntnts/cntntsView.do?mi=40406&cntntsId=238930 — '해당연도 9.16.∼9.30.까지 관할세무서장에게 신청' · '다음 연도부터는 … 별도 신청없이 계속 적용됨' · 다른 세대원 무주택 — 그대로
- https://www.nts.go.kr/nts/cm/cntnts/cntntsView.do?mi=2356&cntntsId=7738 — '합산배제신고는 9.16. ~ 9.30., 정기고지 신고는 12.1. ~ 12.15.' · '고지서를 발부받아 납부' — 그대로
- https://www.fnnews.com/news/202609131016000055 — 현행 774만7000원 → 1203만8000원, 429만1000원 많다 — 그대로
- https://www.segye.com/newsView/20260913504424 — 774만7000원 → 1203만8000원, 429만1000원 — 그대로
- https://www.youtube.com/watch?v=MxQmV3al5sQ — 영상 열림(SBS 9/19 보도, 삭제 안 됨)
- https://www.law.go.kr/법령/종합부동산세법 · https://www.law.go.kr/법령/대한민국헌법/제53조 — 화면은 자바스크립트 껍데기만 받힘(본문 확인 안 함). 조문 값은 raw/law1019(10/19 법제처 API) 그대로 씀 — 개정안이 의결 전이라 현행 종부세법이 바뀔 길이 없음(의안 2221046 의결일자 빈칸)
기준일: 정부안 = 2026-09-01 국무회의 확정·2026-09-03 국회 제출(의안 2221046) · 현행법 = 종합부동산세법(2026-10-19 조문) · 국회 처리 상태 = 2026-10-23 의안정보 화면 · 재경부 추산 = 2026-09-13 보도(국회 제출 자료) · 계산(calc·calc2·calc3) = 공시가격 그대로 가정, 기준일 영향 없음
바뀐 것: 없음 — 숫자·법 조건·국회 상태 모두 그대로, 다시 녹음·렌더할 줄 0. 설명란 출처의 의안정보·국세청 '2026-10-19 확인'만 '2026-10-23 확인'으로 고침(meta.json desc·desc_tpl, 화면 아님). 조사 뒤 공표 중 이 편에 걸리는 것 없음(10/22 금통위는 종부세·납부유예 이자와 무관 — 납부유예 이자 3.1%는 세제개편안 상세본 값)
새로 찾은 것: 10/17~10/23 '종부세 1주택 거주 비거주 조세소위' 웹 검색 — 10월 조세소위 처리·수정 보도 못 찾음(검색에 나온 건 8/3 첫 안 기사뿐: 이투데이 https://www.etoday.co.kr/news/view/2610286 · 헤럴드 https://biz.heraldcorp.com/article/10829442 — 첫 안의 비거주 9억·상한 200%는 9/1 정부안에서 철회, 대본은 이미 9/1 안 기준). 새 댓글 질문 없음(공개 전)

2026-10-25 22:20 firemap-video-producer — 공개 칸 바뀜 2026-10-26(월) 11:30(정지로 10/24 칸 빔, 회의 10/25), 대조 칸 출처 다시 받음(curl, 응답 200 8곳)
- https://likms.assembly.go.kr/bill/bi/billDetailPage.do?billId=ARC_O2S6R0Z9Z0P3V1Z0A5J3R1Y8B6L3L6 — [2221046] 소관위 재정경제기획위원회 · 제안일자 2026-09-03 · **의결일자·의결결과 빈칸 = 10/25 지금도 처리 전**
- https://www.mofe.go.kr/nw/nes/detailNesDtaView.do?searchBbsId1=MOSFBBS_000000000028&menuNo=4010100&searchNttId1=MOSF_000000000078809 — '세제개편안' 그대로
- https://www.mofe.go.kr/nw/nes/detailNesDtaView.do?searchBbsId1=MOSFBBS_000000000028&menuNo=4010100&searchNttId1=MOSF_000000000079193 — '정부안 확정' 그대로
- https://www.nts.go.kr/nts/cm/cntnts/cntntsView.do?mi=40406&cntntsId=238930 — '9.16' 신청·'별도 신청' 문구 그대로
- https://www.nts.go.kr/nts/cm/cntnts/cntntsView.do?mi=2356&cntntsId=7738 — '합산배제신고'·'12.1' 그대로
- https://www.fnnews.com/news/202609131016000055 — 774만7000·1203만8000·429만1000 그대로
- https://www.segye.com/newsView/20260913504424 — 774만7000·429만1000 그대로
- https://www.youtube.com/watch?v=MxQmV3al5sQ — 영상 열림
- law.go.kr 두 곳은 10/23과 같이 본문 확인 안 함 — 의안 의결 전이라 현행법 바뀔 길 없음
기준일: 정부안 = 2026-09-01 국무회의 확정·2026-09-03 국회 제출(의안 2221046) · 현행법 = 종합부동산세법(2026-10-19 조문) · 국회 처리 상태 = 2026-10-25 의안정보 화면 · 재경부 추산 = 2026-09-13 보도 · 계산 = 공시가격 그대로 가정
바뀐 것: 없음 — 숫자·법 조건·국회 상태 그대로, 다시 녹음·렌더할 줄 0. 10/23~10/25 사이 data/release_calendar.json 공표 중 이 편에 걸리는 것 없음
새로 찾은 것: 웹 검색 '종부세 개정안 조세소위 1주택 거주 2026년 10월' — 10월 조세소위 처리·수정 보도 못 찾음(나온 것은 8~9월 기사: 머니투데이 https://mt.co.kr/politics/2026/08/30/2026083009475491114 · 경북매일 https://kbmaeil.com/article/20260901500597, 대본은 9/1 안 기준이라 그대로). 새 댓글 질문 없음(공개 전)
