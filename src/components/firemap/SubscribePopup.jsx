import { useEffect, useState } from 'react';
import { track } from '../../firemap-v2/dailyData.js';
import { account } from '../../utils/identity.js';
import { claimPopup } from '../../utils/popupCoordinator.js';
import {
  pushSupported, isIOSDevice, isStandalone, notifPermission,
  currentSubscription, subscribeFireClock, targetFireDateFrom
} from '../../utils/firePush.js';

// 리텐션 구독 팝업 — 로그인+'매일 데일리 알림' 유도. 기존 firePush/fm_push_subs 재활용.
// 유형테스트 팝업과 동시에 안 뜨게 popupCoordinator로 한 뷰에 하나만. '오늘 보지 않기'·버스트 가드 포함.
const SEEN = 'fm_sub_popup_seen';        // 최근 노출(버스트 가드)
const HIDE_DAY = 'fm_sub_hide_day';      // '오늘 보지 않기'(자정 리셋)
const SUBSCRIBED = 'fm_subscribed';      // 구독 완료 → 더 권유 안 함
const BURST_MS = 45 * 1000;
const todayStr = () => { const d = new Date(); return `${d.getFullYear()}-${d.getMonth() + 1}-${d.getDate()}`; };
const readTs = (k) => { try { return Number(localStorage.getItem(k) || 0) || 0; } catch { return 0; } };

// 기기에서 구독 권유가 의미 있는지: 푸시 가능(데스크탑/안드/standalone iOS) 또는 iOS 미설치(설치 안내 목적)
function eligibleDevice() {
  try { return pushSupported() || (isIOSDevice() && !isStandalone()); } catch { return false; }
}
function suppressed() {
  try {
    if (localStorage.getItem(SUBSCRIBED) === '1') return true;
    // 권한 granted여도 실제 구독은 아래 currentSubscription(비동기)로 확인 — granted만으로 막지 않음(허용했지만 미구독자도 유도).
    if (localStorage.getItem(HIDE_DAY) === todayStr()) return true;
    const se = readTs(SEEN); if (se && Date.now() - se < BURST_MS) return true;
    if (!eligibleDevice()) return true;
    return false;
  } catch { return false; }
}

