// 설정 — 알림 진입점 1곳(항상 메타 포함) · 위젯(금액 숨김) · 앱(홈 화면 추가·다크) · 정보.
import { useEffect, useState } from 'react';
import { TopBar, ListGroup, ListRow, Sheet, Button, toast } from '../../ui/index.js';
import { prefs } from '../../utils/prefs.js';
import { account } from '../../utils/identity.js';
import { pushSupported, isIOSDevice, isStandalone, notifPermission, currentSubscription, subscribeFireClock, unsubscribeFireClock, targetFireDateFrom } from '../../utils/firePush.js';
import { track } from '../../firemap-v2/dailyData.js';
import { CAFE_URL } from '../../firemap-v2/links.js';

function Switch({ on, onChange, disabled }) {
  return <button type="button" className="ds-switch" role="switch" aria-checked={on ? 'true' : 'false'} disabled={disabled} onClick={() => onChange(!on)} />;
}

export default function Settings({ simulation, onMove, onBack }) {
  const acc = account();
  const [notif, setNotif] = useState('idle'); // idle|on|working|denied|ios|unsupported
  const [hide, setHide] = useState(() => prefs.hideAmount());
  const [dark, setDark] = useState(() => prefs.theme() === 'dark');
  const [installOpen, setInstallOpen] = useState(false);
  const iosInstall = (() => { try { return isIOSDevice() && !isStandalone(); } catch { return false; } })();

  useEffect(() => {
    let alive = true;
    (async () => {
      try {
        if (iosInstall) { setNotif('ios'); return; }
        if (!pushSupported()) { setNotif('unsupported'); return; }
        const sub = await currentSubscription();
        if (!alive) return;
        if (sub && notifPermission() === 'granted') setNotif('on');
        else if (notifPermission() === 'denied') setNotif('denied');
      } catch { /* ignore */ }
    })();
    return () => { alive = false; };
  }, [iosInstall]);

  const toggleNotif = async (want) => {
    if (notif === 'ios') { setInstallOpen(true); return; }
    if (notif === 'unsupported') { toast('이 브라우저는 알림을 지원하지 않아요.'); return; }
    setNotif('working');
    if (!want) { await unsubscribeFireClock(); setNotif('idle'); track('notif_off', {}); return; }
    const inp = (simulation && simulation.inputs) || {};
    const r = await subscribeFireClock({ targetFireDate: targetFireDateFrom(simulation), earliestAge: simulation && simulation.earliestRetirementAge, currentAge: inp.currentAge });
    if (r && r.ok) { setNotif('on'); track('notif_on', {}); toast.good('켜졌어요. 매일 아침 파이어 시계가 가요 🔥'); }
    else if (r && r.reason === 'denied') { setNotif('denied'); toast.bad('알림이 차단돼 있어요. 브라우저 설정에서 허용한 뒤 다시 켜주세요.'); }
    else { setNotif('idle'); toast.bad('잠시 후 다시 시도해 주세요.'); }
  };

  return (
    <main className="fm-screen fm-scroll fm-has-tabbar ds-screen-gap">
      <TopBar title="설정" onBack={onBack} />

      <ListGroup label="계정">
        <ListRow lead={acc && acc.handle ? '👤' : '🔒'} title={acc && acc.handle ? acc.handle : '로그인 · 기록 지키기'} desc={acc && acc.handle ? '닉네임 변경 · 로그아웃 · 탈퇴' : '기기를 바꿔도 저축·랭킹 기록이 이어져요'} onClick={() => onMove('account')} />
      </ListGroup>

      <ListGroup label="알림">
        <ListRow lead="🔔" title="아침 파이어 시계" desc={notif === 'on' ? '매일 아침 D-day 알림이 가요' : notif === 'denied' ? '브라우저에서 차단됨' : notif === 'ios' ? '아이폰은 홈 화면에 추가한 뒤 켤 수 있어요' : '매일 아침 파이어까지 남은 날을 받아요'} chevron={false} trail={<Switch on={notif === 'on'} disabled={notif === 'working'} onChange={toggleNotif} />} />
      </ListGroup>

      <ListGroup label="홈 · 위젯">
        <ListRow lead="🙈" title="금액 숨기기" desc="홈·통에서 금액 대신 •••로 표시 (D-day·%만)" chevron={false} trail={<Switch on={hide} onChange={(v) => { prefs.setHideAmount(v); setHide(v); }} />} />
        <ListRow lead="🌙" title="다크 모드" desc="눈이 편한 어두운 화면" chevron={false} trail={<Switch on={dark} onChange={(v) => { prefs.setTheme(v ? 'dark' : 'light'); setDark(v); }} />} />
        <ListRow lead="📲" title="홈 화면에 추가" desc="앱처럼 아이콘으로 바로 열기" onClick={() => setInstallOpen(true)} />
      </ListGroup>

      <ListGroup label="커뮤니티 · 정보">
        <ListRow lead="🟢" title="파이어맵 네이버 카페" desc="인증 · 봐주세요 · 파이어 후 하루" href={CAFE_URL} external />
        <ListRow lead="📄" title="면책 안내" href="/disclaimer.html" />
        <ListRow lead="🔒" title="개인정보처리방침" href="/privacy.html" />
        <ListRow lead="✉️" title="문의" href="/contact.html" />
      </ListGroup>

      <Sheet open={installOpen} title="홈 화면에 추가" onClose={() => setInstallOpen(false)}>
        {iosInstall
          ? <p className="ds-p">사파리 하단 <b>공유 버튼(□↑)</b> → <b>홈 화면에 추가</b>를 누르세요. 추가한 아이콘으로 열면 알림도 켤 수 있어요.</p>
          : <p className="ds-p">브라우저 메뉴(⋮)에서 <b>앱 설치</b> 또는 <b>홈 화면에 추가</b>를 누르세요.</p>}
        <Button variant="primary" size="md" full className="ds-mt-3" onClick={() => setInstallOpen(false)}>확인</Button>
      </Sheet>
    </main>
  );
}
