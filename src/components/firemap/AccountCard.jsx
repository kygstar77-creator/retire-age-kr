import { useState } from 'react';
import { account } from '../../utils/identity.js';
import { signup, login, logout } from '../../utils/firemapAccountApi.js';
import { syncAfterAuth, claimDevice } from '../../utils/firemapStateApi.js';

function mapErr(code, msg) {
  const m = code || msg || '';
  if (m.includes('handle_taken')) return '이미 쓰는 닉네임이에요. 다른 걸로 해주세요.';
  if (m.includes('handle_length')) return '닉네임은 2~16자로 해주세요.';
  if (m.includes('password_short')) return '비밀번호는 4자 이상으로 해주세요.';
  if (m.includes('bad_credentials')) return '닉네임 또는 비밀번호가 올바르지 않아요.';
  return '잠시 후 다시 시도해주세요.';
}

export default function AccountCard({ kicker, sub } = {}) {
  const acc = account();
  const [mode, setMode] = useState('login');
  const [h, setH] = useState('');
  const [pw, setPw] = useState('');
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState('');

  if (acc && acc.handle) {
    return (
      <section className="fm-card fm-acct">
        <p className="fm-kicker">내 계정</p>
        <p className="fm-acct-who"><b>{acc.handle}</b>으로 로그인됨 · 기기가 바뀌어도 내 글·적립·랭킹이 이어져요.</p>
        <button type="button" className="fm-acct-switch" onClick={() => { logout(); window.location.reload(); }}>로그아웃</button>
      </section>
    );
  }

  const submit = async () => {
    setErr('');
    const handle = h.trim();
    if (handle.length < 2) { setErr('닉네임은 2자 이상으로 해주세요.'); return; }
    if (pw.length < 4) { setErr('비밀번호는 4자 이상으로 해주세요.'); return; }
    setBusy(true);
    try {
      if (mode === 'signup') await signup(handle, pw); else await login(handle, pw);
      await claimDevice();
      await syncAfterAuth();
      window.location.reload();
    } catch (e) { setErr(mapErr(e && e.code, e && e.message)); setBusy(false); }
  };

  return (
    <section className="fm-card fm-acct">
      <p className="fm-kicker">{kicker || '내 계정 (선택)'}</p>
      <h2>{mode === 'signup' ? '계정 만들기' : '로그인'}</h2>
      <p className="fm-acct-sub">{sub || '닉네임+비밀번호만 정하면, 기기가 바뀌거나 브라우저를 지워도 내 글·적립·랭킹이 그대로 이어져요. 이메일·가입절차 없어요.'}</p>
      <input className="fm-acct-in" maxLength={16} placeholder="닉네임 (2~16자)" value={h} onChange={(e) => setH(e.target.value)} />
      <input className="fm-acct-in" type="password" maxLength={32} placeholder="비밀번호 (4자 이상)" value={pw} onChange={(e) => setPw(e.target.value)} onKeyDown={(e) => { if (e.key === 'Enter') submit(); }} />
      {err && <p className="fm-acct-err">{err}</p>}
      <button type="button" className="fm-acct-go" onClick={submit} disabled={busy}>{busy ? '처리 중…' : (mode === 'signup' ? '계정 만들기' : '로그인')}</button>
      <button type="button" className="fm-acct-switch" onClick={() => { setMode(mode === 'signup' ? 'login' : 'signup'); setErr(''); }}>
        {mode === 'signup' ? '이미 계정이 있어요 — 로그인' : '처음이에요 — 계정 만들기'}
      </button>
    </section>
  );
}
