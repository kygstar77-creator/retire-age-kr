// 말하는 숫자 / 화면 숫자 나누기(2026-10-03 cloud yt-quality 시제품 — 순수 함수, node --test로 시험).
// 문제: 우리 대본 숫자 밀도가 경쟁의 3.6배(1,000단어당 187 vs 52, speechcompare.py). 숫자를 빼면 정확도가 떨어진다.
// 그래서 말은 반올림한 숫자 하나(유효숫자 2자리), 정확한 값은 화면 꼬리표로 남긴다(cloud-prompts ① "정확한 값은 [자막] 표시로").
// 사실표 값은 show에 그대로 남고, say는 대본·자막 쪽에서 쓴다. 다른 파일을 import하지 않는다.

export type SpokenNumber = {say: string; show: string; rounded: boolean};

const sig2 = (v: number) => {
  if (v === 0) return 0;
  const e = Math.floor(Math.log10(Math.abs(v))) - 1;
  const p = Math.pow(10, e);
  return p >= 1 ? Math.round(Math.round(v / p) * p) : Math.round(v / p) * p;
};

// 1만 아래 덩어리(0~9999)를 말하듯: 6000 → 6천, 4600 → 4천6백, 120 → 120
const chunk = (n: number) => {
  if (n >= 1000 && n % 100 === 0) { const th = Math.floor(n / 1000), h = (n % 1000) / 100; return `${th}천${h ? `${h}백` : ''}`; }
  return n.toLocaleString('en-US');
};

const units: [number, string][] = [[1e12, '조'], [1e8, '억'], [1e4, '만'], [1, '']];

// 말하는 원: 324,567,000 → '약 3억 2천만 원'
export const speakWon = (won: number): SpokenNumber => {
  const r = Math.abs(won) < 1e4 ? Math.round(won / 100) * 100 || Math.round(won) : sig2(won);
  const a = Math.abs(r); const parts: string[] = [];
  let rest = a;
  for (const [u, name] of units) { const q = Math.floor(rest / u); rest -= q * u; if (q) parts.push(`${chunk(q)}${name}`); }
  const body = (r < 0 ? '−' : '') + (parts.join(' ') || '0');
  const rounded = r !== won;
  return {say: `${rounded ? '약 ' : ''}${body} 원`, show: wonExact(won), rounded};
};

// 화면 원(정확): 324,567,000 → '3억 2,456만 7,000원'
export const wonExact = (won: number): string => {
  const a = Math.round(Math.abs(won)); const parts: string[] = []; let rest = a;
  for (const [u, name] of units) { const q = Math.floor(rest / u); rest -= q * u; if (q) parts.push(`${q.toLocaleString('en-US')}${name}`); }
  return (won < 0 ? '−' : '') + (parts.join(' ') || '0') + '원';
};

// 말하는 %: 10 이상은 정수, 10 아래는 소수 한 자리(.0은 뺀다). show는 사실표 자릿수(digits) 그대로.
export const speakPct = (v: number, digits = 1): SpokenNumber => {
  const r = Math.abs(v) >= 10 ? Math.round(v) : Math.round(v * 10) / 10;
  const say = `${r < 0 ? '−' : ''}${Math.abs(r).toString()}%`;
  const show = `${v < 0 ? '−' : ''}${Math.abs(v).toFixed(digits)}%`;
  const rounded = Math.abs(r - v) > 1e-9;
  return {say: `${rounded ? '약 ' : ''}${say}`, show, rounded};
};

// 대본 한 문장에 든 숫자 덩어리 수(콤마·소수점 포함 한 덩어리) — 한 문장 숫자 1개 이하 확인용
export const numbersInSentence = (s: string): number => (s.match(/\d[\d,.]*/g) || []).length;
