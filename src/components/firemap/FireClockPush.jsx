import { useEffect, useState } from 'react';
import { track } from '../../firemap-v2/dailyData.js';
import {
  pushSupported, isIOSDevice, isStandalone, notifPermission,
  currentSubscription, subscribeFireClock, unsubscribeFireClock,
  refreshFireClockMeta, targetFireDateFrom
} from '../../utils/firePush.js';

// '파이어 시계' 매일 알림 구독 카드. 홈(파이어 플랜) 대시보드에 표시.
export default function FireClockPush({ simulation }) {
  const earliest = simulation && simulation.earliestRetirementAge;
  const cur = simulation && simulation.inputs && Number(simulation.inputs.currentAge);
  const targetDate = targetFireDateFrom(simulation);
  const ddays = targetDate ? Math.max(0, Math.round((new Date(targetDate + 'T00:00:00') - new Date()) / 86400000)) : null;

  const [status, setStatus] = useState('idle'); // idle | on | working | denied
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    let alive = true;
    (async () => {
      try {
        const sub = await currentSubscription();
        if (!alive) return;
        if (sub && notifPermission() === 'granted') {
          setStatus('on');
          // 구독중이면 목표일 최신화(재계산 반영)
          if (targetDate) refreshFireClockMeta({ targetFireDate: targetDate, earliestAge: earliest, currentAge: cur });
        } else if (notifPermission() === 'denied') {
          setStatus('denied');
        }
      } catch { /* ignore */ }
      if (alive) setMounted(true);
    })();
    return () => { alive = false; };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [targetDate]);

  // 계산 결과가 없으면(파이어 나이 미정) 카드 숨김
  if (!earliest || !targetDate) return null;

  // iOS인데 홈화면 추가 전이면: 설치 안내(웹푸시는 홈화면 PWA에서만 가능)
  if (isIOSDevice() && !isStandalone()) {
    return (
      <section className="fm-card" style={cardStyle}>
        <p style={kickerStyle}>⏰ 파이어 시계 위젯</p>
        <h2 style={h2Style}>파이어까지 D-{ddays.toLocaleString()}</h2>
        <p style={subStyle}>홈 화면에 추가하면 <b>매일 아침 파이어 시계 알림</b>을 받을 수 있어요. 사파리 공유 버튼 → ‘홈 화면에 추가’ 후 다시 들어와 켜주세요.</p>
      </section>
    );
  }

  if (!pushSupported()) return null;

  const onSubscribe = async () => {
    setStatus('working');
    try { track('fireclock_push_try', {}); } catch { /* ignore */ }
    const r = await subscribeFireClock({ targetFireDate: targetDate, earliestAge: earliest, currentAge: cur });
    if (r.ok) {
      setStatus('on');
      try { track('fireclock_push_on', {}); } catch { /* ignore */ }
      try { window.alert(`켜졌어요! 매일 아침 ‘파이어까지 D-${ddays.toLocaleString()}’ 알림을 보내드릴게요 🔥`); } catch { /* ignore */ }
    } else if (r.reason === 'denied') {
      setStatus('denied');
    } else {
      setStatus('idle');
      const why = (r.reason || '?') + (r.detail ? ` · ${r.detail}` : '');
      try { window.alert(`알림 설정에 실패했어요 (${why}). 잠시 후 다시 시도해 주세요.`); } catch { /* ignore */ }
    }
  };

  const onUnsubscribe = async () => {
    setStatus('working');
    await unsubscribeFireClock();
    setStatus('idle');
    try { track('fireclock_push_off', {}); } catch { /* ignore */ }
  };

  return (
    <section className="fm-card" style={cardStyle}>
      <p style={kickerStyle}>⏰ 파이어 시계 위젯</p>
      <h2 style={h2Style}>파이어까지 D-{ddays.toLocaleString()}</h2>
      {status === 'on' ? (
        <>
          <p style={subStyle}>매일 아침 경제뉴스 + 파이어 D-day 알림을 받고 있어요 🔥 하루 1회 발송.</p>
          <button type="button" onClick={onUnsubscribe} style={btnGhost} disabled={status === 'working'}>알림 끄기</button>
        </>
      ) : status === 'denied' ? (
        <p style={subStyle}>알림이 차단돼 있어요. 휴대폰 설정 → 파이어맵 → 알림을 허용한 뒤 다시 시도해 주세요.</p>
      ) : (
        <>
          <p style={subStyle}>매일 아침 <b>오늘 경제뉴스 + 파이어까지 D-day</b>를 한 번에 알림으로 보내드려요. 하루 1회, 매일 한 걸음씩.</p>
          <button type="button" onClick={onSubscribe} style={btnPrimary} disabled={status === 'working'}>
            {status === 'working' ? '설정 중…' : '🔔 매일 파이어 시계 받기'}
          </button>
        </>
      )}
    </section>
  );
}

const cardStyle = { borderColor: 'rgba(255,90,0,0.3)' };
const kickerStyle = { fontSize: '12px', fontWeight: 700, color: '#ff5a00', margin: '0 0 4px', letterSpacing: '0.02em' };
const h2Style = { margin: '0 0 6px', fontSize: '22px', color: '#1e2859' };
const subStyle = { fontSize: '13px', color: 'var(--fm-muted, #6b6f76)', lineHeight: 1.6, margin: '0 0 12px' };
const btnPrimary = { display: 'block', width: '100%', padding: '13px 16px', borderRadius: '12px', border: 'none', background: '#ff5a00', color: '#fff', fontSize: '14px', fontWeight: 700, cursor: 'pointer' };
const btnGhost = { display: 'inline-block', padding: '8px 14px', borderRadius: '10px', border: '1px solid #d7dae0', background: '#fff', color: '#6b6f76', fontSize: '13px', fontWeight: 600, cursor: 'pointer' };
