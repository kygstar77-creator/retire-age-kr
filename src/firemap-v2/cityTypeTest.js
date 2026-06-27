import { CITY_KRW } from './cities.js';
// 파이어 라이프 유형 테스트 — 데이터 + 채점 로직 (순수 모듈, 기존 계산/데이터 무손상·추가전용).
// 결과: 8개 파이어족 유형 중 1개 + 내게 맞는 국내·해외 도시 Top3(파이어 적합도 분해 점수).
// 도시 태그(nature/warm/medical 0~1)는 재미용 추정치이며 화면에 "추정" 표기.
// 국내 월생활비는 통계청 1인가구·한국부동산원 월세지수 신호 참고한 추정(정확치 아님). 에이징인플레이스(KB골드라이프 2025: "살던 동네 유지" 80.4%) 수요 반영·국내 강화.

// ── 도시 풀 (국내 8 + 해외 10) — 자기완결 데이터(좌표·월생활비·테마컬러·태그) ──
export const TEST_CITIES = [
  // 국내
  { city: '제주(서귀포)', country: '한국', flag: '🇰🇷', dom: true, lat: 33.25, lon: 126.56, krw: 1900000, c1: '#22c55e', c2: '#4ade80', nature: 0.85, warm: 0.70, medical: 0.70, climate: 'mild', blurb: '바다·오름·카페, 비자도 언어도 필요 없는 국내 한달살이의 상징.' },
  { city: '부산', country: '한국', flag: '🇰🇷', dom: true, lat: 35.18, lon: 129.08, krw: 1550000, c1: '#0ea5e9', c2: '#38bdf8', nature: 0.45, warm: 0.65, medical: 0.85, climate: 'mild', blurb: '대도시 인프라 + 바다, 서울보다 낮은 물가의 균형형.' },
  { city: '강릉', country: '한국', flag: '🇰🇷', dom: true, lat: 37.75, lon: 128.90, krw: 1450000, c1: '#06b6d4', c2: '#22d3ee', nature: 0.80, warm: 0.45, medical: 0.60, climate: 'cold', blurb: 'KTX 2시간, 바다와 커피의 도시. 한달살이 인기 급상승.' },
  { city: '양평', country: '한국', flag: '🇰🇷', dom: true, lat: 37.49, lon: 127.49, krw: 1500000, c1: '#16a34a', c2: '#4ade80', nature: 0.80, warm: 0.40, medical: 0.60, climate: 'cold', blurb: '수도권 접근 + 전원, 인구 증가율 높은 근교 정착지.' },
  { city: '속초', country: '한국', flag: '🇰🇷', dom: true, lat: 38.21, lon: 128.59, krw: 1450000, c1: '#0284c7', c2: '#38bdf8', nature: 0.80, warm: 0.40, medical: 0.55, climate: 'cold', blurb: '설악산과 동해, 서울-양양 고속도로로 가까워진 휴양 도시.' },
  { city: '전주', country: '한국', flag: '🇰🇷', dom: true, lat: 35.82, lon: 127.15, krw: 1300000, c1: '#d97706', c2: '#fbbf24', nature: 0.50, warm: 0.55, medical: 0.70, climate: 'cold', blurb: '물가 낮고 음식 좋은 한옥의 도시, 느린 삶에 어울려요.' },
  { city: '경주', country: '한국', flag: '🇰🇷', dom: true, lat: 35.86, lon: 129.22, krw: 1300000, c1: '#ca8a04', c2: '#facc15', nature: 0.60, warm: 0.55, medical: 0.65, climate: 'cold', blurb: '천년 고도, 평지·자전거·역사. 조용한 정착에 좋아요.' },
  { city: '통영', country: '한국', flag: '🇰🇷', dom: true, lat: 34.85, lon: 128.43, krw: 1250000, c1: '#0891b2', c2: '#22d3ee', nature: 0.85, warm: 0.65, medical: 0.55, climate: 'mild', blurb: '한려수도의 바다, 저비용·풍광형 남해 소도시.' },
  { city: '서울', country: '한국', flag: '🇰🇷', dom: true, lat: 37.57, lon: 126.98, krw: 2050000, c1: '#475569', c2: '#94a3b8', nature: 0.20, warm: 0.55, medical: 0.98, climate: 'cold', blurb: '모든 인프라·의료 최고지만 전국 최고 물가. 익숙한 곳 선호형.' },
  { city: '인천', country: '한국', flag: '🇰🇷', dom: true, lat: 37.46, lon: 126.71, krw: 1650000, c1: '#2563eb', c2: '#60a5fa', nature: 0.40, warm: 0.55, medical: 0.85, climate: 'cold', blurb: '수도권 + 바다·공항, 서울보다 낮은 주거비.' },
  { city: '대전', country: '한국', flag: '🇰🇷', dom: true, lat: 36.35, lon: 127.38, krw: 1450000, c1: '#7c3aed', c2: '#a78bfa', nature: 0.40, warm: 0.55, medical: 0.85, climate: 'cold', blurb: '교통의 중심, 무난한 물가와 든든한 의료.' },
  { city: '여수', country: '한국', flag: '🇰🇷', dom: true, lat: 34.76, lon: 127.66, krw: 1300000, c1: '#0d9488', c2: '#2dd4bf', nature: 0.85, warm: 0.65, medical: 0.55, climate: 'mild', blurb: '밤바다와 섬, 남해안 풍광·저비용의 휴양 도시.' },
  // 해외
  { city: '치앙마이', country: '태국', flag: '🇹🇭', dom: false, lat: 18.8, lon: 99.0, krw: 2200000, c1: '#f97316', c2: '#fb923c', nature: 0.70, warm: 0.95, medical: 0.55, climate: 'hot', blurb: '카페·코워킹·사원과 산, 디지털 노마드의 성지.' },
  { city: '다낭', country: '베트남', flag: '🇻🇳', dom: false, lat: 16.0, lon: 108.2, krw: 2300000, c1: '#0ea5e9', c2: '#38bdf8', nature: 0.70, warm: 0.95, medical: 0.50, climate: 'hot', blurb: '긴 해변과 따뜻한 날씨, 낮은 물가로 시작하기 좋은 해외살이.' },
  { city: '우붓(발리)', country: '인도네시아', flag: '🇮🇩', dom: false, lat: -8.5, lon: 115.3, krw: 2300000, c1: '#10b981', c2: '#34d399', nature: 0.95, warm: 0.95, medical: 0.40, climate: 'hot', blurb: '논밭과 요가, 자연 속 힐링형 파이어 라이프.' },
  { city: '쿠알라룸푸르', country: '말레이시아', flag: '🇲🇾', dom: false, lat: 3.1, lon: 101.7, krw: 2900000, c1: '#8b5cf6', c2: '#a78bfa', nature: 0.30, warm: 0.95, medical: 0.75, climate: 'hot', blurb: '대도시 인프라 + 영어 생활권, 의료도 든든한 균형형.' },
  { city: '트빌리시', country: '조지아', flag: '🇬🇪', dom: false, lat: 41.7, lon: 44.8, krw: 2000000, c1: '#ef4444', c2: '#f87171', nature: 0.60, warm: 0.45, medical: 0.45, climate: 'cold', blurb: '초저비용 + 관대한 체류, 와인과 온천의 숨은 성지.' },
  { city: '리스본', country: '포르투갈', flag: '🇵🇹', dom: false, lat: 38.7, lon: -9.1, krw: 3800000, c1: '#0d9488', c2: '#2dd4bf', nature: 0.50, warm: 0.70, medical: 0.75, climate: 'mild', blurb: '온화한 유럽, 해산물과 골목, 느린 오후의 낭만형.' },
  { city: '후쿠오카', country: '일본', flag: '🇯🇵', dom: false, lat: 33.6, lon: 130.4, krw: 3300000, c1: '#3b82f6', c2: '#60a5fa', nature: 0.45, warm: 0.60, medical: 0.85, climate: 'mild', blurb: '한국과 가깝고 음식·치안 최고, 도시와 자연이 한 시간.' },
  { city: '방콕', country: '태국', flag: '🇹🇭', dom: false, lat: 13.7, lon: 100.5, krw: 2700000, c1: '#f59e0b', c2: '#fbbf24', nature: 0.20, warm: 0.95, medical: 0.70, climate: 'hot', blurb: '없는 게 없는 대도시 + 저렴한 외식, 의료관광 허브.' },
  { city: '호치민', country: '베트남', flag: '🇻🇳', dom: false, lat: 10.8, lon: 106.7, krw: 2200000, c1: '#06b6d4', c2: '#22d3ee', nature: 0.20, warm: 0.95, medical: 0.50, climate: 'hot', blurb: '활기찬 거리와 초저비용, 빠르게 성장하는 노마드 도시.' },
  { city: '페낭', country: '말레이시아', flag: '🇲🇾', dom: false, lat: 5.4, lon: 100.3, krw: 2400000, c1: '#a855f7', c2: '#c084fc', nature: 0.55, warm: 0.95, medical: 0.75, climate: 'hot', blurb: '해변 + 유네스코 올드타운, 영어 통하고 의료 좋은 섬도시.' },
  { city: '세부', country: '필리핀', flag: '🇵🇭', dom: false, lat: 10.3, lon: 123.9, krw: 2100000, c1: '#14b8a6', c2: '#2dd4bf', nature: 0.85, warm: 0.95, medical: 0.55, climate: 'hot', blurb: '에메랄드 바다와 다이빙, 영어 통하는 저비용 휴양형 섬도시.' },
  { city: '하노이', country: '베트남', flag: '🇻🇳', dom: false, lat: 21.03, lon: 105.85, krw: 2100000, c1: '#0ea5e9', c2: '#38bdf8', nature: 0.30, warm: 0.85, medical: 0.55, climate: 'hot', blurb: '호수와 구시가의 활기찬 수도. 덥지만 겨울엔 선선, 초저비용.' },
  { city: '푸꾸옥', country: '베트남', flag: '🇻🇳', dom: false, lat: 10.22, lon: 103.96, krw: 2200000, c1: '#06b6d4', c2: '#22d3ee', nature: 0.90, warm: 0.95, medical: 0.40, climate: 'hot', blurb: '에메랄드 바다의 열대 섬, 비자 편의와 휴양형 저비용.' },
  { city: '달랏', country: '베트남', flag: '🇻🇳', dom: false, lat: 11.94, lon: 108.44, krw: 1900000, c1: '#22c55e', c2: '#4ade80', nature: 0.85, warm: 0.45, medical: 0.45, climate: 'cool', blurb: '해발 1,500m 고원, 연중 18~23℃ 봄 날씨의 꽃·커피 도시. 시원한 곳 1순위.' },
  { city: '카메론하이랜드', country: '말레이시아', flag: '🇲🇾', dom: false, lat: 4.47, lon: 101.38, krw: 2000000, c1: '#16a34a', c2: '#4ade80', nature: 0.95, warm: 0.45, medical: 0.45, climate: 'cool', blurb: '말레이시아 고원, 차밭과 14~25℃ 선선함. 영어권 자연 힐링지.' },
  { city: '바기오', country: '필리핀', flag: '🇵🇭', dom: false, lat: 16.41, lon: 120.59, krw: 1900000, c1: '#4d7c0f', c2: '#a3e635', nature: 0.80, warm: 0.45, medical: 0.55, climate: 'cool', blurb: '필리핀 “여름 수도”, 해발 1,500m 소나무 숲의 선선한 산정 도시.' },
  { city: '메데인', country: '콜롬비아', flag: '🇨🇴', dom: false, lat: 6.24, lon: -75.58, krw: 2000000, c1: '#ec4899', c2: '#f472b6', nature: 0.55, warm: 0.55, medical: 0.60, climate: 'cool', blurb: '“영원한 봄의 도시”, 연중 22℃ 상춘 기후 + 급성장 노마드 커뮤니티.' },
  { city: '부다페스트', country: '헝가리', flag: '🇭🇺', dom: false, lat: 47.5, lon: 19.04, krw: 2800000, c1: '#ef4444', c2: '#f87171', nature: 0.40, warm: 0.40, medical: 0.70, climate: 'cold', blurb: '도나우강과 온천, 사계절 뚜렷한 저렴한 유럽 수도.' },
  { city: '삿포로', country: '일본', flag: '🇯🇵', dom: false, lat: 43.06, lon: 141.35, krw: 3000000, c1: '#3b82f6', c2: '#60a5fa', nature: 0.70, warm: 0.30, medical: 0.85, climate: 'cold', blurb: '눈과 사계절, 깨끗한 자연과 음식의 일본 북방 도시.' },
  { city: '바르셀로나', country: '스페인', flag: '🇪🇸', dom: false, lat: 41.39, lon: 2.17, krw: 3600000, c1: '#0d9488', c2: '#2dd4bf', nature: 0.45, warm: 0.65, medical: 0.80, climate: 'mild', blurb: '지중해 해변과 건축, 온화한 기후의 남유럽 대도시.' },
  { city: '타이베이', country: '대만', flag: '🇹🇼', dom: false, lat: 25.03, lon: 121.56, krw: 3000000, c1: '#3b82f6', c2: '#60a5fa', nature: 0.45, warm: 0.70, medical: 0.90, climate: 'mild', blurb: '한국과 가깝고 치안·교통·야시장·의료 좋은 도시형, 온화한 겨울.' },
  { city: '오사카', country: '일본', flag: '🇯🇵', dom: false, lat: 34.69, lon: 135.5, krw: 3100000, c1: '#60a5fa', c2: '#93c5fd', nature: 0.35, warm: 0.55, medical: 0.85, climate: 'mild', blurb: '먹거리와 교통의 간사이 중심, 사계절 있고 겨울은 온화한 편.' }
];

