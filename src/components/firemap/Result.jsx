import { useEffect, useMemo, useState } from 'react';
import Header from './Header.jsx';
import { formatWon } from '../../firemap-v2/formatters.js';
import { buildScenario, fireStatus, runwayText, scenarioEndAge, survivalPhrase } from '../../firemap-v2/scenarios.js';
import { monteCarloSuccess } from '../../utils/retirementSimulator.js';
import { screens, NEXT_ACTION_META } from '../../firemap-v2/screens.js';
import { statsRank, gradeFromScore } from '../../firemap-v2/rank.js';
import { submitScore, fetchUserRank } from '../../utils/firemapScoresApi.js';
import { saveRankSnapshot, getLatestRank } from '../../firemap-v2/rankHistory.js';
import { buildScenarioShareUrl } from '../../utils/shareState.js';
import { FIRE_CITIES } from '../../firemap-v2/cities.js';

function RankHero({ simulation }) {
  const base = statsRank(simulation);
  const [live, setLive] = useState(null);
  const [prevSnap] = useState(() => getLatestRank());
  const score = simulation.survivalScore;
  const delta = prevSnap ? prevSnap.percentile - base.percentile : 0;

  useEffect(() => {
    let alive = true;
    saveRankSnapshot({ percentile: base.percentile, grade: base.grade, score });
    (async () => {
      try {
        const key = `fm_score_sent_${score}`;
        if (!sessionStorage.getItem(key)) {
          let nick = '';
          try { nick = localStorage.getItem('fm_nickname') || ''; } catch { /* ignore */ }
          await submitScore({
            fireScore: score,
            ageBand: base.ageBand,
            survivalAge: (simulation.targetResult && simulation.targetResult.depletionAge) || simulation.inputs.simulationUntilAge,
            nickname: nick,
            earliestAge: simulation.earliestRetirementAge
          });
          sessionStorage.setItem(key, '1');
        }
      } catch { /* ignore */ }
      const r = await fetchUserRank(simulation.earliestRetirementAge);
      if (alive) setLive(r);
    })();
    return () => { alive = false; };
  }, [score]);

  return (
    <section className="fm-rank-hero">
      <p className="fm-rank-label">내 FIRE 자생력 · {base.ageBandLabel} 또래 기준</p>
      <div className="fm-rank-top">
        <span className="fm-rank-pct">상위 {base.percentile}%</span>
        <span className="fm-rank-badge">{base.grade}등급</span>
        {delta !== 0 && <span className={`fm-rank-delta ${delta > 0 ? 'up' : 'down'}`}>{delta > 0 ? `▲ ${delta}%p` : `▼ ${Math.abs(delta)}%p`}</span>}
      </div>
      {live
        ? <p className="fm-rank-line">함께 계산한 {live.total.toLocaleString()}명 중 <b>{live.position.toLocaleString()}등</b></p>
        : <p className="fm-rank-line">함께 계산한 사용자 중 등수 집계 중…</p>}
      {live && (live.position > 1
        ? <p className="fm-rank-climb">1등까지 <b>{(live.position - 1).toLocaleString()}명</b> · 조건을 바꾸면 등수가 올라가요</p>
        : <p className="fm-rank-climb">지금 전체 1등이에요! 이 자리를 지켜보세요</p>)}
      <p className="fm-rank-trend">{base.source}</p>
      <p className="fm-rank-note">등급은 내 자산수명 점수 기준 · 상위 %는 통계청 또래 순자산 기준</p>
    </section>
  );
}

