// 이용 안내·면책 동의 — 첫 결과를 저장하는 시점(결과 화면 첫 진입)에만 Sheet로. 랜딩·홈에서는 안 뜬다.
import { useState } from 'react';
import { Sheet, Button } from '../../ui/index.js';
import { prefs } from '../../utils/prefs.js';

export default function ConsentSheet({ when = true }) {
  const [done, setDone] = useState(() => prefs.consent());
  if (done || !when) return null;
  const accept = () => { prefs.setConsent(); setDone(true); };
  return (
    <Sheet open title="시작하기 전에">
      <p className="ds-p">파이어맵은 입력값을 기계적으로 계산하는 <b>참고용 시뮬레이션 도구</b>예요. 투자·세무 자문이나 특정 상품 권유가 아니며, 실제 세금·건강보험료·연금은 제도와 개인 상황에 따라 달라질 수 있어요.</p>
      <p className="ds-caption" style={{ margin: '10px 0 0' }}>입력값은 기기에서 계산돼요. 이름·연락처·계좌번호는 받지 않아요. 랭킹엔 자산 원금이 아닌 익명 점수(자산은 구간만)가 쓰여요. <a className="ds-link" href="/privacy.html">개인정보처리방침</a></p>
      <Button variant="primary" size="lg" full className="ds-mt-4" onClick={accept}>이해했어요</Button>
    </Sheet>
  );
}