// 도시 월생활비는 cities.js의 CITY_KRW를 단일 소스로 공유 — '어디서 살까'와 영구 일치(공통 도시 한정).
TEST_CITIES.forEach((c) => {
  const base = String(c.city).split('(')[0].trim();
  if (CITY_KRW[base] != null) c.krw = CITY_KRW[base];
});

// ── 8개 파이어족 유형 ──
export const ARCHETYPES = {
  lean:    { id: 'lean',    name: '린파이어 절약형', nick: '짠테크 수도승', emoji: '🧘', c1: '#475569', c2: '#94a3b8',
    tagline: '적게 쓰고 빠르게 자유로워지는 미니멀리스트.', strong: '높은 저축률로 파이어를 가장 빨리 당겨요.', watch: '너무 조이면 지치기 쉬워요 — 가끔은 보상도.', match: 'fat', action: '자동이체로 저축률부터 끌어올리고, 고정비를 한 줄씩 줄여보세요.' },
  barista: { id: 'barista', name: '바리스타 파이어형', nick: '느긋한 반일러', emoji: '☕', c1: '#c2410c', c2: '#fb923c',
    tagline: '좋아하는 일을 조금 하며 자유와 안정을 함께.', strong: '소액 근로로 건보료·생활비 부담이 확 줄어요.', watch: '일과 쉼의 균형 설계가 핵심.', match: 'coast', action: '좋아하는 일로 월 50~100만 원 파트타임 수입을 설계하면 필요자산이 확 줄어요.' },
  coast:   { id: 'coast',   name: '코스트 파이어형', nick: '굴려두는 낙천가', emoji: '🌊', c1: '#0f766e', c2: '#2dd4bf',
    tagline: '일찍 모아둔 씨앗이 복리로 굵어지게 두고, 생활비는 일로 버는 타입.', strong: '추가 저축 없이 시간이 자산을 불려줘요.', watch: '목표 나이까진 근로 소득이 필요 — 완전 은퇴는 아직이에요.', match: 'barista', action: '목표 나이까지의 근로소득 계획을 세우고, 지금 자산은 인덱스에 묻어두세요.' },
  fat:     { id: 'fat',     name: '팻파이어 여유형', nick: '우아한 미식가', emoji: '🍷', c1: '#6d28d9', c2: '#a78bfa',
    tagline: '넉넉한 자산으로 풍요롭게 즐기는 파이어.', strong: '삶의 질을 지키며 은퇴해요.', watch: '필요 자산이 커서 더 오래 모아야 해요.', match: 'lean', action: '목표 생활비부터 정하고 4%룰로 필요자산을 역산해 모으는 속도를 점검하세요.' },
  settle:  { id: 'settle',  name: '눌러앉기형', nick: '내 동네 터줏대감', emoji: '🏡', c1: '#15803d', c2: '#4ade80',
    tagline: '익숙한 동네에서 안정적으로 머무는 현실파.', strong: '이사 비용·적응 리스크 없이 가장 현실적.', watch: '생활비 절감 여지는 적은 편.', match: 'nomad', action: '지금 동네 생활비를 유지하며 건강보험·연금 수령 시점을 최적화하세요.' },
  monthly: { id: 'monthly', name: '국내 한달살이형', nick: '국내 유랑자', emoji: '🧳', c1: '#0369a1', c2: '#38bdf8',
    tagline: '제주·강릉·부산… 국내를 옮겨다니며 사는 타입.', strong: '비자·언어 부담 없이 새로움과 저비용을 동시에.', watch: '거점 없이 떠돌면 피로가 쌓여요.', match: 'nature', action: '제주·강릉 같은 거점 한 곳을 정해 분기마다 한 달씩 살아보세요.' },
  nomad:   { id: 'nomad',   name: '해외 노마드형', nick: '국경 없는 파이어', emoji: '🌏', c1: '#ea580c', c2: '#fb923c',
    tagline: '저비용 해외에서 자유를 극대화하는 모험가.', strong: '같은 자산으로 더 오래·더 풍요롭게.', watch: '의료·비자·환율 리스크를 챙겨야 해요.', match: 'settle', action: '의료보험·비자·환율을 먼저 점검하고 저비용 도시부터 6개월 살아보세요.' },
  nature:  { id: 'nature',  name: '귀촌 자연형', nick: '산과 바다 은둔자', emoji: '⛰️', c1: '#4d7c0f', c2: '#a3e635',
    tagline: '자연 속에서 느리게 사는 힐링 파이어.', strong: '낮은 생활비 + 높은 만족도.', watch: '의료·교통 접근성을 미리 따져봐야 해요.', match: 'monthly', action: '귀촌 전 의료·교통 접근성을 확인하고 텃밭·부업으로 현금흐름을 만드세요.' }
};

