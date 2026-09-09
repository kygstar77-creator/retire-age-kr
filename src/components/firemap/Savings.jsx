// 저축 — 파이어 통(Monzo Pot) · 오늘 규칙(Qapital) · 이번 달 계획 저축 · 26주 도전(카뱅) · 미션 · 달력은 시트.
// 293행·데드 분기·명언·넛지·설명 2·랭킹 카드 → 6블록. 모델은 그대로(fm_save 절약 + fm_daily 적립), UI만 하나로.
import { useEffect, useState } from 'react';
import { TopBar, PotCard, Card, SectionHead, RuleChips, Chips, Chip, Button, Sheet, IconButton, Notice, toast } from '../../ui/index.js';
import DepositCard from './DepositCard.jsx';
import DepositCalendar from './DepositCalendar.jsx';
import ConfirmScreen from './ConfirmScreen.jsx';
import { RULES } from './rules.js';
import { pushState, pullKey } from '../../utils/firemapStateApi.js';
import { notifySavingsChanged, reportBoard, hasCalculated } from '../../utils/savingsEngine.js';
import { fmtAdvance, dailyNeedOf, addSave, readJSON, track } from '../../firemap-v2/dailyData.js';
import { formatWon } from '../../firemap-v2/formatters.js';
import { buildWidgetState, streakOf } from '../../utils/widgetState.js';
import { prefs } from '../../utils/prefs.js';
import { monthStr } from '../../utils/dates.js';

const eok = (n) => formatWon(Math.round(n || 0));
const WEEK_MS = 7 * 86400000;

function week26State() {
  const w = prefs.week26();
  if (!w || !w.startDate) return null;
  const start = new Date(w.startDate).getTime();
  const idx = Math.min(26, Math.floor((Date.now() - start) / WEEK_MS) + 1);
  const weeks = w.weeks || {};
  const done = Object.keys(weeks).length;
  const total = Object.values(weeks).reduce((a, b) => a + (Number(b) || 0), 0);
  return { ...w, idx, done, total, thisDone: !!weeks[idx] };
}