function ResultHero({ simulation }) {
  const targetAge = `${simulation.inputs.targetRetirementAge}세`;
  const phrase = survivalPhrase(simulation);
  const earliest = simulation.earliestRetirementAge;
  const target = simulation.inputs.targetRetirementAge;
  const safeCopy = !earliest
    ? '지금 가정으로는 더 모으거나 생활비를 줄여야 자산이 오래 버텨요.'
    : earliest < target
      ? `지금 자산이면 더 일찍, ${earliest}세 퇴사도 가능해 보여요.`
      : earliest > target
        ? `${earliest}세까지 일하면 자산이 훨씬 안전해져요.`
        : '지금 목표 나이가 적절해 보여요.';
  return (
    <section className="fm-card fm-result fm-result-v3">
      <p>내 FIRE 현재 위치</p>
      {phrase.ok
        ? <h2>{targetAge}에 퇴사하면<br /><b>{phrase.runway}</b>까지 버틸 수 있어요.</h2>
        : <h2>지금 자산으론<br /><b>{targetAge}</b> 퇴사가 일러요.</h2>}
      <div className="fm-result-chips">
        <span>은퇴 나이 <b>{targetAge}</b></span>
        <span>경제적 자유 시점 <b>{phrase.runway}</b></span>
      </div>
      <p className="fm-result-copy">{safeCopy}</p>
      <div className="fm-result-assumptions">
        <span>현재 계산 기준 · 연 수익률 {simulation.inputs.annualReturnRate}% · 물가 {simulation.inputs.inflationRate}%</span>
        <span>국민연금 {simulation.inputs.expectedPensionAge}세부터 월 {formatWon(simulation.inputs.expectedMonthlyPension)} 반영</span>
      </div>
      <div className="fm-score-box">
        <div><small>FIRE 진단</small><b className="fm-score-status">{fireStatus(simulation.survivalScore)}</b></div>
        <div><small>점수</small><b className="fm-score-number"><em>{simulation.survivalScore}</em>/100</b></div>
        <div className="fm-score-meter" aria-label={`FIRE 점수 ${simulation.survivalScore}점`}><i style={{ width: `${Math.max(8, simulation.survivalScore)}%` }} /></div>
        <p>높을수록 퇴사 후 자산 여유가 커요.</p>
      </div>
    </section>
  );
}

const RISK_LEVELS = [
  { k: 'safe', label: '안전', ret: 3 },
  { k: 'balanced', label: '균형', ret: 5 },
  { k: 'aggressive', label: '공격', ret: 8 }
];
function SuccessProbability({ simulation }) {
  const [risk, setRisk] = useState('balanced');
  const cfg = RISK_LEVELS.find((r) => r.k === risk) || RISK_LEVELS[1];
  const pct = useMemo(() => monteCarloSuccess({ ...simulation.inputs, annualReturnRate: cfg.ret }), [simulation, cfg.ret]);
  const level = pct >= 80 ? 'ok' : pct >= 50 ? 'mid' : 'low';
  const msg = pct >= 80 ? '시장이 출렁여도 안정적이에요' : pct >= 50 ? '변동성에 다소 취약해요' : '시장이 나쁘면 부족할 수 있어요';
  return (
    <section className={`fm-card fm-mc fm-mc-${level}`}>
      <p className="fm-kicker">성공 확률 · 변동성 반영</p>
      <div className="fm-mc-row"><b>{pct}%</b><span>{msg}</span></div>
      <div className="fm-mc-risk">
        {RISK_LEVELS.map((r) => (
          <button type="button" key={r.k} className={risk === r.k ? 'on' : ''} onClick={() => setRisk(r.k)}>{r.label}</button>
        ))}
      </div>
      <p className="fm-mc-note">배분별 가정: 안전(연 3%) · 균형(5%) · 공격(8%). 수익률이 높을수록 변동성(위험)도 커집니다. 조건비교의 '수익률 벤치마크'와 같은 기준이에요 — 확률만 보고 무리한 투자는 금물이에요.</p>
    </section>
  );
}

function compareText(base, next) {
  const diff = scenarioEndAge(next) - scenarioEndAge(base);
  if (diff > 0) return `현재보다 ${diff}년 개선`;
  if (diff === 0) return '현재와 비슷함';
  return `${Math.abs(diff)}년 악화`;
}

function leverGain(diff) {
  if (diff > 0) return `+${diff}년`;
  if (diff === 0) return '비슷';
  return `−${Math.abs(diff)}년`;
}