// ── 12문항 (각 보기: 유형 점수 arch + 도시 성향 축 ax) ──
// 축: frugal(절약), nature(자연+/도시-), warm(따뜻+/사계절-), medical(의료중요), dom(국내+/해외-)
export const QUESTIONS = [
  { q: '파이어 후, 돈 쓰는 스타일은?', opts: [
    { t: '극단적 절약 — 적게 쓰고 빨리 자유', arch: { lean: 3, coast: 1 }, ax: { frugal: 2 } },
    { t: '딱 필요한 만큼, 균형 있게', arch: { barista: 2, settle: 1, coast: 1 }, ax: { frugal: 0 } },
    { t: '쓸 땐 쓰는 여유로운 삶', arch: { fat: 3 }, ax: { frugal: -2 } } ] },
  { q: '은퇴 후에도 일은?', opts: [
    { t: '완전히 그만두고 쉰다', arch: { fat: 2 }, ax: {} },
    { t: '좋아하는 일로 반일 근로(건강보험·여유 챙기기)', arch: { barista: 3 }, ax: {} },
    { t: '생활비는 일로 벌고, 투자 추가만 멈춘다', arch: { coast: 3 }, ax: {} } ] },
  { q: '살고 싶은 풍경은?', opts: [
    { t: '바다·산 — 자연 속에서', arch: { nature: 4, monthly: 2 }, ax: { nature: 2 } },
    { t: '활기찬 도시', arch: { nomad: 1 }, ax: { nature: -2 } },
    { t: '둘 다 한 시간 거리면 좋아', arch: { settle: 1, barista: 1 }, ax: { nature: 0 } } ] },
  { q: '어디서 살고 싶어?', opts: [
    { t: '지금 살던 동네 그대로', arch: { settle: 3 }, ax: { dom: 2, medical: 1 } },
    { t: '국내 다른 지역으로', arch: { monthly: 3, nature: 2 }, ax: { dom: 1 } },
    { t: '해외로 떠나고 싶다', arch: { nomad: 3 }, ax: { dom: -2 } } ] },
  { q: '선호하는 기후는?', opts: [
    { t: '1년 내내 따뜻한 열대 — 더워도 저렴하면 OK', arch: { nomad: 1 }, ax: { warm: 2, cHot: 2 } },
    { t: '선선·봄 같은 날씨 — 고지대·상춘 기후', arch: { nature: 1 }, ax: { warm: -1, cCool: 2, cMild: 1 } },
    { t: '온화한 지중해성 — 너무 안 덥고 안 추운', arch: { barista: 1 }, ax: { warm: 0, cMild: 2, cCool: 1 } },
    { t: '사계절 뚜렷 — 겨울·눈도 좋아', arch: { settle: 1, nature: 1 }, ax: { warm: -2, cCold: 2 } } ] },
  { q: '의료·병원 접근성은 얼마나 중요해?', opts: [
    { t: '아주 중요 — 큰 병원 가까이', arch: { settle: 2 }, ax: { medical: 2, dom: 1 } },
    { t: '보통이면 충분', arch: { barista: 1 }, ax: { medical: 1 } },
    { t: '덜 중요 — 자유가 우선', arch: { nomad: 2, nature: 1 }, ax: { medical: -1 } } ] },
  { q: '한 달 생활비, 이상적인 수준은?', opts: [
    { t: '150만 원 이하로 단단하게', arch: { lean: 3, nature: 1 }, ax: { frugal: 2 } },
    { t: '200만 원 안팎', arch: { barista: 1, monthly: 1, coast: 1 }, ax: { frugal: 0 } },
    { t: '넉넉하게 300만 원 이상', arch: { fat: 3 }, ax: { frugal: -2 } } ] },
  { q: '새로운 환경에 대한 마음은?', opts: [
    { t: '설렘 — 자꾸 옮겨보고 싶다', arch: { monthly: 3, nomad: 2 }, ax: {} },
    { t: '익숙함이 편하다', arch: { settle: 3 }, ax: { dom: 1, medical: 1 } },
    { t: '거점 두고 가끔 여행', arch: { coast: 2, barista: 1 }, ax: {} } ] },
  { q: '파이어에서 가장 중요한 건?', opts: [
    { t: '최대한 빨리 자유', arch: { lean: 3 }, ax: { frugal: 1 } },
    { t: '일·취미의 균형', arch: { barista: 2 }, ax: {} },
    { t: '삶의 질·여유', arch: { fat: 2 }, ax: { frugal: -1 } },
    { t: '안정·뿌리내림', arch: { settle: 1, nature: 2 }, ax: { dom: 1 } } ] },
  { q: '투자 위험은 어디까지 감당해?', opts: [
    { t: '원금 지키는 게 최우선 — 예적금 위주', arch: { settle: 1, lean: 1 }, ax: {} },
    { t: '출렁여도 장기 우상향을 믿는다', arch: { coast: 2, barista: 1 }, ax: {} },
    { t: '공격적으로 굴려 빠르게 키운다', arch: { fat: 1, nomad: 2 }, ax: {} } ] },
  { q: '함께 살거나 부양할 가족은?', opts: [
    { t: '혼자 — 가볍게 움직인다', arch: { nomad: 2, monthly: 1, lean: 1 }, ax: { dom: -1 } },
    { t: '배우자와 둘이', arch: { barista: 1, coast: 2 }, ax: {} },
    { t: '아이·부모 등 부양 책임이 있다', arch: { fat: 2, settle: 1 }, ax: { medical: 1, dom: 1 } } ] },
  { q: '주말마다 가고 싶은 곳은?', opts: [
    { t: '해변·바다 곁', arch: { monthly: 2 }, ax: { warm: 1, cHot: 1, nature: 1 } },
    { t: '산·고지대 숲', arch: { nature: 3 }, ax: { cCool: 2, cMild: 1, nature: 1 } },
    { t: '도심 한복판', arch: { nomad: 1 }, ax: { nature: -2 } } ] }
];