export default function Savings({ simulation, onMove }) {
  const [tick, setTick] = useState(0);
  const [confirm, setConfirm] = useState(null);
  const [calOpen, setCalOpen] = useState(false);
  const [customOpen, setCustomOpen] = useState(false);
  const [customVal, setCustomVal] = useState('');
  const [potOpen, setPotOpen] = useState(false);
  const [potName, setPotName] = useState(() => prefs.pot().name);
  const [potEmoji, setPotEmoji] = useState(() => prefs.pot().emoji);
  const dailyNeed = dailyNeedOf(simulation);
  const ws = buildWidgetState(simulation);
  const hide = prefs.hideAmount();
  void tick;

  useEffect(() => {
    track('save_tab_view');
    pullKey('fm_save').then((v) => { if (v) { try { localStorage.setItem('fm_save', JSON.stringify(v)); } catch { /* ignore */ } setTick((n) => n + 1); } });
    const h = () => setTick((n) => n + 1);
    window.addEventListener('fm-savings-changed', h);
    return () => window.removeEventListener('fm-savings-changed', h);
  }, []);

  const advSec = (amount) => (dailyNeed ? (amount / dailyNeed) * 86400 : 0);
  const rules = RULES.map((r) => ({ ...r, gain: dailyNeed ? fmtAdvance(advSec(r.amount)) : null }));
  const log = (amount, label) => {
    const next = addSave(amount, label);
    notifySavingsChanged();
    try { pushState('fm_save', next); } catch { /* ignore */ }
    reportBoard(simulation);
    track('save_log', { value: amount, item: label || '직접입력', from: 'save' });
    setConfirm({ amount, label, adv: fmtAdvance(advSec(amount)) });
  };
  const submitCustom = () => { const n = Number(String(customVal).replace(/[^0-9]/g, '')); if (n > 0) log(n, '직접 입력'); setCustomVal(''); setCustomOpen(false); };

  const sv = readJSON('fm_save') || {};
  const totalSaved = sv.total || 0;
  const streak = streakOf();
  const w26 = week26State();
  const start26 = () => { prefs.setWeek26({ startDate: new Date().toISOString(), weeks: {} }); setTick((n) => n + 1); toast.good('26주 도전 시작! 이번 주 1천원부터'); track('w26_start', {}); };
  const tick26 = () => {
    const w = prefs.week26(); if (!w) return;
    const s = week26State(); if (!s || s.thisDone) return;
    const amt = s.idx * 1000;
    w.weeks = { ...(w.weeks || {}), [s.idx]: amt };
    prefs.setWeek26(w);
    log(amt, `26주 도전 ${s.idx}주차`);
  };
  const monthSaved = (() => { try { const fd = JSON.parse(localStorage.getItem('fm_daily') || 'null'); const m = monthStr(); return Object.entries((fd && fd.days) || {}).filter(([k]) => k.startsWith(m)).reduce((a, [, v]) => a + (Number(v) || 0), 0); } catch { return 0; } })();
  const savePot = () => { prefs.setPot({ name: potName.trim().slice(0, 16) || '내 파이어 통', emoji: potEmoji }); setPotOpen(false); toast.good('파이어 통을 바꿨어요'); };

  return (
    <main className="fm-screen fm-scroll fm-has-tabbar ds-screen-gap">
      <TopBar title="저축" onHome={() => onMove('home')} actions={<><IconButton label="달력" onClick={() => setCalOpen(true)}>📅</IconButton><IconButton label="저축 리그" onClick={() => onMove('ranking')}>🏆</IconButton></>} />

      {!hasCalculated() && <Notice tone="accent" icon="🧮" title="먼저 파이어 나이를 계산하면"><button type="button" className="ds-link" onClick={() => onMove('question')}>아낀 돈이 파이어를 며칠 당기는지 시간으로 보여줘요 →</button></Notice>}

      <PotCard pot={{ name: potName, emoji: potEmoji }} current={ws.asset} target={ws.target} monthLabel="이번 달" monthValue={formatWon(monthSaved)} fmt={eok} hideAmount={hide} onEdit={() => setPotOpen(true)} />

      <Card variant="hero">
        <SectionHead size="sm" kicker={`🔥 ${streak}일 연속`} title="오늘 아낀 돈, 통에 넣기" desc={totalSaved > 0 ? `지금까지 ${formatWon(totalSaved)} 아꼈어요${dailyNeed && fmtAdvance(advSec(totalSaved)) ? ` · 파이어 ${fmtAdvance(advSec(totalSaved))} 당김` : ''}` : '아낀 돈은 전부 파이어를 당기는 보너스예요'} />
        <RuleChips rules={rules} onPick={(r) => log(r.amount, r.label)} onCustom={() => setCustomOpen(true)} />
      </Card>

      <DepositCard simulation={simulation} onMove={onMove} />

      <Card>
        <SectionHead size="sm" kicker="26주 도전" title={w26 ? `${w26.idx}주차 · ${w26.done}/26 완료` : '1천원부터 매주 1천원씩 더'} desc={w26 ? `지금까지 ${formatWon(w26.total)} · 완주하면 351,000원` : '카카오뱅크 800만 좌가 한 그 방식. 26주 뒤 351,000원.'} />
        {w26 ? (
          <>
            <Chips>{Array.from({ length: 26 }, (_, i) => i + 1).map((n) => <Chip key={n} on={!!(w26.weeks || {})[n]} onClick={n === w26.idx && !w26.thisDone ? tick26 : undefined}>{n}</Chip>)}</Chips>
            <Button variant={w26.thisDone ? 'secondary' : 'primary'} size="md" full className="ds-mt-3" disabled={w26.thisDone} onClick={tick26}>{w26.thisDone ? `이번 주 ${formatWon(w26.idx * 1000)} 완료 ✓` : `이번 주 ${formatWon(w26.idx * 1000)} 넣기`}</Button>
          </>
        ) : <Button variant="secondary" size="md" full onClick={start26}>26주 도전 시작</Button>}
      </Card>

      <Sheet open={calOpen} title="저축 달력" onClose={() => setCalOpen(false)}>
        <DepositCalendar editable simulation={simulation} />
      </Sheet>
      <Sheet open={customOpen} title="오늘 아낀 금액" onClose={() => setCustomOpen(false)}>
        <input className="ds-input num" autoFocus inputMode="numeric" value={customVal} onChange={(e) => setCustomVal(e.target.value.replace(/[^0-9]/g, ''))} placeholder="예: 12000" onKeyDown={(e) => { if (e.key === 'Enter') submitCustom(); }} />
        <Chips className="ds-mt-2">{[5000, 10000, 30000, 50000].map((n) => <Chip key={n} onClick={() => setCustomVal(String(n))}>{n / 10000}만</Chip>)}</Chips>
        <div className="ds-bottomcta"><Button variant="secondary" size="md" onClick={() => setCustomOpen(false)}>취소</Button><Button variant="primary" size="md" onClick={submitCustom}>기록</Button></div>
      </Sheet>
      <Sheet open={potOpen} title="파이어 통" onClose={() => setPotOpen(false)}>
        <Chips>{['🔥', '🏝️', '🏡', '✈️', '🐷', '🌱', '🎯'].map((e) => <Chip key={e} on={potEmoji === e} onClick={() => setPotEmoji(e)}>{e}</Chip>)}</Chips>
        <input className="ds-input ds-mt-3" maxLength={16} value={potName} onChange={(e) => setPotName(e.target.value)} placeholder="통 이름" />
        <div className="ds-bottomcta"><Button variant="secondary" size="md" onClick={() => setPotOpen(false)}>취소</Button><Button variant="primary" size="md" onClick={savePot}>저장</Button></div>
      </Sheet>
      {confirm && <ConfirmScreen amount={confirm.amount} label={confirm.label} adv={confirm.adv} streak={streakOf()} onMore={() => setConfirm(null)} onClose={() => setConfirm(null)} onCert={() => { setConfirm(null); onMove('result'); }} />}
    </main>
  );
}
