// 설정 — 알림 진입점 1곳(항상 메타 포함) · 위젯(금액 숨김) · 앱(홈 화면 추가·다크) · 정보.
import { useEffect, useState } from 'react';
import { TopBar, ListGroup, ListRow, Sheet, Button, toast, Icon } from '../../ui/index.js';
import { prefs } from '../../utils/prefs.js';
import { account } from '../../utils/identity.js';
import { pushSupported, isIOSDevice, isStandalone, notifPermission, currentSubscription, subscribeFireClock, unsubscribeFireClock, targetFireDateFrom, inAppBrowser, openExternalUrl } from '../../utils/firePush.js';
import { track } from '../../firemap-v2/dailyData.js';
import { logEvent } from '../../utils/live.js';
import { CAFE_URL, OPENCHAT_URL } from '../../firemap-v2/links.js';

function Switch({ on, onChange, disabled }) {
  return <button type="button" className="ds-switch" role="switch" aria-checked={on ? 'true' : 'false'} disabled={disabled} onClick={() => onChange(!on)} />;
}

export default function Settings({ simulation, onMove, onBack }) {
  const acc = account();
  const [notif, setNotif] = useState('idle'); // idle|on|working|denied|ios|inapp|unsupported
  const [hide, setHide] = useState(() => prefs.hideAmount());
  const [dark, setDark] = useState(() => prefs.theme() === 'dark');
  const [installOpen, setInstallOpen] = useState(false);
  const iosInstall = (() => { try { return isIOSDevice() && !isStandalone(); } catch { return false; } })();
  const inApp = (() => { try { return inAppBrowser(); } catch { return ''; } })();

  useEffect(() => {
    let alive = true;
    (async () => {
      try {
        if (inApp) { setNotif('inapp'); return; }
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

  // 알림 켜기. 지금까지는 성공만 기록하고 실패는 이유와 상관없이 잠시 후 다시 해봐요만 띄웠다.
  // 그래서 2026-09-03~07 실제 시도 6번이 전부 실패했는데 왜인지 아무도 몰랐다.
  // 실패 이유를 전부 남기고, 이유마다 사용자가 실제로 할 수 있는 걸 알려준다.
  // 기록은 logEvent로 바로 보낸다 — track은 GA가 안 뜨면(광고 차단·인앱 브라우저) 아무것도 안 남긴다.
  const log = (name, props) => { try { logEvent(name, props || {}); } catch { /* ignore */ } };
  const toggleNotif = async (want) => {
    if (notif === 'inapp') {
      log('notif_blocked', { reason: 'inapp', app: inApp });
      const url = `${window.location.origin}/?from=inapp#settings`;
      if (!openExternalUrl(url)) toast('앱 안에서 열린 화면이라 알림을 켤 수 없어요 · 오른쪽 위 메뉴에서 다른 브라우저로 열기를 눌러주세요');
      return;
    }
    if (notif === 'ios') { log('notif_blocked', { reason: 'ios-install' }); setInstallOpen(true); return; }
    if (notif === 'unsupported') { log('notif_blocked', { reason: 'unsupported' }); toast('이 브라우저는 알림을 지원하지 않아요 · 크롬이나 사파리에서 열어주세요'); return; }
    setNotif('working');
    if (!want) { await unsubscribeFireClock(); setNotif('idle'); track('notif_off', {}); log('notif_off', {}); return; }
    log('notif_try', { perm: notifPermission() });
    const inp = (simulation && simulation.inputs) || {};
    const r = await subscribeFireClock({ targetFireDate: targetFireDateFrom(simulation), earliestAge: simulation && simulation.earliestRetirementAge, currentAge: inp.currentAge });
    if (r && r.ok) { setNotif('on'); track('notif_on', {}); log('notif_ok', {}); toast.good('켜졌어요. 매일 아침 파이어 시계가 가요'); return; }
    const reason = (r && r.reason) || 'unknown';
    log('notif_fail', { reason, detail: String((r && r.detail) || '').slice(0, 120) });
    if (reason === 'denied') { setNotif('denied'); toast.bad('알림이 차단돼 있어요 · 브라우저 주소창 왼쪽 자물쇠에서 알림을 허용으로 바꿔주세요'); return; }
    if (reason === 'inapp') { setNotif('inapp'); toast.bad('앱 안에서 열린 화면이라 알림을 켤 수 없어요 · 크롬이나 사파리에서 열어주세요'); return; }
    if (reason === 'ios-install') { setNotif('ios'); setInstallOpen(true); return; }
    if (reason === 'sw') { setNotif('idle'); toast.bad('알림 준비가 덜 됐어요 · 페이지를 새로고침한 뒤 다시 눌러주세요'); return; }
    if (reason === 'subscribe') { setNotif('idle'); toast.bad('브라우저가 알림 등록을 막았어요 · 시크릿 모드가 아닌 일반 창에서 다시 해주세요'); return; }
    setNotif('idle'); toast.bad('서버에 저장하지 못했어요 · 잠시 후 다시 눌러주세요');
  };

  return (
    <main className="fm-screen fm-scroll fm-has-tabbar ds-screen-gap">
      <TopBar title="설정" onBack={onBack} />

      <ListGroup label="계정">
        <ListRow lead={<Icon name={acc && acc.handle ? 'user' : 'lock'} />} title={acc && acc.handle ? acc.handle : '로그인 · 기록 지키기'} onClick={() => onMove('account')} />
      </ListGroup>

      <ListGroup label="알림">
        <ListRow lead={<Icon name="bell" />} title="아침 파이어 시계" desc={notif === 'on' ? '매일 아침 D-day 알림이 가요' : notif === 'denied' ? '브라우저에서 차단됨' : notif === 'inapp' ? '앱 안 브라우저에선 켤 수 없어요 · 눌러서 크롬이나 사파리로 열기' : notif === 'ios' ? '아이폰은 홈 화면에 추가한 뒤 켤 수 있어요' : '매일 아침 파이어까지 남은 날을 받아요'} chevron={false} trail={<Switch on={notif === 'on'} disabled={notif === 'working'} onChange={toggleNotif} />} />
      </ListGroup>

      <ListGroup label="홈 · 위젯">
        <ListRow lead={<Icon name="eyeoff" />} title="금액 숨기기" chevron={false} trail={<Switch on={hide} onChange={(v) => { prefs.setHideAmount(v); setHide(v); }} />} />
        <ListRow lead={<Icon name="moon" />} title="다크 모드" chevron={false} trail={<Switch on={dark} onChange={(v) => { prefs.setTheme(v ? 'dark' : 'light'); setDark(v); }} />} />
        <ListRow lead={<Icon name="phone" />} title="홈 화면에 추가" onClick={() => setInstallOpen(true)} />
      </ListGroup>

      <ListGroup label="카페 · 정보">
        <ListRow lead={<Icon name="leaf" />} title="파이어맵 네이버 카페" href={CAFE_URL} external />
        {OPENCHAT_URL && <ListRow lead={<Icon name="chat" />} title="카카오톡 오픈채팅" href={OPENCHAT_URL} external />}
        <ListRow lead={<Icon name="file" />} title="면책 안내" href="/disclaimer" />
        <ListRow lead={<Icon name="lock" />} title="개인정보처리방침" href="/privacy" />
        <ListRow lead={<Icon name="mail" />} title="문의" href="/contact" />
      </ListGroup>

      <Sheet open={installOpen} title="홈 화면에 추가" onClose={() => setInstallOpen(false)}>
        {iosInstall
          ? <p className="ds-p">사파리 하단 <b>공유 버튼(□↑)</b> → <b>홈 화면에 추가</b>를 눌러요. 추가한 아이콘으로 열면 알림도 켤 수 있어요.</p>
          : <p className="ds-p">브라우저 메뉴(⋮)에서 <b>앱 설치</b> 또는 <b>홈 화면에 추가</b>를 눌러요.</p>}
        <Button variant="primary" size="md" full className="ds-mt-3" onClick={() => setInstallOpen(false)}>확인</Button>
      </Sheet>
    </main>
  );
}
