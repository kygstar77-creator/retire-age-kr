// 참고 지표 한 벌 — 환율·기준금리·물가·코스피·S&P500.
// 소식 화면과 결과 화면의 위젯 카드가 같은 값을 쓰도록 로더를 한 곳에 둔다.
// 지표는 참고용이고 파이어 나이 계산에는 쓰지 않는다.
import { sbRpc } from './supabaseClient.js';

const num = (v) => (v == null || Number.isNaN(Number(v)) ? null : Number(v));

export async function fetchIndicators() {
  try {
    const [m, macro] = await Promise.all([sbRpc('fm_market_latest'), sbRpc('fm_macro_latest')]);
    const mk = Array.isArray(m) ? m : [];
    const find = (sym) => mk.find((x) => x && x.symbol === sym) || null;
    const rates = (macro && Array.isArray(macro.rates)) ? macro.rates : [];
    const rate = (key) => rates.find((r) => r && r.key === key) || null;
    return {
      fx: find('usdkrw'),
      kospi: find('^kospi'),
      spx: find('^spx'),
      baseRate: rate('base_rate'),
      deposit: rate('deposit_12m'),
      cpi: (macro && macro.cpi) || null
    };
  } catch {
    return { fx: null, kospi: null, spx: null, baseRate: null, deposit: null, cpi: null };
  }
}

// 화면에 바로 쓰는 짧은 문자열 — 값이 없으면 null을 돌려주고 호출부가 숨긴다.
export const fxText = (fx) => (fx && num(fx.level) != null ? `${Math.round(num(fx.level)).toLocaleString('ko-KR')}원` : null);
export const rateText = (r) => (r && num(r.value) != null ? `${Number(r.value).toFixed(2).replace(/0$/, '')}%` : null);
export const cpiText = (cpi) => (cpi && num(cpi.yoy) != null ? `${Number(cpi.yoy).toFixed(1)}%` : null);
