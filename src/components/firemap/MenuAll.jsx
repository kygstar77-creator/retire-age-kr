import { TopBar, Card, ListGroup, ListRow } from '../../ui/index.js';
import { account } from '../../utils/identity.js';
import { track } from '../../firemap-v2/dailyData.js';
import { CAFE_URL, YOUTUBE_URL, OPENCHAT_URL } from '../../firemap-v2/links.js';

// 전체 — 토스식 목록. 그룹 3(내 여정 / 도구 / 커뮤니티·정보) + 설정.
const SECTIONS = [
  { label: '내 여정', items: [
    { ico: '📊', title: '내 파이어 결과', desc: '파이어 나이 · 필요 자산 · 레버 3', to: 'result' },
    { ico: '🏆', title: '랭킹', desc: '같은 구간 · 또래', to: 'ranking' }
  ] },
  { label: '도구', items: [
    { ico: '🎛️', title: '바꿔보기', desc: '저축·생활비·수익률 미리보기', to: 'experiment' },
    { ico: '💵', title: '배당으로 파이어', desc: '월 배당 목표 · 달성 나이 · 세후', to: 'dividend' },
    { ico: '🩺', title: '파이어 후 건보료', desc: '피부양자 · 지역가입 보험료', to: 'dependent' },
    { ico: '🧾', title: '양도·배당세', desc: '해외주식 양도세 · 배당 소득세', to: 'foreignTax' },
    { ico: '🏦', title: '국민연금 조기수령', desc: '1년 일찍 받을 때마다 6% 감액', to: 'pension' },
    { ico: '🗺️', title: '어디서 살까', desc: '국내·해외 도시 생활비 비교', to: 'cities' },
    { ico: '🧭', title: '파이어 유형 테스트', desc: '12문항 · 살 도시 Top3', to: 'firetype' }
  ] },
  { label: '카페 · 소식', items: [
    { ico: '🟢', title: '파이어맵 네이버 카페', href: CAFE_URL, ext: true },
    ...(OPENCHAT_URL ? [{ ico: '💬', title: '카카오톡 오픈채팅', href: OPENCHAT_URL, ext: true }] : []),
    { ico: '📰', title: '소식', desc: '지표 · 파이어 후 하루 · 배당락', to: 'news' },
    { ico: '▶️', title: '파이어맵 유튜브', desc: '영상으로 보는 파이어', href: YOUTUBE_URL, ext: true },
    { ico: '📚', title: '파이어 백과', desc: '건보료·세금·연금 가이드', href: '/guide/' }
  ] }
];

export default function MenuAll({ onMove }) {
  const acc = account();
  const go = (to) => { try { track('menu_all', { to }); } catch { /* ignore */ } onMove(to); };
  return (
    <main className="fm-screen fm-scroll fm-has-tabbar ds-screen-gap">
      <TopBar title="전체" onHome={() => onMove('result')} />
      <Card variant="hero" as="div" padding="md" className="ds-card--flat ds-card--flush">
        <ListRow lead={acc && acc.handle ? '👤' : '🔒'} title={acc && acc.handle ? acc.handle : '로그인 · 기록 지키기'} desc={acc && acc.handle ? '설정 · 알림 · 위젯' : '기기를 바꿔도 저축·랭킹이 이어져요'} trail={acc && acc.handle ? '설정' : '로그인'} accent size="L" onClick={() => go(acc && acc.handle ? 'settings' : 'account')} />
      </Card>
      {SECTIONS.map((sec) => (
        <ListGroup key={sec.label} label={sec.label}>
          {sec.items.map((it) => (it.href
            ? <ListRow key={it.title} lead={it.ico} title={it.title} desc={it.desc} href={it.href} external={!!it.ext} />
            : <ListRow key={it.title} lead={it.ico} title={it.title} desc={it.desc} onClick={() => go(it.to)} />))}
        </ListGroup>
      ))}
      <ListGroup label="설정 · 정보">
        <ListRow lead="⚙️" title="설정" desc="알림 · 금액 숨김 · 다크 모드 · 홈 화면 추가" onClick={() => go('settings')} />
        <ListRow lead="📄" title="면책 안내" href="/disclaimer.html" />
        <ListRow lead="🔒" title="개인정보처리방침" href="/privacy.html" />
        <ListRow lead="✉️" title="문의" href="/contact.html" />
      </ListGroup>
      <p className="ds-caption ds-textcenter">파이어맵은 정보 제공 서비스예요 · 투자 권유가 아니에요 · 모든 수치는 입력값 기반 추정이에요</p>
    </main>
  );
}
