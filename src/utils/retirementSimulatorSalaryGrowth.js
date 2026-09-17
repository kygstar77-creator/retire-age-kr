import { buildSimulation } from './retirementSimulator.js';

const toNum = (value) => Number(value || 0);

export function monthlyInvestmentWithSalaryGrowth(inputs) {
  const years = Math.max(0, toNum(inputs.targetRetirementAge) - toNum(inputs.currentAge));
  const monthly = toNum(inputs.monthlyInvestment);
  const rate = toNum(inputs.salaryGrowthRate) / 100;
  if (!monthly || !rate || years <= 1) return monthly;
  const total