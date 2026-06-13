import { useEffect, useState } from 'react';
import Header from './Header.jsx';
import ResultSimTabs from './ResultSimTabs.jsx';
import { formatWon } from '../../firemap-v2/formatters.js';
import { buildScenario, buildGrowthSeries, fireStatus, runwayText, scenarioEndAge, survivalPhrase } from '../../firemap-v2/scenarios.js';
import { simulateRetirement } from '../../utils/retirementSimulator.js';
import { screens, NEXT_ACTION_META } from '../../firemap-v2/screens.js';
import { shareToKakao } from '../../utils/kakaoShare.js';
import { statsRank, gradeFromScore } from '../../firemap-v2/rank.js';
import { submitScore, fetchUserRank, fetchAggregates, assetBandOf } from '../../utils/firemapScoresApi.js';
import { saveRankSnapshot, getLatestRank } from '../../firemap-v2/rankHistory.js';
import { FIRE_CITIES } from '../../firemap-v2/cities.js';
import { track } from '../../firemap-v2/dailyData.js';
import AccountCard from './AccountCard.jsx';

function ResultHeroV2({ simulation }) {
  const base = statsRank(simulation);
  const phrase = survivalPhrase(simulation);
  const score = simulation.survivalScore;
  const earliest = simulation.earliestRetirementAge;
  const target = simulation.inputs.targetRetirementAge;
  const inp = simulation.inputs;
  const [live, setLive] = useState(null);
  const [agg, setAgg] = useState(null);

  useEffect(() => {
    let alive = true;
    saveRankSnapshot({ percentile: base.percentile, grade: base.grade, score, earliest });
    track('calc_complete', { earliest: earliest || 0 });
    track('result_view', { earliest: earliest || 0 });
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
            earliestAge: earliest,
            assetBand: assetBandOf(simulation.netWorth)
          });
          sessionStorage.setItem(key, '1');
        }
      } catch { /* ignore */ }
      const [r, a] = await Promise.all([fetchUserRank(earliest), fetchAggregates()]);
      if (alive) { setLive(r); setAgg(a); }
    })();
    return () => { alive = false; };
  }, [score]);

  const peerAvg = agg && agg.avgEarliest ? agg.avgEarliest : null;
  const diff = (peerAvg != null && earliest != null) ? (peerAvg - earliest) : null;

  return (
    <section className="fm-rank-hero fm-result-hero-v4">
      <p className="fm-rank-label">내 퇴사 가능 나이 · {base.ageBandLabel} 또래 기준</p>
      <div className="fm-rank-top">
        <span className="fm-rank-pct">{earliest ? `${earliest}세` : '계산 필요'}</span>
        {diff != null && (
          <span className={`fm-rank-delta ${diff >= 0 ? 'up' : 'down'}`}>
            {diff > 0 ? `또래 ▲ ${diff}년 빠름` : diff < 0 ? `또래 ▼ ${Math.abs(diff)}년 느림` : '또래와 비슷'}
          </span>
        )}
      </div>
      <p className="fm-hero-headline">{earliest ? '지금 계획이면 이 나이에 퇴사할 수 있어요' : '더 모으거나 생활비를 줄이면 퇴사 시점이 보여요'}</p>
      {live
        ? <button type="button" className="fm-rank-line fm-rank-line-link" onClick={() => { window.location.hash = '#ranking'; }}>함께 계산한 <b>{live.total.toLocaleString()}명</b> 중 <b>{live.position.toLocaleString()}등</b> · <span className="fm-rank-go">전체 랭킹 보기 ›</span></button>
        : <p className="fm-rank-line">실시간 집계 중…</p>}
      {live && (live.position > 1
        ? <p className="fm-rank-climb">1등까지 <b>{(live.position - 1).toLocaleString()}명</b> · 조건 바꾸면 등수가 올라가요</p>
        : <p className="fm-rank-climb">지금 전체 1등이에요!</p>)}
      <div className="fm-hero-mini">
        <span>목표 퇴사 <b>{target}세</b></span>
        <span>자산 버티는 나이 <b>{phrase.runway}</b></span>
      </div>
      <p className="fm-rank-note">{peerAvg != null ? `또래 평균 ${peerAvg}세 · ` : ''}또래 순자산 상위 {base.percentile}%(통계청 2025 가계금융복지조사 기준) · 연 수익률 {inp.annualReturnRate}% · 물가 {inp.inflationRate}% · 국민연금 {inp.expectedPensionAge}세~ 월 {formatWon(inp.expectedMonthlyPension)} · <b>세전(세금 미반영)</b></p>
      <button type="button" className="fm-tax-hint" onClick={() => { window.location.hash = '#experiment'; }}>세금·배당 반영해 보기 → 🎛️ 바꿔보기</button>
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

function solveMin(test, hi, round) {
  if (test(0)) return 0;
  if (!test(hi)) return null;
  let lo = 0, h = hi;
  for (let i = 0; i < 22; i += 1) { const m = (lo + h) / 2; if (test(m)) h = m; else lo = m; }
  return Math.ceil(h / round) * round;
}

function TopLevers({ inputs, simulation, onChange }) {
  const until = simulation.inputs.simulationUntilAge;
  const ni = simulation.inputs;
  const ok = (patch) => !simulateRetirement({ ...ni, ...patch }).depletionAge;
  const apply = (patch) => {
    if (onChange) Object.entries(patch).forEach(([k, v]) => onChange(k, v));
    try { window.scrollTo({ top: 0, behavior: 'smooth' }); } catch { /* ignore */ }
  };
  const baseOk = ok({});

  if (baseOk) {
    return (
      <section className="fm-card fm-goal fm-goal-done">
        <p className="fm-kicker">목표 달성</p>
        <h2>이미 {until}세까지 버티는 계획이에요 🎉</h2>
        <p className="fm-goal-sub">{simulation.earliestRetirementAge ? `가장 빠르면 ${simulation.earliestRetirementAge}세에도 은퇴할 수 있어요. 더 당겨볼까요?` : '여유가 있어요. 조건을 더 공격적으로 바꿔보세요.'}</p>
        <button type="button" className="fm-ce-cta" onClick={() => onChange && (window.location.hash = '#experiment')}>조건 바꿔 더 당겨보기</button>
      </section>
    );
  }

  const lc = ni.monthlyLivingCost || 0;
  const items = [
    { tag: '저축', solve: solveMin((d) => ok({ monthlyInvestment: ni.monthlyInvestment + d }), 30000000, 100000),
      label: (d) => `월 ${formatWon(d)} 더 저축`, patch: (d) => ({ monthlyInvestment: ni.monthlyInvestment + d }) },
    { tag: '생활비', solve: solveMin((d) => ok({ monthlyLivingCost: Math.max(800000, lc - d) }), Math.max(0, lc - 800000), 100000),
      label: (d) => `생활비 월 ${formatWon(d)} 줄이기`, patch: (d) => ({ monthlyLivingCost: Math.max(800000, lc - d) }) },
    { tag: '근무', solve: solveMin((d) => ok({ targetRetirementAge: ni.targetRetirementAge + d }), 15, 1),
      label: (d) => `${d}년 더 일하기 (${ni.targetRetirementAge + d}세)`, patch: (d) => ({ targetRetirementAge: ni.targetRetirementAge + d }) },
    { tag: '부업', solve: solveMin((d) => ok({ partTimeIncomeAfterRetirement: ni.partTimeIncomeAfterRetirement + d }), 10000000, 100000),
      label: (d) => `퇴사 후 월 ${formatWon(d)} 벌기`, patch: (d) => ({ partTimeIncomeAfterRetirement: ni.partTimeIncomeAfterRetirement + d }) },
    { tag: '수익률', solve: solveMin((d) => ok({ annualReturnRate: ni.annualReturnRate + d }), 15, 0.5),
      label: (d) => `수익률 +${d}%p (연 ${(ni.annualReturnRate + d).toFixed(1)}%)`, patch: (d) => ({ annualReturnRate: ni.annualReturnRate + d }) }
  ];
  return (
    <section className="fm-card fm-goal">
      <p className="fm-kicker">목표 달성 플랜</p>
      <h2>{ni.targetRetirementAge}세 퇴사를 성공시키려면?</h2>
      <p className="fm-goal-sub">{until}세까지 자산이 버티게 하는 방법이에요. <b>아래 중 하나만</b> 해도 목표 달성!</p>
      <ul className="fm-goal-list">
        {items.map((it) => (
          <li key={it.tag} className={`fm-goal-item${it.solve === null ? ' off' : ''}`}>
            <span className="fm-goal-tag">{it.tag}</span>
            <span className="fm-goal-need">{it.solve === null ? '이 방법만으론 어려워요' : it.label(it.solve)}</span>
            {it.solve !== null && <button type="button" className="fm-goal-apply" onClick={() => apply(it.patch(it.solve))}>적용</button>}
          </li>
        ))}
      </ul>
      <p className="fm-goal-note">각 값은 목표 달성에 필요한 최소치예요. 수익률은 높이면 위험도 커지니 참고만 하세요.</p>
      <button type="button" className="fm-goal-savelink" onClick={() => { window.location.hash = '#save'; }}>💡 이 저축, 매일 조금씩 채우려면 → 저축 탭</button>
    </section>
  );
}

function YearlyAssetChart({ simulation }) {
  const rows = simulation.targetResult.rows || [];
  const [sel, setSel] = useState(null);
  if (rows.length < 2) return null;
  const g = buildGrowthSeries(simulation);
  const pts = rows.map((r, i) => ({
    age: r.age,
    status: r.status,
    principal: Math.max(0, g.principal[i] ?? 0),
    gains: Math.max(0, g.gains[i] ?? 0),
    v: Math.max(0, g.total[i] ?? r.financialAsset)
  }));
  const n = pts.length;
  const maxV = Math.max(...pts.map((p) => p.v), 1);
  const a0 = pts[0].age, a1 = pts[n - 1].age;
  const W = 320, H = 120, P = 8;
  const X = (a) => P + ((a - a0) / Math.max(1, a1 - a0)) * (W - 2 * P);
  const Y = (v) => H - P - (v / maxV) * (H - 2 * P);
  // 스택 영역: 원금(아래) + 불어난 돈(원금 위에)
  const principalTop = pts.map((p, i) => `${i ? 'L' : 'M'}${X(p.age).toFixed(1)} ${Y(p.principal).toFixed(1)}`).join(' ');
  const principalArea = `${principalTop} L${X(a1).toFixed(1)} ${(H - P).toFixed(1)} L${X(a0).toFixed(1)} ${(H - P).toFixed(1)} Z`;
  const totalTop = pts.map((p, i) => `${i ? 'L' : 'M'}${X(p.age).toFixed(1)} ${Y(p.v).toFixed(1)}`).join(' ');
  const principalBack = pts.slice().reverse().map((p) => `L${X(p.age).toFixed(1)} ${Y(p.principal).toFixed(1)}`).join(' ');
  const gainsArea = `${totalTop} ${principalBack} Z`;
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
      <p className="fm-yac-split"><i className="fm-dot fm-dot-principal" />내가 넣은 돈 {formatWon(cur.principal)} · <i className="fm-dot fm-dot-gains" />불어난 돈 {formatWon(cur.gains)}</p>
      <div
        className="fm-yac-canvas"
        style={{ touchAction: 'none' }}
        onPointerDown={pick}
        onPointerMove={(e) => { if (e.buttons) pick(e); }}
        onTouchStart={pick}
        onTouchMove={pick}
      >
        <svg viewBox={`0 0 ${W} ${H}`} preserveAspectRatio="none" role="img" aria-label="나이별 내 자산 그래프 — 원금과 불어난 돈 (눌러서 확인)">
          <path d={principalArea} className="fm-yac-area-principal" />
          <path d={gainsArea} className="fm-yac-area-gains" />
          <path d={totalTop} className="fm-yac-line" fill="none" />
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

function AssetJourney({ simulation }) {
  const rows = simulation.targetResult.rows || [];
  if (rows.length < 2) return null;
  const start = rows[0].financialAsset;
  const y1 = rows[1] ? rows[1].financialAsset - start : 0;
  const y5 = rows[5] ? rows[5].financialAsset - start : null;
  const save1 = rows[1] ? Math.max(0, rows[1].investmentAdded) : 0;
  const ret1 = Math.max(0, y1 - save1);
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
    <section className="fm-card fm-growth">
      <p className="fm-kicker">내 자산 흐름</p>
      <h2>시간이 지나면 자산은 이렇게 움직여요</h2>
      <YearlyAssetChart simulation={simulation} />
      <div className="fm-growth-grid">
        <div><small>1년 뒤</small><b>+{formatWon(Math.max(0, y1))}</b></div>
        {y5 != null && <div><small>5년 뒤</small><b>+{formatWon(Math.max(0, y5))}</b></div>}
        <div><small>은퇴 시점</small><b>{formatWon(simulation.retirementFinancialAsset)}</b></div>
      </div>
      {y1 > 0 && (
        <p className="fm-growth-split">1년 새 <b>+{formatWon(Math.max(0, y1))}</b> = 내 저축 <b>{formatWon(save1)}</b> + 투자수익 <b>{formatWon(ret1)}</b></p>
      )}
      <ol className="fm-road-list">
        {list.map((m, i) => (
          <li key={i} className={`fm-road-step${m.hi ? ' hi' : ''}`}>
            <span className="fm-road-age">{m.age}세</span>
            <span className="fm-road-body"><b>{m.label}</b>{m.sub && <em>{m.sub}</em>}</span>
          </li>
        ))}
      </ol>
      <p className="fm-growth-note">연 수익률 {simulation.inputs.annualReturnRate}% · 저축 반영 · 조건을 바꾸면 단계가 당겨져요</p>
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
    track('share', { type: 'result' });
    const ph = survivalPhrase(simulation);
    const earliest = simulation.earliestRetirementAge;
    const target = simulation.inputs.targetRetirementAge;
    const ret = simulation.inputs.annualReturnRate;
    const inf = simulation.inputs.inflationRate;
    let pos, tot;
    try { const rr = await fetchUserRank(earliest); if (rr && rr.total) { pos = rr.position; tot = rr.total; } } catch (e) { /* ignore */ }
    // 카드 이미지: 항상 프로덕션 /og(개인 숫자). 카카오 서버가 가져가므로 절대경로 firemap.kr.
    const img = new URL('https://firemap.kr/og');
    if (earliest) img.searchParams.set('ea', String(earliest));
    img.searchParams.set('target', String(target));
    img.searchParams.set('rw', ph.runway);
    img.searchParams.set('ret', String(ret));
    img.searchParams.set('inf', String(inf));
    if (pos && tot) { img.searchParams.set('pos', String(pos)); img.searchParams.set('tot', String(tot)); }
    img.searchParams.set('v', 'c2');
    const imageUrl = img.toString();
    // 클릭 시 이동할 짧은 링크
    const l = new URL('https://firemap.kr/s');
    if (earliest) l.searchParams.set('ea', String(earliest));
    l.searchParams.set('target', String(target));
    l.searchParams.set('rwy', ph.runway);
    l.searchParams.set('ret', String(ret));
    l.searchParams.set('inf', String(inf));
    if (pos && tot) { l.searchParams.set('pos', String(pos)); l.searchParams.set('tot', String(tot)); }
    const url = l.toString();
    const title = earliest ? `나는 ${earliest}세에 퇴사할 수 있어요 — 파이어맵` : '파이어맵 — 내 퇴사 가능 나이';
    const description = '파이어족들을 위한 커뮤니티 · 나는 또래 중 파이어 랭킹 몇 등?';
    track('share_summary_copy', { type: 'result_share' });
    // 1순위: 카카오톡 카드(개인 /og 이미지) — 긴 URL 텍스트 없이 카드 하나만 안정적으로 전송
    try {
      await shareToKakao({ title, description, imageUrl, linkUrl: url });
      return;
    } catch (e) { /* SDK 미로드/도메인 미등록 등 → 폴백 */ }
    // 폴백: 시스템 공유 / 복사
    if (navigator.share) {
      try { await navigator.share({ text: '파이어족들을 위한 커뮤니티 · 파이어맵', url }); return; }
      catch (e) { if (e && e.name === 'AbortError') return; }
    }
    try { await navigator.clipboard.writeText(url); window.alert('내 결과 링크를 복사했어요. 단톡방에 붙여넣어 보세요!'); }
    catch { onMove('share'); }
  };
  const shareOther = async () => {
    track('share', { type: 'result_other' });
    const ph = survivalPhrase(simulation);
    const earliest = simulation.earliestRetirementAge;
    let pos, tot;
    try { const rr = await fetchUserRank(earliest); if (rr && rr.total) { pos = rr.position; tot = rr.total; } } catch (e) { /* ignore */ }
    const l = new URL('https://firemap.kr/s');
    if (earliest) l.searchParams.set('ea', String(earliest));
    l.searchParams.set('target', String(simulation.inputs.targetRetirementAge));
    l.searchParams.set('rwy', ph.runway);
    l.searchParams.set('ret', String(simulation.inputs.annualReturnRate));
    l.searchParams.set('inf', String(simulation.inputs.inflationRate));
    if (pos && tot) { l.searchParams.set('pos', String(pos)); l.searchParams.set('tot', String(tot)); }
    const url = l.toString();
    if (navigator.share) {
      try { await navigator.share({ text: '파이어족들을 위한 커뮤니티 · 파이어맵', url }); return; }
      catch (e) { if (e && e.name === 'AbortError') return; }
    }
    try { await navigator.clipboard.writeText(url); window.alert('내 결과 링크를 복사했어요. 어디든 붙여넣어 보세요!'); }
    catch { /* ignore */ }
  };
  return (
    <main className="fm-screen fm-scroll fm-has-tabbar">
      <Header />
      <ResultSimTabs current="result" />
      <ResultHeroV2 simulation={simulation} />
      <div className="fm-rank-cta">
        <button type="button" className="fm-rank-cta-share" onClick={shareRank}>카카오톡 공유</button>
        <button type="button" className="fm-rank-cta-up" onClick={() => onMove('experiment')}>🎛️ 수치 바꿔보기</button>
      </div>
      <button type="button" className="fm-rank-cta-other" onClick={shareOther}>🔗 링크 복사 · 다른 앱으로 공유</button>
      <AccountCard kicker="내 기록 지키기 🔒" sub="방금 나온 퇴사 나이·등수와 적립·절약 기록을 닉네임+비밀번호로 저장하세요. 기기가 바뀌어도 같은 계정으로 이어집니다." />
      <OverseasHope inputs={inputs} simulation={simulation} onMove={onMove} />
      <AssetJourney simulation={simulation} />
      <TopLevers inputs={inputs} simulation={simulation} onChange={onChange} />
      <NextActions onMove={onMove} />
    </main>
  );
}
