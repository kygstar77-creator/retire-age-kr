import { useEffect, useState } from 'react';
import Header from './Header.jsx';
import { formatWon } from '../../firemap-v2/formatters.js';
import { buildScenario, fireStatus, runwayText, scenarioEndAge, survivalPhrase } from '../../firemap-v2/scenarios.js';
import { screens, NEXT_ACTION_META } from '../../firemap-v2/screens.js';
import { statsRank } from '../../firemap-v2/rank.js';
import { submitScore, fetchUserRank } from '../../utils/firemapScoresApi.js';
import { saveRankSnapshot } from '../../firemap-v2/rankHistory.js';

function RankHero({ simulation }) {
  const base = statsRank(simulation);
  const [live, setLive] = useState(null);
  const score = simulation.survivalScore;

  useEffect(() => {
    let alive = true;
    saveRankSnapshot({ percentile: base.percentile, grade: base.grade, score });
    (async () => {
      try {
        const key = `fm_score_sent_${score}`;
        if (!sessionStorage.getItem(key)) {
          await submitScore({
            fireScore: score,
            ageBand: base.ageBand,
            survivalAge: (simulation.targetResult && simulation.targetResult.depletionAge) || simulation.inputs.simulationUntilAge
          });
          sessionStorage.setItem(key, '1');
        }
      } catch { /* ignore */ }
      const r = await fetchUserRank(score);
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
      </div>
      {live
        ? <p className="fm-rank-line">함께 계산한 {live.total.toLocaleString()}명 중 <b>{live.position.toLocaleString()}등</b></p>
        : <p className="fm-rank-line">함께 계산한 사용자 중 등수 집계 중…</p>}
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

function TopLevers({ inputs, simulation }) {
  const baseCost = Number(inputs.monthlyLivingCost || 0);
  const lowerCostValue = Math.max(1000000, baseCost >= 2500000 ? baseCost - 1000000 : Math.round(baseCost * 0.8 / 100000) * 100000);
  const candidates = [
    ['생활비', `생활비 ${formatWon(lowerCostValue)}원으로 줄이면`, buildScenario(inputs, { monthlyLivingCost: lowerCostValue })],
    ['현금흐름', '퇴사 후 월 100만 더 벌면', buildScenario(inputs, { partTimeIncomeAfterRetirement: inputs.partTimeIncomeAfterRetirement + 1000000 })],
    ['퇴사시점', '1년 더 일하면', buildScenario(inputs, { targetRetirementAge: inputs.targetRetirementAge + 1 })],
    ['저축액', '월 100만 더 저축하면', buildScenario(inputs, { monthlyInvestment: inputs.monthlyInvestment + 1000000 })]
  ];
  const baseAge = scenarioEndAge(simulation);
  const topTwo = candidates.map((item) => [...item, scenarioEndAge(item[2]) - baseAge]).sort((a, b) => b[3] - a[3]).slice(0, 2);
  return (
    <section>
      <h2 className="fm-section-title">지금 가장 효과 큰 두 가지</h2>
      <p className="fm-section-sub">이렇게 바꾸면 자산이 더 오래 버텨요</p>
      <div className="fm-improve-grid fm-improve-grid-two">
        {topTwo.map(([tag, title, scenario, diff]) => (
          <article className="fm-improve-card" key={title}>
            <em>{tag}</em><h3>{title}</h3><strong>{leverGain(diff)}</strong><p>{runwayText(scenario)}까지 버텨요</p>
          </article>
        ))}
      </div>
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

export default function Result({ inputs, simulation, onMove, onEditFinalQuestion }) {
  return (
    <main className="fm-screen fm-scroll">
      <Header />
      <RankHero simulation={simulation} />
      <ResultHero simulation={simulation} />
      <TopLevers inputs={inputs} simulation={simulation} />
      <NextActions onMove={onMove} />
      <div className="fm-ad">광고</div>
    </main>
  );
}
