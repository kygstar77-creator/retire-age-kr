export const defaultTaxInputs = {
  annualDividendIncome: 12000000,
  dividendWithholdingRate: 15.4,
  financialIncomeThreshold: 20000000,
  additionalDividendTaxRate: 0,
  foreignStockGain: 10000000,
  foreignStockBasicDeduction: 2500000,
  foreignStockTaxRate: 22,
  targetMonthlyDividendAfterTax: 2000000,
  expectedDividendYield: 7,
  dividendReinvestmentRate: 0
};

export function calculateInvestmentTaxes(inputs = {}) {
  const data = normalizeTaxInputs({ ...defaultTaxInputs, ...inputs });
  const dividendTax = calculateDividendTax(data);
  const foreignStockTax = calculateForeignStockGainTax(data);
  const requiredAsset = calculateRequiredDividendAsset(data);

  return {
    inputs: data,
    dividendTax,
    foreignStockTax,
    requiredAsset
  };
}

export function normalizeTaxInputs(inputs) {
  return Object.fromEntries(
    Object.entries(inputs).map(([key, value]) => [key, Number(String(value ?? '').replace(/[^\d.-]/g, '')) || 0])
  );
}

function calculateDividendTax(data) {
  const grossDividend = Math.max(0, data.annualDividendIncome);
  const withholdingTax = grossDividend * toRate(data.dividendWithholdingRate);
  const amountAboveThreshold = Math.max(0, grossDividend - data.financialIncomeThreshold);
  const additionalTaxEstimate = amountAboveThreshold * toRate(data.additionalDividendTaxRate);
  const totalTax = withholdingTax + additionalTaxEstimate;
  const afterTaxDividend = Math.max(0, grossDividend - totalTax);
  const monthlyAfterTaxDividend = afterTaxDividend / 12;

  return {
    grossDividend,
    withholdingTax,
    amountAboveThreshold,
    additionalTaxEstimate,
    totalTax,
    afterTaxDividend,
    monthlyAfterTaxDividend,
    effectiveTaxRate: grossDividend > 0 ? (totalTax / grossDividend) * 100 : 0
  };
}

function calculateForeignStockGainTax(data) {
  const gain = Math.max(0, data.foreignStockGain);
  const taxableGain = Math.max(0, gain - data.foreignStockBasicDeduction);
  const tax = taxableGain * toRate(data.foreignStockTaxRate);
  const afterTaxGain = Math.max(0, gain - tax);

  return {
    gain,
    basicDeduction: data.foreignStockBasicDeduction,
    taxableGain,
    tax,
    afterTaxGain,
    effectiveTaxRate: gain > 0 ? (tax / gain) * 100 : 0
  };
}

function calculateRequiredDividendAsset(data) {
  const targetAnnualAfterTaxDividend = Math.max(0, data.targetMonthlyDividendAfterTax) * 12;
  const yieldRate = toRate(data.expectedDividendYield);
  const taxRate = toRate(data.dividendWithholdingRate + data.additionalDividendTaxRate);
  const reinvestmentRate = toRate(data.dividendReinvestmentRate);
  const spendableRate = Math.max(0, 1 - taxRate - reinvestmentRate);
  const netYieldRate = yieldRate * spendableRate;
  const requiredAsset = netYieldRate > 0 ? targetAnnualAfterTaxDividend / netYieldRate : 0;

  return {
    targetAnnualAfterTaxDividend,
    expectedDividendYield: data.expectedDividendYield,
    spendableRate: spendableRate * 100,
    netYieldRate: netYieldRate * 100,
    requiredAsset
  };
}

function toRate(value) {
  return Number(value || 0) / 100;
}
