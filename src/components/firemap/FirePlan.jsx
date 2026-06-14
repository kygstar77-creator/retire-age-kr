import { useEffect, useState } from 'react';
import Header from './Header.jsx';
import { formatWon } from '../../firemap-v2/formatters.js';
import { getAssetHistory, logAsset } from '../../utils/assetHistory.js';

const won = (n) => formatWon(Math.round(n || 0));
const eok = (n) => {
  const v = (n || 0) / 1e8;
  return v >= 10 ? `${Math.round(v)}억` : `${v.toFixed(1)}억`;
};

export default function FirePlan({ simulation, onMove, onChange }) {
  const inp = (simulation && simulation.inputs) || {};
  const asset = Number(inp.financialAsset) || 0;
  const target = Math.max(0, Math.round(simulation.requiredFireAssetByFourPercent || 0));
  const earliest = simulation.earliestRetirementAge;
  const pct = target > 0 ? Math.max(0, Math.min(100, Math.round((asset / target) * 100))) : 0;

  const [hist, setHist] = useState(getAssetHistory);
  const [editing, setEditing] = useState(false);
  const [val, setVal] = useState('');

  useEffect(() => { if (asset > 0) setHist(logAsset(asset)); /* eslint-disable-next-line */ }, []);

  const prev = hist.length >= 2 ? hist[hist.length - 2].v : null;
  const mom = prev != null ? asset - prev : null;

  const saveAsset = () => {
    const v = Math.max(0, Math.round(Number(String(val).replace(/[^0-9]/g, '')) || 0));
    if (v > 0) { if (onChange) onChange('financialAsset', v); setHist(logAsset(v)); }
    setEditing(false); setVal('');
  };

  const pts = hist.length ? hist : [{ ym: '', v: asset }];
  const max = Math.max(...pts.map((p) => p.v), 1);
  const min = Math.min(...pts.map((p) => p.v), 0);
  const span = Math.max(1, max - min);
  const line = pts.map((p, i) => {
    const x = pts.length > 1 ? (i / (pts.length - 1)) * 300 : 300;
    const y = 60 - ((p.v - min) / span) * 52;
    return `${x.toFixed(0)},${y.toFixed(0)}`;
  }).join(' ');

  const hi = inp.healthInsuranceEnabled && inp.monthlyHealthInsurance > 0;

  return (
    <main className="fm-screen fm-scroll fm-has-tabbar">
      <Header tag="내 파이어 플랜" onBack={() => onMove('result')} />

      <section className="fm-card fm-plan-hero">
        <div className="fm-plan-top">
          <div className="fm-plan-ring" style={{ background: `conic-gradient(#ff5a00 0 ${pct}%, #eef0f3 ${pct}% 100%)` }}>
            <div className="fm-plan-ring-in"><b>{pct}%</b><span>달성</span></div>
          </div>
          <div className="fm-plan-meta">
            <small>예상 파이어</small>
            <strong>{earliest ? `${earliest}세` : '계산 필요'}</strong>
            <p>목표 <b>{eok(target)}</b> 중 <b>{eok(asset)}</b></p>
          </div>
        </div>
        {mom != null && mom !== 0 && (
          <div className={`fm-plan-mom ${mom >= 0 ? 'up' : 'down'}`}>
            지난달보다 <b>{mom >= 0 ? '+' : '−'}{won(Math.abs(mom))}</b>{mom > 0 ? ' · 목표에 더 가까워졌어요' : ''}
          </div>
        )}
      </section>

      <section className="fm-card">
        <p className="fm-kicker">내 금융자산 추이</p>
        {hist.length >= 2
          ? <svg viewBox="0 0 300 64" className="fm-plan-spark" preserveAspectRatio="none"><polyline points={line} fill="none" stroke="#ff5a00" strokeWidth="2.5" strokeLinejoin="round" strokeLinecap="round" /></svg>
          : <p className="fm-plan-empty">이번 달 자산을 기록하면 다음 달부터 추이가 쌓여요.</p>}
        {!editing
          ? <button type="button" className="fm-plan-update" onClick={() => { setVal(String(asset)); setEditing(true); }}>이번 달 자산 업데이트</button>
          : (
            <div className="fm-save-inline">
              <input inputMode="numeric" className="fm-save-inline-in" value={val} onChange={(e) => setVal(e.target.value.replace(/[^0-9]/g, ''))} placeholder="현재 금융자산 (원)" autoFocus />
              <button type="button" className="fm-save-inline-go" onClick={saveAsset}>저장</button>
              <button type="button" className="fm-save-inline-cancel" onClick={() => setEditing(false)}>취소</button>
            </div>
          )}
      </section>

      <section className="fm-card fm-plan-inst">
        <p className="fm-kicker">한국 제도까지 반영</p>
        <ul className="fm-plan-inst-list">
          <li><span>국민연금</span><b>{inp.expectedPensionAge || 65}세~ 月 {Math.round((inp.expectedMonthlyPension || 0) / 10000).toLocaleString()}만</b></li>
          <li><span>물가 상승</span><b>연 {inp.inflationRate ?? 3}%</b></li>
          <li><span>건강보험료</span>{hi ? <b>月 {Math.round(inp.monthlyHealthInsurance / 10000)}만 반영</b> : <button type="button" className="fm-inline-link" onClick={() => onMove('experiment')}>설정에서 켜기</button>}</li>
          <li><span>세금(양도·배당)</span><button type="button" className="fm-inline-link" onClick={() => onMove('tools')}>세금 도구로 점검 ›</button></li>
        </ul>
        <p className="fm-plan-inst-note">대부분의 계산기가 빠뜨리는 제도까지 반영해요. (랭킹은 공정성 위해 세전 기준)</p>
      </section>

      <div className="fm-plan-mods">
        <button type="button" onClick={() => onMove('cities')}><span>📍</span>지역 바꿔보기</button>
        <button type="button" onClick={() => onMove('dividend')}><span>💰</span>배당 현금흐름</button>
        <button type="button" onClick={() => onMove('experiment')}><span>🎛️</span>조건 바꿔보기</button>
      </div>
    </main>
  );
}