function TopLevers({ inputs, simulation, onChange }) {
  const baseCost = Number(inputs.monthlyLivingCost || 0);
  const lowerCostValue = Math.max(1000000, baseCost >= 2500000 ? baseCost - 1000000 : Math.round(baseCost * 0.8 / 100000) * 100000);
  const baseGrade = gradeFromScore(simulation.survivalScore);
  const baseAge = scenarioEndAge(simulation);
  const defs = [
    { tag: '생활비', title: `생활비 ${formatWon(lowerCostValue)}원으로`, patch: { monthlyLivingCost: lowerCostValue } },
    { tag: '저축액', title: '월 100만 더 저축', patch: { monthlyInvestment: inputs.monthlyInvestment + 1000000 } },
    { tag: '현금흐름', title: '퇴사 후 월 100만 부업', patch: { partTimeIncomeAfterRetirement: inputs.partTimeIncomeAfterRetirement + 1000000 } },
    { tag: '퇴사시점', title: '1년 더 일하기', patch: { targetRetirementAge: inputs.targetRetirementAge + 1 } },
    { tag: '수익률', title: '연 수익률 +1%p', patch: { annualReturnRate: inputs.annualReturnRate + 1 } }
  ];
  const rows = defs
    .map((d) => { const sc = buildScenario(inputs, d.patch); return { ...d, gain: scenarioEndAge(sc) - baseAge, grade: gradeFromScore(sc.survivalScore) }; })
    .sort((a, b) => b.gain - a.gain)
    .slice(0, 4);
  const apply = (patch) => {
    if (onChange) Object.entries(patch).forEach(([k, v]) => onChange(k, v));
    try { window.scrollTo({ top: 0, behavior: 'smooth' }); } catch { /* ignore */ }
  };
  return (
    <section>
      <h2 className="fm-section-title">순위·자산수명 올리는 법</h2>
      <p className="fm-section-sub">탭하면 내 결과에 바로 적용돼요</p>
      <div className="fm-improve-grid fm-improve-grid-two">
        {rows.map((d) => (
          <article className="fm-improve-card" key={d.tag}>
            <em>{d.tag}</em><h3>{d.title}</h3><strong>{leverGain(d.gain)}</strong>
            <p>{baseGrade === d.grade ? `${d.grade}등급 유지` : `${baseGrade} → ${d.grade}등급`}</p>
            <button type="button" className="fm-lever-apply" onClick={() => apply(d.patch)}>이대로 적용</button>
          </article>
        ))}
      </div>
    </section>
  );
}

function YearlyAssetChart({ simulation }) {
  const rows = simulation.targetResult.rows || [];
  const [sel, setSel] = useState(null);
  if (rows.length < 2) return null;
  const pts = rows.map((r) => ({ age: r.age, v: Math.max(0, r.financialAsset), status: r.status }));
  const n = pts.length;
  const maxV = Math.max(...pts.map((p) => p.v), 1);
  const a0 = pts[0].age, a1 = pts[n - 1].age;
  const W = 320, H = 120, P = 8;
  const X = (a) => P + ((a - a0) / Math.max(1, a1 - a0)) * (W - 2 * P);
  const Y = (v) => H - P - (v / maxV) * (H - 2 * P);
  const line = pts.map((p, i) => `${i ? 'L' : 'M'}${X(p.age).toFixed(1)} ${Y(p.v).toFixed(1)}`).join(' ');
  const area = `${line} L${X(a1).toFixed(1)} ${H - P} L${X(a0).toFixed(1)} ${H - P} Z`;
  const ret = simulation.inputs.targetRetirementAge;
  const retX = X(Math.min(a1, Math.max(a0, ret)));
  const retIdx = Math.max(0, pts.findIndex((p) => p.age >= ret));
  const cur = sel != null ? pts[Math.min(sel, n - 1)] : (pts[retIdx] || pts[n - 1]);
  const pick = (e) => {
    const box = e.currentTarget.getBoundingClientRect();
    const clientX = e.touches && e.touches[0] ? e.touches[0].clientX : e.clientX;
    const idx = Math.max(0, Math.min(n - 1, Math.round(((clientX - box.left) / box.width) * (n - 1))));
    setSel(idx);
  };
  return (
    <div className="fm-yac">
      <div className="fm-yac-read">
        <b>{cur.age}세</b>
        <span className={cur.status === '퇴사 후' ? 'after' : 'before'}>{cur.status}</span>
        <strong>{formatWon(cur.v)}</strong>
      </div>
      <div
        className="fm-yac-canvas"
        style={{ touchAction: 'none' }}
        onPointerDown={pick}
        onPointerMove={(e) => { if (e.buttons) pick(e); }}
        onTouchStart={pick}
        onTouchMove={pick}
      >
        <svg viewBox={`0 0 ${W} ${H}`} preserveAspectRatio="none" role="img" aria-label="나이별 내 자산 그래프 (눌러서 확인)">
          <path d={area} className="fm-yac-area" />
          <path d={line} className="fm-yac-line" fill="none" />
          <line x1={retX} y1={P} x2={retX} y2={H - P} className="fm-yac-ret" />
          <line x1={X(cur.age)} y1={P} x2={X(cur.age)} y2={H - P} className="fm-yac-cross" />
          <circle cx={X(cur.age)} cy={Y(cur.v)} r="3.5" className="fm-yac-dot" />
        </svg>
      </div>
      <div className="fm-yac-x"><span>{a0}세</span><span>퇴사 {ret}세</span><span>{a1}세</span></div>
      <p className="fm-yac-hint">그래프를 눌러 나이별 자산을 확인하세요</p>
    </div>
  );
}

