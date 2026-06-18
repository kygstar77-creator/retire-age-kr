import { useEffect, useState } from 'react';
import Header from './Header.jsx';
import { formatWon } from '../../firemap-v2/formatters.js';
import { getAssetHistory, logAsset } from '../../utils/assetHistory.js';
import { getLatestRank } from '../../firemap-v2/rankHistory.js';
import { fetchPeerBoard } from '../../utils/firemapScoresApi.js';
import { ageBandOf } from '../../firemap-v2/stats.js';
import { computeProgress, hasCalculated } from '../../utils/savingsEngine.js';
import InstallButton from './InstallButton.jsx';
import FireClock from './FireClock.jsx';
import FireClockPush from './FireClockPush.jsx';
import CompletionCard from './CompletionCard.jsx';
import StageTargets from './StageTargets.jsx';
import JourneyPulse from './JourneyPulse.jsx';
import OpenChatNotice from './OpenChatNotice.jsx';
import { account } from '../../utils/identity.js';

const won = (n) => formatWon(Math.round(n || 0));

const readJSONsafe = (k) => { try { return JSON.parse(localStorage.getItem(k) || 'null'); } catch { return null; } };

export default function FirePlan({ simulation, onMove, onChange, asHome }) {
  const inp = (simulation && simulation.inputs) || {};
  const asset = Number(inp.financialAsset) || 0;
  const earliest = simulation.earliestRetirementAge;

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

      <CompletionCard simulation={simulation} onMove={onMove} />

      {asHome && <FireClock simulation={simulation} />}

      {asHome && <JourneyPulse simulation={simulation} onMove={onMove} />}

      <StageTargets simulation={simulation} onMove={onMove} />

      {asHome && <OpenChatNotice />}

      {asHome && <FireClockPush simulation={simulation} />}

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
