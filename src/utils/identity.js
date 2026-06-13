// 신원 통합: 로그인(간편계정) 시 계정 user_id, 아니면 기기 고유 ID(fm_cid).
const CID = 'fm_cid';
const ACC = 'fm_account';

export function deviceId() {
  try {
    let id = localStorage.getItem(CID);
    if (!id) {
      id = (window.crypto && crypto.randomUUID) ? crypto.randomUUID() : `${Date.now()}-${Math.random().toString(16).slice(2)}`;
      localStorage.setItem(CID, id);
    }
    return id;
  } catch { return null; }
}

export function account() {
  try { return JSON.parse(localStorage.getItem(ACC) || 'null'); } catch { return null; }
}
export function accountUserId() { const a = account(); return (a && a.userId) || null; }

// 제출/참여에 쓰는 식별자
export function identityId() { return accountUserId() || deviceId(); }

// 소유권 매칭: 계정 user_id + 이 기기 ID(레거시) 모두 내 것으로 인정
export function identityIds() {
  const out = [];
  const a = accountUserId(); if (a) out.push(a);
  try { const c = localStorage.getItem(CID); if (c && !out.includes(c)) out.push(c); } catch { /* ignore */ }
  return out;
}
