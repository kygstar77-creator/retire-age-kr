import { useEffect, useState } from 'react';
import { funHandle } from '../../firemap-v2/funName.js';
import { wonStr } from '../../firemap-v2/dailyData.js';
import { todayTip, todayAction } from '../../firemap-v2/journeyDaily.js';
import { presencePing, fetchLivePresence, fetchRecentSaves, fetchTotalCalc } from '../../utils/live.js';

const SB_URL = ['https://cvhskxdwqubmshdgkzhj', 'supabase', 'co'].join('.');
const SB_KEY = ['sb', 'publishable', 'uhbAVqCA8JrJNXqaAcft9g', 'yYtwgct9'].join('_');

const STYLE = `
.fm-livebar{position:sticky;top:0;z-index:60;width:100%;height:30px;background:#10151c;color:#fff;overflow:hidden;display:flex;align-items:center}
.fm-topbar{top:30px !important}
.fm-livebar-row{display:inline-flex;gap:26px;white-space:nowrap;padding-left:16px;animation:fmLiveScroll 42s linear infinite;will-change:transform}
.fm-livebar-row span{font-size:12.5px;font-weight:600;opacity:.96}
@keyframes fmLiveScroll{from{transform:translateX(0)}to{transform:translateX(-50%)}}
`;

function buildItems({ online, names, recent, total, market }) {
  const items = [];
  // 살아있는 시장 — firemap_market 실데이터
  if (market) {
    const spx = market.find((m) => m.symbol === '^spx');
    if (spx && spx.ret_7d != null) items.push(`📈 이번 주 S&P500 ${spx.ret_7d > 0 ? '+' : ''}${spx.ret_7d}% — 시장이 내 파이어를 움직여요`);
  }
  // 오늘의 한 걸음 + 오늘의 파이어 지식 (매일 바뀜)
  try { const a = todayAction(); if (a && a.label) items.push(`${a.ico || '☀️'} 오늘의 한 걸음 · ${a.label}`); } catch { /* ignore */ }
  try { const t = todayTip(); if (t) items.push(`💡 ${t}`); } catch { /* ignore */ }
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
      const [p, recent, total, market] = await Promise.all([
        fetchLivePresence(),
        fetchRecentSaves(8),
        fetchTotalCalc(),
        fetch(`${SB_URL}/rest/v1/rpc/fm_market_latest`, { method: 'POST', headers: { apikey: SB_KEY, authorization: `Bearer ${SB_KEY}`, 'content-type': 'application/json' }, body: '{}' }).then((r) => (r.ok ? r.json() : null)).catch(() => null)
      ]);
      if (!alive) return;
      setItems(buildItems({ online: p ? p.online : 0, names: p ? p.names : [], recent, total, market }));
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
