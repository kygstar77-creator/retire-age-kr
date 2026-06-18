import { useState } from 'react';

const KEY = 'fm_consent_v1';

export default function Consent() {
  const [done, setDone] = useState(() => {
    try { return localStorage.getItem(KEY) === '1'; } catch { return false; }
  });
  if (done) return null;
  const accept = () => {
    try { localStorage.setItem(KEY, '1'); } catch { /* ignore */ }
    setDone(true);
  };
  return (
    <div className="fm-consent-layer" role="dialog" aria-modal="true" aria-label="이용 안내 및 면책 동의">
      <div className="fm-consent-sheet">
        <strong>시작하기 전에</strong>
        <p>파이어맵은 입력값을 기계적으로 계산하는 <b>참고용 시뮬레이션 도구</b>예요. 투자·세무 자문이나 특정 상품 권유가 아니며, 실제 세금·건강보험료·연금은 제도와 개인 상황에 따라 달라질 수 있어요. 자산 처분·파이어 결정 전에는 전문가 상담을 권장해요.</p>
        <p className="fm-consent-privacy">입력값은 기기에서 계산되고, 로그인하면 기기 간 이어쓰기를 위해 계정에 연결해 안전하게 보관돼요. 이름·연락처·계좌번호는 받지 않고, 등수에는 개인 금액이 아닌 익명 점수만 쓰여요. <a href="/privacy.html">개인정보처리방침</a></p>
        <button type="button" onClick={accept}>이해했어요</button>
      </div>
    </div>
  );
}
