import { TopBar, Card, ListGroup, ListRow, Icon } from '../../ui/index.js';
import { account } from '../../utils/identity.js';
import { track } from '../../firemap-v2/dailyData.js';
import { CAFE_URL, YOUTUBE_URL, OPENCHAT_URL } from '../../firemap-v2/links.js';

// 전체 — 토스식 목록. 그룹 3(내 여정 / 도구 / 커뮤니티·정보) + 설정.
const SECTIONS = [
  { label: '내 여정', items: [
    { ico: 'chartbar', title: '내 파이어 결과', to: 'result' },
    { ico: 'trophy', title: '랭킹', to: 'ranking' }
  ] },
  { label: '도구', items: [
    { ico: 'sliders', title: '바꿔보기', to: 'experiment' },
    { ico: 'coins', title: '배당으로 파이어', to: 'dividend' },
    { ico: 'stethoscope', title: '파이어 후 건보료', to: 'dependent' },
    { ico: 'receipt', title: '양도·배당세', to: 'foreignTax' },
    { ico: 'bank', title: '국민연금 조기수령', to: 'pension' },
    { ico: 'map', title: '어디서 살까', to: 'cities' },
    { ico: 'compass', title: '파이어 유형 테스트', to: 'firetype' }
  ] },
  { label: '카페 · 소식', items: [
    { ico: 'leaf', title: '파이어맵 네이버 카페', href: CAFE_URL, ext: true },
    ...(OPENCHAT_URL ? [{ ico: 'chat', title: '카카오톡 오픈채팅', href: OPENCHAT_URL, ext: true }] : []),
    { ico: 'newspaper', title: '소식', to: 'news' },
    { ico: 'play', title: '파이어맵 유튜브', href: YOUTUBE_URL, ext: true },
    { ico: 'book', title: '파이어 백과', href: '/guide/' }
  ] }
];

export default function MenuAll({ onMove }) {
  const acc = account();
  const go = (to) => { try { track('menu_all', { to }); } catch { /* ignore */ } onMove(to); };
  return (
    <main className="fm-screen fm-scroll fm-has-tabbar ds-screen-gap">
      <TopBar title="전체" onHome={() => onMove('result')} />
      <Card variant="hero" as="div" padding="md" className="ds-card--flat ds-card--flush">
        <ListRow lead={<Icon name={acc && acc.handle ? 'user' : 'lock'} />} title={acc && acc.handle ? acc.handle : '로그인 · 기록 지키기'} trail={acc && acc.handle ? '설정' : '로그인'} accent size="L" onClick={() => go(acc && acc.handle ? 'settings' : 'account')} />
      </Card>
      {SECTIONS.map((sec) => (
        <ListGroup key={sec.label} label={sec.label}>
          {sec.items.map((it) => (it.href
            ? <ListRow key={it.title} lead={<Icon name={it.ico} />} title={it.title} href={it.href} external={!!it.ext} />
            : <ListRow key={it.title} lead={<Icon name={it.ico} />} title={it.title} onClick={() => go(it.to)} />))}
        </ListGroup>
      ))}
      <ListGroup label="설정 · 정보">
        <ListRow lead={<Icon name="settings" />} title="설정" onClick={() => go('settings')} />
        <ListRow lead={<Icon name="file" />} title="면책 안내" href="/disclaimer" />
        <ListRow lead={<Icon name="lock" />} title="개인정보처리방침" href="/privacy" />
        <ListRow lead={<Icon name="mail" />} title="문의" href="/contact" />
      </ListGroup>
    </main>
  );
}
