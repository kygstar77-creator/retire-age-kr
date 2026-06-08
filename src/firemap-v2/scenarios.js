import { buildSimulation } from '../utils/retirementSimulator.js';

export function runwayText(simulation) {
  return simulation.targetResult.depletionAge ? `${simulation.targetResult.depletionAge}세` : `${simulation.inputs.simulationUntilAge}세 이상`;
}

export function scenarioEndAge(simulation) {
  return simulation.targetResult.depletionAge || simulation.inputs.simulationUntilAge;
}

export function buildScenario(inputs, patch) {
  return buildSimulation({ ...inputs, ...patch });
}

export function deltaText(base, next) {
  const diff = Math.max(0, scenarioEndAge(next) - scenarioEndAge(base));
  if (!base.targetResult.depletionAge && !next.targetResult.depletionAge) return '이미 장기 유지';
  return diff > 0 ? `${diff}년 개선` : '변화 작음';
}

export function fireStatus(score) {
  if (score < 35) return '개선 여지 큼';
  if (score < 70) return '조정하면 가까워짐';
  return '안정권에 가까움';
}

export function buildChartRows(simulation, improvedSimulation, inputs) {
  const rows = simulation.targetResult.rows
    .filter((row, index) => index === 0 || row.age % 5 === 0 || row.age === inputs.targetRetirementAge || row.age === inputs.simulationUntilAge)
    .slice(0, 12);
  const improvedRows = improvedSimulation.targetResult.rows;
  const max = Math.max(...rows.map((row) => Math.max(row.financialAsset, improvedRows.find((item) => item.age === row.age)?.financialAsset || 0)), 1);
  const chart = rows.map((row, index) => {
    const matched = improvedRows.find((item) => item.age === row.age) || row;
    const x = 34 + (index / Math.max(1, rows.length - 1)) * 286;
    return {
      age: row.age,
      x,
      current: row.financialAsset,
      improved: matched.financialAsset,
      currentY: 152 - (Math.max(0, row.financialAsset) / max) * 108,
      improvedY: 152 - (Math.max(0, matched.financialAsset) / max) * 108
    };
  });
  return { rows, chart, max };
}