export default function SubscribePopup({ onMove, simulation }) {
  const [open, setOpen] = useState(false);
  const [working, setWorking] = useState(false);
  const [msg, setMsg] = useState('');
  const iosInstall = isIOSDevice() && !isStandalone();
  const loggedIn = !!(account() && account().handle);

  useEffect(() => {
    if (suppressed()) return undefined;
    let alive = true;
    const t = setTimeout(async () => {
      if (!alive) return;
      // 이미 구독돼 있으면 표시 안 함
      try { const sub = await currentSubscription(); if (sub) { try { localStorage.setItem(SUBSCRIBED, '1'); } catch { /* ignore */ } return; } } catch { /* ignore */ }
      if (!alive) return;
      if (!claimPopup('subscribe')) return; // 다른 팝업(유형테스트)이 이미 이 뷰를 차지 → 양보
      setOpen(true);
      try { localStorage.setItem(SEEN, String(Date.now())); } catch { /* ignore */ }
      try { track('subscribe_popup_view', {}); } catch { /* ignore */ }
    }, 1800); // 유형테스트(1.4s)보다 늦게 → 둘 다 가능하면 유형테스트 우선, 이후 방문에 구독
    return () => { alive = false; clearTimeout(t); };
  }, []);

  if (!open) return null;
  const close = () => { try { track('subscribe_popup_close', {}); } catch { /* ignore */ } setOpen(false); };
  const hideToday = () => { try { localStorage.setItem(HIDE_DAY, todayStr()); } catch { /* ignore */ } try { track('subscribe_popup_hide_today', {}); } catch { /* ignore */ } setOpen(false); };
  const go = async () => {
    if (iosInstall) { try { track('subscribe_popup_ios', {}); } catch { /* ignore */ } setMsg('아이폰은 3단계예요 — ① 사파리 공유 버튼 → ‘홈 화면에 추가’ ② 홈 아이콘으로 다시 열기 ③ 상단 ‘🔔 알림’ 버튼 탭!'); return; }
    if (!loggedIn) { try { track('subscribe_popup_login', {}); } catch { /* ignore */ } setOpen(false); if (onMove) onMove('account'); return; }
    setWorking(true);
    try { track('subscribe_popup_try', {}); } catch { /* ignore */ }
    const targetDate = targetFireDateFrom(simulation);
    const earliest = simulation && simulation.earliestRetirementAge;
    const cur = simulation && simulation.inputs && Number(simulation.inputs.currentAge);
    const r = await subscribeFireClock({ targetFireDate: targetDate || null, earliestAge: earliest ?? null, currentAge: cur ?? null });
    setWorking(false);
    if (r.ok) {
      try { localStorage.setItem(SUBSCRIBED, '1'); } catch { /* ignore */ }
      try { track('subscribe_popup_subscribed', {}); } catch { /* ignore */ }
      setMsg('켜졌어요! 매일 아침 경제뉴스 + 파이어 D-day를 보내드릴게요 🔥');
      setTimeout(() => setOpen(false), 1800);
    } else if (r.reason === 'denied') {
      setMsg('알림이 차단돼 있어요. 휴대폰 설정 → 파이어맵 → 알림 허용 후 다시 시도해 주세요.');
    } else if (r.reason === 'ios-install') {
      setMsg('아이폰은 홈 화면에 추가한 뒤에 알림을 켤 수 있어요.');
    } else {
      setMsg('설정에 실패했어요. 잠시 후 다시 시도해 주세요.');
    }
  };

  const ctaText = working ? '설정 중…' : (iosInstall ? '🔔 알림 켜는 법 보기' : (loggedIn ? '🔔 매일 알림 켜기' : '🔔 로그인하고 알림 받기'));

  return (
    <div role="dialog" aria-modal="true" onClick={close} style={{
      position: 'fixed', inset: 0, zIndex: 9000, display: 'flex', alignItems: 'center', justifyContent: 'center',
      padding: 22, background: 'rgba(7,9,22,0.72)', backdropFilter: 'blur(3px)', animation: 'fmSubFade .25s ease'
    }}>
      <style>{`
        @keyframes fmSubFade{from{opacity:0}to{opacity:1}}
        @keyframes fmSubUp{from{opacity:0;transform:translateY(16px) scale(.96)}to{opacity:1;transform:none}}
        @keyframes fmSubGlow{0%,100%{opacity:.5}50%{opacity:.9}}
        @keyframes fmSubRing{0%,100%{transform:rotate(-8deg)}50%{transform:rotate(8deg)}}
      `}</style>
      <div onClick={(e) => e.stopPropagation()} style={{
        position: 'relative', width: '100%', maxWidth: 340, borderRadius: 24, overflow: 'hidden', textAlign: 'center',
        background: 'radial-gradient(130% 90% at 50% 0%, #102a4d, #0b1226 72%)', border: '1px solid #ffffff1f',
        padding: '30px 22px 24px', color: '#fff', animation: 'fmSubUp .4s cubic-bezier(.2,1.1,.3,1)'
      }}>
        <div aria-hidden="true" style={{ position: 'absolute', top: -60, left: '50%', transform: 'translateX(-50%)', width: 200, height: 120, background: 'radial-gradient(circle, #3aa0ff88, transparent 60%)', filter: 'blur(14px)', animation: 'fmSubGlow 2.4s ease-in-out infinite' }} />
        <button type="button" aria-label="닫기" onClick={close} style={{ position: 'absolute', top: 12, right: 14, border: 0, background: 'transparent', color: '#9aa1c4', fontSize: 22, lineHeight: 1, cursor: 'pointer' }}>×</button>
        <div style={{ position: 'relative', fontSize: 50, animation: 'fmSubRing 2.6s ease-in-out infinite' }}>🔔</div>
        <p style={{ position: 'relative', margin: '6px 0 4px', fontSize: 12.5, fontWeight: 800, letterSpacing: '.04em', color: '#bfe0ff' }}>매일 1분, 파이어 습관</p>
        <h2 style={{ position: 'relative', margin: '0 0 8px', fontSize: 22, fontWeight: 900, lineHeight: 1.3 }}>매일 <span style={{ background: 'linear-gradient(90deg,#5db4ff,#9ad0ff)', WebkitBackgroundClip: 'text', backgroundClip: 'text', color: 'transparent' }}>알림</span> 받고 흐름 놓치지 않기</h2>
        <p style={{ position: 'relative', margin: '0 0 18px', fontSize: 13.5, lineHeight: 1.6, color: '#c7d3e6' }}>{msg || <>매일 아침 <b style={{ color: '#fff' }}>오늘 경제뉴스 + 파이어 D-day</b>를 한 번에 받아보세요. 하루 1회 · 언제든 해지.</>}</p>
        <button type="button" onClick={go} disabled={working} style={{ position: 'relative', width: '100%', padding: '14px', borderRadius: 14, border: 0, fontSize: 15.5, fontWeight: 800, color: '#06203d', background: 'linear-gradient(90deg,#5db4ff,#9ad0ff)', cursor: 'pointer', boxShadow: '0 8px 26px #3aa0ff55' }}>{ctaText}</button>
        <button type="button" onClick={hideToday} style={{ position: 'relative', marginTop: 10, background: 'transparent', border: 0, color: '#8b96ad', fontSize: 12.5, fontWeight: 700, cursor: 'pointer' }}>오늘 보지 않기</button>
      </div>
    </div>
  );
}
