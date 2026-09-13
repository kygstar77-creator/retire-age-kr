// 해외/국내 파이어 도시 데이터 (탐색기 + 결과 희망편 공용)
// krw = 1인 월 생활비(집세 포함), 2026-09 조사.
// 해외: Numbeo '1인 월 생활비(집세 제외)' + '도심 1룸 월세' 합산, 2026-08~09 자료, 환율 2026-09-13.
//   numbeo.com/cost-of-living/in/{Chiang-Mai, Bangkok, Da-Nang, Ho-Chi-Minh-City, Kuala-Lumpur, Penang, Cebu, Tbilisi, Lisbon, Porto, Taipei, Medellin}
//   우붓은 Numbeo 페이지가 없어 livingcost.org/cost/indonesia/ubud(2026-06). 후쿠오카는 표본 부족으로 요약치가 없어 예전 값 유지(미확인).
// 국내: 통계청 가계동향조사 2026년 1/4분기 1인가구 소비지출 180.7만 중 주거·수도·광열 35.3만을 뺀 145.4만(전국 공통)
//   + 한국부동산원 지역 평균월세(서울·수도권·광역시 오피스텔, 지방 도시 아파트). 시군별 1인가구 생활비 통계는 없다.
export const FIRE_CITIES = [
  { city: '치앙마이', lat: 18.8, lon: 99.0, country: '태국', flag: '🇹🇭', krw: 1390000, c1: '#f97316', c2: '#fb923c',
    vibe: '태국 북부 산악 도시, 사원과 카페가 많아요.',
    food: ['카오소이', '망고 찰밥', '길거리 팟타이'], play: ['올드시티 사원', '주말 야시장', '도이수텝 일출'],
    visa: '관광·교육·은퇴(Non-O-A) 비자 옵션 · 민간 의료보험 권장 · 건기 11~2월 쾌적' },
  { city: '다낭', lat: 16.0, lon: 108.2, country: '베트남', flag: '🇻🇳', krw: 1320000, c1: '#0ea5e9', c2: '#38bdf8',
    vibe: '베트남 중부 해안 도시, 해변이 길게 이어져요.',
    food: ['반쎄오', '미꽝', '연유 커피'], play: ['미케 비치', '바나힐', '호이안 야경'],
    visa: '관광·거주 옵션 · 사보험 필요 · 우기 9~12월 유의' },
  { city: '우붓(발리)', lat: -8.5, lon: 115.3, country: '인도네시아', flag: '🇮🇩', krw: 1220000, c1: '#10b981', c2: '#34d399',
    vibe: '발리 내륙 지역, 논밭과 요가 스튜디오가 많아요.',
    food: ['나시고렝', '바비굴링', '코코넛'], play: ['라이스테라스', '요가 리트릿', '폭포 트레킹'],
    visa: '관광·B211 등 장기 옵션 · 사보험 필요 · 우기 11~3월' },
  { city: '쿠알라룸푸르', lat: 3.1, lon: 101.7, country: '말레이시아', flag: '🇲🇾', krw: 1630000, c1: '#8b5cf6', c2: '#a78bfa',
    vibe: '말레이시아 수도, 대중교통과 쇼핑몰이 잘 갖춰졌어요.',
    food: ['나시르막', '바쿠테', '두리안'], play: ['페트로나스 트윈타워', '바투 동굴', '루프탑 바'],
    visa: 'MM2H 등 장기 옵션 · 의료 양호 · 연중 고온다습' },
  { city: '트빌리시', lat: 41.7, lon: 44.8, country: '조지아', flag: '🇬🇪', krw: 1810000, c1: '#ef4444', c2: '#f87171',
    vibe: '조지아 수도, 구시가와 온천·와이너리가 있어요.',
    food: ['하차푸리', '힌칼리', '조지아 와인'], play: ['올드타운', '와이너리 투어', '카즈베기 설산'],
    visa: '다수 국적 1년 무비자 체류(확인 필요) · 물가 매우 저렴' },
  { city: '리스본', lat: 38.7, lon: -9.1, country: '포르투갈', flag: '🇵🇹', krw: 3400000, c1: '#0d9488', c2: '#2dd4bf',
    vibe: '포르투갈 수도, 대서양 연안의 언덕 도시예요.',
    food: ['바칼라우', '파스텔 드 나타', '해산물 플레이트'], play: ['트램 28', '신트라 성', '대서양 일몰'],
    visa: '유럽 장기 비자 옵션(요건 까다로움) · 물가 서유럽 중 낮은 편' },
  { city: '후쿠오카', lat: 33.6, lon: 130.4, country: '일본', flag: '🇯🇵', krw: 3300000, c1: '#3b82f6', c2: '#60a5fa',
    vibe: '일본 규슈의 관문 도시, 한국에서 가까워요.',
    food: ['돈코츠 라멘', '모츠나베', '명란'], play: ['포장마차 거리', '온천 당일치기', '벚꽃 시즌'],
    visa: '관광·장기 비자 옵션 · 의료·치안 우수 · 가까운 거리' },
  { city: '제주', lat: 33.5, lon: 126.5, country: '한국', flag: '🇰🇷', krw: 2290000, c1: '#22c55e', c2: '#4ade80',
    vibe: '한국 남쪽 섬, 바다와 오름이 있어요.',
    food: ['고기국수', '갈치조림', '흑돼지'], play: ['올레길', '한라산', '카페 투어'],
    visa: '국내 · 비자 불필요 · 렌터카 권장' },
  { city: '방콕', lat: 13.7, lon: 100.5, country: '태국', flag: '🇹🇭', krw: 1900000, c1: '#f59e0b', c2: '#fbbf24',
    vibe: '태국 수도, 대형 병원과 쇼핑몰이 많은 대도시예요.',
    food: ['팟타이', '똠얌꿍', '망고 스무디'], play: ['왓아룬', '루프탑 바', '짜뚜짝 시장'],
    visa: '관광·장기 비자 옵션 · 사보험 권장 · 연중 무더위' },
  { city: '호치민', lat: 10.8, lon: 106.7, country: '베트남', flag: '🇻🇳', krw: 1440000, c1: '#06b6d4', c2: '#22d3ee',
    vibe: '베트남 남부 최대 도시, 상업 중심지예요.',
    food: ['쌀국수', '반미', '카페 쓰어다'], play: ['벤탄 시장', '메콩강 투어', '루프탑 카페'],
    visa: '관광·거주 옵션 · 사보험 필요 · 우기 5~10월' },
  { city: '페낭', lat: 5.4, lon: 100.3, country: '말레이시아', flag: '🇲🇾', krw: 1240000, c1: '#a855f7', c2: '#c084fc',
    vibe: '말레이시아 북서부 섬, 조지타운 벽화거리가 있어요.',
    food: ['차퀘이테우', '나시칸다', '아삼락사'], play: ['조지타운 벽화', '해변', '국립공원'],
    visa: 'MM2H 등 장기 옵션 · 의료 양호 · 고온다습' },
  { city: '세부', lat: 10.3, lon: 123.9, country: '필리핀', flag: '🇵🇭', krw: 1400000, c1: '#14b8a6', c2: '#2dd4bf',
    vibe: '필리핀 중부 섬, 해변과 다이빙 명소가 많아요.',
    food: ['레촌', '시니강', '망고'], play: ['아일랜드 호핑', '다이빙', '폭포'],
    visa: '관광 연장·파이어(SRRV) 옵션 · 사보험 필요 · 우기 유의' },
  { city: '타이베이', lat: 25.0, lon: 121.5, country: '대만', flag: '🇹🇼', krw: 2360000, c1: '#3b82f6', c2: '#60a5fa',
    vibe: '대만 수도, 대중교통과 야시장이 발달했어요.',
    food: ['우육면', '딤섬', '버블티'], play: ['예스진지', '온천', '야시장 투어'],
    visa: '관광·장기 옵션 · 의료·치안 우수 · 습한 기후' },
  { city: '포르투', lat: 41.1, lon: -8.6, country: '포르투갈', flag: '🇵🇹', krw: 2920000, c1: '#0891b2', c2: '#06b6d4',
    vibe: '포르투갈 북부 도시, 도루강과 와이너리가 있어요.',
    food: ['프란세지냐', '포트 와인', '대구 요리'], play: ['도루강 크루즈', '와이너리', '구시가'],
    visa: '유럽 장기 비자 옵션(요건 까다로움) · 온화한 기후' },
  { city: '메데인', lat: 6.2, lon: -75.6, country: '콜롬비아', flag: '🇨🇴', krw: 2570000, c1: '#ec4899', c2: '#f472b6',
    vibe: '콜롬비아 제2도시, 연중 봄 같은 기후예요.',
    food: ['반데하 파이사', '아레파', '콜롬비아 커피'], play: ['코무나13', '케이블카', '근교 마을'],
    visa: '관광·노마드 비자 옵션 · 사보험 필요 · 치안 지역 확인' },
  { city: '부산', lat: 35.1, lon: 129.0, country: '한국', flag: '🇰🇷', krw: 2030000, c1: '#0ea5e9', c2: '#38bdf8',
    vibe: '한국 제2도시, 바다·온천·회가 있어요.',
    food: ['밀면', '돼지국밥', '회'], play: ['해운대', '감천문화마을', '광안리 야경'],
    visa: '국내 · 비자 불필요 · 대중교통 편리' },
  // ── 2026-09 추가 12곳. 기준은 위와 같음(Numbeo 1인 생활비+도심 1룸 월세). Numbeo 무료 한도 초과로 web.archive.org 보존본(2026-05~09)에서 읽음.
  //    환율 open.er-api.com 2026-09-13 단일 세트. 상세 근거: scratchpad/cities_add_overseas.md (각 항목 아래 src 주석).
  { city: '발렌시아', lat: 39.47, lon: -0.38, country: '스페인', flag: '🇪🇸', krw: 3010000, c1: '#f97316', c2: '#fdba74',
    vibe: '스페인 지중해 연안 제3도시, 파에야의 고향에 해변과 정원이 있어요.',
    food: ['파에야', '오르차타', '피데우아'], play: ['예술과학도시', '투리아 정원', '말바로사 해변'],
    visa: '무비자 90일·비영리 거주비자 옵션(IPREM 400%) · 의료 양호 · 지중해성 온화' },
  // src: ko.wikipedia.org/wiki/발렌시아 (좌표·음식·명소·지중해 연안 제3도시) · en.wikipedia.org/wiki/Valencia (Köppen BSh/Csa, 연평균 18.6℃) · Numbeo Health Care 2026 Mid-Year 77.0 (web.archive.org/web/20260902205033/https://www.numbeo.com/health-care/rankings.jsp) · 비자 exteriores.gob.es/Embajadas/seul/ko/.../Visado-de-residencia-no-lucrativa.aspx · 여행경보 0404.go.kr/ntnSafetyInfo/128/detail
  { city: '마드리드', lat: 40.42, lon: -3.70, country: '스페인', flag: '🇪🇸', krw: 3390000, c1: '#dc2626', c2: '#f87171',
    vibe: '스페인 수도, 해발 667m 고원의 미술관·공원 도시예요.',
    food: ['코시도 마드릴레뇨', '보카디요 데 칼라마레스', '추로스'], play: ['프라도 미술관', '레티로 공원', '마요르 광장'],
    visa: '무비자 90일·비영리 거주비자 옵션 · 의료 우수 · 여름 덥고 겨울 서늘' },
  // src: ko.wikipedia.org/wiki/마드리드 (좌표·해발 667m·프라도/레티로/마요르) · en.wikipedia.org/wiki/Cocido_madrileño · en.wikipedia.org/wiki/Bocadillo_de_calamares (마요르 광장 명물) · en.wikipedia.org/wiki/Madrid Climate (BSk/Csa, 1월 6.5℃·7월 26.2℃) · Health Care 79.2 · 비자 스페인대사관 NLV 페이지(위) · 0404.go.kr/ntnSafetyInfo/128/detail
  { city: '프라하', lat: 50.08, lon: 14.42, country: '체코', flag: '🇨🇿', krw: 2820000, c1: '#b45309', c2: '#f59e0b',
    vibe: '체코 수도, 블타바강과 구시가·프라하성이 있어요.',
    food: ['스비치코바', '트르델니크', '필스너 맥주'], play: ['카를교', '프라하성', '구시가 천문시계'],
    visa: '무비자 90일·장기비자(기타 목적) 옵션 · 치안 우수 · 겨울 춥고 사계절' },
  // src: ko.wikipedia.org/wiki/프라하 (좌표·블타바강·카를교·프라하성·천문시계) · en.wikipedia.org/wiki/Czech_cuisine (svíčková·trdelník·Pilsner) · en.wikipedia.org/wiki/Prague (Cfb, 연평균 11.5℃, 1월 1.8℃) · Health Care 74.7 · Crime Index 24.7(치안 우수) web.archive.org/web/20260908094104/https://www.numbeo.com/crime/rankings.jsp · 0404.go.kr/ntnSafetyInfo/195/detail (전 지역 1단계, "치안상태가 우수") · 비자 overseas.mofa.go.kr/cz-ko/brd/m_8967/view.do?seq=590161 · mzv.gov.cz/jnp/en/information_for_aliens/long_stay_visa/
  { city: '아테네', lat: 37.97, lon: 23.72, country: '그리스', flag: '🇬🇷', krw: 2280000, c1: '#0284c7', c2: '#7dd3fc',
    vibe: '그리스 수도, 아크로폴리스와 지중해성 기후예요.',
    food: ['수블라키', '무사카', '그리스 샐러드'], play: ['아크로폴리스', '리카비토스 언덕', '국립정원'],
    visa: '무비자 90일·경제자립자(FIP) 거주 옵션(월 3,500유로) · 소매치기·지진 유의 · 여름 무더위' },
  // src: ko.wikipedia.org/wiki/아테네 (좌표·아크로폴리스·리카비토스·국립정원) · en.wikipedia.org/wiki/Greek_cuisine · en.wikipedia.org/wiki/Athens Climate 절 (Csa, 연평균 19.2℃, 7월 29.3℃) · Health Care 58.4 · 0404.go.kr/ntnSafetyInfo/11/detail (소매치기·지진·산불 유의) · 비자 mfa.gr/missionsabroad/en/visas.html?mission=sel&mis=republic-of-korea · stathaki-tsopela.gr (FIP 월 €3,500, Law 5038/2023)
  { city: '이스탄불', lat: 41.02, lon: 28.97, country: '튀르키예', flag: '🇹🇷', krw: 2270000, c1: '#e11d48', c2: '#fb7185',
    vibe: '보스포루스 해협을 끼고 유럽·아시아에 걸친 도시예요.',
    food: ['발릭 에크멕', '시미트', '바클라바'], play: ['아야소피아', '그랜드 바자르', '갈라타 타워'],
    visa: '무비자 90일·단기거주허가 옵션 · 여행유의 1단계 · 온화한 해양성' },
  // src: ko.wikipedia.org/wiki/이스탄불 (좌표·보스포루스·아야소피아·그랜드바자르·갈라타) · en.wikipedia.org/wiki/Balık_ekmek (에미뇌뉘 명물) · en.wikipedia.org/wiki/Turkish_cuisine (simit·baklava) · en.wikipedia.org/wiki/Climate_of_Istanbul (Csa/Cfa 경계, 연평균 14.4℃) · Health Care 70.1 · 0404.go.kr/ntnSafetyInfo/228/detail (이스탄불 1단계) · 비자 overseas.mofa.go.kr/tr-istanbul-ko/brd/m_27227/view.do?seq=1347114 · en.goc.gov.tr/residence-
  { city: '안탈리아', lat: 36.90, lon: 30.68, country: '튀르키예', flag: '🇹🇷', krw: 1570000, c1: '#0ea5e9', c2: '#67e8f9',
    vibe: '튀르키예 지중해 연안 휴양 도시, 산과 해변이 가까워요.',
    food: ['안탈리아 피야즈', '케밥', '바클라바'], play: ['칼레이치 구시가', '코냐알트 해변', '뒤덴 폭포'],
    visa: '무비자 90일·단기거주허가 옵션 · 여행유의 1단계 · 여름 무덥고 겨울 온화' },
  // src: ko.wikipedia.org/wiki/안탈리아 (좌표·지중해 연안·산으로 둘러싸임) · en.wikipedia.org/wiki/Antalya (Csa, 연평균 19.0℃, 8월 29.0℃·2월 10.8℃, Kaleiçi·Konyaaltı·Düden) · en.wikipedia.org/wiki/Piyaz (안탈리아 등록 향토음식) · Health Care 73.7 · Crime 29.1 · 0404.go.kr/ntnSafetyInfo/228/detail · 비자 이스탄불과 동일
  { city: '두바이', lat: 25.20, lon: 55.27, country: 'UAE', flag: '🇦🇪', krw: 4830000, c1: '#d97706', c2: '#fcd34d',
    vibe: '페르시아만 연안 UAE 최대 도시, 사막 기후의 초고층 도시예요.',
    food: ['마츠부스', '루카이마트', '샤와르마'], play: ['부르즈 할리파', '두바이 몰', '두바이 크리크'],
    visa: '무비자 90일·은퇴 거주비자(55세+) 옵션 · 치안 매우 우수·사보험 필수 · 여름 40℃ 넘는 사막' },
  // src: ko.wikipedia.org/wiki/두바이 (좌표·페르시아만·UAE 최대 도시·더운 사막 기후·부르즈할리파·두바이몰·크리크) · en.wikipedia.org/wiki/Dubai (BWh, 연평균 27.2℃, 8월 최고 42.1℃) · en.wikipedia.org/wiki/Emirati_cuisine (machboos·luqaimat·shawarma) · Crime 16.2(세계 최저권) · Health Care 70.0 · 비자 mofa.go.kr/ae-ko/brd/m_11118/view.do?seq=1346262 · dubai.ae/living/residency/residence-visa-for-the-retired (55세+, 100만 AED 또는 연 24만 AED, 5년) · 의료보험 의무 globe-insight.com/두바이-이민-절차/
  { city: '알마티', lat: 43.28, lon: 76.90, country: '카자흐스탄', flag: '🇰🇿', krw: 2080000, c1: '#16a34a', c2: '#86efac',
    vibe: '톈산 산맥 기슭의 카자흐스탄 최대 도시, 스키장과 호수가 가까워요.',
    food: ['베쉬바르막', '플로프', '바우르삭'], play: ['메데우 빙상장', '침불락 스키장', '콕토베 케이블카'],
    visa: '무비자 30일(180일 중 90일)·Neo Nomad 비자 옵션 · 의료 보통 · 겨울 영하, 여름 더움' },
  // src: ko.wikipedia.org/wiki/알마티 (좌표·최대 도시·톈산 기슭) · en.wikipedia.org/wiki/Almaty (Dfa, 연평균 10℃, 1월 −4.7℃·7월 23.8℃, Medeu 1,691m·Shymbulak·Kok Tobe·Big Almaty Lake) · en.wikipedia.org/wiki/Kazakh_cuisine (beshbarmak·palaw·bawyrsaq) · Health Care 50.9 · 비자 overseas.mofa.go.kr/kz-almaty-ko/brd/m_8314/view.do?seq=1342549 · astanatimes.com/2025/04/why-neo-nomad-visa-launch-is-kazakhstans-masterstroke/ (월 US$3,000, 1년+연장)
  { city: '멕시코시티', lat: 19.43, lon: -99.13, country: '멕시코', flag: '🇲🇽', krw: 2630000, c1: '#65a30d', c2: '#bef264',
    vibe: '해발 2,250m 고원의 멕시코 수도, 연중 온화해요.',
    food: ['타코 알 파스토르', '타말', '몰레'], play: ['소칼로', '차풀테펙 공원', '소치밀코 운하'],
    visa: '무비자 최대 180일·임시거주 옵션 · 치안 지역 확인 · 고원 연중 온화' },
  // src: ko.wikipedia.org/wiki/멕시코시티 (좌표·해발 2,250m·고원) · en.wikipedia.org/wiki/Mexico_City Climate 절 (Cwb, 연평균 18.1℃, 5월 20.4℃·12월 15.4℃) · en.wikipedia.org/wiki/Mexican_cuisine (tacos al pastor "staple of Mexico City's street food"·tamales·mole) · en.wikipedia.org/wiki/Tourism_in_Mexico_City (Zócalo·Chapultepec·Xochimilco) · Health Care 66.0 · Crime 66.2 · 0404.go.kr/ntnSafetyInfo/58/detail (멕시코시티 1단계, 치아파스·시날로아 3단계) · 비자 mofa.go.kr/mx-ko/brd/m_5936/view.do?seq=1346916 · embamex.sre.gob.mx/corea/index.php/visas/requisitos
  { city: '부에노스아이레스', lat: -34.60, lon: -58.38, country: '아르헨티나', flag: '🇦🇷', krw: 2190000, c1: '#0369a1', c2: '#7dd3fc',
    vibe: '라플라타강 하구의 아르헨티나 수도, 탱고와 공원이 많아요.',
    food: ['아사도', '엠파나다', '둘세 데 레체'], play: ['라 보카 카미니토', '산텔모 시장', '팔레르모 공원'],
    visa: '무비자 90일·연금자 거주 옵션 · 소매치기 유의 · 온난 습윤' },
  // src: ko.wikipedia.org/wiki/부에노스아이레스 (좌표·라플라타 하구·아사도·엠파나다·둘세데레체·라보카·산텔모·팔레르모·탱고) · en.wikipedia.org/wiki/Buenos_Aires (Cfa, 연평균 18.1℃, 1월 24.9℃·7월 11.0℃, 공원 250곳+) · Health Care 68.0 · Crime 63.0 · 0404.go.kr/ntnSafetyInfo/138/detail (산텔모·라보카 소매치기 유의) · 비자 overseas.mofa.go.kr/ar-ko/brd/m_6224/view.do?seq=1347308 · argentina.gob.ar/servicio/obtener-una-residencia-temporaria-como-pensionado
  { city: '도쿄', lat: 35.68, lon: 139.77, country: '일본', flag: '🇯🇵', krw: 3050000, c1: '#4f46e5', c2: '#a5b4fc',
    vibe: '일본 수도이자 최대 도시, 교통과 의료가 촘촘해요.',
    food: ['에도마에 스시', '몬자야키', '라멘'], play: ['아사쿠사 센소지', '우에노 공원', '도쿄 스카이트리'],
    visa: '무비자 90일·디지털노마드(6개월) 옵션 · 의료·치안 우수 · 온난 습윤' },
  // src: ko.wikipedia.org/wiki/도쿄 (좌표·수도·최대 도시·에도마에 스시·몬자야키·라멘·센소지·우에노·스카이트리·온난 습윤) · en.wikipedia.org/wiki/Tokyo Climate 절 (Cfa, 연평균 15.8℃, 8월 26.9℃·1월 5.4℃) · Health Care 78.3 · Crime 24.1 · 0404.go.kr/ntnSafetyInfo/183/detail (여행경보 미발령, 후쿠시마 원전 30km 제외) · 비자 jp.mofa.go.kr/jp-ko/wpge/m_1153/contents.do · moj.go.jp/isa/applications/status/designatedactivities10_00001.html (6개월, 연수입 1,000만엔, 갱신 불가)
  { city: '빈', lat: 48.21, lon: 16.37, country: '오스트리아', flag: '🇦🇹', krw: 3380000, c1: '#7c3aed', c2: '#c4b5fd',
    vibe: '도나우강과 빈 숲이 있는 오스트리아 수도, 카페하우스 문화가 있어요.',
    food: ['비너 슈니첼', '자허토르테', '아펠슈트루델'], play: ['쇤브룬 궁전', '슈테판 대성당', '도나우 섬'],
    visa: '무비자 90일·비취업 정착허가(쿼터) 옵션 · 의료·치안 우수 · 겨울 춥고 사계절' },
  // src: en.wikipedia.org/wiki/Vienna (좌표 48.2083/16.3725, Cfa/Cfb, 연평균 12.6℃, 1월 2.1℃, Schönbrunn·Stephansdom·Danube Island·Vienna Woods) · en.wikipedia.org/wiki/Viennese_cuisine (Wiener Schnitzel·Sachertorte·Apfelstrudel·coffee house) · Health Care 79.9 · Crime 29.4 · 0404.go.kr/ntnSafetyInfo/163/detail · 비자 migration.gv.at/en/types-of-immigration/permanent-immigration/other-forms-of-settlement/ (연금자·경제자립자용, 쿼터제, 2026 1인 월 €2,616.78)
];

