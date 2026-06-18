import { useEffect, useState } from 'react';
import { funHandle } from '../../firemap-v2/funName.js';
import { wonStr } from '../../firemap-v2/dailyData.js';
import { presencePing, fetchLivePresence, fetchRecentSaves, fetchTotalCalc } from '../../utils/live.js';

const SB_URL = ['https://cvhskxdwqubmshdgkzhj', 'supabase', 'co'].join('.');
const SB_KEY = ['sb', 'publishable', 'uhbAVqCA8JrJNXqaAcft9g', 'yYtwgct9'].join('_');
const rpc = (fn) => fetch(`${SB_URL}/rest/v1/rpc/${fn}`, { method: 'POST', headers: { apikey: SB_KEY, authorization: `Bearer ${SB_KEY}`, 'content-type': 'application/json' }, body: '{}' }).then((r) => (r.ok ? r.json() : null)).catch(() => null);
const eok = (manwon) => { const m = Math.round(Number(manwon) || 0); return m >= 10000 ? `${(m / 10000).toFixed(1)}억` : `${m.toLocaleString()}만원`; };

const STYLE = `
.fm-livebar{position:sticky;top:0;z-index:60;width:100%;height:30px;background:#10151c;color:#fff;overflow:hidden;display:flex;align-items:center}
.fm-topbar{top:30px !important}
.fm-livebar-row{display:inline-flex;gap:26px;white-space:nowrap;padding-left:16px;animation:fmLiveScroll 42s linear infinite;will-change:transform}
.fm-livebar-row span{font-size:12.5px;font-weight:600;opacity:.96}
@keyframes fmLiveScroll{from{transform:translateX(0)}to{transform:translateX(-50%)}}
`;

function buildItems({ online, names, recent, total, market, macro, re }) {
  const items = [];
  // 참고 지표 — 시장(매일)·거시(매주)·부동산(매주) 실데이터 자동 갱신
  if (market) {
    const spx = market.find((m) => m.symbol === '^spx');
    const fx = market.find((m) => m.symbol === 'usdkrw');
    const kospi = market.find((m) => m.symbol === '^kospi');
    if (spx && spx.ret_7d != null) items.push(`📈 S&P500 주간 ${spx.ret_7d > 0 ? '+' : ''}${spx.ret_7d}%${fx && fx.level != null ? ` · 환율 1USD≈${Math.round(Number(fx.level)).toLocaleString()}원` : ''}`);
    if (kospi && kospi.ret_7d != null) items.push(`📊 코스피 주간 ${kospi.ret_7d > 0 ? '+' : ''}${kospi.ret_7d}%`);
  }
  if (macro) {
    const rates = macro.rates || [];
    const base = rates.find((r) => r.key === 'base_rate');
    const dep = rates.find((r) => r.key === 'deposit_12m');
    const cpi = macro.cpi;
    const parts = [];
    if (base && base.value != null) parts.push(`기준금리 ${base.value}%`);
    if (cpi && cpi.yoy != null) parts.push(`물가 ${cpi.yoy}%`);
    if (dep && dep.value != null) parts.push(`예금금리 ${dep.value}%`);
    if (parts.length) items.push(`🇰🇷 ${parts.join(' · ')}`);
  }
  if (re) {
    const sale = re.find((r) => r.region === '서울' && r.deal_type === 'sale');
    const jeonse = re.find((r) => r.region === '서울' && r.deal_type === 'jeonse');
    const parts = [];
    if (sale && sale.value != null) parts.push(`매매 ${eok(sale.value)}`);
    if (jeonse && jeonse.value != null) parts.push(`전세 ${eok(jeonse.value)}`);
    if (parts.length) items.push(`🏠 서울 아파트 ${parts.join(' · ')}`);
  }
  // 또래 규모 (실데이터)
  if (total > 0) items.push(`🔥 지금까지 ${total.toLocaleString()}명이 파이어 나이를 계산했어요`);
  if (online >= 2) items.push(`🟢 지금 ${online}명이 함께 파이어를 그리는 중`);
  // 최근 저축 (실데이터)
  (recent || []).slice(0, 5).forEach((s) => {
    const nm = (s.nickname && s.nickname.trim()) || funHandle(s.client_id || '');
    items.push(`💰 ${nm}님이 방금 ${wonStr(s.today_saved)} 저축`);
  });
  (names || []).slice(0, 3).forEach((n) => { if (n) items.push(`👋 ${n}님 접속 중`); });
  if (!items.length) items.push('🔥 오늘의 작은 저축 하나가 파이어를 며칠 당겨요');
  return items;
}

export default function LiveBanner() {
  const [items, setItems] = useState([]);
  useEffect(() => {
    let alive = true;
    const load = async () => {
      const [p, recent, total, market, macro, re] = await Promise.all([
        fetchLivePresence(),
        fetchRecentSaves(8),
        fetchTotalCalc(),
        rpc('fm_market_latest'),
        rpc('fm_macro_latest'),
        rpc('fm_realestate_latest')
      ]);
      if (!alive) return;
      setItems(buildItems({ online: p ? p.online : 0, names: p ? p.names : [], recent, total, market, macro, re }));
    };
    presencePing();
    load();
    const ping = setInterval(presencePing, 45000);
    const refresh = setInterval(load, 40000);
    return () => { alive = false; clearInterval(ping); clearInterval(refresh); };
  }, []);
  if (!items.length) return null;
  const row = [...items, ...items];
  return (
    <div className='fm-livebar' aria-label='실시간 현황'>
      <style>{STYLE}</style>
      <div className='fm-livebar-row'>
        {row.map((t, i) => <span key={i}>{t}</span>)}
      </div>
    </div>
  );
}
