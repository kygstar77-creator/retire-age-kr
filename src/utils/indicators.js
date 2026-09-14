// 참고 지표 한 벌 — 코스피·S&P500·환율·기준금리·예금금리·물가·서울 아파트 매매·전세·월세.
// 소식 화면(목록·상단 한 줄)과 결과 화면의 위젯 카드가 같은 값·같은 줄을 쓰도록 로더와 줄 만들기를 한 곳에 둔다.
// 지표는 참고용이고 파이어 나이 계산에는 쓰지 않는다.
import { sbRpc } from './supabaseClient.js';

const num = (v) => (v == null || Number.isNaN(Number(v)) ? null : Number(v));

const EMPTY = { fx: null, kospi: null, spx: null, baseRate: null, deposit: null, cpi: null, seoulSale: null, seoulJeonse: null, seoulRentDeposit: null, seoulRent: null };

export async function fetchIndicators() {
  try {
    const [m, macro, re] = await Promise.all([sbRpc('fm_market_latest'), sbRpc('fm_macro_latest'), sbRpc('fm_realestate_latest')]);
    const mk = Array.isArray(m) ? m : [];
    const find = (sym) => mk.find((x) => x && x.symbol === sym) || null;
    const rates = (macro && Array.isArray(macro.rates)) ? macro.rates : [];
    const rate = (key) => rates.find((r) => r && r.key === key) || null;
    const rows = Array.isArray(re) ? re : [];
    const seoul = (deal, metric) => rows.find((r) => r && r.region === '서울' && r.deal_type === deal && r.metric === metric) || null;
    return {
      fx: find('usdkrw'),
      kospi: find('^kospi'),
      spx: find('^spx'),
      baseRate: rate('base_rate'),
      deposit: rate('deposit_12m'),
      cpi: (macro && macro.cpi) || null,
      seoulSale: seoul('sale', 'avg_price'),
      seoulJeonse: seoul('jeonse', 'avg_deposit'),
      seoulRentDeposit: seoul('rent', 'avg_deposit'),
      seoulRent: seoul('rent', 'avg_rent')
    };
  } catch {
    return { ...EMPTY };
  }
}

// 화면에 바로 쓰는 짧은 문자열 — 값이 없으면 null을 돌려주고 호출부가 숨긴다.
export const fxText = (fx) => (fx && num(fx.level) != null ? `${Math.round(num(fx.level)).toLocaleString('ko-KR')}원` : null);
export const rateText = (r) => (r && num(r.value) != null ? `${Number(r.value).toFixed(2).replace(/0$/, '')}%` : null);
export const cpiText = (cpi) => (cpi && num(cpi.yoy) != null ? `${Number(cpi.yoy).toFixed(1)}%` : null);

const pct1 = (v) => (num(v) == null ? null : `${Number(v) > 0 ? '+' : ''}${Number(v).toFixed(1)}%`);
const num0 = (v) => Math.round(Number(v)).toLocaleString('ko-KR');
// '202608' → '2026년 8월' · '2025' → '2025년'
export const periodText = (p) => {
  const s = String(p || '');
  if (s.length === 6) return `${s.slice(0, 4)}년 ${Number(s.slice(4))}월`;
  if (s.length === 4) return `${s}년`;
  return s;
};
// 만원 → '12.9억' / '9,500만원'
export const manwonText = (v) => { const m = Math.round(num(v) || 0); return m >= 10000 ? `${(m / 10000).toFixed(1)}억` : `${m.toLocaleString('ko-KR')}만원`; };

// 목록(IndexRow)과 한 줄(Ticker)이 같이 쓰는 줄 — [{ key, label, sub, value, unit, delta, deltaLabel }]
export function buildIndicatorRows(ind) {
  if (!ind) return [];
  const rows = [];
  const idx = (key, label, r) => {
    if (!r || num(r.level) == null) return;
    const d1 = pct1(r.ret_1d); const d7 = pct1(r.ret_7d);
    rows.push({ key, label, value: num0(r.level), delta: d1 || d7, deltaLabel: d1 ? '어제보다' : (d7 ? '이번 주' : null) });
  };
  idx('kospi', '코스피', ind.kospi);
  idx('spx', 'S&P500', ind.spx);
  const fx = ind.fx;
  if (fx && num(fx.level) != null) rows.push({ key: 'fx', label: '환율', sub: '1달러', value: num0(fx.level), unit: '원', delta: pct1(fx.ret_1d) || pct1(fx.ret_7d), deltaLabel: fx.ret_1d != null ? '어제보다' : (fx.ret_7d != null ? '이번 주' : null) });
  const pctRow = (key, label, r) => { if (r && num(r.value) != null) rows.push({ key, label, sub: r.as_of ? periodText(r.as_of) : null, value: Number(r.value).toFixed(2).replace(/0$/, ''), unit: '%' }); };
  pctRow('base', '기준금리', ind.baseRate);
  pctRow('deposit', '예금금리', ind.deposit);
  const cpi = ind.cpi;
  if (cpi && num(cpi.yoy) != null) rows.push({ key: 'cpi', label: '물가', sub: cpi.period ? periodText(cpi.period) : '1년 전보다', value: Number(cpi.yoy).toFixed(1), unit: '%' });
  const reRow = (key, label, r) => { if (r && num(r.value) != null) rows.push({ key, label, sub: r.period ? periodText(r.period) : null, value: manwonText(r.value) }); };
  reRow('seoulSale', '서울 아파트 매매', ind.seoulSale);
  reRow('seoulJeonse', '서울 아파트 전세', ind.seoulJeonse);
  if (ind.seoulRent && num(ind.seoulRent.value) != null) {
    const dep = ind.seoulRentDeposit && num(ind.seoulRentDeposit.value) != null ? `${manwonText(ind.seoulRentDeposit.value)} · ` : '';
    rows.push({ key: 'seoulRent', label: '서울 아파트 월세', sub: ind.seoulRent.period ? periodText(ind.seoulRent.period) : null, value: `${dep}월 ${manwonText(ind.seoulRent.value)}` });
  }
  return rows;
}