function OverseasHope({ inputs, simulation, onMove }) {
  const baseEnd = scenarioEndAge(simulation);
  const cands = FIRE_CITIES
    .filter((c) => c.krw < inputs.monthlyLivingCost)
    .map((c) => { const sc = buildScenario(inputs, { monthlyLivingCost: c.krw }); return { ...c, sc, gain: scenarioEndAge(sc) - baseEnd }; })
    .filter((c) => c.gain > 0)
    .sort((a, b) => b.gain - a.gain)
    .slice(0, 3);
  if (cands.length === 0) return null;
  return (
    <section className="fm-card fm-hope">
      <p className="fm-kicker">희망편</p>
      <h2>해외에 살면 더 오래 버틸 수 있어요</h2>
      <p className="fm-hope-lead">지금 생활비({formatWon(inputs.monthlyLivingCost)})로는 <b>{runwayText(simulation)}</b>까지지만, 물가가 낮은 곳이라면:</p>
      <ul className="fm-hope-list">
        {cands.map((c) => (
          <li key={c.city}>
            <span className="fm-hope-city">{c.flag} {c.city}</span>
            <span className="fm-hope-end">{runwayText(c.sc)}까지</span>
            <span className="fm-hope-gain">+{c.gain}년</span>
          </li>
        ))}
      </ul>
      <button type="button" className="fm-hope-cta" onClick={() => onMove('cities')}>전 세계 파이어 도시 탐색 →</button>
    </section>
  );
}

function Roadmap({ simulation }) {
  const rows = simulation.targetResult.rows || [];
  if (rows.length < 2) return null;
  const cur = rows[0];
  const items = [{ age: cur.age, label: '지금 시작', sub: formatWon(cur.financialAsset), hi: false }];
  [100000000, 300000000, 500000000, 1000000000, 2000000000].forEach((t) => {
    if (t > cur.financialAsset) {
      const hit = rows.find((r) => r.financialAsset >= t);
      if (hit && hit.age > cur.age) items.push({ age: hit.age, label: `자산 ${formatWon(t)} 돌파`, sub: null, hi: false });
    }
  });
  const req = simulation.requiredFireAssetByFourPercent;
  if (req && req > cur.financialAsset) {
    const hit = rows.find((r) => r.financialAsset >= req);
    if (hit) items.push({ age: hit.age, label: 'FIRE 목표 자산 달성', sub: `4%룰 ${formatWon(req)}`, hi: true });
  }
  if (simulation.earliestRetirementAge) items.push({ age: simulation.earliestRetirementAge, label: '가장 이른 은퇴 가능', sub: null, hi: true });
  items.push({ age: simulation.inputs.targetRetirementAge, label: '목표 퇴사', sub: null, hi: true });
  const seen = new Set();
  const list = items
    .filter((m) => { const k = m.age + m.label; if (seen.has(k)) return false; seen.add(k); return true; })
    .sort((a, b) => a.age - b.age);
  return (
    <section className="fm-card fm-road">
      <p className="fm-kicker">파이어 로드맵</p>
      <h2>지금부터 은퇴까지, 단계로 보기</h2>
      <ol className="fm-road-list">
        {list.map((m, i) => (
          <li key={i} className={`fm-road-step${m.hi ? ' hi' : ''}`}>
            <span className="fm-road-age">{m.age}세</span>
            <span className="fm-road-body"><b>{m.label}</b>{m.sub && <em>{m.sub}</em>}</span>
          </li>
        ))}
      </ol>
      <p className="fm-road-note">현재 입력 기준 예상 경로예요. 조건을 바꾸면 단계가 당겨져요.</p>
    </section>
  );
}

