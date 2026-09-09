// 오늘(홈) — 계산한 사람의 매일 화면. 블록 7: 3숫자 · 오늘 한 걸음 · 미션 · 파이어 통 · 소식 한 줄 · 여정 · 카페.
// 팝업 0. 로그인 유도는 없음(설정·전체에서). 근거: 최종본 §3-1, Robinhood 위젯 % only, Qapital 규칙, Monzo Pot.
import { useEffect, useMemo, useState } from 'react';
import { TopBar, Card, SectionHead, Stat, Button, RuleChips, PotCard, ListRow, Notice, Sheet, Chips, Chip, toast } from '../../ui/index.js';
import { buildWidgetState, loggedToday } from '../../utils/widgetState.js';
import { prefs } from '../../utils/prefs.js';
import { account } from '../../utils/identity.js';
import { formatWon } from '../../firemap-v2/formatters.js';
import { dailyNeedOf, addSave, fmtAdvance, track } from '../../firemap-v2/dailyData.js';
import { notifySavingsChanged, reportBoard } from '../../utils/savingsEngine.js';
import { pushState } from '../../utils/firemapStateApi.js';
import { journeyStage, JOURNEY_STAGES } from '../../utils/journeyStage.js';
import { missionsFor } from '../../utils/missions.js';
import { sbRpc } from '../../utils/supabaseClient.js';
import { CAFE_URL } from '../../firemap-v2/links.js';
import ConfirmScreen from './ConfirmScreen.jsx';
import { RULES } from './rules.js';

const eok = (n) => formatWon(Math.round(n || 0));

function useNewsLine() {
  const [line, setLine] = useState(null);
  useEffect(() => {
    let alive = true;
    (async () => {
      const m = await sbRpc('fm_market_latest');
      if (!alive || !Array.isArray(m)) return;
      const spx = m.find((x) => x.symbol === '^spx');
      const kospi = m.find((x) => x.symbol === '^kospi');
      const parts = [];
      if (kospi && kospi.ret_7d != null) parts.push(`코스피 주간 ${kospi.ret_7d > 0 ? '+' : ''}${kospi.ret_7d}%`);
      if (spx && spx.ret_7d != null) parts.push(`S&P500 ${spx.ret_7d > 0 ? '+' : ''}${spx.ret_7d}%`);
      if (parts.length) setLine(`${parts.join(' · ')} — 내 파이어 나이엔 영향 없어요`);
    })();
    return () => { alive = false; };
  }, []);
  return line;
}

