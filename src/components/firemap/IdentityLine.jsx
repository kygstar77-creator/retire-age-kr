import { account } from '../../utils/identity.js';
import { logout } from '../../utils/firemapAccountApi.js';

// 닉네임은 '계정'으로만 정함. 로그인 시 핸들 고정 표시, 비로그인 시 계정 만들기 유도.
export default function IdentityLine({ onMove }) {
  const acc = account();
  if (acc && acc.handle) {
    return (
      <div className="fm-idline">
        <span>내 닉네임 <b>{acc.handle}</b> · 계정 연결됨</span>
        <button type="button" className="fm-idline-link" onClick={() => { logout(); window.location.reload(); }}>로그아웃</button>
      </div>
    );
  }
  return (
    <div className="fm-idline">
      <span>닉네임 만들고 기록 지키기</span>
      <button type="button" className="fm-idline-cta" onClick={() => onMove && onMove('account')}>로그인 →</button>
    </div>
  );
}
