// 데이터 출처/기준일 단일 레지스트리 (#15). #3·#4·#17이 공통 참조.
// 정밀 수치/주기 갱신은 refreshPlanned 항목을 데이터 파이프라인에서 보정.
export const DATA_SOURCES = {
  netWorthStats: { label: '순자산 분포', source: '통계청 가계금융복지조사', asOf: '2025', note: '또래 상위 % 추정 기준', approximate: true },
  returnPresets: { label: '투자 수익률 가정', source: '주요 지수 장기 역사적 평균 기반 가정', asOf: '2026', note: '과거 수익률은 보장값이 아니며 투자 권유가 아닙니다' },
  taxRules: { label: '세제·사회보험', source: '현행 세법·국민건강보험 제도', asOf: '2026', note: '제도 변경 시 결과가 달라질 수 있어요' },
  cityCost: { label: '도시 생활비', source: '1인 월 생활비 참고 추정치', asOf: '2026', note: '주거·의료·환율·비자에 따라 달라질 수 있어요', refreshPlanned: true },
  fx: { label: '환율 가정', source: '기준 환율 가정', asOf: '2026', note: '실제 환율 변동 미반영', refreshPlanned: true }
};

export function sourceLine(key) {
  const s = DATA_SOURCES[key];
  return s ? `출처: ${s.source} · 기준 ${s.asOf}` : '';
}
