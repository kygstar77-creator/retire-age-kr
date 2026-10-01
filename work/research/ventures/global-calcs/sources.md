# ③ 나라별 공식 원문 접근성·갱신 주기 (global-calcs)

- 조사: firemap-venture-research-global, 2026-10-01 17:06~17:20 KST. 로그인 없음. curl(데스크톱 UA)·WebFetch·브라우저로 직접 열어 HTTP 상태 확인.
- 요약: 12개국 모두 로그인 없이 공식 원문이 있다. 미국 SSA·호주 ATO·인도 소득세청은 curl 403(브라우저는 열림), 멕시코 IMSS는 브라우저에서도 빈 화면(확인 안 함). → 자동 감시는 브라우저 방식이 필요한 나라가 있다.

| 나라 | 공식 원문 (HTTP) | 형식 | 갱신·연중 변경 | 언어 | 대조용 공식 계산기 | AI 단독 유지 |
|---|---|---|---|---|---|---|
| 미국 | IRS Pub 15-T https://www.irs.gov/publications/p15t (200) · SSA 상한 https://www.ssa.gov/oact/cola/cbb.html (curl 403, 브라우저 OK) | HTML·PDF(워크시트 1A·2026 표) | 연 1회. 2026 사회보장 상한 $184,500·6.2%, 메디케어 1.45% | 영어 | https://apps.irs.gov/app/tax-withholding-estimator (200, 개인용이라 대조 제한) | **어려움** — 주세·지방세 50곳+, 모은 공식 출처 없음 |
| 영국 | https://www.gov.uk/guidance/rates-and-thresholds-for-employers-2026-to-2027 (200) · https://www.gov.uk/income-tax-rates (200) | HTML 표 | 4/6 시작. 2026-01-30 발행, 09-01 갱신(연료 요율만) | 영어 | https://www.gov.uk/estimate-income-tax (200) | **쉬움** — 한 쪽, 스코틀랜드·웨일스만 따로 |
| 독일 | PAP 2026 https://www.bundesfinanzministerium.de/Content/DE/Downloads/Steuern/Steuerarten/Lohnsteuer/Programmablaufplan/2025-11-12-PAP-2026.html (200) · XML https://www.bmf-steuerrechner.de/javax.faces.resource/daten/xmls/Lohnsteuer2026.xml.xhtml (200) · 사회보험 https://www.bmas.de/DE/Service/Presse/Pressemitteilungen/2025/sozialversicherungsrechengroessen-2026.html (200) | **기계용 XML 의사코드** | 연 1회(2025-11-12 확정). 과거 연중판 2024-12·2023-07 | 독일어 | https://www.bmf-steuerrechner.de/ (200) + 외부 인터페이스 /interface/einganginterface.xhtml (200) | **중간** — 식은 쉬움, 의보 추가보험료(보험사별)·교회세(주별) |
| 프랑스 | 원천징수 중립세율 https://bofip.impots.gouv.fr/bofip/11255-PGP.html (200, 2026-07-06) · URSSAF https://www.urssaf.fr/accueil/outils-documentation/taux-baremes/taux-cotisations-secteur-prive.html (200) | HTML 표 | 세율표 "2026-05-01부터"(연중 변경) · URSSAF 1/1, 상한 연 192,240€ | 프랑스어 | https://mon-entreprise.urssaf.fr/simulateurs/salaire-brut-net (200, 소스 MIT 공개 betagouv/mon-entreprise) | **어려움** — 항목 많음, Agirc-Arrco 별도 출처 |
| 스페인 | https://sede.agenciatributaria.gob.es/Sede/Retenciones.shtml (200) · https://www.seg-social.es/wps/portal/wss/internet/Trabajadores/CotizacionRecaudacionTrabajadores/36537 (200) | 알고리즘 PDF·XSD·웹서비스 | **2026년 2판(1/1~9/9, 9/10~)** · 노동자 4.70%, 상한 월 5,101.20€, MEI 0.9% | 스페인어 | R260/R261 https://www2.agenciatributaria.gob.es/wlpl/PRET-R200/R261/index.zul (200) | **중간** — 연중 판 교체, 자치주 차이 |
| 캐나다 | T4127 https://www.canada.ca/en/revenue-agency/services/forms-publications/payroll/t4127-payroll-deductions-formulas.html (curl 시간 초과, WebFetch OK) | HTML 공식 | 1/1(122판)·7/1(123판) 연 2회 | 영·불 | PDOC(브라우저 OK), 퀘벡은 WebRAS | **중간** — 주 13 + 퀘벡 별도 |
| 호주 | Schedule 1 https://www.ato.gov.au/tax-rates-and-codes/payg-withholding-schedule-1-statement-of-formulas-for-calculating-amounts-to-be-withheld (curl 403, 브라우저 OK) | HTML 계수표+샘플 | 7/1 적용, 2026판 6/17 발행 | 영어 | https://www.ato.gov.au/calculators-and-tools/tax-withheld-calculator (브라우저 OK) | **쉬움** — 계수표 1개, 수집은 403 |
| 일본 | https://www.nta.go.jp/publication/pamph/gensen/zeigakuhyo2026/01.htm (200) · 전산 특례 PDF denshi_01.pdf (200) · 협회건보 r08 (200) · 연금 (200) | PDF·Excel | 2026-01-01 지급분부터(기초공제 개정). 건보 매년 3월분, 도도부현별 | 일본어 | 확인 안 함 | **중간** — 건보 47곳 |
| 인도 | https://www.incometaxindia.gov.in/ (curl 403, 브라우저 OK) | HTML·PDF | 2월 예산 → 4/1 시행. **2026-04-01 새 소득세법 2025 시행** | 영·힌디 | https://www.incometax.gov.in/iec/foportal/income-tax-calculator (200) | **어려움** — 법 교체 중, 신·구 제도. 세율표 쪽·EPF 확인 안 함 |
| 네덜란드 | 자동급여 계산규정 https://www.belastingdienst.nl/wps/wcm/connect/bldcontentnl/themaoverstijgend/brochures_en_publicaties/rekenvoorschriften-voor-de-geautomatiseerde-loonadministratie (200) · PDF (200) · 원천징수표 (200) | PDF + 파라미터 XLSX | 1월 연 1회, 2025~26 연중판 없음 | 네덜란드어 | 확인 안 함 | **쉬움~중간** |
| 브라질 | https://www.gov.br/receitafederal/pt-br/assuntos/meu-imposto-de-renda/tabelas/2026 (200, 2026-04-27) · INSS https://www.gov.br/inss/pt-br/direitos-e-deveres/inscricao-e-contribuicao/tabela-de-contribuicao-mensal (200) | HTML 표 | 연중 변경 잦음(2025-05 Lei 15.191, 2026 Lei 15.270 감면) · INSS 상한 8,475.55 | 포르투갈어 | 확인 안 함 | **중간** |
| 멕시코 | SAT 부속서 8 PDF https://www.sat.gob.mx/minisitio/NormatividadRMFyRGCE/documentos2026/rmf/anexos/Anexo-8-RMF-2026_DOF-28122025.pdf (200) · IMSS (403, 빈 화면) | PDF | 12월 말 관보, 연중 변경 확인 안 함 | 스페인어 | 확인 안 함 | **어려움** — subsidio·IMSS 요율 원문 확보 못 함 |

