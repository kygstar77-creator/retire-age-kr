// 내 파이어 여정 — 6단계 중 지금 어디인지(StatHero) · 6단계 목록 · 다음 한 걸음 · 단계별 할 일 · 읽어볼 글.
import { useEffect, useMemo, useState } from 'react';
import { TopBar, StatHero, ProgressBar, ListGroup, ListRow, Badge, Card, SectionHead, Button, Chip, Fold, toast } from '../../ui/index.js';
import { journeyStage } from '../../utils/journeyStage.js';
import { missionsFor, setManual } from '../../utils/missions.js';
import { computeProgress } from '../../utils/savingsEngine.js';
import { getAssetHistory } from '../../utils/assetHistory.js';
import { fetchAggregates } from '../../utils/firemapScoresApi.js';
import { account } from '../../utils/identity.js';
import { track } from '../../firemap-v2/dailyData.js';
import '../../ui/screens/journey.css';

const DESC = {
  1: '내 파이어 나이를 알았어요. 유형과 또래 위치를 확인할 차례예요.',
  2: '목표 나이와 월 저축을 정해요. 바꿔보기로 경로를 맞춰요.',
  3: '가장 긴 구간이에요. 매달 기록하면 숫자가 살아 움직여요.',
  4: '생활비를 낮추거나 부업·배당을 더하면 몇 년씩 당겨져요.',
  5: '건보료·연금 공백·인출 순서를 점검해야 안전한 파이어예요.',
  6: '축하해요. 이제 돈이 안 떨어지게 지키는 단계예요.'
};
const NEXT_LABEL = { 1: '결과 보고 내 프로필 만들기', 2: '조건 바꿔 파이어 당기기', 3: '이번 달 저축 기록하기', 4: '파이어 더 당기는 도구 보기', 5: '건보료·세금 점검하기', 6: '카페에서 파이어족 만나기' };

const READS = {
  1: [['파이어 종류 · 린·팻·코스트·바리스타', 'fire-types'], ['나이별 파이어 전략', 'fire-by-age'], ['4%룰이란', 'four-percent-rule'], ['물가와 은퇴 자금', 'inflation-retirement']],
  2: [['목표 자산 시나리오', 'asset-target-scenarios'], ['코스트파이어 계산', 'coast-fire-calculation'], ['ISA·연금계좌 절세', 'isa-pension-accounts'], ['반퇴', 'semi-retirement']],
  3: [['생활비 구조적으로 줄이기', 'cut-living-cost'], ['알뜰한 식비 절약법', 'frugal-food-tips'], ['배당으로 월 현금흐름', 'dividend-monthly-income']],
  4: [['지방·주택 다운사이징', 'real-estate-downsizing'], ['동남아 은퇴', 'southeast-asia-retirement'], ['파이어 후 부업', 'post-retirement-side-jobs'], ['디지털노마드 소득', 'digital-nomad-income']],
  5: [['파이어 후 건보료·피부양자', 'health-insurance-dependent'], ['소득 크레바스', 'income-crevasse'], ['국민연금 조기수령', 'national-pension-early'], ['인출 순서 전략', 'withdrawal-order-strategy'], ['해외주식 양도세', 'foreign-stock-tax'], ['퇴직금·IRP 세금', 'severance-irp-tax']],
  6: [['인출 순서 전략', 'withdrawal-order-strategy'], ['배당과 건강보험료', 'dividend-health-insurance'], ['배당 소득세 기준', 'dividend-tax-thresholds']]
};