// 국내 지역 1인 월 생활비(집세 포함) — 전국 비주거 145.4만(통계청 2026 1Q) + 지역 평균월세(한국부동산원). 지역 차이는 월세에서만 난다.
export const KR_REGIONS = [
  { city: '서울', krw: 2400000, note: '전국 최고 비용' },
  { city: '경기(수도권)', krw: 2300000, note: '서울 인접' },
  { city: '제주', krw: 2290000, note: '관광 물가로 비교적 높음' },
  { city: '인천', krw: 2150000, note: '수도권 + 바다' },
  { city: '부산', krw: 2030000, note: '대도시 인프라 + 바다' },
  { city: '대전', krw: 2010000, note: '교통 중심, 무난' },
  { city: '대구', krw: 2050000, note: '대도시 인프라' },
  { city: '광주', krw: 2000000, note: '음식·물가 무난' },
  { city: '청주', krw: 2190000, note: '중부 거점' },
  { city: '창원', krw: 2060000, note: '계획도시 인프라' },
  { city: '원주', krw: 2100000, note: '수도권 접근 + 저비용' },
  { city: '전주', krw: 2110000, note: '물가 낮고 음식 좋음' },
  { city: '구미', krw: 2020000, note: '월세 저렴(50만대)' },
  // 아래 10곳: 한국부동산원 전국주택가격동향조사 2026.7 아파트 평균월세(시계열 엑셀 '월세가격_아파트' 시트) + 전국 비주거 145.4만.
  // https://www.reb.or.kr/r-one/portal/bbs/rpt/searchBulletinPage.do (등록 2026-08-18 첨부)
  { city: '세종', krw: 2367000 },
  { city: '천안', krw: 2233000 },
  { city: '울산', krw: 2214000 },
  { city: '춘천', krw: 2197000 },
  { city: '순천', krw: 2093000 },
  { city: '포항', krw: 2084000 },
  { city: '김해', krw: 2065000 },
  { city: '안동', krw: 2038000 },
  { city: '목포', krw: 2030000 },
  { city: '거제', krw: 1955000 },
  { city: '군 단위 시골(읍·면)', krw: 1000000, note: '최저 비용, 인프라 적음' }  // 읍·면 단위 공표 통계 없음(미확인)
];

// 도시 월생활비 '단일 소스' — FIRE_CITIES + KR_REGIONS에서 파생. 유형테스트도 이 값을 공유해 영구 싱크(드리프트 방지).
// 비용을 바꿀 땐 위 두 리스트만 고치면 유형테스트까지 자동 일치.
export const CITY_KRW = {};
[...FIRE_CITIES, ...KR_REGIONS].forEach((c) => {
  const base = String(c.city).split('(')[0].trim();
  if (CITY_KRW[base] == null) CITY_KRW[base] = c.krw;
});
