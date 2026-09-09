// 이번 달 계획 저축 — 실제로 넣은 돈을 기록. 월 계획을 넘긴 만큼만 파이어가 당겨진다(savingsEngine 모델 그대로).
import { useState, useEffect } from 'react';
import { Card, SectionHead, ProgressBar, Button, Sheet, Chips, Chip, Dialog, toast } from '../../ui/index.js';
import { pushState, pullKey, pushDailyMerged, mergeDailyValues } from '../../utils/firemapStateApi.js';
import { notifySavingsChanged, reportBoard } from '../../utils/savingsEngine.js';
import { track } from '../../firemap-v2/dailyData.js';
import { formatWon } from '../../firemap-v2/formatters.js';
import { todayStr, yesterdayStr, monthStr } from '../../utils/dates.js';

const KEY = 'fm_daily';
const load = () => { try { return JSON.parse(localStorage.getItem(KEY) || 'null'); } catch { return null; } };
const save = (o) => { try { localStorage.setItem(KEY, JSON.stringify(o)); } catch { /* ignore */ } };

export default function DepositCard({ simulation }) {
  const inp = (simulation && simulation.inputs) || {};
  const monthlyPlan = inp.monthlyInvestment || 0;
  const suggested = monthlyPlan > 0 ? Math.max(1000, Math.round(monthlyPlan / 30 / 1000) * 1000) : 10000;
  const [cfg, setCfg] = useState(() => load() || { days: {} });
  const [open, setOpen] = useState(false);
  const [amt, setAmt] = useState('');
  const [day, setDay] = useState('today');
  const [askReset, setAskReset] = useState(false);

  useEffect(() => {
    let alive = true;
    pullKey(KEY).then((v) => { if (alive && v && v.days) { const merged = mergeDailyValues(load() || { days: {} }, v); save(merged); setCfg(merged); notifySavingsChanged(); } });
    const h = () => { const v = load(); if (v) setCfg(v); };
    window.addEventListener('fm-savings-changed', h);
    return () => { alive = false; window.removeEventListener('fm-savings-changed', h); };
  }, []);

  const days = cfg.days || {};
  const today = todayStr(); const yest = yesterdayStr(); const m = monthStr();
  const sel = day === 'yesterday' ? yest : today;
  const monthTotal = Object.entries(days).filter(([k]) => k.startsWith(m)).reduce((a, [, v]) => a + (Number(v) || 0), 0);
  const pct = monthlyPlan > 0 ? Math.max(0, Math.min(100, (monthTotal / monthlyPlan) * 100)) : 0;
  const loggedToday = days[today] != null;

  const commit = (date, value, mode) => {
    const nextDays = { ...days };
    if (value > 0) nextDays[date] = value; else delete nextDays[date];
    const next = { ...cfg, days: nextDays };
    save(next); setCfg(next); notifySavingsChanged();
    pushDailyMerged(next).then((merged) => { save(merged); setCfg(merged); notifySavingsChanged(); reportBoard(simulation); });
    try { track('deposit_log', { mode, amt: value }); } catch { /* ignore */ }
  };
  const quick = () => { commit(today, suggested, 'quick'); toast.good(`오늘 ${formatWon(suggested)} 기록했어요`); };
  const openSheet = () => { setDay('today'); setAmt(String(days[today] || suggested)); setOpen(true); };
  const pick = (c) => { setDay(c); const d = c === 'yesterday' ? yest : today; setAmt(days[d] != null ? String(days[d]) : (c === 'today' ? String(suggested) : '')); };
  const submit = () => { const v = Math.max(0, Math.round(Number(String(amt).replace(/[^0-9]/g, '')) || 0)); commit(sel, v, 'manual'); setOpen(false); if (v > 0) toast.good(`${day === 'yesterday' ? '어제' : '오늘'} ${formatWon(v)} 기록했어요`); };
  const reset = () => { const next = { days: {} }; save(next); setCfg(next); pushState(KEY, next); notifySavingsChanged(); reportBoard(simulation); setAskReset(false); toast('저축 기록을 지웠어요'); };

  return (
    <Card>
      <SectionHead size="sm" kicker="이번 달 계획 저축" title={monthlyPlan > 0 ? <>이번 달 <b className="num">{formatWon(monthTotal)}</b> / 목표 {formatWon(monthlyPlan)}</> : <>이번 달 <b className="num">{formatWon(monthTotal)}</b> 넣었어요</>} desc={monthlyPlan > 0 ? (monthTotal >= monthlyPlan ? '계획 달성 · 더 넣는 만큼 파이어가 당겨져요' : '계획대로 넣으면 지금 파이어 나이 그대로예요') : '계산하면 월 계획 대비 진행이 보여요'} action={Object.keys(days).length > 0 ? <Button variant="ghost" size="sm" onClick={() => setAskReset(true)}>지우기</Button> : null} />
      {monthlyPlan > 0 && <ProgressBar value={pct} max={100} right={`${Math.round(pct)}%`} tone={pct >= 100 ? 'good' : undefined} />}
      <div className="ds-bottomcta">
        {loggedToday
          ? <Button variant="secondary" size="md" full onClick={openSheet}>오늘 {formatWon(days[today])} 기록됨 · 수정</Button>
          : <>
            {monthlyPlan > 0 && <Button variant="primary" size="md" onClick={quick}>오늘 {formatWon(suggested)} 넣었어요</Button>}
            <Button variant="secondary" size="md" onClick={openSheet}>{monthlyPlan > 0 ? '다른 금액' : '오늘 저축 기록하기'}</Button>
          </>}
      </div>
      <Sheet open={open} title="실제로 넣은 돈" onClose={() => setOpen(false)}>
        <Chips><Chip on={day === 'today'} onClick={() => pick('today')}>오늘</Chip><Chip on={day === 'yesterday'} onClick={() => pick('yesterday')}>어제</Chip></Chips>
        <input className="ds-input num ds-mt-3" inputMode="numeric" value={amt} onChange={(e) => setAmt(e.target.value.replace(/[^0-9]/g, ''))} placeholder={String(suggested)} autoFocus />
        <p className="ds-caption ds-mt-2">= {formatWon(Number(amt) || 0)} · 빠뜨린 날은 달력에서 채울 수 있어요</p>
        <div className="ds-bottomcta"><Button variant="secondary" size="md" onClick={() => setOpen(false)}>취소</Button><Button variant="primary" size="md" onClick={submit}>저장</Button></div>
      </Sheet>
      <Dialog open={askReset} title="저축 기록을 모두 지울까요?" desc="되돌릴 수 없어요." primary={{ label: '지우기', variant: 'danger', onClick: reset }} secondary={{ label: '취소' }} onClose={() => setAskReset(false)} />
    </Card>
  );
}
