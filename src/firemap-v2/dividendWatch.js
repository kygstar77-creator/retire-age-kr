// 배당 관심 종목 — 배당락(이 날 전에 사야 배당을 받는 날) 예상 규칙표. 전부 '예상'이에요.
// 미국 ETF 실제 배당락은 supabase fetch-dividends(Yahoo events=div)로만 확정. 국내 ETF 분배금은 공식 소스가 없어 예상만 표기.
// 규칙: months(배당락이 있는 달) · day(숫자 또는 'last'=그달 말일) · expected(항상 true).

const ALL = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12];
const Q_US = [3, 6, 9, 12];
const Q_KR = [1, 4, 7, 10];

export const DIVIDEND_WATCH = [
  { symbol: 'SCHD', name: 'SCHD', market: 'US', freq: 'quarterly', months: Q_US, day: 20, expected: true },
  { symbol: 'JEPI', name: 'JEPI', market: 'US', freq: 'monthly', months: ALL, day: 1, expected: true },
  { symbol: 'JEPQ', name: 'JEPQ', market: 'US', freq: 'monthly', months: ALL, day: 1, expected: true },
  { symbol: 'VYM', name: 'VYM', market: 'US', freq: 'quarterly', months: Q_US, day: 21, expected: true },
  { symbol: 'O', name: '리얼티인컴 O', market: 'US', freq: 'monthly', months: ALL, day: 1, expected: true },
  { symbol: 'VTI', name: 'VTI', market: 'US', freq: 'quarterly', months: Q_US, day: 24, expected: true },
  { symbol: 'QQQ', name: 'QQQ', market: 'US', freq: 'quarterly', months: Q_US, day: 22, expected: true },
  { symbol: 'VOO', name: 'VOO', market: 'US', freq: 'quarterly', months: Q_US, day: 26, expected: true },
  { symbol: '458730', name: 'TIGER 미국배당다우존스', market: 'KR', freq: 'monthly', months: ALL, day: 'last', expected: true },
  { symbol: '402970', name: 'ACE 미국배당다우존스', market: 'KR', freq: 'monthly', months: ALL, day: 'last', expected: true },
  { symbol: '446720', name: 'SOL 미국배당다우존스', market: 'KR', freq: 'monthly', months: ALL, day: 15, expected: true },
  { symbol: '069500', name: 'KODEX 200', market: 'KR', freq: 'quarterly', months: Q_KR, day: 'last', expected: true },
  { symbol: '360750', name: 'TIGER 미국S&P500', market: 'KR', freq: 'quarterly', months: Q_KR, day: 'last', expected: true }
];

export const lastDayOf = (year, month) => new Date(year, month, 0).getDate(); // month: 1~12

// 해당 연·월의 예상 배당락 목록 [{ symbol, name, market, day, expected }] — 날짜순
export function expectedExDates(year, month) {
  const last = lastDayOf(year, month);
  return DIVIDEND_WATCH
    .filter((w) => w.months.includes(month))
    .map((w) => ({ symbol: w.symbol, name: w.name, market: w.market, freq: w.freq, day: w.day === 'last' ? last : Math.min(last, w.day), expected: true }))
    .sort((a, b) => a.day - b.day || a.name.localeCompare(b.name));
}

// 배당률 예시(참고치) — 칩용
export const YIELD_PRESETS = [
  { label: 'S&P500', value: 1.3 },
  { label: 'SCHD', value: 3.7 },
  { label: '한국 고배당', value: 5.0 },
  { label: 'JEPI', value: 8.4 }
];
