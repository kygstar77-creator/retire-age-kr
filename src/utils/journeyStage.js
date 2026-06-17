// 파이어 여정 단계 판정 — 기존 데이터만 사용(신규 수집 0). 순수 함수.
// 6단계: 1 각성 · 2 설계 · 3 실행 · 4 가속 · 5 임박 · 6 파이어
import { inputsIsReal } from './retirementSimulator.js';

const read = (k) => { try { return JSON.parse(localStorage.getItem(k) || 'null'); } catch { return null; } };

export const JOURNEY_STAGES = [
  { n: 1, key: 'awaken', name: '각성', emoji: '🔥', tag: '내 파이어 나이 알기' },
  { n: 2, key: 'plan', name: '설계', emoji: '🗺️', tag: '목표까지의 길' },
  { n: 3, key: 'start', name: '실행', emoji: '🌱', tag: '추적 시작' },
  { n: 4, key: 'accel', name: '가속', emoji: '📈', tag: '진짜 전진' },
  { n: 5, key: 'near', name: '임박', emoji: '🎯', tag: '코스트파이어·검증' },
  { n: 6, key: 'fire', name: '파이어', emoji: '🏝️', tag: '도달 & 이후' }
];

// opts: { advanceDays, peerAvg, assetHistoryLen, notifGranted } — 없으면 로컬에서 직접 읽음
export function journeyStage(simulation, opts = {}) {
  const inp = (simulation && simulation.inputs) || {};
  const earliest = simulation && simulation.earliestRetirementAge;
  const curAge = Number(inp.currentAge) || 0;
  const targetAge = Number(inp.targetRetirementAge) || 0;
  const asset = Number(inp.financialAsset) || 0;
  const monthlyInvestment = Number(inp.monthlyInvestment) || 0;
  const target = Math.max(0, Math.round((simulation && simulation.requiredFireAssetByFourPercent) || 0));
  const pct = target > 0 ? Math.max(0, Math.min(100, Math.round((asset / target) * 100))) : 0;

  let calculated = false; try { calculated = !!localStorage.getItem('firemap-inputs-v3'); } catch { /* ignore */ }
  const real = inputsIsReal(inp);
  const histLen = (opts.assetHistoryLen != null) ? opts.assetHistoryLen : ((read('fm_asset_history') || []).length);
  const sv = read('fm_save'); const saveTotal = sv ? Math.max(0, Number(sv.total) || 0) : 0;
  const fd = read('fm_daily'); const dailyN = (fd && fd.days) ? Object.keys(fd.days).length : 0;
  let notif = opts.notifGranted;
  if (notif == null) { try { notif = (typeof Notification !== 'undefined') && Notification.permission === 'granted'; } catch { notif = false; } }
  const hasTracking = histLen >= 1 || saveTotal > 0 || dailyN > 0 || !!notif;
  const hasPlan = monthlyInvestment > 0 || asset > 0 || (Number(inp.savingYears) || 0) > 0;
  const peerAvg = opts.peerAvg || null;
  const adv = Number(opts.advanceDays) || 0;

  let stage;
  if (!calculated || !earliest) stage = 1;
  else if ((target > 0 && asset >= target) || (curAge > 0 && earliest && curAge >= earliest)) stage = 6;
  else if ((target > 0 && pct >= 80) || (earliest && earliest - curAge <= 3 && earliest > curAge)) stage = 5;
  else if (hasTracking && (histLen >= 2 || asset >= 100000000 || (peerAvg && earliest && earliest < peerAvg))) stage = 4;
  else if (hasTracking) stage = 3;
  else if (real && targetAge > 0 && hasPlan) stage = 2;
  else stage = 1;

  const NEXT = {
    1: { label: '결과 자세히 보고 내 프로필 만들기', to: 'result' },
    2: { label: '조건 바꿔 파이어 당겨보기', to: 'experiment' },
    3: { label: '이번 달 저축·절약 기록하기', to: 'save' },
    4: { label: '파이어 더 당기는 도구 보기', to: 'tools' },
    5: { label: '파이어 리얼리티 체크 (건보·세금)', to: 'dependent' },
    6: { label: '파이어족 라운지 가기', to: 'community' }
  };

  const milestones = [
    { label: '첫 계산', done: calculated && !!earliest },
    { label: '목표 설정', done: targetAge > 0 && hasPlan },
    { label: '추적 시작', done: hasTracking },
    { label: '1억 돌파', done: asset >= 100000000 },
    { label: '3억 돌파', done: asset >= 300000000 },
    { label: '10억 돌파', done: asset >= 1000000000 },
    { label: '파이어 달성', done: stage === 6 }
  ];

  const signals = { calculated, earliest, curAge, targetAge, asset, monthlyInvestment, histLen, saveTotal, dailyN, notif: !!notif, hasTracking, hasPlan, peerAvg, pct, adv };

  return {
    stage,
    stages: JOURNEY_STAGES,
    current: JOURNEY_STAGES[stage - 1],
    nextStep: NEXT[stage],
    pct,
    momentum: adv > 0.5 ? { advanceDays: adv } : null,
    milestones,
    signals,
    target,
    asset,
    earliest,
    targetAge
  };
}
