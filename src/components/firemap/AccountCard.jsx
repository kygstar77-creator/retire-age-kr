import { useState } from 'react';
import { account } from '../../utils/identity.js';
import { signup, login, logout, setHandle, deleteAccount } from '../../utils/firemapAccountApi.js';
import { syncAfterAuth, claimDevice, logoutClearLocal, clearLocalOnly } from '../../utils/firemapStateApi.js';
import { kakaoLoginStart } from '../../utils/kakaoAuth.js';

function mapErr(code, msg) {
  const m = code || msg || '';
  if (m.includes('handle_taken')) return '이미 쓰는 닉네임이에요. 다른 걸로 해주세요.';
  if (m.includes('handle_length')) return '닉네임은 2~16자로 해주세요.';
  if (m.includes('password_short')) return '비밀번호는 4자 이상으로 해주세요.';
  if (m.includes('bad_credentials')) return '닉네임 또는 비밀번호가 올바르지 않아요.';
  return '잠시 후 다시 시도해주세요.';
}

export default function AccountCard({ kicker, sub, compact } = {}) {
  const acc = account();
  const [mode, setMode] = useState('login');
  const [open, setOpen] = useState(!compact);
  const [h, setH] = useState('');
  const [pw, setPw] = useState('');
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState('');
  const [editing, setEditing] = useState(false);
  const [nh, setNh] = useState('');
  const [wd, setWd] = useState(false);
  const [wbusy, setWbusy] = useState(false);

  if (acc && acc.handle) {
    const saveNick = async () => {
      setErr('');
      const v = nh.trim();
      if (v.length < 2) { setErr('닉네임은 2자 이상으로 해주세요.'); return; }
      setBusy(true);
      try { await setHandle(v); window.location.reload(); }
      catch (e) { setErr(mapErr(e && e.code, e && e.message)); setBusy(false); }
    };
    const doWithdraw = async () => {
      setErr('');
      setWbusy(true);
      try {
        await deleteAccount();
        clearLocalOnly();
        window.location.href = '/';
      } catch (e) { setErr('탈퇴 처리 중 문제가 생겼어요. 잠시 후 다시 시도해주세요.'); setWbusy(false); }
    };
    return (
      <section className="fm-card fm-acct">
        <p className="fm-kicker">내 계정</p>
        {wd ? (
          <>
            <p className="fm-acct-who"><b>정말 탈퇴할까요?</b> 되돌릴 수 없어요.</p>
            <p className="fm-acct-sub">탈퇴하면 <b>닉네임·비밀번호·카카오 연결 등 개인정보는 즉시 파기</b>돼요. 이미 남긴 커뮤니티 글·랭킹 점수는 작성자 정보를 지우고 <b>‘(탈퇴한 회원)’</b>으로 익명 처리돼 남을 수 있어요(통계 유지). 기기에 저장된 내 기록도 함께 삭제돼요.</p>
            {err && <p className="fm-acct-err">{err}</p>}
            <button type="button" className="fm-acct-go" style={{ background: '#dc2626' }} onClick={doWithdraw} disabled={wbusy}>{wbusy ? '탈퇴 처리 중…' : '탈퇴 확정하기'}</button>
            <button type="button" className="fm-acct-switch" onClick={() => { setWd(false); setErr(''); }}>취소</button>
          </>
        ) : !editing ? (
          <>
            <p className="fm-acct-who"><b>{acc.handle}</b>으로 로그인됨 · 랭킹·저축 보드에 이 닉네임이 표시돼요.</p>
            <button type="button" className="fm-acct-go" onClick={() => { setNh(acc.handle); setEditing(true); setErr(''); }}>✏️ 닉네임 변경</button>
            <button type="button" className="fm-acct-switch" onClick={async () => { await logoutClearLocal(); window.location.reload(); }}>로그아웃</button>
            <button type="button" className="fm-acct-withdraw" style={{ display: 'block', margin: '10px auto 0', background: 'transparent', border: 'none', color: '#9ca3af', fontSize: '12px', textDecoration: 'underline', cursor: 'pointer' }} onClick={() => { setWd(true); setErr(''); }}>회원 탈퇴</button>
          </>
        ) : (
          <>
            <p className="fm-acct-sub">랭킹·저축 보드에 표시될 닉네임이에요. (2~16자)</p>
            <input className="fm-acct-in" maxLength={16} placeholder="새 닉네임" value={nh} onChange={(e) => setNh(e.target.value)} onKeyDown={(e) => { if (e.key === 'Enter') saveNick(); }} />
            {err && <p className="fm-acct-err">{err}</p>}
            <button type="button" className="fm-acct-go" onClick={saveNick} disabled={busy}>{busy ? '저장 중…' : '저장'}</button>
            <button type="button" className="fm-acct-switch" onClick={() => { setEditing(false); setErr(''); }}>취소</button>
          </>
        )}
      </section>
    );
  }

  if (compact && !open) {
    return (
      <section className="fm-card fm-acct">
        <p className="fm-kicker">{kicker || '내 계정 (선택)'}</p>
        <p className="fm-acct-sub">{sub || '닉네임만 정하면 기기를 바꾸거나 브라우저를 지워도 내 기록이 그대로 이어져요.'}</p>
        <button type="button" className="fm-acct-go" onClick={() => setOpen(true)}>🔒 로그인 · 계정 만들기</button>
      </section>
    );
  }

  const kakao = async () => {
    setErr('');
    setBusy(true);
    try { await kakaoLoginStart(); } // 카카오로 리다이렉트 → 복귀 시 FireMapMVP가 처리
    catch (e) { setErr('카카오 로그인을 시작할 수 없어요. 잠시 후 다시 시도해주세요.'); setBusy(false); }
  };

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
      <p className="fm-acct-sub">{sub || '카카오로 3초 만에 시작하거나, 닉네임+비밀번호로 만들 수 있어요. 기기가 바뀌거나 브라우저를 지워도 내 글·저축·랭킹이 그대로 이어져요.'}</p>
      <button type="button" className="fm-acct-kakao" onClick={kakao} disabled={busy}>
        <span className="fm-acct-kakao-ico" aria-hidden="true">💬</span> 카카오로 시작하기
      </button>
      <div className="fm-acct-or"><span>또는 닉네임으로</span></div>
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