function YearlyGrowth({ simulation }) {
  const rows = simulation.targetResult.rows || [];
  if (rows.length < 2) return null;
  const start = rows[0].financialAsset;
  const y1 = rows[1] ? rows[1].financialAsset - start : 0;
  const y5 = rows[5] ? rows[5].financialAsset - start : null;
  return (
    <section className="fm-card fm-growth">
      <p className="fm-kicker">내 자산 성장</p>
      <h2>시간이 지나면 자산은 이렇게 늘어요</h2>
      <YearlyAssetChart simulation={simulation} />
      <div className="fm-growth-grid">
        <div><small>1년 뒤</small><b>+{formatWon(Math.max(0, y1))}</b></div>
        {y5 != null && <div><small>5년 뒤</small><b>+{formatWon(Math.max(0, y5))}</b></div>}
        <div><small>은퇴 시점</small><b>{formatWon(simulation.retirementFinancialAsset)}</b></div>
      </div>
      <p className="fm-growth-note">연 수익률 {simulation.inputs.annualReturnRate}% · 저축 반영 · 조건을 바꾸면 더 빨라져요</p>
    </section>
  );
}

function NextActions({ onMove }) {
  const actions = screens.result.next || [];
  return (
    <section className="fm-next-actions" aria-label="다음 행동">
      <h2 className="fm-section-title">다음으로 해볼 것</h2>
      <div className="fm-next-grid">
        {actions.map((id) => {
          const meta = NEXT_ACTION_META[id];
          if (!meta) return null;
          return (
            <button type="button" key={id} className={`fm-next-card${meta.primary ? ' fm-next-primary' : ''}`} onClick={() => onMove(id)}>
              <em>{meta.tag}</em><strong>{meta.title}</strong><span>{meta.desc}</span>
            </button>
          );
        })}
      </div>
    </section>
  );
}

export default function Result({ inputs, simulation, onMove, onChange, onEditFinalQuestion }) {
  const shareRank = async () => {
    const rk = statsRank(simulation);
    const ph = survivalPhrase(simulation);
    const u = new URL(buildScenarioShareUrl(inputs));
    u.pathname = '/s';
    u.searchParams.set('p', String(rk.percentile));
    u.searchParams.set('g', rk.grade);
    u.searchParams.set('rw', ph.short);
    const url = u.toString();
    const text = `또래 상위 ${rk.percentile}% · ${rk.grade}등급 — 내 FIRE 등수, 너도 확인해봐`;
    if (navigator.share) {
      try { await navigator.share({ title: '파이어맵 — 내 FIRE 등수', text, url }); return; }
      catch (e) { if (e && e.name === 'AbortError') return; }
    }
    try { await navigator.clipboard.writeText(url); window.alert('내 등수 링크를 복사했어요. 단톡방에 붙여넣어 보세요!'); }
    catch { onMove('share'); }
  };
  return (
    <main className="fm-screen fm-scroll">
      <Header />
      <RankHero simulation={simulation} />
      <div className="fm-rank-cta">
        <button type="button" className="fm-rank-cta-share" onClick={shareRank}>내 등급 자랑하기</button>
        <button type="button" className="fm-rank-cta-up" onClick={() => onMove('experiment')}>등수 올리기</button>
      </div>
      <ResultHero simulation={simulation} />
      <SuccessProbability simulation={simulation} />
      <OverseasHope inputs={inputs} simulation={simulation} onMove={onMove} />
      <YearlyGrowth simulation={simulation} />
      <Roadmap simulation={simulation} />
      <TopLevers inputs={inputs} simulation={simulation} onChange={onChange} />
      <NextActions onMove={onMove} />
      <div className="fm-ad">광고</div>
    </main>
  );
}
