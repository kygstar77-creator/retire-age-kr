# semietf1116 자료조사 (카페 2026-11-16 12:40 칸 — firemap-write 11/15 21:2x) — 주식·ETF 축: 국내 반도체 ETF 9개, 담은 종목과 기간별 하락 순서

## 검증
- 수요: work/kwvol.py 11/15 21:2x — 반도체ETF 14,650(PC 3,550·모바일 11,100) · 같은 때 TDF환헤지 10(접음)
- 겹침: 우리 제목 342개 중 반도체 2편([ETF 시황] 레버리지 하루 등락) · SOXL(미국)·단일종목 레버리지 — 국내 반도체 ETF 담은 종목 비교 0편 · 어제 tdf1115와 자료(FunETF)는 같지만 대상·각도 다름(TDF 빈티지 ↔ 반도체 기간 뒤집힘)
- 경쟁에서 터진 증거: toprank '반도체ETF' 블로그 상위 8편 중 6편이 11/9~11/15 작성(raw/toprank.txt) — 지금 화제 · 8편 모두 상품 한두 개·한 기간, 9개를 두 기간으로 맞댄 글 0편

## 원문
- S1 FunETF 상품 정보(운용사 공시 모음, 2차) 9개 — 기간별 수익률(NAV, 분배금 재투자) 26.11.13 기준·실부담비율·기초지수 — 2026-11-15 확인(raw/funetf_*.txt, parse_out.txt): https://www.funetf.co.kr/product/etf/view/KR7396500001 · https://www.funetf.co.kr/product/etf/view/KR7091160002 · https://www.funetf.co.kr/product/etf/view/KR70167A0001 · https://www.funetf.co.kr/product/etf/view/KR7395160005 · https://www.funetf.co.kr/product/etf/view/KR7395270002 · https://www.funetf.co.kr/product/etf/view/KR7091230003 · https://www.funetf.co.kr/product/etf/view/KR7455850008 · https://www.funetf.co.kr/product/etf/view/KR7469150007 · https://www.funetf.co.kr/product/etf/view/KR7471990002
- S2 같은 페이지 '구성종목(PDF)' 탭 — 종목별 비중(%)·종가 26.11.13 — 2026-11-15 확인(raw/pdf_*.txt, pdf_out.txt)
- S3 야후 파이낸스 일별 종가(2차, S1 대조) — 2026-11-15 확인(raw/yahoo_*.json): https://query1.finance.yahoo.com/v8/finance/chart/396500.KS · https://query1.finance.yahoo.com/v8/finance/chart/091160.KS · https://query1.finance.yahoo.com/v8/finance/chart/455850.KS · https://query1.finance.yahoo.com/v8/finance/chart/395160.KS
- S4 네이버페이 증권 ETF 목록(2차, 대상 고르기 — 이름 '반도체' 67개, 순자산 순) — 2026-11-15 확인(raw/naver_etflist.json): https://finance.naver.com/api/sise/etfItemList.nhn
- S5 네이버페이 증권 ETF 지표(2차, 참고 — 1·3개월 값이 S1과 기준일이 달라 글에 안 씀) — https://m.stock.naver.com/api/stock/396500/integration

## 경쟁
(bench.md 6편) 1위는 소부장 ETF 한 주 급등과 담은 범위 차이, 2위는 SOL AI반도체TOP2플러스 하나의 구성·최근 수익률, 3·4·6위는 '지금 담을 이유'·소부장 대장주 소개(권유 성격), 5위는 DRAM·HBM ETF 둘 비교. 빠뜨린 것: 국내 반도체 ETF 여럿을 같은 날 공시로 맞댄 것, 기간을 바꾸면 순서가 뒤집히는 것, 두 회사 비중으로 묶은 비교

## 질문
1. 이름이 비슷한 반도체 ETF끼리 뭐가 다른가? — https://blog.naver.com/seulo_ol/224477801633 ('이름이 비슷해도 투자 범위는 달라요') → 답: c04(두 회사 절반쯤 / 37% / 0% 세 갈래)
2. 반도체 ETF는 왜 이렇게 빠졌나, 다 같이 빠졌나? — https://blog.naver.com/ssibar1188/224477760091 ('반도체 ETF 다들 탈출각 재는데') → 답: c01·c02(석 달 -10.3~-28.3%, 한 달 -17.3~-30.2%, 기간마다 순서 다름)
3. 두 ETF를 함께 사면 무엇이 달라지나(겹치는 종목)? — https://blog.naver.com/minpro38/224473630384 ('SOL과 PLUS를 함께 사면 무엇이 달라질까?') → 답: c04(TOP2류 5개는 두 회사가 절반쯤으로 겹침, 구성종목(PDF) 탭으로 확인)
4. SOL AI반도체TOP2플러스는 무엇을 담았나? — https://blog.naver.com/dja974/224470868856 ('어르신이 사기 전에 알아둘 구성종목') → 답: 그림 02(삼성전자 27.9%·SK하이닉스 26.3%)

