# kofinpair1124 — 쇼츠 de1s_kofin(m51UDa2pd-g, 11/24 19:20) 짝 카페 글 준비 자료 (firemap-write 2026-11-23 09:3x, 아직 묶음 아님)
쇼츠 질문: 국내 고배당 ETF는 담은 돈 절반 넘게 금융주(PLUS 55.6%·SOL 56.5%, 운용사 11/20자)
짝 글 다음 질문 후보: "다른 국내 고배당 ETF도 금융주가 절반일까?" — 영상에 없는 새 사실

## 네이버 증권 ETF 분석(m.stock.naver.com/api/stock/<코드>/etfAnalysis) 2026-11-23 받음, 기준일 2026.11.20 — raw/etf_*.json (2차 1곳)
| ETF | 금융 % | 1위 업종이 금융 아님 |
|---|---|---|
| KODEX 주주환원고배당주 0153K0 | 56.64 | |
| SOL 코리아고배당 0105E0 | 56.57 | |
| PLUS 고배당주 161510 | 56.01 | |
| KODEX 고배당주 279530 | 52.57 | |
| HANARO K고배당 322410 | 43.51 | |
| ACE 고배당주 0139P0 | 37.42 | |
| TIGER 코스피고배당 210780 | 34.11 | |
| RISE 대형고배당10TR 315960 | 33.13 | IT 49.2(삼성전자 25.84·SK하이닉스 23.37) |
| RISE 고배당 266160 | 29.82 | IT 45.5(삼성전자 23.90·SK하이닉스 21.58) |
| KIWOOM 코리아고배당 104530 | 26.90 | |
→ 10종 중 4종만 절반 넘음, 2종은 반도체 두 종목이 절반 가까이

## 막힌 것 / 남은 일
- 2차 1곳뿐 → 대조 줄마다 2곳 필요(A-02). PLUS·SOL은 운용사 원문 있음(cardshorts/de1s_kofin/prepub_1121.txt). 나머지 8종은 운용사 PDF(KODEX samsungfund·RISE riseetf·TIGER tigeretf·ACE aceetf·HANARO hanaroetf·KIWOOM kiwoometf) 받아 금융 분류(은행·보험·증권·카드·지주·재보험, 영상과 같은 기준)로 직접 합산하면 1차가 됨
- FunETF 업종별(제로인, 9/30 분기)은 curl·헤드리스 둘 다 zeroinstock API가 빈 값 — 쓰지 못함
- 칸: slots 11/24 22:40(배당, 관문 기한 11/24 16:40) · 쇼츠 공개 확인 뒤 발행 · 영상 링크 m51UDa2pd-g

## 1차 대조 (운용사 원문) — 2026-11-23 09:3x
- KODEX 고배당주: https://m.samsungfund.com/api/v1/kodex/product-pdf/2ETF96.do?gijunYMD=20261120 (raw/kodex_279530_20261120.json, calc.py) → calc_out.txt. 네이버 52.57과 맞음
- PLUS·SOL: cardshorts/de1s_kofin/prepub_1121.txt (55.645·56.463)
- 남은 7종: KODEX 주주환원고배당주(fId 찾기 — samsungfund 상품 목록), RISE 2종·TIGER·ACE·HANARO·KIWOOM 운용사 PDF
