import { useEffect, useState } from 'react';
import { pushSupported, isIOSDevice, isStandalone, notifPermission, currentSubscription, subscribeFireClock, unsubscribeFireClock } from '../../utils/firePush.js';
import { track } from '../../firemap-v2/dailyData.js';

// 헤더 상시 노출 종 아이콘 — 매일 알림 켜짐/꺼짐을 한눈에 보여주고 탭 한 번으로 토글.
// 글 없이 아이콘만으로 상태를 알려, '켜진 건지 모르겠다' 혼란을 해소.
export default function NotifBell() {
  const iosInstall = (() => { try { return isIOSDevice() && !isStandalone(); } catch { return false; } })();
  const supported = (() => { try { return pushSupported(); } catch { return false; } })();
  const [state, setState] = useState(iosInstall ? 'ios' : 'idle'); // idle(off) | on | working | denied | ios
  const [flash, setFlash] = useState('');

  useEffect(() => {
    if (iosInstall || !supported) return undefined;
    let alive = true;
    (async () => {
      try {
        const sub = await currentSubscription();
        if (!alive) return;
        if (sub && notifPermission() === 'granted') setState('on');
        else if (notifPermission() === 'denied') setState('denied');
        else setState('idle');
      } catch { /* ignore */ }
    })();
    return () => { alive = false; };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // 푸시가 불가능한 기기(아이폰 미설치는 안내 목적상 예외)면 아예 숨김
  if (!supported && !iosInstall) return null;

  const showFlash = (t) => { setFlash(t); setTimeout(() => setFlash(''), 2400); };

  const onClick = async () => {
    if (state === 'ios') { showFlash('아이폰은 사파리 공유 → ‘홈 화면에 추가’ 후, 홈 아이콘으로 들어와 켜주세요'); return; }
    if (state === 'working') return;
    if (state === 'on') {
      setState('working');
      try { track('notif_bell_off', {}); } catch { /* ignore */ }
      await unsubscribeFireClock();
      setState('idle'); showFlash('알림을 껐어요');
      return;
    }
    setState('working');
    try { track('notif_bell_on_try', {}); } catch { /* ignore */ }
    const r = await subscribeFireClock();
    if (r && r.ok) { setState('on'); try { track('notif_bell_on', {}); } catch { /* ignore */ } showFlash('켜졌어요! 매일 아침 알림이 가요 🔥'); }
    else if (r && r.reason === 'denied') { setState('denied'); showFlash('알림이 차단돼 있어요. 브라우저 설정에서 허용해 주세요'); }
    else if (r && r.reason === 'ios-install') { setState('ios'); showFlash('아이폰은 홈 화면에 추가한 뒤 켤 수 있어요'); }
    else { setState('idle'); showFlash('잠시 후 다시 시도해 주세요'); }
  };

  const on = state === 'on';
  const title = on ? '매일 알림 켜짐 · 탭하면 끄기' : state === 'denied' ? '알림 차단됨 · 탭하면 안내' : '매일 알림 켜기';

  return (
    <span style={{ position: 'relative', display: 'inline-flex', alignItems: 'center' }}>
      <button
        type="button"
        onClick={onClick}
        aria-label={title}
        title={title}
        style={{ border: 0, background: 'transparent', cursor: 'pointer', fontSize: 17, lineHeight: 1, padding: '2px 4px', opacity: state === 'working' ? 0.5 : 1 }}
      >
        {on ? '🔔' : '🔕'}
      </button>
      {flash && (
        <span style={{ position: 'absolute', top: '120%', right: 0, background: '#18212c', color: '#fff', fontSize: 11.5, fontWeight: 600, lineHeight: 1.45, padding: '7px 10px', borderRadius: 9, zIndex: 60, width: 'max-content', maxWidth: 230, whiteSpace: 'normal', boxShadow: '0 6px 18px rgba(0,0,0,0.2)' }}>{flash}</span>
      )}
    </span>
  );
}
