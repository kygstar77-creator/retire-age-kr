export const statusMeta = {
  stable: { label: '안정', summary: '퇴사 가능성이 높습니다' },
  caution: { label: '주의', summary: '완충자금 점검이 필요합니다' },
  risk: { label: '위험', summary: '목표 퇴사 나이에는 위험합니다' },
  neutral: { label: '정보', summary: '참고 지표입니다' }
};

export function formatWon(value) {
  return new Intl.NumberFormat('ko-KR', {
    style: 'currency',
    currency: 'KRW',
    maximumFractionDigits: 0
  }).format(Math.round(value || 0));
}

export function formatCompactMoney(value) {
  const amount = Number(value || 0);
  const abs = Math.abs(amount);

  if (abs >= 100000000) {
    const eok = amount / 100000000;
    return `${eok.toLocaleString('ko-KR', {
      maximumFractionDigits: eok >= 10 ? 0 : 1
    })}억 원`;
  }

  if (abs >= 10000) {
    return `${(amount / 10000).toLocaleString('ko-KR', {
      maximumFractionDigits: 0
    })}만 원`;
  }

  return formatWon(amount);
}

export function formatEok(value) {
  const eok = Number(value || 0) / 100000000;
  return `${eok.toLocaleString('ko-KR', {
    maximumFractionDigits: 1,
    minimumFractionDigits: Math.abs(eok) < 10 && eok !== 0 ? 1 : 0
  })}억 원`;
}

export function formatAge(age) {
  return age ? `${age}세` : '고갈 없음';
}

export function formatPercent(value) {
  return `${Number(value || 0).toLocaleString('ko-KR', {
    maximumFractionDigits: 1,
    minimumFractionDigits: 1
  })}%`;
}
