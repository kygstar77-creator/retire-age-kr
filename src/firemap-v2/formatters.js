export function cleanNumber(value) {
  return Number(String(value ?? '').replace(/[^\d.-]/g, '')) || 0;
}

export function formatWon(value) {
  const amount = cleanNumber(value);
  if (Math.abs(amount) >= 100000000) {
    const eok = amount / 100000000;
    return `${Number.isInteger(eok) ? eok.toFixed(0) : eok.toFixed(1)}억`;
  }
  if (Math.abs(amount) >= 10000) return `${Math.round(amount / 10000).toLocaleString('ko-KR')}만`;
  return `${Math.round(amount).toLocaleString('ko-KR')}원`;
}

export function formatInputWon(value) {
  const amount = Math.max(0, cleanNumber(value));
  const eok = Math.floor(amount / 100000000);
  const man = Math.round((amount % 100000000) / 10000);
  if (eok > 0 && man > 0) return `${eok}억 ${man.toLocaleString('ko-KR')}만`;
  if (eok > 0) return `${eok}억`;
  if (man > 0) return `${man.toLocaleString('ko-KR')}만`;
  return '0원';
}

export function formatEok(value) {
  return `${(Math.max(0, cleanNumber(value)) / 100000000).toFixed(1)}억`;
}

export function formatValue(value, type, key) {
  if (type === 'age') return `${cleanNumber(value)}세`;
  return key === 'financialAsset' ? formatInputWon(value) : formatWon(value);
}
