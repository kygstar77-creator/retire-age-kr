import Header from './Header.jsx';
import { account } from '../../utils/identity.js';
import { track } from '../../firemap-v2/dailyData.js';
import { CAFE_URL, YOUTUBE_URL } from '../../firemap-v2/links.js';
import { Card, ListGroup, ListRow } from '../../ui/index.js';

// 전체(토스식) — 파이어 여정 단계별로 모든 기능을 한 목록에 정리. DS v1: ListGroup/ListRow (인라인 스타일 0)
const SECTIONS = [
  {
    label: '① 내 여정',
    items: [
      { ico: '🧭', title: '내 파이어 여정', desc: '지금 단계 · 다음 한 걸음 · 진도', to: 'journey' },
      { ico: '🎯', title: '내 파이어 플랜', desc: '목표까지 매달·하루 얼마', to: 'firePlan' },
      { ico: '📊', title: '내 파이어 결과', desc: '파이어 가능 나이 · 자산 추이', to: 'result' },
      { ico: '🇰🇷', title: '대한민국 파이어 지수', desc: '연령대별 현황 · 또래 중 내 위치', to: 'index' }
    ]
  },
  {
    label: '② 실행·가속 (기록)',
    items: [
      { ico: '💰', title: '저축·기록', desc: '저축·오늘의 한 걸음·미션 한 곳에', to: 'save' }
    ]
  },
  {
    label: '③ 또래 속 나',
    items: [
      { ico: '🏆', title: 'FIRE 랭킹 · 파이어 지수', desc: '여정 단계별 경쟁 · 또래 중 내 위치', to: 'ranking' },
      { ico: '💬', title: '방명록 전체 보기', desc: '실시간 한마디는 홈의 💬 버튼 · 여기선 전체 글·답글', to: 'community' }
    ]
  },
  {
    label: '설계 도구',
    items: [
      { ico: '🧭', title: '파이어 유형 테스트 ✨', desc: '12문항으로 내 파이어족 유형 + 살 도시 Top3 (공유)', to: 'firetype' },
      { ico: '🎛️', title: '조건 바꿔 비교', desc: '저축·수익률·은퇴나이 What-If', to: 'experiment' }
    ]
  },
  {
    label: '🗺️ 지역으로 파이어 보기',
    items: [
      { ico: '🗺️', title: '지역으로 파이어 보기', desc: '국내·해외 도시 비교 + 생활비·집값·필요자산 자료까지 한 곳에', to: 'cities' }
    ]
  },
  {
    label: '임박·파이어 — 리얼리티 체크',
    items: [
      { ico: '🩺', title: '파이어 후 건보료', desc: '피부양자 자격 + 지역가입 보험료', to: 'dependent' },
      { ico: '🧾', title: '양도·배당세', desc: '해외주식 양도세 + 배당 소득세', to: 'foreignTax' },
      { ico: '💵', title: '파이어 후 현금흐름', desc: '배당·인출·세금·건보까지', to: 'dividend' },
      { ico: '🏦', title: '국민연금 조기수령', desc: '당겨 받기 득실', to: 'pension' }
    ]
  }
];

const LINKS = [
  { ico: '🟢', title: '파이어맵 네이버 카페', desc: '파이어 인증·질문·후기 — 파이어족 커뮤니티 본진', href: CAFE_URL, ext: true },
  { ico: '▶️', title: '파이어맵 유튜브', desc: '영상으로 보는 파이어 — 채널 구독하기', href: YOUTUBE_URL, ext: true },
  { ico: '📚', title: '파이어 백과', desc: '건보료·세금·연금·현실 금액 가이드', href: '/guide/' },
  { ico: '📄', title: '면책 안내', desc: '정보 제공 목적 · 투자자문 아님', href: '/disclaimer.html' },
  { ico: '🔒', title: '개인정보처리방침', desc: '수집 항목 · 목적 · 보관', href: '/privacy.html' },
  { ico: '✉️', title: '문의', desc: '의견·제보 보내기', href: '/contact.html' }
];

export default function MenuAll({ onMove }) {
  const acc = account();
  const go = (to) => { try { track('menu_all', { to }); } catch { /* ignore */ } onMove(to); };

  return (
    <main className="fm-screen fm-scroll fm-has-tabbar">
      <Header tag="전체" />

      <Card variant="hero" as="div" className="ds-card--flat" style={{ marginBottom: 18, padding: 0, overflow: 'hidden' }}>
        <ListRow
          lead={acc && acc.handle ? '👤' : '🔒'}
          title={acc && acc.handle ? acc.handle : '카카오로 간편·안전 로그인'}
          desc={acc && acc.handle ? '기록이 안전하게 이어져요' : '내 기록을 안전하게 보관 · 기기 바꿔도 그대로'}
          trail={acc && acc.handle ? '관리' : '로그인'}
          accent
          size="L"
          onClick={() => go('account')}
        />
      </Card>

      <div className="ds-stack" style={{ gap: 20 }}>
        {SECTIONS.map((sec) => (
          <ListGroup key={sec.label} label={sec.label}>
            {sec.items.map((it) => (
              <ListRow key={it.title} lead={it.ico} title={it.title} desc={it.desc} onClick={() => go(it.to)} />
            ))}
          </ListGroup>
        ))}
        <ListGroup label="정보 · 정책">
          {LINKS.map((it) => (
            <ListRow key={it.title} lead={it.ico} title={it.title} desc={it.desc} href={it.href} external={!!it.ext} />
          ))}
        </ListGroup>
      </div>

      <p className="ds-caption" style={{ padding: '14px 8px 0', margin: 0 }}>※ 파이어맵은 정보 제공 서비스이며 투자자문이 아니에요. 모든 수치는 입력값 기반 추정이에요.</p>
    </main>
  );
}
