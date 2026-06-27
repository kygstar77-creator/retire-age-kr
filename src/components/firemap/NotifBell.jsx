import { useEffect, useState } from 'react';
import { pushSupported, isIOSDevice, isStandalone, notifPermission, currentSubscription, subscribeFireClock, unsubscribeFireClock } from '../../utils/firePush.js';
import { track } from '../../firemap-v2/dailyData.js';

// 헤더 상시 노출 알림 칩 — 🔔 알림(켜짐) / 🔕 알림(꺼짐) 한눈에, 탭하면 토글.
// '켜진 건지 모르겠다' 혼란 해소. 헤더 .fm-actions button 공통 칩 스타일을 그대로 사용.
export default function NotifBell() {
  const iosInstall = (() => { try { return isIOSDevice() && !isStandalone(); } catch { return false; } })();
  const supported = (() => { try { return pushSupported(); } catch { return false; } })();
  const [state, setState] = useState(iosInstall ? 'ios' : 'idle'); // idle(off) | on | working | denied | ios

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

  // 푸시 불가 기기(아이폰 미설치는 안내 목적상 예외)면 숨김
  if (!supported && !iosInstall) return null;

  const notify = (t) => { try { window.alert(t); } catch { /* ignore */ } };

  const onClick = async () => {
    if (state === 'ios') { notify('아이폰은 사파리 공유 버튼 → ‘홈 화면에 추가’ 후, 홈 아이콘으로 들어와 다시 눌러 켜주세요.'); return; }
    if (state === 'working') return;
    if (state === 'on') {
      setState('working');
      try { track('notif_bell_off', {}); } catch { /* ignore */ }
      await unsubscribeFireClock();
      setState('idle');
      return;
    }
    setState('working');
    try { track('notif_bell_on_try', {}); } catch { /* ignore */ }
    const r = await subscribeFireClock();
    if (r && r.ok) { setState('on'); try { track('notif_bell_on', {}); } catch { /* ignore */ } notify('켜졌어요! 매일 아침 알림이 가요 🔥'); }
    else if (r && r.reason === 'denied') { setState('denied'); notify('알림이 차단돼 있어요. 휴대폰/브라우저 설정에서 알림을 허용한 뒤 다시 시도해 주세요.'); }
    else if (r && r.reason === 'ios-install') { setState('ios'); notify('아이폰은 홈 화면에 추가한 뒤 켤 수 있어요.'); }
    else { setState('idle'); notify('잠시 후 다시 시도해 주세요.'); }
  };

  const on = state === 'on';
  const title = on ? '매일 알림 켜짐 · 탭하면 끄기' : state === 'denied' ? '알림 차단됨' : '매일 알림 켜기';

  return (
    <button
      type="button"
      onClick={onClick}
      aria-label={title}
      title={title}
      style={{ cursor: 'pointer', justifyContent: 'center', opacity: state === 'working' ? 0.6 : 1 }}
    >
      {(on ? '🔔' : '🔕') + ' 알림'}
    </button>
  );
}