## 왜
- 석 달에 TOP2류가 더 빠진 이유: 삼성전자·SK하이닉스를 절반쯤 담아(S2) 두 회사 흐름을 크게 받음 — 같은 날 9개에서 비중 묶음과 하락 순서가 같음
- 한 달에 거꾸로인 이유: 그 앞 두 달(8/13~10/13)을 (1+3개월)/(1+1개월)-1로 직접 계산하면 소부장 +21.3·+24.4%, TOP2류 -1.3~-11.4% — 소부장은 오른 뒤 되돌림, TOP2류는 계속 내림
- 두 회사·소부장 주가가 왜 그렇게 움직였는지: 원문(공시)에 없음(한계) — 글에 '공시에 나오지 않는다'
- TIGER TOP10과 HANARO 1년 차이(43.77 vs 109.83%): 원문에 이유 없음(한계)

## 그래서
- 내 반도체 ETF가 무엇을 담았는지 FunETF·운용사 상품 페이지 '구성종목(PDF)' 탭에서 기준일과 함께 확인(S2)
- 수익률은 한 기간만 보지 말고 1개월·3개월을 같이 보기(S1 기간별 수익률 표에 나란히 있음)

## 누구라면
- TOP2류(삼성전자·SK하이닉스 절반쯤)를 가진 사람: 석 달 -22.1~-28.3%, 한 달 -17.3~-21.2%
- KRX 반도체 지수형(KODEX·TIGER 반도체)을 가진 사람: 석 달 -20.5·-20.9%, 한 달 -26.0·-26.1%
- 소부장형을 가진 사람: 석 달 -10.3·-15.3%, 한 달 -27.9·-30.2%

## 함정
- 석 달 성적만 보면 소부장이 덜 빠진 것처럼 보이지만 최근 한 달은 가장 많이 빠짐
- 두 회사 비중이 비슷해도(53.2 vs 52.7%) 1년 수익률은 43.8 vs 109.8%로 다름 — 비중 하나로 성적이 정해지지 않음
- 구성종목 비중은 매일 바뀜 — 기준일 확인

## 우리만
- 국내 반도체 ETF 9개 석 달·한 달 순서 뒤집힘을 담은 종목 비중으로 묶어 맞댐 · 앞 두 달 수익률(+24.4% ↔ -11.4%)을 직접 계산(calc_out.txt) · 1천만원이면 석 달 뒤 약 897만원 vs 718만원 — 경쟁 8편 0편

## 예외
- 9개만 봄(국내 반도체 주식형, 레버리지·커버드콜·해외형·채권혼합 뺌) — SOL 반도체전공정·후공정 등 순자산 작은 상품은 셈에 없음
- 석 달·한 달은 11/13에서 거꾸로 센 한 구간 — 다른 날 기준이면 순서가 달라질 수 있음
- SOL AI반도체TOP2플러스는 1년이 안 돼 1년 수익률 없음

## 한계
- 두 회사·소부장 주가가 왜 그렇게 움직였는지, TIGER TOP10과 HANARO 1년 차이 원인은 원문(공시)에 없음
- 구성종목 비중은 11/13 화면 값 — 석 달 동안 비중이 바뀐 것은 확인 안 함(지수 정기변경 원문 못 봄)
- FunETF는 운용사 공시를 모은 2차 — 운용사 원 페이지는 이번에 따로 안 열었고 야후 종가(S3)로 대조
- 석 달·한 달의 시작일(8/13·10/13)은 FunETF 1·3개월 구간을 11/13에서 거꾸로 센 값 — 야후 종가 8/13·10/13→11/13 계산이 FunETF 종가 수익률과 0.1%p 안(396500 -17.46·-22.51)이라 같은 구간으로 봄
- 네이버 지표(S5)의 1·3개월 값은 S1과 기준일이 달라 숫자가 다름(396500 3개월 -16.97 vs -22.61) — 글은 S1만 씀

