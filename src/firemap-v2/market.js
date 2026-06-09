import data from './marketData.json';

const FALLBACK_FX = { USD: 1380, THB: 40, VND: 0.055, MYR: 310 };

export function getFx(currency) {
  const v = data?.fxToKrw?.[currency];
  return typeof v === 'number' && v > 0 ? v : (FALLBACK_FX[currency] || 1);
}
export function marketAsOf() {
  return data?.asOf || '';
}