## 재사용 조건(사이트에 적힌 것만)
- 영국: Open Government Licence v3.0 — 출처 표시로 재사용 가능.
- 호주: 복사·수정·배포 가능, 단 ATO·정부 보증처럼 보이면 안 됨(https://www.ato.gov.au/about-ato/using-our-website/copyright-notice).
- 캐나다: **비상업 복제만**, 상업 재배포는 서면 허가(https://www.canada.ca/en/transparency/terms.html) → 원문을 옮기지 말고 숫자로 직접 계산만.
- 프랑스: URSSAF 계산기 소스 MIT.
- 독일·미국·일본·스페인·네덜란드·브라질·멕시코·인도: 확인 안 함.

## 판정 — AI 직원만으로 법 개정을 따라갈 수 있나
- **된다(조건부):** 영국·호주·독일·네덜란드·캐나다·스페인은 공식 식/계수표 + 대조 공식 계산기가 있어 'X-CN-1식 원문 대조 도장'을 그대로 쓸 수 있다. 독일(XML+외부 인터페이스)·스페인(XSD+웹서비스)은 기계 대조까지 된다.
- **연 1회 갱신으론 부족:** 캐나다 7월판, 스페인 9/10판, 프랑스 5/1, 브라질 2025-05, 독일 과거 연중판, 호주 7/1 회계연도. → 감시 루틴은 월 1회 원문 해시 비교가 최소.
- **첫 판에서 뺄 나라:** 미국(주세), 인도(법 교체), 멕시코(원문 미확보), 프랑스(항목·보충연금).
- 미확인: 미국 주별 원천징수 공식, 일본 고용보험·2026-04 육아지원금, 인도 EPF, 멕시코 IMSS·subsidio, 프랑스 Agirc-Arrco.
