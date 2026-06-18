import Header from './Header.jsx';
import { account } from '../../utils/identity.js';
import { track } from '../../firemap-v2/dailyData.js';

// 전체(토스식) — 파이어 여정 단계별로 모든 기능을 한 목록에 정리.
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
      { ico: '💬', title: '커뮤니티', desc: '단계별 그룹 · 익명 한마디·후기', to: 'community' }
    ]
  },
  {
    label: '설계 도구',
    items: [
      { ico: '🎛️', title: '조건 바꿔 비교', desc: '저축·수익률·은퇴나이 What-If', to: 'experiment' },
      { ico: '📍', title: '지역별 파이어 — 내 조건으로 비교', desc: '내 입력값 기준, 도시를 옮기면 파이어가 몇 년 당겨지는지', to: 'cities' }
    ]
  },
  {
    label: '지역으로 보는 파이어 (자료·플랜)',
    items: [
      { ico: '🏘️', title: '지역·가구별 파이어 플랜', desc: '지역×가구형태×유형별 필요자산·저축 — 사례처럼 찾아보기', href: '/guide/region-plan/' },
      { ico: '🏙️', title: '도시별 생활비·집값 백과', desc: '도시별 생활비·아파트 실거래가·물가 사전', href: '/guide/regions/' }
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

      <button type="button" style={S.acct} onClick={() => go('account')}>
        <span style={S.acctIco}>{acc && acc.handle ? '👤' : '🔒'}</span>
        <span style={S.acctTx}>
          {acc && acc.handle
            ? <><b style={S.acctName}>{acc.handle}</b><em style={S.acctSub}>기록이 안전하게 이어져요</em></>
            : <><b style={S.acctName}>🔒 카카오로 간편·안전 로그인</b><em style={S.acctSub}>내 기록을 안전하게 보관 · 기기 바꿔도 그대로</em></>}
        </span>
        <span style={S.acctGo}>{acc && acc.handle ? '관리 ›' : '로그인 ›'}</span>
      </button>

      {SECTIONS.map((sec) => (
        <div key={sec.label} style={S.section}>
          <p style={S.secLabel}>{sec.label}</p>
          <div style={S.list}>
            {sec.items.map((it) => (it.href
              ? (
                <a key={it.title} href={it.href} style={S.row}>
                  <span style={S.rowIco}>{it.ico}</span>
                  <span style={S.rowTx}><b style={S.rowTitle}>{it.title}</b><em style={S.rowDesc}>{it.desc}</em></span>
                  <span style={S.rowGo}>›</span>
                </a>
              )
              : (
                <button type="button" key={it.title} style={S.row} onClick={() => go(it.to)}>
                  <span style={S.rowIco}>{it.ico}</span>
                  <span style={S.rowTx}><b style={S.rowTitle}>{it.title}</b><em style={S.rowDesc}>{it.desc}</em></span>
                  <span style={S.rowGo}>›</span>
                </button>
              )
            ))}
          </div>
        </div>
      ))}

      <div style={S.section}>
        <p style={S.secLabel}>정보 · 정책</p>
        <div style={S.list}>
          {LINKS.map((it) => (
            <a key={it.title} href={it.href} style={S.row}>
              <span style={S.rowIco}>{it.ico}</span>
              <span style={S.rowTx}><b style={S.rowTitle}>{it.title}</b><em style={S.rowDesc}>{it.desc}</em></span>
              <span style={S.rowGo}>›</span>
            </a>
          ))}
        </div>
      </div>

      <p style={S.foot}>※ 파이어맵은 정보 제공 서비스이며 투자자문이 아니에요. 모든 수치는 입력값 기반 추정이에요.</p>
    </main>
  );
}

const S = {
  acct: { display: 'flex', alignItems: 'center', gap: 11, width: '100%', textAlign: 'left', cursor: 'pointer', background: 'linear-gradient(180deg,#fff6f2,#fff)', border: '1px solid rgba(255,90,0,0.22)', borderRadius: 16, padding: '14px 15px', marginBottom: 18 },
  acctIco: { fontSize: 22, flex: '0 0 auto' },
  acctTx: { display: 'flex', flexDirection: 'column', flex: 1, minWidth: 0, gap: 2 },
  acctName: { fontSize: 14, fontWeight: 800, color: '#15151b' },
  acctSub: { fontSize: 11.5, fontWeight: 500, color: '#8a8f99', fontStyle: 'normal' },
  acctGo: { fontSize: 12.5, fontWeight: 800, color: '#ff5a00', flex: '0 0 auto' },
  section: { marginBottom: 20 },
  secLabel: { fontSize: 12, fontWeight: 800, color: '#9aa3bf', letterSpacing: '0.01em', margin: '0 0 9px 4px' },
  list: { background: '#fff', border: '1px solid #ececec', borderRadius: 16, overflow: 'hidden' },
  row: { display: 'flex', alignItems: 'center', gap: 12, width: '100%', textAlign: 'left', cursor: 'pointer', background: 'none', border: 0, borderBottom: '1px solid #f3f1ee', padding: '13px 14px', textDecoration: 'none' },
  rowIco: { fontSize: 19, flex: '0 0 auto', width: 24, textAlign: 'center' },
  rowTx: { display: 'flex', flexDirection: 'column', flex: 1, minWidth: 0, gap: 2 },
  rowTitle: { fontSize: 14, fontWeight: 700, color: '#15151b', lineHeight: 1.3 },
  rowDesc: { fontSize: 11.5, fontWeight: 500, color: '#8a8f99', fontStyle: 'normal', lineHeight: 1.4 },
  rowGo: { fontSize: 18, color: '#c2c7d0', fontWeight: 700, flex: '0 0 auto' },
  foot: { fontSize: 10.5, color: '#9aa3bf', lineHeight: 1.6, padding: '4px 8px 0', margin: 0 }
};