const clamp01 = (x) => Math.max(0, Math.min(1, x));

// 답변 인덱스 배열 → { archetype, axes }
export function scoreAnswers(answers) {
  const arch = {}; const ax = { frugal: 0, nature: 0, warm: 0, medical: 0, dom: 0, cHot: 0, cMild: 0, cCool: 0, cCold: 0 };
  Object.keys(ARCHETYPES).forEach((k) => { arch[k] = 0; });
  answers.forEach((ai, qi) => {
    const opt = QUESTIONS[qi] && QUESTIONS[qi].opts[ai];
    if (!opt) return;
    if (opt.arch) for (const k in opt.arch) arch[k] += opt.arch[k];
    if (opt.ax) for (const k in opt.ax) ax[k] += opt.ax[k];
  });
  let top = 'barista'; let best = -1;
  for (const k in arch) { if (arch[k] > best) { best = arch[k]; top = k; } }
  return { archetype: ARCHETYPES[top], archScores: arch, axes: ax };
}

// 도시 파이어 적합도(0~100) + 분해. simulation 있으면 비용적합도에 실제 계산 반영.
export function scoreCity(city, axes, simulation, buildScenario) {
  const kMin = 1250000; const kMax = 3800000;
  const cheap = clamp01(1 - (city.krw - kMin) / (kMax - kMin));
  const frugalW = clamp01(0.5 + axes.frugal * 0.18);
  let costFit = cheap * (0.6 + frugalW * 0.4);
  let fireAge = null;
  if (simulation && buildScenario) {
    try {
      const sc = buildScenario(simulation.inputs, { monthlyLivingCost: city.krw });
      fireAge = sc.earliestRetirementAge || null;
      const base = simulation.earliestRetirementAge;
      if (fireAge && base) costFit = clamp01(costFit + Math.max(-0.15, Math.min(0.2, (base - fireAge) * 0.03)));
    } catch { /* ignore */ }
  }
  const natureUser = clamp01(0.5 + axes.nature * 0.2);
  const natureFit = 1 - Math.abs(city.nature - natureUser);
  const warmUser = clamp01(0.5 + axes.warm * 0.2);
  const warmFit = 1 - Math.abs(city.warm - warmUser);
  // 기후 선호(열대/온화/선선/사계절) ↔ 도시 기후 태그 매칭 (additive). 선호 없으면 중립(0.6).
  const cw = { hot: axes.cHot || 0, mild: axes.cMild || 0, cool: axes.cCool || 0, cold: axes.cCold || 0 };
  const cMax = Math.max(cw.hot, cw.mild, cw.cool, cw.cold);
  const climateFit = cMax > 0 ? clamp01((cw[city.climate] || 0) / cMax) : 0.6;
  const medicalFit = city.medical * clamp01(0.4 + axes.medical * 0.22);
  const domWant = axes.dom;
  const domFit = domWant === 0 ? 0.6 : (city.dom === (domWant > 0) ? 1 : 0.25);
  const raw = costFit * 0.30 + climateFit * 0.18 + natureFit * 0.14 + warmFit * 0.04 + medicalFit * 0.14 + domFit * 0.20;
  const score = Math.round(clamp01(raw) * 100);
  return { score, fireAge, parts: { 비용: Math.round(costFit * 100), 자연: Math.round(natureFit * 100), 기후: Math.round(climateFit * 100), 의료: Math.round(medicalFit * 100), 지역: Math.round(domFit * 100) } };
}

export function recommendCities(axes, simulation, buildScenario, n = 3) {
  return TEST_CITIES
    .map((c) => ({ city: c, ...scoreCity(c, axes, simulation, buildScenario) }))
    .sort((a, b) => b.score - a.score)
    .slice(0, n);
}