## 대조
| 글 값 | 원문 값 | 출처 |
|---|---|---|
| 국내 반도체 ETF 9개(순자산 순, 레버리지·커버드콜 뺌) | 이름 '반도체' 67개 중 국내 주식형(etfTabCode 2) 순자산 상위 9개(레버리지·커버드콜 제외) | S4 https://finance.naver.com/api/sise/etfItemList.nhn |
| KODEX AI반도체TOP2플러스 석 달 -28.3%, 한 달 -19.0% | NAV 3개월 -28.25 · 1개월 -19.02 | S1 https://www.funetf.co.kr/product/etf/view/KR7395160005 · S3 https://query1.finance.yahoo.com/v8/finance/chart/395160.KS (-28.09·-19.13) |
| 두 회사 절반 정도(49.9~54.2%) 5개 석 달 -22.1~-28.3% | -22.09(ACE)~-28.25 | S1 https://www.funetf.co.kr/product/etf/view/KR7469150007 · https://www.funetf.co.kr/product/etf/view/KR7395160005 |
| KODEX·TIGER 반도체 37%, 석 달 -20.5·-20.9%, 한 달 -26.0·-26.1% | 삼성 19.7+하이닉스 17.3 · -20.52·-20.93 · -26.01·-26.05 | S1·S2 https://www.funetf.co.kr/product/etf/view/KR7091160002 · https://www.funetf.co.kr/product/etf/view/KR7091230003 · S3 https://query1.finance.yahoo.com/v8/finance/chart/091160.KS |
| 소부장 석 달 -15.3·-10.3%, 한 달 -30.2·-27.9% | -15.34·-10.33 · -30.18·-27.91 | S1 https://www.funetf.co.kr/product/etf/view/KR7455850008 · https://www.funetf.co.kr/product/etf/view/KR7471990002 · S3 https://query1.finance.yahoo.com/v8/finance/chart/455850.KS |
| TIGER 반도체TOP10 한 달 -17.3% | -17.34 | S1 https://www.funetf.co.kr/product/etf/view/KR7396500001 · S3 https://query1.finance.yahoo.com/v8/finance/chart/396500.KS (-17.46 종가) |
| 두 회사 절반 정도(49.9~54.2%) 5개 한 달 -17.3~-21.2% | -17.34~-21.21 | S1 https://www.funetf.co.kr/product/etf/view/KR7396500001 · https://www.funetf.co.kr/product/etf/view/KR70167A0001 |
| 1천만원 석 달 뒤 약 718만원 vs 약 897만원 | 1,000×(1-0.2825)=717.5 · ×(1-0.1033)=896.7 | S1 https://www.funetf.co.kr/product/etf/view/KR7395160005 · https://www.funetf.co.kr/product/etf/view/KR7471990002 · calc_out.txt |
| 앞 두 달 소부장 +21.3·+24.4%, 반도체 +7.4·+6.9%, TOP2류 -1.3~-11.4% | (1+3개월)/(1+1개월)-1 직접 계산 | S1 https://www.funetf.co.kr/product/etf/view/KR7455850008 · https://www.funetf.co.kr/product/etf/view/KR7471990002 · calc_out.txt |
| 두 회사 0%, 한미반도체·이수페타시스·주성엔지니어링 | PDF 한미 16.2·주성 12.0·이수 9.7(455850) / 이수 20.2·한미 18.5·주성 16.7(471990), 삼성·하이닉스 없음 | S2 https://www.funetf.co.kr/product/etf/view/KR7455850008 · https://www.funetf.co.kr/product/etf/view/KR7471990002 |
| TIGER TOP10·HANARO 두 회사 53% 안팎, 1년 43.8 vs 109.8% | 27.4+25.8=53.2 · 27.6+25.1=52.7 · NAV 1년 43.77 · 109.83 | S1·S2 https://www.funetf.co.kr/product/etf/view/KR7396500001 · https://www.funetf.co.kr/product/etf/view/KR7395270002 |
| SOL TOP2+ 삼성 27.9·하이닉스 26.3 | PDF 27.9 · 26.3 | S2 https://www.funetf.co.kr/product/etf/view/KR70167A0001 |

# 올리기 전 확인
- 2026-11-15 21:4x firemap-write(발행 전날 — 11/16 12:40 발행 회차는 토·일 장이 없어 11/13 기준값이 그대로인지만 확인)
- 다시 연 주소: https://www.funetf.co.kr/product/etf/view/KR7396500001 · https://www.funetf.co.kr/product/etf/view/KR7091160002 · https://www.funetf.co.kr/product/etf/view/KR70167A0001 · https://www.funetf.co.kr/product/etf/view/KR7395160005 · https://www.funetf.co.kr/product/etf/view/KR7395270002 · https://www.funetf.co.kr/product/etf/view/KR7091230003 · https://www.funetf.co.kr/product/etf/view/KR7455850008 · https://www.funetf.co.kr/product/etf/view/KR7469150007 · https://www.funetf.co.kr/product/etf/view/KR7471990002 · https://query1.finance.yahoo.com/v8/finance/chart/396500.KS · https://query1.finance.yahoo.com/v8/finance/chart/091160.KS · https://query1.finance.yahoo.com/v8/finance/chart/455850.KS · https://query1.finance.yahoo.com/v8/finance/chart/395160.KS · https://finance.naver.com/api/sise/etfItemList.nhn (21:2x 받음)
- 기준일: 수익률 2026-11-13(금) 기준가·종가, 구성종목 2026-11-13 종가 화면
- 바뀐 것: 없음(처음 받음, 11/14·15 주말 장 없음)
- 새로 찾은 것: 소부장 ETF 앞 두 달 +21~24% 상승 뒤 한 달 되돌림(직접 계산)
