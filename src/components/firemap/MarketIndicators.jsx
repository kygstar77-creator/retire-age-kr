import { useEffect, useState } from 'react';

// 살아있는 참고 지표 — firemap_market / fm_macro_latest / fm_realestate_latest 실데이터.
// 매일(시장)·매주(거시·부동산) 자동 수집된 값을 그대로 보여줘요. 데이터 없으면 조용히 숨김.
const SB = ['https://cvhskxdwqubmshdgkzhj', 'supabase', 'co'].join('.');
const KEY = ['sb', 'publishable', 'uhbAVqCA8JrJNXqaAcft9g', 'yYtwgct9'].join('_');
const rpc = (fn) => fetch(`${SB}/rest/v1/rpc/${fn}`, { method: 'POST', headers: { apikey: KEY, authorization: `Bearer ${KEY}`, 'content-type': 'application/json' }, body: '{}' }).then((r) => (r.ok ? r.json() : null)).catch(() => null);
const eok = (manwon) => { const m = Math.round(Number(manwon) || 0); return m >= 10000 ? `${(m / 10000).toFixed(1)}억` : `${m.toLocaleString()}만원`; };
const pf = (p) => { const s = String(p || ''); return s.length === 6 ? `${s.slice(0, 4)}.${s.slice(4)}` : s; };

export default function MarketIndicators({ region = '서울' }) {
  const [m, setM] = useState(null);
  const [macro, setMacro] = useState(null);
  const [re, setRe] = useState(null);
  useEffect(() => {
    let a = true;
    Promise.all([rpc('fm_market_latest'), rpc('fm_macro_latest'), rpc('fm_realestate_latest')]).then(([mk, mc, r]) => {
      if (!a) return;
      setM(Array.isArray(mk) ? mk : null);
      setMacro(mc && typeof mc === 'object' ? mc : null);
      setRe(Array.isArray(r) ? r : null);
    });
    return () => { a = false; };
  }, []);

  const spx = m && m.find((x) => x.symbol === '^spx');
  const fx = m && m.find((x) => x.symbol === 'usdkrw');
  const cpi = macro && macro.cpi;
  const rates = (macro && macro.rates) || [];
  const base = rates.find((r) => r.key === 'base_rate');
  const dep = rates.find((r) => r.key === 'deposit_12m' && r.source !== 'worldbank'); // 연간 평균(전년도)은 비노출
  const sale = re && re.find((r) => r.region === region && r.deal_type === 'sale');
  const jeonse = re && re.find((r) => r.region === region && r.deal_type === 'jeonse');

  if (!spx && !cpi && !base && !sale) return null;

  const macroParts = [];
  if (base && base.value != null) macroParts.push(`기준금리 ${base.value}%`);
  if (cpi && cpi.yoy != null) macroParts.push(`물가 상승률 ${cpi.yoy}%${cpi.period ? `(${pf(cpi.period)})` : ''}`);
  if (dep && dep.value != null) macroParts.push(`예금금리 ${dep.value}%`);
  const reParts = [];
  if (sale && sale.value != null) reParts.push(`매매 ${eok(sale.value)}`);
  if (jeonse && jeonse.value != null) reParts.push(`전세 ${eok(jeonse.value)}`);
  const rePeriod = pf((sale && sale.period) || (jeonse && jeonse.period) || '');

  return (
    <section className="fm-card" style={S.card}>
      <div style={S.head}>
        <span style={S.kicker}>📊 오늘의 참고 지표</span>
        <span style={S.auto}>자동 업데이트</span>
      </div>
      {spx && <p style={S.line}>📈 <b>S&P500</b> 주간 <b style={{ color: spx.ret_7d >= 0 ? '#0f6e56' : '#e8431c' }}>{spx.ret_7d > 0 ? '+' : ''}{spx.ret_7d}%</b>{fx ? <> · 환율 1USD≈<b>{Math.round(Number(fx.level)).toLocaleString()}원</b></> : null}</p>}
      {macroParts.length > 0 && <p style={S.line}>🇰🇷 <b>거시지표</b> — {macroParts.join(' · ')}</p>}
      {reParts.length > 0 && <p style={S.line}>🏠 <b>{region} 아파트 실거래</b> — {reParts.join(' · ')}{rePeriod ? <span style={S.sub}> ({rePeriod})</span> : null}</p>}
      <p style={S.note}>한국은행·World Bank·국토부 실거래가 기반 · 시장은 매일, 거시·부동산은 매주 자동 갱신돼요. (정보 제공용 참고치)</p>
    </section>
  );
}

const S = {
  card: { borderColor: 'rgba(30,40,89,0.14)' },
  head: { display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 10 },
  kicker: { fontSize: 13, fontWeight: 800, color: '#1e2859', letterSpacing: '-0.01em' },
  auto: { fontSize: 10.5, fontWeight: 800, color: '#0f6e56', background: 'rgba(16,185,129,0.10)', borderRadius: 999, padding: '3px 8px' },
  line: { fontSize: 13, color: '#15151b', fontWeight: 600, lineHeight: 1.5, margin: '0 0 8px' },
  sub: { fontSize: 11, color: '#9aa3bf', fontWeight: 600 },
  note: { fontSize: 10.5, color: '#9aa3bf', lineHeight: 1.5, margin: '4px 0 0' }
};
