import { useEffect, useState } from 'react';
import { funHandle } from '../../firemap-v2/funName.js';
import { wonStr } from '../../firemap-v2/dailyData.js';
import { presencePing, fetchLivePresence, fetchRecentSaves, fetchTotalCalc } from '../../utils/live.js';

const STYLE = `
.fm-livebar{position:relative;width:100%;height:30px;background:#10151c;color:#fff;overflow:hidden;display:flex;align-items:center}
.fm-livebar-row{display:inline-flex;gap:26px;white-space:nowrap;padding-left:16px;animation:fmLiveScroll 36s linear infinite;will-change:transform}
.fm-livebar-row span{font-size:12.5px;font-weight:600;opacity:.96}
@keyframes fmLiveScroll{from{transform:translateX(0)}to{transform:translateX(-50%)}}
`;

function buildItems({ online, names, recent, total }) {
  const items = [];
  if (online >= 2) items.push(`🟢 지금 ${online}명이 함께 보고 있어요`);
  if (total > 0) items.push(`🔥 지금까지 ${total.toLocaleString()}명이 파이어를 계산했어요`);
  (recent || []).slice(0, 6).forEach((s) => {
    const nm = (s.nickname && s.nickname.trim()) || funHandle(s.client_id || '');
    items.push(`💰 ${nm}님이 방금 ${wonStr(s.today_saved)} 절약`);
  });
  (names || []).slice(0, 4).forEach((n) => { if (n) items.push(`👋 ${n}님 접속 중`); });
  items.push('🏆 이번 주 절약왕 경쟁 중 — 저축 탭에서 도전!');
  if (items.length === 0) items.push('🦝 알뜰한 너구리를 키우며 파이어에 다가가요');
  return items;
}

export default function LiveBanner() {
  const [items, setItems] = useState([]);
  useEffect(() => {
    let alive = true;
    const load = async () => {
      const [p, recent, total] = await Promise.all([fetchLivePresence(), fetchRecentSaves(8), fetchTotalCalc()]);
      if (!alive) return;
      setItems(buildItems({ online: p ? p.online : 0, names: p ? p.names : [], recent, total }));
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