export default function JourneyStage({ simulation, onMove, onBack }) {
  const [peerAvg, setPeerAvg] = useState(null);
  const [tick, setTick] = useState(0);
  useEffect(() => { let a = true; fetchAggregates().then((x) => { if (a && x && x.avgEarliest) setPeerAvg(x.avgEarliest); }).catch(() => {}); return () => { a = false; }; }, []);
  const j = useMemo(() => {
    let adv = 0; try { adv = Math.max(0, computeProgress(simulation).advanceDays || 0); } catch { /* ignore */ }
    let h = 0; try { h = getAssetHistory().length; } catch { /* ignore */ }
    return journeyStage(simulation, { advanceDays: adv, peerAvg, assetHistoryLen: h });
  }, [simulation, peerAvg]);
  const s = j.signals || {};
  const acc = account();
  const ctx = { calculated: s.calculated, histLen: s.histLen, saveTotal: s.saveTotal, loggedIn: !!(acc && acc.handle), asset: s.asset, notif: s.notif, rateOK: false };
  const missions = useMemo(() => { try { return missionsFor(j.stage, ctx); } catch { return { items: [], doneCount: 0, total: 0 }; } }, [j.stage, tick]); // eslint-disable-line react-hooks/exhaustive-deps
  const milestones = j.milestones || [];
  const doneMs = milestones.filter((m) => m.done).length;
  const reads = READS[j.stage] || [];
  const nextTo = (j.nextStep && j.nextStep.to) || 'home';

  const toggle = (m) => {
    const next = !m.done;
    setManual(m.id, next);
    setTick((n) => n + 1);
    if (next) toast.good('완료로 표시했어요');
  };
  const go = (to) => { try { track('journey_task', { stage: j.stage, to }); } catch { /* ignore */ } onMove(to); };
  const readGuide = (slug) => { try { track('journey_read', { slug }); } catch { /* ignore */ } try { window.open(`/guide/${slug}.html`, '_blank', 'noopener'); } catch { window.location.href = `/guide/${slug}.html`; } };

  return (
    <main className="fm-screen fm-scroll fm-has-tabbar ds-screen-gap">
      <TopBar title="내 파이어 여정" onBack={onBack} />

      <StatHero tone="light" size="title" label={`${j.current.emoji} ${j.current.name}`} value={`${j.stage}단계`} sub={<>{j.current.tag} · {DESC[j.stage]}</>}>
        <ProgressBar className="ds-mt-3" value={doneMs} max={Math.max(1, milestones.length)} left="이정표" right={`${doneMs}/${milestones.length}`} />
        <p className="ds-caption ds-mt-2 sc-jr-ms">{milestones.map((m) => <span key={m.label} className={m.done ? 'is-done' : ''}>{m.done ? '✓' : '·'} {m.label}</span>)}</p>
      </StatHero>

      <ListGroup label="여정 6단계">
        {j.stages.map((st) => {
          const done = st.n < j.stage, cur = st.n === j.stage, next = st.n === j.stage + 1;
          const badge = done ? <Badge tone="good">완료</Badge> : cur ? <Badge tone="accent">지금 여기</Badge> : next ? <Badge tone="neutral">다음</Badge> : null;
          return (
            <ListRow key={st.key} lead={st.emoji} title={`${st.n}. ${st.name}`} desc={st.tag} trail={badge} chevron={false} size="M" className={cur ? 'sc-jr-row--cur' : (done ? 'sc-jr-row--done' : '')} />
          );
        })}
      </ListGroup>

      <Card variant="hero">
        <SectionHead size="sm" kicker="다음 한 걸음" title={NEXT_LABEL[j.stage] || '다음 단계로'} desc="이 하나만 하면 다음 단계에 가까워져요" />
        <Button variant="primary" size="lg" full onClick={() => go(nextTo)}>🔥 지금 하기</Button>
      </Card>

      <Card>
        <SectionHead size="sm" kicker={`${j.stage}단계 할 일`} title={`${missions.doneCount}/${missions.total} 끝났어요`} desc="자동으로 체크되는 것도 있고, 직접 표시하는 것도 있어요" />
        <div className="ds-list">
          {missions.items.map((m) => (
            <ListRow
              key={m.id} size="M" chevron={false}
              className={m.done ? 'sc-jr-task--done' : ''}
              title={m.label} desc={m.hint}
              trail={<>
                {!m.done && m.to && <Button variant="ghost" size="sm" onClick={() => go(m.to)}>하기</Button>}
                {m.kind === 'manual'
                  ? <Chip on={m.done} onClick={() => toggle(m)} aria-label={`${m.label} ${m.done ? '완료 취소' : '완료 표시'}`}>{m.done ? '✓ 완료' : '완료'}</Chip>
                  : <Chip on={m.done}>{m.done ? '✓ 완료' : '진행 중'}</Chip>}
              </>}
            />
          ))}
        </div>
      </Card>

      {reads.length > 0 && (
        <Fold icon="📖" title="이 단계에서 읽어볼 글" hint={`${reads.length}편`}>
          <div className="ds-list">
            {reads.map(([title, slug]) => (
              <ListRow key={slug + title} size="S" title={title} onClick={() => readGuide(slug)} />
            ))}
          </div>
        </Fold>
      )}

      <p className="ds-caption ds-textcenter">단계는 내 기록을 바탕으로 자동으로 정해져요 · 몇 년이 남았든 여기서 함께해요</p>
    </main>
  );
}
