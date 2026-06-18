import { useEffect, useState } from 'react';
import { funHandle } from '../../firemap-v2/funName.js';
import { wonStr } from '../../firemap-v2/dailyData.js';
import { presencePing, fetchLivePresence, fetchTotalCalc } from '../../utils/live.js';

const SB_URL = ['https://cvhskxdwqubmshdgkzhj', 'supabase', 'co'].join('.');
const SB_KEY = ['sb', 'publishable', 'uhbAVqCA8JrJNXqaAcft9g', 'yYtwgct9'].join('_');
const rpc = (fn) => fetch(`${SB_URL}/rest/v1/rpc/${fn}`, { method: 'POST', headers: { apikey: SB_KEY, authorization: `Bearer ${SB_KEY}`, 'content-type': 'application/json' }, body: '{}' }).then((r) => (r.ok ? r.json() : null)).catch(() => null);
const eok = (manwon) => { const m = Math.round(Number(manwon) || 0); return m >= 10000 ? `${(m / 10000).toFixed(1)}억` : `${m.toLocaleString()}만원`; };
// 저축 기록 경과시간 — '방금'은 정말 최근(3분 이내)만, 오래된 건(3일 초과) 표시 안 함
const relSave = (ts) => {
  const t = ts ? new Date(ts).getTime() : 0;
  if (!t) return null;
  const min = Math.floor((Date.now() - t) / 60000);
  if (min < 3) return '방금';
  if (min < 60) return `${min}분 전`;
  const hr = Math.floor(min / 60);
  if (hr < 24) return `${hr}시간 전`;
  const day = Math.floor(hr / 24);
  if (day <= 3) return day === 1 ? '어제' : `${day}일 전`;
  return null;
};

const STYLE = `
.fm-livebar{position:sticky;top:0;z-index:60;width:100%;height:30px;background:#10151c;color:#fff;overflow:hidden;display:flex;align-items:center}
.fm-topbar{top:30px !important}
.fm-livebar-row{display:inline-flex;gap:26px;white-space:nowrap;padding-left:16px;animation:fmLiveScroll 42s linear infinite;will-change:transform}
.fm-livebar-row span{font-size:12.5px;font-weight:600;opacity:.96}
@keyframes fmLiveScroll{from{transform:translateX(0)}to{transform:translateX(-50%)}}
`;

function buildItems({ online, names, recent, total, market, macro, re, calc }) {
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
  // 최근 활동 — 계산·저축·절약 (실데이터, 경과시간 표기)
  (calc || []).slice(0, 4).forEach((c) => {
    const rel = relSave(c.created_at);
    if (!rel) return;
    const nm = (c.nickname && c.nickname.trim()) || funHandle(c.client_id || '');
    items.push(c.earliest_age ? `🧮 ${nm}님이 ${rel} 파이어 나이 계산 — ${c.earliest_age}세` : `🧮 ${nm}님이 ${rel} 파이어 나이 계산`);
  });
  (recent || []).slice(0, 5).forEach((s) => {
    const rel = relSave(s.updated_at);
    if (!rel) return; // 너무 오래된 기록은 활동으로 표시하지 않음
    const nm = (s.nickname && s.nickname.trim()) || funHandle(s.client_id || '');
    if (s.today_saved > 0) items.push(`💰 ${nm}님이 ${rel} ${wonStr(s.today_saved)} 절약`);
    else if (s.deposit_month > 0) items.push(`🏦 ${nm}님이 ${rel} 저축 기록을 남겼어요`);
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
      const H = { apikey: SB_KEY, authorization: `Bearer ${SB_KEY}` };
      const recentAct = fetch(`${SB_URL}/rest/v1/firemap_save_events?select=client_id,nickname,today_saved,deposit_month,updated_at&or=(today_saved.gt.0,deposit_month.gt.0)&order=updated_at.desc&limit=8`, { headers: H }).then((r) => (r.ok ? r.json() : [])).catch(() => []);
      const recentCalc = fetch(`${SB_URL}/rest/v1/firemap_scores?select=client_id,nickname,earliest_age,created_at&order=created_at.desc&limit=8`, { headers: H }).then((r) => (r.ok ? r.json() : [])).catch(() => []);
      const [p, recent, total, market, macro, re, calc] = await Promise.all([
        fetchLivePresence(),
        recentAct,
        fetchTotalCalc(),
        rpc('fm_market_latest'),
        rpc('fm_macro_latest'),
        rpc('fm_realestate_latest'),
        recentCalc
      ]);
      if (!alive) return;
      setItems(buildItems({ online: p ? p.online : 0, names: p ? p.names : [], recent, total, market, macro, re, calc }));
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