export default function Today({ simulation, onMove }) {
  const ws = useMemo(() => buildWidgetState(simulation), [simulation]);
  const acc = account();
  const hide = prefs.hideAmount();
  const dailyNeed = dailyNeedOf(simulation);
  const [tick, setTick] = useState(0);
  const [confirm, setConfirm] = useState(null); // {amount,label}
  const [customOpen, setCustomOpen] = useState(false);
  const [customVal, setCustomVal] = useState('');
  const [potOpen, setPotOpen] = useState(false);
  const [potName, setPotName] = useState(() => prefs.pot().name);
  const [potEmoji, setPotEmoji] = useState(() => prefs.pot().emoji);
  const newsLine = useNewsLine();
  const done = loggedToday();
  useEffect(() => { const h = () => setTick((n) => n + 1); window.addEventListener('fm-savings-changed', h); return () => window.removeEventListener('fm-savings-changed', h); }, []);
  void tick;

  const advSec = (amount) => (dailyNeed ? (amount / dailyNeed) * 86400 : 0);
  const rules = RULES.map((r) => ({ ...r, gain: dailyNeed ? fmtAdvance(advSec(r.amount)) : null }));

  const log = (amount, label) => {
    const next = addSave(amount, label);
    notifySavingsChanged();
    try { pushState('fm_save', next); } catch { /* ignore */ }
    reportBoard(simulation);
    track('save_log', { value: amount, item: label || '직접입력', from: 'today' });
    setConfirm({ amount, label, adv: fmtAdvance(advSec(amount)) });
  };
  const submitCustom = () => { const n = Number(String(customVal).replace(/[^0-9]/g, '')); if (n > 0) log(n, '직접 입력'); setCustomVal(''); setCustomOpen(false); };

  // 오늘의 미션 2지선다 — 단계별 풀에서 미완료 2개
  const stage = (() => { try { return journeyStage(simulation).stage; } catch { return 1; } })();
  const stageMeta = JOURNEY_STAGES.find((s) => s.n === stage) || JOURNEY_STAGES[0];
  const ctx = { calculated: ws.calculated, histLen: 0, saveTotal: 1, loggedIn: !!(acc && acc.handle), asset: ws.asset, notif: false };
  const missions = (() => { try { return missionsFor(stage, ctx).items.filter((m) => !m.done).slice(0, 2); } catch { return []; } })();
  const doneMap = prefs.missions();
  const missionsLeft = missions.filter((m) => !doneMap[m.id]);

  const savePot = () => { prefs.setPot({ name: potName.trim().slice(0, 16) || '내 파이어 통', emoji: potEmoji }); setPotOpen(false); toast.good('파이어 통 이름을 바꿨어요'); };
  const monthSaved = (() => { try { const fd = JSON.parse(localStorage.getItem('fm_daily') || 'null'); const ym = new Date(); const key = `${ym.getFullYear()}-${String(ym.getMonth() + 1).padStart(2, '0')}`; return Object.entries((fd && fd.days) || {}).filter(([k]) => k.startsWith(key)).reduce((a, [, v]) => a + (Number(v) || 0), 0); } catch { return 0; } })();

  return (
    <main className="fm-screen fm-scroll fm-has-tabbar ds-screen-gap">
      <TopBar
        onHome={() => onMove('home')}
        actions={<>
          <button type="button" className="ds-topbar__handle" onClick={() => onMove(acc && acc.handle ? 'account' : 'settings')} aria-label="설정"><span>{acc && acc.handle ? acc.handle : '설정'}</span> ⚙︎</button>
        </>}
      />

      {/* 1. 3숫자 카드 — 위젯과 같은 값 */}
      <Card>
        <div className="ds-three">
          <Stat label="파이어까지" value={ws.dday != null ? `D-${ws.dday.toLocaleString()}` : '—'} size="md" />
          <Stat label="연속 기록" value={<>{ws.streak}<span className="ds-stat__unit">일</span></>} size="md" />
          <Stat label="목표 달성" value={<>{ws.progressPct}<span className="ds-stat__unit">%</span></>} size="md" />
        </div>
        <p className="ds-caption ds-textcenter" style={{ margin: '8px 0 0' }}>
          {ws.earliestAge ? <>지금 계획이면 <b>{ws.earliestAge}세</b>에 파이어 · 필요 자산 {hide ? '•••' : eok(ws.target)}</> : '아직 파이어 나이가 안 나와요 · 조건을 바꿔보세요'}
          {' '}<button type="button" className="ds-link" onClick={() => onMove('result')}>결과 →</button>
        </p>
      </Card>

      {/* 2. 오늘 한 걸음 */}
      <Card variant="hero">
        <SectionHead kicker={done ? '오늘 기록 완료 ✓' : '오늘 한 걸음'} title={done ? '하나 더 하면 더 당겨져요' : '오늘 뭘 아꼈어요?'} desc={dailyNeed ? `하루 ${formatWon(dailyNeed)}씩 모으면 계획대로예요. 아낀 만큼 파이어가 앞당겨져요.` : '이미 목표 자산을 넘었어요. 아낀 돈은 여유로 쌓여요.'} size="sm" />
        <RuleChips rules={rules} onPick={(r) => log(r.amount, r.label)} onCustom={() => setCustomOpen(true)} />
      </Card>

      {/* 3. 오늘의 미션 2지선다 */}
      {missionsLeft.length > 0 && (
        <Card variant="soft">
          <SectionHead kicker={`${stageMeta.emoji} ${stage}단계 ${stageMeta.name}`} title="오늘의 미션, 하나만 골라요" size="sm" />
          <div className="ds-stack">
            {missionsLeft.map((m) => (
              <Button key={m.id} variant="secondary" size="md" full onClick={() => { if (m.to) { onMove(m.to); } else { prefs.setMissionDone(m.id); setTick((n) => n + 1); toast.good('미션 완료 🔥'); } }}>
                {m.label}{m.hint ? <span className="ds-caption"> · {m.hint}</span> : null}
              </Button>
            ))}
          </div>
        </Card>
      )}

      {/* 4. 파이어 통 */}
      <PotCard pot={{ name: potName, emoji: potEmoji }} current={ws.asset} target={ws.target} monthLabel="이번 달" monthValue={formatWon(monthSaved)} fmt={eok} hideAmount={hide} onEdit={() => setPotOpen(true)} />

      {/* 5. 소식 한 줄 */}
      <Card variant="soft" padding="md">
        <ListRow lead="📰" title={newsLine || '오늘의 소식'} desc={newsLine ? '지표는 참고만 · 파이어 후 하루·배당락 소식' : '시장 지표 · 파이어 후 하루 · 배당락'} onClick={() => onMove('news')} size="S" />
      </Card>

      {/* 6. 여정 · 7. 카페 */}
      <Card padding="md">
        <ListRow lead="🧭" title="내 파이어 여정" desc={`${stage}단계 ${stageMeta.name} · ${stageMeta.tag}`} onClick={() => onMove('journey')} size="S" />
        <ListRow lead="🟢" title="파이어맵 카페" desc="인증·봐주세요·파이어 후 하루" href={CAFE_URL} external size="S" />
      </Card>

      <Sheet open={customOpen} title="오늘 아낀 금액" onClose={() => setCustomOpen(false)}>
        <input className="ds-input num" autoFocus inputMode="numeric" value={customVal} onChange={(e) => setCustomVal(e.target.value.replace(/[^0-9]/g, ''))} placeholder="예: 12000" onKeyDown={(e) => { if (e.key === 'Enter') submitCustom(); }} />
        <Chips className="ds-mt-2">{[5000, 10000, 30000, 50000].map((n) => <Chip key={n} onClick={() => setCustomVal(String(n))}>{n / 10000}만</Chip>)}</Chips>
        <div className="ds-bottomcta"><Button variant="secondary" size="md" onClick={() => setCustomOpen(false)}>취소</Button><Button variant="primary" size="md" onClick={submitCustom}>기록</Button></div>
      </Sheet>

      <Sheet open={potOpen} title="파이어 통" onClose={() => setPotOpen(false)}>
        <Chips>{['🔥', '🏝️', '🏡', '✈️', '🐷', '🌱', '🎯'].map((e) => <Chip key={e} on={potEmoji === e} onClick={() => setPotEmoji(e)}>{e}</Chip>)}</Chips>
        <input className="ds-input ds-mt-3" maxLength={16} value={potName} onChange={(e) => setPotName(e.target.value)} placeholder="통 이름 (예: 제주 한 달 살기)" />
        <p className="ds-caption ds-mt-2">목표 금액은 파이어 필요 자산({eok(ws.target)})이에요. 결과에서 조건을 바꾸면 같이 바뀌어요.</p>
        <div className="ds-bottomcta"><Button variant="secondary" size="md" onClick={() => setPotOpen(false)}>취소</Button><Button variant="primary" size="md" onClick={savePot}>저장</Button></div>
      </Sheet>

      {confirm && <ConfirmScreen amount={confirm.amount} label={confirm.label} adv={confirm.adv} streak={buildWidgetState(simulation).streak} onMore={() => setConfirm(null)} onClose={() => setConfirm(null)} onCert={() => { setConfirm(null); onMove('result'); }} />}
      {!acc && prefs.certCount() === 0 && false && <Notice tone="neutral">로그인하면 기기를 바꿔도 기록이 이어져요.</Notice>}
    </main>
  );
}
