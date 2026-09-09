// 기록 확인 풀스크린 — 토스뱅크 "쏙!" 문법. 숫자 하나(파이어가 얼마나 가까워졌나) + 스트릭 + 하나 더.
import { useEffect } from 'react';
import { Button, ProgressBar } from '../../ui/index.js';
import { formatWon } from '../../firemap-v2/formatters.js';

const MILESTONES = [3, 7, 14, 21, 30, 60, 100];

export default function ConfirmScreen({ amount, label, adv, streak = 0, onClose, onMore, onCert }) {
  useEffect(() => {
    const h = (e) => { if (e.key === 'Escape') onClose(); };
    window.addEventListener('keydown', h);
    return () => window.removeEventListener('keydown', h);
  }, [onClose]);
  const next = MILESTONES.find((m) => m > streak) || null;
  const prev = [...MILESTONES].reverse().find((m) => m <= streak) || 0;
  const hit = MILESTONES.includes(streak);
  const pct = next ? ((streak - prev) / (next - prev)) * 100 : 100;
  return (
    <div className="ds-confirm" role="dialog" aria-modal="true" aria-label="기록 완료">
      <div className="ds-confirm__emoji" aria-hidden="true">{hit ? '🏅' : '🔥'}</div>
      <h2 className="ds-confirm__title">{adv ? <>파이어가 <b>{adv}</b> 가까워졌어요</> : <>{formatWon(amount)} 기록했어요</>}</h2>
      <p className="ds-confirm__sub">{label} +{formatWon(amount)}{hit ? ` · ${streak}일 연속 달성 배지를 받았어요!` : ''}</p>
      <div className="ds-card ds-card--dark ds-confirm__card" style={{ background: 'rgba(255,255,255,.08)', borderColor: 'rgba(255,255,255,.14)' }}>
        <div className="ds-row" style={{ justifyContent: 'space-between', marginBottom: 8 }}>
          <span className="ds-caption">🔥 {streak}일째</span>
          {next && <span className="ds-caption">다음 배지 {next}일</span>}
        </div>
        <ProgressBar value={pct} max={100} thin />
      </div>
      <div className="ds-confirm__actions">
        <Button variant="primary" size="lg" onClick={onMore}>하나 더 기록</Button>
        {hit && <Button variant="tint" size="md" onClick={onCert}>🪪 인증 카드 만들기</Button>}
        <Button variant="secondary" size="md" onClick={onClose}>확인</Button>
      </div>
    </div>
  );
}
