import { useEffect, useState } from 'react';
import Header from './Header.jsx';
import { formatWon } from '../../firemap-v2/formatters.js';
import { getAssetHistory, logAsset } from '../../utils/assetHistory.js';
import { getLatestRank } from '../../firemap-v2/rankHistory.js';
import { fetchPeerBoard } from '../../utils/firemapScoresApi.js';
import { ageBandOf } from '../../firemap-v2/stats.js';
import { computeProgress, hasCalculated } from '../../utils/savingsEngine.js';
import InstallButton from './InstallButton.jsx';
import PetCard from './PetCard.jsx';
import FireClock from './FireClock.jsx';
import OpenChatNotice from './OpenChatNotice.jsx';
import { account } from '../../utils/identity.js';

const won = (n) => formatWon(Math.round(n || 0));
const eok = (n) => {
  const v = (n || 0) / 1e8;
  return v >= 10 ? `${Math.round(v)}억` : `${v.toFixed(1)}억`;
};

const readJSONsafe = (k) => { try { return JSON.parse(localStorage.getItem(k) || 'null'); } catch { return null; } };
function pickNextAction() {
  const sv = readJSONsafe('fm_save');
  const fd = readJSONsafe('fm_daily');
  const hasSave = (sv && (sv.total || 0) > 0) || (fd && fd.days && Object.keys(fd.days).length > 0);
  if (!hasSave) return { label: '오늘 절약 한 번 기록하고 파이어 시간 벌기', to: 'save', ico: '⏱️' };
  // 자산 업데이트는 바로 위 대시보드 카드에 이미 있어 중복 → 다음 할 일에서는 제외
  const pool = [
    { label: '지방 살면 몇 년 빨라지나 보기', to: 'cities', ico: '📍' },
    { label: '파이어 후 건보료 얼마인지 확인하기', to: 'dependent', ico: '🩺' },
    { label: '배당으로 월 현금흐름 만들어보기', to: 'dividend', ico: '💵' },
    { label: '조건 바꿔서 파이어 더 당겨보기', to: 'experiment', ico: '🎛️' },
    { label: '또래 중 내 파이어 등수 보기', to: 'ranking', ico: '🏆' }
  ];
  return pool[Math.floor(Date.now() / 86400000) % pool.length];
}

