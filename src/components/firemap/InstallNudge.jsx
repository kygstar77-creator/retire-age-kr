import { useEffect, useState } from 'react';
import { installAvailable, onInstallChange, promptInstall } from '../../utils/installPrompt.js';
import { isIOSDevice, isStandalone } from '../../utils/firePush.js';
import { track } from '../../firemap-v2/dailyData.js';

// 설치 유도(2단계) — 결과/저축 '효용을 느낀 순간'에 뜨는 1회성 컨텍스트 배너.
// 재활용: installPrompt.js(안드 beforeinstallprompt) + firePush.js(iOS/standalone 판정) + 기존 install 이벤트.
// 닫으면 일정 기간 재노출 자제(localStorage). 이미 앱으로 실행(standalone) 중이면 안 뜸. 신규 인프라 없음.
const DISMISS_KEY = 'fm_install_nudge_v1';
const SUPPRESS_DAYS = 30;

function suppressed() {
  try {
    const v = localStorage.getItem(DISMISS_KEY);
    if (!v) return false;
    const t = Number(v);
    if (!t) return true; // 값은 있는데 숫자 아님 → 영구 숨김 취급
    return (Date.now() - t) < SUPPRESS_DAYS * 86400000;
  } catch { return false; }
}

export default function InstallNudge({ moment = 'result' }) {
  const [avail, setAvail] = useState(installAvailable());
  const [gone, setGone] = useState(suppressed());
  useEffect(() => onInstallChange(() => setAvail(installAvailable())), []);

  const ios = isIOSDevice() && !isStandalone();
  // 줄 게 있을 때만: 안드 설치 프롬프트 가능 OR iOS(홈화면 추가 안내). 이미 설치/닫음이면 숨김.
  const show = !isStandalone() && !gone && (avail || ios);

  useEffect(() => {
    if (show) { try { track('install_nudge_view', { moment, platform: ios ? 'ios' : 'android' }); } catch { /* ignore */ } }
  }, [show]);

  if (!show) return null;

  const dismiss = () => {
    try { localStorage.setItem(DISMISS_KEY, String(Date.now())); } catch { /* ignore */ }
    setGone(true);
    try { track('install_nudge_dismiss', { moment }); } catch { /* ignore */ }
  };
  const install = async () => {
    try { track('install_click', { moment }); } catch { /* ignore */ }
    const outcome = await promptInstall();
    try { track('install_result', { outcome: outcome || 'none', moment }); } catch { /* ignore */ }
    if (outcome === 'accepted') { try { localStorage.setItem(DISMISS_KEY, String(Date.now())); } catch { /* ignore */ } setGone(true); }
  };

  const head = moment === 'save' ? '내 저축 기록, 홈에서 바로 이어가기' : '방금 본 내 파이어, 홈에 추가해두기';
  const sub = moment === 'save'
    ? '홈 화면에 추가하면 내일도 까먹지 않고 한 번 탭으로 기록할 수 있어요.'
    : '홈 화면에 추가하면 한 번 탭으로 들어와 매일 1분 점검할 수 있어요.';

  return (
    <section className="fm-card" style={{ position: 'relative', background: '#fff7ef', border: '1px solid #ffd9c2', borderRadius: 16, padding: '14px 16px' }} aria-live="polite">
      <button type="button" onClick={dismiss} aria-label="닫기" style={{ position: 'absolute', top: 8, right: 10, border: 'none', background: 'transparent', color: '#b6927d', fontSize: 18, lineHeight: 1, cursor: 'pointer' }}>✕</button>
      <p style={{ margin: '0 24px 4px 0', fontSize: 15, fontWeight: 800, color: '#15151b' }}>📲 {head}</p>
      <p style={{ margin: '0 0 10px', fontSize: 12.5, color: '#9a3412', lineHeight: 1.5 }}>{sub}</p>
      {ios ? (
        <p style={{ margin: 0, fontSize: 12.5, color: '#c2410c', fontWeight: 700, lineHeight: 1.5 }}>아이폰: 사파리 <b>공유 버튼</b> → <b>‘홈 화면에 추가’</b>를 누르면 끝이에요.</p>
      ) : (
        <button type="button" onClick={install} style={{ display: 'block', width: '100%', padding: '12px 16px', borderRadius: 12, border: 'none', background: '#ff5a00', color: '#fff', fontSize: 14, fontWeight: 800, cursor: 'pointer' }}>홈 화면에 추가하기</button>
      )}
    </section>
  );
}
