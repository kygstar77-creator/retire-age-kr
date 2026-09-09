// 내 계정 — 카카오 · 닉네임+비밀번호. tool() 래퍼 안에서 렌더되므로 TopBar는 여기서 안 그린다.
import { useState } from 'react';
import { Card, SectionHead, Button, Notice, Dialog, BottomCTA } from '../../ui/index.js';
import { account } from '../../utils/identity.js';
import { signup, login, setHandle, deleteAccount } from '../../utils/firemapAccountApi.js';
import { syncAfterAuth, claimDevice, logoutClearLocal, clearLocalOnly } from '../../utils/firemapStateApi.js';
import { kakaoLoginStart } from '../../utils/kakaoAuth.js';
import '../../ui/screens/account.css';

function mapErr(code, msg) {
  const m = code || msg || '';
  if (m.includes('handle_taken')) return '이미 쓰는 닉네임이에요 · 다른 걸로 바꿔봐요';
  if (m.includes('handle_length')) return '닉네임은 2~16자예요';
  if (m.includes('password_short')) return '비밀번호는 4자 이상이에요';
  if (m.includes('bad_credentials')) return '닉네임 또는 비밀번호가 달라요';
  return '잠시 후 다시 해봐요';
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
      if (v.length < 2) { setErr('닉네임은 2자 이상이에요'); return; }
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
      } catch { setErr('탈퇴 처리가 안 됐어요 · 잠시 후 다시 해봐요'); setWbusy(false); setWd(false); }
    };
    return (
      <Card>
        <SectionHead size="sm" kicker="내 계정" title={acc.handle} desc="랭킹·저축 기록에 이 닉네임이 보여요" />
        {err && <Notice tone="bad" className="ds-mt-2">{err}</Notice>}
        {editing ? (
          <>
            <input className="ds-input ds-mt-2" maxLength={16} placeholder="새 닉네임 · 2~16자" value={nh} onChange={(e) => setNh(e.target.value)} onKeyDown={(e) => { if (e.key === 'Enter') saveNick(); }} aria-label="새 닉네임" />
            <BottomCTA secondary={{ label: '취소', onClick: () => { setEditing(false); setErr(''); } }} primary={{ label: '저장', onClick: saveNick, loading: busy }} />
          </>
        ) : (
          <div className="ds-stack ds-mt-2">
            <Button variant="secondary" size="md" full onClick={() => { setNh(acc.handle); setEditing(true); setErr(''); }}>✏️ 닉네임 바꾸기</Button>
            <Button variant="ghost" size="md" full onClick={async () => { await logoutClearLocal(); window.location.reload(); }}>로그아웃</Button>
            <button type="button" className="sc-acct-withdraw" onClick={() => { setWd(true); setErr(''); }}>회원 탈퇴</button>
          </div>
        )}
        <Dialog
          open={wd} title="정말 탈퇴할까요?"
          desc="닉네임·비밀번호·카카오 연결은 바로 지워져요. 남긴 글과 등수는 익명으로 남을 수 있고, 이 기기의 기록도 함께 지워져요."
          primary={{ label: wbusy ? '처리 중…' : '탈퇴하기', variant: 'danger', onClick: () => { if (!wbusy) doWithdraw(); } }}
          secondary={{ label: '취소', onClick: () => setWd(false) }}
          onClose={() => setWd(false)}
        />
      </Card>
    );
  }

  if (compact && !open) {
    return (
      <Card>
        <SectionHead size="sm" kicker={kicker || '내 계정 · 선택'} title="기록을 지켜요" desc={sub || '닉네임만 정하면 기기를 바꿔도 내 기록이 그대로 이어져요'} />
        <Button variant="secondary" size="md" full onClick={() => setOpen(true)}>🔒 로그인 · 계정 만들기</Button>
      </Card>
    );
  }

  const kakao = async () => {
    setErr('');
    setBusy(true);
    try { await kakaoLoginStart(); } // 카카오로 리다이렉트 → 복귀 시 FireMapMVP가 처리
    catch { setErr('카카오 로그인을 시작할 수 없어요 · 잠시 후 다시 해봐요'); setBusy(false); }
  };

  const submit = async () => {
    setErr('');
    const handle = h.trim();
    if (handle.length < 2) { setErr('닉네임은 2자 이상이에요'); return; }
    if (pw.length < 4) { setErr('비밀번호는 4자 이상이에요'); return; }
    setBusy(true);
    try {
      if (mode === 'signup') await signup(handle, pw); else await login(handle, pw);
      await claimDevice();
      await syncAfterAuth();
      window.location.reload();
    } catch (e) { setErr(mapErr(e && e.code, e && e.message)); setBusy(false); }
  };

  return (
    <Card>
      <SectionHead size="sm" kicker={kicker || '내 계정 · 선택'} title={mode === 'signup' ? '계정 만들기' : '로그인'} desc={sub || '카카오로 3초면 돼요 · 기기를 바꿔도 내 글·저축·등수가 이어져요'} />
      <Button variant="secondary" size="lg" full className="sc-acct-kakao" onClick={kakao} disabled={busy}>💬 카카오로 시작하기</Button>
      <div className="sc-acct-or"><span>또는 닉네임으로</span></div>
      <div className="ds-stack">
        <input className="ds-input" maxLength={16} placeholder="닉네임 · 2~16자" value={h} onChange={(e) => setH(e.target.value)} aria-label="닉네임" autoComplete="username" />
        <input className="ds-input" type="password" maxLength={32} placeholder="비밀번호 · 4자 이상" value={pw} onChange={(e) => setPw(e.target.value)} onKeyDown={(e) => { if (e.key === 'Enter') submit(); }} aria-label="비밀번호" autoComplete={mode === 'signup' ? 'new-password' : 'current-password'} />
      </div>
      {err && <Notice tone="bad" className="ds-mt-2">{err}</Notice>}
      <Button variant="primary" size="lg" full className="ds-mt-3" onClick={submit} loading={busy}>{mode === 'signup' ? '계정 만들기' : '로그인'}</Button>
      <Button variant="ghost" size="sm" full className="ds-mt-2" onClick={() => { setMode(mode === 'signup' ? 'login' : 'signup'); setErr(''); }}>
        {mode === 'signup' ? '이미 계정이 있어요 · 로그인' : '처음이에요 · 계정 만들기'}
      </Button>
    </Card>
  );
}