export default function FirePlan({ simulation, onMove, onChange, asHome }) {
  const inp = (simulation && simulation.inputs) || {};
  const asset = Number(inp.financialAsset) || 0;
  const target = Math.max(0, Math.round(simulation.requiredFireAssetByFourPercent || 0));
  const earliest = simulation.earliestRetirementAge;
  const pct = target > 0 ? Math.max(0, Math.min(100, Math.round((asset / target) * 100))) : 0;

  // 목표(사용자가 정한 목표 파이어 나이) = 기준선, 예상(지금 예상) = 현재 위치.
  const targetAge = Number(inp.targetRetirementAge) || 0;
  const ageGap = earliest != null ? earliest - targetAge : null;
  const gapDir = ageGap == null ? '' : ageGap > 0 ? 'behind' : ageGap < 0 ? 'ahead' : 'even';
  const gapText = ageGap == null ? '' : ageGap > 0 ? `목표보다 ${ageGap}년 늦음` : ageGap < 0 ? `목표보다 ${Math.abs(ageGap)}년 빠름` : '목표와 같음';
  const gapColor = gapDir === 'ahead' ? '#0f6e56' : gapDir === 'behind' ? '#854f0b' : 'var(--fm-muted, #6b6f76)';

  const [hist, setHist] = useState(getAssetHistory);
  const [editing, setEditing] = useState(false);
  const [val, setVal] = useState('');
  const [peerRank, setPeerRank] = useState(null);

  useEffect(() => { if (asset > 0) setHist(logAsset(asset)); /* eslint-disable-next-line */ }, []);
  useEffect(() => {
    if (!asHome) return undefined;
    let alive = true;
    (async () => {
      try {
        const adv = hasCalculated() ? Math.max(0, computeProgress(simulation).advanceDays) : 0;
        const pr = await fetchPeerBoard({ currentAge: inp.currentAge, ageBand: ageBandOf(inp.currentAge), earliestAge: earliest, advancedDays: adv });
        if (alive) setPeerRank(pr);
      } catch { /* ignore */ }
    })();
    return () => { alive = false; };
    // eslint-disable-next-line
  }, [asHome, earliest, inp.currentAge]);

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
      <Header tag="내 파이어 플랜" onBack={asHome ? undefined : () => onMove('result')} />

      {asHome && (() => {
        const acc = account();
        return (
          <button type="button" className={`fm-acct-bar${acc && acc.handle ? ' on' : ''}`} onClick={() => onMove('account')}>
            <span className="fm-acct-bar-ic">{acc && acc.handle ? '👤' : '🔒'}</span>
            {acc && acc.handle
              ? <span className="fm-acct-bar-tx"><b>{acc.handle}</b><em>기록이 안전하게 이어져요</em></span>
              : <span className="fm-acct-bar-tx"><b>로그인하고 내 기록 지키기</b><em>기기 바꿔도 그대로 이어져요</em></span>}
            <span className="fm-acct-bar-go">{acc && acc.handle ? '관리 ›' : '로그인 ›'}</span>
          </button>
        );
      })()}

      <section className="fm-card fm-plan-hero">
        <div className="fm-plan-top">
          <div className="fm-plan-ring" style={{ background: `conic-gradient(#ff5a00 0 ${pct}%, #eef0f3 ${pct}% 100%)` }}>
            <div className="fm-plan-ring-in"><b>{pct}%</b><span>달성</span></div>
          </div>
          <div className="fm-plan-meta">
            <small>{targetAge ? `목표 ${targetAge}세 · 지금 예상` : '예상 파이어'}</small>
            <strong>{earliest ? `${earliest}세` : '계산 필요'}</strong>
            {earliest && gapText
              ? <p><b style={{ color: gapColor }}>{gapText}</b> · 목표 <b>{eok(target)}</b> 중 <b>{eok(asset)}</b></p>
              : <p>목표 <b>{eok(target)}</b> 중 <b>{eok(asset)}</b></p>}
          </div>
        </div>
        {mom != null && mom !== 0 && (
          <div className={`fm-plan-mom ${mom >= 0 ? 'up' : 'down'}`}>
            지난달보다 <b>{mom >= 0 ? '+' : '−'}{won(Math.abs(mom))}</b>{mom > 0 ? ' · 목표에 더 가까워졌어요' : ''}
          </div>
        )}
      </section>

      {asHome && <FireClock simulation={simulation} />}

      {asHome && (
        <button type="button" className="fm-plan-result" onClick={() => onMove('result')}>📊 내 파이어 결과·또래 등수 자세히 보기 →</button>
      )}

      {asHome && (() => {
        const fd = readJSONsafe('fm_daily');
        const ym = new Date().toISOString().slice(0, 7);
        const monthDep = fd && fd.days ? Object.entries(fd.days).filter(([k]) => k.startsWith(ym)).reduce((a, [, v]) => a + (Number(v) || 0), 0) : 0;
        const sv = readJSONsafe('fm_save');
        const totalSave = sv ? (sv.total || 0) : 0;
        const streak = sv ? (sv.streak || 0) : 0;
        const rankNum = peerRank && peerRank.percentile != null
          ? `상위 ${peerRank.percentile}%`
          : (peerRank && peerRank.position != null ? `${peerRank.position.toLocaleString()}위` : '순위 보기');
        return (
          <div className="fm-sum-grid">
            <button type="button" className="fm-sum-tile" onClick={() => onMove('save')}>
              <small>저축·절약</small>
              <b>이번 달 {won(monthDep)}</b>
              <em>누적 절약 {won(totalSave)}{streak > 0 ? ` · ${streak}일 연속` : ''} ›</em>
            </button>
            <button type="button" className="fm-sum-tile" onClick={() => onMove('ranking')}>
              <small>내 나이 순위</small>
              <b>{rankNum}</b>
              <em>{peerRank ? `${peerRank.ageLabel} 중 · 등수 보기 ›` : '내 또래 등수 보기 ›'}</em>
            </button>
          </div>
        );
      })()}

      {asHome && <OpenChatNotice />}

      {asHome && <PetCard />}

      <section className="fm-card">
        <p className="fm-kicker">내 금융자산 추이</p>
        <p className="fm-plan-sub">매달 한 번 자산을 기록하면, 목표까지 얼마나 다가가는지 그래프로 보여줘요.</p>
        {hist.length >= 2
          ? <svg viewBox="0 0 300 64" className="fm-plan-spark" preserveAspectRatio="none"><polyline points={line} fill="none" stroke="#ff5a00" strokeWidth="2.5" strokeLinejoin="round" strokeLinecap="round" /></svg>
          : (hist.length === 1 || asset > 0)
            ? <div className="fm-plan-one"><b>{won(hist.length ? hist[hist.length - 1].v : asset)}</b><span>이번 달 기록됨 · 다음 달 또 기록하면 추이 선이 그려져요</span></div>
            : <p className="fm-plan-empty">지금 기록해두면 다음 달부터 추이 선이 그려져요.</p>}
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
          <li><span>건강보험료</span>{hi ? <button type="button" className="fm-inline-link" onClick={() => onMove('dependent')}>月 {Math.round(inp.monthlyHealthInsurance / 10000)}만 반영 · 끄기 ›</button> : <button type="button" className="fm-inline-link" onClick={() => onMove('dependent')}>계산해서 반영하기 ›</button>}</li>
          <li><span>세금(양도·배당)</span>{(() => { const t = Number(inp.investType) || 0; const lbl = t === 3 ? '양도세+배당세 반영' : t === 1 ? '해외 양도세 반영' : t === 2 ? '배당세 반영' : null; return <button type="button" className="fm-inline-link" onClick={() => onMove('foreignTax')}>{lbl ? `${lbl} · 끄기 ›` : '계산해서 반영하기 ›'}</button>; })()}</li>
        </ul>
        <p className="fm-plan-inst-note">국민연금·물가·건보·세금까지 결과에 반영해요. (또래 순위는 순자산 기준)</p>
      </section>

      {(() => {
        const na = pickNextAction();
        return (
          <button type="button" className="fm-next-best" onClick={() => (na.to === 'self' ? (setVal(String(asset)), setEditing(true)) : onMove(na.to))}>
            <span className="fm-next-best-cap">🎯 다음 할 일</span>
            <span className="fm-next-best-main">{na.ico} {na.label}</span>
            <span className="fm-next-best-go">바로 하기 →</span>
          </button>
        );
      })()}
      <button type="button" className="fm-plan-tools" onClick={() => onMove('tools')}>🧰 정밀 도구 전체 보기 (지역·현금흐름·건보·세금) →</button>
      {asHome && <InstallButton />}
      {asHome && (
        <nav className="fm-policy-links" aria-label="정책 및 문의">
          <a href="/privacy.html">개인정보처리방침</a>
          <a href="/disclaimer.html">면책 안내</a>
          <a href="/guide/">파이어 백과</a>
          <a href="/contact.html">문의</a>
        </nav>
      )}
    </main>
  );
}
